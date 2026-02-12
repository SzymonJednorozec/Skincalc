import { testData } from './../types/items';


export async function testfetch(): Promise<testData> {
    const response = await fetch('http://127.0.0.1:8000/');

    if (!response.ok) {
        throw new Error('Error while collecting data from API');
    }

    const data: testData = await response.json();
    return data;
}

export async function submitfetch(data: testData) {
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