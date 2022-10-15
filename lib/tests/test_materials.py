import unittest
from lib.materials import Materials
from lib.material import Material


class TestMaterials(unittest.TestCase):
    def setUp(self) -> None:
        self.mat = Materials()

    def test_load_csv(self):
        len1 = self.mat.len_materials()
        self.mat.dump_json('materials.json')
        self.mat.load_json('materials.json')
        len2 = self.mat.len_materials()
        self.assertEqual(len1, len2)

    def test_get_material1(self):
        self.mat.load_csv('materials.csv')
        with self.assertRaises(ValueError):
            mat = self.mat.get_by_name(name="Экструдированный пенополистирол", density=25)

    def test_get_material2(self):
        self.mat.load_json('materials.json')
        with self.assertRaises(ValueError):
            mat = self.mat.get_by_name(name="Экструдированный пенополистирол", density=25)

    def test_add_material(self):
        self.mat.add_material(("Кирпичная кладка", "123.5", "0.76", "0.81", "9.7", "10.8"))
        new_material1 = self.mat.get_by_index(0)
        new_dict = {"name": "Кирпичная кладка", "density": 123.5, "ratio_lama": 0.76, "ratio_lamb": 0.81,
                    "ratio_sa": 9.7, "ratio_sb": 10.8}
        new_material2 = Material()
        new_material2.set_data_from_dict(new_dict)
        self.assertEqual(new_material1 == new_material2, True)


    def test_dublicate_material(self):
        self.mat.add_material(("Кирпичная кладка", "123.5", "0.76", "0.81", "9.7", "10.8"))
        new_material1 = self.mat.get_by_index(0)
        self.mat.dublicate_material(0)
        new_material2 = self.mat.get_by_index(1)
        self.assertEqual(new_material1 == new_material2, True)
