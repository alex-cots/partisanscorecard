import { Suspense } from "react"
import MemberDetail from "@/app/(sub-pages)/members/[id]/components/MemberDetail"
import { SUPPORTED_CONGRESSES } from "@/constants/supported_congresses"
import { getMemberList } from "@/lib/api"
import { Chambers } from "@/constants/chamber"
import { getInfoList, getMemberDetail } from "./api"

export const dynamicParams = false

// Return a list of all member ids so next.js generates all member pages at build time.
export async function generateStaticParams(): Promise<{ id: string }[]> {
  const members = new Set()
  for (const congress of SUPPORTED_CONGRESSES) {
    const senatorsInCongress = await getMemberList(Chambers.SENATE, congress)
    senatorsInCongress.forEach(member => members.add(member))
    const representativesInCongress = await getMemberList(Chambers.HOUSE, congress)
    representativesInCongress.forEach(member => members.add(member))
  }

  return Array.from(members).map((member: any) => ({
    id: member.bioguide_id,
  }))
}

export default async function Member({params}: {params: Promise<{ id: string }>}) {
  const { id } = await params
  const infoDataList = await getInfoList()
  const memberData = await getMemberDetail(id)
  return (
    <Suspense>
      <MemberDetail memberData={memberData} infoDataList={infoDataList}/>
    </Suspense>
  )
}
