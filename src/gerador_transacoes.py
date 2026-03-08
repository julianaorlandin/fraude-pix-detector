import pandas as pd
import random

print("Gerando transações simuladas...")

dados = []

for i in range(10000):

    transacao = {
        "id": i + 1,
        "cooperado": random.randint(100, 500),
        "valor": random.randint(10, 10000),
        "hora": random.randint(0, 23),
        "dispositivo_novo": random.choice([0, 1]),
        "chave_nova": random.choice([0, 1])
    }

    dados.append(transacao)

df = pd.DataFrame(dados)

df.to_csv("data/transacoes_pix.csv", index=False)

print("Arquivo de transações criado com sucesso!")