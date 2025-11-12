export type Chamber = typeof Chambers[keyof typeof Chambers]

export const Chambers = {
  HOUSE: 'house',
  SENATE: 'senate'
} as const

export const ChamberUtils = {
  toMemberType(chamber: Chamber, capitalize = true) {
    if (capitalize) {
      return {
        [Chambers.HOUSE]: 'Representative',
        [Chambers.SENATE]: 'Senator'
      }[chamber]
    }

    return {
      [Chambers.HOUSE]: 'representative',
      [Chambers.SENATE]: 'senator'
    }[chamber]

  }
}
