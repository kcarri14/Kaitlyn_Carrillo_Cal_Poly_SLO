import { currentUser } from "@clerk/nextjs/server";
import React from 'react';
import StreamChat from "./stream-chat";

export default async function Chat() {
    const user = await currentUser();
    
    if(!user){
        return null;
    }

    const userData = {
        id: user.id,
        ...(user.fullName ? {name: user.fullName} : {}),
        ...(user.imageUrl ? {image: user.imageUrl} : {})
    }
    // user_2teE5f4oyYA3VXldk53KCNsMWhF - jakes userid
    return (
        <StreamChat userData={userData}/>
        );
    }