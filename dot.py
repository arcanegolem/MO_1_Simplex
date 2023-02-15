from __future__ import annotations

class Dot:
    '''
    Класс точек в двумерном пространстве

    coord_x : координата по X
    coord_y : координата по Y
    '''
    coord_x : float
    coord_y : float

    def __init__(self, coord_x: float, coord_y: float) -> None:
        self.coord_x = coord_x
        self.coord_y = coord_y


    def __mul__(self, other: Dot) -> Dot:
        return Dot(round(self.coord_x * other, 3), round(self.coord_y * other, 3))


    def __add__(self, other: Dot) -> Dot:
        return Dot(round(self.coord_x + other.coord_x, 3), round(self.coord_y + other.coord_y, 3))
    

    def __sub__(self, other: Dot):
        return Dot(round(self.coord_x - other.coord_x, 3), round(self.coord_y - other.coord_y, 3))
    

    def __eq__(self, other: Dot) -> bool:
        if (self.coord_x == other.coord_x) and (self.coord_y == other.coord_y):
            return True
        return False


    def __ne__(self, other: object) -> bool:
        if (self.coord_x != other.coord_x) or (self.coord_y != other.coord_y):
            return True
        return False


    def copy(self):
        return self
    

    def __str__(self) -> str:
        ret_str = "Dot: x = {xCoord}, y = {yCoord}".format(xCoord = self.coord_x, yCoord = self.coord_y)
        return ret_str + " " * (25 - len(ret_str))
    

def sum_dots(dot_list: list) -> Dot:
    buff_dot = Dot(0.0, 0.0)

    for dot in dot_list:
        buff_dot = buff_dot + dot

    return buff_dot

# dot_1 = Dot(1.32, 10.21)
# dot_2 = Dot(0.32, 10.21 )

# print(str(dot_1 - dot_2))

#Dot: x = 1.129, y = 1.483