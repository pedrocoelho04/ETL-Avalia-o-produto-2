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

### Portas do projeto
| Porta | Servico |
|---|---|
| 8443 | UI / API do NiFi (https) |
| 8080 | ListenHTTP — entrada dos dados dos sensores |
| 5434 | PostgreSQL (mapeada para a 5432 interna; 5432/5433 ja estavam em uso na maquina) |

### Simulador de sensores
```bash
pip install -r requirements.txt
python3 sensor_simulador.py
```
Confira os dados no banco:
```bash
docker exec postgres-container psql -U admin -d dbetl \
  -c "SELECT * FROM sensor_readings ORDER BY id DESC LIMIT 5;"
```