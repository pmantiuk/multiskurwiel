import pandas as pd
import itertools

#--- otwiera listę, dla której chcemy znaleźć multiściany, trzeba to będzie przerobić na funkcję 'input'; 
#--- w przypadku problemów z ładowaniem plików 'xlsx' trzeba dodać silnik odczytu: 'openpyxl'
df = pd.read_excel(r'C:\Users\pmantiuk\Desktop\5-315-16X.xlsx', sheet_name = 'Sciany', skiprows=(4), engine = 'openpyxl') 

#--- odfiltrowuje z data frame puste wiersze
filt = df['Numer'].notnull()
df = df[filt]

#--- zawęża data frame do kolumn: numer, słupek, H ramy i L całk
#--- sortuje dane po grubości słupka
df = df[['Numer','Słupek','H ramy','L całk']]
df['Słupek'] = df['Słupek'].apply(round)
df['H ramy'] = df['H ramy'].apply(round)
df['L całk'] = df['L całk'].apply(round)
df.sort_values(['Słupek','H ramy','Numer'], inplace = True)
parametry_ścian = df.to_dict(orient="index")

#--- trzeba wprowadzić możliwość wyboru z jakich długości belek będą wycinane dane przekroje
#--- przykładowo:    LVL 51x100x130000
#---                 KVH 50x100x5000
#--- na razie jest to ustawione na sztywno na 13 metrów
max_lenght = 13000

#--- wyodrębnienie unikatowych grubości słupków i wysokości ścian
przekroje_słupków = sorted(set(x['Słupek'] for x in parametry_ścian.values()))
wysokości_ścian = sorted(set(x['H ramy'] for x in parametry_ścian.values()))


def znajdz_najlepsza_kombinacje(kombinacje, słupek, wysokość, kombo):
    najdłuższy_pas = []
    for x,kombinacja in enumerate(kombinacje,1):
        ściany = []
        pas_multiściany = sum(kombinacja)
        # print(f'{x}:{kombinacja} : {pas_multiściany/1000} m')
        for l in kombinacja:
            ściany.append(list(kombo.keys())[list(kombo.values()).index(l)])
        # print(f'To są ściany z kombinacji {ściany}')
        zestaw = (x, pas_multiściany)
        if najdłuższy_pas:
            if pas_multiściany > najdłuższy_pas[1]:
                najlepsza_kombinacja.pop()
                najdłuższy_pas.extend(zestaw)
        else: 
            najdłuższy_pas.extend(zestaw)
            
               
    # return print(f'kombinacja {najdłuższy_pas[0]} : {najdłuższy_pas[1]/1000} m \n')  
                 

#--- pętla grupuje nazwy ścian o tej samej grubości słupka i wysokości            
for słupek in przekroje_słupków: 
    for wys in wysokości_ścian:
        nazwy_ścian = []
        dł_ścian = []  
        
        for value in parametry_ścian.values():
            if value['Słupek'] == słupek and value['H ramy'] == wys:
                nazwy_ścian.append(value['Numer'])
                dł_ścian.append(value['L całk'])  
        print(f'Słupek: {słupek}, wys: {wys} : {nazwy_ścian}') # printuje przekrój słupka i wysokość ściany

#--- sprawdza czy lista 'dł ścian' nie jest pusta, czyli czy dla danego słupka występują zadane wysokości ścian, jeśli nie, pętla przechodzi do kolejnej iteracji
        if dł_ścian:
            #--- tworzy słownik nazw i długości ścian o tych samych słupkach i wysokościach
            kombo = dict(zip(nazwy_ścian, dł_ścian))
            możliwe_pasy = {}
            for x in reversed(range(1,len(dł_ścian)+1)):
                combinations = itertools.combinations(dł_ścian, x)
                indeksy = itertools.combinations(range(len(dł_ścian)), x)  
                dł_indeksy = list(zip(combinations, indeksy))
                print(f'możliwe kombinacje dla {x} ścian/y {dł_indeksy}')   
            
                for z,y in dł_indeksy:
                    if sum(z) < max_lenght:
                        możliwe_pasy['ilość ścian'] = x
                        możliwe_pasy['długość pasa'] = (sum(z))
    
            print(f'-------------możliwe pasy: {możliwe_pasy}')
                        

