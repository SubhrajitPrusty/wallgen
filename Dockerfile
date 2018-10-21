FROM ubuntu:latest
MAINTAINER Subhrajit Prusty "subhrajit1997@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
ADD . /wallgen
WORKDIR /wallgen
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]

