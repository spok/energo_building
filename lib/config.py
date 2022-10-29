PATH_MATERIALS = "lib/materials.json"
HEADER_MATERIALS = ("Название", "Плотность, \nкг/м³", "λа, \nВт/(м∙ºС)", "λb, \nВт/(м∙ºС)", "sa, \nВт/(м²∙ºС)",
                    "sb, \nВт/(м²∙ºС)")
HEADER_CONSTRUCTION = ('Тип конструкции', 'Название конструкции', 'S, м²', 'Ro', 'Назначение', '', '', '')

# Параметры внутренней и наружной поверхности
HEADER_CONSTRUCTION = ('Название материала', 'δ, \nмм', 'λ, \nВт/(м∙ºС)', 's, \nВт/(м²·°С)', 'R, \n(м²·°С)/Вт', 'D')
TYPE_SURFACE_INT = (
    'стен, полов, гладких потолков, потолков с выступающими ребрами \nпри отношении высоты h ребер к расстоянию а между гранями соседних ребер h/a < 0,3',
    'потолков с выступающими ребрами при отношении h/a > 0,3', 'окон', 'зенитных фонарей')
TYPE_SURFACE_EXT = (
    'наружных стен, покрытий, перекрытий над проездами и над холодными (без ограждающих стенок) подпольями \nв Северной строительно-климатической зоне.',
    'перекрытий над холодными подвалами, сообщающимися с наружным воздухом, перекрытий над холодными \n(с ограждающими стенками) подпольями и холодными этажами в Северной строительно-климатической зоне.',
    'перекрытий чердачных и над неотапливаемыми подвалами со световыми проемами в стенах, а также наружных стен \nс воздушной прослойкой, вентилируемой наружным воздухом.',
    'перекрытий над неотапливаемыми подвалами и техническими, подпольями не вентилируемых наружным воздухом.')
RATIO_ALFA_INT = (8.7, 7.6, 8.0, 9.9)
RATIO_ALFA_EXT = (23, 17, 12, 6)

# Типы конструкций
TYPE_CONSTRUCTION = ('Наружная стена', 'Покрытие', 'Чердачное перекрытие', 'Перекрытие над холодным подвалом',
              'Перекрытие над проездом', 'Окна', 'Витражи', 'Фонари', 'Двери', 'Ворота',
              'Конструкция в контакте с грунтом')
TYPE_BUILDINGS = ("Жилое", "Лечебно-профилактическое", "Детское учреждение", "Школа", "Интернат", "Гостиница",
                 "Общежитие", "Общественное", "Административное", "Сервисного обслуживания", "Бытовое",
                 "Производственное и другое с влажным или мокрым режимом эксплуатации",
                 "Производственное с сухим и нормальным режимом эксплуатации")
TYPE_HEAT_SYSTEM = ('система отопления с местными терморегуляторами и пофасадным авторегулированием на вводе',
               'система отопления с местными терморегуляторами и центральным авторегулированием на вводе',
               'система отопления без местных терморегуляторов и пофасадным авторегулированием',
               'система отопления с местными терморегуляторами и без авторегулирования на вводе',
               'система отопления без местных терморегуляторов и центральным авторегулированием на вводе',
               'система отопления без местных терморегуляторов и без авторегулирования на вводе')
LATITUDE = (37, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78)
ORIENTATION = ('С', 'З', 'Ю', 'В', 'СЗ', 'СВ', 'ЮЗ', 'ЮВ')
LOCATION = ('Ограждающая', 'Внутреняя чердака', 'Наружная чердака', 'Внутреняя подвала', 'Наружная подвала')
