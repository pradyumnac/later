FROM python:3.11.4-slim-bullseye

# RUN apt-get update && \
#     apt-get upgrade -y --no-install-recommends && \
#     apt clean && \
#     rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8


COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

WORKDIR /code
COPY ./src /code/src
COPY ./certificates /code/certificates

RUN useradd -m -d /src -s /bin/bash app \
    && chown -R app:app /code/src/* 

USER app
ENV PATH "$PATH:/code/src"
ENV PYTHONPATH="${PYTHONPATH}:/code/src"

EXPOSE 8001
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
