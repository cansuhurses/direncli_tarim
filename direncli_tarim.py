# -*- coding: utf-8 -*-
#paketler
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import seaborn as sns
import folium
import geopandas as gpd
import plotly.express as px
from PIL import Image
import numpy as np

st.set_page_config(layout="wide",initial_sidebar_state='collapsed')

#Veri seti içeri aktarma ve manipülasyon
history = pd.read_csv('history.csv')
future = pd.read_csv('future.csv')
tum = pd.read_csv('tum.csv')
ilceler = gpd.read_file('https://raw.githubusercontent.com/tahasarnic/ilceler/master/turkiye-ilceler.geojson')
tum['Bölge'] = tum['Bölge'].astype('object')



dicti_s={'Ortalama günlük sıcaklık farkı': 'Ort. Günlük Sıcaklık Farkı',
 'Günlük ortalama sıcaklık ortalaması': 'GOrtSıcOrt',
 'Günlük minimum sıcaklık ortalaması': 'GMinSıcOrt',
 'Günlük minimum sıcaklığın minimumu': 'GMinSıcMin',
 'Günlük minimum sıcaklığın maksimumu': 'GMinSıcMax',
 'Günlük maksimum sıcaklık ortalaması': 'GMaxSıcOrt',
 'Günlük maksimum sıcaklığın minimumu': 'GMaxSıcMin',
 'Maksimum günlük sıcaklığın maksimumu': 'MaxGMaxSıc'}


dicti_y={'Yoğun yağışlı gün sayısı': 'Yoğun Yağış Sayısı',
 'Aşırı yağışlı gün sayısı': 'Aşırı Yağış Sayısı',
 'Toplam yağış (mm)': 'Toplam Yağış (mm)',
 'Yağışlı gün sayısı': 'Yağışlı Gün Sayısı'}

dicti_d={'Biyolojik gün sayısı': 'Biyolojik Gün Sayısı',
'Don gün sayısı': 'Don Gün Sayısı',
'Buzlu gün sayısı': 'Buzlu Gün Sayısı',
'Yaz günleri sayısı': 'Yaz Günleri Sayısı',
'Tropik gece sayısı': 'Tropik Geceler Sayısı'}

dicti_tum={'Ortalama günlük sıcaklık farkı': 'Ort. Günlük Sıcaklık Farkı',
 'Günlük ortalama sıcaklık ortalaması': 'GOrtSıcOrt',
 'Günlük minimum sıcaklık ortalaması': 'GMinSıcOrt',
 'Günlük minimum sıcaklığın minimumu': 'GMinSıcMin',
 'Günlük minimum sıcaklığın maksimumu': 'GMinSıcMax',
 'Günlük maksimum sıcaklık ortalaması': 'GMaxSıcOrt',
 'Günlük maksimum sıcaklığın minimumu': 'GMaxSıcMin',
 'Maksimum günlük sıcaklığın maksimumu': 'MaxGMaxSıc','Yoğun yağışlı gün sayısı': 'Yoğun Yağış Sayısı',
 'Aşırı yağışlı gün sayısı': 'Aşırı Yağış Sayısı',
 'Toplam yağış (mm)': 'Toplam Yağış (mm)',
 'Yağışlı gün sayısı': 'Yağışlı Gün Sayısı', 'Biyolojik gün sayısı': 'Biyolojik Gün Sayısı',
'Don gün sayısı': 'Don Gün Sayısı',
'Buzlu gün sayısı': 'Buzlu Gün Sayısı',
'Yaz günleri sayısı': 'Yaz Günleri Sayısı',
'Tropik gece sayısı': 'Tropik Geceler Sayısı'}


