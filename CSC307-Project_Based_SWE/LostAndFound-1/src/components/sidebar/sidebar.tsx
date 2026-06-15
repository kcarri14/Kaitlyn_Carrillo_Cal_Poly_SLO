import { FaRegSquarePlus } from "react-icons/fa6";
// import { BsFillFilterSquareFill } from "react-icons/bs";
import styles from "@/styles/sidebar.module.css";
//import SideBarItem from "@/components/sidebarItem";
import { SideBarMode } from "./sidebar.data";
import Search from "./search";
import QuerySearch from "./querySearch";

function BarElements(type: SideBarMode) {
  switch (type) {
    case "Search":
      return (
        <div
          id="hstack"
          style={{
            width: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: "5px",
            flexDirection: "column",
          }}
        >
          <div style={{ width: "85%" }}>
            <Search />
          </div>
          <div style={{ width: "100%" }}>
            <QuerySearch onlyUserPosts={false}/>
          </div>
        </div>
      );
    case "Posts":
      return (
        <div
          id="hstack"
          style={{
            width: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: "5px",
            flexDirection: "column",
          }}
        >
          <div style={{ width: "100%" }}>
            <QuerySearch onlyUserPosts/>
          </div>
        </div>
      );

    case "Chat":
      window.location.href = "/chat_page";

    default:
      break;
  }
}

export default function SideBar(props: {
  mode: SideBarMode;
  onClick: (mode: SideBarMode) => void;
}) {
  const handlePostButtonClick = () => {
    location.href = "/post_page";
  };

  return (
    <div
      className="h-64"
      style={{
        position: "absolute",
        right: "0",
        width: "15vw",
        height: "93vh",
        backgroundColor: "#5583bb",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        paddingTop: "8px",
        borderLeft: "4px solid #162c49",
        overflowY: "auto", // Enables vertical scrolling
      overflowX: "hidden", // Prevents horizontal scrolling
      }}
    >
      {/* MAPPING ITEMS */}
      {props.mode == "Posts" && (
        <button
          id="create-post-button"
          className={styles.sidebarButton}
          onClick={handlePostButtonClick}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            width: "100%",
            minHeight: "120px",
            borderWidth: "0px",
          }}
        >
          <FaRegSquarePlus size="4rem" />
          <p
            style={{
              margin: "0px",
              fontSize: "1rem",
            }}
          >
            Create New Post
          </p>
        </button>
      )}
      {BarElements(props.mode)}
    </div>
  );
}
