FROM python:3.8-slim

# Allow service to handle stops gracefully
STOPSIGNAL SIGQUIT

# Set pip to have cleaner logs and no saved cache
ENV PIP_NO_CACHE_DIR=false \
    PIPENV_HIDE_EMOJIS=1 \
    PIPENV_IGNORE_VIRTUALENVS=1 \
    PIPENV_NOSPIN=1

# Install pipenv
RUN pip install -U pipenv

# Create the working directory
WORKDIR /xythrion

# Install packages
COPY Pipfile* ./
RUN pipenv install --system --deploy

# Copy working directory
COPY . .

ENTRYPOINT ["python"]
CMD ["-m", "xythrion"]
