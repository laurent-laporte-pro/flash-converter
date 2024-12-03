import whisper

# Charger le modèle Whisper (taille 'base' ou 'large' pour plus de précision)
model = whisper.load_model("base")

# Transcrire l'audio et générer des sous-titres
audio_file = "/Users/laurent/Desktop/IMG_3806.mp3"
result = model.transcribe(audio_file, task="transcribe", language="fr")


def format_time(seconds):
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes = seconds // 60
    hours = minutes // 60
    seconds = seconds % 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"


# Sauvegarder en fichier SRT
with open("subtitles.srt", "w", encoding="utf-8") as f:
    for i, segment in enumerate(result["segments"]):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        f.write(f"{i + 1}\n")
        f.write(f"{format_time(start)} --> {format_time(end)}\n")
        f.write(f"{text}\n\n")
