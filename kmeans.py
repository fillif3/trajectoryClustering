import os
import numpy as np
from sklearn.cluster import DBSCAN,KMeans
import pandas as pd
import matplotlib.pyplot as plt

def dist(X,Y):
    l = int(len(X)/2)
    dist=0
    for i in range(l):
        dist=dist+((X[i]-Y[i])**2+(X[i+l]-Y[i+l])**2)**(0.5)
    #print(dist)
    return dist

def pdToTraj(df):
    traj=np.array([])
    for d in df['x']:
        traj=np.append(traj,d)
    for d in df['y']:
        traj=np.append(traj,d)
    return traj

def saveText(labels,num):
    text=''
    for l in labels:
        text = text+str(l)+' '
    text = text[0:-1]
    f = open("clusteringDivided/"+str(num)+".txt", "w")
    f.write(text)
    f.close()

def readLabels(dira):
    f = open(dira, "r")
    lin=f.read()
    lin=lin.split(' ')
    out=[]
    for l in lin:
        out.append(int(l))
    return out

def createColors(num):
    step = 14777215//num
    colors=[]
    for i in range(num):
        helper = i * step
        d= hex(helper)
        l = len(d)
        if l<8:
            d2= '0x'
            for i in range(8-l):
                d2=d2+'0'
            d = d2 + d[2::]

        colors.append('#'+d[2::])
    print(colors)
    return colors



''''''

def calculateAVariable(distances,labels):
    a=[]
    for i in range(len(labels)):
        label = labels[i]
        divided = 0
        dist=0
        for j in range(len(labels)):
            if i!=j and label==labels[j]:
                dist = dist + distances[i,j]
                divided=divided+1
        if divided==0:
            a.append(0)
        else:
            a.append(dist/divided)
    return a

def calculateBVariable(distances,a,labels):
    bMin=[]
    numberOfLabels = max(labels)+1
    for i in range(len(labels)):
        b=[]
        if a[i]==0:
            bMin.append(0)
            continue
        divided = 0
        dist=0
        for label in range(numberOfLabels):
            if label == labels[i]:
                continue
            for j in range(len(labels)):
                if label==labels[j]:
                    dist = dist + distances[i,j]
                    divided=divided+1
            if divided!=0:
                b.append(dist/divided)
        bMin.append(min(b))
    return bMin

def calculateSVariable(a, b):
    s=[]
    for i,j in zip(a,b):
        if i==0:
            s.append(0)
            continue
        s.append((j-i)/max(i,j))

    return s

def calculateSiletter(distances,labels):
    a=calculateAVariable(distances,labels)
    b=calculateBVariable(distances,a,labels)
    s = calculateSVariable(a,b)
    s=np.mean(s)
    return s

#for i in range(1432):
#    for j in range(1432):
#        if i==j:
#            continue
#        distances[i,j]=dist(trajectories[i],trajectories[j])

#np.savetxt('distances.csv', distances, delimiter=',')
#print(distances)
#input()


trajectories = np.empty([1432,200])


di=os.listdir('trajDiv')
di.sort()
for i,filename in enumerate(di):
    dira = "trajDiv/"+filename
    df = pd.read_csv(dira, header=0)
    # x=np.linspace(i,i+10000,10000)
    # y=np.linspace(0,i*0.01,10000)
    # vec = np.array([x,y]).transpose()
    #
    # df=pd.DataFrame(vec,columns=['x','y'])
    traj= pdToTraj(df)
    trajectories[i]=traj
    #plt.plot(trajectories[i][0:1000], trajectories[i][1000:2000])
    #plt.xlim(-7000, 15000)
    #plt.ylim(-7000, 15000)
    #plt.show()
distances = np.loadtxt('distances.csv', delimiter=',')
for value in range(2,200,1):

    #clustering=KMeans(n_clusters=value).fit(trajectories)
    #clustering=KMeans(n_clusters=value).fit(trajectories)

    #saveText(clustering.labels_,value)
    #print(max(clustering.labels_))
    labels = readLabels("clusteringDivided/" + str(value) + ".txt", )
    sil = calculateSiletter(distances,labels)
    print('For '+str(value)+' clusters we have a score equal to '+ str(sil))
    '''

    labels=clustering.labels_
    colors = createColors(5)#max(labels)+1)
    d = max(labels)+1
    print(len(labels))
    #print(d)
    for j in range(d):
        #plt.figure()
        #plt.get_current_fig_manager().full_screen_toggle()  # toggle fullscreen mode
        for i in range(1431):

            if labels[i]==-1:
                continue
            #print(colors)
            #print(labels[i])
            if labels[i]==j:
                #print(i)
                #print(len(trajectories))
                #print(len(trajectories[i]))
                #plt.plot(trajectories[i][0:1000],trajectories[i][1000:2000])
        if True:#j%0==0 or j==(d-1):
            plt.xlim(-7000, 15000)
            plt.ylim(-7000, 15000)
            plt.title(str(value)+"kmena")


            #plt.show()
    '''