import type { Metadata } from "next";
import { DM_Mono, DM_Serif_Display, Outfit } from "next/font/google";
import "./globals.css";

const display = DM_Serif_Display({ subsets: ["latin"], weight: "400", variable: "--font-display" });
const body = Outfit({ subsets: ["latin"], variable: "--font-body" });
const mono = DM_Mono({ subsets: ["latin"], weight: ["300", "400", "500"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: "Autonomous Real Estate Investment Analyzer",
  description: "Five AI agents evaluate investment potential and generate a full real estate memo."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${display.variable} ${body.variable} ${mono.variable} min-h-screen bg-bg text-text-primary`}>
        {children}
      </body>
    </html>
  );
}

