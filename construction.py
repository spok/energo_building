class Material:
    def __init__(self):
        self.name = ''
        self.plotn = 0.0
        self.lam_a = 0.0
        self.lam_b = 0.0
        self.s_a = 0.0
        self.s_b = 0.0


class Layer:
    def __init__(self):
        self.name = ''
        self.delta = 0.0
        self.lam = 0.0
        self.r = 0.0
        self.s = 0.0
        self.d = 0.0

    def get_r(self):
        self.r = self.delta / self.lam
        return self.r

    def get_d(self):
        self.d = self.r * self.s
        return self.d


class Construction:
    def __init__(self):
        self.layer = []
        self.typ = ''
        self.name = ''
        self.area = 0.0
        self.alfa_v = 0.0
        self.alfa_n = 0.0
        self.r_neodn = 0.0
        self.ro = 0.0
        self.r_pr = 0.0
        self.b = 0.0
        self.y_int = 0.0


class Building:
    def __init__(self):
        self.typ = 'Жилое'
        self.v_heat = 0.0
        self.floors = 0
        self.area_all = 0.0
        self.area_calc = 0.0
        self.area_live = 0.0
        self.height_building = 0.0
        self.t_int = 20.0
        self.w_int = 55.0

        self.citi = 'Волгоград'
        self.t_nhp = 0.0
        self.t_ot = 0.0
        self.z_ot = 0.0
        self.gsop = 0.0


