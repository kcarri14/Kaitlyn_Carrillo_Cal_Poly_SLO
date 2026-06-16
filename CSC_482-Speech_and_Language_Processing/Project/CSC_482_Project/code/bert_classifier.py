import re
import json
import random
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    get_linear_schedule_with_warmup
)
from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold
from sklearn.metrics import accuracy_score, classification_report, f1_score


LABELS = {
    "parent": 0,
    "child": 1,
    "spouse": 2,
    "sibling": 3
}
ID2LABEL = {v: k for k, v in LABELS.items()}

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_data(data_file):
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)


class RelationDataset(Dataset):
    def __init__(self, df, tokenizer, max_len=128):
        self.df = df.reset_index(drop=True)
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        encoding = self.tokenizer(
            row["input_text"],
            max_length=self.max_len,
            truncation=True,
            padding="max_length",
            return_attention_mask=True,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(row["label"], dtype=torch.long)
        }


def compute_class_weights(train_df, device):
    counts = train_df["label"].value_counts().sort_index()
    counts = counts.reindex(range(len(LABELS)), fill_value=1)
    weights = 1.0 / torch.tensor(counts.values, dtype=torch.float)
    weights = weights / weights.sum() * len(weights)
    return weights.to(device)


def train_epoch(model, data_loader, optimizer, scheduler, device, criterion):
    model.train()
    losses, preds_all, labels_all = [], [], []

    for batch in data_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        loss = criterion(logits, labels)

        loss.backward()
        optimizer.step()
        scheduler.step()

        preds = torch.argmax(logits, dim=1)
        losses.append(loss.item())
        preds_all.extend(preds.detach().cpu().numpy())
        labels_all.extend(labels.detach().cpu().numpy())

    acc = accuracy_score(labels_all, preds_all)
    macro_f1 = f1_score(labels_all, preds_all, average="macro")
    return np.mean(losses), acc, macro_f1


def eval_model(model, data_loader, device, criterion):
    model.eval()
    losses, preds_all, labels_all = [], [], []

    with torch.no_grad():
        for batch in data_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            loss = criterion(logits, labels)

            preds = torch.argmax(logits, dim=1)
            losses.append(loss.item())
            preds_all.extend(preds.detach().cpu().numpy())
            labels_all.extend(labels.detach().cpu().numpy())

    acc = accuracy_score(labels_all, preds_all)
    macro_f1 = f1_score(labels_all, preds_all, average="macro")
    report = classification_report(
        labels_all,
        preds_all,
        target_names=[ID2LABEL[i] for i in range(len(ID2LABEL))],
        digits=4
    )
    return np.mean(losses), acc, macro_f1, report, labels_all, preds_all


def make_loaders(train_df, val_df, tokenizer, batch_size=16, max_len=128):
    train_ds = RelationDataset(train_df, tokenizer, max_len=max_len)
    val_ds = RelationDataset(val_df, tokenizer, max_len=max_len)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader


def build_model(model_name):
    model = BertForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(LABELS),
        id2label=ID2LABEL,
        label2id=LABELS
    )
    return model


def train_one_split(
    train_df,
    val_df,
    model_name,
    device,
    epochs=3,
    batch_size=16,
    max_len=128,
    lr=2e-5
):
    tokenizer = BertTokenizer.from_pretrained(model_name)
    tokenizer.add_special_tokens({
        "additional_special_tokens": [
            "[PERSON]", "[/PERSON]", "[RELATIVE]", "[/RELATIVE]"
        ]
    })

    train_loader, val_loader = make_loaders(
        train_df, val_df, tokenizer, batch_size=batch_size, max_len=max_len
    )

    model = build_model(model_name)
    model.resize_token_embeddings(len(tokenizer))
    model.to(device)

    optimizer = AdamW(model.parameters(), lr=lr)
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=total_steps
    )

    class_weights = compute_class_weights(train_df, device)
    criterion = torch.nn.CrossEntropyLoss(weight=class_weights)

    best_f1 = -1
    best_state = None

    for epoch in range(epochs):
        train_loss, train_acc, train_f1 = train_epoch(
            model, train_loader, optimizer, scheduler, device, criterion
        )
        val_loss, val_acc, val_f1, _, _, _ = eval_model(
            model, val_loader, device, criterion
        )

        print(f"Epoch {epoch+1}/{epochs}")
        print(f"  Train loss: {train_loss:.4f} | acc: {train_acc:.4f} | macro-F1: {train_f1:.4f}")
        print(f"  Val   loss: {val_loss:.4f} | acc: {val_acc:.4f} | macro-F1: {val_f1:.4f}")

        if val_f1 > best_f1:
            best_f1 = val_f1
            best_state = {
                "model_state_dict": {k: v.cpu() for k, v in model.state_dict().items()},
                "tokenizer": tokenizer
            }

    model.load_state_dict(best_state["model_state_dict"])
    model.to(device)

    val_loss, val_acc, val_f1, report, y_true, y_pred = eval_model(
        model, val_loader, device, criterion
    )

    return {
        "model": model,
        "tokenizer": best_state["tokenizer"],
        "val_loss": val_loss,
        "val_acc": val_acc,
        "val_f1": val_f1,
        "report": report,
        "y_true": y_true,
        "y_pred": y_pred
    }


