import json

with open("C:/jsons/0/30_cl.json") as loaded_file:
  data = json.load(loaded_file)


cargo_space = data["cargo_space"]
groups = data["cargo_groups"]
cargos = []

class Space:
  def __init__(self, a, b, c, pos = [0,0,0], rotation = 0):
    self.a = a
    self.b = b
    self.c = c
    if( rotation != 0 ):
      self.turn(rotation)
    self.pos = pos


  def give_all_variations(self):
    res = []
    res.append(Space(a,b,c))
    res.append(Space(a,c,b))
    res.append(Space(b,a,c))
    res.append(Space(b,c,a))
    res.append(Space(c,a,b))
    res.append(Space(c,b,a))
    return res


  def get_volume(self):
    return self.a*self.b*self.c


  def rotate(self, rotation):
    if( rotation == 0 ):
      return self
    if( rotation == 1 ):
      self.b, self.c = self.c, self,b
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


  def check_without_rot(self, free_space):
    return ( self.a <= free_space.a and self.b <= free_space.b and self.c <= free_space.c )


  def check(self, free_space):
    rots = self.give_all_variations()
    for i in range(6):
      if( rots[i].check_without_rot(free_space) ):
        return i
    return -1

  def check_bool(self, free_space):
    result = self.check(free_space)
    if result == -1:
      return False
    else:
      return True



class CargoGroup:
  def __init__(self, json_obj):
    size = json_obj["size"]
    self.size = Space(size[0], size[1], size[2])
    self.count = json_obj["count"]
    self.id = json_obj["id"]





class Room:
  def __init__(self, json_obj):
    size = json_obj["size"]
    self.id = json_obj['id']
    self.free_spaces = Space(size[0], size[1], size[2])


  def put_cargo(self, cargo, position = [0,0,0], rot = 0):
    cargo.rotate(rot)
    if (cargo.pos == [0,0,0]) and (position != [0,0,0]) :
      cargo.pos = position
    for i in range(len(free_spaces)):
      if self.free_spaces[i].pos == cargo.pos:
        cur_space = free_spaces[i]
        self.free_spaces.pop(i)
        if cargo.c < cur_space.c:
          pos = cargo.pos
          pos[2] += cargo.c
          self.free_spaces.append(Space(cargo.a, cargo.b, cur_space.c - cargo.c, pos))
        if cargo.b < cur_space.b:
          pos = cargo.pos
          pos[1] += cargo.b
          self.free_spaces.append(Space(cur_space.a, cur_space.b - cargo.b, cur_space.c, pos))
        if cargo.c < cur_space.c:
          pos = cargo.pos
          pos[0] += cargo.a
          self.free_spaces.append(Space(cur_space.a - cargo.a, cur_space.b, cur_space.c, pos))
    self.recalculate_free_spaces()

  def recalculate_free_spaces(self):
    free_spaces = sorted(self.free_spaces, key = lambda x : x.c)
    for i in range(1, len(free_spaces)):
      if free_spaces[i-1].c == free_spaces[i].c:
        new_spaces = combine_spaces(free_spaces[i-1], free_spaces[i])
        if len(new_spaces) == 1:
          free_spaces.pop(i-1)
          free_spaces[i] = new_spaces[0]
        else:
          free_spaces[i-1] = new_spaces[0]
          free_spaces[i] = new_spaces[1]
    self.free_spaces = free_spaces


            




  def calculate_free_spaces(self):
    res = []
    height = 0

def combine_spaces(space1, space2):
  new_spaces = []
  if space1.pos[0] + cpace1.a == space2.pos[0]:
    if space1.pos[1] == space2.pos[1]:
      new_spaces.append(Space(space1.a + space2.a, min(space1.b, space2.b), space2.c, space1.pos))
      if space1.b != space2.b:
        new_spaces.append(space1)
    else:
      new_spaces.append(Space(space2.a + space1.a, space2.b, cpace1.c, [space1.pos[0], space2.pos[1], space2.pos[2]]))
      new_spaces.append(space1)
    return new_spaces
  if space1.pos[1] + space1.b == space2.pos[1]:
    if space1.pos[0] == space2.pos[0]:
      new_spaces.append(Space(min(space1.a, space2.a), space2.b+space1.b, space1.c, space1.pos))
      if space1.a != space2.a:
        new_spaces.append(space1)
    else:
      new_spaces.append(Space(space2.a, space2.b+space1.b, space1.c, [space2.pos[0], space1.pos[1], space1.pos[2]]))
      new_spaces.append(space1)
    return new_spaces
  return combine_spaces(space2, space1)



for i in range(len(groups)):
  groups[i] = CargoGroup(groups[i])

room = Room(cargo_space)




groups = sorted( groups, key = lambda group: group.size.get_volume(), reverse=True )
for group in groups:
  print( group.size.get_volume() )

print("Cargo space")
print(cargo_space)

while True:
  for group in groups:
    for space in room.free_spaces
      rot = group.size.check(space)
      if rot != -1:
        cargo = group.size
        cargo.rotate(rot)
        room.put_cargo(cargo, space.pos)

delay = input()