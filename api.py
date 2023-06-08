from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from function import det
import json
from typing import List, Union

app = FastAPI()
class Item(BaseModel):
    url: str
    sequence: list

async def process_item(item: Item):
    url = item.url
    sequence = item.sequence
    result = await asyncio.create_task(det(url, sequence))
    final_result_json = json.loads(result)
    return final_result_json


@app.post("/AI_Detection")
async def create_item(item: Item):
    url = item.url
    sequence = item.sequence
    # sequence = json.dumps(sequence)
    result =await  asyncio.create_task(det(url, sequence))
    final_result_json = json.loads(result)
    return final_result_json


@app.post("/item")
async def create_item(items: Union[Item, List[Item]]):

    if isinstance(items, list):
        coroutines = []
        for item in items:
            coroutines.append(process_item(item))
        results = await asyncio.gather(*coroutines)


    else:
        results = await process_item(items)


    return results
