# Dashoy

Este repositório possui os assets necessários para análise de dados de área, produtividade e produção de Soja no Brasil, assim como início do protótipo de um dashboard, utilizando a biblioteca Dash, em Python. 

## Requisitos

Este tutorial assume que o usuário utilize o sistema operacional Linux ou MacOS. Etapas abaixo podem ser adaptadas para Windows, mas não foram testadas. Caso você esteja no windows, baixe o emulador Linux no site oficial da microsoft: https://learn.microsoft.com/pt-br/windows/wsl/install. Após abrir e instalar, você terá acesso ao terminal Linux, onde poderá digitar comandos. Os passos abaixo são necessários e garantem o uso do notebook de análise pelo terminal:

1. Instale os pacotes `jupyter` e `virtualenv`: `sudo apt install jupyter virtualenv`
2. Instale o pacote `uv`: `sudo pip install uv`;
3. Crie o ambiente de desenvolvimento: `virtualenv venv`;
4. Ative o ambiente: `source venv/bin/activate`
5. Instale dependências necessárias para desenvolvimento: `uv pip install -r pesquisa/requirements.txt && uv pip install -r painel/requirements.txt` 
6. Execute o ambiente notebook: `jupyter notebook`

## Estrutura de diretórios

A estrutura abaixo organiza os arquivos e diretórios do repositório.

```
dashoy
│   README.md
└─── pesquisa
│   └───Análise climática - Soja.ipynb
└─── painel
    └───src
    └───tests
```

## Como reproduzir

Para reproduzir o painel, execute o comando abaixo. O painel estará disponível em `http://127.0.0.1:8050/`. 

    ```bash
    python painel/src/app.py
    ```

No momento, o painel encontra-se em estágio de desenvolvimento, e apresenta apenas um esboço de funcionalidades.
    
