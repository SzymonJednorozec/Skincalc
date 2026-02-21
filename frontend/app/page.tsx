"use client";
import { useEffect, useState } from "react";
import { testfetch,submitfetch, deleteItem,apiTestFetch, scrapeSteam, syncSkinport, updateCurrencyRatio,item_row, getAllItems, updateItemRow } from "./services/api";
import { testData } from "./types/items";
import { setDefaultAutoSelectFamily } from "net";

export default function Home() {
  const [items, setItems] = useState<item_row[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const ScrapeSteam = async () => {
    setIsLoading(true);
    try{
      const response = await scrapeSteam();
      console.log(response);
    }
    catch(error) {
      console.error("Error:", error);
    }
    finally{
      setIsLoading(false);
    }
  }

  const SyncSkinport = async () => {
    setIsLoading(true);
    try{
      const response = await syncSkinport();
      console.log(response);
    }
    catch(error) {
      console.error("Error:", error);
    }
    finally{
      setIsLoading(false);
    }
  }

  const UpdateCurrencyRatio = async () => {
    setIsLoading(true);
    try{
      const response = await updateCurrencyRatio();
      console.log(response);
    }
    catch(error) {
      console.error("Error:", error);
    }
    finally{
      setIsLoading(false);
    }
  }

  const LoadItems = async () => {
    try{
      const response = await getAllItems();
      setItems(response);
    }
    catch(error) {
      console.error("Error:", error);
    }
  }

  const UpdateItemRow = async (hash_name: string) =>{
    setIsLoading(true);
    try{
      const response = await updateItemRow(hash_name);
      setItems((prev) => {
      const filtered = prev.filter((item) => item.name !== hash_name);
      return [response,...filtered];
      });
    }
    catch(error) {
      console.error("Error:", error);
    }
    finally{
      setIsLoading(false);
    }
  }

  // const GetItemsPage = (page_num) =>{

  // }

  return (
  <main className="p-8 bg-[#032533] h-screen">
    <h1 className="mb-6 text-5xl font-bold text-[#94d2bd]">SkinCalc</h1>
    <div className="flex flex-row gap-3">
      <button className="rounded-3xl bg-[#bb3e03] px-4 py-2 text-white hover:bg-[#9b2226] disabled:bg-gray-400 transition-colors"
        onClick={UpdateCurrencyRatio}
        disabled={isLoading}
      >
        Update USD/PLN
      </button>
      <button className="rounded-3xl bg-[#bb3e03] px-4 py-2 text-white hover:bg-[#9b2226] disabled:bg-gray-400 transition-colors"
        onClick={ScrapeSteam}
        disabled={isLoading}
      >
        Scrape Steam
      </button>
      <button className="rounded-3xl bg-[#bb3e03] px-4 py-2 text-white hover:bg-[#9b2226] disabled:bg-gray-400 transition-colors"
        onClick={SyncSkinport}
        disabled={isLoading}
      >
        Sync Skinport
      </button>
      <button className="rounded-3xl bg-[#bb3e03] px-4 py-2 text-white hover:bg-[#9b2226] disabled:bg-gray-400 transition-colors"
        onClick={LoadItems}
        disabled={isLoading}
      >
        Refresh Table
      </button>
    </div>
    <div className="mt-7 flex overflow-x-auto rounded-lg shadow-2xl">
      <table className="w-full border-collapse text-left">
        <thead className="bg-[#531315] text-white">
          <tr>
            <th className="p-3">Name</th>
            <th className="p-3">Steam price</th>
            <th className="p-3">Skinport price</th>
            <th className="p-3">Ratio</th>
            <th className="p-3">Skinport price after fee</th>
            <th className="p-3">Steam price Update</th>
            <th className="p-3">Skinport price Update</th>
          </tr>
        </thead>
        <tbody className="bg-[#001219]">
          {items.map((item)=>(
            <tr key={item.name} onClick={()=>{UpdateItemRow(item.name)}} className="transition-colors border-b border-black hover:bg-[#531315] hover:border-5">
              <td className="items-center p-3 flex">
                {item.image_url && <img src={item.image_url} alt="" className="w-15 h-15 object-contain mx-3"/>}
                <span>{item.name}</span>
              </td>
              <td className="items-center p-3">{item.steam_price} zł</td>
              <td className="items-center p-3">{item.skinport_price} zł</td>
              <td className="items-center p-3">{item.ratio_percentage} %</td>
              <td className="items-center p-3">{item.sell_price_after_fee} zł</td>
              <td className="items-center p-3">
                <span className="mx-0.5">{new Date(item.steam_updated).toLocaleTimeString()}</span>
                <span className="mx-0.5">{new Date(item.steam_updated).toLocaleDateString()}</span>
              </td>
              <td className="items-center p-3">
                <span className="mx-0.5">{new Date(item.skinport_updated).toLocaleTimeString()}</span>
                <span className="mx-0.5">{new Date(item.skinport_updated).toLocaleDateString()}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </main>
);
}

// colors [#001219] [#005f73] [#0a9396] [#94d2bd] [#e9d8a6] [#ee9b00] [#ca6702] [#bb3e03] [#ae2012] [#9b2226]