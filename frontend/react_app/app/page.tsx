import FloorplanForm from "./components/FloorplanForm";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <h2 className="text-6xl font-bold">CargoBuddy</h2>
        <ol className="list-inside list-decimal text-sm text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
          <li className="mb-2">
            Upload the floorplan image
          </li>
          <li>Set where the robot is right now and where you want it to go.</li>
        </ol>
        <FloorplanForm />
      </main>
    </div>
  );
}
