# Esame


Repository per la consegna del progetto di Metodi Computazionali per la Fisica. 

Nella cartella sono contenuti il file "dati.txt", il modulo "analizza.py" e il file "main.py". I dati possono in alternativa essere scaricati da https://www.ncei.noaa.gov/pub/data/paleo/icecore/antarctica/epica_domec/edc3deuttemp2007-noaa.txt. Nella classe sono definiti i metodi utilizzati nel main. 

Per eseguire il programma è necessario aggiungere nella repository di main.py la classe analizza e il file dati, se non presenti è necessario modificiare il percorso di importazione degli stessi nel main. Lanciando main.py viene eseguito l'intero progetto, in alternativa si possono testare i metodi contenuti in analizza.py singolarmente in un file separato importando la classe. 








Il modulo analizza.py contiene la classe Analyze che ha i seguenti metodi:

__init__(time, temp): è il costruttore, salva il tempo e la temperatura in dei campi

datas(): restituisce i dati salvati nei campi di tempo e temperatura

uniform(passo): uniforma i dati in modo tale da ottenere un campionamento uniforme rispetto ad un passo dato, aggiorna i dati e restituisce gli indici dei dati selezionati

trasff(): fa la trasformata di Fourier dei dati salvati usando fft di scipy, restituisce i valori di frequenza ed i coefficenti della trasformata

maschera(soglia): seleziona solo i picchi dello spettro di potenza sopra una soglia data, restituisce l'array dei coefficienti con i dati sotto soglia mandati a zero

reconstruct(coeff, *args, num = None): fa l'antitrasformata, ricostruisce i dati a partire dai coefficenti dati, il numero di elementi ricostruito è uguale al numero di elementi iniziali, può essere cambiato modifcando il valore di num

trova_picco(freq, power): trova il picco dello spettro di potenza, ne restituisce la frequenza corrispondente e il valore

sintetizza(array): crea un nuvo array di dati sintetici ottenuto mescolando casualmente i valori in ingresso, restituisce l'array con gli elementi mescolati

valuta(array, n): crea un numero a scelta n di dati sintetici a partire da un array di elementi dato, per ogni serie di dati sintetici trova il corrispettivo valore massimo di potenza e lo salva in un array, restituisce quindi tale array


Nel main sono stati testati tutti i metodi sopra indicati, si sono inoltre utilizzate le funzioni lombscargle di scipy.signal e optimize sempre di scipy, essendo tali funzioni usate una volta sola non è stato necessario creare dei moduli appositi. 

 
