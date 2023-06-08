import torch
import asyncio
import json
import pandas as pd

async def det(url, sequence):
    Brand_model = torch.hub.load('yolov5', 'custom', path='weights/StartNew/Model98_v2.pt', source='local', device=0)
    Brand_model.conf = 0.4
    Brand_model.iou = 0.5

    Count_model = torch.hub.load('yolov5', 'custom', path='weights/Brand.pt', source='local', device=0)
    Count_model.conf = 0.2
    Count_model.iou = 0.6

    Brand_result = await asyncio.get_event_loop().run_in_executor(None, Brand_model, url)
    Brand_result = Brand_result.pandas().xyxy[0].sort_values(by=['xmin', 'ymax'])
    Brand_df = pd.DataFrame(Brand_result)
    Brand_sorted_df = pd.DataFrame(Brand_df)
    name_counts = Brand_sorted_df.groupby('name').size().to_dict()
    Brand_result_dict = {}
    for index, row in Brand_sorted_df.iterrows():
        name = row['name']
        Brand_result_dict.update({name: name_counts.get(name, 0)})
    Brand_result_json = json.dumps(Brand_result_dict)
    dict1 = json.loads(Brand_result_json)

    Count_result = await asyncio.get_event_loop().run_in_executor(None, Count_model, url)
    Count_result = Count_result.pandas().xyxy[0].sort_values(by=['xmin', 'ymax'])
    Count_df = pd.DataFrame(Count_result)
    Count_sorted_df = pd.DataFrame(Count_df)
    name_counts = Count_sorted_df.groupby('name').size().to_dict()
    Count_result_dict = {}
    for index, row in Count_sorted_df.iterrows():
        name = row['name']
        Count_result_dict.update({name: name_counts.get(name, 0)})
    Count_result_json = json.dumps(Count_result_dict)
    dict2 = json.loads(Count_result_json)

    item = ['v', 'w']
    for i in item:
        for key, value in dict2.items():
            if i == key:
                add = {key: value}
                dict1.update(add)
            else:
                continue

    ds = [*dict1]
    extra_item = []
    for i in ds:
        if i not in sequence:
            extra_item.append(i)
    for i in extra_item:
        ds.remove(i)
    print('Detected Sequence:', ds)
    if ds == sequence:
        sku = "Valid Sequence"
    else:
        sku = "Wrong Sequence"
    print("Given Sequence:", sequence)

    extra = []
    for key in dict1.keys():
        if key not in sequence:
            extra.append(key)
    for items in extra:
        del dict1[items]

    result = {'Result': dict1, 'Sequence': sku}
    Final_Result = json.dumps(result)
    print("Result Sent to User:", Final_Result)
    print("###################################################################################################")

    return Final_Result
