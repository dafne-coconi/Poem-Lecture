from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from skimage import morphology
from PIL import Image
import win32com.client as wincl
plt.close('all')
#----------------------------------------------
def poslin(n):
    a = np.where(n<=0,0,n)
    return a
def purelin(n):
    a = 1*n
    return a

Ima1=io.imread('poema_times.bmp')
LETRAS=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q',
        'R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i',
        'j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z']

W1=np.load('W1_letras.npy')
W2=np.load('W2_letras.npy')
b1=np.load('b1_letras.npy')

[filas,columnas]=Ima1.shape
IMA_rev=np.zeros([filas,columnas])
IMA_rev[np.where(Ima1==0)]=1

sumafil=np.sum(IMA_rev,axis=1)

# RECORTE DE CADA FILA
fila_rec=[]
inicio = 1
for i in range(sumafil.shape[0]):
    if sumafil[i]!=0 and inicio==1:
        inicio=0
        val1=i
    elif sumafil[i]==0 and inicio==0:
        inicio=1
        val2=i
        fila_rec.append(np.array([val1-2,val2+2]))
        

for ii in range(len(fila_rec)):
    recorte=IMA_rev[fila_rec[ii][0]:fila_rec[ii][1],:] #recorta la fila
    sumacol=np.sum(recorte,axis=0)
   
    # RECORTE DE CADA LETRA
    letra_rec=[]
    inicio = 1
    MAX=0
    for i in range(sumacol.shape[0]):
        if sumacol[i]!=0 and inicio==1:
            inicio=0
            val1=i
        elif sumacol[i]==0 and inicio==0:
            inicio=1
            val2=i
            letra_rec.append(np.array([val1-1,val2+1]))

    Val_letras=[]            
    for i in range(len(letra_rec)):
        r1=recorte[:,letra_rec[i][0]:letra_rec[i][1]]
        #recorte letra fila
        sumafil_l=np.sum(r1,axis=1)
        inicio = 1
        for i in range(sumafil_l.shape[0]):
            if sumafil_l[i]!=0:
                val1=i-2
                break
        for i in range(sumafil_l.shape[0]-1,0,-1):
            if sumafil_l[i]!=0:
                val2=i+2
                break 
        r2=r1[val1:val2,:]
        r2=morphology.binary_closing(r2)
        r3=np.array(Image.fromarray(r2).resize((36,44)))
        Val_letras.append(np.reshape(r3,[1,36*44]))
    
    alpha=0.09

    linea=''
    for k in range(len(Val_letras)):
        a1 = purelin(np.dot(W1,Val_letras[k].T)+b1)
        norm = np.linalg.norm(a1)
        a20 = a1/norm
        #Parte recursiva
        for i in range(60):
            a2n = poslin(np.dot(W2,a20)) 
            a20=a2n
        norm = np.linalg.norm(a20)
        a20=a20/norm
        val_max=np.argmax(a1)
        A1=np.copy(a1)
        A1[val_max]=0
        val2_max=np.argmax(A1)
        if (abs(a1[val2_max]-a1[val_max])<6 and val_max==31) or(abs(a1[val2_max]-a1[val_max])<9 and val_max==1):
            val_max=val2_max
        if k<len(Val_letras)-1:
            if abs(letra_rec[k][1]-letra_rec[k+1][0])<10:        
                linea=linea+LETRAS[val_max]
            else:
                linea=linea+LETRAS[val_max]+' '
        else:
            linea=linea+LETRAS[val_max]

    print(linea)
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(linea)   
