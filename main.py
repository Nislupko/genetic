import json
from ownga import start_ga
from libga import start_lib_ga

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

"""Находим решение с помощью GA"""
res1 = start_lib_ga()
res2 = start_ga()

"""Приводим данные к виду, требуемому в тз"""
resultWeight = 0
resultVolume = 0
resultPrice = 0
resultSum = []

"""Запись в json и вывод"""
for i in range(len(res1[1])):
    if res1[1][i] > 0:
        resultWeight +=items[i][0]
        resultVolume += items[i][1]
        resultPrice += items[i][2]
        resultSum.append(i)
result1={'weight': resultWeight, 'volume': resultVolume, 'price': resultPrice, 'items': resultSum}

resultWeight = 0
resultVolume = 0
resultPrice = 0
resultSum = []

lst = list(res2.values())[0]
for i in range(len(lst)):
    if (lst[i] > 0):
        resultWeight +=items[i][0]
        resultVolume += items[i][1]
        resultPrice += items[i][2]
        resultSum.append(i)
result2={'weight': resultWeight, 'volume': resultVolume, 'price': resultPrice, 'items': resultSum}

json_file={1:result1,2:result2}
with open('results.json', 'w') as outfile:
    json.dump(json_file, outfile, indent=4, ensure_ascii=False)