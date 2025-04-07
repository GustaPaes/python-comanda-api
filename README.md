Rodar localmente:

# Passo 1
utilizar "python .\src\main.py" na pasta raiz do projeto

# Passo 2
Para visualizar usar Swagger "http://127.0.0.1:8000/docs#/"


Para subir no Docker:


# Passo 1
docker build -t comanda-api -f DockerFile .

# Passo 2
docker login -u gustapaes

# Passo 3
docker tag comanda-api gustapaes/comanda-api

# Passo 4
docker push gustapaes/comanda-api

# Passo 5
docker run -d -it --name comanda-api -p 4443:4443 gustapaes/comanda-api