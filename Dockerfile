# docker image build -t 0jsec/false_gate

# base image - must be python3.10 due to greenlet make errors
FROM python:3.10.10-bullseye

# Updatde
RUN apt-get update -y

# copy the pip requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install python dependencies with pip
RUN pip install -r requirements.txt

# Install playwright broswer & dependencies
RUN playwright install chromium
RUN playwright install-deps

# copy project to the image
COPY . /app

# set entrypoint & run
ENTRYPOINT [ "python" ]
CMD ["browser_driver.py" ]