# Model cards

Add a new model card. You need to give the `model-id`, `prompt-template` and `context-size`.

```
python3 model_cli.py add second-state/Meta-Llama-3.1-8B-Instruct-GGUF llama-3-chat 131072
```

Remove a model from `index.json` but leave it in the model cards.

```
python3 model_cli.py delete second-state/Meta-Llama-3.1-8B-Instruct-GGUF
```

Sync models in `index.json` for download and like stats.

```
python3 sync-model.py
```
