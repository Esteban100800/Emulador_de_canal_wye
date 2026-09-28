import numpy as np
import matplotlib.pyplot as plt

def plot_rcosine(plt,t,rc0_fixed_f,rc1_fixed_f,rc2_fixed_f, NB, NBF, mode):
    ### Generacion de las graficas
    plt.figure(figsize=[14,7])
    plt.title( "S" + "(" + str(NB) + "," + str(NBF) + ") " + mode)
    plt.plot(t,rc0_fixed_f,'ro-',linewidth=2.0,label=r'$\beta=0.0$')
    plt.plot(t,rc1_fixed_f,'gs-',linewidth=2.0,label=r'$\beta=0.5$')
    plt.plot(t,rc2_fixed_f,'k^-',linewidth=2.0,label=r'$\beta=1.0$')
    plt.legend()
    plt.grid(True)
    #plt.xlim(0,len(rc0)-1)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')


def plot_concolution(plt, rc0_fixed_f, rc1_fixed_f, rc2_fixed_f, symb00, rc0Symb00, rc1Symb00, rc2Symb00, os, NB, NBF, offsetPot, mode):

    plt.figure(figsize=[14,7])
    plt.title ("convolucion de " + "S" + "(" + str(NB) + "," + str(NBF) + ") " + mode + " con un pulso de 3 bits")
    plt.subplot(3,1,1)
    plt.plot(np.arange(0,len(rc0_fixed_f)),rc0_fixed_f,'r.-',linewidth=2.0,label=r'$\beta=0.0$')
    plt.plot(np.arange(os,len(rc0_fixed_f)+os),rc0_fixed_f,'k.-',linewidth=2.0,label=r'$\beta=0.0$')
    plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits')
    plt.plot(rc0Symb00[os::],'--',linewidth=3.0,label='Convolution')
    plt.legend()
    plt.grid(True)
    #plt.xlim(0,35)
    plt.ylim(-0.2,1.4)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')

    #plt.figure()
    plt.subplot(3,1,2)
    plt.plot(np.arange(0,len(rc1_fixed_f)),rc1_fixed_f,'r.-',linewidth=2.0,label=r'$\beta=0.5$')
    plt.plot(np.arange(os,len(rc1_fixed_f)+os),rc1_fixed_f,'k.-',linewidth=2.0,label=r'$\beta=0.5$')
    plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits')
    plt.plot(rc1Symb00[os::],'--',linewidth=3.0,label='Convolution')
    plt.legend()
    plt.grid(True)
    #plt.xlim(0,35)
    plt.ylim(-0.2,1.4)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    #plt.title('Rcosine - OS: %d'%int(os))

    #plt.figure()
    plt.subplot(3,1,3)
    plt.plot(np.arange(0,len(rc2_fixed_f)),rc2_fixed_f,'r.-',linewidth=2.0,label=r'$\beta=1.0$')
    plt.plot(np.arange(os,len(rc2_fixed_f)+os),rc2_fixed_f,'k.-',linewidth=2.0,label=r'$\beta=1.0$')
    plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits')
    plt.plot(rc2Symb00[os::],'--',linewidth=3.0,label='Convolution')
    plt.legend()
    plt.grid(True)
    #plt.xlim(0,35)
    plt.ylim(-0.2,1.4)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    #plt.title('Rcosine - OS: %d'%int(os))
    plt.show()


def plot_freq_resp(plt, H0, F0, H1, F1, H2, F2, Ts, T, NB, NBF, mode):
    
    ### Generacion de los graficos
    plt.figure(figsize=[14,6])
    plt.title( "respuesta en frecuencia"+"S" + "(" + str(NB) + "," + str(NBF) + ") " + mode)
    plt.semilogx(F0, 20*np.log10(H0),'r', linewidth=2.0, label=r'$\beta=0.0$')
    plt.semilogx(F1, 20*np.log10(H1),'g', linewidth=2.0, label=r'$\beta=0.5$')
    plt.semilogx(F2, 20*np.log10(H2),'k', linewidth=2.0, label=r'$\beta=1.0$')
    
    plt.axvline(x=(1./Ts)/2.,color='k',linewidth=2.0)
    plt.axvline(x=(1./T)/2.,color='k',linewidth=2.0)
    plt.axhline(y=20*np.log10(0.5),color='k',linewidth=2.0)
    plt.legend(loc=3)
    plt.grid(True)
    plt.xlim(F2[1],F2[len(F2)-1])
    plt.xlabel('Frequencia [Hz]')
    plt.ylabel('Magnitud [dB]')
    plt.show()



