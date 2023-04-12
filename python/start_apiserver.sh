# starts the api server with gunicorn

export $(grep -v '^#' .env | xargs)

gunicorn -b ${APISERVER_HOST}:${APISERVER_PORT} --log-level debug -w 10 apiserver:app