def save_model(model, tokenizer, save_dir="chatbot_relation_model"):
    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)
    with open(f"{save_dir}/label_map.json", "w", encoding="utf-8") as f:
        json.dump({"label2id": LABELS, "id2label": ID2LABEL}, f, indent=2)
    print(f"Saved chatbot-ready model to: {save_dir}")


def predict_relation(input_text, model, tokenizer, device, max_len=128):
    if "[PERSON]" not in input_text or "[RELATIVE]" not in input_text:
        raise ValueError("input_text must already contain [PERSON] and [RELATIVE] tags")

    encoding = tokenizer(
        input_text,
        max_length=max_len,
        truncation=True,
        padding=True,
        return_tensors="pt"
    )
    encoding = {k: v.to(device) for k, v in encoding.items()}

    model.eval()
    with torch.no_grad():
        outputs = model(**encoding)
        probs = torch.softmax(outputs.logits, dim=1)
        conf, pred = torch.max(probs, dim=1)

    return ID2LABEL[pred.item()], conf.item()


def main():
    set_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_name = "bert-base-cased"
    n_splits = 5

    df = load_data("wikidata_updated.json")
    df = df.dropna(subset=["input_text"]).copy()
    df = df.drop_duplicates(subset=["text", "person", "relative", "relation"]).copy()
    df["relation"] = df["relation"].replace({
        "father": "parent",
        "mother": "parent",
    })
    df["label"] = df["relation"].map(LABELS)
    df = df.dropna(subset=["label"]).copy()
    df["label"] = df["label"].astype(int)

    df = df.dropna(subset=["label", "input_text"]).copy()
    df["label"] = df["label"].astype(int)

    # sanity checks
    person_tag_rate = df["input_text"].str.contains(r"\[PERSON\]", regex=True).mean()
    relative_tag_rate = df["input_text"].str.contains(r"\[RELATIVE\]", regex=True).mean()
    both_tag_rate = (
        df["input_text"].str.contains(r"\[PERSON\]", regex=True) &
        df["input_text"].str.contains(r"\[RELATIVE\]", regex=True)
    ).mean()

    print("Total rows after filtering:", len(df))
    print("PERSON tag rate:", round(person_tag_rate, 4))
    print("RELATIVE tag rate:", round(relative_tag_rate, 4))
    print("BOTH tag rate:", round(both_tag_rate, 4))
    print(df["relation"].value_counts())

    # Hold out final test set by person
    gss = GroupShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
    train_idx, test_idx = next(gss.split(df, y=df["label"], groups=df["person"]))

    train_df = df.iloc[train_idx].reset_index(drop=True)
    test_df = df.iloc[test_idx].reset_index(drop=True)

    print("train rows:", len(train_df))
    print("test rows:", len(test_df))
    print("shared people:", len(set(train_df["person"]) & set(test_df["person"])))

    sgkf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=42)
    fold_results = []

    for fold, (tr_idx, val_idx) in enumerate(
        sgkf.split(train_df, y=train_df["label"], groups=train_df["person"])
    ):
        print(f"\n========== Fold {fold+1}/{n_splits} ==========")

        fold_train_df = train_df.iloc[tr_idx].reset_index(drop=True)
        fold_val_df = train_df.iloc[val_idx].reset_index(drop=True)

        result = train_one_split(
            fold_train_df,
            fold_val_df,
            model_name=model_name,
            device=device,
            epochs=3,
            batch_size=16,
            max_len=128,
            lr=2e-5
        )

        print(result["report"])
        fold_results.append({
            "fold": fold + 1,
            "val_acc": result["val_acc"],
            "val_f1": result["val_f1"]
        })

    print("\n===== CV summary =====")
    for r in fold_results:
        print(f"Fold {r['fold']}: acc={r['val_acc']:.4f}, macro-F1={r['val_f1']:.4f}")

    print(f"Mean CV accuracy: {np.mean([r['val_acc'] for r in fold_results]):.4f}")
    print(f"Mean CV macro-F1: {np.mean([r['val_f1'] for r in fold_results]):.4f}")

    print("\n===== Final training for chatbot =====")
    final_result = train_one_split(
        train_df,
        test_df,
        model_name=model_name,
        device=device,
        epochs=3,
        batch_size=16,
        max_len=128,
        lr=2e-5
    )

    print("\n===== Held-out test results =====")
    print(f"Test accuracy: {final_result['val_acc']:.4f}")
    print(f"Test macro-F1: {final_result['val_f1']:.4f}")
    print(final_result["report"])

    save_model(
        final_result["model"],
        final_result["tokenizer"],
        save_dir="chatbot_relation_model"
    )


if __name__ == "__main__":
    main()
