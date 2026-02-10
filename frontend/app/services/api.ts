export interface TestSchema{
    id: number;
    name: string;
}

export async function testfetch(): Promise<TestSchema> {
    const response = await fetch('http://127.0.0.1:8000/');

    if (!response.ok) {
        throw new Error('Error while collecting data from API');
    }

    const data: TestSchema = await response.json();
    return data
}