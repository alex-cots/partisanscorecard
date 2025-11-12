import type { Metadata } from "next";
import { Merriweather } from "next/font/google";
import "@/styles/main.scss"

const sourceSerif4 = Merriweather({
  subsets: ['latin'],
  weight: ['300', '400', '700', '900']
});

export const metadata: Metadata = {
  title: "Congressional Partisan Scorecard",
  description: "Track the partisanship of congressional voting.",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={sourceSerif4.className}>
        {children}
      </body>
    </html>
  );
}
