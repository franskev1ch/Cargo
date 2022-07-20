import json

#класс описывает пространство в виде параллелипипеда, у которого есть размер и координаты. можно вращать
class Space:
    def __init__(self, a, b, c, pos = [0,0,0]):
        self.a = a
        self.b = b
        self.c = c
        self.pos = pos

    #возвращает все возможные повороты объекта
    def give_all_variations(self):
        res = []
        a = self.a
        b = self.b
        c = self.c
        res.append(Space(a,b,c))
        res.append(Space(a,c,b))
        res.append(Space(b,a,c))
        res.append(Space(b,c,a))
        res.append(Space(c,a,b))
        res.append(Space(c,b,a))
        return res

    #Возвращает объём
    def get_volume(self):
        return self.a*self.b*self.c

    #Копирует массив координат
    def get_pos(self):
        return [self.pos[0], self.pos[1], self.pos[2]]

    #Вращает объект по индексу поворота, совпадающим с индексом массива из функции give_all_variations
    def rotate(self, rotation):
        if( rotation == 0 ):
          return self
        if( rotation == 1 ):
            self.b, self.c = self.c, self.b
            return self
        if( rotation == 2 ):
            self.a, self.b = self.b, self.a
            return self
        if( rotation == 3 ):
            self.a, self.b, self.c = self.b, self.c, self.a
            return self
        if( rotation == 4 ):
            self.a, self.b, self.c = self.c, self.a, self.b
            return self
        if( rotation == 5 ):
            self.a, self.c = self.c, self.a
            return self

    #Проверяет возможность объекту вместится в пространство, описанное объектом Space, не используя поворот
    def check_without_rot(self, free_space):
        return ( self.a <= free_space.a and self.b <= free_space.b and self.c <= free_space.c )

    #Проверяет для всех возможных оборотов объекта, способно ли оно вместиться в пространство. Возвращает индекс оборота либо -1 если это невозможно
    def check(self, free_space):
        rots = self.give_all_variations()
        for i in range(6):
            if( rots[i].check_without_rot(free_space) ):
                return i
        return -1
    #Делает то же что и функция check, но возвращает bool
    def check_bool(self, free_space):
        result = self.check(free_space)
        if result == -1:
            return False
        else:
            return True


#Описывает группу грузов, хранит в себе общий для них размер, айди, а также количество грузов оставшихся в группе
class CargoGroup:
    def __init__(self, json_obj):
        size = json_obj["size"]
        self.size = Space(size[0], size[1], size[2])
        self.count = json_obj["count"]
        self.id = json_obj["id"]





#Описывает оставшееся свободное пространство в которое нужно вмещать грузы
#Свободное пространство хранится в нём в виде массива пересекающихся параллелепидов, описанных классом Space
#Кроме этого массива хранит количество грузов, вписанных в него, начиная с -1. Это сделано для упрощения индексации грузов
class Room:
    def __init__(self, json_obj):
        size = json_obj["size"]
        self.free_spaces = [Space(size[0], size[2], size[1])]
        self.count = -1

    #Кладёт груз в свободное пространство
    #В качестве аргументов принимает груз(Space) и номер элемента массива пустых пространств, в который груз предназначен
    #Так как этот класс хранит только информацию о свободном месте, задача этой функции заключается только в пересчёте свободного пространства, 
    #которое останется впоследствии
    def put_cargo(self, cargo, i):
        cur_space = self.free_spaces[i]
        print('putting cargo ', cur_space.pos, cargo.a, cargo.b, cargo.c)
        cur_space = Space(cur_space.a, cur_space.b, cur_space.c, cur_space.get_pos())
        self.free_spaces.pop(i)
    
        #всего остаться может от 0 до трёх параллелепипедов: один -- пространство над ящиком
        #второй -- пространство справа от ящика
        #третий -- пространство перед ящиком
        #второй и третий параллелепипеды пересекаются между собой в противоположном от груза углу
        #и это нормально, так как мы не используем их одновременно
        if cargo.c < cur_space.c:
            pos = cur_space.get_pos()
            pos[2] += cargo.c
            self.free_spaces.append(Space(cargo.a, cargo.b, cur_space.c - cargo.c, pos))
        if cargo.b < cur_space.b:
            pos = cur_space.get_pos()
            pos[1] += cargo.b
            self.free_spaces.append(Space(cur_space.a, cur_space.b - cargo.b, cur_space.c, pos))
        if cargo.c < cur_space.c:
            pos = cur_space.get_pos()
            pos[0] += cargo.a
            self.free_spaces.append(Space(cur_space.a - cargo.a, cur_space.b, cur_space.c, pos))

        #Основная проблема такого подхода заключается в том что при установке рядом двух грузов с одинаковой высотой
        #В массив свободного места запишется два разных элемента
        #В связи с чем пришлось описывать костыль, пересчитывающий все элементы одной высоты после каждой новой установки груза
        self.recalculate_free_spaces()
        for q in range(len(self.free_spaces)):
            print(q, ": ", self.free_spaces[q].pos, self.free_spaces[q].a, self.free_spaces[q].b, self.free_spaces[q].c)
        self.count += 1



    #Здесь мы берём все пустые пространства одинаковой высоты(высота пустого пространства в моём решении всегда идёт от потолка комнаты)
    #Группируем их в словарь, где ключом является значение высоты
    #И попарно применяем к ним функцию unite_spaces, в результате которой могут получиться 1, 2 или 3 разных спейса
    def recalculate_free_spaces(self):
        free_spaces = sorted(self.free_spaces, key = lambda x : x.c)
        grouped = {}
        grouped[free_spaces[0].c] = [free_spaces[0]]
        for i in range(1, len(free_spaces)):
            height = free_spaces[i].c
            if height != free_spaces[i-1].c:
                grouped[height] = [free_spaces[i]]
            else:
                grouped[height].append(free_spaces[i])

        for key in grouped:
            for i in range(len(grouped[key])):
                for k in range(i):
                    united = unite_spaces(grouped[key][k], grouped[key][i])
                    if len(united) == 3:
                        grouped[key].append(united[0])
                    if len(united) == 2:
                        grouped[key][k] = united[0]
                        grouped[key][i] = united[1]
                    if len(united) == 1:
                        grouped[key][k] = united[0]
                        grouped[key].pop(i)



        

        



