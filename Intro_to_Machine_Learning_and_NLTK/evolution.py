from random import choice, random, sample

def randomGenome(l, possible):
    return ''.join([choice(possible) for i in range(l)])

def fitness(goal):
    def fit(g):
        t = 0
        for i in range(len(g)):
            if g[i] == goal[i]:
                t += 1

        return t
    return fit

def crossoverAndMutation(g0, g1, possible, mutationChance):
    new = ''
    for i in range(len(g0)):
        if random() < mutationChance:
            new += choice(possible)
        else:
            if random() < 0.5:
                new += g0[i]
            else:
                new += g1[i]

    return new

target = 'my name is jeff'
possible = 'abcdefghijklmnopqrstuvwxyz0123456789 '

populationSize = 10

population = []
for g in range(populationSize):
    population.append(randomGenome(len(target), possible))

fitFunc = fitness(target)

while target not in population:
    population.sort(key=fitFunc, reverse=True)

    print(population[0], fitFunc(population[0]))

    population = population[:len(population) // 2]

    while len(population) < populationSize:
        g0, g1 = sample(population, 2)

        population.append(crossoverAndMutation(g0, g1, possible, 0.05))

print(target)