#Başlık
st.markdown('# Ankara Kırsalında İklim Değişikliğine Dirençli Tarım')
st.markdown('Bu platform, Ankara’nın 5 agro-ekolojik bölgesi içinde tarımsal üretim faaliyetlerinin yoğun olduğu 15 çeper ilçenin iklim değişkenlerine ve ürün verimine ait veri setlerinin analizlerini sunmaktadır. Geçmiş aylık iklim göstergeleri ve yıllık verim miktarları (1994-2020) makine öğrenmesi yöntemleri kullanılarak modellenmiş ve gelecek tahminlemesi yapılmıştır.')
st.markdown('## Agro-Ekolojik Bölge Analizi')
st.markdown('Aşağıdaki grafikte X ve Y eksenlerini sıcaklık, yağış ve diğer agro-klimatik göstergelere göre seçip aralarındaki ilişkileri inceleyebilirsiniz.')
st.markdown('**Not:** Baloncuk büyüklükleri seçili ürünün verimiyle orantılı olarak büyüyüp küçülmektedir.')



#Gapminder-Tarla-Filtreler
row1_0, row1_1, row1_2, row1_3= st.beta_columns([1.35,1,1,1])

with row1_0:
    arpa_bugday = st.radio('Ürün seçiniz:', ['Arpa Verim', 'Buğday Verim'])
    
with row1_1:
    eksen_x = st.selectbox('X-ekseni seçiniz:', ['Sıcaklık', 'Yağış', 'Diğer'])
    eksen_y = st.selectbox('Y-ekseni seçiniz:', ['Yağış', 'Sıcaklık', 'Diğer'])
    
with row1_2:
    if eksen_x== 'Sıcaklık':
        sicaklik_x = dicti_s[st.selectbox('Sıcaklık parametresi (X-ekseni):', list(dicti_s.keys()))]
       
    elif eksen_x== 'Yağış':
        yagis_x = dicti_y[st.selectbox('Yağış parametresi (X-ekseni):', list(dicti_y.keys()))]
       
    elif eksen_x== 'Diğer':
        diger_x = dicti_d[st.selectbox('Diğer parametreler (X-ekseni):', list(dicti_d.keys()))]
        
    if eksen_y== 'Sıcaklık':
        sicaklik_y = dicti_s[st.selectbox('Sıcaklık parametresi (Y-ekseni):', list(dicti_s.keys()))]
        
    elif eksen_y== 'Yağış':
        yagis_y = dicti_y[st.selectbox('Yağış parametresi (Y-ekseni):', list(dicti_y.keys()))]
        
    elif eksen_y== 'Diğer':
        diger_y = dicti_d[st.selectbox('Diğer parametreler (Y-ekseni):', list(dicti_d.keys()))]
        
with row1_3:
    ay_x = st.selectbox('Ay seçiniz (X-ekseni):', [1,2,3,4,5,6,7,8,9,10,11,12])
    ay_y = st.selectbox('Ay seçiniz (Y-ekseni):', [1,2,3,4,5,6,7,8,9,10,11,12])   
    
        
row2_0, row2_1 = st.beta_columns([0.45,1])

with row2_0:
    alt_bolge = pd.DataFrame({'İlçe':list(history['İlçe'].unique()) + ['Yenimahalle', 'Etimesgut', 'Altındağ', 'Mamak', 'Çankaya', 'Keçiören', 'Sincan', 'Akyurt', 'Çamlıdere']})
    alt_bolge['Bölge'] = [3, 1, 1, 1, 3, 2, 2, 2, 4, 1, 4, 4, 4, 4, 4, 5,5,5,5,5,5,5, 2, 3]
    alt_bolge_harita = alt_bolge.merge(ilceler, how = 'left', left_on = 'İlçe', right_on = 'name')
    alt_bolge_harita = gpd.GeoDataFrame(alt_bolge_harita)
    
    m = folium.Map(location = [39.55077, 32.70411], zoom_start=7, width=480,height=310, tiles="cartodbpositron")

    #Renk Tonlu Harita
    choropleth = folium.Choropleth(
        geo_data=alt_bolge_harita,
        data = alt_bolge,
        columns = ['İlçe', 'Bölge'],
        key_on = 'feature.properties.İlçe',
        fill_color='Set1',
        line_opacity = 0.2,
        fill_opacity = 0.8,
        legend_name='Bölge',
        bins = [1,2,3,4,5,6],
        highlight = True
        )
    for key in choropleth._children:
            if key.startswith('color_map'):
                del(choropleth._children[key])
    
    choropleth.add_to(m)
    

    folium.LayerControl().add_to(m)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['İlçe', 'Bölge'], labels=True)
        )
    with st.beta_expander("Agro-ekolojik alt bölge bilgileri için tıklayınız"):
        image = Image.open('altbolgeler.PNG')
        st.image(image)

    folium_static(m)
     

    
