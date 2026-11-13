import os
import json
import pandas as pd
import joblib
from util_func import create_embedding

jsons = os.listdir('jsons')
my_dicts = []
chunk_id = 0

for json_file in jsons:
    with open(f'jsons/{json_file}') as f:
        content = json.load(f)

    print(f"Creating Embeddings for {json_file}")
    embeddings = create_embedding([c['text'] for c in content['chunks']])

    for i, chunk in enumerate(content['chunks']):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        chunk_id += 1
        my_dicts.append(chunk)

df = pd.DataFrame(my_dicts)
# Save this dateframe
joblib.dump(df, 'embeddings_dataframe.pkl')