import pandas as pd

# --- 1. CARREGAR E LIMPAR O SIA (AMBULATORIAL) ---
print("⌛ Lendo SIA de Santo André...")
# O skiprows=4 pula o cabeçalho do TabNet
df_sia = pd.read_csv('sia_santo_andre_2024.csv', sep=';', encoding='iso-8859-1', skiprows=4, skipfooter=3, engine='python')

# Filtro para manter apenas a linha de Santo André
df_sia = df_sia[df_sia['Município'].str.contains('354780', na=False)]

# Transformar meses de colunas para linhas
df_sia_melted = df_sia.melt(id_vars=['Município'], var_name='Mes_Chave', value_name='Qtd_SIA')
df_sia_melted = df_sia_melted[df_sia_melted['Mes_Chave'] != 'Total']
print("✅ SIA pronto.")

# --- 2. CARREGAR E TRATAR O SIH (HOSPITALAR) ---
arquivo_sih = 'sih_sp_2024.parquet'

try:
    print(f"⌛ Lendo SIH de: {arquivo_sih}")
    df_sih_bruto = pd.read_parquet(arquivo_sih)

    # 1. Filtro de Santo André (IBGE 354780)
    # Conversão MUNIC_RES para string para garantir a comparação
    df_sih_sa = df_sih_bruto[df_sih_bruto['MUNIC_RES'].astype(str).str.contains('354780')].copy()

    # 2. Criar a coluna de data compatível com o SIA (Ex: 2024/Jan)
    mapa_meses = {
        '1': 'Jan', '2': 'Fev', '3': 'Mar', '4': 'Abr', '5': 'Mai', '6': 'Jun',
        '7': 'Jul', '8': 'Ago', '9': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez',
        '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr', '05': 'Mai', '06': 'Jun',
        '07': 'Jul', '08': 'Ago', '09': 'Set'
    }

    # Combinar ANO_CMPT + MES_CMPT transformando em string
    def formatar_data_sih(linha):
        ano = str(linha['ANO_CMPT'])
        mes_num = str(linha['MES_CMPT']).zfill(2) # dois dígitos (ex: '01')
        mes_nome = mapa_meses.get(mes_num, mes_num)
        return f"{ano}/{mes_nome}"

    df_sih_sa['Mes_Chave'] = df_sih_sa.apply(formatar_data_sih, axis=1)

    # 3. Agrupar para contar as internações por mês
    df_sih_agrupado = df_sih_sa.groupby('Mes_Chave').size().reset_index(name='Qtd_SIH')
    
    print("SIH pronto.")

    # --- 3. UNIFICAÇÃO FINAL (JOIN) ---
    df_final = pd.merge(
        df_sia_melted, 
        df_sih_agrupado, 
        on='Mes_Chave', 
        how='left'
    ).fillna(0)

    # Organizar e Renomear
    df_final = df_final[['Mes_Chave', 'Qtd_SIA', 'Qtd_SIH']]
    
    # Salvar a base mestre
    df_final.to_parquet('base_unificada_santo_andre.parquet')
    
    print("\n Base unificada gerada.")
    print(df_final)

except Exception as e:
    print(f"\n Erro no processamento: {e}")