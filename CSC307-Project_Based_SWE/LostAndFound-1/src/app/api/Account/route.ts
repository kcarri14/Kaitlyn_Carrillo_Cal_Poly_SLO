import { NextRequest, NextResponse } from  'next/server';
import prisma from '@/lib/prisma';

export async function GET(Request: NextRequest): Promise<NextResponse> {
  const accounts = await prisma.account.findMany();
  return NextResponse.json({ accounts });
}
