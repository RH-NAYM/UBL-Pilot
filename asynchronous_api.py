from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from typing import List, Union
from test_function import *

app = FastAPI()

class Item(BaseModel):
    url: str
    sequence: list

async def process_item(item: Item):
    result = await mainDetect(item.url, item.sequence)
    result = json.loads(result)
    return result

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

@app.post("/test")
async def create_items(items: Union[Item, List[Item]]):
    results = await process_items(items)
    print("Result Sent to User:", results)
    print("###################################################################################################")

    return results


