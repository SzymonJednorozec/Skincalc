"use client";
import { useEffect, useState } from "react";
import { testfetch } from "./services/api";

export default function Home() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      const x = await testfetch();
      setData(x);
    }
    fetchData()
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      {data ? (
          <div className="space-y-2">
            <p><strong>Nazwa:</strong> {data.name}</p>
            <p><strong>id:</strong> {data.id}</p>
          </div>
        ) : (
          <p className="animate-pulse">Łączenie z Pythonem...</p>
        )}
    </div>
  );
}
