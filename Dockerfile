# Pull base image
FROM yangpeilyn/rires_indri_base:latest

MAINTAINER Peilin Yang yangpeilyn@gmail.com

ADD ./eval.py /home/MinRunQuery/
WORKDIR /home/MinRunQuery/
RUN mkdir -p /results/
ENTRYPOINT ["python", "eval.py"]
#ENTRYPOINT ["./runquery/IndriRunQuery", "title_425"]
