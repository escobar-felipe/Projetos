
# Desenvolvimento de um Dashboard com python e streamlit
## Detalhes do Projeto:

Esse projeto consiste na construção de um Dashboard com dados extraídos a partir o DataSus pelo <a href="https://www.kaggle.com/psicodata/dados-de-suicidios-entre-2010-e-2019"><strong> Psicodata</strong></a>. Nessa parte do projeto foram feitas algumas análises e alguns gráficos foram criados para acompanhamento de algumas métricas. Todos os gráficos podem ser acessados pelo <a href="https://share.streamlit.io/escobar-felipe/projetos/main/Suicidio_brasil/app.py"><strong> DashBoard</strong></a>

## Projeto

1.  Bibliotecas usadas no Projeto.
```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates
from pywaffle import Waffle
import json
```
* streamlit - criação de web apps
* pandas - biblioteca para análise e manipulação de dados.
* numpy - biblioteca para operações com vetores e matrizes
* plotly.express - parte da biblioteca plotly, para criação de figuras
*  matplotlib.pyplot - coleções de funções que fazem o matplotlib funcionar como o matlab
* matplotlib.dates - módulo para trabalhar com datas no matplotlib
* pywaffle -  biblioteca para criar gráficos em formato "waffle"
* json - biblioteca para manipular arquivos JSON

 # Explicando alguns comandos básicos do streamlit:
1. st.write()
 ```python
 st.write("hello,world")
```
* Com essa chamada você pode escrever diversos argumentos para o app, dataframe , gráficos entre outros argumentos que podem ser encontrado na documentação da biblioteca.
2. st.markdown(body, unsafe_allow_html=False)
 ```python
 st.markdown("texto", unsafe_allow_html=False)
```
* exibe uma string em formato MarkDown
* unsafe_allow_html - falso trata uma tag html como texto , verdadeiro considera tag html
3. st.title, st.header ,  st.subheader
 ```python
 st.title("texto")
 st.header("texto")
 st.subheader("texto")
```
*  Exibe textos em diferentes formatos e tamanhos
4. st.pyplot - st.plotly_chart
 ```python
 st.pyplot(fig)
 st.plotly_chart(fig)
```
* pyplot  - exibe uma figura matplotlib
* plotly_chart - exibe um gráfico interativo plotly

5. st.set_page_config() - Configurações da página
 ```python
 st.set_page_config( page_title="Suicídio Brasil", page_icon="chart_with_upwards_trend", layout="centered", initial_sidebar_state="expanded")
```

* page_title - designar um título para web app
* page_icon - ícone do web app
* layout - como o conteúdo é apresentado ( centered - centralizado / wide - tela toda)
* initial_sidebar_state - estado da barra lateral ( expanded - expandida / collapsed - oculta / auto - oculta somente em dispositivos móveis)

6. @st.experimental_memo
 ```python
@st.experimental_memo
```
* st.experimenta_memo memoriza a execução das suas funções em cache, otimizando o seu código. 

# Contato

Deixo aqui meu contato para receber sugestões , correções e ideias.
<a href="https://www.linkedin.com/in/escobar-felipe/"><strong> Linkedin</strong></a>.
