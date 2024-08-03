#! /bin/bash
docker rm fitness_data_integrator
docker run -it -p 8888:8888 --name fitness_data_integrator fitness_data_integrator:latest