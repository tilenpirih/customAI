FROM python:3.10.13-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends wget gnupg && \
#     echo "deb http://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
#     wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
#     apt-get update && \
#     apt-get install -y --no-install-recommends \
#     ffmpeg \
#     ghostscript \
#     postgresql-client-17 \
#     && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["./entrypoint.sh"]