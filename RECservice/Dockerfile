FROM python:3.9
RUN apt-get update
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir app
WORKDIR /app
ENV TZ="America/New_York"
CMD ["./entrypoint.sh"]

