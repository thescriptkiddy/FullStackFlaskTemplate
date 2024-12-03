FROM ubuntu:latest
LABEL authors="simonhardt"

ENTRYPOINT ["top", "-b"]