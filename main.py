import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fft
from scipy.signal import lombscargle
from scipy import optimize as opt
import analizza 



dati = 'dati.txt'



df1 = pd.read_csv(dati,header=None,comment='#', sep='\t') 
df1.columns = [df1[0][0], df1[1][0], df1[2][0], df1[3][0], df1[4][0]] 
df1 = df1.dropna() 
df1 = df1.iloc[1:] 



time = df1.age_calBP.values #tempo in anni dal 1950
time = time.astype(float)
delta = np.diff(time)
temp = df1.Temperature #temperatura in variazione di gradi centigradi rispetto alla media dei mille anni precedenti 
temp = temp.astype(float)
temp = temp.values

num = 5000



an = analizza.Analyze(time[:5000], temp[:5000])

index = an.uniform(286)

uniform_time, uniform_temp = an.datas()

dx = np.linspace(0, len(time), len(time)-1)
dxu = np.linspace(0, 5000, len(uniform_time)-1)
delta = np.diff(time)
delta_uniform = np.diff(uniform_time)
fm = np.mean(delta_uniform)

fig, ax = plt.subplots(1, 2, figsize = (16, 6))

ax[0].plot(time, temp, label = 'dati originali')
ax[0].plot(uniform_time, uniform_temp,label=  'dati uniformati')
ax[0].set_xlabel('tempo(anni dal 1950)')
ax[0].set_ylabel('variazione di temperatura rispetto alla media dei 1000 anni precedenti (°C)')
ax[0].set_title('Andamento della temperatura nel tempo')
ax[0].legend(loc = 'upper right')

ax[1].plot(dx, delta, '-o', label = 'dati originali')
ax[1].plot(index[1:], delta_uniform, '-o', label = 'dati uniformati')
ax[1].plot([0, 6000], [fm, fm], 'r')
ax[1].set_xlabel('indice')
ax[1].set_ylabel('intervallo di campionamento (anni)')
ax[1].legend(loc = 'upper right')
ax[1].set_title('Intervallo di campionamento')
plt.show()





freq, trasf  = an.trasff()
freq = freq[:int(len(freq)/2)]
power = np.abs(trasf[:len(trasf)//2])**2
fmax, pmax = an.trova_picco(freq, power)


plt.plot(freq, power, '-o')
plt.plot(fmax ,pmax, 'ro', label = 'valore di picco')
plt.xlabel('frequenza (anni$^{-1}$)')
plt.ylabel('potenza (u.a.)')
plt.xscale('log')
plt.yscale('log')
plt.title('Spettro di potenza della temperatura')
plt.legend(loc = 'upper left')
plt.show()




temp_r = np.copy(uniform_temp)
ntemp = an.sintetizza(temp_r)

an1 = analizza.Analyze(uniform_time, ntemp)


nfreq, ntrasf = an1.trasff()
nfreq = nfreq[:int(len(nfreq)/2)]
npower = np.abs(ntrasf[:ntrasf.size//2])**2



fig, ax = plt.subplots(1, 2, figsize = (16, 6))
fig.subplots_adjust(hspace=0)


ax[0].plot(uniform_time, uniform_temp, label = 'dati iniziali')
ax[0].plot(uniform_time, ntemp, label = 'dati mescolati', color = 'tab:orange')
ax[0].set_xlabel('tempo (anni dal 1950)')
ax[0].set_ylabel('variazione di temperatura rispetto alla media dei 1000 anni precedenti (°C)')

ax[1].plot(freq, power, '-o', label = 'spettro di potenza')
ax[1].plot(nfreq, npower, '-o', label = 'spettro di potenza per dati mescolati', color = 'tab:orange')
ax[1].set_xscale('log')
ax[1].set_yscale('log')
ax[1].set_xlabel('frequenza (anni$^{-1}$)')
ax[1].set_ylabel('potenza (u.a.)')

ax[0].legend(loc = 'upper right')
ax[1].legend(loc = 'upper right')

fig.suptitle('Esempio di dati sintetici e relativo spettro di potenza')
plt.show()

v = an.valuta(uniform_temp, 1000000)

plt.hist(v, 30, label = 'picchi sintetici')
plt.scatter(pmax, 1, color = 'r', label = 'valore osservato')
plt.yscale('log')
plt.xlabel('potenza massima (u.a.)')
plt.ylabel('numero di elementi')
plt.legend()
plt.title('Simulazione di significatività del picco')
plt.show()


freq_m, trasf_m = an.maschera(7e4)
freq_m = freq_m[:int(len(freq_m)/2)]
power_m = np.abs(trasf_m[:trasf_m.size//2])**2

plt.plot(freq, power, '-o', label = 'spettro di potenza')
plt.plot(freq_m, power_m, 'o', label = 'spettro filtrato') 
plt.xscale('log')
plt.yscale('log')
plt.xlabel('frequenza (anni$^{-1}$)')
plt.ylabel('potenza (u.a.)')
plt.legend()
plt.title('Spettro di potenza della temperatura')
plt.show()

temp_masked = an.reconstruct(trasf_m)

plt.plot(uniform_time, uniform_temp, label = 'dati iniziali')
plt.plot(uniform_time, temp_masked, label = 'dati ricostruiti')
plt.xlabel('tempo (anni dal 1950)')
plt.ylabel('variazione di temperatura rispetto alla media dei 1000 anni precedenti (°C)')
plt.title('Andamento della temperatura nel tempo')
plt.legend(loc = 'upper right')
plt.show()

def f_ip(x, A, B):
    return A/x**B 

n = 20

params, params_covariance = opt.curve_fit(f_ip, freq[n:], power[n:],p0 = [1e-5, 2], maxfev=10000)

print(params)

xfreq = np.linspace(1e-6, np.max(freq), len(freq))
yfreq = f_ip(xfreq, params[0], params[1])

plt.plot(freq, power, '-o', label = 'spettro di potenza')
plt.plot(freq[n:], power[n:], '-o', label = 'dati della regressione') 
plt.plot(xfreq, yfreq, label  = 'funzione di regressione')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('frequenza (anni$^{-1}$)')
plt.ylabel('potenza (u.a.)')
plt.legend()
plt.title('Regressione dello spettro di potenza ad una curva')
plt.show()


freq1 = np.linspace(2e-6, 3e-3, len(uniform_time))
puls = 2*np.pi*freq1

pgram = lombscargle(time, temp, puls, normalize = False)



plt.plot(freq1, pgram, '-o', label  = 'coefficienti ottenuti con Lomb-Scargle')
plt.plot(freq, power, '-o', label = 'coefficienti ottenuti con fft')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('frequenza (anni$^{-1}$)')
plt.ylabel('potenza (u.a.)')
plt.legend()
plt.title('Confronto fra Lomb-Scargle e fast Fourier transform')
plt.show()