#Выдаёт массив из массивов, 4 координаты прямоугольника. 
#Здесь не нужно рассматривать трёхмерное пространство, так как мы работает со спейсами одинаковой высоты
def get_square_sides(space):
    res = [[space.pos[0], space.pos[0]+space.a],
           [space.pos[1], space.pos[1]+space.b]]
    return res


#Вызов этой функции подразумевает, что высота спейс1 и спейс2 одинакова, так что комментарии в дальнейшем даны в контексте двумерных величин
#Функция проверяет, есть ли возможность объединить их чтобы найти наибольшее пространство
#и возвращает массив из 1, 2 или 3 элементов
def unite_spaces(space1, space2):
    new_spaces = []
    a = get_square_sides(space1)
    b = get_square_sides(space2)

    #Объединить два прямоугольника мы можем только если нижняя грань одного совпадает с верхней гранью другого
    if (a[0][1] == b[0][0]) and (min(b[1][1] - a[1][0], a[1][1] - b[1][0]) > 0):
        cur_pos = space1.get_pos()
        cur_pos[1] = max(space1.get_pos()[1], space2.get_pos()[1])

        cur_length = space1.a + space2.a
        cur_width = min(space1.b, space2.b, (b[1][1] - a[1][0]), (a[1][1] - b[1][0]))
        cur_height = space1.c
        new_spaces.append(Space(cur_length, cur_width, cur_height, cur_pos))
        if cur_width == space1.b and cur_width != space2.b:
            new_spaces.append(Space(space2.a, space2.b, space2.c, space2.get_pos()))
            return new_spaces
        if cur_width == space2.b and cur_width != space1.b:
            new_spaces.append(Space(space1.a, space1.b, space1.c, space1.get_pos()))
            return new_spaces
        #В данном случае вторым и третьим элементами должны были вернутся изначальные спейс1 и спейс2, 
        #однако я не вижу смысла заменять объект им же, поэтому при вызове данной функции программа проверяет количество элементов в возвращённом массиве
        #и если их три, то последние 2 не котируются
        new_spaces.append(0)
        new_spaces.append(0)
        return new_spaces

    #Здесь мне пришлось переписать код, который выаолняет абсолютно те же действия для ширины. Не очень красиво, но увы
    if (a[1][1] == b[1][0]) and (min(b[0][1] - a[0][0], a[0][1] - b[0][0]) > 0):
        cur_pos = space1.get_pos()
        cur_pos[0] = max(space1.get_pos()[0], space2.get_pos()[0])

        cur_length = min(space1.a, space2.a, (b[0][1] - a[0][0]), (a[0][1] - b[0][0]))
        cur_width = space1.b + space2.b
        cur_height = space1.c
        new_spaces.append(Space(cur_length, cur_width, cur_height, cur_pos))
        if cur_length == space1.a and cur_length != space2.a:
            new_spaces.append(Space(space2.a, space2.b, space2.c, space2.get_pos()))
            return new_spaces
        if cur_length == space1.a and cur_length != space2.a:
            new_spaces.append(Space(space1.a, space1.b, space1.c, space1.get_pos()))
            return new_spaces
        new_spaces.append(0)
        new_spaces.append(0)
        return new_spaces

    #До сих пор мы проверяли лишь совпадает ли нижняя граница второго с верхней первого (правая второго с левой первого)
    #Однако так как массив в классе Room перемешивается в ходе работы, нам необходимо также проверить и обратный случай
    need_reverse1 = ((b[0][1] == a[0][0]) and (min(a[1][1] - b[1][0], b[1][1] - a[1][0]) > 0))
    need_reverse2 = ((b[1][1] == a[1][0]) and (min(a[0][1] - b[0][0], b[0][1] - a[0][0]) > 0))
    #Рекурсивный запуск, в данном случае это достаточно дёшево по ресурсам, так как максимально возможная глубина рекурсии = 1
    if need_reverse1 or need_reverse2:
        return unite_spaces(space2, space1)

    #В случае, если проверки не дали возможности объединить прямоугольники, мы возвращаем массив с исходными данными
    new_spaces.append(Space(space1.a, space1.b, space1.c, space1.get_pos()))
    new_spaces.append(Space(space2.a, space2.b, space2.c, space2.get_pos()))
    return new_spaces

