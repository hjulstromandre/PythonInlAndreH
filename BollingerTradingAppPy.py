# Importerar numpy, för att kunna generera (pseudo)slumpade tal.
# importerar plotly för att generera diagram som är mer interaktiva än matplot.
# eftersom att flera linjer inkluderas i diagrammet, används graph_objects.
# pandas importeras för att skapa dataframes där den genererade datan ingår.
# För att göra statistiska uträkningar (t.ex. standardavvikelser) importeras statistics-biblioteket.

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import statistics
'''
Nytt kodblock

'''

# priceindex är varje given tidpunkt för simulationen (representerar x-axeln i diagrammet).
# stockprices populeras med aktiepriser när simulationen körs (representerar y-axeln i diagrammet).
# tradingperiod är längden på simulationens period.

# profitorloss-variabeln blir tillskriven ett värde för varje iteration.
# Det representerar den procentuella sänkningen eller ökningen

# startprice är aktiens ursprungliga värde, det styr kursens inledande fas tillsammans med profitorloss.
# windowsize är längden på det spann av värden/aktiepriser vi vill räkna ut genomsnittet för.

# standarddeviations är antalet standardavvikelser från spannets genomsnitt vi vill att köp och sälj-signalerna ska baseras på.
# Detta avgör alltså distansen från det glidande genomsnittet som Bollinger-banden kommer ha.

priceindex = []
stockprices = []
tradingperiod = int(input("Ange antalet tidsenheter tradingsimulatorn körs"))
profitorloss = 1
startprice = float(input("Ange aktiens initiala värde i början av tidsperioden"))
windowsize = int(input("Ange antalet tidsenheter som det glidande medelvärdet ska beräknas över"))
standarddeviations = float(input("Ange antalet standardavvikelser som du vill att Bollinger-banden ska vara från det glidande genomsnittet"))

# Generateprices-funktionen ansvarar för att skapa de listor som dataframen baseras på.
# chance-variabeln är sannolikheten att ett slumpgenererat tal faller inom ett angivet soann. Detta avgör om kursen går upp eller ner
# Efter att listan med aktiepriser börjat populeras, blir det senaste värdet i listan det som utsätts för upp eller nedgång. I början är det istället det startvärde som användaren angav

def generateprices():
    for i in range(tradingperiod): # Här fylls listorna som utgör x och y-värden för diagrammet.
        priceindex.append(i) # Varje index sparas i listan för tidpunkter .
        chance = np.random.randint(0, 12585)
        if chance <6200: # sannolikheten att aktien stiger (cirka 49,3%).
            profitorloss = 1.01503 # Aktien stiger med 1,5% om det slumpade värdet är under 6200.
        else:
            profitorloss = 0.98574 # Aktien sjunker med lite över 1,4% om värdet är annat än ovanstående.
        if len(stockprices) == 0: # I simulationens initiering är startpriset multiplicerat med prisfluktuationen
           stockprices.append(startprice * profitorloss) # Aktiepriset läggs till i listan.
        if len(stockprices) > 0 and len(stockprices) < tradingperiod: # Om aktieprislistan är längre än 0, är det senaste värdet som lagts till, det som ska vara föremål för prisfluktuationen.
            stockprices.append(stockprices[-1] * profitorloss) # Det senaste värdet är det som förändras och resultat placeras framför.

generateprices()

# En Pandas-dataframe skapas, där aktieprisutvecklingen sparas i en ny kolumn kallad "Priser".
# Det glidande genomsnittet räknas ut genom att använda de inbyggda funktionerna "rolling" och "mean", som tar emot aktieprislistan och variablen windowsize som representerar hur många tidsenheter genomsnittet räknas över, sen tar genomsnittet för detta vid varje given tidpunkt som simulationen körs. T.ex. dag 1-20,2-21,3-22 etc... om windowsize är 20. Denna information sparas i en ny kolumn kallad "Moving Average".



df = pd.DataFrame(stockprices, columns=['Priser'])
df['Glidande genomsnitt'] = df['Priser'].rolling(window=windowsize).mean()
df['Övre band'] = np.nan
df['Nedre band'] = np.nan

# Två nya kolumner skapas i dataframen som representerar det övre och nedre bandet (köp respektive säljsignal). Nan-värden populerar dessa kolumner inledningsvis, fram till dess att man kan räkna ut det glidande genomsnittet. Varpå de populeras med genomsnittet för det fönstret + eller - de antal standardavvikelser som användaren angivit.
# För att bandens kolumner ska populeras, behöver vi veta standardavvikelsen inom varje fönster, det utförs genom stdev-metoden från statistics-biblioteket.

def generatebollingerbands():
    for i in range(len(stockprices) - windowsize + 1):
        window = stockprices[i : i + windowsize] # Serien av fönster definieras
        window_average = sum(window) / windowsize # Genomsnittet för alla värden inom varje givet fönster under perioden.
        std_dev = statistics.stdev(window)
        df.loc[i + windowsize - 1, 'Övre band'] = window_average + standarddeviations*std_dev # övre bandets kolumn
        df.loc[i + windowsize - 1, 'Nedre band'] = window_average - standarddeviations*std_dev # nedre bandets kolumn
generatebollingerbands()


'''
Nytt kodblock

'''

# Alla transaktioner som sker läggs in i transaction_history. Varje transaktion är en dictionary, med attributen:
# Period-index: Anger den tidpunkt då transaktionen ägde rum.
# Signal: Syftar på vilken typ av transaktion det rör sig om.
# Stocks in transaction: Antalet aktier som köps eller säljs vid transaktionen.
# Stocks after transaction: Antalet aktier i portfolion efter det att transaktionen ägt rum.
# Bank Amount: Hur mycket kapital som finns kvar efter att transaktionen skett (här ingår ej värdet för portfolions innehav).

