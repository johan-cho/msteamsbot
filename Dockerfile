# syntax=docker/dockerfile:1

FROM python:3.11.4-bookworm


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r requirements.txt
COPY . .

RUN apt-get update && apt-get install -y tzdata
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["python3", "main.py"]
# CMD ["wait"]