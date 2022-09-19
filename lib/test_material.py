import unittest
from material import Material


class TestMaterai(unittest.TestCase):
    def setUp(self):
        self.mat = Material()

    def test_name(self):
        self.mat.name = "Кирпичная кладка"
        self.assertEqual(self.mat.name, "Кирпичная кладка")

    def test_name_raise(self):
        with self.assertRaises(ValueError):
            self.mat.name = 123

    def test_density(self):
        self.mat.density = 123.5
        self.assertEqual(self.mat.density, 123.5)

    def test_density_raise(self):
        with self.assertRaises(ValueError):
            self.mat.density = '123'

    def test_get_dict(self):
        new_dict = {"name": "Кирпичная кладка", "density": 123.5, "ratio_lama": 0.76, "ratio_lamb": 0.81,
                    "ratio_sa": 9.7, "ratio_sb": 10.8}
        self.mat.set_data_from_dict(new_dict)
        self.assertEqual(self.mat.get_dict_from_data(), new_dict)


if __name__ == '__main__':
    unittest.main()
