
import asyncio
import httpx

items = [
    [{"url": "https://i.ibb.co/mB15YV7/D26-1573427-jpg-rf-b6adaba1d3057c1abd2380511240fed6.jpg", "sequence": ["a"]}],
    [{"url": "https://i.ibb.co/mB15YV7/D26-1573427-jpg-rf-b6adaba1d3057c1abd2380511240fed6.jpg", "sequence": ["a", "b"]}],
    [{"url": "https://i.ibb.co/mB15YV7/D26-1573427-jpg-rf-b6adaba1d3057c1abd2380511240fed6.jpg", "sequence": ["a", "b", "c", "d"]}]
]



async def send_requests():
    semaphore = asyncio.Semaphore(10) 
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=60.0)) as client:
        tasks = []
        for item in items:
            task = asyncio.create_task(send_request(client, item, semaphore))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)

async def send_request(client, item, semaphore):
    async with semaphore:
        try:
            response = await client.post("http://127.0.0.1:8050/test", json=item)
            print(response.json())
        except httpx.ReadTimeout as e:
            raise RuntimeError("Request timed out.") from e

# Run the requests concurrently
asyncio.run(send_requests())

