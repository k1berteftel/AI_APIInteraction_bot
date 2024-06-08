import asyncio
import os

import requests
import json

from PIL import Image

#mark_img_url = 'https://png.pngtree.com/png-clipart/20230512/original/pngtree-smiley-face-png-image_9158302.png'
#watermark_url = 'https://quickchart.io/watermark'
api_url = 'https://developer.remaker.ai/api/remaker/v1/face-swap/create-job'
headers = {
    'accept': 'application/json',
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjM2NTY2NywicHJvZHVjdF9jb2RlIjoiMDY3MDAzIiwidGltZSI6MTcxNjI4OTM2OH0.XTfsp-xD8cvehBvAXsrDeEnQLhNCpGrqyDD458AZgSU',
}


async def generate_process(target_image, swap_image) -> str | bool:
    '''Возвращает ссылку на полученную фотографию'''
    headers = {
        'accept': 'application/json',
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjM2NTY2NywicHJvZHVjdF9jb2RlIjoiMDY3MDAzIiwidGltZSI6MTcxNjI4OTM2OH0.XTfs', # token invalid
    }
    files = {
        'target_image': target_image,
        'swap_image': swap_image
    }

    response = requests.post(url=api_url, headers=headers, files=files)
    print(response.text)
    #response = json.dumps('{"code":100000,"result":{"job_id":"f7c330cd-92e1-4f4b-8c4c-47648c88106b"},"message":{"en":"Request Success."}}')
    print(type(response))
    task_id = json.loads(response.content)['result']['job_id']  # просмотреть расположение ключа

    req = json.loads(requests.get(url=f'https://developer.remaker.ai/api/remaker/v1/face-swap/{task_id}', headers=headers).content)['message']['en']
    while req != 'Image generated successfully.':
        await asyncio.sleep(5)
        print('wait for generation')
        req = json.loads(requests.get(url=f'https://developer.remaker.ai/api/remaker/v1/face-swap/{task_id}', headers=headers).content)['message']['en']
        print(req)
        if req == 'Image generated failed.':
            return False

    req = requests.get(url=f'https://developer.remaker.ai/api/remaker/v1/face-swap/{task_id}', headers=headers)
    print(req.content, req.json(), sep='\n')
    if json.loads(req.content)['message']['en'] == 'Image generated successfully.':
        return json.loads(req.content)['result']['output_image_url'][0]
    else:
        raise Exception

def add_watermark(input_photo_url: str, user_id: int) -> str:
    img_data = requests.get(input_photo_url).content
    with open(f'{user_id}.png', 'wb') as handler:
        handler.write(img_data)
    out_photo = Image.open(f'{user_id}.png').convert('RGBA')
    water_mark = Image.open('IMG_8170.png').convert('RGBA')

    width = (out_photo.width - water_mark.width) // 2
    height = (out_photo.height - water_mark.height) // 2
    out_photo.paste(water_mark, (width, height), water_mark)
    out_photo.save(f'{user_id}.png')
    out_photo.close()
    return f'{user_id}.png'


