new-model.p : en förtränad modell tränad på två kategorier endast till för testning.

new-model-tester.py : skickar in 'test-image.jpg' till new-model.p som returnerar matchning i procent mot modellens två kategorier. Resultat skrivs till result.json och printas till terminalen.

Utveckling:

Med python modulen 'flask':

Utöka new-model-tester.py till att med flask vara en REST API server och vänta på anrop. Servern tar emot requests som innehåller en bild och skickar tillbaka 'result.json'