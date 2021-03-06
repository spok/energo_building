class BaseElement:
    """Класс для элементов конструкций"""
    def __init__(self):
        # для многослойных конструкций
        self.name = ''
        self.thickness = 0.0
        self.lam = 0.0
        self.r = 0.0
        self.s = 0.0
        self.d = 0.0
        # для окон и витражей
        self.r_pr = 0.0
        self.area = 0.0
        self.size = '0*0'
        self.size_b = 0.0
        self.size_h = 0.0
        self.count_orientation = dict()
        self.g_koef = 0.0
        self.tau_koef = 0.0
        self.i_rad = 0.0
        # для дверей
        self.count = 0
        # для грунта
        self.area_list = []

    def set_size(self, size: str):
        """Определение размера окна из строковой переменной"""
        self.size = size
        s = []
        for razd in ['*', 'x', 'х', 'X', 'Х']:
            if razd in size:
                s = size.split(razd)
        if len(s) > 1 and len(size) > 0:
            self.size_b = float(s[0])
            self.size_h = float(s[1])

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
        self.purpose = 'Ограждающая'
        self.t_ext = 0.0
        self.n_coef = 1.0
        self.nAR = 0.0
        self.r_fact = 0.0

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
        cur_typ = data['typ']
        for key in data:
            if key == 'elements':
                self.elements.clear()
                for i, con in enumerate(data[key]):
                    if cur_typ in ['Наружная стена', 'Покрытие', 'Чердачное перекрытие',
                                   'Перекрытие над холодным подвалом', 'Перекрытие над проездом']:
                        self.add_layer(index=i)
                    elif cur_typ in ['Окна', 'Витражи', 'Фонари']:
                        self.add_window(index=i)
                    elif cur_typ in ['Двери', 'Ворота']:
                        self.add_door(index=i)
                    elif cur_typ == 'Конструкция в контакте с грунтом':
                        self.add_ground(index=i)
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