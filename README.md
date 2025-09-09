# LêPraMim – Conversor PDF/TXT → Áudio (Python)


Projeto simples de **impacto social**: converte conteúdos de estudo (PDF/TXT) em **áudio** para apoiar alunos com baixa visão, dislexia ou dificuldade de leitura. Funciona **offline** por padrão com `pyttsx3`. Opcionalmente, gera **MP3** com `pydub` + `ffmpeg`.

## Requisitos
- Python 3.9+
- `pip install -r requirements.txt`
  - Mínimo: `pyttsx3`, `PyPDF2`
  - Opcional (MP3): `pydub` + instalar `ffmpeg` no sistema

## Uso rápido
```bash
# WAV (offline, recomendado por compatibilidade)
python lepramim.py entrada.pdf saida.wav
python lepramim.py entrada.txt saida.wav

# MP3 (requer pydub + ffmpeg)
python lepramim.py entrada.pdf saida.mp3
```

Parâmetros adicionais:
```bash
python lepramim.py <entrada.(pdf|txt)> <saida.(wav|mp3)> [velocidade] [voz]
# Exemplo ajustando velocidade e tentando voz
python lepramim.py aula.pdf aula.mp3 170 brazil
```

> Dica: para listar vozes disponíveis, rode um pequeno script com `pyttsx3` e imprima `engine.getProperty("voices")`.

## Estrutura
- `lepramim.py` – script principal
- `requirements.txt` – dependências
- Relatório (PDF) do projeto com Canvas: inclua o link público no seu post do LinkedIn.

## Impacto Social
- **Acessibilidade:** transforma materiais em áudio para estudo móvel.
- **Baixo custo:** bibliotecas livres e execução offline.
- **Escala:** professores podem converter turmas inteiras rapidamente.

## Licença
MIT
