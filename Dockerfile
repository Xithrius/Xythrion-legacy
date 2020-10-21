FROM python:3.8

# Allow service to handle stops gracefully
STOPSIGNAL SIGQUIT

# Set pip to have cleaner logs and no saved cache
ENV PIP_NO_CACHE_DIR=false \
    PIPENV_HIDE_EMOJIS=1 \
    PIPENV_IGNORE_VIRTUALENVS=1 \
    PIPENV_NOSPIN=1

# Copy the project files into working directory
WORKDIR /xythrion
COPY . .

# Install git
RUN apt update -y && apt install -y git

RUN pip install -U pipenv && pipenv install --system --deploy
#RUN pip install -U pipenv && pipenv install --system --deploy

ENTRYPOINT ["python"]
CMD ["-m", "xythrion"]
