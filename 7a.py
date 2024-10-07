import random
from deap import base, creator, tools

creator.create("AptitudMax", base.Fitness, weights=(1.0,))
creator.create("Individuo", list, fitness=creator.AptitudMax)

def evaluar(individuo):
    x = individuo[0]
    return (x**2 + 2*x - 1,)

herramientas = base.Toolbox()
herramientas.register("x", random.randint, 1, 100)
herramientas.register("individuo", tools.initRepeat, creator.Individuo, herramientas.x, n=1)
herramientas.register("poblacion", tools.initRepeat, list, herramientas.individuo)
herramientas.register("evaluar", evaluar)
herramientas.register("cruzar", tools.cxBlend, alpha=0.5)
herramientas.register("mutar", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
herramientas.register("seleccionar", tools.selTournament, tournsize=3)

def main():
    poblacion = herramientas.poblacion(n=10)
    NGEN = 3
    for gen in range(NGEN):
        descendencia = herramientas.seleccionar(poblacion, len(poblacion))
        descendencia = list(map(herramientas.clone, descendencia))
        for hijo1, hijo2 in zip(descendencia[::2], descendencia[1::2]):
            if random.random() < 0.5:
                herramientas.cruzar(hijo1, hijo2)
                del hijo1.fitness.values
                del hijo2.fitness.values
        for mutante in descendencia:
            if random.random() < 0.2:
                herramientas.mutar(mutante)
                del mutante.fitness.values
        individuos_invalidos = [ind for ind in descendencia if not ind.fitness.valid]
        aptitudes = map(herramientas.evaluar, individuos_invalidos)
        for ind, fit in zip(individuos_invalidos, aptitudes):
            ind.fitness.values = fit
        poblacion[:] = descendencia

    aptitudes = [ind.fitness.values[0] for ind in poblacion]
    mejor_idx = aptitudes.index(max(aptitudes))
    print(f"Mejor individuo: {poblacion[mejor_idx]} con aptitud {aptitudes[mejor_idx]}")

if __name__ == "__main__":
    main()
