'use client'
import Link from "next/link";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { AriaAttributes, ChangeEvent, MouseEventHandler, ReactNode, useState } from "react"
import styles from "@/styles/member-table.module.scss"
import { CURRENT_CONGRESS, SUPPORTED_CONGRESS, SUPPORTED_CONGRESSES } from "@/constants/supported_congresses";
import { Chamber } from "@/constants/chamber";
import { Parties } from "@/constants/party";
import { StateUtils } from "@/constants/state";

type SortState =  {
  ascending: boolean;
  field: string;
  type: string;
}

export default function MemberTable({ chamber, membersByCongress }: { chamber: Chamber, membersByCongress: any }) {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const congressInput = Number(searchParams.get('congress'))
  let congress: SUPPORTED_CONGRESS = CURRENT_CONGRESS
  if (SUPPORTED_CONGRESSES.includes(congressInput as any)) {
      congress = congressInput as SUPPORTED_CONGRESS
  }

  const members = membersByCongress[congress]
  const [sortState, setSortState] = useState<SortState>(
    {
      ascending: true,
      field: "inverted_name",
      type: "string",
    }
  )

  function handleSelectCongress(event:  ChangeEvent<HTMLSelectElement>) {
    const selectedCongress = event.target.value
    const params = new URLSearchParams(searchParams.toString())
    params.set('congress', selectedCongress)
    router.replace(pathname + '?' + params.toString())
  }

  function handleClickSort(field: string, type: string) {
    let ascending = true
    if (sortState.field === field) {
      // Click on an already sorted column indicates we should reverse the sort order.
      ascending = !sortState.ascending
    }
    setSortState({ ascending, field, type })
  }
  let comparator: (a: any, b: any) => number
  if (sortState.type === "string") {
    comparator = new Intl.Collator('en', { sensitivity: 'base' }).compare
  } else if (sortState.type === "number") {
    comparator = (a, b) => a - b
  }

  members.sort((member1: any, member2: any) => comparator(member1[sortState.field], member2[sortState.field]))

  if (!sortState.ascending) {
    members.reverse()
  }

  function partyTextClassName(party: string): string | undefined {
    if (party === Parties.DEMOCRATIC) {
      return styles.democraticText
    }
    if (party === Parties.REPUBLICAN) {
      return styles.republicanText
    }
  }

  function votesPlurality(num: number): 'vote' | 'votes' {
    if (num === 1) {
      return 'vote'
    }
    return 'votes'
  }

  return (
    <>
    <div className={styles.congressSelectContainer}>
      <label htmlFor="congress-select" >Choose a Congress:</label>
      <select id="congress-select" defaultValue={congress} onChange={handleSelectCongress}>
        {SUPPORTED_CONGRESSES
          .map((congress_option) => (
            <option value={congress_option} key={congress_option}>{congress_option}</option>
          )
        )}
      </select>
    </div>
    <div className={styles.tableContainer}>
    <table className={styles.table}>
      <thead>
        <tr>
          <th className={styles.rank} scope="column">Rank</th>
          <SortableHeader className={styles.name} field="inverted_name" onClick={() => handleClickSort("inverted_name", "string")} sortState={sortState}>
            Name
          </SortableHeader>
          <SortableHeader className={styles.party} field="current_party" onClick={() => handleClickSort("current_party", "string")} sortState={sortState}>
            Party
          </SortableHeader>
          <SortableHeader className={styles.state} field="state" onClick={() => handleClickSort("state", "string")} sortState={sortState}>
            State
          </SortableHeader>
          <SortableHeader field="vote_with_democrats_percentage" onClick={() => handleClickSort("vote_with_democrats_percentage", "number")} sortState={sortState}>
            <span className={styles.democraticText}>D</span> Agree %
          </SortableHeader>
          <SortableHeader field="vote_with_democrats_count" onClick={() => handleClickSort("vote_with_democrats_count", "number")} sortState={sortState}>
            <span className={styles.democraticText}>D</span> Agree #
          </SortableHeader>
          <SortableHeader field="vote_with_republicans_percentage" onClick={() => handleClickSort("vote_with_republicans_percentage", "number")} sortState={sortState}>
            <span className={styles.republicanText}>R</span> Agree %
          </SortableHeader>
          <SortableHeader field="vote_with_republicans_count" onClick={() => handleClickSort("vote_with_republicans_count", "number")} sortState={sortState}>
            <span className={styles.republicanText}>R</span> Agree #
          </SortableHeader>
          <SortableHeader field="vote_count" onClick={() => handleClickSort("vote_count", "number")} sortState={sortState}>
            Total Votes
          </SortableHeader>
        </tr>
      </thead>
      <tbody>
        {members
          .map((member: any, index: any) => (
            <tr key={member.bioguide_id}>
              <td className={styles.rank}>{index + 1}</td>
              <td className={styles.name}><Link href={`/members/${member.bioguide_id}/?congress=${congress}&chamber=${chamber}`}>{member.inverted_name}</Link></td>
              <td className={`${styles.party} ${partyTextClassName(member.current_party)}`}>
                <abbr>{member.current_party.charAt(0)}</abbr>
                <span className={styles.full}>{member.current_party}</span>
              </td>
              <td className={styles.state}>
                <abbr>{StateUtils.toPostalAbbreviation(member.state)}</abbr>
                <span className={styles.full}>{member.state}</span>
              </td>
              <td>{(member.vote_with_democrats_percentage * 100).toFixed(1)}%</td>
              <td>{member.vote_with_democrats_count} {votesPlurality(member.vote_with_democrats_count)}</td>
              <td>{(member.vote_with_republicans_percentage * 100).toFixed(1)}%</td>
              <td>{member.vote_with_republicans_count} {votesPlurality(member.vote_with_republicans_count)}</td>
              <td>{member.vote_count} {votesPlurality(member.vote_count)}</td>
            </tr>
          ))}
      </tbody>
    </table>
    </div>
    </>
  )
}

function SortableHeader(
  { children, className = '', field, onClick, sortState }: { children: ReactNode, className?: string, field: string, onClick: MouseEventHandler, sortState: SortState }
  ) {
    let ariaSort: AriaAttributes["aria-sort"] = undefined
    let orderIcon = ""
    if (field === sortState.field) {
      ariaSort = sortState.ascending ? "ascending" : "descending"
      orderIcon = sortState.ascending ? "⇧" : "⇩"
    }

    return (
      <th aria-sort={ariaSort} className={`${styles.sortable} ${className}`} scope="column">
        <button onClick={onClick}>
            <span>{children}</span>
            <span aria-hidden="true">{orderIcon}</span>
        </button>
      </th>
    )
}
