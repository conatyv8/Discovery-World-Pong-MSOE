# This dockerfile was quickly made to dockerize the application it has not been optimized.
ARG CERTS=default

FROM python:3.8-slim-bookworm AS ssl_default

FROM ssl_default AS ssl_zscaler
COPY --from=certs . ./certs
RUN cp ./certs/zscaler.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

FROM ssl_${CERTS} AS builder

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY --from=util . ./shared

COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN python -m pip install --upgrade pip && python -m pip install --no-compile --no-cache-dir -r requirements.txt 

FROM python:3.8-slim-bookworm AS final

LABEL org.opencontainers.image.source=https://github.com/aaron97neu/Discovery-World-Pong
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /app

COPY --from=builder /app .
COPY --from=builder /opt/venv /opt/venv
COPY --from=models . visualizer/models/

COPY . .

ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "visualization_driver.py"]


