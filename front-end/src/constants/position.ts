// Positions can have a wide range of values depending on the vote type, so this file will just be
// for functions related to yes/no positions.

const YES_POSITIONS = ['aye', 'yea']
const NO_POSITIONS = ['no', 'nay']

export function appendEmoji(position: string): string {
  if (YES_POSITIONS.includes(position.toLowerCase())) {
    return position + ' ✅'
  }
  if (NO_POSITIONS.includes(position.toLocaleLowerCase())) {
    return position + ' ❌'
  }
  return position
}
