import math
import numpy as np
import copy

class cluster:

    def __init__(self, k, beta):
        self.trajectories = []
        self.trajectoriesProb = []
        self.trajectoriesIndex = []
        self.variance = [''] * k
        self.mean = [''] * k
        self.k = k
        self.beta = beta

    def probabilityOfTrajInCluster(self, traj):
        LogProb = 0
        # beta =len(traj)/self.k
        for i in range(len(traj)):

            index = math.floor(i / self.beta)
            if index >= (self.k-1):
                index=self.k-1
            helper = np.array([traj['x'][i], traj['y'][i]])
            LogProb = LogProb + cluster.logValueOfGaussuan2D(self.mean[index], self.variance[index], helper)


        return LogProb

    @staticmethod
    def findLowestIndex(clusters):
        index = 0
        MinProb = 0
        for i, c in enumerate(clusters):
            l = len(c.trajectories)
            prob = 0
            if l == 0:
                return i
            for p in c.trajectoriesProb:
                prob = prob + p
            prob = prob / l
            if MinProb > prob:
                MinProb = prob
                index = i
        return index

    @staticmethod
    def findLEastLiklyTraj(clusters):
        index = 0
        MinProb = 0
        for c in clusters:
            for i, p in zip(c.trajectoriesIndex, c.trajectoriesProb):
                if p < MinProb:
                    MinProb = p
                    index = i
        return index



    @staticmethod
    def Expectation(d, trajectories):
        labels=[]
        clusters = copy.deepcopy(d)
        for c in clusters:
            c.trajectories = []
            c.trajectoriesProb = []
            c.trajectoriesIndex = []
        for j, traj in enumerate(trajectories):
            maxprob = 0
            index = 0
            for i, c in enumerate(clusters):
                if d[i].trajectoriesIndex == []:
                    continue
                prob = c.probabilityOfTrajInCluster(traj)
                if i == 0:
                    maxprob = prob
                    continue
                if maxprob < prob:
                    maxprob = prob
                    index = i
            clusters[index].trajectories.append(traj)
            clusters[index].trajectoriesProb.append(maxprob)
            clusters[index].trajectoriesIndex.append(j)
            labels.append(index)
        return clusters,labels
    @staticmethod
    def ExpectationOutliers(d, trajectories,labels):
        clusters = copy.deepcopy(d)

        for j, traj in enumerate(trajectories):
            maxprob = 0
            index = 0
            for i, c in enumerate(clusters):
                if labels!= -1:
                    continue
                prob = c.probabilityOfTrajInCluster(traj)
                if i == 0:
                    maxprob = prob
                    continue
                if maxprob < prob:
                    maxprob = prob
                    index = i
            clusters[index].trajectories.append(traj)
            clusters[index].trajectoriesProb.append(maxprob)
            clusters[index].trajectoriesIndex.append(j)
        return clusters

    def Maximization(self):
        for i in range(self.k):
            points = []
            for traj in self.trajectories:
                for b in range(self.beta * i, self.beta * (i + 1)):
                    points.append([traj.to_numpy()[b][0], traj.to_numpy()[b][1]])
            self.mean[i] = np.mean(points, axis=0)
            self.variance[i] = np.cov(np.array(points).transpose())

    @staticmethod
    def logValueOfGaussuan2D(mean, variance, value):
        # print(value)
        # print(mean)
        dif = value - mean
        # print(variance)
        return -np.log(2 * math.pi) - 0.5 * np.log(np.linalg.det(variance)) - 0.5 * np.matmul(
            np.matmul(dif.transpose(), np.linalg.inv(variance)), dif)

    @staticmethod
    def BIC(clusters):
        k= 0
        n=0
        logLiklyhood=0
        for c in clusters:
            k=k+c.k*6
            n=n+len(c.trajectories)*200
            for traj in c.trajectories:
                logLiklyhood=logLiklyhood+c.probabilityOfTrajInCluster(traj)
        n=np.log(n)
        return k*n-2*logLiklyhood

    @staticmethod
    def AIC(clusters):
        k= 0
        logLiklyhood=0
        for c in clusters:
            k=k+c.k*6
            for traj in c.trajectories:
                logLiklyhood=logLiklyhood+c.probabilityOfTrajInCluster(traj)
        return 2*k-2*logLiklyhood