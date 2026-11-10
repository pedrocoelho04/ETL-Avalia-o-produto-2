import datetime
import random
import time

import requests
from faker import Faker


def log(msg):
    print(msg, flush=True)


fake = Faker()

URL_NIFI = "http://localhost:8080/contentListener"

log("\nIniciando geracao de leituras de sensores - Pressione Ctrl+C para parar...")

try:
    while True:
        payload = {
            "id_sensor": f"sensor-{random.randint(100, 105)}",
            "localizacao": fake.city(),
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6),
            "data": (datetime.date.today() - datetime.timedelta(days=random.randint(0, 365))).isoformat(),
            "hora": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}",
        }

        try:
            response = requests.post(URL_NIFI, json=payload, timeout=5)
        except requests.ConnectionError:
            log("\n[Nao conectado] NiFi ListenHTTP nao esta no ar na porta 8080.")
            log("Configure o fluxo (ListenHTTP -> PutDatabaseRecord), inicie os")
            log("processadores e salve o fluxo. Tentando novamente em 10s...\n")
            time.sleep(10)
            continue

        if response.status_code in (200, 201):
            log(f"\n[{payload['id_sensor']}] leitura enviada com sucesso "
                f"(HTTP {response.status_code}) - {payload}")
        else:
            log(f"\nFalha no envio do pacote (HTTP {response.status_code})")
            try:
                log(response.json())
            except ValueError:
                log(response.text)

        time.sleep(random.uniform(1, 3))

except KeyboardInterrupt:
    log("\nGerador de leituras de sensores parado.")