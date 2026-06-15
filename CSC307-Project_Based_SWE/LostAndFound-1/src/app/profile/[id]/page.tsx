import { clerkClient } from "@clerk/clerk-sdk-node";
import { notFound } from "next/navigation";
import Image from "next/image";
import styles from "@/styles/profile.module.css";
import Rating from "@/components/profile/rating";

interface ProfilePageProps {
  params: { id: string };
}

export default async function ProfilePage({ params }: ProfilePageProps) {
  const { id: userId } = await params;

  try {
    const user = await clerkClient.users.getUser(userId);

    return (
      <div className={styles.profileWrapper}>
        <div className={styles.clerkContainer}>
          <Image
            src={user.imageUrl}
            alt={`${user.fullName}'s profile picture`}
            width={0}
            height={0}
            className={styles.clerkImage}
          />
          <h1 className="text-2xl font-semibold">{user.fullName}</h1>
        </div>
        <Rating clerkId={userId} />
      </div>
    );
  } catch (error) {
    console.log(error);
    return notFound();
  }
}