def plot_symbols(symb_out0I, symb_out0Q, symb_out1I, symb_out1Q, symb_out2I, symb_out2Q, os, offset, NB, NBF, mode):

    plt.figure(figsize=[15,5])
    plt.title ("constelacion de " + "S" + "(" + str(NB) + "," + str(NBF) + ") " + mode)

    plt.subplot(1, 3, 1)
    plt.plot(symb_out0I[100+offset:len(symb_out0I)-(100-offset):int(os)],
             symb_out0Q[100+offset:len(symb_out0Q)-(100-offset):int(os)],
                 '.',linewidth=2.0)
    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    plt.grid(True)
    plt.xlabel('Real')
    plt.ylabel('Imag')
    plt.title(r'$\beta=0.0$')

    plt.subplot(1, 3, 2)
    plt.plot(symb_out1I[100+offset:len(symb_out1I)-(100-offset):int(os)],
             symb_out1Q[100+offset:len(symb_out1Q)-(100-offset):int(os)],
                 '.',linewidth=2.0)
    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    plt.grid(True)
    plt.xlabel('Real')
    plt.ylabel('Imag')
    plt.title(r'$\beta=0.5$')

    plt.subplot(1, 3, 3)
    plt.plot(symb_out2I[100+offset:len(symb_out2I)-(100-offset):int(os)],
             symb_out2Q[100+offset:len(symb_out2Q)-(100-offset):int(os)],
                 '.',linewidth=2.0)
    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    plt.grid(True)
    plt.xlabel('Real')
    plt.ylabel('Imag')
    plt.title(r'$\beta=0.99$')

    plt.tight_layout()

    plt.show()



def plot_prbs_outputs(plt, output_1, output_2, title="PRBS9"):

    plt.figure(figsize=[14,7])
    plt.suptitle(title)

    plt.subplot(2,1,1)
    plt.step(np.arange(len(output_1)), output_1, 'r-', where='post', linewidth=1.5, label='output_1')
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Bit')
    plt.ylim(-0.2, 1.2)

    plt.subplot(2,1,2)
    plt.step(np.arange(len(output_2)), output_2, 'g-', where='post', linewidth=1.5, label='output_2')
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Bit')
    plt.ylim(-0.2, 1.2)

    plt.tight_layout()
    plt.show()


def plot_bpsk_outputs(plt, bpsk_1, bpsk_2, title="BPSK"):

    plt.figure(figsize=[14,7])
    plt.suptitle(title)

    plt.subplot(2,1,1)
    plt.step(np.arange(len(bpsk_1)), bpsk_1, 'r-', where='post', linewidth=1.5, label='bpsk_1')
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.ylim(-1.5, 1.5)

    plt.subplot(2,1,2)
    plt.step(np.arange(len(bpsk_2)), bpsk_2, 'g-', where='post', linewidth=1.5, label='bpsk_2')
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.ylim(-1.5, 1.5)

    plt.tight_layout()
    plt.show()


def plot_correlation(plt, correlation_matrix, delay=None, title="Correlacion"):

    plt.figure(figsize=[14,7])
    plt.title(title)
    plt.plot(np.arange(len(correlation_matrix)), correlation_matrix, 'b-', linewidth=1.5, label='correlacion')

    if delay is not None:
        plt.axvline(x=delay, color='r', linestyle='--', linewidth=1.5, label='delay=%d' % delay)

    plt.grid(True)
    plt.legend()
    plt.xlabel('Desfase (muestras)')
    plt.ylabel('Correlacion')
    plt.show()


