# syntax=docker/dockerfile:1
FROM python:3.6.10

# Install Chromedriver
RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

# Put Chromedriver into the PATH
ENV PATH /chromedriver:$PATH

# set a directory for the app
WORKDIR /app

# copy requirements.txt
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# copy all the files to the container
COPY . .

# set env variables
ENV MONGODB_DATABASE=quotes_db

# tell the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "main.py"]
