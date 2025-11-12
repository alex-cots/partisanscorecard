import VoteCollection from "@/components/VoteCollection";

export default async function SenateVotes() {
  // const response = await fetch(`${process.env.API_ROOT}/senate/118/roll-calls/`, {
  //   headers: {
  //     'Accept': 'application/json',
  //     'Content-Type': 'application/json',
  //   }
  // })
  const senateVotes: any[] = [] //await response.json()
  return (
    <main>
      <h1>Senate Votes</h1>
      <VoteCollection votes={senateVotes} />
    </main>
  );
}
