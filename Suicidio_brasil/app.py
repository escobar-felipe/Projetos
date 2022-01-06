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
geojson = json.load(open('Suicidio_brasil/csv/brasil_estados.json'))

#=================================== code ============================================


df = pd.read_csv("Suicidio_brasil/csv/suicidios_2010_a_2019.csv")
df_censo=pd.read_csv('Suicidio_brasil/csv/IBGE2010.csv')
df_pop = pd.read_csv('Suicidio_brasil/csv/popbrasil.csv')

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
#================================= faixa etária ============================================
df_idade = df.dropna(subset = ['DTNASC'])
df_idade = df[df['ano_nasc'].astype(float).between(1925, 2019)]
df_idade['idade'] = ((df_idade.DTOBITO - df_idade.DTNASC)/np.timedelta64(1, 'Y')).astype('int')
bins= [0,10,20,30,40,50,60,70,80,90,110]
labels = ['0-10','10-20','20-30','30-40','40-50','50-60','60-70','70-80','80-90','90-110']
df_idade['grupos'] = pd.cut(df_idade['idade'], bins=bins, labels=labels, right=False)
df_idade_gp_ano = pd.DataFrame(df_idade.groupby(['ano','grupos']).agg('size'))
df_idade_gp_ano.columns = ['size']

#==================================== Local da ocorrência ==================================
df['LOCOCOR'].fillna('Não Informado', inplace=True)
df['LOCOCOR'].replace('Outro estabelecimento de saúde','Departamentos de Saúde', inplace=True)
df['LOCOCOR'].replace('Hospital','Departamentos de Saúde', inplace=True)
df_lococor = pd.DataFrame(df.groupby(['ano','LOCOCOR']).agg('size'))
df_lococor.columns = ['size']
#=================================== escolaridade ==========================================
df_esc_ano = pd.DataFrame(df.groupby(['ano', 'ESC']).agg('size'))
df_esc_ano.columns = ['size']
df2 = pd.DataFrame({
    'Escolaridade': ['1 a 3 anos', '4 a 7 anos', '8 a 11 anos', '12 e mais', 'Nenhuma'],
    'num': [0, 1, 2, 3, 4]})

#==================================== page =================================================


st.set_page_config(
     page_title="Suicídio Brasil",
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
    ['Início', 'Setembro Amarelo' , 'Perfil Das Vítimas','Dashboard'])
header_html = """<img src="avatar.png" style="width:200px;height:200px;">"""
col1, col2,col3,col4 = st.sidebar.columns(4)
with col2:
    st.image("avatar.png" ,width=150)
st.sidebar.text("""        Felipe Escobar
Cursando Análise e Desenvolvimento 
de Sistemas na ULBRA - Universidade
Luterana do Brasil.""")
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
        with st.expander("Série Histórica dos suicídios"):
            st.write("""
         Houve um aumento de 43.03% no número de suicídio no ano de 2019 em relação ao ano de 2010, 
         indo de 9476 no ano de 2010 a 13554 no ano de 2019. Para lidar com o aumento populacional 
         — uma das possibilidades do aumento no número de suicídios — 
         foi calculado a taxa de suicídio por 100 mil Habitantes 
         (Número de suicídios divido pela População do Brasil multiplicado por 100 mil) no período entre 2010 e 2019 ,
          assim foi possível verificar que o número vítimas vem crescendo independente do aumento populacional.
     """)
        st.plotly_chart(taxa)
        with st.expander("Taxa de suicídio"):
            st.write("""
   Existem diversos outros fatores que podem estar ocasionando esse aumento , não podemos afirmar as causas do aumento sem realizar testes de casualidade. Deixo dois principais problemas da atualidade que precisam ser estudados que podem estar ocasionando esse aumento.
    1 - A fragilidade social, famílias ou pessoas que estão perdendo sua representatividade na sociedade principalmente por questões socioeconômicas.
    2 - Problemas financeiros, de acordo com a pesquisa THE EMPLOYER’S GUIDE TO FINANCIAL WELLNESS, pessoas com dificuldades financeiras são 4x mais propensas a desenvolver a depressão.
     """)

