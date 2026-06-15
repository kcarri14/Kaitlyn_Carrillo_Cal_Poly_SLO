'use server'
import { StreamChat } from "stream-chat"

const serverClient = StreamChat.getInstance(
    process.env.NEXT_PUBLIC_STREAM_API_KEY!,
    process.env.STREAM_API_SECRET
)

    
export async function createToken(userId: string): Promise<string> {
    return serverClient.createToken(userId)
}

export async function createChat(userId: string, receiverId: string){
    const channel = serverClient.channel("messaging", {
        members:[userId, receiverId], created_by_id: userId
    })
    await channel.create()
    
}

// // this code creates channels that include jake's google accounts
// // they can message each other
// const channel = serverClient.channel("messaging", "travel", {
//     name: "Awesome channel about traveling",
//     members:["user_2teE5f4oyYA3VXldk53KCNsMWhF"]
//   });
// // you can add yourself to this chat with this code:
// //      channel.addMembers(["user_2u33OMZjCx8WXpqYehpWAbBZ2hG", "YOUR CLERK USER ID HERE"]);
// // when you go to /chat_page, i am displaying your clerk userid underneath the channels,
// //  copy that and add here if you want. make sure to reload the page after.
// //  right now, it only adds my 2nd google account:
//   channel.addMembers(["user_2u33OMZjCx8WXpqYehpWAbBZ2hG"]);
//   // Here, 'travel' will be the channel ID
//   channel.create();

// //   second channel to test, functions the same way as the first channel
//   const channel2 = serverClient.channel("messaging", "gaming", {
//     name: "Awesome channel about gaming",
//     members:["user_2teE5f4oyYA3VXldk53KCNsMWhF"]
//   });
//   // Here, 'travel' will be the channel ID
//   channel2.addMembers(["user_2u33OMZjCx8WXpqYehpWAbBZ2hG"]);
//   channel2.create();