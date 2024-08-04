#! /bin/bash
docker rm -f fitness_data_integrator 2> /dev/null
environment="${1:-production}"
docker run -it -e FLASK_ENV=$environment -p 8888:8888 --restart always --name fitness_data_integrator fitness_data_integrator:latest