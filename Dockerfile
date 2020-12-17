FROM python:3.10.0a3-alpine3.12

# set work directory
WORKDIR /usr/src/app

# update programs
RUN apk update && apk add postgresql-dev gcc python3-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["python","/usr/src/app/main.py"]