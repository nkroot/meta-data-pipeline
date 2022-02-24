FROM python:3.9.5-alpine
#3.9-slim-buster
#3.8.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apk update
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev\
    libc-dev \
    libffi-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
#Change the location accordingly to populate the data
CMD ["python","main.py","40.741895","-73.989308"]
