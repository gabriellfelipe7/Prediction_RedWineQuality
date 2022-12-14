# -*- coding: utf-8 -*-
"""Red_Wine_Quality.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SAo87mGOMcTw_FXk-mJ9Qx-P6IYwHbiK

# **Red Wine Quality**

Autor: Gabriel Felipe Machado de Oliveira, 2021

## 1. Introdução: Formulação do problema

O presente projeto tem como objetivo estudar as diversas etapas de um projeto de Ciência de Dados utilizando uma base dedos real.

Considerando a base de dados que relata a qualidade de vinhos temos 11 atributos de entrada (baseados em análises físico-químicas) e 1 atributo de saída, são eles:
1. Fixed Acidity: Indicador de acidez;
2. Volatile Acidity: Indicador de volatilidade;
3. Citric Acid: Indicador de acidez cítrica;
4. Residual Sugar: Indica a quantidade de açucar natural após a frementação;
5. Chlorides: Indica a quantidade de Cloretos na bebida;
6. Free Sulfur Dioxide: Indica a quantidade de enxofre livre;
7. Total Sulfur Dioxide: Indica a quantidade de enxofre total;
8. Density: Dendidade da bebida;
9. pH: pH da bebida;
10. Sulphates: Indicador de sulfatos na bebida;
11. Alcohol: Indicador de álcool na bebida;
12. Quality: Pontuação do vinho que varia de 1 a 10.

O objetivo é classificar a qualidade do vinho com base no conjunto de atributos de entrada.

## 2. Leitura dos Dados

Importando o módulo Pandas e Numpy para leitura e preparação dos dados, e outros módulo que serão necessários, vamos ler e exibir o conjunto dados que usaremos.
"""

import pandas as pd
import numpy as np

data = pd.read_csv('winequality-red.csv') #Importando a base de dados
data.head() #Mostrando as 5 primeiras linhas

data.describe() #Descrevendo estatisticamente os atributos

data.info() #Verificando valores vazios

"""
Podemos ver que não há valores nulos, logo não será necessário realizar a limpeza. Considerando as diferentes escalas dos atributos, vamos realizar o processo de normalização."""

from sklearn.preprocessing import StandardScaler

datanp = data.to_numpy() #Transformando para NumPy
nrow, ncol = data.shape

Y = datanp[:,0]
X = datanp[:,1:ncol]

#Normalizando os dados
scaler = StandardScaler().fit(X) 
X = scaler.transform(X)

print('Dados Transformados:')
print('Media:', np.mean(X, axis = 0))
print('Desvio Padrao:', np.std(X, axis = 0))

"""## 3. Análise Exploratória e Estatística Descritiva

Nesse momente, focaremos em analisar qual a influência/relação de nossos atributos em nossa classe. Dessa forma, usaremos funções e métodos do Matploblib e do Seaborn para nos auxiliar.
"""

import seaborn as sb
import matplotlib.pyplot as plt

"""Primeiro, vamo analizar as frequâncias de valores utilizando Histogramas para cada atributo e para a classe."""

data.hist(bins = 20, figsize = (10,10)) #Gerando Histogramas para os atributos
plt.show() #Plotando

"""Percebamos que a maioris dos atributos tendem a uma dsistribuição Normal, e ainda que a nossa classe "Quality" possui como valores mais frquentes o 5 e o 6.

Agora, analisemos a possiveis correlações e dependências dos atributos, utilizando um mapa de calor.
"""

#Configurando o tamanho do gráfico, inicializando e printando o mapa de calor dos atributos
plt.figure(figsize = (19,8))
sb.heatmap(data.corr(), annot = True)
plt.show()

"""Podemos ainda fazermos Boxplots de cada atributos condicionado a classe, a fim de inferirmos possíveis correlaçoões."""

colunas = data.columns
cont = 1
plt.figure(figsize = (19,8))

#Para cada atributo condicionamos o Boxplot para a classe
for coluna in colunas:
    plt.subplot(4,3,cont)
    sb.boxplot(x = 'quality', y = coluna, data = data)
    cont += 1

plt.show()

"""Agora, vamos a possíveis conclusões: os atributos 'Alcohol', 'Sulphates' e 'Citric Acid' tendem a influenciar positivamente a qualidade do vinho quando em grandes quantidades; os atributos 'acidity', 'pH' e 'density', quando em grandes quantidades, tendem a influenciar negativamente na qualidade do vinho.

## 4. Preparação e Normalização dos Dados

Antes ainda da seleção do modelo de aprendizado, temos algumas alterações a serem realizadas. Precisamo determinar algumas variáveis categóricas para nos auxiliarem na predição dos dados e ainda, realizar a normalização dos atributos para eliminarmos possiíveis efeitos das diferentes escalas consideradas.
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score

#Categorizando os tipos de vinhos cm ruim e bom
valores = (2, 6.5, 8)
grupos = ['ruim', 'bom']
data['quality'] = pd.cut(data['quality'], bins = valores, labels = grupos)

label_quality = LabelEncoder() #Iniciando a função de categorização

data['quality'] = label_quality.fit_transform(data['quality']) #Categoriando com 0 ou 1

data['quality'].value_counts() #Analisando a categorizações

data.head()

#Dividindo o dataset entre atributos (X) e classe (Y)
X = data.drop('quality', axis = 1)
y = data['quality']

#Separando o conjunto de teste (2% do total) e o conjunto de treinamento
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

#Normalização dos dados e treinamento dos conjuntos
sc = StandardScaler() 
X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)

"""## 5. Treinamento e Avaliação dos Modelo e Predições

Temos inúmeros modelos de clasificação como opção para classifiarmos os vinhos. Entretanto, testaremos o Random Forest Classifier e o Stochastic Gradient Decent Classifier

### Random Forest Classifier
"""

#Inicialização do modelo, treinamento e predição
RandomFC = RandomForestClassifier(n_estimators = 200)
RandomFC.fit(X_train, y_train)
pred_RandomFC = RandomFC.predict(X_test)

#Printando a acurácia da predição
print(classification_report(y_test, pred_RandomFC))

"""Conseguimos uma acurácia de 88% no conjuto de teste.

### Stochastic Gradient Decent Classifier
"""

#Inicialização do modelo, treinamento e predição
StochasticGDC = SGDClassifier(penalty = None)
StochasticGDC.fit(X_train, y_train)
pred_StochasticGDC = StochasticGDC.predict(X_test)

#Printando a acurácia da predição
print(classification_report(y_test, pred_StochasticGDC))

"""Utilizando o Stochastic Gradient Decent Classifier conseguimos uma acurácia de 83%.

## 6. Interpretação dos Resultados

Dado que dividimos a classe entre 0 e 1, como categorias de bom e ruim, colocamos dois modeos de classificação para fazerem as respectivas predições de qualidade dos vinhos. Concluímos que o modelo que melhor performa nesse contexto é o Random Forest Classifier, na qual alcançou uma acurácia de 88% no conjunto de teste, isto é, acertou a maioria da qualidade dos vinhos no conjnto de teste, após treinar com o conjunto de treinamento.

Portanto, segue que o Random Forest Classifier é o melhor modelo de Machine Learning entre os dois testados, para predizer qualidade de vinhos de um conjunto de dados.
"""