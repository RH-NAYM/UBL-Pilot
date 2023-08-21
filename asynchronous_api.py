from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from typing import List, Union
from asynchronus_function import *
import uvicorn

app = FastAPI()

class Item(BaseModel):
    url: str
    sequence: list

async def process_item(item: Item):
    try:
        result = await mainDetect(item.url, item.sequence)
        # print(item.url)
        result = json.loads(result)
        return result
    finally:
        torch.cuda.empty_cache()
        pass

async def process_items(items: Union[Item, List[Item]]):
    if isinstance(items, list):
        coroutines = [process_item(item) for item in items]
        results_dict = await asyncio.gather(*coroutines)
        results = {}
        for item in results_dict:
            results.update(item)
    else:
        results = await process_item(items)
    return results

@app.post("/AI_Detection")
async def create_items(items: Union[Item, List[Item]]):
    try:
        results = await process_items(items)
        print("Result Sent to User:", results)
        print("###################################################################################################")
        print(items)
        return results
    finally:
        torch.cuda.empty_cache()
        pass

if __name__ == "__main__":
    try:
        del Brand_model
        del Count_model
        uvicorn.run(app, host="127.0.0.1", port=8000)
    finally:
        torch.cuda.empty_cache()


