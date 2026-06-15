import { NextRequest, NextResponse } from "next/server";
import prisma from "@/lib/prisma";

export async function PUT(Request: NextRequest, context: { params: { id: string } }) {
    try {
        //extract user id from URL and get the request body
        const { id } = await context.params;
        const data = await Request.json();

        //make sure id is filled and parsed corrrectly
        const parsedId = parseInt(id, 10);
        if (isNaN(parsedId)) {
            return NextResponse.json({ error: "Invalid account ID" }, { status: 400 });
        }

        // update the fields based on inputted id
        const updatedUser = await prisma.Account.update({
            where: { id: parsedId },
            data,
        });

        return NextResponse.json({ message: "User updated successfully", user: updatedUser }, { status: 200 });
    } catch (error) {
        return NextResponse.json({ error: "Failed to update user" }, { status: 500 });
    }
}