with row2_1:
    
    fig = px.scatter(tum, x = [sicaklik_x if eksen_x == 'Sıcaklık' else yagis_x if eksen_x == 'Yağış' else diger_x][0]+str(ay_x), y = [sicaklik_y if eksen_y == 'Sıcaklık' else yagis_y if eksen_y == 'Yağış' else diger_y][0]+str(ay_y), animation_frame='yil', size = arpa_bugday, color = 'Bölge',
          color_discrete_map={1:'#e64545',
                               2:'#5c95c2',
                               3:'#4daf4a',
                               4:'#984ea3'},
          category_orders= {"Bölge":[1,2,3,4]},
          width=1050, height=490,
          animation_group='İlçe',
          hover_name = 'İlçe',
          range_y = [tum[[sicaklik_y if eksen_y == 'Sıcaklık' else yagis_y if eksen_y == 'Yağış' else diger_y][0]+str(ay_y)].min(),tum[[sicaklik_y if eksen_y == 'Sıcaklık' else yagis_y if eksen_y == 'Yağış' else diger_y][0]+str(ay_y)].max()],
          range_x = [tum[[sicaklik_x if eksen_x == 'Sıcaklık' else yagis_x if eksen_x == 'Yağış' else diger_x][0]+str(ay_x)].min(),tum[[sicaklik_x if eksen_x == 'Sıcaklık' else yagis_x if eksen_x == 'Yağış' else diger_x][0]+str(ay_x)].max()],
          template = 'none',
          size_max=60,
          labels = {'Ort. Günlük Sıcaklık Farkı1': 'Ortalama günlük sıcaklık farkı', 'GOrtSıcOrt1': 'Günlük ortalama sıcaklık ortalaması', 'GMinSıcOrt1': 'Günlük minimum sıcaklık ortalaması', 'GMinSıcMin1': 'Günlük minimum sıcaklığın minimumu', 'GMinSıcMax1': 'Günlük minimum sıcaklığın maxsimumu', 'GMaxSıcOrt1': 'Günlük maksimum sıcaklık ortalaması', 'GMaxSıcMin1': 'Günlük maksimum sıcaklığın minimumu', 'MaxGMaxSıc1': 'Maksimum günlük sıcaklığın maksimumu'}
          )
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
    st.plotly_chart(fig)

#########################################################################################################
zamansal = pd.read_csv('zaman.csv').drop('Unnamed: 0', axis = 1)
st.markdown('## İklim Göstergelerinin Zaman İçindeki Değişimi')

row3_0, row3_1 = st.beta_columns([1.33,3])

with row3_0:
    ilce = st.multiselect('İlçe(ler) seçiniz:', list(zamansal['İlçe'].unique()),  default=['Ayaş', 'Şereflikoçhisar'])
    parametre_zaman_1 = st.selectbox('Parametre seçiniz:', list(dicti_tum.keys()))
    parametre_zaman = dicti_tum[parametre_zaman_1]
    
with row3_1:
    zamansal['Zaman'] = 'Geçmiş'
    zamansal.loc[zamansal['yil'] > 2019, 'Zaman'] = 'Gelecek'
    fig = px.line(zamansal[(zamansal['İlçe'].isin(ilce)) & (zamansal['vars'] == parametre_zaman)].sort_values(by = ['yil', 'nums']), x = 'tarih', y = 'value', color = 'İlçe', template = 'none', width = 1050, height = 490, title = str(parametre_zaman_1)+' '+ 'parametresinin zamana bağlı değişimi')
    fig.add_vrect(x0="2020-1", x1="2040-12", 
              annotation_text="Gelecek Tahminleri", annotation_position="top left",
              fillcolor="green", opacity=0.15, line_width=0, annotation=dict(font_size=16))
    fig.update_xaxes(title = dict(text = 'Yıl'))
    fig.update_yaxes(title = dict(text = parametre_zaman_1))
    st.plotly_chart(fig)
    
