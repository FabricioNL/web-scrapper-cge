# Webscrapper de Dados de Alagamento do CGE SP


![GitHub repo size](https://img.shields.io/github/repo-size/FabricioNL/web-scrapper-cge)
![GitHub](https://img.shields.io/github/license/FabricioNL/web-scrapper-cge)
![GitHub last commit](https://img.shields.io/github/last-commit/FabricioNL/web-scrapper-cge)


[<img src="https://github.com/FabricioNL.png" width="60px;"/><br /><sub><a href="https://github.com/FabricioNL">FabricioNL</a></sub>](https://github.com/FabricioNL/FabricioNL)

[<img src="https://github.com/jeansilas.png" width="60px;"/><br /><sub><a href="https://github.com/jeansilas">Jean Silas</a></sub>](https://github.com/jeansilas/jeansilas)

[<img src="https://github.com/guifl2001.png" width="60px;"/><br /><sub><a href="https://github.com/guifl2001">Guilherme Fontana</a></sub>](https://github.com/guifl2001/guifl2001)

Este é um projeto de webscrapper para coletar e armazenar dados de alagamento do Centro de Gerenciamento de Emergências (CGE) de São Paulo. Os dados históricos são extraídos de uma tabela e atualizados diariamente por meio de um script executado pelo GitHub Actions.

## Estrutura da Tabela

O banco de dados contém três tabelas: Subprefeitura, Chuvas e Alagamentos. Abaixo está a estrutura detalhada de cada tabela:

### Tabela Subprefeitura

- `id`: Identificador único da subprefeitura (chave primária).
- `nome`: Nome da subprefeitura.

### Tabela Chuvas

- `id`: Identificador único da entrada de chuva (chave primária).
- `subprefeitura_id`: ID da subprefeitura associada.
- `data`: Data da ocorrência da chuva.
- `quantidade_mm`: Quantidade de chuva em milímetros.
- `FOREIGN KEY (subprefeitura_id) REFERENCES Subprefeitura(id)`: Chave estrangeira referenciando a tabela Subprefeitura.

### Tabela Alagamentos

- `id`: Identificador único do registro de alagamento (chave primária).
- `subprefeitura_id`: ID da subprefeitura associada.
- `data`: Data da ocorrência do alagamento.
- `quantidade_alagamentos`: Quantidade de alagamentos registrados.
- `referencia`: Referência geográfica do alagamento.
- `sentido`: Sentido do alagamento (opcional).
- `rua`: Nome da rua onde ocorreu o alagamento.
- `horario_inicio`: Horário de início do alagamento.
- `horario_fim`: Horário de término do alagamento.
- `FOREIGN KEY (subprefeitura_id) REFERENCES Subprefeitura(id)`: Chave estrangeira referenciando a tabela Subprefeitura.

## Uso do Projeto

Este projeto é executado automaticamente através do GitHub Actions para atualizar os dados diariamente. Para utilizar ou contribuir com o código, siga as instruções abaixo:

1. Clone este repositório:

```bash
git clone https://github.com/seu_usuario/nome_do_repositorio.git
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o script principal:
```bash
python scrapper.py
```

Isso irá executar o script scrapper.py, que atualiza os dados do projeto. Se desejar, você pode agendar a execução deste script em seu próprio ambiente configurando um cronjob para executá-lo periodicamente.
