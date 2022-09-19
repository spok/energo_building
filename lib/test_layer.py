import unittest
from layer import Layer
from material import Material

class TestLayer(unittest.TestCase):
    def setUp(self) -> None:
        self.l = Layer()

    def test_null_layer(self):
        self.assertEqual(self.l.resistance, 0)

    def test_null_environment(self):
        self.assertEqual(self.l.environment, "A")

    def test_set_environment(self):
        self.l.environment = "B"
        self.assertEqual(self.l.environment, "B")

    def test_set_thickness(self):
        self.l.thickness = 100
        self.assertEqual(self.l.thickness, 100)
        self.assertEqual(self.l.resistance, 0)

    def test_set_lambda(self):
        self.l.thickness = 100
        self.l.ratio_lam = 0.1
        self.assertEqual(self.l.ratio_lam, 0.1)
        self.assertEqual(self.l.resistance, 1)

    def test_get_dict(self):
        new_dict = {"number": 1, "thickness": 100, "ratio_lam": 0.1,
                    "material": {"name": "Кирпичная кладка", "density": 123.5,
                                 "ratio_lama": 0.76, "ratio_lamb": 0.81,
                                 "ratio_sa": 9.7, "ratio_sb": 10.8}}
        self.l.set_data_from_dict(new_dict)
        self.assertEqual(self.l.get_dict_from_data(), new_dict)
