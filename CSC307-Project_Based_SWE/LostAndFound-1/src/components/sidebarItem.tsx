import { useUser } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { createChat } from "@/lib/actions";
import { useEffect, useState } from "react";
import { getLocationName } from "./Map/map.data";
import { Account } from "@prisma/client";

interface ItemProps {
  sidebarType: "Post" | "Chat";
  ownerId: number;
  name: string;
  location: number[];
  date: Date;
  description: string;
}



export default function SideBarItem(props: ItemProps) {
  const [account, setAccount] = useState<Account | null>(null);
  const [userName, setUsername] = useState<string>("");
  {
    /* Identify Account based on OwnerID*/
  }
  const router = useRouter();
  useEffect(() => {
    const fetchAccount = async () => {
      const response = await fetch("/api/Account/");
      if (!response.ok) {
        throw new Error(`Status: ${response.status}`);
      }
      const content = await response.json();
      if(content){
        const foundAccount = content.accounts.find((acc: {id: number}) => acc.id == props.ownerId);
        setAccount(foundAccount);
      }
    };

    fetchAccount().catch(console.error);
  }, [props.ownerId]);

  {
    /*Identify clerk username from Account */
  }
  
  useEffect(() => {
    if(!account){
      return;
    }
    const fetchUser = async () => {
      const response = await fetch(`/api/clerkAccount/?clerkId=${account?.clerkId}`);
      if (!response.ok) {;
        throw new Error(`Status: ${response}`)
      }
      const content = await response.json();
      if(content){
        const user = content.user;
        console.log("CONtENT: " + user.firstName);
        console.log("TTTm: " + user.emailAddresses[0].emailAddress);
        setUsername(`${user.firstName ? user.firstName : user.emailAddresses[0].emailAddress}`)
      } else {
        setUsername("");
      }
    };

    fetchUser().catch(console.error);
  }, [account, props.ownerId]);

  const [collapsed, setCollapsed] = useState<boolean>(true);
  const {user} = useUser();
  const handleItemClick = () => {
    setCollapsed(!collapsed);
  };
  
  const handleContactClick = () => {
    
    // THIS IS THE OWNER OF THE POST
    // user_2teE5f4oyYA3VXldk53KCNsMWhF - jakes userid
    // user_2uCDZFAAFpCjlmPEY6W6X6vXQgH - some random id

    if(user && account){ 
      createChat(user.id, account.clerkId);
      // createChat(user.id, props.user)
      console.log(`Redirecting to chat with ${account.clerkId}...`);
      router.push('/chat_page');
    }
  };
  const handleProfileClick = () => {
    // when clicked, go to profile page of owner.Id

    if(user && account){ 
      console.log(`Redirecting to profile page with ${account.clerkId}...`);
      router.push(`/profile/${account.clerkId}`);
    }
  };

  switch (props.sidebarType) {
    case "Post":
      return (
        <div
          style={{
            backgroundColor: "#FFFFFF", 
            color: "#000000",
            width: "100%",
            minHeight: "120px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            borderTopStyle: "solid",
            borderBottomStyle: "solid",
            borderTopWidth: "2px",
            borderBottomWidth: "2px",
            borderColor: "#000000"
          }}
        >
          <button style={{ margin: "4px" }} onClick={handleItemClick}>
            <h3
              style={{
                margin: "0px",
                justifySelf: "flex-start",  
              }}
            >
              {props.name}
            </h3>
            {props.location && (
              <h6 style={{ margin: "0px", justifySelf: "flex-start" }}>
                {getLocationName([props.location[0], props.location[1]])}
              </h6>
            )}
          </button>
          {!collapsed && (
            <>
              <div
                className="description"
                style={{
                  padding: "4px",
                  width: "75%",
                  backgroundColor: "#000000",
                  color: "#FFFFFF",
                  marginTop: "1rem",
                  marginBottom: "1rem",
                  alignSelf: "center",
                  minHeight: "128px",
                }}
              >
                {props.description}
              </div>
              <button
                onClick={handleContactClick}
                style={{ alignSelf: "center", right: "0px", width: "80%", borderRadius: "10px" }}
              >
                Contact: &quot;{userName}&quot;
              </button>
              <button
                onClick={handleProfileClick}
                style={{ alignSelf: "center", right: "0px", width: "50%", borderRadius: "10px" }}
                >
                Profile
              </button>
            </>
          )}
          <div
            className="hstack"
            style={{
              justifySelf: "flex-end",
              margin: "8px",
              marginBottom: "2px",
              justifyContent: "space-between",
              display: "flex",
            }}
          >
            <p style={{ margin: "0px" }}>{userName}</p>
            {props.date && (
              <p style={{ margin: "0px" }}>{props.date.toLocaleDateString()}</p>
            )}
          </div>
        </div>
      );

    case "Chat":
      return (
        <button
          onClick={handleContactClick}
          style={{
            backgroundColor: "#FFFFFF",
            color: "#000000",
            width: "100%",
            minHeight: "120px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "flex-end",
          }}
        >
          <h3 style={{ margin: "2rem", alignSelf: "center" }}>{userName}</h3>
          <p
            style={{ margin: "0px", justifySelf: "flex-end", alignSelf: "end" }}
          >
            {props.date.toLocaleDateString()}
          </p>
        </button>
      );

    default:
      return (
        <div>
          <p>hi</p>
        </div>
      );
  }
}
