# Import Library
import torch
import asyncio
import json
from collections import ChainMap
import math
import pandas as pd 
from collections import OrderedDict



# Load and Adjust Model : 1
# Brand_model = torch.hub.load('yolov5', 'custom', path='weights/Brand_Model/BrandModel96.pt', source='local', device=0)
Brand_model = torch.hub.load('yolov5', 'custom', path='weights/StartNew/Model98_v2.pt', source='local', device=0)
Brand_model.conf = 0.4
Brand_model.iou = 0.5

# Load and Adjust Model : 2
Count_model = torch.hub.load('yolov5', 'custom', path='weights/Brand.pt', source='local', device=0)
Count_model.conf = 0.2
Count_model.iou = 0.6



# def merge_and_average_dicts(dict1, dict2):
#     merged_dict = OrderedDict(dict1)
#     common_keys = set(dict1.keys()).intersection(set(dict2.keys()))
#     for key,x in dict1.items():

#         if key not in common_keys:
#             merged_dict[key] = dict1[key]
#     v = []
#     for c,d in dict1.items():
#         if c not in dict2 and d<=1:
#             v.append(c)
#     for i in v:
#         del dict1[i]
#     u = []
#     for a,b in dict2.items():
#         if a not in dict1 and b<=1:
#             u.append(a)
#     for i in u:
#         del dict2[i]
#     for key,y in dict2.items():
#         if key not in common_keys:
#             merged_dict[key] = dict2[key]
#     for key in common_keys:

#         if math.ceil((dict2[key] - dict1[key]))>=7:
#             del dict2[key]      
#         else:
#             average = math.ceil((dict1[key] + dict2[key]) / 2)
#             merged_dict[key] = average
    
#     return merged_dict

# Created an Asynchronus Function to perform the detection
async def det(url, sequence):

    # Execute Brand Model
    Brand_loop = asyncio.get_running_loop()
    Brand_result =await Brand_loop.run_in_executor(None, Brand_model, url)
    Brand_result = Brand_result.pandas().xyxy[0].sort_values(by=['xmin', 'ymax'])
    Brand_df = pd.DataFrame(Brand_result)
    Brand_sorted_df = pd.DataFrame(Brand_df)
    name_counts = Brand_sorted_df.groupby('name').size().to_dict()
    Brand_result_dict = {}
    for index, row in Brand_sorted_df.iterrows():
        name = row['name']
        Brand_result_dict.update({name:name_counts.get(name, 0)})
    Brand_result_json = json.dumps(Brand_result_dict)
    a = Brand_result_json
    a_dict = json.loads(a)
    dict1 = a_dict
    # del dict1['Tresemme_HD']
    # print("Brand_Model: ",dict1)

    # Execute Count Model
    Count_loop = asyncio.get_running_loop()
    Count_result =await Count_loop.run_in_executor(None, Count_model, url)
    Count_result = Count_result.pandas().xyxy[0].sort_values(by=['xmin', 'ymax'])
    Count_df = pd.DataFrame(Count_result)
    Count_sorted_df = pd.DataFrame(Count_df)
    name_counts = Count_sorted_df.groupby('name').size().to_dict()
    Count_result_dict = {}
    for index, row in Count_sorted_df.iterrows():
        name = row['name']
        Count_result_dict.update({name:name_counts.get(name, 0)})
    Count_result_json = json.dumps(Count_result_dict)
    b = Count_result_json
    b_dict = json.loads(b)
    dict2 = b_dict
    # del dict2['Tresemme_HD']
    # print("Count_Model: ",dict2)


    item = ['v','w']
    for i in item:
        for key,value in dict2.items():
            if i==key:
                add = {key:value}
                dict1.update(add)
            else:
                continue
    # print("Brand_Model: ",dict1)
    # Merging 2 dictionary with the function that was created earlier
    # result_dict = merge_and_average_dicts(dict1), dict2)

    # Sequence Detection
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


    # Finalise the results    
    # result = {'Hair_Care_Items': result_dict, 'Sequence': sku}
    result = {'Result': dict1, 'Sequence': sku}
    Final_Result = json.dumps(result)
    print("Result Sent to User : ", Final_Result)
    print("###################################################################################################")
    return Final_Result



