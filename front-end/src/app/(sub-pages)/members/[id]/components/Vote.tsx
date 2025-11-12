import { DateTime } from "luxon";
import ExternalLink from "@/components/ExternalLink";
import { VoteModel } from "@/models/vote";
import { Chamber, Chambers, ChamberUtils } from "@/constants/chamber";
import { Parties } from "@/constants/party";
import { appendEmoji } from "@/constants/position";
import toOrdinalString from "@/lib/ordinal";
import styles from "../styles/vote.module.scss";
import { MemberDetailModel } from "../models";

export default function Vote({ chamber, member, vote }: { chamber: Chamber, member: MemberDetailModel, vote: VoteModel }) {

  const demPosition = <>
    <div className={`${styles.positionLabel} ${styles.democraticText}`}>Democratic majority:</div>
    <div className={styles.positionValue}>{appendEmoji(vote.rollCall.demMajPosition)}</div>
  </>

  const repubPosition = <>
    <div className={`${styles.positionLabel} ${styles.republicanText}`}>Republican majority:</div>
    <div className={styles.positionValue}>{appendEmoji(vote.rollCall.repubMajPosition)}</div>
  </>

  let ownPartyMajorityPosition = <></>
  let oppositionPartyMajorityPosition = <></>
  let memberPartyStyle = ''
  if (member.currentParty === Parties.DEMOCRATIC) {
    memberPartyStyle = styles.democraticText
    ownPartyMajorityPosition = demPosition
    oppositionPartyMajorityPosition = repubPosition
  } else if (member.currentParty === Parties.REPUBLICAN) {
    memberPartyStyle = styles.republicanText
    ownPartyMajorityPosition = repubPosition
    oppositionPartyMajorityPosition = demPosition
  }
  return (
    <article className={styles.container}>
            <h3 className={styles.title}>{vote.rollCall.question}</h3>
              <div className={styles.body}>
                <div className={`${styles.positionLabel} ${memberPartyStyle}`}>
                {ChamberUtils.toMemberType(chamber)} {member.lastName}:
                </div>
                <div className={styles.positionValue}>{appendEmoji(vote.position)}</div>
                {ownPartyMajorityPosition}
                {oppositionPartyMajorityPosition}
                <div className={styles.resultLabel}>Result:</div>
                <div className={styles.resultValue}>{vote.rollCall.result}</div>
              </div>
            <div className={styles.footer}>
              <span className={styles.voteNumber}>{chamber} Vote #{vote.rollCall.number} {toOrdinalString(vote.rollCall.congressNumber)} congress, {toOrdinalString(vote.rollCall.sessionNumber)} session</span>
              <span className={styles.date}>{vote.rollCall.timestamp.toLocaleString(DateTime.DATETIME_FULL)} </span>
              <span className={styles.links}>
                <ExternalLink href={vote.rollCall.govtrackUrl}>
                  GovTrack
                </ExternalLink>
                <ExternalLink href={vote.rollCall.governmentUrl}>
                  {chamber === Chambers.HOUSE ? 'house.gov' : 'senate.gov'}
                </ExternalLink>
              </span>
            </div>
          </article>
  )
}
