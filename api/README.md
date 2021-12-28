# API Preditividade Óbito 🩺

Esta API serve um modelo de *machine learning* que prediz se um paciente obteve melhora ou veio a óbito a partir das seguintes informações:

- idade 
- setor
- temperatura
- frequência respiratória
- pressão arterial sistólica
- pressão arterial diastólica
- pressão arterial média
- saturação da oxigenação

Uma análise exploratória dos dados encontra-se disponível em [notebooks](../notebooks).



## :hammer_and_wrench: Como executar o projeto

Essa API foi desenvolvida com a biblioteca FastAPI, e necessita de algumas configurações básicas para executar.

### Pré-requisitos

Antes de começar é necessário possuir o Python 3 instalado em seu sistema operacional, de preferência a versão 3.9, além disso é necessário o [Git](https://git-scm.com/) para realizar os passos abaixo. 

> É possível também executar a aplicação através do docker.

### :spider_web: Rodando a aplicação

#### :snake: Opção 1: Python

```bash
# clone este repositório
$ git clone https://github.com/abcp4/docker-deterioracao.git

# acesse a pasta do projeto
$ cd docker-deterioracao

# em seguida acessa a pasta da api
$ cd api

# instale as dependências necessárias
$ pip install -r requirements.txt

# execute a aplicação
$ uvicorn main:app --reload
```

#### :whale2: Opção 2: Docker

```
# clone este repositório
$ git clone https://github.com/abcp4/docker-deterioracao.git

# acesse a pasta do projeto
$ cd docker-deterioracao

# em seguida acessa a pasta da api
$ cd api

# construir a imagem docker
$ docker build -t api-deterioracao:latest .

# executar imagem
$ docker run --env PORT=8000 -p 8000:8000 api-deterioracao:latest
```

O servidor iniciará na porta:8000 e a documentação estará acessível em http://localhost:8000/docs.
