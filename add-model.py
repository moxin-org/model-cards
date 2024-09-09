import json
import sys

import urllib.request


def get_huggingface_models(repo_id):
    url = f"https://huggingface.co/api/models/{repo_id}?blobs=1"
    with urllib.request.urlopen(url) as response:
        response_data = response.read()
        response_json = json.loads(response_data)
        return response_json


def parse_to_model_cards(
    hugging_face_model,
    featured,
    model_type,
    prompt_template="llama-3-chat",
    reverse_prompt="",
    context_size=4096,
):
    org_name, model_name = hugging_face_model["id"].split("/")
    model_index = {
        "id": hugging_face_model["id"],
        "name": model_name,
        "architecture": "",
        "featured": featured,
        "model_type": model_type,
        "like_count": hugging_face_model["likes"],
        "download_count": hugging_face_model["downloads"],
    }
    files = []
    for item in hugging_face_model["siblings"]:
        if item["rfilename"].endswith(".gguf"):
            model_id = hugging_face_model["id"]
            file_size = item["size"]
            file_id = item["rfilename"]

            file = {
                "name": item["rfilename"],
                "url": f"https://huggingface.co/{hugging_face_model['id']}/resolve/main/{item['rfilename']}",
                "size": f"{file_size}",
                "quantization": "",
                "tags": [],
                "sha256": item["lfs"]["sha256"],
                "download": {
                    "default": f"https://huggingface.co/{model_id}/resolve/main/{file_id}"
                },
            }
            files.append(file)

    model_card = {
        "id": hugging_face_model["id"],
        "name": model_name,
        "author": {
            "name": org_name,
            "url": f"https://huggingface.co/{org_name}",
            "description": "",
        },
        "summary": "",
        "size": "",
        "requires": "",
        "architecture": "",
        "released_at": hugging_face_model["createdAt"],
        "files": files,
        "prompt_template": prompt_template,
        "reverse_prompt": reverse_prompt,
        "context_size": context_size,
        "metrics": {},
    }
    return model_index, model_card


def read_index(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


def rewrite_index(file_path, indexs):
    text = json.dumps(indexs, indent=4)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)


def save_model_card(model_card):
    file_path = f"./{model_card['id']}.json"
    text = json.dumps(model_card, indent=4)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
    pass


file_path = "./index.json"
model_id = sys.argv[1]
prompt_template = sys.argv[2]

indexs = read_index(file_path)

model_index, model_card = parse_to_model_cards(
    get_huggingface_models(model_id), True, "chat", prompt_template=prompt_template
)

indexs.append(model_index)
save_model_card(model_card)
rewrite_index(file_path, indexs)
