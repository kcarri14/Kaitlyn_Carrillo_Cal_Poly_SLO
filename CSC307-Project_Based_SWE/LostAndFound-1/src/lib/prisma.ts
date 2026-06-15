import { PrismaClient } from '@prisma/client';

//DOCUMENTATION IMPLEMENTATION
const globalForPrisma = global as unknown as { prisma: PrismaClient };

const prisma =
  globalForPrisma.prisma || new PrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

export default prisma

//OLD IMPLEMENTATION
//declare global {
//  var prisma: PrismaClient | undefined;
//}
//
//const prisma = globalThis.prisma ?? new PrismaClient();
//
//if (process.env.NODE_ENV !== 'production') {
//  globalThis.prisma = prisma
//}
//
//export default prisma
