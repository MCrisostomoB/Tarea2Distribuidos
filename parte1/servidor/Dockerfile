FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y software-properties-common vim \
    && add-apt-repository universe \
    && apt-get update -y \
    && apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv \
	&& apt update\
    && pip3 install --upgrade pip

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /app
COPY . /app
CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["python3","chat_server.py"]