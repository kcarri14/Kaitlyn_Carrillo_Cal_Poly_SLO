"use client";

import { useSearchParams, usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Search() {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  useEffect(() => {
    const params = new URLSearchParams(searchParams);
    if (params.has("query")) {
      params.delete("query");
      replace(`${pathname}?${params.toString()}`);
    }
  }, []); // Runs only once when component mounts

  const handleSearch = (searchTerm: string) => {
    const params = new URLSearchParams(searchParams);
    if (searchTerm) {
      params.set("query", searchTerm);
    } else {
      params.delete("query");
    }
    replace(`${pathname}?${params.toString()}`);
  };

  return (
    <div className="relative flex flex-1 flex-shrink-0">
      <input
        style={{ width: "97%" }}
        placeholder="Search..."
        defaultValue="" // Clears input on reload
        onChange={(e) => {
          handleSearch(e.target.value);
        }}
      />
    </div>
  );
}
