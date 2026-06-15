import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';

export async function POST(Request: NextRequest) {
  try {
    //get userId from request json
    const { userId } = await Request.json()
    //check if userID is there
    if (!userId) {
      return NextResponse.json({ error: "Missing user data" }, { status: 400 });
    }
    //try to get user from database
    const existingUser = await prisma.Account.findUnique({
      where: { clerkId: userId }
    });
    //check if user was found in database
    if (!existingUser) {
      //add user to database
      await prisma.Account.create({
        data: { clerkId: userId }
      });
    }
    
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json(
      {error: "Server error", details: (error as Error).message },
      { status: 500 }
    );
  }
}
