import { Chamber } from "@/constants/chamber"
import { Parties, Party } from "@/constants/party"
import { MemberData, MemberModel } from "@/models/member"
import { VoteData, VoteModel } from "@/models/vote"

export type InfoData = {
 congress: number,
 chamber: Chamber,
 member_count: number,
 democrat_count: number,
 republican_count: number,
 roll_call_count: number
}

export class InfoModel {
  congress: number
  chamber: Chamber
  memberCount: number
  democratCount: number
  republicanCount: number
  rollCallCount: number

  constructor(infoData: InfoData) {
    this.congress = infoData.congress
    this.chamber = infoData.chamber
    this.memberCount = infoData.member_count
    this.democratCount = infoData.democrat_count
    this.republicanCount = infoData.republican_count
    this.rollCallCount = infoData.roll_call_count
  }

  partyMemberCount(party: Party) {
    if (party === Parties.DEMOCRATIC) {
      return this.democratCount
    }
    if (party === Parties.REPUBLICAN) {
      return this.republicanCount
    }
  }
}

export type MemberDetailData = MemberData & {
  congresses_served: {
    calculation_time: string
    chamber: 'house' | 'senate'
    congress: number
    district: string
    democratic_loyalty_rank_in_chamber: number
    democratic_loyalty_rank_in_party: number
    republican_loyalty_rank_in_chamber: number
    republican_loyalty_rank_in_party: number
    state: string
    vote_with_democrats_percentage: number
    vote_with_democrats_count: number
    vote_with_republicans_percentage: number
    vote_with_republicans_count: number
    vote_count: number
    vote_set: VoteData[]
  }[]
}

export class MemberDetailModel extends MemberModel {
  congressesServed: {
    calculationTime: string
    chamber: Chamber
    congress: number
    district: string
    democraticLoyaltyRankInChamber: number
    democraticLoyaltyRankInParty: number
    republicanLoyaltyRankInChamber: number
    republicanLoyaltyRankInParty: number
    state: string
    voteWithDemocratsPercentage: number
    voteWithDemocratsCount: number
    voteWithRepublicansPercentage: number
    voteWithRepublicansCount: number
    voteCount: number
    voteSet: VoteModel[]
  }[]

  constructor(memberDetailData: MemberDetailData) {
    super(memberDetailData)
    this.congressesServed = memberDetailData.congresses_served.map(term => ({
      calculationTime: term.calculation_time,
      chamber: term.chamber,
      congress: term.congress,
      district: term.district,
      democraticLoyaltyRankInChamber: term.democratic_loyalty_rank_in_chamber,
      democraticLoyaltyRankInParty: term.democratic_loyalty_rank_in_party,
      republicanLoyaltyRankInChamber: term.republican_loyalty_rank_in_chamber,
      republicanLoyaltyRankInParty: term.republican_loyalty_rank_in_party,
      state: term.state,
      voteWithDemocratsPercentage: term.vote_with_democrats_percentage,
      voteWithDemocratsCount: term.vote_with_democrats_count,
      voteWithRepublicansPercentage: term.vote_with_republicans_percentage,
      voteWithRepublicansCount: term.vote_with_republicans_count,
      voteCount: term.vote_count,
      voteSet: term.vote_set.map(vote => new VoteModel(vote))
    }))
  }
}
