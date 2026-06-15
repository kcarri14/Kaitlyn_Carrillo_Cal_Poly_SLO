import { NextRequest, NextResponse } from 'next/server';
import { clerkClient } from '@clerk/nextjs/server';

export async function GET(Request: NextRequest): Promise<NextResponse> {
  const { searchParams } = new URL(Request.url);
  const clerkId = searchParams.get("clerkId")?.trim() || "";

  const client = await clerkClient()

  const user = await client.users.getUser(clerkId)

  // Return the Backend User object
  return NextResponse.json({ user: user }, { status: 200 })
}
