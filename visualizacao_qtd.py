import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. CARREGAR OS DADOS 
try:
    df_final = pd.read_parquet('base_unificada_santo_andre.parquet')
    print("Dados carregados com sucesso!")
except FileNotFoundError:
    print("Erro: O arquivo não foi encontrado.")
    print("Certifique-se de rodar o script de tratamento primeiro.")
    exit()

# 2. Design Grafico
sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(14, 7))

# 3. EIXO 1: Produção Ambulatorial (SIA) - Barras
color_sia = 'skyblue'
ax1.set_xlabel('Mês de 2024', fontsize=12)
ax1.set_ylabel('Quantidade SIA (Ambulatorial)', color='tab:blue', fontsize=12)
sns.barplot(x='Mes_Chave', y='Qtd_SIA', data=df_final, color=color_sia, ax=ax1)
ax1.tick_params(axis='y', labelcolor='tab:blue')

# 4. EIXO 2: Internações (SIH) - Linha
ax2 = ax1.twinx()  # Cria o eixo secundário
color_sih = 'darkred'
ax2.set_ylabel('Quantidade SIH (Hospitalar)', color=color_sih, fontsize=12)
sns.lineplot(x='Mes_Chave', y='Qtd_SIH', data=df_final, color=color_sih, marker='o', linewidth=3, ax=ax2)
ax2.tick_params(axis='y', labelcolor='darkred')

# 5. FINALIZAÇÃO
plt.title('Produção de Saúde em Santo André (2024): Ambulatorial vs Hospitalar', fontsize=16, pad=20)
fig.tight_layout()

# Salvar gráfico
plt.savefig('grafico_saude_santo_andre.png', dpi=300)
print("Gráfico gerado e salvo como 'grafico_saude_santo_andre.png'")

plt.show()