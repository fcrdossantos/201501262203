from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# Data to plot.
w = 4.0
s = 35.0

pict_w = 500
pict_h = 500

world_x = 54.0
world_y = 54.0

xa, ya = np.meshgrid(np.linspace(0.0, world_x, num=pict_w), np.linspace(0.0, world_y, num=pict_h))
#x = np.linspace(0.0, 4.0, num=150)
#y = np.linspace(0.0, 4.0, num=150)
#za = np.power(np.sin(w * xa),2) * np.power(np.sin(w * ya),2) * np.exp((xa+ya)/s)
za = np.power(np.sin(w * xa),2) * np.power(np.sin(w * ya),2) * np.exp((xa+ya)/s)

population = np.random.rand(100,2) * 4.0

print(population)

plt.contourf(xa,ya,za)

def getfitness(x,y):
    return np.power(np.sin(w * x),2) * np.power(np.sin(w * y),2) * np.exp((x+y)/s)


def bin2int(cromossomo):
    num = 0
    for p,gene in enumerate(reversed(cromossomo)):
        num += (gene*2**p)
    return num    

def getvalue(cromossomo):
    k=8
    inf=0.0
    sup=world_x
    rx = bin2int(cromossomo[:k])
    ry = bin2int(cromossomo[k:])
    x= inf + ( (sup - inf)/(2**k - 1) ) * rx
    y= inf + ( (sup - inf)/(2**k - 1) ) * ry
    return x,y

def generate_individuo():
    k=16
    prob = np.random.rand(k)
    cromossomo = []
    for ip in prob:
        if ip < 0.5:
            cromossomo.append(0)
        else:
            cromossomo.append(1)
    return cromossomo

class CPopulation:
    def __init__(self):
        self.population = []
        self.fitness = []
        self.sum = 0
        self.roleta = []
        self.generation = 0
    def gen_roleta(self):    
        self.roleta = []
        fitness_acc = 0
        for i in range(len(self.population)):
            fitness = self.fitness[i]
            fitness_acc += fitness
            individuo = self.population[i]
            self.roleta.append((i,individuo,fitness_acc))
    def seleciona(self):
        position = np.random.rand() * self.sum
        for i,ind,acc in self.roleta:
            if acc >= position:
                return ind
    def generate(self, size):
        self.population = []
        self.fitness = []
        for i in range(size):
            individuo = generate_individuo()
            self.population.append(individuo)
            xp,yp = getvalue(individuo)
            self.fitness.append(getfitness(xp,yp))
        self.sum = np.sum(self.fitness)
    def crossover(self,ind1,ind2):
        k = len(ind1)
        p = np.random.randint(k)
        new1 = ind1[:p] + ind2[p:]
        mutate = np.random.randint(100)
        if mutate < 2:
            gene = np.random.randint(16)
            if new1[gene] == 1:
                new1[gene] = 0
            else:
                new1[gene] = 1

        new2 = ind2[:p] + ind1[p:]
        mutate = np.random.randint(100)
        if mutate < 2:
            gene = np.random.randint(16)
            if new2[gene] == 1:
                new2[gene] = 0
            else:
                new2[gene] = 1
        return new1,new2
    def evolve(self,size):
        offspring = []
        offspring_fit = []
        #criando a roleta
        self.gen_roleta()
        for i in range(int(size/2)):
            individuo_1 = self.seleciona()
            individuo_2 = self.seleciona()
            
            offspring1, offspring2 = self.crossover(individuo_1,individuo_2)
            #offspring1 = individuo_1
            #offspring2 = individuo_2
            
            #first 
            offspring.append(offspring1)
            xp,yp = getvalue(offspring1)
            offspring_fit.append(getfitness(xp,yp))
            #second
            offspring.append(offspring2)
            xp,yp = getvalue(offspring2)
            offspring_fit.append(getfitness(xp,yp))            
        
        self.generation += 1        
        self.population = offspring 
        self.fitness = offspring_fit     
        self.sum = np.sum(self.fitness) 
    def plot(self,color="red"):
        print("#%d  population len: %d"%(self.generation,len(self.population)))
        #print '    sum: ',self.sum
        print('    best: %f'%max(self.fitness))
        print('    worst: %f'%min(self.fitness))
        for individuo in self.population:
            xp,yp = getvalue(individuo)
            plt.plot(xp,yp, marker='o', markersize=3, color=color)

pop0 = CPopulation()
pop0.generate(100)
pop0.plot("red")
pop0.evolve(100)
pop0.plot("green")

for i in range(100):
    pop0.evolve(100)

pop0.plot("black")


fig = plt.figure()
ax = fig.gca(projection='3d')
#ax.contour3D(x,y,z)
ax.plot_surface(xa,ya,za)


plt.show()