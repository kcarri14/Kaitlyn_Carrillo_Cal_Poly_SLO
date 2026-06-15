"use client";
import "@/app/chat_page/chat_page.css";
// import 'stream-chat-react/dist/css/v2/index.css';
import { createToken } from "@/lib/actions";
import { useCallback } from "react";
import {
  ChannelList,
  useCreateChatClient,
  Chat,
  Channel,
  ChannelHeader,
  MessageInput,
  MessageList,
  Thread,
  Window,
} from "stream-chat-react";

interface StreamChatProps {
  userData: {
    id: string;
    name?: string;
    image?: string;
  };
}

export default function StreamChat({ userData }: StreamChatProps) {
  const tokenProvider = useCallback(async () => {
    return await createToken(userData.id);
  }, [userData.id, createToken]);

  const client = useCreateChatClient({
    userData,
    tokenOrProvider: tokenProvider,
    apiKey: process.env.NEXT_PUBLIC_STREAM_API_KEY!,
  });

  if (!client) return <div>Setting up client & connection...</div>;

  // // for adding way to see profile
  // const handleClick = (event: MouseEvent) => {
  //   const element = event.target as HTMLElement;
  //   console.log("click " + element + element.classList);
  //   // console.log("" + element.attributes[0] + element.attributes[1]);
  //   if (element.classList.contains("str-chat__avatar-image")) {
  //     console.log(element.attributes.length);
  //     console.log(element.attributes[0]);
  //     console.log(element.attributes[1]); 
  //     console.log(element.attributes[2]); 
  //     console.log(element.attributes[3]); 
  //   }
  // };

  // document.addEventListener("click", handleClick, { once: true });

  // creates a messaging channel to chat in
  // this channel will contain the user and jake to test
  // const channel = client.channel("messaging", {
  //   name: "Awesome channel with you and Jake",
  //   members: [userData.id, "user_2teE5f4oyYA3VXldk53KCNsMWhF"],
  // });
  // // this channel doesnt need an ID because it is distinct
  // channel.create();
  // for adding way to see profile
  // const handleClick = (event: MouseEvent) => {
  //   const element = event.target as HTMLElement;
  //   console.log("click " + element);
  //   if (element && element.classList.contains("str-chat__avatar-image")) {
  //     console.log(element);
  //   }
  // };


  // document.addEventListener("click", handleClick, { once: true });

  return (
    <div>
    <Chat client={client}>
      <div style={{display:"flex"}}>
      <ChannelList filters={{ members: { $in: [userData.id] } }} />
      <Channel>
        <Window>
          <ChannelHeader />
          <div style={{overflow:"scroll"}}>
          <MessageList />
          </div>
          <MessageInput />
        </Window>
        <Thread />
      </Channel>
      </div>
    </Chat>
    </div>
  );
}
