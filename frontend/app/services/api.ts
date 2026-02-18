import { testData } from './../types/items';


export async function testfetch(): Promise<testData> {
    const response = await fetch('http://127.0.0.1:8000/');

    if (!response.ok) {
        throw new Error('Error while collecting data from API');
    }

    const data: testData = await response.json();
    return data;
}

export async function submitfetch(data: string): Promise<testData> {
    const response = await fetch('http://127.0.0.1:8000/',
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data),
        });
    if (!response.ok){
        throw new Error("Something went wrong durning POST")
    }
    const new_item: testData = await response.json();

    return new_item;
}

// export async function submitfetch(data: testData): Promise<testData> {
//     const response = await fetch('http://127.0.0.1:8000/',
//         {
//             method: "POST",
//             headers: {"Content-Type": "application/json"},
//             body: JSON.stringify(data),
//         });
//     if (!response.ok){
//         throw new Error("Something went wrong durning POST")
//     }
//     const new_item: testData = await response.json();

//     return new_item;
// }

export async function deleteItem(id: number): Promise<boolean>{
    const response = await fetch(`http://127.0.0.1:8000/?item_id=${id}`,
        {
            method: "DELETE",
        });
    if (!response.ok){
        throw new Error("Something went wrong durning DELETE")
    }
    return response.ok;
}

export async function apiTestFetch(): Promise<boolean> {
    const response = await fetch('http://127.0.0.1:8000/api');
    if (!response.ok){
        throw new Error("Something went wrong durning api test")
    }
    return response.ok;
}

export interface item_row {
    name: string;
    image_url: string | null;
    steam_price: number;
    steam_updated: string; 
    skinport_price: number;
    sell_price_after_fee: number;
    skinport_updated: string;
    ratio_percentage: number;
}

export async function getAllItems(): Promise<item_row[]>{
    const response = await fetch("http://127.0.0.1:8000/api/get-items",
        {
            method: "GET",
            headers: {"Accept": "application/json"}
        }
    );
     if (!response.ok){
        throw new Error("Something went wrong | getAllItems()");
    }

    const data: item_row[] = await response.json();
    return data;
}

export async function updateCurrencyRatio(): Promise<string>{
        const response = await fetch("http://127.0.0.1:8000/api/get-currency-ratio",
        {
            method: "GET",
            headers: {"Accept": "application/json"},
        }
    );
    if(!response.ok){
        throw new Error("Something went wrong | updateCurrencyRatio()");
    }
    const data = await response.json();
    return data.message;
}

export async function scrapeSteam(): Promise<string>{
    const response = await fetch("http://127.0.0.1:8000/api/scrape-steam",{
        method: "GET",
        headers: {"Accept": "application/json"},
    });
    if(!response.ok){
        throw new Error("Something went wrong | scrapeSteam()");
    }
    const data = await response.json();
    return data.message;
}

export async function syncSkinport(): Promise<string>{
    const response = await fetch("http://127.0.0.1:8000/api/sync-skinport",{
        method: "GET",
        headers: {"Accept": "application/json"},
    });
    if(!response.ok){
        throw new Error("Something went wrong | syncSkinport()");
    }
    const data = await response.json();
    return data.message;
}