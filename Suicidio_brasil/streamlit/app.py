import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates
from pywaffle import Waffle
import json
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

#funções 
def make_text(rows, # number of rows
              cols, # number of cols
              texts, # number of texts to display
              result, # featured text
              label = '', # detailed text
              font1_size = 80, # featured text font size
              font2_size = 20, # detailed text font size
              ha = 'center', # horizontal alignment
              va = 'center', # vertical alignment
              font1_color = '#A43428', # featured text font color
              font2_color = '#5F6A6A', # detailed text font color
              font1_weight = 'bold', # featured text font weight
              font2_weight = 'normal', # detailed text font weight
              sup_title = '', # suptitle
              font_suptitle = 30, # font size suptitle
              title1 = '', # title left figure
              title2 = '', # title right figure
              loc = 'center', # loc
              font_title = 20, # font size of titles
              a = 0.5, # percentage for va featured text
              b = 0.5, # percentage for ha featured text
              c = 0.5, # percentage for va detailed text
              d = 0.1, # percentage for ha detailed text
              figsize = (6, 2) # figure size
             ): 
    
    # axes coordenates

    left, width = 0.25, 0.5
    bottom, height = 0.25, 0.5
    right = left + width
    top = bottom + height
    
    # text fonts
    
    fonttitle = {'family': 'monospace', 'weight': 'normal', 'size': font_title, 'horizontalalignment': loc}
    font1 = {'family': 'sans-serif', 'color': font1_color, 'weight': font1_weight, 'size': font1_size}
    font2 = {'family': 'sans-serif', 'color':font2_color, 'weight': font2_weight, 'size': font2_size} 
        
    # creating texts
    
    if texts > 1:
        
        # creating the figure for texts
        
        fig, ax = plt.subplots(rows, cols, figsize = figsize)
        
        ax = ax.ravel()
        
        for i in range(len(result)):
            
            if i == 0:
                ax[i].set_title(title1, fontdict = fonttitle)
            elif i == 1:
                ax[i].set_title(title2, fontdict = fonttitle)
                           
            ax[i].set(xlim = (0, 1), ylim = (0, 1))
                
            ax[i].text(a * (left + right), b * (bottom + top), result[i],
                    ha = ha,
                    va = va,
                    fontdict = font1,
                    transform = ax[i].transAxes)
            if label != '':
                ax[i].text(c * (left + right), d * (bottom + top), label[i],
                        ha = ha,
                        va = va,
                        fontdict = font2,
                        transform = ax[i].transAxes)
   
            ax[i].axis('off')
            
        plt.suptitle(sup_title, fontsize = font_suptitle)
                      
    else:
        
        fig, ax = plt.subplots(rows, cols, figsize = figsize)
        
        ax.set_title(title1, fontdict = fonttitle)
        
        ax.set(xlim = (0, 1), ylim = (0, 1))
                
        ax.text(a * (left + right), b * (bottom + top), result,
                ha = ha,
                va = va,
                fontdict = font1,
                transform = ax.transAxes)
        ax.text(c * (left + right), d * (bottom + top), label,
                ha = ha,
                va = va,
                fontdict = font2,
                transform = ax.transAxes)
                
        ax.axis('off')
        
    plt.suptitle(sup_title, fontsize = font_suptitle) #by:ghermsen
#============================ geojson =============================================
geojson = json.load(open('brasil_estados.json'))

#=================================== code ============================================


df = pd.read_csv("suicidios_2010_a_2019.csv")
#df_pip = pd.read_csv("pibbrasil.csv")
df_censo=pd.read_csv('IBGE2010.csv')
df_pop = pd.read_csv('popbrasil.csv')

df.drop('Unnamed: 0', axis=1, inplace=True) #retirando coluna unnmamed

df.drop(["CIRURGIA",'ESCMAE' ], axis=1, inplace=True) #drop columns(miss values)

df['DTOBITO'] = pd.to_datetime( df['DTOBITO'] ,format="%Y/%m/%d")
df['DTNASC']=  pd.to_datetime( df['DTNASC'] ,format="%Y/%m/%d",errors = 'coerce')
df['ano_tri'] =df['DTOBITO'].dt.to_period("Q")
df['ano_mes'] =df['DTOBITO'].dt.strftime('%Y-%m')
df['ano_nasc'] =df['DTNASC'].dt.strftime('%Y')

#=============================== suicídio =============================

df_data = df.groupby('ano_mes').agg('size').reset_index()

df_data.columns = ['ano_mes', 'size']

#================================ taxa 100mil habitantes ===================================
df_ano = df.groupby('ano').agg('size').reset_index()
df_ano.columns = ['year', 'size']
df_pop_brasil = pd.merge(df_ano, df_pop,how='inner', on="year")
df_pop_brasil['taxa']= (df_pop_brasil['size']/df_pop_brasil['Brazil'])*100000


