import { NextRequest, NextResponse } from "next/server";
import prisma from "@/lib/prisma";

export async function PUT(Request: NextRequest, context: { params: { id: string }}) {
    try {
        const { id } = await context.params;
        const parsedId =parseInt(id);
        const newItem = await Request.json();

        if(isNaN(parsedId)){
            return NextResponse.json({error: "Invalid item ID"}, { status: 400 });
        }

        const current = await prisma.item.findUnique({
            where: { id: parsedId },
            include: {
                foundMatches: true,
                lostMatches: true,
            }
        })

        if(!current){
            return NextResponse.json({error: "Item not found"}, {status: 404 });
        }

        let updatedItem: typeof current;
        
        if(current?.isLost){
            updatedItem = await prisma.item.update({
                where: { id: parsedId},
                include: {
                    foundMatches: true,
                    lostMatches: true,
                },
                data : {
                    foundMatches : {
                        set: [...current.foundMatches, newItem]
                    }
                },
            })
        } else {
            updatedItem = await prisma.item.update({
                where: { id: parsedId},
                include: {
                    foundMatches: true,
                    lostMatches: true,
                },
                data : {
                    lostMatches : {
                        set: [current.lostMatches, newItem]
                    }
                },
            })
        }

        return NextResponse.json({message: "Item updated succesfully", item: updatedItem}, { status: 200 });

    } catch (error){
        console.log(error);
        return NextResponse.json({error: "Failed to update item"}, {status: 500});
    }
}