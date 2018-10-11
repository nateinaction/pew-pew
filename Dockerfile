FROM alpine:3.8

# Install SVN
RUN apk add --no-cache \
    bash \
    python3 \
    rsync \
    subversion

# install python dependencies
RUN pip3 install requests

# Copy WordPress theme/plugin updater
ENV APP_DIR "/app"
COPY ./validate_input.py "${APP_DIR}/"
COPY ./upload_to_svn.sh "${APP_DIR}/"

WORKDIR /workspace
ENTRYPOINT ["python3", "/app/validate_input.py"]
