FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn

ARG APP_VERSION=unknown
ENV APP_VERSION=$APP_VERSION

COPY main.py .

ENV PORT=8080
EXPOSE $PORT

CMD ["python", "main.py"]
