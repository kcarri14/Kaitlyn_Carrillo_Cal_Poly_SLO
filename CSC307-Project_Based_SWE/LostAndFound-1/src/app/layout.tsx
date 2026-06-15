import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "@/styles/global.css";
import { Barlow, Montserrat } from "next/font/google";
import NavBar from "@/components/navbar";
import { ClerkProvider } from "@clerk/nextjs";

const barlow = Barlow({
  variable: "--font-barlow",
  subsets: ["latin"],
  weight: "400",
});

const montserrat = Montserrat({
  variable: "--font-montserrat",
  subsets: ["latin"],
});

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Lost and Found",
  description: "Lost and Found at Cal Poly - By the Professional Crastinators",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}>
      <html lang="en">
        <body
          className={`${geistSans.variable} ${geistMono.variable} ${montserrat.variable} ${barlow.variable} antialiased`}
        >
          <NavBar />
          <header className="flex justify-end items-center p-4 gap-4 h-16"></header>
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
