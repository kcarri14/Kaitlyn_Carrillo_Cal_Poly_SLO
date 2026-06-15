"use Client";

import { useEffect } from "react";
import { useAuth } from "@clerk/nextjs";

const AuthListener = () => {
  const { userId } = useAuth();

  useEffect(() => {
    const authenticateUser = async () => {
      if(!userId) return;

      try {
        await fetch("/api/authentication", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ userId })
        });

      } catch (error) {
        console.error("Network or API error:", error);
      }
    };
    authenticateUser();
  }, [userId]);

  return null;
};

export default AuthListener;
