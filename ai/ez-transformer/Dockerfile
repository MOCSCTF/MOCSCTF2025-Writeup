FROM python:3.10-slim

WORKDIR /app

COPY ./src /app
COPY flag.txt /flag.txt

RUN pip install --no-cache-dir gradio transformers torch

EXPOSE 7860

CMD ["python", "chall.py"]
