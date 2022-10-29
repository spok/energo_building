import unittest
from lib.layer import Layer
from lib.material import Material

class TestLayer(unittest.TestCase):
    def setUp(self) -> None:
        self.layer = Layer()
        self.layer.thickness = 100
        self.layer.number = 3
        self.material = Material()
        new_dict = {"name": "Кирпичная кладка", "density": 1800, "ratio_lama": 0.1, "ratio_lamb": 0.2,
                    "ratio_sa": 9.7, "ratio_sb": 10.8}
        self.material.set_from_dict(new_dict)
        self.layer.material = self.material

    def test_null_layer(self):
        self.assertEqual(self.layer.resistance, 1)

    def test_set_environment1(self):
        Material.environment = 'А'
        self.layer.calc_resistance()
        self.assertEqual(self.layer.ratio_lam, 0.1)
        self.assertEqual(self.layer.resistance, 1)

    def test_set_environment2(self):
        Material.environment = 'В'
        self.layer.calc_resistance()
        self.assertEqual(self.layer.ratio_lam, 0.2)
        self.assertEqual(self.layer.resistance, 0.5)

    def test_set_thickness(self):
        Material.environment = 'А'
        self.layer.thickness = 200
        self.assertEqual(self.layer.thickness, 200)
        self.assertEqual(self.layer.resistance, 2)

    def test_change_material(self):
        self.material = Material()
        new_dict = {"name": "Минераловатный утеплитель", "density": 50, "ratio_lama": 0.05, "ratio_lamb": 0.1,
                    "ratio_sa": 9.7, "ratio_sb": 10.8}
        self.material.set_from_dict(new_dict)
        self.layer.material = self.material
        self.layer.thickness = 150
        self.assertEqual(self.layer.thickness, 150)
        self.assertEqual(self.layer.resistance, 3)

    def test_get_text_sym(self):
        self.assertEqual(self.layer.get_text_sym(), f'δ<sub>3</sub>/λ<sub>3</sub>')

    def test_get_text_num(self):
        self.assertEqual(self.layer.get_text_num(), f'{100/1000}/{0.1}')

    def test_get_name1(self):
        self.assertEqual(self.layer.name, "Кирпичная кладка")
        new_dict = {"name": "Минераловатный утеплитель", "density": 50, "ratio_lama": 0.05, "ratio_lamb": 0.1,
                    "ratio_sa": 9.7, "ratio_sb": 10.8}
        self.material.set_from_dict(new_dict)
        self.layer.material = self.material
        self.assertEqual(self.layer.name, "Минераловатный утеплитель")

    def test_get_dict(self):
        new_dict = {"number": 1, "thickness": 100, "ratio_lam": 0.1,
                    "material": {"name": "Кирпичная кладка", "density": 123.5,
                                 "ratio_lama": 0.76, "ratio_lamb": 0.81,
                                 "ratio_sa": 9.7, "ratio_sb": 10.8}}
        self.layer.set_from_dict(new_dict)
        self.assertEqual(self.layer.get_dict(), new_dict)
