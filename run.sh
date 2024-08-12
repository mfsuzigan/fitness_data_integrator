#! /bin/bash
# Google API Credentials JSON file path must be set in the following environment variable:
# GOOGLE_API_CREDENTIALS_FILE_PATH

# For a testing execution, pass "test" as command line parameter:
#     ./run.sh test

docker rm -f fitness_data_integrator 2> /dev/null
run_environment="${1:-production}"
docker run -it -e FLASK_ENV=$run_environment -v $GOOGLE_API_CREDENTIALS_FILE_PATH:/app/resources/credentials.json -p 8888:8888 --restart always --name fitness_data_integrator fitness_data_integrator:latest
