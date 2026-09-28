
#!/usr/bin/env python
# coding: utf-8

# In[1]:


# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *
import plotting 
import pmd_module 


pmd_module.print_smth()


##  ipython nbconvert --to latex --post PDF <Name.ipynb>

## Parametros generales
T = 1.0/1.0e9 # Periodo de baudio
Nsymb = 1000          # Numero de simbolos
os    = 4
## Parametros de la respuesta en frecuencia
Nfreqs = 256          # Cantidad de frecuencias

## Parametros del filtro de caida cosenoidal
beta   = [0.0,0.5,0.99] # Roll-Off
Nbauds = 6    # Cantidad de baudios del filtro
## Parametros funcionales
Ts = T/os              # Frecuencia de muestreo


samples = 1533
frequency_sim = samples * os


seed   = [0, 1, 0, 1, 0, 1, 0, 1, 1]
seed_q = [0, 1, 1, 1, 1, 1, 1, 1, 1]
prbs_bits   = np.zeros(samples, dtype=int)
prbs_bits_q = np.zeros(samples, dtype=int)




def rcosine(beta, Tbaud, oversampling, Nbauds, Norm):
    """ Respuesta al impulso del pulso de caida cosenoidal """
    t_vect = np.arange(-0.5*Nbauds*Tbaud, 0.5*Nbauds*Tbaud, 
                       float(Tbaud)/oversampling)

    y_vect = []
    for t in t_vect:
        y_vect.append(np.sinc(t/Tbaud)*(np.cos(np.pi*beta*t/Tbaud)/
                                        (1-(4.0*beta*beta*t*t/
                                            (Tbaud*Tbaud)))))

    y_vect = np.array(y_vect)

    if(Norm):
        return (t_vect, y_vect/np.sqrt(np.sum(y_vect**2)))
        #return (t_vect, y_vect/y_vect.sum())
    else:
        return (t_vect,y_vect)

rcosine(beta[2], T, os, Nbauds, Norm=False)

def resp_freq(filt, Ts, Nfreqs):
    """Computo de la respuesta en frecuencia de cualquier filtro FIR"""
    H = [] # Lista de salida de la magnitud
    A = [] # Lista de salida de la fase
    filt_len = len(filt)

    #### Genero el vector de frecuencias
    freqs = np.matrix(np.linspace(0,1.0/(2.0*Ts),Nfreqs))
    #### Calculo cuantas muestras necesito para 20 ciclo de
    #### la mas baja frec diferente de cero
    Lseq = 20.0/(freqs[0,1]*Ts)

    #### Genero el vector tiempo
    t = np.matrix(np.arange(0,Lseq))*Ts

    #### Genero la matriz de 2pifTn
    Omega = 2.0j*np.pi*(t.transpose()*freqs)

    #### Valuacion de la exponencial compleja en todo el
    #### rango de frecuencias
    fin = np.exp(Omega)

    #### Suma de convolucion con cada una de las exponenciales complejas
    for i in range(0,np.size(fin,1)):
        fout = np.convolve(np.squeeze(np.array(fin[:,i].transpose())),filt)
        mfout = abs(fout[filt_len:len(fout)-filt_len])
        afout = np.angle(fout[filt_len:len(fout)-filt_len])
        H.append(mfout.sum()/len(mfout))
        A.append(afout.sum()/len(afout))

    return [H,A,list(np.squeeze(np.array(freqs)))]


(t,rc1) = rcosine(beta[1], T,os,Nbauds,Norm=False)

[H1,A1,F1] = resp_freq(rc1, Ts, Nfreqs)

### Generacion de los graficos
plt.figure(figsize=[14,6])
plt.semilogx(F1, 20*np.log10(H1),'g', linewidth=2.0, label=r'$\beta=0.5$')

plt.axvline(x=(1./Ts)/2.,color='k',linewidth=2.0)
plt.axvline(x=(1./T)/2.,color='k',linewidth=2.0)
plt.axhline(y=20*np.log10(0.5),color='k',linewidth=2.0)
plt.legend(loc=3)
plt.grid(True)
plt.xlim(F1[1],F1[len(F1)-1])
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.show()




print (rc1)



shift_reg_prbs   = np.zeros(6, dtype=int)
shift_reg_prbs_q = np.zeros(6, dtype=int)

phase_0 = np.zeros(Nbauds)
phase_1 = np.zeros(Nbauds)
phase_2 = np.zeros(Nbauds)
phase_3 = np.zeros(Nbauds)


for i in range(Nbauds):
    phase_0[i] = rc1[i*os + 0]
    phase_1[i] = rc1[i*os + 1]
    phase_2[i] = rc1[i*os + 2]
    phase_3[i] = rc1[i*os + 3]

phases = [phase_0, phase_1, phase_2, phase_3]

y_out   = np.zeros(frequency_sim)
y_out_q = np.zeros(frequency_sim)

offset_decision = 0   # fase de decision dentro del simbolo (0..os-1); igual para el ojo y la constelacion

