from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import morphology
from os import system

system("cls")
plt.close('all')
#----------------------------------------------
def poslin(n):
    a = np.where(n<=0,0,n)
    return a
def purelin(n):
    a = 1*n
    return a
Ima1=io.imread('letras_times.bmp')

[filas,columnas]=Ima1.shape
IMA_rev=np.zeros([filas,columnas])
IMA_rev[np.where(Ima1==0)]=1 #Se invierte la imagen

#SUMA DE FILAS
sumafil=np.sum(IMA_rev,axis=1)
plt.figure(1)
plt.plot(sumafil)

recorte=IMA_rev[15:72,:] #recorta la fila

#SUMA DE COLUMNAS
sumacol=np.sum(recorte,axis=0)
plt.figure(2)
plt.plot(sumacol)

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
        
c=-1
Val_letras=[]            
for i in range(54):
    c+=1
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

# SE INICIALIZAN PESOS
W1=np.random.rand(54,36*44)*0.01+0.5
b1=np.ones([54,1])*0.5

W2=np.random.rand(54,54)*0.01+0.5
alpha=0.006

# SE REALIZA EL APRENDIZAJE
for epocas in range(100):
    for k in range(54):
        a1 = purelin(np.dot(W1,Val_letras[k].T)+b1)
        a20 = a1/max(a1)
        norm = a1/max(a1)
        #Parte recursiva
        for i in range(60):
            a2n = poslin(np.dot(W2,a20)) 
            a20=a2n
        j=np.argmax(abs(a20))
        a20=a20/max(a20)
        W1[k,:] = W1[k,:]+alpha*(a20[k]*(Val_letras[k]-W1[k,:]))
    
np.save("W1_letras",W1)
np.save("W2_letras",W2)
np.save("b1_letras",b1)
