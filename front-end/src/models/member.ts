import { Party } from "@/constants/party"

export type MemberData = {
  bioguide_id: string
  inverted_name: string
  current_party: Party
  lis_id: string
  name: string
}

export class MemberModel {
  bioguideId: string
  name: string
  invertedName: string
  currentParty: Party
  lisId: string

  constructor(memberData: MemberData) {
    this.bioguideId = memberData.bioguide_id
    this.name = memberData.name
    this.invertedName = memberData.inverted_name
    this.currentParty = memberData.current_party
    this.lisId = memberData.lis_id
  }

  get lastName(): string {
    return this.invertedName.split(',')[0]
  }
}
