import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fft
from scipy.signal import lombscargle
from scipy import optimize as opt


'''

classe per l'analisi di Fourier dei dati

metodi:

'''



class Analyze:
    #__init__(time, temp): costruttore, acquisisce un array di tempo e uno di temperatura
    def __init__(self, time, temp):
        self.time = np.array(time)
        self.temp = np.array(temp)


    #datas(): ritorna i dati

    def datas(self):
        return self.time, self.temp


    #uniform(passo): uniforma i campionamenti lungo l'asse temporale dato un passo, aggiorna i dati 

    def uniform(self, passo):
        array = self.time
        array_unif = np.array([array[0]])
        indici = np.array([0])
        for i in range(1,len(array)-1):
            c = np.absolute(array[i]-array_unif[-1]-passo)
            ci =np.absolute(array[i-1]-array_unif[-1]-passo)
        
            if c > ci:
            
                if np.abs(array[i-1]-array[i]) > np.abs(array[i] - array[i+1]):
                    array_unif = np.append(array_unif, array[i])
                    indici = np.append(indici, i)
                else:
                    array_unif = np.append(array_unif, array[i-1])
                    indici = np.append(indici, i-1)
                
        self.time = array_unif
        self.temp = self.temp[indici]
        return indici

    #trasff(): fa la trasformata di Fourier, ritorna lo spettro di potenza ed i coefficienti

    def trasff(self):
        trasf = fft.fft(self.temp)
        delta = np.diff(self.time)
        fm = np.mean(delta)
        freq  = fft.fftfreq(len(trasf), fm)
        return freq,trasf


    #maschera(soglia): prende solo i picchi sopra una soglia fissata

    def maschera(self, soglia):
        freq, trasf = self.trasff()
        mask = np.abs(trasf)**2 < soglia
        fil_trasf = trasf.copy()
        fil_freq = freq.copy()
        fil_trasf[mask] = 0
        fil_freq[mask] = 0
        return fil_freq, fil_trasf        
        

    
    #reconstruct(coeff): fa l'antitrasformata 

    def reconstruct(self, coeff, num = None):
        if num is None:
            num = len(self.temp)
        y = fft.irfft(coeff, n = num)
        return y


#class 
    
    
    #trova_picco(trasf, freq): trova il picco non nullo dello spettro di potenza

    def trova_picco(self, freq, power):      
        i = np.argmax(power)
        if freq[i] == 0:
            power = np.delete(power, i)
            freq = np.delete(freq, i)
            j = np.argmax(power)
            return freq[j], power[j]
        else:
            return freq[i], power[i]

        
    #sintetizza(array): crea un nuovo array rimescolando i dati in ingresso

    def sintetizza(self, array):
        copia = np.copy(array)
        np.random.shuffle(copia)
        return copia

    #valuta(n): crea n serie di dati sintetici e restituisce un array con i rispettivi massimi

    def valuta(self,array, n):
        massimi = np.empty(n)
        for i in range(n):
            print(round(i/n*100, 3), '%')
            nuovo = self.sintetizza(array)
            trasf = fft.fft(nuovo)
            delta = np.diff(self.time)
            fm = np.mean(delta)
            freq = fft.fftfreq(len(trasf), fm)            
            power = np.abs(trasf[:trasf.size//2])**2
            a, m = self.trova_picco(freq, power)
            massimi[i] = m

        return massimi

    



    

