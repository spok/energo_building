class BaseElement:
    """Класс для элементов конструкций"""
    def __init__(self):
        self.name = ''

    def get_dict(self):
        """Генерация словаря с данными
        :return - словарь"""
        data = dict()
        for key in self.__dict__:
            data[key] = self.__dict__[key]
        return data

    def data_from_dict(self, data: dict):
        """Загрузка данных из словаря"""
        for key in data:
            if key in self.__dict__.keys():
                self.__dict__[key] = data[key]


class BaseConstruction:
    """Класс базовой конструкции"""
    def __init__(self):
        self.typ = ''
        self.name = ''
        self.area = 0.0
        self.r_pr = 0.0
        self.r_tr = 0.0
        self.r_tr_min = 0.0
        self.elements = []

    def get_dict(self):
        """Генерация словаря с данными
        :return - словарь"""
        data = dict()
        for key in self.__dict__:
            if key == 'elements':
                elements = []
                for elem in self.__dict__[key]:
                    elements.append(elem.get_dict())
                data[key] = elements
            else:
                data[key] = self.__dict__[key]
        return data

    def data_from_dict(self, data: dict):
        """Загрузка данных из словаря"""
        for key in data:
            if key == 'elements':
                self.elements.clear()
                for i, con in enumerate(data[key]):
                    if con.typ in ['Наружная стена', 'Покрытие', 'Чердачное перекрытие',
                                   'Перекрытие над холодным подвалом', 'Перекрытие над проездом']:
                        self.add_layer()
                    elif con.typ in ['Окна', 'Витражи', 'Фонари']:
                        self.add_window()
                    elif con.typ in ['Двери', 'Ворота']:
                        pass # дописать
                    elif con.typ == 'Конструкция в контакте с грунтом':
                        pass # дописать
                    self.elements[i].data_from_dict(con)
            else:
                if key in self.__dict__.keys():
                    self.__dict__[key] = data[key]

    def get_construction_name(self):
        """Генерация имени конструкции для дерева"""
        elem_text = ''
        if len(self.name) > 20:
            elem_text = self.name
        else:
            if len(self.name) == 0:
                elem_text = self.typ
            else:
                elem_text = self.typ + ' - ' + self.name
        return elem_text


class Material:
    def __init__(self):
        self.name = ''
        self.plotn = 0.0
        self.lam_a = 0.0
        self.lam_b = 0.0
        self.s_a = 0.0
        self.s_b = 0.0