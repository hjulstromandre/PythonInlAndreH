import numpy as np # Importerar numpy, för att kunna generera (pseudo)slumpade tal.
import plotly.express as px # importerar plotly för att generera diagram som är mer interaktiva än matplot.
import plotly.graph_objects as go # eftersom att flera linjer inkluderas i diagrammet, används graph_objects.
import pandas as pd # pandas importeras för att skapa dataframes där den genererade datan ingår.
import statistics # För att göra statistiska uträkningar (t.ex. standardavvikelser) importeras statistics-biblioteket.

'''
Nytt kodblock

'''

priceindex = [] #Index/varje given tidpunkt för simulationen (representerar x-axeln i diagrammet).
stockprices = [] # En lista som populeras med aktiepriser när simulationen körs (representerar y-axeln i diagrammet).
tradingperiod = int(input("Ange antalet tidsenheter tradingsimulatorn körs")) # Längden på simulationens period.
profitorloss = 1 # Ett värde tillskrivs hit för varje tidsenhert som simulerar prisfluktuation. Start är 1, då det ursprungliga aktievärdet bör vara 100% av det användaren angivit
startprice = float(input("Ange aktiens initiala värde i början av tidsperioden")) # Aktiens ursprungliga värde, det styr antalet enheter man kan köpa vid varje given tidpunkt.
windowsize = int(input("Ange antalet tidsenheter som det glidande medelvärdet ska beräknas över")) # En nödvändig variabel för att uträkna det glidande genomsnittet, samt Bollinger-bandens beskaffenhet.
standarddeviations = float(input("Ange antalet standardavvikelser som du vill att Bollinger-banden ska vara från det glidande genomsnittet"))

def generateprices():
    for i in range(tradingperiod): # Här fylls listorna som utgör x och y-värden för diagrammet.
        priceindex.append(i) # Varje index sparas i listan för tidpunkter .
        chance = np.random.randint(0, 12585) # Chance-variabeln represneterar sannolikheten att priset stiger eller sjunker vid varje given tidpunkt, tröskeln är godtyckligt vald för att skapa mer intressanta prisutvecklingar. Datan gällande fluktuationer är hämtad från tester av S&P aktier.
        if chance <6200: # sannolikheten att aktien stiger (cirka 49,3%).
            profitorloss = 1.01503 # Aktien stiger med 1,5% om det slumpade värdet är under 6200.
        else:
            profitorloss = 0.98574 # Aktien sjunker med lite över 1,4% om värdet är annat än ovanstående.
        if len(stockprices) == 0: # I simulationens initiering är startpriset multiplicerat med prisfluktuationen det vi vill lägga in i aktieprislistan.
           stockprices.append(startprice * profitorloss) # Aktiepriset läggs till i listan.
        if len(stockprices) > 0 and len(stockprices) < tradingperiod: # Om aktieprislistan är längre än 0, är det senaste värdet som lagts till, det som ska vara föremål för prisfluktuationen.
            stockprices.append(stockprices[-1] * profitorloss) #Det senaste värdet i aktieprislistan blir utsatt för procentuell sänkning eller ökning och läggs till längst fram i listan. Detta repeteras sedan för hela tidsperioden som användaren angivit.

generateprices()

df = pd.DataFrame(stockprices, columns=['Data']) # En Pandas-dataframe skapas, där aktieprisutvecklingen sparas i en ny kolumn kallad "Data".


df['Glidande genomsnitt'] = df['Data'].rolling(window=windowsize).mean() # Det glidande genomsnittet räknas ut genom att använda de inbyggda funktionerna "rolling" och "mean", som tar emot aktieprislistan och variablen windowsize som representerar hur många tidsenheter genomsnittet räknas över, sen tar genomsnittet för detta vid varje given tidpunkt som simulationen körs. T.ex. dag 1-20,2-21,3-22 etc... om windowsize är 20. Denna information sparas i en ny kolumn kallad "Moving Average".


