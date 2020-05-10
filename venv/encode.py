from PIL import  Image
import numpy as np
from numpy import *
im = (Image.open('enc.jpg').convert('LA'))
val = input("Enter Blocksize: ")
blocksize=int(val)
datatype = input("Enter datatype: ")
if(datatype=="float16"):
    datatype=float16
elif(datatype=="float32"):
    datatype = float32
elif(datatype=="float64"):
    datatype = float64
im=array(im,dtype=datatype)
n=im.shape[0]
m=im.shape[1]
flattenImage=im.flatten()
freqDict={}
prob = {}
npprob=[]
for j in range(256):
    freqDict[j]=0

for j in range(len(flattenImage)):
    freqDict[flattenImage[j]]+=1
    prob[flattenImage[j]]=0.0
finalimage=[]
sympols=[]
def probability():
    for item in range(len(freqDict)):
         probab= round((freqDict[item] /len(flattenImage)),16)
         if(probab != 0.0):
             sympols.append(item)
             prob[item]=probab
             npprob.append(probab)
probability()
c=len(flattenImage)
while (c%blocksize!=0):
        flattenImage.append(0)
        c+=1
symbolRange={}
def setrange(last,high):
    rng=high-last
    for i in range(len(sympols)):
        symbolRange[sympols[i]]=[last,last+((prob[sympols[i]])*rng)]
        last+=prob[sympols[i]]

setrange(0,1)
low=0
high=1
def encode(blocksize,start):
    lowhigh=0
    ranges=0
    high=1
    low=0
    for i in range(start,start+blocksize):
        lowhigh=symbolRange[flattenImage[i]]
        ranges=high-low
        high=low+ranges*lowhigh[1]
        low=low+ranges*lowhigh[0]

    return low
npfarray=[]
for i in range(0,len(flattenImage),blocksize):
    npfarray.append(encode(blocksize,i))

encoded=array((npfarray))
savetxt('nparray.csv', encoded, delimiter=',')
npprob=array(npprob)
savetxt('npprob.csv', npprob, delimiter=',')

'''''''n*m - encoded -blocksize-uniquesympols(0-255)-prob'''''''

def decode(blocksize,encodenum):
    retarr=[]
    low=0
    high=1
    ranges=high-low
    for i in range(blocksize):
        t=round((encodenum-low)/ranges,16)
        setrange(low,high)
        for j in range(len(sympols)):
            lowhigh=symbolRange[sympols[j]]
            if(t>=lowhigh[0] and t<lowhigh[1]):
                low=lowhigh[0]
                high=lowhigh[1]
                retarr.append(sympols[j])
                break

    return retarr
decodedimg=[]


for i in range(len(encoded)):

    res=decode(blocksize,encoded[i])
    print(res)
    for k in range((blocksize-1)):
        decodedimg.append(res[k])


image=np.reshape(decodedimg,(n,m))
img = Image.fromarray(image).convert('LA')
img.save("decode.png")
