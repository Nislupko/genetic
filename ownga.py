from random import random, randint


def start_ga():
    def get_data(path: str = 'data.txt'):
        """Чтение из файла и построчная запись в lines"""
        f = open(path)
        lines = [line.strip() for line in f]
        f.close()
        """Создание пустого словаря и переменной-итератора"""
        resultTotal = {}
        result = []
        first = True
        """Запись в словарь всех данных"""
        for i in lines:
            item = i.split(' ', -1)
            if (first):
                resultTotal['maxWeight'] = int(item[0])
                resultTotal['maxVolume'] = float(item[1])
                first = False
                continue

            elem = (int(item[0]), float(item[1]), int(item[2]))
            result.extend([elem])

        resultTotal['items'] = result
        return resultTotal

    def fitness(individual, data):
        weight, volume, price = 0, 0, 0
        for (selected, item) in zip(individual, data):
            if selected:
                weight += item[0]
                volume += item[1]
                price += item[2]
        if weight > bag['weight'] or volume > bag['volume']:
            price = 0

        return price

    # random
    def create_individual(data):
        return [randint(0, 1) for i in range(len(data))]

    # every bit from random parent
    def crossover(parent_1, parent_2):
        child_1 = list.copy(parent_1)
        child_2 = list.copy(parent_1)

        for i in range(len(parent_1)):
            r1 = randint(0, 1)
            r2 = randint(0, 1)
            if r1 > 0:
                child_1[i] = parent_2[i]
            if r2 > 0:
                child_2[i] = parent_2[i]

        return child_1, child_2

    # +1 random item to 10% of population
    def mutate(individual):
        countZeroes = 0
        for i in range(len(individual)):
            if individual[i] == 0:
                countZeroes += 1
        countZeroes = int(countZeroes * random())
        cur = 0
        for i in range(len(individual)):
            if individual[i] == 0:
                if cur == countZeroes:
                    individual[i] = 1
                    return individual
                else:
                    cur += 1
        return individual

    def populationCost(population):
        accum = 0
        for elem in population:
            accum += list(elem)[0]
        return accum

    def sortList(x):
        return list(x)[0]

    """Получение и приведение данных к стандартизиированному в бибилиотеке виду"""
    allData = get_data()
    bag = {'weight': allData['maxWeight'], 'volume': allData['maxVolume']}
    data = allData['items']

    def ga(population_size=200,
           generations_num=500,
           old_generation_penalty=0.8,
           mutation_probability=0.1):
        """
        Функция реализует генетический алгоритм для решения задачи об упаковки многомерного рюкзака
        Размер популяции = 200, Максимальное количество поколений = 500,
        Вероятность скрещивания определяется пропорционально значению фитнесс-функции(рулетка)
        Штраф  старому поколению х0.8, Вероятность мутации 0.1
        """
        counter = 0  # счетчик считает, сколько раз подряд родилось слабоэволюционировавших поколений
        """Первое поколение"""
        firstPopulation = []
        for i in range(population_size):
            firstPopulation.append(create_individual(data))
        population = [{fitness(firstPopulation[i], data): firstPopulation[i]} for i in range(population_size)]
        population.sort(key=sortList)
        best = population

        # Полный цикл одного поколения
        for gen in range(generations_num):

            # выбор особей для скрещивания
            maxChance = list(population[-1])[0]
            forCrossover = [0 for i in population]
            for index in range(len(population)):
                chance = list(population[index])[0] / maxChance
                if (random() < chance): forCrossover[index] = 1

            # получение новых особей
            first_parent = []
            childs = []
            for index in range(len(forCrossover)):
                if forCrossover[index] > 0:
                    if len(first_parent) == 0:
                        first_parent = population[index]
                    else:
                        second_parent = population[index]
                        x = crossover(list(first_parent.values())[0], list(second_parent.values())[0])
                        childs.append(x[0])
                        childs.append(x[1])
                        # print(first_parent,second_parent,crossover(list(first_parent.values())[0],list(second_parent.values())[0]))
                        # print(fitness(list(first_parent.values())[0],data),list(first_parent.values())[0])
                        # print(fitness(list(second_parent.values())[0],data),list(second_parent.values())[0])

                        # print(fitness(x[0],data),x[0])
                        # print(fitness(x[1], data), x[1])
                        first_parent = []
                        second_parent = []
            # мутация для детей
            # for child in childs:
            #      if random()< mutation_probability: child=mutate(child)
            # мутация для предков
            postMutation = []
            for elem in population:
                if random() < mutation_probability:
                    mutElem = mutate(list(elem.values())[0])
                    mutElem = {fitness(mutElem, data): mutElem}
                    postMutation.append(mutElem)
                else:
                    postMutation.append(elem)
            population = postMutation
            # новая популяция
            childs = [{fitness(childs[i], data): childs[i]} for i in range(len(childs))]
            newPopulation = []
            for elem in population:
                newPopulation.append({int(list(elem)[0] * old_generation_penalty): list(elem.values())[0]})
            newPopulation.extend(childs)
            newPopulation.sort(key=sortList)
            population = newPopulation[-population_size:]

            # условие досрочного выхода: 5 раз подряд был получен текущий или худший результат
            if list(best[-1])[0] < list(population[-1])[0]:
                best = population
                counter = 0
            else:
                if counter > 10:
                    return best
                else:
                    counter += 1

    return ga()[-1]


#print(start_ga())
