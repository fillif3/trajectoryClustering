import math
import pandas as pd
import os
from os import listdir
from os.path import isfile, join

def interpolate(traj, samples):
    l = len(traj) - 1
    move = l / samples
    data = []
    # print(l)
    for i in range(samples):
        # print(i)
        movement = i * move
        k = math.floor(movement)
        dif = movement - k
        data.append([traj['x'][k] + (traj['x'][k + 1] - traj['x'][k]) * dif,
                     traj['y'][k] + (traj['y'][k + 1] - traj['y'][k]) * dif])
    out = pd.DataFrame(data, columns=['x', 'y'])
    return out

k=os.getcwd()
onlyfiles = [f for f in listdir(k) if isfile(join(k, f))]
print(onlyfiles)
for i in range(1432):  # 947
    dira = "trajDiv/" + str(i) + ".csv"
    df = pd.read_csv(dira, header=0)
    # x=np.linspace(i,i+10000,10000)
    # y=np.linspace(0,i*0.01,10000)
    # vec = np.array([x,y]).transpose()
    #
    # df=pd.DataFrame(vec,columns=['x','y'])
    traj = interpolate(df,100)
    traj.to_csv('trajDiv2/'+str(i)+'.csv',index=False)