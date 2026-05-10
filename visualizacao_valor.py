import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar dados
df = pd.read_parquet('base_completa_santo_andre_2024.parquet')

sns.set_theme(style="white") # Estilo mais limpo
fig, ax1 = plt.subplots(figsize=(14, 8))

# --- GRÁFICO 1: CUSTO TOTAL (BARRAS) ---
color_bar = '#D3D3D3' # Cinza claro para não brigar com a linha
sns.barplot(x='Mes_Chave', y='Valor_SIH', data=df, color=color_bar, ax=ax1, alpha=0.6)
ax1.set_ylabel('Gasto Total Mensal (R$)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Mês de Processamento 2024', fontsize=12)

# --- GRÁFICO 2: CUSTO MÉDIO (LINHA) ---
ax2 = ax1.twinx()
sns.lineplot(x='Mes_Chave', y='Custo_Medio_SIH', data=df, marker='o', 
             color='#B22222', linewidth=4, markersize=10, ax=ax2)
ax2.set_ylabel('Custo Médio por Internação (R$)', color='#B22222', fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#B22222')
ax2.set_ylim(df['Custo_Medio_SIH'].min() * 0.8, df['Custo_Medio_SIH'].max() * 1.2)

for i, row in df.iterrows():
    ax2.annotate(f'R$ {row["Custo_Medio_SIH"]:.0f}', 
                 xy=(i, row["Custo_Medio_SIH"]),
                 xytext=(0, 15), # Move o texto 15 pontos para cima
                 textcoords='offset points',
                 ha='center',
                 va='bottom',
                 fontsize=10,
                 fontweight='bold',
                 color='#B22222',
                 bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#B22222', alpha=0.7))

plt.title('Análise de Eficiência Hospitalar: Santo André (2024)\nVolume de Gastos vs. Complexidade por Paciente', 
          fontsize=16, fontweight='bold', pad=25)

# Remover grades desnecessárias para clareza
ax1.grid(False)
ax2.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('analise_hospitalar_limpa.png', dpi=300)
plt.show()