#================================= mapa ====================================================
df_estado_ano = pd.DataFrame(df.groupby(['ano','estado']).agg('size'))
df_estado_ano.columns = ['size']
df_censo.columns =['estado', 'censo2010']

#================================ homem x mulher ===========================================

k = df.groupby(['ano','SEXO'])['SEXO'].count()
k_df = pd.DataFrame(k)

for ano in df['ano'].unique():
    divisor = k_df.loc[(ano)].sum()
    k_df.loc[(ano, "Feminino")]=(k_df.loc[(ano, "Feminino")]/divisor).round(2)
    k_df.loc[(ano, "Masculino")]=(k_df.loc[(ano, "Masculino")]/divisor).round(2)

#=================================== racacor ================================================
df_raca_ano = pd.DataFrame(df.groupby(['ano','RACACOR']).agg('size'))
df_raca_ano.columns=['size']

#================================== estado civil ===========================================
df['ESTCIV'].fillna('Não Informado', inplace=True)
df_estciv_ano = pd.DataFrame(df.groupby(['ano','ESTCIV']).agg('size'))
df_estciv_ano.columns = ['size']
#==================================== page =================================================


st.set_page_config(
     page_title="FelipeEscobar",
     page_icon="chart_with_upwards_trend",
     layout="centered",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )

st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}

</style>
""", unsafe_allow_html=True)
#=============sidebar / menu ================#

st.sidebar.title('Navegation')
options = st.sidebar.radio('Select a page:', 
    ['Início', 'Setembro Amarelo' ,'Dashboard'])

#============ paginas ================#

def home():
    st.markdown('# Série histórica de suicídios no Brasil entre 2010 e 2019' , unsafe_allow_html=False)

    st.markdown('<p class="big-font">&emsp;"Diversos dados sobre suicídios foram reunidos em uma série histórica baseando-se nos dados provenientes do DATASUS. Mais especificamente, a base de dados do Sistema de Informação sobre Mortalidade (SIM) foi utilizada para extração de dados a partir do pacote PySUS. Para selecionar apenas os casos de suicídio, a variável CAUSABAS ou CAUSABAS_O (ambas retratando causa básica da morte) deveriam possuir valores da Classificação Internacional de Doenças (CID) entre X600 e X850. Essa faixa de casos do CID englobaria lesões autoprovocadas."<a href="https://www.kaggle.com/psicodata/dados-de-suicidios-entre-2010-e-2019">PsicoData</a></p>' , unsafe_allow_html=True)

    st.markdown("""### Variáveis
    
* **DTOBITO:** data do óbito.
* **DTNASC:** data de nascimento.
* **SEXO:** sexo. 1 : Masculino, 2 : Feminino.
* **RACACOR:** raça. 1 : Branca, 2 : Preta, 3 : Amarela, 4 : Parda, 5 : Indígena.
* **ESTCIV:** estado civil. 1 : Solteiro, 2 : Casado, 3 : Viúvo, 4 : Separado judicialmente, 5 : União consensual.
* **ESC:** escolaridade. 1 : Nenhuma, 2: 1 a 3 anos, 3 : 4 a 7 anos, 4 : 8 a 11 anos, 5 : 12 e mais, 8 : De 9 a 11 anos.
* **OCUP:** ocupação. Para óbitos a partir de 2006, segue-se a tabela CBO2002.
* **CODMUNRES:** município de residência do falecido (codificado).
* **LOCOCOR:** Local de ocorrência do óbito. 1 : Hospital, 2 : Outro estabelecimento de saúde, 3 : Domicílio, 4 : Via pública, 5 : Outros, 9 : NA.
* **ASSISTMED:** Assistência médica. 1 : Sim, 2 : Não, 9 : NA.
* **CAUSABAS:** Causa básica do óbito. Código CID-10.
* **CAUSABAS_O:** Causa básica do óbito. Código CID-10.""", unsafe_allow_html=False)

    st.dataframe(df.head())

    st.markdown("""### Análise dos dados
<p class="big-font">&emsp;Serão abordados na análise dos dados os aspectos temporais , territoriais e sociais.</p>

### Temporal e Territorial:<br>

<p class="big-font">
1. Qual o aumento no número de suicídio com o passar dos anos ?<br>
2. A taxa de suicídio por 100 mil habitantes aumentou ?<br>
4. Qual o estado com a maior taxa de suicídio por 100 mil habitantes?<br>
5. Qual é o local que mais ocorre os suicídios ?<br></p>

### Sociais :<br>

