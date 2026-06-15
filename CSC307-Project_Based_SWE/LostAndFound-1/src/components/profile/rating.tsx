"use client";

import { useEffect, useState } from "react";
import { CiStar } from "react-icons/ci";
import { FaStar } from "react-icons/fa6";
import { FaRegStarHalfStroke } from "react-icons/fa6";

import "@/styles/rating.css";

type Account = {
  id: string;
  clerkId: string;
  ratings: number[];
};

type RatingProps = {
  clerkId: string;
};

function calculateAverageRating(ratingList: number[]) {
  console.log("calculate average of: " + ratingList);
  if (!ratingList || ratingList.length === 0) return 0;
  const sum = ratingList.reduce((i, cur) => i + cur, 0);
  return sum / ratingList.length;
}

export default function Rating({ clerkId }: RatingProps) {
  const [account, setAccount] = useState<Account | null>(null);
  const [rating, setRating] = useState<number>(0);
  const [hasSubmitted, setHasSubmitted] = useState(false);

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        const response = await fetch("/api/Account/");
        if (!response.ok) throw new Error("Failed to fetch accounts");
        const data = await response.json();
        const matchingAccount = data.accounts.find(
          (account: Account) => account.clerkId === clerkId
        );

        setAccount(matchingAccount ?? null);
      } catch (error) {
        console.error("Error fetching accounts", error);
      }
    };
    fetchAccounts();
  }, [clerkId]);

  const handleStarClick = (index: number) => {
    if (rating === index + 1) {
      setRating(index); // Allow the user to "unselect" a rating
    } else {
      setRating(index + 1); // Set the rating to the clicked star
    }
  };
  const updatedRatings = [...(account?.ratings ?? [])];

  const handleSubmit = async () => {
    if (!account) return;

    try {
      console.log("in the original handle: " + updatedRatings);
      updatedRatings.push(rating);

      const response = await fetch(`/api/Account/${account.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ratings: updatedRatings }),
      });

      if (!response.ok) {
        throw new Error("Failed to submit rating");
      }

      setAccount((prevAccount) =>
        prevAccount ? { ...prevAccount, ratings: updatedRatings } : null
      );
      setHasSubmitted(true); // Set the flag for submission status

      console.log("Updated ratings:", updatedRatings);
    } catch (error) {
      console.error("Error submitting rating", error);
    }
  };

  const handleEditRating = () => {
    setHasSubmitted(false); // Allow the user to edit their rating again
    //setRating(0); // Optionally reset the rating if needed
    updatedRatings.pop();
    console.log("post pop: " + updatedRatings);

    handleForEdit(updatedRatings);
  };

  const handleForEdit = async (updatedRatings: number[]) => {
    if (!account) return;
    try {
      console.log("in the edit handle: " + updatedRatings);
      const response = await fetch(`/api/Account/${account.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ratings: updatedRatings }),
      });

      console.log("account ratings now in edit: " + account.ratings);

      if (!response.ok) {
        throw new Error("Failed to submit rating");
      }

      setAccount((prevAccount) =>
        prevAccount ? { ...prevAccount, ratings: updatedRatings } : null
      );

      console.log("Updated ratings:", updatedRatings);
    } catch (error) {
      console.error("Error submitting rating", error);
    }
  };

  const averageRating = account ? calculateAverageRating(account.ratings) : 0;

  return (
    <div className="giveRating">
      <h1>Give a Rating:</h1>
      <div className="currentContainer">
        <div className="rowForCurrent">
          <div className="currentRating">
            <p>Current Rating: </p>
            <div className="starRating">
              {[...Array(5)].map((_, index) => {
                const fullStar = index < Math.floor(averageRating);
                const halfStar =
                  index < Math.ceil(averageRating) && averageRating % 1 >= 0.5;
                const emptyStar = index >= Math.ceil(averageRating);

                return (
                  <span key={index}>
                    {fullStar ? (
                      <FaStar />
                    ) : halfStar ? (
                      <FaRegStarHalfStroke />
                    ) : (
                      <CiStar />
                    )}
                  </span>
                );
              })}
            </div>
          </div>
        </div>
        <div className="rowForCurrent">
          <p>{account?.ratings.length} Ratings</p>
        </div>
      </div>

      {!hasSubmitted && (
        <div className="stars">
          {[...Array(5)].map((_, index) => {
            const isFilled = index < rating;
            return (
              <span key={index} onClick={() => handleStarClick(index)}>
                {isFilled ? <FaStar /> : <CiStar />}
              </span>
            );
          })}
        </div>
      )}
      {hasSubmitted && (
        <div className="stars-done">
          {[...Array(5)].map((_, index) => {
            const isFilled = index < rating;
            return (
              <span key={index}>{isFilled ? <FaStar /> : <CiStar />}</span>
            );
          })}
        </div>
      )}
      {!hasSubmitted && <button onClick={handleSubmit}>Submit Rating</button>}
      {hasSubmitted && <button onClick={handleEditRating}>Edit Rating</button>}
    </div>
  );
}
