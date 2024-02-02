# PythonInlAndreH
Inlämning för pythonkurs

OBS: Se koden i Python-filen, då det visade sig vara problem att visa Notebooken i preview här på GitHub. Jag har markerat var i koden där blockens gränser är. Den är menad att köras som Notebook.

Applikationen är tänkt att vara en testyta för simpel trading-algoritm. Denna går ut på att köpa då aktiepriset verkar billigt i förhållande till trenden och sälja då den verkar dyr. Användaren har möjlighet att avgöra periodens längd, aktiens urpsrungliga värde, hur långt spann av priser som medelvärdet ska räknas på (fönster), samt hur många standardavvikelser från medelvärdet de vill handla utifrån.

Applikationen är indelad i tre huvudsakliga delar:
- Prisgenerering: I den här delen simuleras en prisutveckling genom att använda biblioteken Numpy (random), samt Pandas för att spara denna utveckling i en dataframe för senare analys och visualisering. Funktionen som ansvarar för detta heter: generateprices
- Statistisk analys: I den här delen räknas medelvärdet ut för varje fönster, det börjar på det index som användaren valt. Om användaren väljer 50 som fönsterstorlek, så börjar den räkna medelvärdet för index 50 och bakåt (0-50,1-51,2-52 etc...), detta kallas för gidande medelvärde. Sedan räknas standardavvikelsen ut för varje enskilt fönster och läggs till i form av linjediagram tillsammans med det glidande medelvärdet. Om priset hamnar under det nedre bandet, så köper applikationen och om det hamnar över det övre bandet, säljer applikationen. Funktionen som ansvarar för detta heter: generatebollingerbands
- Trading: I den här delen sker själva köpandet och säljandet utifrån angivna villkor. Logiken är skriven helt utifrån ovannnämnd idé, dvs att köpa billigt och sälja dyrt utifrån den dittills observerade trenden i det ögonblicket då villkoren kontrolleras. Varje transaktion är objekt inuti en dataframe som samlar alla transaktioner för analys och visualisering i tabellformat. Dessa objekt har följande attribut:
  - Period-index: Detta är den positionen simulationen hade då beslutet togs att utföra en transaktion (inte index i listan av transaktioner)
      - Signal: Vilken typ av transaktion det gäller (köp eller sälj)
      - Stocks in transaction: Hur många aktier som köptes eller såldes i det ögonblicket
      - Stocks after transaction: Hur många aktier som finns i portfolion efter transaktionen ägt rum
      - Bank Amount: Hur mycket fritt kapital användaren har i simulationen efter transaktionen utförts
      - Price: Priset för aktien då transaktionen skedde
  
Funktionen som ansvarar för denna del av applikationen heter: transaction

Slutligen visas diagrammet med prisutvecklingskurvan, glidande medelvärde för perioden och Bollinger-banden. Förutom detta visas även transaktionshistoriken i form av en dataframe-tabell där man kan se vid vilka skeden applikationen sålt och köpt aktier. Det visas även en jämförelse mellan total vinst efter periodens slut och hur mycket man hade haft om man helt enkelt hade köpt aktier för allt fritt kapital och hållt för hela perioden utan vidare transaktioner.
  
