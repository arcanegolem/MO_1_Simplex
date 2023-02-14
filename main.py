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

    dots   : list = []


    def __init__(self, n: int, m: float, epsilon: float, starting_x1: float, starting_x2: float, func) -> None:

        self.n       = n
        self.m       = m

        self.epsilon = epsilon

        self.delta1  = self.calcDelta1()
        self.delta2  = self.calcDelta2()

        self.func = func

        starting_coords_heights = [[starting_x1, starting_x2]] + self.getAdditionalStartingValues(x1_0 = starting_x1, x2_0 = starting_x2)
        self.dots + starting_coords_heights

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
    

    def getAdditionalStartingValues(self, x1_0, x2_0) -> list:
        '''
        Получение дополнительных вершин под индексами 1 и 2
        '''
        x1_1 = round(x1_0 + self.delta1, 3)
        x2_1 = round(x2_0 + self.delta2, 3)
        x1_2 = round(x1_0 + self.delta2, 3)
        x2_2 = round(x2_0 + self.delta1, 3)

        return [[x1_1, x1_2], [x2_1, x2_2]]


    def find_3_lowest(self):
        '''
        Нахождение индексов наименьших результатов
        '''
        sorted_res = sorted(self.results)[:3:]
        self.current_calc_ids = list(map(lambda it: self.results.index(it), sorted_res))


    def find_exclusion(self):
        '''
        Нахождение наибольшего среди наименьших
        '''
        tmp_value = self.results[self.current_calc_ids[0]]
        exclusion = 0

        for cc in self.current_calc_ids:
            if self.results[cc] > tmp_value:
                exclusion = cc
        
        self.exclude.append(exclusion)


    def reduction(self):
        '''
        Нахождение редукции
        '''
        min_id = self.find_min_id()

        buff_calc = self.current_calc_ids.copy()
        buff_calc.remove(min_id)

        self.dots[buff_calc[0]] = [(self.dots[min_id][0] + 0.5(self.dots[buff_calc[0]][0]) - self.dots[buff_calc[min_id]][0]), 
                                   (self.dots[min_id][1] + 0.5(self.dots[buff_calc[0]][1]) - self.dots[buff_calc[min_id]][1])]
        
        self.dots[buff_calc[1]] = [(self.dots[min_id][0] + 0.5(self.dots[buff_calc[1]][0]) - self.dots[buff_calc[min_id]][0]), 
                                   (self.dots[min_id][1] + 0.5(self.dots[buff_calc[1]][1]) - self.dots[buff_calc[min_id]][1])]


    def find_min_id(self):
        sorted_res = sorted(self.results)[0]
        return self.results.index(sorted_res)


    def find_reflected_dot(self):
        '''
        Отражение точки
        '''
        dots = self.current_calc_ids.copy()
        dots.remove(self.exclude[-1])

        weight_center = self.find_weight_center(self.dots[dots[0]], self.dots[dots[1]])
        excluded_dot = self.dots[self.exclude[-1]]

        self.dots.append([(2 * weight_center - excluded_dot[0]), (2 * weight_center - excluded_dot[1])])

    
    def find_weight_center(self, dot_1_coords: list, dot_2_coords: list):
        '''
        Нахождение центра тяжести
        '''
        return [(0.5 * (dot_1_coords[0] + dot_2_coords[0])), (0.5 * (dot_1_coords[1] + dot_2_coords[1]))]


    def prepare(self, dots: list):
        for dot in dots:
            self.results.append(round(self.func(dot[0], dot[1]), 3))


    def iterate(self, dots: list):
        pass

    
    def check_epsilon(self, wc):
        '''
        Проверка на соответствие критериям
        '''
        for id in self.current_calc_ids:
            if self.results[id] - wc < self.epsilon:
                continue
            else: return False

        return True


simplex = SimplexMinimize(n = 2, m = 0.5, epsilon = 0.1, starting_x1 = 1, starting_x2 = 1, func = targetFunction)
print(simplex.results)
simplex.find_3_lowest()
print(simplex.find_exclusion())