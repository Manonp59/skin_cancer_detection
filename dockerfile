FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

COPY . .

CMD ["streamlit", "run", "streamlit.py", "--server.address", "0.0.0.0", "--server.port", "80"]