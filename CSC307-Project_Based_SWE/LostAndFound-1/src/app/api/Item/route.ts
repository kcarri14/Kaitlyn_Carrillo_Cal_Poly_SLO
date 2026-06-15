import { NextRequest, NextResponse } from "next/server";
import prisma from "@/lib/prisma";

export async function GET(Request: NextRequest): Promise<NextResponse> {
  try {
    // extract search query parameter safely
    const { searchParams } = new URL(Request.url);
    const query = searchParams.get("query")?.trim() || "";

    //console.log("query " + query);
    //console.log("searchParams" + searchParams);
    // fetch items with optional search filtering
    const items1 = await prisma.item.findMany({
      where: query
        ? {
            OR: [
              { name: { contains: query, mode: "insensitive" } },
              { event: { contains: query, mode: "insensitive" } },
              { description: { contains: query, mode: "insensitive" } },
              { tags: { hasSome: [query] } },
            ],
          }
        : {},
    });
    //console.log(items1);
    return NextResponse.json({ items: items1 });
  } catch (error) {
    console.error("Error fetching items:", error);
    return NextResponse.json({ error: "Internal Server Error" });
  }
}

export async function POST(Request: NextRequest): Promise<NextResponse> {
  const { Item } = await Request.json();
  const newItem = await prisma.item.create({
    data: {
      isLost: Item.isLost,
      bounty: Item.bounty,
      date: new Date(Item.date),
      images: Item.images || [],
      name: Item.name,
      location: Item.location,
      event: Item.event,
      description: Item.description,
      tags: Item.tags,
      owner: {connect: { id: Item.ownerId }}
    },
  });
  return NextResponse.json({ Item: newItem });
}
