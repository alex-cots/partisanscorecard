import Link from "next/link";
import styles from "@/styles/header.module.scss"

export default function CongressRootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
    <header>
      <nav className={styles.header}>
        <Link className={styles.navLogo} href="/">
          <span className={styles.noUnderline}>📜📊📋</span>
          Congressional Partisan Scorecard
        </Link>
        <Link href="/senators">Senators</Link>
        <Link href="/representatives">Representatives</Link>
        {/*
        Disable until complete.
        <Link href="/senate-votes">Senate Votes</Link>
        <Link href="/house-votes">House Votes</Link>
        */}
      </nav>
    </header>
    {children}
    </>
  );
}