df['Övre band'] = np.nan #En ny kolumn skapas i df som representerar det övre bandet (säljsignal) OBS: nan-värden populerar dessa kolumner inledningsvis, fram till dess att man kan räkna ut det glidande genomsnittet.
df['Nedre band'] = np.nan #En ny kolumn skapas i df som representerar det nedre bandet (köpsignal).

def generatebollingerbands():
    for i in range(len(stockprices) - windowsize + 1): #Här populeras dataframe-kolumnerna för övre och nedre banden. Spannet som loopen går igenom representerar det rum som det glidande genomsnittet kan räknas ut inom, vilket beror på periodens längd, liksom fönstrets storlek.
        window = stockprices[i : i + windowsize] # window-variabeln representerar ett spann av värden vars start och slut ökar med ett inkrement för varje loop-omgång fram till dess att det nått slutet av aktieprislistan.
        window_average = sum(window) / windowsize # Genomsnittet för alla värden inom varje givet fönster under perioden.
        std_dev = statistics.stdev(window) # För att bandens kolumner ska populeras, behöver vi veta standardavvikelsen inom varje fönster.
        df.loc[i + windowsize - 1, 'Övre band'] = window_average + standarddeviations*std_dev # Kolumnen som representerar det övre bandet populeras med värden som motsvarar det glidande genomsnittet + så många standardavvikelser som användaren vill att den ska vara över detta värde.
        df.loc[i + windowsize - 1, 'Nedre band'] = window_average - standarddeviations*std_dev # Kolumnen som representerar det nedre bandet populeras med värden som motsvarar det glidande genomsnittet - så många standardavvikelser som användaren vill att den ska vara under detta värde.
generatebollingerbands()

fig = px.line(x=priceindex, y=stockprices) #Linjediagrammet skapas, med index för periodinstans som x-värde och aktiepris som y-värde.
fig.add_trace(go.Scatter(x=priceindex, y=df['Glidande genomsnitt'], mode='lines', name='Glidande genomsnitt')) #En linje läggs till som representerar det glidande genomsnittet.
fig.add_trace(go.Scatter(x=priceindex, y=df['Övre band'], mode='lines', name='Övre band')) # En linje läggs till som representerar det övre Bollinger-bandet. Alla instanser då priset överstiger denna, kommer en säljsignal att skickas.
fig.add_trace(go.Scatter(x=priceindex, y=df['Nedre band'], mode='lines', name='Nedre band')) # En linje läggs till som representerar det nedre Bollinger-bandet. Alla instanser då priset understiger denna, kommer en köpsignal att skickas.

'''
Nytt kodblock

'''

transaction_history = []  # Alla transaktioner som sker läggs in här. Varje transaktion är ett objekt, med attributen:
# Period-index: Anger den tidpunkt då transaktionen ägde rum.
# Signal: Syftar på vilken typ av transaktion det rör sig om.
# Stocks in transaction: Antalet aktier som köps eller säljs vid transaktionen.
# Stocks after transaction: Antalet aktier i portfolion efter det att transaktionen ägt rum.
# Bank Amount: Hur mycket kapital som finns kvar efter att transaktionen skett (här ingår ej värdet för portfolions innehav).

bank = float(input(
    "Ange startkapital"))  # Startvärdet för hur mycket användaren har på det konto som transaktionerna adderar till/subtraherar ifrån
startbank = bank  # startkapitalet sparas i en variabel, används senare för att bedömma hur mycket man vunnit/förlorat i simulationen
portfolio = 0  # Denna variabel sparar antalet aktier. I periodens början är värdet 0


