'use client'
import { useState } from "react"

const PAGE_SIZE = 25

export default function VoteCollection({ votes }: { votes: any[] }) {
  const [pageState, setPageState] = useState<number>(1)
  const displayLength = pageState * PAGE_SIZE
  const displayedVotes = votes.slice(0, displayLength)
  function handleLoadMoreClick() {
    setPageState(pageState => pageState + 1)
  }

  let buttonClass = ''
  if (displayLength < votes.length) {
    buttonClass = 'hidden'
  }

  return (
    <section className="vote-collection">
      {displayedVotes.map(vote => (
        <article className="vote" key={vote.id}>
          <h2 className="vote-title">{vote.question}</h2>
          <div className="vote-category">{vote.category}</div>
          <div className="vote-date">{new Date(vote.timestamp).toLocaleString()}</div>
          <div className="vote-result">{vote.result}</div>
          <div className="vote-dem-maj-position">Democratic majority vote: {vote.dem_maj_position}</div>
          <div className="vote-repub-maj-position">Republican majority vote: {vote.repub_maj_position}</div>
          <div className="vote-id">{vote.id}</div>
        </article>
      ))}
      <button className={buttonClass} onClick={handleLoadMoreClick}>Load More</button>
    </section>
  )
}
