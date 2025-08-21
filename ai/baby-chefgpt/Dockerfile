FROM python:3.10-slim

WORKDIR /app

COPY ./src /app

RUN pip install openai
RUN pip install gradio

EXPOSE 9999

CMD ["python", "chall.py"]