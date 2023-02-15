from dot import Dot, sum_dots
from math import sqrt, pow, exp
import sys

def targetFunction(dot: Dot) -> float:
    '''
    Функция 13 варианта
    '''
    return round(pow(dot.coord_x, 2) + exp(pow(dot.coord_x, 2) + pow(dot.coord_y, 2)) + (4 * dot.coord_x) + (3 * dot.coord_y), 3)


def guidedFunction(dot: Dot) -> float:
    return round(pow(dot.coord_x, 2) - (dot.coord_x * dot.coord_y) + (3 * pow(dot.coord_y, 2)) - dot.coord_x, 3)


class Simplex:
    '''
    Класс для минимизации функции сипмлексным методом

    n : Размерность функции
    m : Длина ребра
    epsilon : Точность симплексного метода
    targetFunction : Минимизируемая функция
    '''

    result_matrix: list
    dots         : dict = {}

    startingDot  : Dot

    n            : int
    
    m            : float
    epsilon      : float

    def __init__(self, n: int, start_dot: Dot, m: float, epsilon: float, targetFunction) -> None:
        # Инициализация
        self.          n = n
        self.          m = m
        self.    epsilon = epsilon
        self.startingDot = start_dot
        self.targetFunc  = targetFunction

        # Добавление первой точки в список
        self.dots[self.targetFunc(self.startingDot)] = self.startingDot

        isDone = False

        # Шаг 2
        print("\nТочки в списке после первоначального заполнения:")
        self.generateDotsInitial()
        for res in self.dots:
            print(str(res) + "\t: ", str(self.dots[res]))

        iters = 0

        while not isDone:
            iters += 1
            # Шаг 3
            print("\nИсключаемая точка:")
            exclusion = self.findResultToExclude()
            print(str(exclusion[0]) + "\t:", str(exclusion[1]))

            # Шаг 4
            print("\nПервый центр тяжести:")
            cut_wc = self.findCutWeightCenter(exclusion[1])
            print(str(cut_wc))

            # Шаг 5
            print("\nОтраженная точка и результат функции в ней:")
            reflection = self.reflectDotAndResult(cut_wc, exclusion[1])
            print(str(reflection[0]) + "\t:", str(reflection[1]))

            # Шаг 6
            print("\nТочки в списке после проверки и замены отраженной точки:")
            self.checkAndSwap(exclusion, reflection)
            for result, dot in self.dots.items():
                print(str(result) + "\t:", str(dot))

            # Шаг 7
            print("\nОбщий центр тяжести:")
            wc = self.findFullWeightCenter()
            print(str(self.findFullWeightCenter()))

            # Шаг 8
            print("\nРезультат проверки на остановку:")
            isDone = self.checkStopCriteria(wc)
            print("Критерий останова: " + str(isDone))

        print("Всего итераций: ", iters)

    
    def generateDotsInitial(self):
        '''
        Создание начальных точек
        '''
        newDot_1 = self.startingDot + Dot(round(self.calcDelta1(), 3), round(self.calcDelta2(), 3))
        newDot_2 = self.startingDot + Dot(round(self.calcDelta2(), 3), round(self.calcDelta1(), 3))

        self.dots[self.targetFunc(newDot_1)] = newDot_1
        self.dots[self.targetFunc(newDot_2)] = newDot_2


    def findResultToExclude(self):
        max_res = -sys.maxsize

        for result, dot in self.dots.items():
            if result > max_res:
                max_res = result
                max_dot = dot
        
        return (max_res, max_dot)
    

    def checkAndSwap(self, exclusion: tuple, reflection: tuple):
        if reflection[0] < exclusion[0]:
            self.dots[reflection[0]] = reflection[1]
            del self.dots[exclusion[0]]
        else:
            self.reduce()


    def findMinValDot(self):
        min_result = sys.maxsize

        for result, dot in self.dots.items():
            if result < min_result:
                min_result = result
                min_dot    = dot

        return (min_result, min_dot)


    def reduce(self):
        print("Результат хуже. Отмена! Редукция!")

        minValDot = self.findMinValDot()
        minDot = minValDot[1]

        res_to_del = []

        for result, dot in self.dots.copy().items():
            if dot == minDot:
                continue
            else:
                newDot = minDot + ((dot - minDot) * 0.5)
                self.dots[self.targetFunc(newDot)] = newDot
                res_to_del.append(result)

        for key in res_to_del:
            if key in self.dots.copy():
                del self.dots[key]


    def reflectDotAndResult(self, wc, dot) -> tuple:
        reflected_dot = (wc * 2) - dot
        return (self.targetFunc(reflected_dot), reflected_dot)
    

    def findCutWeightCenter(self, excludedDot: Dot) -> Dot:
        operated_dots = []

        for result, dot in self.dots.items():
            if dot != excludedDot:
                operated_dots.append(dot)

        return (sum_dots(operated_dots)) * (1/self.n)
    

    def findFullWeightCenter(self) -> Dot:
        return (sum_dots(self.dots.values())) * (1/self.n)
    

    def checkStopCriteria(self, wc):
        isStopped = True

        for dot in self.dots.values():
            cmp_to_eps = abs(round(self.targetFunc(dot) - self.targetFunc(wc), 3))
            if cmp_to_eps < self.epsilon:
                print(str(cmp_to_eps) + " < ", self.epsilon)
            else:
                isStopped = False
                print(str(cmp_to_eps) + " > ", self.epsilon)

        return isStopped


    def calcDelta1(self) -> float:
        '''
        Получение первой дельты
        '''
        return ((sqrt(self.n + 1) - 1) / (self.n * sqrt(2))) * self.m
    
    
    def calcDelta2(self) -> float:
        '''
        Получение второй дельты
        '''
        return ((sqrt(self.n + 1) + self.n - 1) / (self.n * sqrt(2))) * self.m


simplex = Simplex(n = 2, start_dot = Dot(1, 1), m = 0.5, epsilon = 0.1, targetFunction = targetFunction)