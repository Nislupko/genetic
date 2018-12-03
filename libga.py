from pyeasyga import pyeasyga
import json
import ownga
def start_lib_ga():

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
                resultTotal['maxWeight']=int(item[0])
                resultTotal['maxVolume']=float(item[1])
                first = False
                continue

            elem = (int(item[0]), float(item[1]), int(item[2]))
            result.extend([elem])

        resultTotal['items'] = result
        return resultTotal


    """Получение и приведение данных к стандартизиированному в бибилиотеке виду"""
    data = get_data()
    bag = {'weight': data['maxWeight'], 'volume': data['maxVolume']}
    items = data['items']

    """Начальные условия"""
    ga = pyeasyga.GeneticAlgorithm(items)
    ga.population_size = 200

    """ Фитнес-фукнция определяет насколько жизнеспособна и эволюционно перспективна особь
        определяется прямой суммой стоимостей входящих в рюкзак вещей"""
    def fitness(individual, data):
        weight, volume, price = 0, 0, 0
        for (selected, item) in zip(individual, data):
            if selected:
                weight += item[0]
                volume += item[1]
                price += item[2]
        if weight > bag['weight'] or volume > bag['volume']:
            price = 0

        #print("W: " + str(weight) + "; V: " + str(volume) + "; P: " + str(price))
        return price

    """Запуск генетического алгоритма"""
    ga.fitness_function = fitness
    ga.run()

    return ga.best_individual()


#print (start_lib_ga())
