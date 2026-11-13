from sklearn.metrics.pairwise import cosine_similarity
from util_func import create_embedding, inference, create_prompt
import joblib
import numpy as np

df = joblib.load('embeddings_dataframe.pkl')

incoming_query = input("Ask a Question:")
question_embedding = create_embedding([incoming_query])[0]

similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
top_results = 5
max_indx = similarities.agrsort()[::-1][:top_results]
new_df = df.loc[max_indx]

prompt = create_prompt(incoming_query, new_df)

with open("prompt.txt", "w") as f:
    f.write(prompt)

response = inference(prompt)["response"]
with open("response.text", "w") as f:
    f.write(response)