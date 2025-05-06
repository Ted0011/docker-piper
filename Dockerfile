FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    alsa-utils \
    libasound2 \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install flask flask-cors
COPY asound.conf /etc/asound.conf
EXPOSE 8080 5000

CMD bash -c "python3 app.py & python3 -m http.server 8080"
