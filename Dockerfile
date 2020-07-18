FROM python:3.8

# Set pip to have cleaner logs and no saved cache
ENV PIP_NO_CACHE_DIR=false \
    PIPENV_HIDE_EMOJIS=1 \
    PIPENV_IGNORE_VIRTUALENVS=1 \
    PIPENV_NOSPIN=1

# Install git
# RUN apt-get -y update && \
    # apt-get install -y git

# Install postgres
# RUN command

# Install pipenv
RUN pip install -U pipenv

# Copy the project files into working directory
WORKDIR /xythrion
COPY . .

# Install project dependencies
RUN pipenv install --deploy --system

ENTRYPOINT ["python"]
CMD ["-m", "xythrion"]

# Define docker persistent volumes
VOLUME /Xythrion/xythrion/log /xythrion/data
