print("SCRIPT INICIADO")

import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================
# 1. Carregar base de dados
# =========================

df = pd.read_csv("data/transacoes_pix.csv")

# =========================
# 2. Regras de detecção de fraude
# =========================

alertas = []

for index, row in df.iterrows():

    if row["valor"] > 5000 and row["dispositivo_novo"] == 1:
        alertas.append("RISCO_ALTO")

    elif row["valor"] > 3000 and row["hora"] >= 22:
        alertas.append("RISCO_MEDIO")

    else:
        alertas.append("NORMAL")

df["classificacao"] = alertas

# =========================
# 3. Mostrar dados analisados
# =========================

print("\nDados analisados:")
print(df)

# =========================
# 4. Resumo de classificação
# =========================

print("\nResumo de risco:")
print(df["classificacao"].value_counts())

# =========================
# 5. Indicadores de fraude
# =========================

total_transacoes = len(df)

fraudes_altas = len(df[df["classificacao"] == "RISCO_ALTO"])
fraudes_medias = len(df[df["classificacao"] == "RISCO_MEDIO"])

taxa_fraude = (fraudes_altas + fraudes_medias) / total_transacoes * 100

print("\nIndicadores de risco:")
print("Total de transações:", total_transacoes)
print("Transações risco alto:", fraudes_altas)
print("Transações risco médio:", fraudes_medias)
print(f"Taxa de transações suspeitas: {taxa_fraude:.2f}%")

# =========================
# 6. Análise por cooperado
# =========================

print("\nTransações por cooperado:")

transacoes_cooperado = df.groupby("cooperado")["valor"].agg([
    "count",
    "sum",
    "mean"
])

print(transacoes_cooperado)

# =========================
# 7. Detecção comportamental
# =========================

df["transacao_alta"] = df["valor"] > 3000

alerta_comportamental = (
    df.groupby("cooperado")["transacao_alta"]
    .sum()
    .reset_index()
)

suspeitos = alerta_comportamental[alerta_comportamental["transacao_alta"] >= 2]

print("\nCooperados com múltiplas transações altas:")
print(suspeitos)

# =========================
# 8. Score de risco por transação
# =========================

df["score_risco"] = 0

for index, row in df.iterrows():

    score = 0

    if row["valor"] > 5000:
        score += 50

    elif row["valor"] > 3000:
        score += 30

    if row["hora"] >= 22:
        score += 20

    if row["dispositivo_novo"] == 1:
        score += 20

    if row["chave_nova"] == 1:
        score += 10

    df.loc[index, "score_risco"] = score

print("\nScore de risco das transações:")
print(df[["id", "cooperado", "valor", "score_risco"]])

# =========================
# 9. Ranking de cooperados suspeitos
# =========================

ranking_risco = df.groupby("cooperado")["score_risco"].sum().sort_values(ascending=False)

print("\nRanking de cooperados por risco:")
print(ranking_risco)

# =========================
# 10. Gráfico de classificação
# =========================

df["classificacao"].value_counts().plot(kind="bar")

plt.title("Distribuição de classificação de risco")
plt.xlabel("Classificação")
plt.ylabel("Quantidade")

plt.show()

# =========================
# 11. Fraudes por horário
# =========================

fraudes = df[df["classificacao"] != "NORMAL"]

fraudes.groupby("hora").size().plot(kind="bar")

plt.title("Fraudes por horário")
plt.xlabel("Hora")
plt.ylabel("Quantidade")

plt.show()

# =========================
# 12. Salvar gráfico para README
# =========================

plt.figure()

df["classificacao"].value_counts().plot(kind="bar")

plt.title("Distribuição de risco das transações PIX")
plt.xlabel("Classificação")
plt.ylabel("Quantidade")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
grafico = os.path.join(BASE_DIR, "grafico_risco.png")

plt.savefig(grafico)

# =========================
# 13. Salvar resultado final
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
caminho = os.path.join(BASE_DIR, "data", "transacoes_analisadas.csv")

df.to_csv(caminho, index=False)

print("\nArquivo salvo em:")
print(caminho)