def SetAmarelo():
    st.title("Setembro Amarelo")
    st.markdown("""<p class="big-font">&emsp;O Setembro Amarelo é uma campanha de conscientização sobre a prevenção do suicídio, no dia 10 deste mês é comemorado o Dia Mundial de Prevenção ao Suicídio.<br>&emsp;A ideia da campanha visa conscientizar as pessoas sobre o suicídio, bem como evitar o seu acontecimento.
     A divulgação é um fator muito importante, o assunto suicídio ainda é um tabu em nossa sociedade, a campanha acredita que falar sobre o mesmo é uma forma de entender quem passa por situações que levem a ideias suicidas, ajudá-las a partir do momento em que as mesmas são identificadas.<br>
&emsp;Caso esteja tendo esse tipo de pensamento ou passando por um momento de crise, busque ajuda. Os psicólogos são profissionais habilitados para tratar com esse tipo de problema ,assim como o apoio da família e amigos é muito importe nesse momento.<br>
&emsp;O <a href="https://www.cvv.org.br/">'CVV — Centro de Valorização da Vida'</a> realiza apoio emocional e prevenção do suicídio, atendendo voluntária e gratuitamente todas as pessoas que querem e precisam conversar, sob total sigilo por telefone, e-mail e chat 24 horas todos os dias.’ Informações sobre o atendimento ligue: 188)</p>""", unsafe_allow_html=True)

def perfil():
    st.title("Perfil das vítimas")
    df_masc = df_idade[df_idade['SEXO']=='Masculino']
    df_masc =df_masc.groupby(['SEXO','RACACOR','ESTCIV','ESC','grupos']).size().to_frame().reset_index()
    df_masc.columns = ['SEXO','RACACOR', 'ESTCIV', 'ESC','grupo/idade','total vitimas']
    df_fem = df_idade[df_idade['SEXO']=='Feminino']
    df_fem =df_fem.groupby(['SEXO','RACACOR','ESTCIV','ESC','grupos']).size().to_frame().reset_index()
    df_fem.columns = ['SEXO','RACACOR', 'ESTCIV', 'ESC','grupo/idade','total vitimas']
    df_masc = df_masc.sort_values('total vitimas', ascending = False).reset_index(drop=True)
    df_fem = df_fem.sort_values('total vitimas', ascending = False).reset_index(drop=True)
    with st.container():
        with st.expander("Perfil Masculino"):
            list_perfil_masc = []
            label_perfil_masc = []

            for i in range(0,5):
                list_perfil_masc.append(f'{df_masc["total vitimas"][i]} vitimas')
                label_perfil_masc.append(f'{i+1}°- {df_masc.loc[i][0]} , {df_masc.loc[i][1]} , {df_masc.loc[i][2]} ,Escolaridade: {df_masc.loc[i][3]} ,Entre {df_masc.loc[i][4]} Anos')
            perfil_masc = make_text(5,
          1,
          10,
          label_perfil_masc,
          label =  list_perfil_masc,
          font1_size = 15,
          font2_size = 15,
          ha = 'left',
          font1_color = '#5F6A6A',
          font2_color = '#A93226',
          font1_weight = 'heavy',
          font2_weight = 'bold',
          title1 = "Perfil das vítimas do sexo masculino",
          loc= 'center',
          a = 0,
          c = 0,
          figsize = (12, 5))
            st.pyplot(perfil_masc)
        with st.expander("Taxa de suicídio"):
            list_perfil_fem = []
            label_perfil_fem = []

            for i in range(0,5):
                list_perfil_fem.append(f'{df_fem["total vitimas"][i]} vitimas')
                label_perfil_fem.append(f'{i+1}°- {df_fem.loc[i][0]} , {df_fem.loc[i][1]} , {df_fem.loc[i][2]} ,Escolaridade: {df_fem.loc[i][3]} ,Entre {df_fem.loc[i][4]} Anos')
            perfil_fem =make_text(5,
          1,
          10,
          label_perfil_fem,
          label =  list_perfil_fem,
          font1_size = 15,
          font2_size = 15,
          ha = 'left',
          font1_color = '#5F6A6A',
          font2_color = '#A93226',
          font1_weight = 'heavy',
          font2_weight = 'bold',
          title1 = "Perfil das vítimas do sexo feminino",
          loc= 'center',
          a = 0,
          c = 0,
          figsize = (12, 5))
            st.pyplot(perfil_fem)
        st.subheader("O perfil das vítimas foi gerado com base em atributos como ‘gênero, raça/cor, estado civil, escolaridade, e grupo de idades.")
