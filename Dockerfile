FROM ubuntu:22.04
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y python3 && apt-get install -y python3-pip
RUN pip install -r BS/requeriments.txt
CMD ["python3", "BS/run.py"]
