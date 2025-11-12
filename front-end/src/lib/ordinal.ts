export default function toOrdinalString(int: number): string {
  const lastDigit = int % 10
  const lastTwoDigits = int % 100;
  if (lastDigit === 1 && lastTwoDigits !== 11) {
      return `${int}st`;
  }
  if (lastDigit === 2 && lastTwoDigits !== 12) {
      return `${int}nd`;
  }
  if (lastDigit === 3 && lastTwoDigits !== 13) {
      return `${int}rd`;
  }
  return `${int}th`;
}