def transaction(bank,portfolio):  # I den här funktionen exekveras köp av aktier, samt sälj av innehav beroende på vilka signaler som genereras.
    for i, price in enumerate(df[
                                  'Data']):  # En for-loop skapas för att komma åt aktiepriset vid varje indexposition och enumerate används för att iterera över dataframe-kolumnen samtidigt som den spårar indexet för varje värde.

        if price <= df['Nedre band'][
            i] and bank > price:  # Här ställs villkoren för att ett köp ska äga rum: priset behöver vara lika med eller under det nedre bandet vid den tidpunkten och det måste finnas mer kapital än vad aktien kostar.
            stocks_purchased = int(
                np.floor((bank / 5) / price))  # En femtedel av kapitalet används för att köpa aktier.
            # Antalet aktier som köps varje gång sparas inuti stocks_purchased
            if np.round(
                    bank / 5) < price:  # Undantaget är om en femtedel av kapitalet understiger det aktuella aktiepriset.
                # I det fallet köper funktionen endast en aktie.
                stocks_purchased = 1

            portfolio += stocks_purchased  # Antalet aktier adderas till portfolion
            bank -= round(stocks_purchased * price,
                          2)  # Summan aktierna kostade subtraheras från det tillgängliga kapitalet
            transaction_history.append({'Period-index': i, ' Signal': 'Buy', 'Stocks in transaction': stocks_purchased,
                                        'Stocks after transaction': portfolio, ' Bank Amount': bank,
                                        'Price': round(price, 2)})
            # transactionhistory-listan tar emot ett transaktionsobjekt innehållande all info vi behöver.

        if price >= df['Övre band'][
            i] and portfolio > 0:  # Här ställs villkoret för att en försäljning ska äga rum: Priset behöver vara lika med eller över det övre bandet och portfolion behöver innehålla fler aktier än 0,
            stocks_sold = int(np.round(
                portfolio / 5))  # Antalet aktier som säljs vid varje tillfälle sparas i stocks_sold variabeln. En femtedel av innehavet säljs vid varje gång om det finns 5 eller fler aktier.
            if np.round(
                    portfolio / 5) < 1 and portfolio > 0:  # Undantaget till detta är då aktierna är färre än 5, då säljs en åt gången
                stocks_sold = 1

            portfolio -= stocks_sold  # Aktierna som sålts subtraheras från innehavet
            bank += round(stocks_sold * price, 2)  # Försäljningens värde adderas till kapitalet
            transaction_history.append({'Period-index': i, ' Signal': 'Sell', 'Stocks in transaction': stocks_sold,
                                        'Stocks after transaction': portfolio, ' Bank Amount': round(bank, 2),
                                        'Price': round(price, 2)})
            # transactionhistory-listan tar emot sälj-händelsen.
        if i == len(df['Data']) - 1:  # I det fall då vi kommit till periodens slut, ska alla aktier säljas och slutgiltiga kapitalet visas.
            bank += portfolio * price  # Aktieinnehavets mängd multiplicerat med det aktuella aktiepriset adderas till kapitalet.
            transaction_history.append({'Period-index': i, ' Signal': 'Sell', 'Stocks in transaction': portfolio,
                                        'Stocks after transaction': 0, ' Bank Amount': round(bank, 2),
                                        'Price': round(price, 2)})
            # Den slutgiltiga försäljningen läggs till i slutet av transaktionshistoriken
            portfolio = 0  # Potfolion töms, då alla aktier är sålda.


transaction(bank, portfolio)  # Startkapital och portfoliovariabeln är input till transaction-funktionen
transaction_df = pd.concat([pd.DataFrame(data, index=[i]) for i, data in enumerate(transaction_history)],
                           ignore_index=True)
# En dataframe skapas vari ingår all data som lagts in vid transaktionerna.
pd.set_option('display.max_rows', None)  # Möjliggör att alla rader kan synas

print(transaction_df.to_string(index=False))  # Dataframen som innehåller simulationen visas
fig.show()  # Diagrammet visas

print("Total vinst för hela perioden: " + str(transaction_df[' Bank Amount'].iloc[-1] - startbank))
print("Total vinst om man endast köpt i början av perioden och aldrig sålt: " + str(
    transaction_df['Price'].iloc[-1] * (startbank / startprice) - startbank))
