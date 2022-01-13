FROM python:3.9.6-slim

# Allow service to handle stops gracefully
STOPSIGNAL SIGQUIT

# Set pip to have cleaner logs and no saved cache
ENV PIP_NO_CACHE_DIR=false \
    POETRY_HOME="/opt/poetry"

# Install poetry
RUN pip install -U poetry

# Create the working directory
WORKDIR /xythrion

# Install packages
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy working directory
COPY . .

CMD ["poetry", "run", "python", "-m", "xythrion"]
