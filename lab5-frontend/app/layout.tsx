import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Summarization UI",
  description: "Text-In → Summary-Out",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
