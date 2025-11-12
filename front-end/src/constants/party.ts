
export const Parties = {
  DEMOCRATIC: 'Democratic',
  REPUBLICAN: 'Republican'
} as const

export type Party = typeof Parties[keyof typeof Parties]

export const PartyUtils = {
  toShortHand(party: Party): 'dem' | 'repub' {
    const lookupObj = {
      [Parties.DEMOCRATIC]: 'dem',
      [Parties.REPUBLICAN]: 'repub'
    } as const
    return lookupObj[party]
  }
}
