import random
import requests
from faker import Faker

fake = Faker()

url = 'http://localhost:8443/requests'

print("\n Iniciando geração de requisições de usuarios - Pressione Crtl+C para parar...")

try: 
    while True:
        payload = {
            "id-sensor": f"sensor-{random.randint(100, 105)}",
            "localizacao": fake.city(),
            "latitude": random.randint(-90, 90),
            "longitude": random.randint(-180, 180),
            "data": fake.date(),
            "hora": fake.hour(),
        }
        
        response = requests.post(url, json=payload, timeout=5)
        
        if response.status_code == 201 or response.status_code == 200:
            print("Entidade enviada com sucesso")
        else:
            print("Falha no envio do pacote")
            print
            print(response.json())

except KeyboardInterrupt:
    print("\nGerador de requisições de usuarios parada")