def plot_resolution(plt, resolution, title="Resolucion de punto fijo"):

    fracs = np.arange(1, len(resolution))

    plt.figure(figsize=[10,6])
    plt.title(title)
    plt.plot(fracs, resolution[1:], 'bo-', linewidth=2.0, label='SQNR estimado')
    plt.grid(True)
    plt.legend()
    plt.xlabel('Bits de fraccion (NBF)')
    plt.ylabel('SQNR [dB]')
    plt.xticks(fracs)
    plt.show()


def plot_resolution_compare(plt, resolution_trunc, resolution_round, title="Resolucion de punto fijo"):

    fracs = np.arange(1, len(resolution_trunc))

    plt.figure(figsize=[10,6])
    plt.title(title)
    plt.plot(fracs, resolution_trunc[1:], 'bo-', linewidth=2.0, label='Truncado')
    plt.plot(fracs, resolution_round[1:], 'rs-', linewidth=2.0, label='Redondeado')
    plt.grid(True)
    plt.legend()
    plt.xlabel('Bits de fraccion (NBF)')
    plt.ylabel('SQNR [dB]')
    plt.xticks(fracs)
    plt.show()


def plot_pulse_train (plt, symb_out0I, symb_out0Q, symb_out1I, symb_out1Q, symb_out2I, symb_out2Q, os, NB, NBF, beta, mode):

    plt.figure(figsize=[10,6])
    plt.title ("trenes de pulsos de " + "S" + "(" + str(NB) + "," + str(NBF) + ") " + mode)
    plt.subplot(2,1,1)
    plt.plot(symb_out0I,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])
    plt.plot(symb_out1I,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
    plt.plot(symb_out2I,'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
    plt.xlim(1000,1250)
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')

    plt.subplot(2,1,2)
    plt.plot(symb_out0Q,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])
    plt.plot(symb_out1Q,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
    plt.plot(symb_out2Q,'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
    plt.xlim(1000,1250)
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')

def plot_prbs_9(plt, prbs_bits):
    plt.figure()
    plt.step(range(len(prbs_bits)), prbs_bits, where='post')
    plt.xlabel('muestra')
    plt.ylabel('bit')
    plt.title('PRBS9 bits')
    plt.grid(True)
    plt.show()

def plot_filter_output(plt, y_out, title='Salida del filtro polifasico'):
    plt.figure(figsize=[14,5])
    plt.plot(y_out, linewidth=1.0)
    plt.xlabel('muestra (ciclo rapido)')
    plt.ylabel('y_out')
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_constellation_iq(plt, i_data, q_data, os, offset, title='Constelacion I/Q'):
    puntos_i = i_data[offset::os]
    puntos_q = q_data[offset::os]
    plt.figure(figsize=[6,6])
    plt.plot(puntos_i, puntos_q, '.', markersize=4)
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    plt.grid(True)
    plt.xlabel('I')
    plt.ylabel('Q')
    plt.title(title)
    plt.show()

def plot_constellation(plt, y_out, os, offset, title='Constelacion'):
    puntos = y_out[offset::os]
    plt.figure(figsize=[6,6])
    plt.plot(puntos, np.zeros_like(puntos), '.', markersize=4)
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1, 1)
    plt.grid(True)
    plt.xlabel('Real')
    plt.title(title)
    plt.show()

def eyediagram(plt, data, n, offset, period, ax=None):
    span     = 2*n
    segments = int(len(data)/span)
    xmax     = (n-1)*period
    xmin     = -(n-1)*period
    x        = list(np.arange(-n,n,)*period)
    xoff     = offset

    standalone = ax is None
    if standalone:
        ax = plt.subplots()[1]

    for i in range(0,segments-1):
        ax.plot(x, data[(i*span+xoff):((i+1)*span+xoff)],'b')
    ax.grid(True)
    ax.set_xlim(xmin, xmax)

    if standalone:
        plt.show()
    plt.grid(True)
    plt.show()