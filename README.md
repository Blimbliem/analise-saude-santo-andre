# Análise de Saúde Pública: Santo André (2024) 🏥📊

Este projeto realiza a extração, tratamento e unificação de dados do **SIA** (Sistema de Informações Ambulatoriais) e **SIH** (Sistema de Informações Hospitalares) do DATASUS, com foco no município de **Santo André - SP**.

O objetivo principal é correlacionar o volume de atendimentos ambulatoriais com as internações hospitalares e seus respectivos custos operacionais durante o ano de 2024.

## 🚀 Desafios Técnicos Superados
- **Processamento de Dados Públicos:** Conversão e limpeza de arquivos extraídos do TabNet (CSV com codificação ISO-8859-1 e formatação brasileira).
- **Unificação de Bases:** Cruzamento de dados de microdados hospitalares (Parquet) com dados consolidados ambulatoriais.
- **Data Tidying:** Transformação de estruturas *Wide* para *Long* para viabilizar séries temporais.

## 🛠️ Tecnologias Utilizadas
- **Python 3.13**
- **Pandas:** Manipulação e limpeza de dados.
- **Seaborn & Matplotlib:** Visualização de dados e criação de dashboards.
- **Pyarrow:** Engine para processamento de arquivos Parquet de alta performance.

## 📂 Estrutura do Projeto
- `tratamento_qtd_valor.py`: Script de ETL que limpa os dados do SIA, filtra o SIH por código IBGE (354780) e gera a base mestre unificada.
- `visualizacao.py`: Dashboard de comparação entre volume de atendimentos (SIA) e internações (SIH).
- `visualizacao_financeira.py`: Análise de custo total vs. custo médio por internação.
- `base_completa_santo_andre_2024.parquet`: Base de dados final tratada (Arquivo de saída).

## 📈 Principais Insights (Fase 1)
1. **Sazonalidade:** Identificação de picos de atendimento em Março e Outubro.
2. **Impacto Financeiro:** Análise da flutuação do custo médio por internação, com pico identificado em **Julho**, sugerindo maior gravidade nos casos de inverno.
3. **Eficiência:** Estudo da correlação entre a atenção básica (SIA) e o desfecho hospitalar (SIH).

## 🔧 Como executar
### 1. Clone o repositório:
   ```bash
   git clone [https://github.com/Blimbliem/analise-saude-santo-andre.git](https://github.com/Blimbliem/analise-saude-santo-andre.git)
```
### 2. Pré-requisitos
Certifique-se de ter o **Python 3.13** (ou superior) instalado.

### 3. Instalação das Dependências
Abra o seu terminal na pasta do projeto e execute o comando abaixo para instalar as bibliotecas necessárias:

```bash
   pip install pandas matplotlib seaborn pyarrow
```
### 4. Instalação das Dependências
Para gerar a base de dados unificada:
```
  python tratamento_qtd_valor.py
```

Para visualizar os gráficos financeiros:
```
  python visualizacao_financeira.py
```


 

