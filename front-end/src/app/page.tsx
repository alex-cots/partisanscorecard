import Link from "next/link";
import styles from "@/styles/home.module.scss"

export default function Home() {
  return (
    <>
      <header>
        <h1 id="home-title">📜📊📋Congressional Partisan Scorecard</h1>
      </header>
      <main>
        <nav className={styles.nav}>
          <Link href="/senators">Senators</Link>
          <Link href="/representatives">Representatives</Link>
          {/*
          Disable until complete.
          <Link href="/senate-votes">Senate Votes</Link>
          <Link href="/house-votes">House Votes</Link>
          */}
        </nav>
      <p className={styles.description}>A site for understanding members of Congress&apos;s relationship with the major political parties.</p>

    {/*
      Disable until complete.
        <h2>Recent Votes</h2>
        <table>
          <thead>
            <tr>
              <th>Bill</th>
              <th>Chamber</th>
              <th>Result</th>
              <th>Democratic majority vote</th>
              <th>Republican majority vote</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>Example Bill Here</td>
              <td>House</td>
              <td>PASS</td>
              <td>YEA</td>
              <td>NAY</td>
            </tr>
          </tbody>
        </table>
    */}
    </main>
    </>
  );
}
