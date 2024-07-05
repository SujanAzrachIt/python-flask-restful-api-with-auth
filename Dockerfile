ARG BASE_IMAGE_VERSION=3.12.4
FROM python:$BASE_IMAGE_VERSION-slim-bullseye as build
RUN pip install poetry

RUN apt update -qq \
    && apt install git curl gcc g++ make file musl-dev libffi-dev zlib1g zlib1g-dev libpq-dev -y

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Google Chrome PPA and install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm /etc/apt/sources.list.d/google-chrome.list && \
    rm -rf /var/lib/apt/lists/*

RUN pip install webdriver_manager

# Set up ChromeDriver path and permissions
RUN CHROMEDRIVER_PATH=$(python -c "from webdriver_manager.chrome import ChromeDriverManager; print(ChromeDriverManager().install())") && \
    chmod +x ${CHROMEDRIVER_PATH} && \
    echo "ChromeDriver installed at: ${CHROMEDRIVER_PATH}" && \
    touch /tmp/chromedriver_installed

WORKDIR /usr/src/app/

COPY pyproject.toml poetry.lock ./

RUN poetry install

Copy . .

EXPOSE 1610

ENTRYPOINT ["poetry", "run", "python", "run.py"]