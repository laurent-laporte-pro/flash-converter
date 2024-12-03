import torch
from pydub import AudioSegment


def detect_voice_segments(audio_file, output_format="mp3", threshold=0.6):
    """
    Détecte les passages contenant de la voix dans un fichier audio.

    :param audio_file: Chemin du fichier audio à analyser.
    :param output_format: Format des extraits générés (mp3 ou raw).
    :param threshold: Seuil de confiance pour considérer un segment comme contenant de la voix.
    :return: Liste des segments détectés avec leurs timecodes.
    """
    # Charger le modèle Silero VAD
    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
    get_speech_timestamps, sauve_audio, read_audio, VADIterator, collect_chunks = utils

    # Lire l'audio
    wav = read_audio(audio_file, sampling_rate=16000)
    speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=16000, threshold=threshold)

    # Charger l'audio avec pydub pour extraction
    audio = AudioSegment.from_file(audio_file)

    # Extraire les segments
    segments = []
    for i, ts in enumerate(speech_timestamps):
        start_ms = ts['start'] * 1000 // 16000 - 500  # Décaler le début de 500ms
        end_ms = ts['end'] * 1000 // 16000 + 500  # Décaler la fin de 500ms
        segment = audio[start_ms:end_ms]
        segments.append({
            "start_time": start_ms / 1000,
            "end_time": end_ms / 1000,
            "file": f"segment_{i + 1}.{output_format}"
        })
        # Sauvegarder l'extrait
        segment.export(f"segment_{i + 1}.{output_format}", format=output_format)

    return segments


def main():
    # Exemple d'utilisation
    audio_file = "/Users/laurent/Desktop/IMG_3806.mp3"
    segments = detect_voice_segments(audio_file)

    for segment in segments:
        print(f"Voix détectée de {segment['start_time']}s à {segment['end_time']}s, extrait : {segment['file']}")


if __name__ == '__main__':
    main()
