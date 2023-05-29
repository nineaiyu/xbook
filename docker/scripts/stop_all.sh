#!/bin/bash
#
#


cd ../nginx/ && docker compose down

cd ../xbook/ && docker compose down

cd ../redis/ && docker compose down

cd ../mariadb/ && docker compose down
