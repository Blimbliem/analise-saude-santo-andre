import pandas as pd

# --- CONFIGURAÇÃO DE NOMES ---
file_sia_qtd = 'sia_santo_andre_2024.csv'
file_sia_val = 'sia_santo_andre_valor_2024.csv'
file_sih_parquet = 'sih_sp_2024.parquet'

def carregar_tabnet(arquivo, nome_coluna):
    # Lendo o CSV ignorando o lixo do cabeçalho e rodapé
    df = pd.read_csv(arquivo, sep=';', encoding='iso-8859-1', skiprows=4, skipfooter=3, engine='python')
    
    # Filtro de Santo André
    df = df[df['Município'].str.contains('354780', na=False)]
    
    # Transformação de colunas em linhas
    df_melted = df.melt(id_vars=['Município'], var_name='Mes_Chave', value_name=nome_coluna)
    df_melted = df_melted[df_melted['Mes_Chave'] != 'Total']
    
    # --- LIMPEZA NUMÉRICA ---
    # 1. Converte para string 
    # 2. Remove o ponto de milhar
    # 3. Substitui a vírgula decimal por ponto
    # 4. Converte para float numérico
    df_melted[nome_coluna] = (
        df_melted[nome_coluna]
        .astype(str)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
    )
    df_melted[nome_coluna] = pd.to_numeric(df_melted[nome_coluna], errors='coerce').fillna(0)
    
    return df_melted

# 1. Carregar SIA (Ambulatorial)
print("⌛ A processar dados do SIA...")
df_sia_qtd = carregar_tabnet(file_sia_qtd, 'Qtd_SIA')
df_sia_val = carregar_tabnet(file_sia_val, 'Valor_SIA')
df_sia_final = pd.merge(df_sia_qtd, df_sia_val, on=['Município', 'Mes_Chave'])

# 2. Carregar SIH (Hospitalar)
print("⌛ A processar dados do SIH...")
df_sih_bruto = pd.read_parquet(file_sih_parquet)
df_sih_sa = df_sih_bruto[df_sih_bruto['MUNIC_RES'].astype(str).str.contains('354780')].copy()

mapa_meses = {'01':'Jan','02':'Fev','03':'Mar','04':'Abr','05':'Mai','06':'Jun',
              '07':'Jul','08':'Ago','09':'Set','10':'Out','11':'Nov','12':'Dez'}

def formatar_data(row):
    mes = str(row['MES_CMPT']).zfill(2)
    return f"{row['ANO_CMPT']}/{mapa_meses.get(mes, mes)}"

df_sih_sa['Mes_Chave'] = df_sih_sa.apply(formatar_data, axis=1)

# Agrupamento Hospitalar (Soma de VAL_TOT e contagem de internações)
df_sih_agrupado = df_sih_sa.groupby('Mes_Chave').agg(
    Qtd_SIH=('VAL_TOT', 'size'),
    Valor_SIH=('VAL_TOT', 'sum')
).reset_index()

# 3. Unificação Final
print("🚀 A criar a base mestre unificada...")
df_final = pd.merge(df_sia_final, df_sih_agrupado, on='Mes_Chave', how='left').fillna(0)

# 4. Cálculo de Custo Médio 
df_final['Custo_Medio_SIA'] = df_final['Valor_SIA'] / df_final['Qtd_SIA']
df_final['Custo_Medio_SIH'] = df_final['Valor_SIH'] / df_final['Qtd_SIH']

# Tratamento para evitar divisão por zero (NaN -> 0)
df_final = df_final.fillna(0)

df_final.to_parquet('base_completa_santo_andre_2024.parquet')
print("\n🏆 SUCESSO! Base unificada e financeira gerada.")
print(df_final[['Mes_Chave', 'Valor_SIA', 'Valor_SIH', 'Custo_Medio_SIH']].head())