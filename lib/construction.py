from layer import Layer


class Construction:
    def __init__(self):
        self.__layers = []
        self.__ratio_inner_surface = 8.7
        self.__ratio_outer_surface = 23
        self.__ratio_r = 1.0
        self.__resistance = 0.0
        self.__name = ""
        self.__heat_construction = True

    def add_layer(self, index: int = -1):
        """
        Добавление нового слоя
        :param index: номер слоя для вставки, -1 вставка слоя в конец
        :return: None
        """