#В ходе работы я буду пользоваться нижним левым углом, однако в задании требуется указать центр коробки
def get_pos(size, pos):
    return [pos[0] + (size.a / 2), pos[2] + (size.c / 2), pos[1] + (size.b / 2)]



#********************************************************************
#Здесь заканчивается описание функций                               *
# и методов,                                                        *
# и начинается работа непосредственно с данными                     *
#********************************************************************

print('Укажите имя файла (путь к нему можно настроить в settings.py')
source_path="C:/jsons/0/"
result_path="C:/jsons/0/"
name = input()
source_path = source_path  + name

with open(source_path) as loaded_file:
    data = json.load(loaded_file)


cargo_space = data["cargo_space"]
groups = data["cargo_groups"]
cargos = []
for i in range(len(groups)):
    groups[i] = CargoGroup(groups[i])

room = Room(cargo_space)


#Жадный алгоритм заключается в том чтобы каждый раз брать максимально возможную коробку из предоставленных
#Поэтому начнём с сортировки массива
groups = sorted( groups, key = lambda group: group.size.get_volume(), reverse=True )


#Это словарь, в который мы будем упаковывать результаты работы по ходу программы
#И из словаря уже преобразуем всё в джейсон
result = {}

result["cargoSpace"] = {"loading_size": cargo_space['size'], 
                          'type': "pallet", 
                          "position": [cargo_space['size'][0]/2, cargo_space['size'][2]/2,cargo_space['size'][1]/2]}
result['cargos'] = []


#Основной алгоритм, выполняющий саму работу
#Я обернул его в функцию, чтобы иметь возможность пользоваться оператором break во внешнем цикле
def do_it_all(groups, room):
    res = {}

    for k in range(len(groups)):
        group = groups[k]
        if group.count == 0:
            continue
        for i in range(len(room.free_spaces)):
            space = room.free_spaces[i]
            rot = group.size.check(space)
            if rot != -1:
                res["size"] = [group.size.a, group.size.c, group.size.b]
                res["cargo_id"] = group.id
                cargo = group.size
                cargo.rotate(rot)
                room.put_cargo(cargo, i)
                groups[k].count -= 1

                res["calculated_size"] = [cargo.a, cargo.c, cargo.b]
                res["position"] = get_pos(cargo, space.pos)
                res["type"] = "box"
                res["id"] = room.count
                return (groups, room, res)
    return 0

while True:
    #Вызываем наш мейн, он выдаст или 0 -- если ему не удалось вместить ни один больше груз 
    #Или новые значения для room и groups, которые мы перепишем заместо старых, а также res -- словарь, который мы добавим к нашим результатам, 
    #тем которые в конце и будем выгружать в json
    alg = do_it_all(groups, room)
    if alg != 0:
        groups, room, new_res = alg
        result['cargos'].append(new_res)
    else:
        break


counter = room.count
result['unpacked'] = []

for group in groups:
    while group.count > 0:
        cur_res = {}
        cur_res["size"] = [group.size.a, group.size.c, group.size.b]
        cur_res["cargo_id"] = group.id
        result['unpacked'].append(cur_res)
        group.count -= 1

result_path = result_path + name[:-5] + "_result.json"
with open(res_dir, 'w') as outfile:
    json.dump(result, outfile)


