"use client";
import { useEffect, useState } from "react";
import { testfetch,submitfetch, deleteItem } from "./services/api";
import { testData } from "./types/items";

export default function Home() {
  const [data, setData] = useState<testData[]>([]);
  const [submitData, setsubmitData] = useState<testData>({
    id: 0,
    name: ""
  });


  useEffect(() => {
    const fetchData = async () => {
      const x = await testfetch();
      setData(x);
    }
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const formData = new FormData(e.currentTarget);
    const name = formData.get("skinName") as string;

    if (!name){
      return;
    }

    try{
      const newItem = await submitfetch(name);
      setData((prev) =>  [...prev,newItem]);

      // setData((data) => (data ? [...data,newItem] : [newItem]));
      // setsubmitData({id: 0, name: ""})
    }
    catch(error) {
      console.error("Error:", error);
    }
  };

  const handleClick = async (id: number) => {
    try{
      await deleteItem(id)
      setData((data) => data.filter((item) => item.id !== id));
    }
    catch(error){
      console.error("Error:", error);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      
        <div>
          {data && data.length > 0 ? (
            data.map((item)=> (
                <li key={item.id}>
                  <span>id:{item.id}  name:{item.name}</span>
                  <button onClick={() => handleClick(item.id)} className="bg-red-500 hover:bg-blue-700 text-white font-bold py-1 px-1 rounded ml-2">
                    x
                  </button>
                </li>
            ))
          ) : (
            <p>brak danych</p>
          )}
        </div>
        <form onSubmit={handleSubmit}>
          <input name="skinName"/>
          <button type="submit">Submit</button>
        </form>

    </div>
    
  );
}
