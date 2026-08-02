import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)

plt.style.use('ggplot')

df = pd.read_csv('Data/case_inadimplencia_dataset.csv')

print(df.info())
print(df.head(10))
print(df.sample(10))
print(df.tail(10))

df['data_contratacao'] = pd.to_datetime(df['data_contratacao'])

print(df.isnull().sum())

print(df[df['idade'] < 18].shape[0])

print(df.duplicated(subset='id_cliente').sum())

# Análisando as coluna idade, renda_mensal, score_interno, valor-solicitado,comprometimento_renda e dias_atraso_max.
print(df.describe())

df['faixa_idade'] = pd.cut(df['idade'], bins = [18,25,35,45,60,70], labels = ['Jovem', 'Jovem Adulto', 'Adulto', 'Maduro', 'Sênior'] ,include_lowest=True)
df['faixa_score'] = pd.cut(df['score_interno'], bins = [0,300,600,800,1000], labels = ['Alto risco', 'Médio risco', 'Baixo risco', 'Muito baixo risco'], include_lowest=True)
df['faixa_comprometimento_renda'] = pd.cut(df['comprometimento_renda'], bins = [0,0.30,0.60,1.0,1.50], labels = ['Saudável', 'Atenção', 'Alto risco', 'Crítico'], include_lowest=True)
print(df.isnull().sum())

# Processo de EDA

print(df['inadimplente_90d'].value_counts())

print(df.groupby('faixa_score')['inadimplente_90d'].mean())
print(df.groupby('possui_restricao')['inadimplente_90d'].mean())
print(df.groupby('canal_aquisicao')['inadimplente_90d'].mean())
print(df.groupby('classe_social')['inadimplente_90d'].mean())


# Gráfico 1 - Taxa geral de inadimplência

import seaborn as sns
import matplotlib.pyplot as plt

taxa = df['inadimplente_90d'].value_counts(normalize=True).mul(100).reset_index()
taxa.columns = ['Situação', 'Percentual']

taxa['Situação'] = taxa['Situação'].replace({
    0: 'Adimplentes',
    1: 'Inadimplentes'
})

plt.figure(figsize=(7,5))

ax = sns.barplot(
    data=taxa,
    x='Situação',
    y='Percentual'
)

plt.title('Taxa Geral de Inadimplência', fontsize=15, weight='bold')
plt.xlabel('')
plt.ylabel('Percentual (%)')

for i in ax.containers:
    ax.bar_label(i, fmt='%.1f%%')

plt.tight_layout()
plt.savefig('Output/Output/Graficos/grafico_taxa_geral.png', dpi=300, bbox_inches='tight')
plt.show()

# Gráfico 2 - Inadimplência por Faixa de Score

score = (
    df.groupby('faixa_score')['inadimplente_90d']
      .mean()
      .mul(100)
      .reset_index()
)

ordem = [
    'Muito baixo risco',
    'Baixo risco',
    'Médio risco',
    'Alto risco'
]

plt.figure(figsize=(8,5))

ax = sns.barplot(
    data=score,
    x='faixa_score',
    y='inadimplente_90d',
    order=ordem
)

plt.axhline(
    y=18.1,
    color='red',
    linestyle='--',
    label='Média da carteira'
)

plt.title('Taxa de Inadimplência por Faixa de Score', fontsize=15, weight='bold')
plt.xlabel('Faixa de Score')
plt.ylabel('Inadimplência (%)')
plt.legend()

for i in ax.containers:
    ax.bar_label(i, fmt='%.1f%%')

plt.tight_layout()
plt.savefig('Output/Output/Graficos/grafico_score.png', dpi=300, bbox_inches='tight')
plt.show()

# Gráfico 3 - Possui Restrição

restricao = (
    df.groupby('possui_restricao')['inadimplente_90d']
      .mean()
      .mul(100)
      .reset_index()
)

restricao['possui_restricao'] = restricao['possui_restricao'].replace({
    0: 'Não',
    1: 'Sim'
})

plt.figure(figsize=(6,5))

ax = sns.barplot(
    data=restricao,
    x='possui_restricao',
    y='inadimplente_90d'
)

plt.axhline(
    y=18.1,
    color='red',
    linestyle='--',
    label='Média da carteira'
)

plt.title('Inadimplência por Restrição de Crédito', fontsize=15, weight='bold')
plt.xlabel('Possui restrição')
plt.ylabel('Inadimplência (%)')
plt.legend()

for i in ax.containers:
    ax.bar_label(i, fmt='%.1f%%')

plt.tight_layout()
plt.savefig('Output/Output/Graficos/grafico_restricao.png', dpi=300, bbox_inches='tight')
plt.show()

# Gráfico 4 - Canal de Aquisição

canal = (
    df.groupby('canal_aquisicao')['inadimplente_90d']
      .mean()
      .mul(100)
      .sort_values(ascending=False)
      .reset_index()
)

plt.figure(figsize=(10,5))

ax = sns.barplot(
    data=canal,
    x='canal_aquisicao',
    y='inadimplente_90d'
)

plt.axhline(
    y=18.1,
    color='red',
    linestyle='--',
    label='Média da carteira'
)

plt.title('Inadimplência por Canal de Aquisição', fontsize=15, weight='bold')
plt.xlabel('')
plt.ylabel('Inadimplência (%)')
plt.xticks(rotation=20)
plt.legend()

for i in ax.containers:
    ax.bar_label(i, fmt='%.1f%%')

plt.tight_layout()
plt.savefig('Output/Output/Graficos/grafico_canal.png', dpi=300, bbox_inches='tight')
plt.show()






