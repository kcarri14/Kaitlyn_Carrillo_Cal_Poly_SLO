"use client"
import React from "react";
import Map from "@/components/Map";
import AuthListener from "@/components/authListener"
import "leaflet/dist/leaflet.css";

const App: React.FC = () => {
  return (
    <>
      <AuthListener />
      <Map />
    </>
  );
};

export default App;
