FROM python:3.10.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DockerHOME=/home/todo_challenge/  

WORKDIR $DockerHOME
RUN mkdir -p $DockerHOME

RUN pip3 install --upgrade pip  

COPY . $DockerHOME

RUN pip3 install -r requirements.txt  

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]