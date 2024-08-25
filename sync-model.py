import json

import urllib.request
import urllib.parse

def read_and_serialize_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def get_huggingface_models(repo_id):
    url = f"https://huggingface.co/api/models/{repo_id}"
    with urllib.request.urlopen(url) as response:
        response_data = response.read()
        response_json = json.loads(response_data)
        return response_json

file_path = './index.json'
indexs = read_and_serialize_json(file_path)


i = 0
total = len(indexs)
for index in indexs:
    print(f"index {i}/{total}")
    if index['model_type']=='instruct' or index['model_type']=='chat':
        try:
            remote_index = get_huggingface_models(index['id'])
            index['like_count'] = remote_index['likes']
            index['download_count'] = remote_index['downloads']
        except Exception as e:
            pass
    i+=1


text = json.dumps(indexs,indent=4)

with open(file_path, 'w', encoding='utf-8') as file:
    file.write(text)
