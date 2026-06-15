"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import SideBarItem from "../sidebarItem";
import { Item } from "@prisma/client";
import { useAuth } from "@clerk/clerk-react";

export default function QuerySearch(props: { onlyUserPosts: boolean}) {
  const searchParams = useSearchParams();
  const query = searchParams.get("query") || "";
  const [items, setItems] = useState<Item[]>([]);
  const [filteredItems, setFilteredItems] = useState<Item[]>([]);

  const { userId } = useAuth();
  const [ownerId, setOwnerId] =useState<number | null>(null); 

  console.log("bool: " + props.onlyUserPosts);

  useEffect(() => {
    const fetchOwnerId = async () => {
      try {
        const response = await fetch(`/api/Account/?clerkId=${userId}`);
        const data = await response.json();
  
        
        
        if (data) {
          const owner = data.accounts.find((account: { clerkId: string }) => account.clerkId === userId); 
          setOwnerId(owner.id);  
        } else {
          console.error("Owner ID not found.");
        }
      } catch (error) {
        console.error("Error fetching ownerId:", error);
      }
    };
    if (userId){
      fetchOwnerId();
    }
      
  }, [userId]);

  // Fetch items from API
  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await fetch(`/api/Item?query=${query}`);
        const text = await response.text(); // Read raw response
        //console.log("API Response:", text);
        const data = JSON.parse(text); // Convert to JSON
        setItems(data.items || []);
      } catch (error) {
        console.error("Error fetching items:", error);
      }
    };

    fetchItems();
  }, [query]);

  // Filter items based on search query across multiple fields
  useEffect(() => {
    const lowerCaseQuery = query.toLowerCase();

    const matchesQuery = (item: Item) =>
      item.name.toLowerCase().includes(lowerCaseQuery) ||
      item.event?.toLowerCase().includes(lowerCaseQuery) ||
      item.description.toLowerCase().includes(lowerCaseQuery) ||
      item.tags.some((tag) => tag.toLowerCase().includes(lowerCaseQuery));

    if(props.onlyUserPosts){
      items.filter((item:Item) => item.ownerId == ownerId);
    }
    setFilteredItems(items
      .filter((item) => item.isLost)
      .filter(matchesQuery)
      .filter((item) => 
        (props.onlyUserPosts ? item.ownerId == ownerId : true)
      ));
  }, [items, query, ownerId, props.onlyUserPosts]);

  console.log("FINAL: " + filteredItems);

  return (
    <div>
      {filteredItems.length === 0 ? (
        <p>{props.onlyUserPosts ? "You have not posted anything" : "No matching items found" }</p>
      ) : (
        <div className="test">
          {filteredItems.map((item) => (
            <SideBarItem
              key={item.id}
              sidebarType="Post"
              {...item}
              date={new Date(item.date)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
