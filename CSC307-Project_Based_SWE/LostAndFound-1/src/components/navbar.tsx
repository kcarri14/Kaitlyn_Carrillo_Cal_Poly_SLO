// TODO: change the links when the pages exist
// TODO: open side nav bar with each component
"use client";
import Link from "next/link";

import { FaSearch, FaMapSigns, FaRegBell } from "react-icons/fa";
import { LuMessagesSquare } from "react-icons/lu";
import styles from "@/styles/navbar.module.css";
import { UserButton, useUser } from "@clerk/nextjs";
import { SideBarMode } from "./sidebar/sidebar.data";
import { MouseEvent, useState } from "react";
import SideBar from "./sidebar/sidebar";
import { usePathname, useRouter } from "next/navigation";

function check_page(){
  const path = usePathname()
  if(path == "/" || path == "/chat_page"){
    return true
  }
  return false
}

export default function NavBar() {
  const router = useRouter();
  const { user } = useUser();
  console.log(user?.id);

  const [sidebarMode, setSidebarMode] = useState<SideBarMode | null>("Search");

  const handleClick = (e: MouseEvent<HTMLButtonElement>) => {
    setSidebarMode(e.currentTarget.id as SideBarMode);
  };

  const SIDEBAR_ITEMS = [
    { id: "Search", icon: FaSearch },
    { id: "Posts", icon: FaMapSigns },
    { id: "Chat", icon: LuMessagesSquare },
  ];

  console.log(usePathname() + " : " + sidebarMode);
  return (
    <div className={styles.nav_wrapper}>
      <ul className={styles.navbar_list}>
        <div className={styles.nav_left}>
          <li className={styles.title}>
            <Link href={"/"}>Lost and Found</Link>
          </li>
          <li className={styles.centerProfileImage}>
            {/* profile */}
            <UserButton>
              <UserButton.MenuItems>
                <UserButton.Action
                  label="View Profile"
                  labelIcon={<FaSearch />}
                  onClick={() => router.push(`/profile/${user?.id}`)}
                />
              </UserButton.MenuItems>
            </UserButton>
          </li>
        </div>
        {usePathname() == "/" && (
          <div
            className={styles.nav_right}
            style={{
              width: "15vw",
              display: "flex",
              margin: "0px",
              padding: "0px",
            }}
          >
            {SIDEBAR_ITEMS.map((item) => (
              <li
                key={item.id}
                style={{
                  height: "4vw",
                  width: "5vw",
                }}
              >
                <button
                  id={item.id}
                  disabled={sidebarMode == item.id}
                  onClick={handleClick}
                  style={{
                    height: "100%",
                    width: "100%",
                  }}
                >
                  <item.icon size="32px" />
                </button>
              </li>
            ))}
          </div>
        )}
      </ul>
      {check_page() && sidebarMode && <SideBar mode={sidebarMode} onClick={(mode: SideBarMode) => setSidebarMode(mode)}/> }
    </div>
  );
}
