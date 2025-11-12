import VoteCollection from "@/components/VoteCollection";

export default async function HouseVotes() {
  // const response = await fetch(`${process.env.API_ROOT}/house/118/roll-calls/`, {
  //   headers: {
  //     'Accept': 'application/json',
  //     'Content-Type': 'application/json',
  //   }
  // })
  const houseVotes: any[] = [] //await response.json()
  return (
    <main>
      <h1>House Votes</h1>
      <VoteCollection votes={houseVotes} />
    </main>
  );
}
