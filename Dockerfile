FROM python:3.13-bullseye
WORKDIR /catalog
COPY . .
RUN pip install -ur requirements.txt
EXPOSE 8000
CMD [ "python", "-m", "manage.py", "runserver", "0.0.0.0:8000" ]