#####################################################################################################
dictis={'Ort. Günlük Sıcaklık Farkı': 'Ortalama günlük sıcaklık farkı', 'GOrtSıcOrt': 'Günlük ortalama sıcaklık ortalaması', 'GMinSıcOrt': 'Günlük minimum sıcaklık ortalaması', 'GMinSıcMin': 'Günlük minimum sıcaklığın minimumu', 'GMinSıcMax': 'Günlük minimum sıcaklığın maxsimumu', 'GMaxSıcOrt': 'Günlük maksimum sıcaklık ortalaması', 'GMaxSıcMin': 'Günlük maksimum sıcaklığın minimumu', 'MaxGMaxSıc': 'Maksimum günlük sıcaklığın maksimumu'}

 

st.markdown('## Buğday ve Arpanın Verimini Etkileyen En Önemli İklim Değişkenleri')
st.markdown('Ürün verim tahmininde bulunmak için kullanılacak **önemli tahmin edici parametreler** yapay öğrenme algoritmalarıyla bulunmuştur.')

 

tablo = pd.read_csv('tum.csv')
tablo = tablo[tablo['yil'] > 2019].iloc[:,2:]
arpa_onemli = pd.read_excel('arpa_onemli.xls')
arpa_onemli_2 = pd.read_excel('arpa_onemli2.xls')
bugday_onemli = pd.read_excel('bugday_onemli.xls')
bugday_onemli_2 = pd.read_excel('bugday_onemli2.xls')

arpa_parametre = dict()
for i in range(len(arpa_onemli)):
    arpa_parametre[arpa_onemli['ilce'][i]] = list((arpa_onemli['Parametre1'][i], arpa_onemli['Parametre2'][i], arpa_onemli['Parametre3'][i]))
bugday_parametre = dict()
for i in range(len(bugday_onemli)):
    bugday_parametre[bugday_onemli['ilce'][i]] = list((bugday_onemli['Parametre1'][i], bugday_onemli['Parametre2'][i], bugday_onemli['Parametre3'][i]))
for i in range(len(arpa_onemli)):
    arpa_parametre[arpa_onemli['ilce'][i]] = list((arpa_onemli['Parametre1'][i], arpa_onemli['Parametre2'][i], arpa_onemli['Parametre3'][i]))
bugday_parametre = dict()
for i in range(len(bugday_onemli)):
    bugday_parametre[bugday_onemli['ilce'][i]] = list((bugday_onemli['Parametre1'][i], bugday_onemli['Parametre2'][i], bugday_onemli['Parametre3'][i]))
    
arpa_parametre2 = dict()
for i in range(len(arpa_onemli)):
    arpa_parametre2[arpa_onemli_2['ilce'][i]] = list((arpa_onemli_2['Parametre1'][i], arpa_onemli_2['Parametre2'][i], arpa_onemli_2['Parametre3'][i]))
    
bugday_parametre2 = dict()
for i in range(len(bugday_onemli_2)):
    bugday_parametre2[bugday_onemli_2['ilce'][i]] = list((bugday_onemli_2['Parametre1'][i], bugday_onemli_2['Parametre2'][i], bugday_onemli_2['Parametre3'][i]))    
    
    
dicti=dict()
for i in arpa_parametre.keys():
    for j in range(3):
        dicti[arpa_parametre[i][j]]=arpa_parametre2[i][j]
        
       
dicti1=dict()
for i in bugday_parametre.keys():
    for j in range(3):
        dicti1[bugday_parametre[i][j]]=bugday_parametre2[i][j]     


        
row6_0, row6_1, row6_2, row6_3 = st.beta_columns([1.33,1,1,1])

with row6_0:
    urun_tablo = st.radio('Önemli parametre değerlerini görmek istediğiniz ürünü seçiniz:', ['Arpa Verim', 'Buğday Verim'])
    ilce_tablo = st.selectbox('Önemli parametre değerlerini görmek istediğiniz ilçeyi seçiniz:', list(tablo['İlçe'].unique()))
        
