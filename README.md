<h1 align="center">
    <img alt="Previsão Deterioração" title="#PrevisaoDeterioracao" src="./assets/banner.png" />
</h1>

<p align="center">
  <a href="https://share.streamlit.io/abcp4/sepse_app/main/app.py">
    <img alt="Open in Streamlit" src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg">
  </a>
  <a href="https://api-deterioracao.herokuapp.com/docs">
      <img alt="Open in Heroku" src="https://img.shields.io/static/v1?label=Heroku&message=Open API Docs&color=green">
  </a>
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/abcp4/docker-deterioracao?color=%2304D361">
  <a href="https://github.com/abcp4/docker-deterioracao/commits/master">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/abcp4/docker-deterioracao">
  </a>
</p>

## 🔖 Visão Geral

❤️ Previsão Deterioração - é uma aplicação que utliza aprendizado de máquina para predizer a partir de dados de exames se um paciente vai melhorar ou ir a óbito.

O algoritmo considerado foi o XGBoost por ter obtido o melhor desempenho. As seguintes variáveis foram levadas em consideração para o treinamento do modelo.
- idade 
- setor
- temperatura
- frequência respiratória
- pressão arterial sistólica
- pressão arterial diastólica
- pressão arterial média
- saturação da oxigenação

Dois modelos foram treinados considerando:
- Todos os dados informados
- Ignorando a informação de setor

Foi realizada uma análise exploratória dos dados e um **notebook** detalhado encontra-se disponível em [notebooks](notebooks). Ao final foi desenvolvida uma API para entrega do modelo e uma aplicação web que permite entender quais variáveis são consideradas mais importantes na predição.

## 🛠 Tecnologias

As seguintes ferramentas foram usadas na aplicação:

- [XGBoost][docker] - algoritmo para classificação
- [Streamlit][streamlit] - para demonstração visual da predição
- [FastAPI][fastapi] - para entrega do modelo através de uma API


## :gear: Como executar o projeto

Esse projeto se encontra dividido em duas partes:
1. [API](api) - https://api-deterioracao.herokuapp.com/docs
2. [WebAPP](webapp) - https://share.streamlit.io/abcp4/sepse_app/main/app.py

### Pré-requisitos

Antes de começar, é necessário ter instalado [Git](https://git-scm.com), [Docker][docker] e [docker-compose][compose]. Caso opte por executar as aplicações separadamente, acesse a pasta [api](api) e [webapp](webapp) e siga as instruções dos READMEs de cada.

### 🎲 Rodando a aplicação

```bash
# clone este repositório
$ git clone https://github.com/abcp4/docker-deterioracao.git

# acesse a pasta do projeto
$ cd docker-deterioracao

# execute o docker-compose
$ docker-compose up --build

# A aplicação iniciará na porta:8501 - disponível em http://0.0.0.0:8501
```
A documentação da API estará disponível em http://0.0.0.0:8000/docs


[docker]: https://docs.docker.com/engine/install/
[streamlit]: https://streamlit.io/
[fastapi]: https://fastapi.tiangolo.com/
[compose]: https://docs.docker.com/compose/