def dashboard():
    with st.container():
        st.title("Dashboard")
    #=====================================================================================#
    st.subheader("Selecione o ano:")
    ano = st.slider('', 2010, 2019, 2010) #slider
    st.subheader("Selecione o gráfico:")
    option = st.selectbox(
     '',
     ('Porcentagem de vítimas Masculinas e Femininas', 'Taxa de Suicídio por 100 mil habitantes dos estados', 'Número de suicídio por RAÇA / COR','Número de suicídio por estado civil','Suicídio no Brasil por faixa etária','Locais onde ocerram os suicídios','Suicídio por nível de escolaridade','Ocupação das vítimas'))

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
    def vitimas():
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
    def mapa_suicide():
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
    def Raçacor():
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
    def estadocivil():
        st.plotly_chart(estciv)
#===================================== faixa etária =============================================#
    color_map = ['#EAECEE' for _ in range(9)]
    color_map[3] = color_map[2] = '#A93226' 

    FE, ax = plt.subplots(1,1, figsize=(12, 10),dpi=600)
    ax.bar(df_idade_gp_ano.loc[(ano)].index, df_idade_gp_ano.loc[(ano)]['size'], width=0.7, 
       edgecolor='darkgray',
       linewidth=0.6,color=color_map)


# anotações
    for i in range(0,len(df_idade_gp_ano.loc[(ano)].index)):
        ax.annotate(f"{df_idade_gp_ano.loc[(ano)]['size'][i]}", 
                   xy=(i, df_idade_gp_ano.loc[(ano)]['size'][i] + 3),
                   va = 'bottom', ha='center',fontweight='light', fontfamily='serif')
    for s in ['top', 'left', 'right']:
        ax.spines[s].set_visible(False)
    
    ax.set_xticklabels(df_idade_gp_ano.loc[(ano)].index, fontfamily='serif', rotation=0)

# titulos 

    FE.text(0.09, 1, 'Suicídio no Brasil por faixa etária no período de {ano}'.format(ano=ano), fontsize=16, fontweight='bold', fontfamily='monospace')
    FE.text(0.09, 0.95, 'As faixas etárias que mais cometem suicídio estão destacadas', fontsize=12, fontweight='light', fontfamily='monospace')


    ax.grid(axis='y', linestyle='-', alpha=0.4) 
    ax.set_axisbelow(True)

#Axis labels

    plt.xlabel("Faixa Etária", fontsize=12, fontweight='light', fontfamily='serif',loc='center',y=-2)
    
    def faixaetaria():
        st.pyplot(FE)
#=================================== local da ocência ===========================================#
    local_o = px.bar(df_lococor.loc[(ano)].sort_values(by='size', ascending=False), y="size", x=df_lococor.loc[(ano)].sort_values(by='size', ascending=False).index,
             color=df_lococor.loc[(ano)].sort_values(by='size', ascending=True).index,
             color_discrete_sequence=['#7B241C','#C0392B','#CD6155','#D98880','#F2D7D5'],
             height=400,
             width=850,
             text='size',
             template='ggplot2')
    local_o.update_layout(yaxis_title='Número de Suicídios',
                  xaxis_title='Local da ocorrência',
                  title={
                  'text': "<b>Locais onde ocerram os suicídios no período {ano} </b><br>".format(ano=ano),
                  'xanchor': 'auto',
                  'yanchor': 'top'},
                  title_font_family="monospace",
                  title_font_size=25)
    
    def local_ocorrencia():
        st.plotly_chart(local_o)
