FROM python:3.12 AS requirements-stage

WORKDIR /tmp
COPY ./requirements.txt /tmp/

FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libgl1 \
      libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug", "--use-colors"]
