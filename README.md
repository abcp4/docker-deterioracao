<h1 align="center">
    <img alt="Previsão Deterioração" title="#PrevisaoDeterioracao" src="./assets/banner.png" />
</h1>

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
1. API
2. WebAPP

### Pré-requisitos

Antes de começar,  é necessário ter instalado [Git](https://git-scm.com), [Docker][docker] e [docker-compose][compose] . Caso opte por executar as aplicações separadamente, acesse a pasta `api` e `webapp` e siga as instruções dos READMEs de cada.

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

