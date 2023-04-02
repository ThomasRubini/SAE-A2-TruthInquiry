FROM ubuntu:latest
MAINTAINER Djalim.S djaimS.pro@outlook.fr
RUN apt-get update -y && apt-get install -y python3-pip
WORKDIR /truthInquiry
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
