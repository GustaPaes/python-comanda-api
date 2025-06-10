# API Python com FastAPI, Hypercorn e QUIC


# Rodar localmente:

## Passo 1
utilizar "python .\src\main.py" na pasta raiz do projeto

## Passo 2
Para visualizar usar Swagger "http://127.0.0.1:8000/docs#/"


## Para subir no Docker:

## Passo 1
docker build -t comanda-api -f DockerFile .

## Passo 2
docker login -u gustapaes

## Passo 3
docker tag comanda-api gustapaes/comanda-api

## Passo 4
docker push gustapaes/comanda-api

## Passo 5
docker compose up -d

## Para visualização no Docker pode ser utilizado: https://127.0.0.1:4443/docs

OBS: Alguns passos não são necessarios, desta forma estão subindo no docker local manualmente, subindo no hub do docker e também subindo usando o compose, que seria esse ultimo passo, que esta subindo completo inclusive com banco MYSQL.
