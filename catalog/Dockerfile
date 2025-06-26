FROM python:3.13-bullseye
WORKDIR /catalog
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD [ "python", "-m", "manage.py", "runserver", "0.0.0.0:8080"]