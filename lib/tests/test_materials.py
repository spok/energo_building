import unittest
from lib.materials import Materials
from lib.material import Material


class TestMaterials(unittest.TestCase):
    def setUp(self) -> None:
        self.mat = Materials()
        self.mat.load_csv("materials.csv")

    def test_count_material(self):
        len1 = self.mat.count_materials()
        self.assertEqual(len1, 236)

    def test_load_json(self):
        len1 = self.mat.count_materials()
        self.mat.dump_json()
        self.mat.load_json()
        len2 = self.mat.count_materials()
        self.assertEqual(len1, len2)

    def test_get_material1(self):
        with self.assertRaises(ValueError):
            mat = self.mat.get_by_name(name="Экструдированный пенополистирол", density=25)

    def test_get_material2(self):
        with self.assertRaises(ValueError):
            mat = self.mat.get_by_name(name="Экструдированный пенополистирол", density=25)

    def test_add_material(self):
        self.mat.add_material(("Кирпичная кладка", "123.5", "0.76", "0.81", "9.7", "10.8"))
        new_material1 = self.mat.get_by_index(0)
        new_dict = {"name": "Кирпичная кладка", "density": 123.5, "ratio_lama": 0.76, "ratio_lamb": 0.81,
                    "ratio_sa": 9.7, "ratio_sb": 10.8}
        new_material2 = Material()
        new_material2.set_from_dict(new_dict)
        self.assertEqual(new_material1 == new_material2, True)

    def test_copy_material(self):
        self.mat.add_material(("Кирпичная кладка", "123.5", "0.76", "0.81", "9.7", "10.8"))
        new_material1 = self.mat.get_by_index(0)
        self.mat.copy_material(0)
        new_material2 = self.mat.get_by_index(1)
        self.assertEqual(new_material1 == new_material2, True)

    def test_filter(self):
        count = 0
        for item in self.mat.get_materials("кирп"):
            count += 1
        self.assertEqual(count, 12)
