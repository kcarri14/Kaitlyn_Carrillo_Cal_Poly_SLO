import { Item } from "@prisma/client";
import levenshtein from "string-comparison";

const REQUIRED_MATCH_SCORE: number = 14;

/**Returns string-similarity score between two given strings*/
function getStringSimilarityScore(stringOne: string, stringTwo: string) {
  return levenshtein.levenshtein.similarity(stringOne, stringTwo);
}

/**Returns a score representing matching strength between two items */
function getMatchScore(itemOne: Item, itemTwo: Item) {
  if (itemOne.isLost == itemTwo.isLost) {
    return 0;
  }

  let score = 0;

  //Name
  score += getStringSimilarityScore(itemOne.name, itemTwo.name) * 10;

  //Location
  score += itemOne.location == itemTwo.location ? 2 : 0;

  //Event
  score +=
    itemOne.event != null && itemTwo.event != null
      ? getStringSimilarityScore(itemOne.event, itemTwo.event) * 5
      : 0;

  //Tags
  itemOne.tags.forEach((item) => {
    if (itemTwo.tags.includes(item)) {
      score += 3;
    }
  });

  return score;
}

export async function MatchItem(newItem: Item) {
  console.log("MATCHING INIT");

  //Update found/lost matches for both items matched
  const response = await fetch(`http://localhost:3000/api/Item`, {
    headers: {
      "Content-type": "application/json",
    },
  });
  const text = await response.text();
  console.log("RESPONSE TEXT:\n " + text);
  const data = JSON.parse(text);
  console.log(data.items);
  data.items.forEach(async (item: Item) => {
    const matchScore = getMatchScore(newItem, item);

    if (matchScore < REQUIRED_MATCH_SCORE) {
      return null;
    }

    //Update Item Matches
    const response = await fetch(`/api/Item/${newItem.id}`, {
      method: "PUT",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(item),
    });

    const responseData = await response.json();
    console.log(responseData);
    return responseData;
  });
  console.log("MATCHING END");
}
