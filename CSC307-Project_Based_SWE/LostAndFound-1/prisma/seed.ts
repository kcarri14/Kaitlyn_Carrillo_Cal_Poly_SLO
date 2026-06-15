import prisma from '../src/lib/prisma';
async function main() {
  const testUser1 = await prisma.account.upsert({
    where: { id: 69 },
    update: {},
    create: {
      id: 69,
      clerkId: "user_2tdtsi6OI3CXPzAIyIVst90RPYP",
      //email: 'testUser1@testing.com',
      //password: 'testUser1Password',
      //name: 'testUser1'
    }
  })
  const testUser2 = await prisma.account.upsert({
    where: { id: 420 },
    update: {},
    create: {
      id: 420,
      clerkId: "user_2uCDq46ByXKgBGIynckr96Xqz7M",
      //email: 'testUser2@testing.com',
      //password: 'testUser2Password',
      //name: 'testUser2'
    }
  })
  const testLostItem = await prisma.item.upsert({
    where: { id: 69420 },
    update: {},
    create: {
      id: 69420,
      ownerId: 69,
      isLost: true,
      bounty: 10,
      date: '2025-03-10T00:00:00.000Z',
      images: [],
      name: "iPhone 13",
      location: [35.3002, -120.6588],
      event: "Career Fair",
      description: "Test item on databse",
      tags: ["Red"],
    }
  })
  const testFoundItem = await prisma.item.upsert({
    where: { id: 42069 },
    update: {},
    create: {
      id: 42069,
      ownerId: 420,
      isLost: false,
      bounty: 0,
      date: '2025-03-01T00:00:00.000Z',
      images: [],
      name: "Backpack",
      location: [35.30836180357595, -120.65871169319334],
      description: "Test item on databse",
      tags: ["Blue"],
    }
  })
  console.log({ testUser1, testUser2, testLostItem, testFoundItem})
}
main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error(e)
    await prisma.$disconnect()
    process.exit(1)
  })