<p class="big-font">
1. Qual é o gênero principal das vítimas?<br>
2. Qual é o principal grupo étnico das vítimas?<br>
3. Qual é o estado civil das vítimas ?<br>
4. Qual é a principal faixa etária das vítimas?<br>
5. Qual é a escolaridade das vítimas ?<br>
6. Quais são as ocupações das vítimas ?<br></p>""", unsafe_allow_html=True)

def SetAmarelo():
    st.title("Setembro Amarelo")
    st.markdown("""<p class="big-font">&emsp;O Setembro Amarelo é uma campanha de conscientização sobre a prevenção do suicídio, no dia 10 deste mês é comemorado o Dia Mundial de Prevenção ao Suicídio.<br>&emsp;A ideia da campanha visa conscientizar as pessoas sobre o suicídio, bem como evitar o seu acontecimento.
     A divulgação é um fator muito importante, o assunto suicídio ainda é um tabu em nossa sociedade, a campanha acredita que falar sobre o mesmo é uma forma de entender quem passa por situações que levem a ideias suicidas, ajudá-las a partir do momento em que as mesmas são identificadas.<br>
&emsp;Caso esteja tendo esse tipo de pensamento ou passando por um momento de crise, busque ajuda. Os psicólogos são profissionais habilitados para tratar com esse tipo de problema ,assim como o apoio da família e amigos é muito importe nesse momento.<br>
&emsp;O <a href="https://www.cvv.org.br/">'CVV — Centro de Valorização da Vida'</a> realiza apoio emocional e prevenção do suicídio, atendendo voluntária e gratuitamente todas as pessoas que querem e precisam conversar, sob total sigilo por telefone, e-mail e chat 24 horas todos os dias.’ Informações sobre o atendimento ligue: 188)</p>""", unsafe_allow_html=True)

def dashboard():
    with st.container():
        st.title("Dashboard")
#====================================== crescimento =============================================#
    fig = px.line(df_data, 
              x=df_data['ano_mes'], 
              y=df_data['size'],
              labels=dict(y="Número de casos"),
              color_discrete_sequence=['#E74C3C'],
              height=400,
             width=800,
             template='ggplot2')
    fig.update_layout(yaxis_title='Número de suicídios',
                  xaxis_title='Ano / Mês',
                  title={
                  'text': "<b>Série Histórica dos suicídios no Brasil durante o período de 2010 a 2019</b><br><sup>Crescimento no número de casos de suicídio</sup>",
                  'xanchor': 'auto',
                  'yanchor': 'top'},
                  title_font_family="monospace",
                 title_font_size=14,
                  font_size=10)
    fig.add_annotation( x='2019-05', 
                    y=1100,
                    text="",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize = 2,
                    arrowcolor = 'black',
                    ax = '2010-06',
                    ay = 800,
                    axref="x",
                    ayref='y',)
    fig.add_annotation( x='2015',
                    y=1000,
                    text="Aumento de 43.03%",
                    showarrow=True,
                    font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="#ffffff"),
                    align="center",
                    bordercolor="#c7c7c7",
                    borderwidth=2,
                    borderpad=4,
                    bgcolor="grey")
#===================================================== taxa ============================================#
    taxa = px.line(df_pop_brasil, 
              x=df_pop_brasil['year'], 
              y=df_pop_brasil['taxa'],
              labels=dict(y="Número de casos"),
              color_discrete_sequence=['#E74C3C'],
              height=400,
             width=800,
             template='ggplot2')
    taxa.update_layout(yaxis_title='Taxa de suicídio por 100 mil Habitantes',
                  xaxis_title='Ano',
                  title={
                  'text': "<b>Taxa de suicídio por 100 mil habitantes no Brasil</b><br><sup>Período de 2010 a 2019</sup>",
                  'xanchor': 'auto',
                  'yanchor': 'top'},
                  title_font_family="monospace",
                  title_font_size=14,
                  font_size=10)
    taxa.add_annotation( x='2018.5', 
                    y=6.2,
                    text="",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize = 2,
                    arrowcolor = 'black',
                    ax = '2010.5',
                    ay = 4.9,
                    axref="x",
                    ayref='y',)
    taxa.add_annotation( x='2014.5',
                    y=5.7,
                    text="Aumento de 32.64%",
                    showarrow=True,
                    font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="#ffffff"),
                    align="center",
                    bordercolor="#c7c7c7",
                    borderwidth=2,
                    borderpad=4,
                    bgcolor="grey")


    #============================================================================================#
    with st.container():
        st.plotly_chart(fig)
        st.plotly_chart(taxa)
    #=====================================================================================#
    st.subheader("Selecione o ano:")
    ano = st.slider('', 2010, 2019, 2010) #slider
    #====================================== bonecos =============================================#
    data = {'Masculino':round((k_df.loc[(ano)].T['Masculino']['SEXO']*100), 2),
            'Feminino':round((k_df.loc[(ano)].T['Feminino']['SEXO']*100), 2)}
    data = {'Masculino':round((k_df.loc[(ano)].T['Masculino']['SEXO']*100), 2),
       'Feminino':round((k_df.loc[(ano)].T['Feminino']['SEXO']*100), 2)}
    font_title = {'family': 'sans-serif', 'color':'#424949','weight': 'normal','size': 25}

    fig = plt.figure(
      FigureClass = Waffle,
      rows = 5,
      columns = 20,
      colors = ('#7B241C', '#515A5A'),
      values = data, 
      icons = ['male', 'female'], 
      icon_size = 23,
      title = {'label':'Porcentagem de vítimas Masculinas e Femininas',
               'loc': 'center', 'fontdict':font_title},
      labels = [f"{k} ({round(v / sum(data.values()) * 100)}%)" for k, v in data.items()],
      legend = {        
        'loc': 'lower left',
        'bbox_to_anchor': (0, -0.25),
        'ncol': len(data),
        'framealpha': 0,
        'fontsize': 15
    },
      icon_legend = True,
      figsize=(15,6)
    )
    fig.set_tight_layout(False)
    st.pyplot(fig)
# ================================================= mapa ===================================+#
    df_sui_pop = pd.merge(pd.DataFrame(df_estado_ano.loc[(ano)]['size']), df_censo,how='inner', on="estado")
    df_sui_pop['taxa']= (df_sui_pop['size']/df_sui_pop['censo2010'])*100000

    mapa = px.choropleth_mapbox(df_sui_pop, geojson=geojson, locations='estado', color='taxa',
                           color_continuous_scale="reds",
                           mapbox_style="white-bg",
                           zoom=3.3, center =  {"lat":-15 ,"lon":  -51},
                           opacity=0.9,
                           height=900, width=800)

    mapa.update_geos(fitbounds="locations", visible=False)
    mapa.update_layout(title={
                'text': "<b>Taxa de Suicídio por 100 mil habitantes dos estados</b><br><sup>Período de {ano}</sup>".format(ano=ano),
                'xanchor': 'left',
                'yanchor': 'top'},
                title_font_family="monospace",
                title_font_size=21)

    st.plotly_chart(mapa)
#===================================  racacor ====================================

    racacor = px.bar(df_raca_ano.loc[(ano)].sort_values(by='size', ascending=False), y="size", x=df_raca_ano.loc[(ano)].sort_values(by='size', ascending=False).index,
             color=df_raca_ano.loc[(ano)].sort_values(by='size', ascending=False).index,
            title='Número de suicídio por RAÇA / COR',
             color_discrete_sequence=['#7B241C','#C0392B','#CD6155','#D98880','#F2D7D5','#F9EBEA'],
            height=400,
             width=800,text='size',
            template ='ggplot2')
    racacor.update_layout(yaxis_title='Número de Suicídios',
                 xaxis_title='RAÇA / COR',
                 font=dict(
                family="Courier New, monospace",
                size=18),
                  title={
                  'text': "<b>Número de suicídio por RAÇA / COR <br><sup>Período de {ano}</sup>".format(ano=ano),
                  'xanchor': 'auto',
                  'yanchor': 'top'},
                  title_font_family="monospace",
                  title_font_size=20)
    racacor.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    racacor.update_layout(uniformtext_minsize=40, uniformtext_mode='hide')
    st.plotly_chart(racacor)

#================================== estado civil =========================================
    estciv = px.bar(df_estciv_ano.loc[(ano)].sort_values(by='size', ascending=True), x="size",y=df_estciv_ano.loc[(ano)].sort_values(by='size', ascending=True).index,
             color=df_estciv_ano.loc[(ano)].sort_values(by='size', ascending=True).index,
             title="<b>Número de suicídio por estado civil<br><sup>Período de {ano}</sup>".format(ano=ano),
             color_discrete_sequence=['#FADBD8','#E6B0AA','#D98880','#CD6155','#C0392B','#7B241C'],
             height=400,
             width=850,
             text=df_estciv_ano.loc[(ano)].sort_values(by='size', ascending=True).index,
             template='ggplot2')
    estciv.update_traces( textposition='outside',textfont_size=20)
    estciv.update_yaxes(showticklabels=False)
    estciv.update_layout(xaxis_range=[0,7200],
                  xaxis_title='Suicídios',
                  yaxis_title='Estado Civil',
                  title={
                  'text': "<b>Número de suicídio por estado civil em {ano} </b><br>".format(ano=ano),
                  'xanchor': 'auto',
                  'yanchor': 'top'},
                  title_font_family="monospace",
                  title_font_size=20)
    st.plotly_chart(estciv)

#================================== code ============================================

if options == "Início":
    home()
elif options == "Setembro Amarelo":
    SetAmarelo()
elif options =="Dashboard":
    dashboard()