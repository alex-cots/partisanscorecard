import { MemberData } from "@/models/member"
import { SUPPORTED_CONGRESS } from "../constants/supported_congresses"
import { Chamber } from "../constants/chamber"

export async function apiFetch<T>(path: string): Promise<T> {
  const response = await fetch(`${process.env.API_ROOT}${path}`, {
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      }
    })
  return response.json()
}

export async function getMemberList(chamber: Chamber, congress: SUPPORTED_CONGRESS): Promise<MemberData[]> {
  return await apiFetch(`/${chamber}/${congress}/members/`)
}
