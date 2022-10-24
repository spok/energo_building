import unittest
from lib.material import Material


class TestMaterai(unittest.TestCase):
    def setUp(self):
        self.mat = Material()
        self.mat.name = "Кирпичная кладка"

    def test_name(self):
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
        self.mat.set_from_dict(new_dict)
        self.assertEqual(self.mat.get_dict_from_data(), new_dict)

    def test_set_lama(self):
        with self.assertRaises(ValueError):
            self.mat.ratio_lama = '0.82'

    def test_set_lamb(self):
        with self.assertRaises(ValueError):
            self.mat.ratio_lamb = '0.82'

    def test_get_lama(self):
        self.mat.ratio_lama = 0.76
        self.assertEqual(self.mat.ratio_lama, 0.76)

    def test_get_lamb(self):
        self.mat.ratio_lamb = 0.81
        self.assertEqual(self.mat.ratio_lamb, 0.81)

    def test_get_lam1(self):
        self.mat.ratio_lama = 0.76
        self.mat.ratio_lamb = 0.81
        Material.environment = 'А'
        self.assertEqual(self.mat.get_lam(), 0.76)

    def test_get_lam2(self):
        self.mat.ratio_lama = 0.76
        self.mat.ratio_lamb = 0.81
        Material.environment = 'В'
        self.assertEqual(self.mat.get_lam(), 0.81)

    def test_get_lam3(self):
        self.mat.ratio_lama = 0
        self.mat.ratio_lamb = 0.81
        Material.environment = 'А'
        self.assertEqual(self.mat.get_lam(), 0.81)

    def test_get_lam4(self):
        self.mat.ratio_lama = 0.76
        self.mat.ratio_lamb = 0
        Material.environment = 'В'
        self.assertEqual(self.mat.get_lam(), 0.76)


if __name__ == '__main__':
    unittest.main()
