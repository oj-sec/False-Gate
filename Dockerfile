# docker image build -t 0jsec/false_gate

# base image
FROM python:3.12.0a3-bullseye

# set the display server
RUN apt-get update -y
RUN apt-get install -y xvfb
ENV DISPLAY=:1
RUN Xvfb $DISPLAY -screen $DISPLAY 1280x1024x16 &

# add chromedriver binary
ADD ./chromedriver /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver

# install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# copy the pip requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install python dependencies with pip
RUN pip install -r requirements.txt

# copy project to the image
COPY . /app

# set entrypoint & run
ENTRYPOINT [ "python" ]
CMD ["false_gate_API.py" ]