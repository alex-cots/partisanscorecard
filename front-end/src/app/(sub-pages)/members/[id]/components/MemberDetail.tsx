'use client'
import { ChangeEvent, useState } from "react"
import { DateTime } from 'luxon'
import { usePathname, useRouter, useSearchParams } from "next/navigation"
import toOrdinalString from "@/lib/ordinal"
import { SUPPORTED_CONGRESSES } from "@/constants/supported_congresses"
import styles from "../styles/member-detail.module.scss"
import { ChamberUtils } from "@/constants/chamber"
import { InfoData, InfoModel, MemberDetailData, MemberDetailModel } from "../models"
import { DC_TIMEZONE } from "@/constants/timezone"
import Vote from "./Vote"
import capitalize from "@/lib/capitalize"

const PAGE_SIZE = 15

export default function MemberDetail({ infoDataList, memberData }: { infoDataList: InfoData[], memberData: MemberDetailData }) {
  const infoList = infoDataList.map(infoData => new InfoModel(infoData))
  const member = new MemberDetailModel(memberData)
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  let selectedTerm = member.congressesServed[0]

  let inputCongress = Number(searchParams.get('congress'))
  let inputChamber = searchParams.get('chamber')
  if (inputCongress && inputChamber && SUPPORTED_CONGRESSES.includes(inputCongress as any)) {
    for (const term of member.congressesServed) {
      if (term.congress === inputCongress && term.chamber === inputChamber) {
        selectedTerm = term
        break
      }
    }
  }

  const selectedInfo = infoList.find(info =>
     (info.congress === selectedTerm.congress && info.chamber === selectedTerm.chamber)
  )

  const [pageState, setPageState] = useState(1)
  const [outlierChecked, setOutlierChecked] = useState(true)
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const filteredVotes = selectedTerm.voteSet.filter(vote => {
    if (outlierChecked && !vote.isOutlier(member.currentParty)) {
      return false
    }
    if (startDate) {
      const startDateObj = DateTime.fromISO(startDate, { zone: DC_TIMEZONE })
      if (startDateObj > vote.rollCall.timestamp) {
        return false
      }
    }

    if (endDate) {
      const endDateObj = DateTime.fromISO(endDate, { zone: DC_TIMEZONE })
      if (endDateObj < vote.rollCall.timestamp) {
        return false
      }
    }

    return true
  })

  const displayLength = pageState * PAGE_SIZE
  const displayedVotes = filteredVotes.slice(0, displayLength)
  const hiddenShowMoreButton = displayLength >= filteredVotes.length ? 'hidden' : ''
  function handleShowMoreClick() {
    setPageState(pageState => pageState + 1)
  }

  function handleSelectCongress(event: ChangeEvent<HTMLSelectElement>) {
    const selectedKey = event.target.value
    const [selectedCongress, selectedChamber] = selectedKey.split('-')
    const params = new URLSearchParams(searchParams.toString())
    params.set('congress', selectedCongress)
    params.set('chamber', selectedChamber)
    router.replace(pathname + '?' + params.toString())
  }

  function handleOutlierCheck() {
    setOutlierChecked(!outlierChecked)
    setPageState(1)
  }

  function handleStartDate(event: ChangeEvent<HTMLInputElement>) {
    const newStartDate = event.currentTarget.value
    setStartDate(newStartDate)
    if (
      newStartDate && endDate
      && DateTime.fromISO(endDate) < DateTime.fromISO(newStartDate)
    ) {
      event.currentTarget.setCustomValidity('Start state must be earlier than end date.')
      event.currentTarget.reportValidity()
    } else {
      event.currentTarget.setCustomValidity('')
    }
    setPageState(1)
  }

  function handleEndDate(event: ChangeEvent<HTMLInputElement>) {
    const newEndDate = event.currentTarget.value
    setEndDate(newEndDate)
    if (
      startDate && newEndDate
      && DateTime.fromISO(newEndDate) < DateTime.fromISO(startDate)
    ) {
      event.currentTarget.setCustomValidity('Start state must be earlier than end date.')
      event.currentTarget.reportValidity()
    } else {
      event.currentTarget.setCustomValidity('')
    }
    setPageState(1)
  }

  return (
    <main><div className={styles.mainContentContainer}>
      <hgroup className={styles.title}>
        <h1>{member.name}</h1>
        <p>{member.currentParty} {ChamberUtils.toMemberType(selectedTerm.chamber)} From {selectedTerm.state}</p>
      </hgroup>
      <div className={styles.termSelectContainer}>
        <label htmlFor="term-select">Viewing:</label>
        <select id="term-select" defaultValue={`${selectedTerm.congress}-${selectedTerm.chamber}`} onChange={handleSelectCongress}>
          {member.congressesServed
            .map((term) => (
              <option value={`${term.congress}-${term.chamber}`} key={`${term.congress}-${term.chamber}`}>
                {toOrdinalString(term.congress)} Congress in the {capitalize(term.chamber)}
              </option>
            )
            )}
        </select>
      </div>
      <div className={styles.statsContainer}>
        <div>
          <div>Democratic Agreement</div>
          <div className={styles.subRow}>How often this {ChamberUtils.toMemberType(selectedTerm.chamber, false)} voted with the majority of Democrats</div>
        </div>
        <div>
          <div>{(selectedTerm.voteWithDemocratsPercentage * 100).toFixed(1)}%</div>
          <div className={styles.subRow}>{selectedTerm.voteWithDemocratsCount} out of {selectedTerm.voteCount} votes</div>
        </div>
        <div>
          <div>Republican Agreement</div>
          <div className={styles.subRow}>How often this {ChamberUtils.toMemberType(selectedTerm.chamber, false)} voted with the majority of Republicans</div>
        </div>
        <div>
          <div> {(selectedTerm.voteWithRepublicansPercentage * 100).toFixed(1)}%</div>
          <div className={styles.subRow}>{selectedTerm.voteWithRepublicansCount} out of {selectedTerm.voteCount} votes</div>
        </div>
        <div>Democratic Agreement Rank</div>
        <div> {toOrdinalString(selectedTerm.democraticLoyaltyRankInChamber)}<span className={styles.countTotal}>/{selectedInfo?.memberCount}</span></div>

        <div>Republican Agreement Rank</div>
        <div> {toOrdinalString(selectedTerm.republicanLoyaltyRankInChamber)}<span className={styles.countTotal}>/{selectedInfo?.memberCount}</span></div>

        <div>Democratic Agreement Rank In Party</div>
        <div> {toOrdinalString(selectedTerm.democraticLoyaltyRankInParty)}<span className={styles.countTotal}>/{selectedInfo?.partyMemberCount(member.currentParty)}</span></div>

        <div>Republican Agreement Rank In Party</div>
        <div> {toOrdinalString(selectedTerm.republicanLoyaltyRankInParty)}<span className={styles.countTotal}>/{selectedInfo?.partyMemberCount(member.currentParty)}</span></div>
      </div>
      <h2>Votes</h2>
      <div className={ styles.voteControls }>
        <div>
          <label htmlFor="outlierCheckbox">Outliers only:</label>
          <input id="outlierCheckbox" type="checkbox" defaultChecked={true} onChange={handleOutlierCheck}/>
        </div>
        <div>
          <label htmlFor="startDate">Starting this date:</label>
          <input id="startDate" type="date" value={startDate} onChange={handleStartDate}/>
        </div>
        <div>
          <label htmlFor="startDate">Ending this date:</label>
          <input id="endDate" type="date" value={endDate} onChange={handleEndDate}/>
        </div>
      </div>
      {displayedVotes.map(vote => (
        <Vote chamber={selectedTerm.chamber} member={member} vote={vote} key={vote.rollCall.id} />
      ))}
      <button className={`${styles.showMoreButton} ${hiddenShowMoreButton}`} onClick={handleShowMoreClick}>Show More</button>
    </div></main>
  )
}
