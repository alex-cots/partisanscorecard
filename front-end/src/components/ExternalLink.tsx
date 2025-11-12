import Link from "next/link";
import styles from "@/styles/external-link.module.scss";


export default function ExternalLink({ children, className, href }: { children: React.ReactNode, className?: string, href: string }) {

  return (
    <Link className={className} href={href} target="_blank" rel="noopener noreferrer">
      {children} <span className={styles.arrowIcon}>⇲</span>
    </Link>
  )
}
