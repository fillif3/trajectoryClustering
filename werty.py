import cluster as cl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def saveText(labels,num):
    text=''
    for l in labels:
        text = text+str(l)+' '
    text = text[0:-1]
    f = open("clusteringEM/"+str(num)+".txt", "w")
    f.write(text)
    f.close()


def containsTraj(arr, v):
    for a in arr:
        if v['x'][3] == a['x'][3] and v['y'][3] == a['y'][3]:
            return True
    return False

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


def readLabels(dira):
    f = open(dira, "r")
    lin=f.read()
    lin=lin.split(' ')
    out=[]
    for l in lin:
        out.append(int(l))
    return out

def plotClusters(clusters):
    colors = createColors(len(clusters))
    for i, c in enumerate(clusters):
        for traj in c.trajectories:
            plt.plot(traj['x'], traj['y'], colors[i])
    plt.show()

def createColors(num):
    step = 16777215//num
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
    #print(colors)
    return colors
'''
trajectories = np.empty([947,2000])


for i in range(947):  # 947
    dira = "trajectories2/" + str(i) + ".csv"
    df = pd.read_csv(dira, header=0)
    traj= pdToTraj(df)
    trajectories[i]=traj
'''
dft = pd.DataFrame([],columns = ['number of cluster','k','BIC'])


trajectories=[]
for i in range(1431):  # 947
    dira = "trajDiv/" + str(i) + ".csv"
    df = pd.read_csv(dira, header=0)
    trajectories.append(df)



for value in range(12,200,1):
    labels=readLabels("clusteringDivided/"+str(value)+".txt",)
    numberOfClusters = max(labels)+1
    colors = createColors(numberOfClusters)
    for k in range(3,4):
        #if value == 500000 and k<3:
        #    continue
        clusters=[]
        for i in range(numberOfClusters):
            c = cl.cluster(k, int(100/k))
            clusters.append(c)

        for i in range(1431):  # 947
            if labels[i] == -1:
                continue
            clusters[labels[i]].trajectories.append(trajectories[i])
            clusters[labels[i]].trajectoriesIndex.append(i)
        #plotClusters(clusters)
        i=0
        oldvec = []
        vec = []
        for j, traj in enumerate(trajectories):

            for i in range(value):
                if containsTraj(clusters[i].trajectories, traj):
                    vec.append(i)
        d=6
        while True:
            i = i + 1
            # print(i)
            if d<5:
                #plotClusters(clusters)
                break
            else:

                for c in clusters:
                    c.Maximization()

            clusters,labels = cl.cluster.Expectation(clusters, trajectories)
            oldvec = vec
            vec = []
            for j, traj in enumerate(trajectories):

                for i in range(value):
                    if containsTraj(clusters[i].trajectories, traj):
                        vec.append(i)
            d = 0
            for o, v in zip(oldvec, vec):
                if o != v:
                    d = d + 1
            print(d)
        #clusters = cl.cluster.ExpectationOutliers(clusters, trajectories,labels)
        #for c in clusters:
        #    c.Maximization()
        #a = cl.cluster.AIC(clusters)
        #b = cl.cluster.BIC(clusters)
        #df2 = pd.DataFrame([[numberOfClusters,k,b]], columns=['number of cluster', 'k', 'BIC'])

        #dft=dft.append(df2,ignore_index=True)
        #dft.to_csv('final103.csv', index=False)

        saveText(labels,value)