#==================================== escolaridade ==============================================#
    df_esc = pd.DataFrame(df_esc_ano.loc[(ano)]).reset_index()
    df_esc.columns = ['Escolaridade','size']
    df_esc = pd.merge(df_esc, df2, on='Escolaridade')
    df_esc = df_esc.sort_values(by='num', ascending=True)
    df_esc= df_esc.reset_index(drop=True)
    color_map = ['#EAECEE' for _ in range(9)]
    color_map[df_esc['size'].argmax()]  = '#A93226' 

    esc_fig, ax_esc = plt.subplots(1,1, figsize=(12, 10),dpi=600)
    ax_esc.bar(df_esc['Escolaridade'], df_esc['size'], width=0.7, 
       edgecolor='darkgray',
       linewidth=0.6,color=color_map)


#anotações
    for i in df_esc['Escolaridade'].index:
        ax_esc.annotate(f"{df_esc['size'][i]}", 
                   xy=(i, df_esc['size'][i] + 3),
                   va = 'bottom', ha='center',fontweight='light', fontfamily='serif')
    for s in ['top', 'left', 'right']:
        ax_esc.spines[s].set_visible(False)
    
    ax_esc.set_xticklabels(df_esc['Escolaridade'], fontfamily='serif', rotation=0)

# Titulos

    esc_fig.text(0.09, 1, 'Nível de escolaridade X Número de suicídios', fontsize=16, fontweight='bold', fontfamily='monospace')
    esc_fig.text(0.09, 0.96, '1 a 3 anos : Fundamental 1 incompleto', fontsize=12, fontweight='light', fontfamily='monospace')
    esc_fig.text(0.09, 0.94, '4 a 7 anos : Fundamental 1 completo / Fundamental 2 incompleto', fontsize=12, fontweight='light', fontfamily='monospace')
    esc_fig.text(0.09, 0.92, '8 a 11 anos :  Ensino médio completo ou incompleto', fontsize=12, fontweight='light', fontfamily='monospace')
    esc_fig.text(0.09, 0.90, '12 e mais : Ensino superior completo ou incompleto', fontsize=12, fontweight='light', fontfamily='monospace')
    ax_esc.grid(axis='y', linestyle='-', alpha=0.4) 
    ax_esc.set_axisbelow(True)

#Axis labels

    plt.xlabel("Escolaridade", fontsize=12, fontweight='light', fontfamily='serif',loc='center',y=-2)

    def escolaridade():
        st.pyplot(esc_fig)
#==================================== ocupacao ==================================================#
    df_ocup_ano = pd.DataFrame(df.groupby(['ano','SEXO','OCUP']).agg('size'))
    df_ocup_ano.columns = ['size']
    # Masculino 
    
    def ocupacao():
        ocup_masc= make_text(1,
          3,
          2,
          list(df_ocup_ano.loc[(ano,'Masculino')].sort_values(by='size',ascending= False)[:3]['size']),
          list(df_ocup_ano.loc[(ano,'Masculino')].sort_values(by='size',ascending= False)[:3].index),
          figsize = (20,2), 
          title2 = 'Ocupação das vítimas do sexo Masculino',
          font_title = 40)
        st.pyplot(ocup_masc)
        ocup_fem= make_text(1,
          3,
          2,
          list(df_ocup_ano.loc[(ano,'Feminino')].sort_values(by='size',ascending= False)[:3]['size']),
          list(df_ocup_ano.loc[(ano,'Feminino')].sort_values(by='size',ascending= False)[:3].index),
          figsize = (20,2), 
          title2 = 'Ocupação das vítimas do sexo Feminino',
          font_title = 40)
        st.pyplot(ocup_fem)
          
#====================================== code ====================================================#
    if option == 'Porcentagem de vítimas Masculinas e Femininas':
        vitimas()
    elif option == "Taxa de Suicídio por 100 mil habitantes dos estados":
        mapa_suicide()
    elif option =="Número de suicídio por RAÇA / COR":
        Raçacor()
    elif option =="Número de suicídio por estado civil":
        estadocivil()
    elif option =="Suicídio no Brasil por faixa etária":
        faixaetaria()
    elif option =="Locais onde ocerram os suicídios":
        local_ocorrencia()
    elif option =="Suicídio por nível de escolaridade":
        escolaridade()
    elif option =="Ocupação das vítimas":
        ocupacao()

#================================== code ============================================

if options == "Início":
    home()
elif options == "Setembro Amarelo":
    SetAmarelo()
elif options =="Perfil Das Vítimas":
    perfil()
elif options =="Dashboard":
    dashboard()
