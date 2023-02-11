from math import pow, exp, sqrt

def targetFunction(x1: float, x2: float) -> float:
    '''
    Функция 13 варианта
    '''
    return pow(x1, 2) + exp(pow(x1, 2) + pow(x2, 2)) + (4 * x1) + (3 * x2)


class SimplexMinimize:
    '''
    Класс для минимизации функции сипмлексным методом

    n : Размерность функции\n
    m : Длина ребра\n
    epsilon : точность симплексного метода\n

    '''
    n      : int   # Размерность
    m      : float # Длина ребра (каво?)

    epsilon: float # Точность симлексного метода

    delta1 : float # Приращение
    delta2 : float # Приращение

    results: list = [] # Список результатов работы функции

    exclude: list = []

    current_calc_ids: list = []


    def __init__(self, n: int, m: float, epsilon: float, starting_x1: float, starting_x2: float, func) -> None:

        self.n       = n
        self.m       = m

        self.epsilon = epsilon

        self.delta1  = self.calcDelta1()
        self.delta2  = self.calcDelta2()

        self.func = func

        starting_coords_heights = [[starting_x1, starting_x2]] + self.getAdditionalStartingValues(x1_0 = starting_x1, x2_0 = starting_x2)

        self.iterate(starting_coords_heights)

        print(starting_coords_heights)


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
    

    def calcNewHeights(self):
        pass 


    def getAdditionalStartingValues(self, x1_0, x2_0):
        '''
        Получение дополнительных вершин под индексами 1 и 2
        '''
        x1_1 = round(x1_0 + self.delta1, 3)
        x2_1 = round(x2_0 + self.delta2, 3)
        x1_2 = round(x1_0 + self.delta2, 3)
        x2_2 = round(x2_0 + self.delta1, 3)

        return [[x1_1, x1_2], [x2_1, x2_2]]


    def find_3_lowest(self):
        sorted_res = sorted(self.results)[:3:]
        self.current_calc_ids = sorted_res
        

    #def calcWeightCenter(self):


    def iterate(self, dots: list):
        for dot in dots:
            self.results.append(round(self.func(dot[0], dot[1]), 3)) 


simplex = SimplexMinimize(n = 2, m = 0.5, epsilon = 0.1, starting_x1 = 1, starting_x2 = 1, func = targetFunction)
print(simplex.results)