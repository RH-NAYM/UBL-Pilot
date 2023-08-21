import torch
import asyncio
import json
import pandas as pd


Brand_model = torch.hub.load('yolov5', 'custom', path='AI_Model/Model_Jun13.pt', source='local', device=0)
Brand_model.conf = 0.4
Brand_model.iou = 0.5

Count_model = torch.hub.load('yolov5', 'custom', path='AI_Model/Model_Jun13.pt', source='local', device=0)
Count_model.conf = 0.2
Count_model.iou = 0.6


async def detect_objects(model, url):
    result = await asyncio.get_event_loop().run_in_executor(None, model, url)
    result = result.pandas().xyxy[0].sort_values(by=['ymax', 'xmin'])
    df = pd.DataFrame(result)
    name_counts = df.groupby('name').size().to_dict()
    result_dict = {}
    for index, row in df.iterrows():
        name = row['name']
        result_dict[name] = name_counts.get(name, 0)
        json.dumps(result_dict)
        # json.loads(result_dict)
    return result_dict

async def detect_sequence(url, sequence):


    tasks = [
        detect_objects(Brand_model, url),
        detect_objects(Count_model, url)
    ]
    results = await asyncio.gather(*tasks)

    dict1, dict2 = results

    item = ['v','w']
    for i in item:
        for key,value in dict2.items():
            if i==key:
                add = {key:value}
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
    print('Detected Sequence: ', ds)
    if ds == sequence:
        sku = ("Valid Sequence")
    else:
        sku = ("Wrong Sequence")
    print("Given Sequence: ", sequence)



    extra = []
    for key in dict1.keys():
        if key not in sequence:
            extra.append(key)
    for items in extra:
        del dict1[items]

    result = {'Result': dict1, 'Sequence': sku}
    final_result = json.dumps(result)
    # print("Result Sent to User:", final_result)
    # print("###################################################################################################")

    return final_result

async def mainDetect(url,sequence):
    result = await detect_sequence(url, sequence)
    # print("Result Sent to User:", result)
    # print("###################################################################################################")

    return result

