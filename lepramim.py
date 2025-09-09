
# lepramim.py
# Conversor simples de PDF/TXT para áudio (WAV ou MP3) usando Python puro.
# Uso offline por padrão (pyttsx3). Conversão para MP3 opcional com pydub + ffmpeg.
#
# Exemplo de uso:
#   python lepramim.py entrada.pdf saida.wav
#   python lepramim.py entrada.txt saida.mp3
#
# Requisitos mínimos: pip install pyttsx3 PyPDF2
# MP3 opcional: pip install pydub && instalar ffmpeg no sistema (se desejar MP3)

import sys
import os
from pathlib import Path

def _lazy_imports():
    global pyttsx3, PdfReader
    import pyttsx3
    try:
        from PyPDF2 import PdfReader
    except Exception as e:
        print("[AVISO] PyPDF2 não disponível:", e)
        PdfReader = None
    return pyttsx3, PdfReader

def read_text_from_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        if PdfReader is None:
            raise RuntimeError("PyPDF2 não está instalado. Rode: pip install PyPDF2")
        reader = PdfReader(str(path))
        parts = []
        for page in reader.pages:
            txt = page.extract_text() or ""
            parts.append(txt)
        return "\n".join(parts).strip()
    else:
        return path.read_text(encoding="utf-8", errors="ignore").strip()

def synthesize_to_wav(text: str, out_wav: Path, rate: int = 175, voice: str = None):
    engine = pyttsx3.init()
    if rate:
        engine.setProperty("rate", rate)
    if voice:
        # Tenta selecionar voz pelo nome/id
        for v in engine.getProperty("voices"):
            if voice.lower() in (v.name or "").lower():
                engine.setProperty("voice", v.id)
                break
    engine.save_to_file(text if text else "Sem conteúdo legível.", str(out_wav))
    engine.runAndWait()

def try_convert_wav_to_mp3(wav_path: Path, mp3_path: Path) -> bool:
    try:
        from pydub import AudioSegment  # requer ffmpeg instalado no sistema
    except Exception as e:
        print("[INFO] pydub/ffmpeg não disponíveis. Mantendo WAV. Detalhe:", e)
        return False
    try:
        audio = AudioSegment.from_wav(str(wav_path))
        audio.export(str(mp3_path), format="mp3")
        return True
    except Exception as e:
        print("[INFO] Falha ao converter para MP3. Mantendo WAV. Detalhe:", e)
        return False

def main():
    _lazy_imports()
    if len(sys.argv) < 3:
        print("Uso: python lepramim.py <entrada.(pdf|txt)> <saida.(wav|mp3)> [velocidade] [voz]")
        print("Exemplo: python lepramim.py aula.pdf aula.wav 175")
        print("         python lepramim.py resumo.txt resumo.mp3 170 'brazil'")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    rate = int(sys.argv[3]) if len(sys.argv) >= 4 and sys.argv[3].isdigit() else 175
    voice = sys.argv[4] if len(sys.argv) >= 5 else None

    if not in_path.exists():
        print(f"[ERRO] Arquivo de entrada não encontrado: {in_path}")
        sys.exit(2)

    text = read_text_from_file(in_path)

    # Sempre sintetiza primeiro em WAV (compatível com pyttsx3)
    tmp_wav = out_path if out_path.suffix.lower() == ".wav" else out_path.with_suffix(".wav")
    print(f"[INFO] Sintetizando fala → {tmp_wav.name} (rate={rate}, voice={voice or 'padrão'})")
    synthesize_to_wav(text, tmp_wav, rate=rate, voice=voice)

    # Se o usuário pediu MP3, tenta converter
    if out_path.suffix.lower() == ".mp3":
        print("[INFO] Tentando converter WAV → MP3...")
        ok = try_convert_wav_to_mp3(tmp_wav, out_path)
        if ok and tmp_wav != out_path:
            try:
                os.remove(tmp_wav)
            except Exception:
                pass
        print(f"[OK] Arquivo final: {out_path if ok else tmp_wav}")
    else:
        print(f"[OK] Arquivo final: {tmp_wav}")

if __name__ == "__main__":
    main()
