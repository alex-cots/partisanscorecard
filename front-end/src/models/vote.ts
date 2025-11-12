import { DateTime } from 'luxon'
import { Chambers } from '@/constants/chamber'
import { PartyUtils, Party } from '@/constants/party'
import { DC_TIMEZONE } from '@/constants/timezone'

export type RollCallData = {
    id: string
    bill: number
    chamber: string
    number: number
    question: string
    category: string
    dem_maj_position: string
    repub_maj_position: string
    result: string
    timestamp: string
}

export type VoteData = {
  roll_call: RollCallData
  position: string
}


export class RollCallModel {
  id: string
  bill: number
  chamber: string
  number: number
  question: string
  category: string
  demMajPosition: string
  repubMajPosition: string
  result: string
  timestamp: DateTime

  constructor(rollCallData: RollCallData) {
    this.id = rollCallData.id
    this.bill = rollCallData.bill
    this.chamber = rollCallData.chamber
    this.number = rollCallData.number
    this.question = rollCallData.question
    this.category = rollCallData.category
    this.demMajPosition = rollCallData.dem_maj_position
    this.repubMajPosition = rollCallData.repub_maj_position
    this.result = rollCallData.result
    this.timestamp = DateTime.fromISO(rollCallData.timestamp, { zone: DC_TIMEZONE })
  }

  get sessionYear(): number {
    return Number(this.id.split('.')[1])
  }

  get sessionNumber(): number {
    // Assume congresses have one session a year and a maximum of two.
    // This assumption holds for all congresses after the 76th (so far).
    return 2 - (this.sessionYear % 2)
  }

  get congressNumber(): number {
    return Number(this.id.split('.')[0].split('-')[1])
  }

  get govtrackUrl(): string {
    const sessionSection = `${this.congressNumber}-${this.sessionYear}`
    const numberSection = `${this.chamber.charAt(0)}${this.number}`
    return `https://govtrack.us/congress/votes/${sessionSection}/${numberSection}`
  }

  get governmentUrl(): string {
    if (this.chamber === Chambers.HOUSE) {
      return `https://clerk.house.gov/Votes/${this.sessionYear}${this.number}`
    } else {
      const paddedVoteNumber = String(this.number).padStart(5, '0')
      const sessionSection = `vote${this.congressNumber}${this.sessionNumber}`
      const filename = `vote_${this.congressNumber}_${this.sessionNumber}_${paddedVoteNumber}`
      return `https://www.senate.gov/legislative/LIS/roll_call_votes/${sessionSection}/${filename}.htm`
    }
  }

}

export class VoteModel {
  rollCall: RollCallModel
  position: string

  constructor(voteData: VoteData) {
    this.rollCall = new RollCallModel(voteData.roll_call)
    this.position = voteData.position
  }

  isOutlier(currentParty: Party) {
    const majPositionField: 'demMajPosition' | 'repubMajPosition'= `${PartyUtils.toShortHand(currentParty)}MajPosition`
    return (this.position !== this.rollCall[majPositionField])
  }
}
