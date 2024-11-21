# !pip install openai openai-whisper pytubefix pydub ffmpeg

from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment
import os
import whisper
import uuid

def generate_transcript_from_url(url):

  unique_id = str(uuid.uuid4())[:8]  # Shorten UUID for brevity
  m4a_file = f"{unique_id}"
  wav_file = f"{unique_id}.wav"
  # Download audio file from youtube
  yt = YouTube(url, on_progress_callback=on_progress)
  print(yt.title)
  ys = yt.streams.get_audio_only()
  ys.download(filename=m4a_file)

  # Convert the downloaded .m4a file to .wav
  #wav_file = os.path.splitext(m4a_file)[0] + ".wav"
  audio = AudioSegment.from_file(f"{m4a_file}.m4a", format="m4a")
  audio.export(wav_file, format="wav")
  print(f"Conversion complete! File saved as {wav_file}")

  # Transcribe audio using Whisper model
  model = whisper.load_model("base")
  result = model.transcribe(wav_file)
  print("Transcript:")
  print(result["text"])

  # Step 4: Auto-delete the audio files
  os.remove(f"{m4a_file}.m4a")
  os.remove(wav_file)
  print(f"Temporary files deleted: {m4a_file}.m4a, {wav_file}")

  return result["text"]