def prbs_9():
    count_prbs = 0
    idx = 0
    for i in range(frequency_sim):
        fase = i % os
        y_out[i]   = np.dot(shift_reg_prbs,   phases[fase])
        y_out_q[i] = np.dot(shift_reg_prbs_q, phases[fase])
        count_prbs = count_prbs + 1

        if (count_prbs == os):
            count_prbs = 0

            # rama I
            bit = seed[8]
            prbs_bits[idx] = bit
            simbolo = 1 - 2*bit                    # BPSK: 0 -> +1, 1 -> -1
            for k in range(5, 0, -1):
                shift_reg_prbs[k] = shift_reg_prbs[k-1]
            shift_reg_prbs[0] = simbolo
            new_bit = seed[4] ^ seed[8]
            for j in range(8, 0, -1):
                seed[j] = seed[j-1]
            seed[0] = new_bit

            # rama Q (misma logica, semilla y shift register propios)
            bit_q = seed_q[8]
            prbs_bits_q[idx] = bit_q
            simbolo_q = 1 - 2*bit_q
            for k in range(5, 0, -1):
                shift_reg_prbs_q[k] = shift_reg_prbs_q[k-1]
            shift_reg_prbs_q[0] = simbolo_q
            new_bit_q = seed_q[4] ^ seed_q[8]
            for j in range(8, 0, -1):
                seed_q[j] = seed_q[j-1]
            seed_q[0] = new_bit_q

            

            idx = idx + 1


    plotting.plot_prbs_9(plt, prbs_bits)
    plotting.plot_filter_output(plt, y_out)
    plotting.eyediagram(plt, y_out[100:len(y_out)-100], os, offset_decision, 1)
    plotting.plot_constellation_iq(plt, y_out[100:len(y_out)-100], y_out_q[100:len(y_out_q)-100], os, offset_decision)


def calcular_ber(y_out, prbs_bits, os, offset_decision, label="I"):
    bits_rx = (y_out[offset_decision::os] < 0).astype(int)   # simbolo = 1-2*bit -> bit=0:+1, bit=1:-1

    n = min(len(bits_rx), len(prbs_bits))
    bits_rx = bits_rx[:n]
    bits_tx = prbs_bits[:n]

    tx_pm1 = 1 - 2*bits_tx
    rx_pm1 = 1 - 2*bits_rx
    corr = np.correlate(rx_pm1, tx_pm1, mode="full")
    delay = np.argmax(corr) - (n - 1)   # delay > 0: rx atrasado respecto a tx (caso tipico por el FIR)

    if delay >= 0:
        bits_tx_al = bits_tx[:n-delay]
        bits_rx_al = bits_rx[delay:delay+len(bits_tx_al)]
    else:
        bits_rx_al = bits_rx[:n+delay]
        bits_tx_al = bits_tx[-delay:-delay+len(bits_rx_al)]

    errores = int(np.sum(bits_rx_al != bits_tx_al))
    ber = errores / len(bits_tx_al)

    print(f"[{label}] delay detectado: {delay} simbolos | "
          f"errores: {errores}/{len(bits_tx_al)} | BER: {ber:.3e}")
    return ber, delay, errores


prbs_9()

calcular_ber(y_out,   prbs_bits,   os, offset_decision, label="I")
calcular_ber(y_out_q, prbs_bits_q, os, offset_decision, label="Q")


# Patron de test: 4 ceros de delay UNA sola vez al principio, y despues
# 512 corridas seguidas de 1 periodo completo del PRBS9 sin gaps (periodo
# real 511, igual que el generador local -> el delay que encuentra
# prbs_sync es estable en el tiempo, no se corre corrida a corrida).
ZEROS_DELAY = 4
PERIOD = 511                       # 2^9 - 1, periodo maximo del LFSR
N_RUNS = 512

prbs_period = prbs_bits[:PERIOD]   # un periodo completo arrancando en "seed"
test_pattern = np.concatenate([
    np.zeros(ZEROS_DELAY, dtype=int),
    np.tile(prbs_period, N_RUNS),
])                                  # 4 + 512*511 = 261636 bits

print(f"test_pattern: {len(test_pattern)} bits "
      f"({ZEROS_DELAY} ceros de delay inicial + {N_RUNS} corridas de {PERIOD} bits)")

# Un bit por linea, para leer con $readmemb en el testbench (1 bit por ciclo).
# Se guarda directo en el directorio de trabajo de xsim (ahi es donde
# $readmemb("test_pattern.mem", ...) lo va a buscar cuando corra la sim).
TEST_PATTERN_PATH = r"C:\Users\Esteban\OneDrive\Desktop\tps_vivado_procom\rcosine\rcosine.sim\sim_1\behav\xsim\test_pattern.mem"
np.savetxt(TEST_PATTERN_PATH, test_pattern, fmt="%d")
print(f"guardado: {TEST_PATTERN_PATH}")