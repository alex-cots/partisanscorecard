import { apiFetch } from "@/lib/api"
import { InfoData, MemberDetailData } from "./models"

export async function getMemberDetail(id: string): Promise<MemberDetailData> {
  return await apiFetch(`/members/${id}/`)
}

export async function getInfoList(): Promise<InfoData[]> {
  return await apiFetch('/info/')
}
