import whisper
import json
import os

model = whisper.load_model("large-v2")

def create_chunks_with_metadata(result: dict, number: str, title: str) -> dict:
    """
    Create a dictionary containing chunks of transcribed text along with metadata.
    """
    chunks = []
    for segment in result["segments"]:
        chunks.append({
            "number": number, 
            "title": title, 
            "start": segment["start"], "end": segment["end"],
            "text": segment["text"]
        })

    chunks_with_metadata = {"chunks": chunks, "text": result["text"], "language": result["language"]}
    return chunks_with_metadata


def transcribe_audio_to_json(audio_file: str, output_dir: str) -> None:
    """
    Transcribe an audio file to text using the Whisper model and save the transcription in JSON format.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if ("_" in audio_file):
        number = audio_file.split("_")[0]
        title = audio_file.split("_")[1].replace(".mp3", "")

        print(f"Transcribing audio file: {audio_file} with number:{number} and title: {title}")
        result = model.transcribe(audio_file, language="hi", task="translate", word_timestamps=False) 

        chunks_with_metadata = create_chunks_with_metadata(result, number, title)
        with open(f"{output_dir}/{audio_file.replace('.mp3', '.json')}", 'w') as f:
            json.dump(chunks_with_metadata, f)


audios = os.listdir('audios')
for audio_file in audios:
    transcribe_audio_to_json(f"audios/{audio_file}", "transcriptions")