/*
  Warnings:

  - A unique constraint covering the columns `[clerkId]` on the table `Account` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `clerkId` to the `Account` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Account" ADD COLUMN     "clerkId" TEXT NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "Account_clerkId_key" ON "Account"("clerkId");
