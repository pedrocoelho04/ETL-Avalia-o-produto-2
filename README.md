# ETL-Avalia-o-produto-2
Produção de um trabalho pratico e teorico sobre o tema: Apache Hifi. Uma ferramenta responsável por realizar roteamento e automação de fluxo de dados entre diferentes sistemas.

O projeto irá procurar realizar a demonstração pratica de uma integração e sincronizazação de dados Iot's sendo enviados para o framework e sendo salvos dentro de uma base de dados estruturada.

## Tecnologias a serem utilizadas:
### Ambiente
- Docker

### Base de dados
- PostgreSQL

### Geradores de Carga e Simulação
- Pyhton

## Operando o projeto
Para iniciar o projeto com o docker:
```bash
docker compose up
```

Parar os projetos:
```bash
docker compose down
```
### Acesso
Quando tiverem subido normalmente, o nifi deve ser acessivel no link https://localhost:8443/login

#### Login e Senha default's do projeto:
##### Nifi
- Login: admin
- Senha: SenhaForte123!

##### Postgres
- Database: dbetl
- Login: admin
- Senha: segredo