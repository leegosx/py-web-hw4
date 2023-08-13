FROM python:3.11.4

WORKDIR /app/

#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFEREED 1

COPY . /app/

CMD ["python", "main.py"]


