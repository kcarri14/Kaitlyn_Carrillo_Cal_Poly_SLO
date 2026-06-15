from keras.datasets import mnist
from keras import models 
from keras import layers
from keras.utils import to_categorical
import os, glob, numpy as np
from PIL import Image, ImageOps
from keras.models import load_model

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

MODEL_PATH = "mnist_dense.keras" 
IMAGE_FOLDER = "/Users/kaitlyncarrillo/CSC 480/Lab 7/my_digits" 

network = models.Sequential()
network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,))) 
network.add(layers.Dense(10, activation='softmax'))

network.compile(optimizer='rmsprop',
loss='categorical_crossentropy',
metrics=['accuracy'])

train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255
test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255


train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)


network.fit(train_images, train_labels, epochs=5, batch_size=128)
test_loss, test_acc = network.evaluate(test_images, test_labels)
print('test_acc:', test_acc)

network.save("mnist_dense.keras")

def preprocess_image(path):
    img = Image.open(path).convert("L")         
    img = ImageOps.autocontrast(img)             
    w, h = img.size
    side = max(w, h)
    canvas = Image.new("L", (side, side), color=255)  
    canvas.paste(img, ((side - w)//2, (side - h)//2))
    img = canvas.resize((28, 28), Image.Resampling.LANCZOS)

    arr = np.array(img).astype("float32") / 255.0     
    if arr.mean() > 0.5:
        arr = 1.0 - arr

    arr = arr.reshape(1, 28*28)  
    return arr

def main():
    if not os.path.exists(MODEL_PATH):
        raise SystemExit(f"Model not found: {MODEL_PATH}. Train and save it first.")

    model = load_model(MODEL_PATH)
    paths = sorted(glob.glob(os.path.join(IMAGE_FOLDER, "*.*")))
    if not paths:
        print(f"No images found in '{IMAGE_FOLDER}'. Add PNG/JPG digit photos and re-run.")
        return

    for p in paths:
        x = preprocess_image(p)
        probs = model.predict(x, verbose=0)[0]
        pred = int(np.argmax(probs))
        conf = float(np.max(probs))
        print(f"{os.path.basename(p)} -> {pred} (p={conf:.3f})")

if __name__ == "__main__":
    main()
