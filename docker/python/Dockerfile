FROM python:3.10-slim
LABEL maintainer="serfer2@protonmail.com"
ENV PYTHONPATH=/app \
    TZ='Europe/Madrid' \
    PYTHONUNBUFFERED=1
RUN rm /etc/localtime \
    && ln -s /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo "${TZ}" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata
COPY . /app
ENV BASE_DIR=/app
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