# bank-variabeln är ursprungligen det startkapital som användaren angivit att de har. Det blir senare den summa som avgör hur många aktier som kan köpas och dit alla vinster adderas.
# startkapitalet sparas i en variabel, används senare för att bedömma hur mycket man vunnit/förlorat i simulationen, denna variabel är det som subtraheras från slutsumman för att avgöra hur mycket användare ngått på förlust eller vinst
# portfolio-variabeln representerar antalet aktier användaren har vid varje tillfälle. Detta börjar på noll.

transaction_history = []
bank = float(input("Ange startkapital"))
startbank = bank
portfolio = 0


# I transaction-funktionen exekveras transaktioner. Dessa sparas sedan i en ny dataframe (transaction_history), som nämnts ovan. Startkapital och portfoliovariabeln är input till transaction-funktionen.
# En for-loop skapas för att komma åt aktiepriset vid varje indexposition och enumerate används för att iterera över dataframe-kolumnen samtidigt som den spårar indexet för varje värde.

# Sedan ställs villkoren för att ett köp ska äga rum: priset behöver vara lika med eller under det nedre bandet vid den tidpunkten och det måste finnas mer kapital än vad aktien kostar. Varje gång ett köp sker, används en femtedel av det fria kapitalet användaren har vid det skedet. Antalet aktier som köps just det illfället sparas i variabeln stocks_purchased. Om en femtedel av kapitalet underskrider det aktuella aktiepriset, så köps endast en aktie. Om det inte finns tillräckligt med kapital för en aktie och en köpsignal är närvarande, så köper programmet inte något.

# För att en försäljning av innehav ska ske, behöver priset vara lika med eller över det övre bandet och portfolion behöver innehålla fler aktier än 0. Antalet aktier som säljs vid varje tillfälle sparas i stocks_sold variabeln. En femtedel av innehavet säljs vid varje gång om det finns 5 eller fler aktier. Om aktieinnehavet är färre än 5, säljs en åt gången.
# När vi nått slutet av perioden, säljs allt innehav även om ingen säljsignal är närvarande.

def transaction(bank, portfolio):
    for i, price in enumerate(df['Priser']):
        if price <= df['Nedre band'][i] and bank > price:
            stocks_purchased = int(np.floor((bank / 5) / price))
            if np.round(bank / 5) < price:
                stocks_purchased = 1
            portfolio += stocks_purchased
            bank -= round(stocks_purchased * price,
                          2)  # Summan aktierna kostade subtraheras från det tillgängliga kapitalet
            transaction_history.append({'Period-index': i, ' Signal': 'Buy', 'Stocks in transaction': stocks_purchased,
                                        'Stocks after transaction': portfolio, ' Bank Amount': bank,
                                        'Price': round(price, 2)})

        if price >= df['Övre band'][i] and portfolio > 0:
            stocks_sold = int(np.round(portfolio / 5))
            if np.round(portfolio / 5) < 1 and portfolio > 0:
                stocks_sold = 1

            portfolio -= stocks_sold  # Aktierna som sålts subtraheras från innehavet
            bank += round(stocks_sold * price, 2)  # Försäljningens värde adderas till kapitalet
            transaction_history.append({'Period-index': i, ' Signal': 'Sell', 'Stocks in transaction': stocks_sold,
                                        'Stocks after transaction': portfolio, ' Bank Amount': round(bank, 2),
                                        'Price': round(price, 2)})

        if i == len(df['Priser']) - 1:
            bank += portfolio * price
            transaction_history.append({'Period-index': i, ' Signal': 'Sell', 'Stocks in transaction': portfolio,
                                        'Stocks after transaction': 0, ' Bank Amount': round(bank, 2),
                                        'Price': round(price, 2)})
            portfolio = 0


transaction(bank, portfolio)

# För att skapa en tabell som visar var transaktionerna hände under kursens period, ignorereras själva transaktionernas index och index inuti en originella dataframen (som innehåller priser och genomsnitt etc... bevaras och är index i den nya dataframen. Enumerate sparar indexet och datapunkten det gäller i en tuple, concat fogar ihop alla dictionaries från transaction_history till en enhetlig dataframe.
# Dataframen som innehåller simulationen visas i form av en tabell och diagrammet som visar prisutvecklingen, med glidande genomsnitt och Bollinger-band visas.
# I slutet skrivs den total vinstne ut och en jämförelse med vad man hade vunnit/förlorat om man hade köpt aktier för hela startsumman i början av perioden och aldrig sålt

transaction_df = pd.concat([pd.DataFrame(data, index=[i]) for i, data in enumerate(transaction_history)],
                           ignore_index=True)
pd.set_option('display.max_rows', None)  # Möjliggör att alla rader kan synas.

print(transaction_df.to_string(index=False))
fig = px.line(x=priceindex, y=df['Priser'], labels=dict(x='Periodindex', y='Priser'), title='Trading-simulation')
fig.add_trace(go.Scatter(x=priceindex, y=df['Glidande genomsnitt'], mode='lines', name='Glidande genomsnitt'))
fig.add_trace(go.Scatter(x=priceindex, y=df['Övre band'], mode='lines', name='Övre band'))
fig.add_trace(go.Scatter(x=priceindex, y=df['Nedre band'], mode='lines', name='Nedre band'))
fig.show()

print("Total vinst för hela perioden: " + str(transaction_df[' Bank Amount'].iloc[-1] - startbank))
print("Total vinst om man endast köpt i början av perioden och aldrig sålt: " + str(transaction_df['Price'].iloc[-1] * (startbank / startprice) - startbank)) + str()
