# docker build -t audio-engine .
# docker run --rm --device /dev/snd audio-engine -c --set text='Hello, My name is Paul.' --set filename='hello.wav' --set vm='en_US-hfc_male-medium'
ARG CERTS=default

FROM python:3.11-bookworm AS ssl_default

FROM ssl_default AS ssl_zscaler
COPY --from=certs . ./certs
RUN cp ./certs/zscaler.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

FROM ssl_${CERTS} AS builder
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# simpleaudio & pydub audio player requires alsa-utils, portaudio19-dev, ffmpeg 
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y alsa-utils portaudio19-dev ffmpeg && rm -rf /var/lib/apt/lists/*
# vlc audio player requires vlc, libvlc-dev
# RUN apt update -y && apt upgrade -y && apt install -y vlc libvlc-dev
RUN python -m pip install --upgrade pip && python -m pip install --no-compile --no-cache-dir -r requirements.txt 

# base to speed up the build when only src changes
FROM python:3.11-slim-bookworm AS base
WORKDIR /app
COPY data ./data
COPY voices ./voices
COPY schema ./schema
# simpleaudio & pydub audio player requires alsa-utils, portaudio19-dev, ffmpeg 
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y alsa-utils portaudio19-dev ffmpeg && rm -rf /var/lib/apt/lists/*
# vlc audio player requires vlc, libvlc-dev
# RUN apt update -y && apt upgrade -y && apt install -y vlc libvlc-dev

FROM base AS final

LABEL org.opencontainers.image.source=https://github.com/aaron97neu/Discovery-World-Pong
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /app
COPY . .
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["python", "audio_engine.py"]
