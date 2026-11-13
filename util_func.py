import requests

def create_embedding(text_list: list[str]):
    # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
    r = requests.post("http://localhost:11434/api/embed", json={"model": "bge-m3", "input": text_list})

    if r.status_code == 200:
        return r.json()['embeddings']
    else:
        raise Exception(f"Error creating embeddings: {r.status_code} - {r.text}")


def inference(prompt: str):
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })

    response = r.json()
    return response


def create_prompt(incoming_query: str, new_df):
    prompt = f'''
    I am teaching web development in my Sigma web development course. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:
    
    {new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
    ---------------------------------
    "{incoming_query}"
    User asked this question related to the video chunks, you have to answer in a human way (dont mention the above format, its just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. If user asks unrelated question, tell him that you can only answer questions related to the course
    '''

    return prompt