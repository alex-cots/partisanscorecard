import { Suspense } from "react";
import styles from "@/styles/member-table.module.scss"
import MemberTable from '@/components/MemberTable';
import { SUPPORTED_CONGRESSES } from "@/constants/supported_congresses";
import { Chambers } from "@/constants/chamber";
import { getMemberList } from "@/lib/api";

export default async function Representatives() {
  const membersByCongress: any = {}
  for (const congress of SUPPORTED_CONGRESSES) {
     membersByCongress[congress] = await getMemberList(Chambers.HOUSE, congress)
  }
  return (
    <main>
      <h1 className={styles.title}>Representatives</h1>
      <Suspense>
        <MemberTable chamber={Chambers.HOUSE} membersByCongress={membersByCongress} />
      </Suspense>
    </main>
  );
}
