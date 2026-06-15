/*
  Warnings:

  - You are about to drop the `Match` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "Match" DROP CONSTRAINT "Match_foundItemId_fkey";

-- DropForeignKey
ALTER TABLE "Match" DROP CONSTRAINT "Match_lostItemId_fkey";

-- DropTable
DROP TABLE "Match";

-- CreateTable
CREATE TABLE "_ItemMatches" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL,

    CONSTRAINT "_ItemMatches_AB_pkey" PRIMARY KEY ("A","B")
);

-- CreateIndex
CREATE INDEX "_ItemMatches_B_index" ON "_ItemMatches"("B");

-- AddForeignKey
ALTER TABLE "_ItemMatches" ADD CONSTRAINT "_ItemMatches_A_fkey" FOREIGN KEY ("A") REFERENCES "Item"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_ItemMatches" ADD CONSTRAINT "_ItemMatches_B_fkey" FOREIGN KEY ("B") REFERENCES "Item"("id") ON DELETE CASCADE ON UPDATE CASCADE;