with row6_1:
    st.text('')        
        
        
with row6_2:
    if urun_tablo == 'Arpa Verim':
        tablo.rename(columns = dicti, inplace = True)
        st.table(tablo[tablo['İlçe'] == ilce_tablo][['yil'] + arpa_parametre2[ilce_tablo]].iloc[0:20:2,:].reset_index(drop = True).set_index('yil').style.bar(subset=arpa_parametre2[ilce_tablo], align='mid', color=['#FF8C7E', '#FDBE88']).hide_index())
    else:
        tablo.rename(columns = dicti1, inplace = True)
        st.table(tablo[tablo['İlçe'] == ilce_tablo][['yil'] + bugday_parametre2[ilce_tablo]].iloc[0:20:2,:].reset_index(drop = True).set_index('yil').style.bar(subset=bugday_parametre2[ilce_tablo], align='mid', color=['#FF8C7E', '#FDBE88']).hide_index())
        
with row6_3:
    st.text('')       

    
#####################################################################################################
st.markdown('## Buğday ve Arpanın Verim Öngörüleri')
st.markdown('Yapay öğrenme modelleri yoluyla ürün verim öngörüleri elde edilmiştir. İlgili ürün veriminin tahmininde kullanılan yukarıdaki parametreler doğrultusunda "Ürün Verim Öngörüleri" haritalandırma çalışması görünmektedir.')

row4_0, row4_1= st.beta_columns([1,3])
heat = pd.read_csv('tum.csv').iloc[:,2:]


with row4_0:
    urun = st.radio('Ürün seçiniz', ['Arpa Verim', 'Buğday Verim'])
    ilce_heat = st.multiselect('İlçe(ler) seçiniz', list(heat['İlçe'].unique()),  default=['Ayaş', 'Çubuk', 'Güdül', 'Gölbaşı(Ankara)', 'Polatlı', 'Elmadağ','Bala'])
    baslangic = st.number_input('Başlangıç yılı giriniz:', value = 1994)
    bitis = st.number_input('Bitiş yılı giriniz:', value = 2040)
    
with row4_1:
    fig = px.imshow(heat[(heat['yil'] >= baslangic) & (heat['yil'] <=  bitis) & (heat['İlçe'].isin(ilce_heat))].pivot_table(index = 'İlçe', columns = 'yil', values = urun), color_continuous_scale = px.colors.sequential.OrRd,
               labels=dict(x="Yıl", y="   ", color=urun),
               width = 925,
               title = 'Zaman Bazlı Verim Analizi')
    fig.update_layout(
    title={
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    st.plotly_chart(fig)


###################################################################################################

gelecek = pd.read_csv('tum.csv')
ilceler = gpd.read_file('https://raw.githubusercontent.com/tahasarnic/ilceler/master/turkiye-ilceler.geojson')
gelecek = tum.iloc[:,2:]
gelecek = gelecek[gelecek['yil'] > 2019].reset_index(drop = True)
gelecek_geo = gelecek.merge(ilceler, how = 'left', left_on = 'İlçe', right_on = 'name')
gelecek_geo = gpd.GeoDataFrame(gelecek_geo)
    

row5_0, row5_1 = st.beta_columns([1.37,3])

with row5_0:
    yil_map = st.select_slider('Yıl seçiniz:', options=list(gelecek.yil.unique()))
    #urun_map = st.radio('Ürün:', ['Arpa Verim', 'Buğday Verim'])
    
with row5_1:
    m = folium.Map(location = [39.70077, 33.10], zoom_start=8, width = 900, height = 500, tiles="cartodbpositron")
    #Renk Tonlu Harita
    choropleth = folium.Choropleth(
        geo_data=gelecek_geo[gelecek_geo['yil'] == yil_map],
        data = gelecek[gelecek['yil'] == yil_map],
        columns = ['İlçe', urun],
        key_on = 'feature.properties.İlçe',
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=urun + ' ' + 'Tahmini'
        ).add_to(m)

    folium.LayerControl().add_to(m)
    choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['İlçe',urun], labels=True)
        )        
    folium_static(m)     

############################################################################################################

    
