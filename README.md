# Dashoy

Este repositório possui os assets necessários para análise de dados de área, produtividade e produção de Soja no Brasil, assim como início do protótipo de um dashboard, utilizando a biblioteca Dash, em Python. 

## Requisitos

Este tutorial assume que o usuário utilize o sistema operacional Linux ou MacOS. Etapas abaixo podem ser adaptadas para Windows, mas não foram testadas.

## Estrutura de diretórios

A estrutura abaixo organiza os arquivos e diretórios do repositório.

```
dashoy
│   README.md
└─── pesquisa
│   │   Análise climática - Soja.ipynb
│   └───data
│       └───soja
│       └───clima
└─── painel
    └───src
    └───tests
```

# Como reproduzir

## Pesquisa

    ### Pré-requisitos

    As bibliotecas necessárias para pesquisa encontram-se no arquivo `pesquisa/requirements.txt`.  Para instalar, execute o comando abaixo:

    ```bash
    pip install -r pesquisa/requirements.txt
    ```

    ### Reprodução

    Para reproduzir a análise de dados, execute o arquivo `pesquisa/Análise climática - Soja.ipynb` em um ambiente Jupyter Notebook. As células de código estão organizadas de forma a reproduzir a análise de dados de forma sequencial. Desta forma, execute cada célula com comando `Shift + Enter` ou `Ctrl + Enter`.

## Painel

    ### Pré-requisitos

    As bibliotecas necessárias para o painel encontram-se no arquivo `painel/requirements.txt`.  Para instalar, execute o comando abaixo:

    ```bash
    pip install -r painel/requirements.txt
    ```

    ### Reprodução

    Para reproduzir o painel, execute o arquivo `painel/src/app.py` em um ambiente Python. O painel estará disponível em `http://127.0.0.1:8050/`


