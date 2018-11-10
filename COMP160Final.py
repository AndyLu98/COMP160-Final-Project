#Rogue:Infinitum is a 2D top-down roguelike game. 
#This is the final version of the game. 
#Each level is randomly generated and is a map that consists of a set of rooms and corridors. 
#In each level, a chest and a weapon rack will be randomly generated. You can obtain random consumables and equipments from them.
#In each level, there will be monsters chasing after you. 
#There are two types of monster: regular monster and poison spider. As the name suggests, poison spider's attack can poison the player and causes continuous damage to the player.
#The monsters get stronger and stronger as the player ventures deeper and deeper into the dungeon.
#Textual display of the player's actions is also implemented in this final version. 

#A Cheat-Mode button is implemented. When you hit the button, the fog of war is removed and you can see every room. This button is designed to make the debugging process easier.

#Link to the game pitch sheet: https://drive.google.com/file/d/0B4-4lYKY6JTgUkZQOXh5b2dXaHM/view?usp=sharing

#Control: 
# 'w' - move up/ attack when the enemy is directly above
# 'a' - move left/ attack when the enemy is directly to the left
# 's' - move down/ attack when the enemy is directly beneath
# 'd' - move right/ attack when the enemy is directly to the right
# 'z' - pick up items from chest/weapon rack
# 'mouse click' - click on the consumables to use. Click on the little 'x' beside the item to discard.
# 'space' - restore stamina

import simplegui
import random
import math

CANVAS_WIDTH = 900
CANVAS_HEIGHT = 600
INDI_GRID_SIZE = 20
GRID_WIDTH = (CANVAS_WIDTH)/INDI_GRID_SIZE
GRID_HEIGHT = CANVAS_HEIGHT/INDI_GRID_SIZE
EARTH = 0
ROOM = 1
CORRIDOR = 2
ITEM = 3
WEAPON = 4
type_of_terrain = dict()
DESIRED_NUM_ROOM = 8
Monster_group = list()
Map_group = list()
Cheat_Mode = False
Monster_Number = 2
Chest_group = list()
Weapon_rack_group = list()
box_for_inventory = list()
ITEM_SIZE = 50
ITEM_NUMBER = 7
TIMER_COUNTER = 0
counter = 0
IN_PLAY = False
HELP = False
HIGH_SCORE = False
GAME_OVER = False
IN_GAME_GUIDE = False
high_score = list()
sword_wielding = False
shield_wielding = False
torch_wielding = False
amulet_of_stamina = False
amulet_of_health = False
music_timer = 0 

#############################################Images and Sound#############################################
#Find the coordinates of the image rectangle based on its center and size

class ImageInfo:
    def __init__(self,center, size, dest_center, dest_size):
        self.center = center
        self.size = size
        self.dest_center = dest_center
        self.dest_size = dest_size
        
    def get_center(self):
        return self.center
    
    def get_size(self):
        return self.size
    
    def get_dest_center(self):
        return self.dest_center
    
    def get_dest_size(self):
        return self.dest_size

Title_image_info = ImageInfo((892,191),(1784, 382),(575,150),(891,191))
Title_image = simplegui.load_image("https://dl.dropbox.com/s/ai4i2caec79vxnd/Screen%20Shot%202017-11-16%20at%201.26.41%20PM.png")

Play_button_info = ImageInfo((327,141),(654,282),(575,325),(204,88))
Play_button = simplegui.load_image('https://dl.dropbox.com/s/s37x6rdmfa3bdqv/Screen%20Shot%202017-11-16%20at%201.54.27%20PM.png')

Help_button_info = ImageInfo((295,130),(590,260),(575,425),(204,88))
Help_button = simplegui.load_image('https://dl.dropbox.com/s/afo78622elbg5jc/Screen%20Shot%202017-11-17%20at%201.11.08%20AM.png')

High_score_button_info = ImageInfo((577,128),(1154,256),(575,525),(392,88))
High_score_button = simplegui.load_image('https://dl.dropbox.com/s/5r8c2bxpvp8e5ax/Screen%20Shot%202017-11-18%20at%205.18.04%20PM.png')

Back_button_info = ImageInfo((284,108),(568,216),(1000,550),(189,72))
Back_button = simplegui.load_image('https://dl.dropbox.com/s/pi82qakbcz7ulzj/Screen%20Shot%202017-11-17%20at%205.06.35%20PM.png')

Help_screen_info = ImageInfo((400,300),(800,600),(450,300),(900,600))
Help_screen = simplegui.load_image('https://dl.dropbox.com/s/1ebafeaxul47c72/How%20to%20play%20screeen%205.png')
                                   
You_died_info1 = ImageInfo((133,86),(266,172),(425,300),(266,172))
You_died1 = simplegui.load_image('https://dl.dropbox.com/s/jd7bc7o8p4c4ufv/Screen%20Shot%202017-11-18%20at%206.28.46%20PM.png')

You_died_info2 = ImageInfo((181,90),(362,180),(725,300),(266,172))
You_died2 = simplegui.load_image('https://dl.dropbox.com/s/ybxvnz15bcig7ig/Screen%20Shot%202017-11-18%20at%206.30.41%20PM.png')

High_score_info1 = ImageInfo((175,97),(350,194),(375,150),(350,194))
High_score1 = simplegui.load_image('https://dl.dropbox.com/s/fdgtd3kz7j4rnzs/Screen%20Shot%202017-11-18%20at%2010.30.52%20PM.png')

High_score_info2 = ImageInfo((212,103),(424,206),(750,150),(350,194))
High_score2 = simplegui.load_image('https://dl.dropbox.com/s/chl2e3gd4sycu41/Screen%20Shot%202017-11-18%20at%2010.31.14%20PM.png')

One_info = ImageInfo((68,93),(136,186),(150,300),(50,96))
ONE = simplegui.load_image('https://dl.dropbox.com/s/mw7gto4yd9eqazg/Screen%20Shot%202017-11-18%20at%2011.00.42%20PM.png')

Two_info = ImageInfo((75,90),(150,180),(150,400),(50,96))
Two = simplegui.load_image('https://dl.dropbox.com/s/b3d4podf8zs9nbb/Screen%20Shot%202017-11-18%20at%2010.45.48%20PM.png')

Three_info = ImageInfo((77,100),(154,200),(150,500),(50,96))
Three = simplegui.load_image('https://dl.dropbox.com/s/c4y378kgcfmrmye/Screen%20Shot%202017-11-18%20at%2010.46.09%20PM.png')

soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

def image_coord(center,size):
    coord = []
    coord1 = [center[0]- 0.5* size[0], center[1]- 0.5* size[1]]
    coord2 = [center[0]+ 0.5* size[0], center[1]- 0.5* size[1]]
    coord3 = [center[0]+ 0.5* size[0], center[1]+ 0.5* size[1]]
    coord4 = [center[0]- 0.5* size[0], center[1]+ 0.5* size[1]]
    coord = [coord1, coord2, coord3, coord4]
    return coord

def item_coord(center, size):
    coord = []
    coord1 = [center[0]- 0.5* size, center[1]- 0.5* size]
    coord2 = [center[0]+ 0.5* size, center[1]- 0.5* size]
    coord3 = [center[0]+ 0.5* size, center[1]+ 0.5* size]
    coord4 = [center[0]- 0.5* size, center[1]+ 0.5* size]
    coord = [coord1, coord2, coord3, coord4]
    return coord

for i in range(ITEM_NUMBER):
    box_for_inventory.append(item_coord([950, 260+ i* ITEM_SIZE],ITEM_SIZE))
    
class Map:    
    def __init__(self,grid_width,grid_height):
        global type_of_terrain, distance_field        
        self.GRID_WIDTH = grid_width
        self.GRID_HEIGHT = grid_height
        self.mapgrid = [[EARTH for col in range(self.GRID_WIDTH)] 
                   for row in range(self.GRID_HEIGHT)]          
        self.rooms = list()
        self.fog_of_war = list()
        self.readable_grid = [[(y,x) for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)] 
        self.exit = []       
        for row in range(self.GRID_HEIGHT):
            for grid in self.readable_grid[row]:
                type_of_terrain[grid] = EARTH 
                
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                self.fog_of_war.append((y,x))
        
    def create_room(self,room):
        self.rooms.append(room)
                    
    def generate_room(self, pos):
        char_pos = pos 
        if pos[0] >= 4 and pos[0] <= GRID_HEIGHT -4 and pos[1] >= 4 and pos[1] <= GRID_WIDTH - 4:
            ROOM_HEIGHT = random.randrange(1,4)
            ROOM_WIDTH = random.randrange(1,4)
                                   
        elif pos[0] >= 4 and pos[0] <= GRID_WIDTH -4 and pos[1] < 4:
            ROOM_HEIGHT = random.randrange(1,4)
            ROOM_WIDTH = pos[1]
        
        elif pos[0] >= 4 and pos[0] <= GRID_WIDTH -4 and pos[1] >= GRID_WIDTH - 4:
            ROOM_HEIGHT = random.randrange(1,4)
            ROOM_WIDTH = 0
        
        elif pos[0] < 4 and pos[1] >= 4 and pos[1] <= GRID_WIDTH - 4:
            ROOM_HEIGHT = pos[0]
            ROOM_WIDTH = random.randrange(1,4)

        elif pos[0] >= GRID_HEIGHT - 4 and pos[1] >= 4 and pos[1] <= GRID_WIDTH - 4:
            ROOM_HEIGHT = GRID_HEIGHT - pos[0]
            ROOM_WIDTH = random.randrange(1,4)
        
        elif pos[0] < 4 and pos[1] < 4:
            ROOM_HEIGHT = pos[0]
            ROOM_WIDTH = pos[1]
        
        elif pos[0] >= GRID_HEIGHT - 4 and pos[1] < 4:
            ROOM_HEIGHT = GRID_HEIGHT - pos[0]
            ROOM_WIDTH = pos[1]
        
        elif pos[0] < 4 and pos[1] >= GRID_WIDTH - 4:
            ROOM_HEIGHT = pos[0]
            ROOM_WIDTH = GRID_WIDTH - pos[1]
        
        elif pos[0] >= GRID_HEIGHT - 4 and pos[1] >= GRID_WIDTH - 4:
            ROOM_HEIGHT = GRID_HEIGHT - pos[0]
            ROOM_WIDTH = GRID_WIDTH - pos[1]
        
        coord1 = (char_pos[0]-ROOM_HEIGHT,char_pos[1]-ROOM_WIDTH)
        coord2 = (coord1[0],coord1[1] + 2*ROOM_WIDTH)
        coord3 = (coord1[0]+ 2*ROOM_HEIGHT,coord1[1] + 2*ROOM_WIDTH)
        coord4 = (coord1[0]+ 2*ROOM_HEIGHT,coord1[1])
        newroom = Room(coord1,coord2,coord3,coord4)
        self.create_room(newroom)
        newroom.update_type_of_terrain()
                 
        while len(self.rooms) < DESIRED_NUM_ROOM:
            ROOM_LENGTH = random.randrange(6,8)
            ROOM_WIDTH = random.randrange (6,8)
            i = random.randrange(0,GRID_HEIGHT)
            coord1 = random.choice(self.readable_grid[i])
            coord2 = (coord1[0],coord1[1] + ROOM_LENGTH)
            coord3 = (coord1[0]+ ROOM_WIDTH,coord1[1] + ROOM_LENGTH)
            coord4 = (coord1[0]+ ROOM_WIDTH,coord1[1])
            if coord2[1] <  self.GRID_WIDTH - 1 and coord3[0] < self.GRID_HEIGHT - 1:
                newroom = Room(coord1,coord2,coord3,coord4)
                for rooms in self.rooms:
                    if not any([newroom.intersect(rooms) for rooms in self.rooms]):
                        newroom.connect_rooms(self.rooms[-1])
                        newroom.update_type_of_terrain()
                        self.rooms.append(newroom)
        
        if len(self.rooms) == DESIRED_NUM_ROOM:
            self.rooms[-1].connect_rooms(self.rooms[0])
            self.rooms[-1].update_type_of_terrain()
    
    def generate_treasure_chest(self):
        global Chest_group, type_of_terrain
        Potential_spawn_point = []
        for key in type_of_terrain:
            if type_of_terrain[key] == 1:
                Potential_spawn_point.append(key)
        Chest_group.append(Chest(random.choice(Potential_spawn_point)))
        type_of_terrain[Chest_group[0].get_pos()] = ITEM
    
    def generate_weapon_rack(self):
        global Weapon_rack_group
        Potential_spawn_point = []
        for key in type_of_terrain:
            if type_of_terrain[key] == 1:
                Potential_spawn_point.append(key)
        Weapon_rack_group.append(weapon_rack(random.choice(Potential_spawn_point)))
        type_of_terrain[Weapon_rack_group[0].get_pos()] = WEAPON
    
    def generate_exit(self):
        Potential_spawn_point = []
        for key in type_of_terrain:
            if type_of_terrain[key] == 1:
                Potential_spawn_point.append(key)    	
        self.exit = random.choice(Potential_spawn_point)
         
    def regenerate(self):
        global type_of_terrain, Monster_group, Map_group, counter, Monster_Number, Chest_group, Weapon_rack_group
        type_of_terrain = dict()
        Monster_group = list()
        Chest_group = list()
        Weapon_rack_group = list()
        Map_group.append(Map(GRID_WIDTH,GRID_HEIGHT))
        counter += 1
        Map_group[counter].generate_room(My_adventurer.get_pos())
        Map_group[counter].generate_exit()
        Map_group[counter].generate_treasure_chest()
        Map_group[counter].generate_weapon_rack()
        if Monster_Number <= 5:
            Monster_Number += 1
        for i in range(Monster_Number):
            spawn_monsters()
        if counter >= 3:
            for i in range(Monster_Number - 3):
                spawn_spiders()
        My_adventurer.update_fog_of_war()
        My_adventurer.attack += 1
                
    def draw(self,canvas):
        for i in range(self.GRID_HEIGHT):
            for grid in self.readable_grid[i]:
                canvas.draw_polygon(grid_to_coord(grid),1,'black','black')
        
        for room in self.rooms:
            room.draw(canvas)
                        
        for chest in Chest_group:
            chest.draw(canvas)
        
        for rack in Weapon_rack_group:
            rack.draw(canvas)
            
        canvas.draw_polygon(grid_to_coord(self.exit),1,'green','green')
        
        for Monster in Monster_group:
            Monster.draw1(canvas)
        
        if Cheat_Mode == False:
            for grid in self.fog_of_war:
                canvas.draw_polygon(grid_to_coord(grid),1,'black','grey')		
        
        for Monster in Monster_group:
            Monster.draw2(canvas)

            
class Room(Map):
    def __init__(self,corner1,corner2,corner3,corner4):
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.corner4 = corner4
        self.room_area = list()
        for j in range(corner1[0], corner4[0]+1):
            for i in range(corner1[1], corner2[1]+1):
                self.room_area.append((j,i))
        self.center = determine_center(self.corner1,self.corner3)
        
        self.corridor_area = list()
        
    def __str__(self):
        return 'The room is' + str(self.corner1) + '' + str(self.corner2) + '' + str(self.corner3) + ''+ str(self.corner4)

    def get_area(self):
        return self.room_area
    
    def get_corners(self):
        return self.corner1,self.corner2,self.corner3,self.corner4
    
    def get_center(self):
        return self.center
    
    def update_type_of_terrain(self):
        global type_of_terrain
        for grid in self.room_area:
            type_of_terrain[grid] = ROOM
        for grid in self.corridor_area:
            type_of_terrain[grid] = CORRIDOR
                
    def intersect(self,room2): 
        corners = room2.get_corners()
        top_left = corners[0]
        bottom_right = corners[2]
        if self.corner1[1] > bottom_right[1] or self.corner3[1] < top_left[1] or self.corner1[0] > bottom_right[0] or self.corner3[0] < top_left[0]:
            overlap = False
        else: 
            overlap = True
        return overlap
                   
    def connect_rooms(self,Room2):
        center2 = Room2.get_center()
        x_dist = center2[1] - self.center[1]
        y_dist = center2[0] - self.center[0]
        
        if x_dist > 0 and y_dist > 0: 
            for i in range(x_dist):
                self.corridor_area.append((self.center[0] ,(self.center[1]+i)))
            for i in range(y_dist):
                self.corridor_area.append((self.center[0]+ i,(self.center[1]+x_dist)))
                
        elif x_dist < 0 and y_dist > 0: 
            for i in range(abs(x_dist)):
                self.corridor_area.append((self.center[0] ,(self.center[1]-i)))
            for i in range(y_dist):
                self.corridor_area.append((self.center[0]+ i,(self.center[1]+x_dist)))
                                
        elif x_dist > 0 and y_dist < 0: 
            for i in range(x_dist):
                self.corridor_area.append((self.center[0] ,(self.center[1]+i)))
            for i in range(abs(y_dist)):
                self.corridor_area.append((self.center[0]- i,(self.center[1]+ x_dist)))
                
        elif x_dist < 0 and y_dist < 0:
            for i in range(abs(x_dist)):
                self.corridor_area.append((self.center[0] ,(self.center[1]-i)))
            for i in range(abs(y_dist)):
                self.corridor_area.append((self.center[0]- i,(self.center[1] + x_dist)))
        return self.corridor_area  
        
    def draw(self,canvas):
        for grid in self.room_area:
            canvas.draw_polygon(grid_to_coord(grid),1,'black','white')
        for grid in self.corridor_area:
            canvas.draw_polygon(grid_to_coord(grid),1,'black','white')
            
class character(Map):
    def __init__(self,grid):
        self.pos = [grid[0],grid[1]]
        self.hp_max = 100
        self.stam_max = 100
        self.hp = self.hp_max
        self.stam = self.hp_max
        self.item = []
        self.attack = 7
        self.defense = 5
        self.poison_counter_max = 10
        self.poison_counter = 0
        self.timer = simplegui.create_timer(250, self.Timer_counter)
        self.timer_counter = 0
        self.update_fog_of_war()
        self.PICK_UP = False
        self.INVENTORY_FULL = False
        self.ALREADY_OWN = False
        #This stores the item in terms of a number instead of the name so that the coding is easier
        #e.g. Teleport Scroll will be stord as "1", Illumination Scroll as "2", etc
                
    def get_pos(self):
        return self.pos
    
    def get_item(self):
        return self.item
        
    def change_pos(self,pos):
        self.pos = pos
        
    def move_up(self):
        global Monster_group,GAME_OVER
        pos_of_monster = []
        for monster in Monster_group:
            pos_of_monster.append(monster.get_pos() == (self.pos[0]-1, self.pos[1]))
        if any(pos_of_monster) == False: 
            if (self.pos[0]-1,self.pos[1]) in type_of_terrain and self.pos[0] > 0 and type_of_terrain[(self.pos[0]-1,self.pos[1])]:
                self.pos[0] -= 1
                if self.poison_counter > 0:
                    self.hp -= 1
                    self.poison_counter -= 1
                for i in range(len(Monster_group)):
                    Monster_group[i].update_monster_position(Monster_group[i].get_pos(),(self.pos[0], self.pos[1]))
                if self.stam > 0:
                    self.stam -= 1
                elif self.stam <= 0:
                    self.hp -= 1
                if self.hp <=0:
                    GAME_OVER = True
                self.update_fog_of_war()
                if (self.pos[0], self.pos[1]) == Map_group[counter].exit:
                    Map_group[counter].regenerate()
        
        else:            
            monster_near_by = []
            other_monster = list(Monster_group)
            monster_to_remove = []
            for monster in Monster_group:
                if monster.get_pos() == (self.pos[0]-1, self.pos[1]):
                    monster_near_by.append(monster)
                
            for monster in monster_near_by:
                monster.Attack()
                monster.being_attacked = False
                monster.being_attacked = True
                if self.attack > monster.defense:
                    monster.hp -= (self.attack - monster.defense)
                else:
                    monster.hp -= 1
                if monster.hp <= 0:
                    monster_to_remove.append(monster)
            
            for monster in monster_to_remove:
                Monster_group.remove(monster)
            
            for monster in monster_near_by:
                other_monster.remove(monster)            
           
            for i in range(len(other_monster)):                
                other_monster[i].update_monster_position(other_monster[i].get_pos(),(self.pos[0], self.pos[1]))
            if self.stam > 0:
                self.stam -= 1
            elif self.stam == 0:
                self.hp -= 1
            if self.hp <= 0:
                GAME_OVER = True

    def move_down(self):
        global Monster_group,GAME_OVER
        pos_of_monster = []
        for monster in Monster_group:
            pos_of_monster.append(monster.get_pos() == (self.pos[0]+1, self.pos[1]))
        if any(pos_of_monster) == False: 
            if self.poison_counter > 0:
                self.hp -= 1
                self.poison_counter -= 1
            if (self.pos[0]+1,self.pos[1]) in type_of_terrain and self.pos[0] < GRID_WIDTH and type_of_terrain[(self.pos[0]+1,self.pos[1])]:
                self.pos[0] += 1
                for i in range(len(Monster_group)):
                    Monster_group[i].update_monster_position(Monster_group[i].get_pos(),(self.pos[0], self.pos[1]))
                if self.stam > 0:
                    self.stam -= 1
                elif self.stam <= 0:
                    self.hp -= 1
                if self.hp <= 0:
                    GAME_OVER = True
                        
                self.update_fog_of_war()
                if (self.pos[0], self.pos[1]) == Map_group[counter].exit:
                    Map_group[counter].regenerate()
        else:                                         
            monster_near_by = []
            other_monster = list(Monster_group)
            for monster in Monster_group:
                if monster.get_pos() == (self.pos[0]+1, self.pos[1]):
                    monster_near_by.append(monster)
                
            for monster in monster_near_by: 
                monster.Attack()
                monster.being_attacked = False
                monster.being_attacked = True
                if self.attack > monster.defense:
                    monster.hp -= (self.attack - monster.defense)
                else:
                    monster.hp -= 1
                if monster.hp <= 0:
                    Monster_group.remove(monster)
                    
            for monster in monster_near_by:
                other_monster.remove(monster) 
            
            for i in range(len(other_monster)):
                other_monster[i].update_monster_position(other_monster[i].get_pos(),(self.pos[0], self.pos[1]))
            if self.stam > 0:
                self.stam -= 1
            elif self.stam == 0:
                self.hp -= 1
            if self.hp <= 0:
                GAME_OVER = True
                                    
    def move_left(self):
        global Monster_group,GAME_OVER
        pos_of_monster = []
        for monster in Monster_group:
            pos_of_monster.append(monster.get_pos() == (self.pos[0], self.pos[1] - 1))
        if any(pos_of_monster) == False: 
            if self.poison_counter > 0:
                self.hp -= 1
                self.poison_counter -= 1            
            if (self.pos[0],self.pos[1]-1) in type_of_terrain and self.pos[1] < GRID_WIDTH and type_of_terrain[(self.pos[0],self.pos[1]-1)]:
                self.pos[1] -= 1
                for i in range(len(Monster_group)):
                    Monster_group[i].update_monster_position(Monster_group[i].get_pos(),(self.pos[0], self.pos[1]))
                if self.stam > 0:
                    self.stam -= 1
                elif self.stam <= 0:
                    self.hp -= 1
                if self.hp <= 0:
                    GAME_OVER = True
                self.update_fog_of_war()
                if (self.pos[0], self.pos[1]) == Map_group[counter].exit:
                    Map_group[counter].regenerate()
        else:                                         
            monster_near_by = []
            other_monster = list(Monster_group)
            for monster in Monster_group:
                if monster.get_pos() == (self.pos[0], self.pos[1]- 1):
                    monster_near_by.append(monster)
                    
            for monster in monster_near_by: 
                monster.Attack()
                monster.being_attacked = False
                monster.being_attacked = True
                if self.attack > monster.defense:
                    monster.hp -= (self.attack - monster.defense)
                else:
                    monster.hp -= 1              
                if monster.hp <= 0:
                    Monster_group.remove(monster)
                    
            for monster in monster_near_by:
                other_monster.remove(monster) 
            
            for i in range(len(other_monster)):
                other_monster[i].update_monster_position(other_monster[i].get_pos(),(self.pos[0], self.pos[1]))
            if self.stam > 0:
                self.stam -= 1
            elif self.stam == 0:
                self.hp -= 1
            if self.hp <= 0:
                GAME_OVER = True

    def move_right(self):
        global Monster_group,GAME_OVER
        pos_of_monster = []
        for monster in Monster_group:
            pos_of_monster.append(monster.get_pos() == (self.pos[0], self.pos[1] + 1))
        if any(pos_of_monster) == False:
            if self.poison_counter > 0:
                self.hp -= 1
                self.poison_counter -= 1
            if (self.pos[0],self.pos[1]+1) in type_of_terrain and self.pos[1] < GRID_WIDTH and type_of_terrain[(self.pos[0],self.pos[1]+1)]:
                self.pos[1] += 1
                for i in range(len(Monster_group)):
                    Monster_group[i].update_monster_position(Monster_group[i].get_pos(),(self.pos[0], self.pos[1]))
                if self.stam > 0:
                    self.stam -= 1
                elif self.stam <= 0:
                    self.hp -= 1
                if self.hp <= 0:
                    GAME_OVER = True
                self.update_fog_of_war()
                if (self.pos[0], self.pos[1]) == Map_group[counter].exit:
                    Map_group[counter].regenerate()
        else:                                         
            monster_near_by = []
            other_monster = list(Monster_group)
            for monster in Monster_group:
                if monster.get_pos() == (self.pos[0], self.pos[1]+ 1):
                    monster_near_by.append(monster)
                
            for monster in monster_near_by:
                monster.Attack()
                monster.being_attacked = False
                monster.being_attacked = True
                if self.attack > monster.defense:
                    monster.hp -= (self.attack - monster.defense)
                else:
                    monster.hp -= 1
                if monster.hp <= 0:
                    Monster_group.remove(monster)
            
            for monster in monster_near_by:
                other_monster.remove(monster) 
            
            for i in range(len(other_monster)):
                other_monster[i].update_monster_position(other_monster[i].get_pos(),(self.pos[0], self.pos[1]))
            if self.stam > 0:
                self.stam -= 1
            elif self.stam == 0:
                self.hp -= 1
            if self.hp <= 0:
                GAME_OVER = True
                                
    def rest(self):
        global GAME_OVER
        if self.hp <= 0:
            GAME_OVER = True
        if self.stam <= self.stam_max - 15:
            self.stam += 15
        else: 
            self.stam += (self.stam_max - self.stam)
        for i in range(len(Monster_group)):
            Monster_group[i].update_monster_position(Monster_group[i].get_pos(),(self.pos[0], self.pos[1]))
    
    def pick_up(self):
        global picked_up, PICK_UP, INVENTORY_FULL,already_own
        if len(list(set(self.item))) < 5: 
            if type_of_terrain[(self.pos[0],self.pos[1])] == ITEM and Chest_group[0].get_item() != []:
                picked_up = []
                for item in Chest_group[0].get_item():
                    self.item.append(item)
                    if item == 1:
                        picked_up.append('Teleport Potion')
                    elif item == 2:
                        picked_up.append('Illumination Potion')
                    elif item == 3:
                        picked_up.append('Healing Potion')
                    elif item == 4:
                        picked_up.append('Destruction Potion')                        
                Chest_group[0].clear()
                self.PICK_UP = False
                self.PICK_UP = True
                                                
            elif type_of_terrain[(self.pos[0],self.pos[1])] == WEAPON and Weapon_rack_group[0].get_item() != []:
                picked_up = []
                already_own = []
                for item in Weapon_rack_group[0].get_item():
                    if item not in self.item:
                        self.item.append(item)
                        if item == 5:
                            picked_up.append('Shield')
                        elif item == 6:
                            picked_up.append('Sword')
                        elif item == 7:
                            picked_up.append('Torch')
                        elif item == 8:
                            picked_up.append('Amulet of Stamina ')
                        elif item == 9: 
                            picked_up.append('Amulet of Health')                        
                        Weapon_rack_group[0].clear()
                        self.PICK_UP = False
                        self.PICK_UP = True
                    else:
                        if item == 5:
                            already_own.append('Shield')
                        elif item == 6:
                            already_own.append('Sword')
                        elif item == 7:
                            already_own.append('Torch')
                        elif item == 8:
                            already_own.append('Amulet of Stamina ')
                        elif item == 9: 
                            already_own.append('Amulet of Health') 
                        self.ALREADY_OWN = True
                        
        elif len(list(set(self.item))) == 5:
            if type_of_terrain[(self.pos[0],self.pos[1])] == ITEM and len(Chest_group[0].get_item()) == 2:
                picked_up = []
                for item in Chest_group[0].get_item():
                    self.item.append(item)
                    if item == 1:
                        picked_up.append('Teleport Potion')
                    elif item == 2:
                        picked_up.append('Illumination Potion')
                    elif item == 3:
                        picked_up.append('Healing Potion')
                    elif item == 4:
                        picked_up.append('Destruction Potion')       
                Chest_group[0].clear()
                self.PICK_UP = False
                self.PICK_UP = True
                
            elif type_of_terrain[(self.pos[0],self.pos[1])] == ITEM and len(Chest_group[0].get_item()) == 3:
                picked_up = []
                for _ in range(2):
                    item_to_added = []
                    for item in Chest_group[0].get_item():
                        item_to_added.append(item)                        
                    item_added = random.choice(item_to_added)
                    if item_added == 1:
                        picked_up.append('Teleport Potion')
                    elif item_added == 2:
                        picked_up.append('Illumination Potion')
                    elif item_added == 3:
                        picked_up.append('Healing Potion')
                    elif item_added == 4:
                        picked_up.append('Destruction Potion')   
                    self.item.append(item_added)
                    Chest_group[0].remove(item_added)
                    self.PICK_UP = False
                    self.PICK_UP = True
                if len(list(set(self.item))) == 7:
                    self.INVENTORY_FULL = True
                else:
                    self.INVENTORY_FULL = False
                    
            elif type_of_terrain[(self.pos[0],self.pos[1])] == WEAPON and Weapon_rack_group[0].get_item() != []:
                picked_up = []
                already_own = []
                for item in Weapon_rack_group[0].get_item():
                    if item not in self.item:
                        self.item.append(item)
                        if item == 5:
                            picked_up.append('Shield')
                        elif item == 6:
                            picked_up.append('Sword')
                        elif item == 7:
                            picked_up.append('Torch')
                        elif item == 8:
                            picked_up.append('Amulet of Stamina ')
                        elif item == 9: 
                            picked_up.append('Amulet of Health')     
                        Weapon_rack_group[0].clear()
                        self.PICK_UP = False
                        self.PICK_UP = True
                    else:
                        if item == 5:
                            already_own.append('Shield')
                        elif item == 6:
                            already_own.append('Sword')
                        elif item == 7:
                            already_own.append('Torch')
                        elif item == 8:
                            already_own.append('Amulet of Stamina ')
                        elif item == 9: 
                            already_own.append('Amulet of Health') 
                        self.ALREADY_OWN = True

        elif len(list(set(self.item))) == 6:
            if type_of_terrain[(self.pos[0],self.pos[1])] == ITEM and Chest_group[0].get_item() != []:
                picked_up = []
                item_to_add = []
                for item in Chest_group[0].get_item():
                    item_to_add.append(item)
                item_added = random.choice(item_to_add)
                if item_added == 1:
                    picked_up.append('Teleport Potion')
                elif item_added == 2:
                    picked_up.append('Illumination Potion')
                elif item_added == 3:
                    picked_up.append('Healing Potion')
                elif item_added == 4:
                    picked_up.append('Destruction Potion')  
                self.item.append(item_added)
                Chest_group[0].remove(item_added)
                self.PICK_UP = False
                self.PICK_UP = True
                if len(list(set(self.item))) == 7:
                    self.INVENTORY_FULL = True
                
            elif type_of_terrain[(self.pos[0],self.pos[1])] == WEAPON and Weapon_rack_group[0].get_item() != []:
                picked_up = []
                already_own = []
                for item in Weapon_rack_group[0].get_item():
                    if item not in self.item:
                        self.item.append(item)
                        if item == 5:
                            picked_up.append('Shield')
                        elif item == 6:
                            picked_up.append('Sword')
                        elif item == 7:
                            picked_up.append('Torch')
                        elif item == 8:
                            picked_up.append('Amulet of Stamina ')
                        elif item == 9: 
                            picked_up.append('Amulet of Health')     
                        Weapon_rack_group[0].clear()
                        self.PICK_UP = False
                        self.PICK_UP = True
                    else:
                        if item == 5:
                            already_own.append('Shield')
                        elif item == 6:
                            already_own.append('Sword')
                        elif item == 7:
                            already_own.append('Torch')
                        elif item == 8:
                            already_own.append('Amulet of Stamina ')
                        elif item == 9: 
                            already_own.append('Amulet of Health') 
                        self.ALREADY_OWN = True
                        
        elif len(list(set(self.item))) == 7:
            if type_of_terrain[(self.pos[0],self.pos[1])] == ITEM and Chest_group[0].get_item() != []:
                picked_up = []
                item_to_clear = []
                for item in Chest_group[0].get_item():
                    if item in self.item:
                        self.item.append(item)
                        if item == 1:
                            picked_up.append('Teleport Potion')
                        elif item == 2:
                            picked_up.append('Illumination Potion')
                        elif item == 3:
                            picked_up.append('Healing Potion')
                        elif item == 4:
                            picked_up.append('Destruction Potion')  
                        item_to_clear.append(item)
                for item in item_to_clear:
                    Chest_group[0].remove(item)
                self.PICK_UP = False
                self.PICK_UP = True
                self.INVENTORY_FULL = True
            elif type_of_terrain[(self.pos[0],self.pos[1])] == WEAPON and Weapon_rack_group[0].get_item() != []:
                picked_up = []
                self.INVENTORY_FULL = True
            
                      
    def check_weapon(self):
        global sword_wielding, shield_wielding, torch_wielding, amulet_of_stamina, amulet_of_health
        
        if 5 in self.item:
            if shield_wielding == False:
                shield_wielding = True
                self.defense += 3
                
        if 6 in self.item:
            if sword_wielding == False:
                sword_wielding = True
                self.attack += 6
        
        if 7 in self.item:
            if torch_wielding == False:
                torch_wielding = True
        
        if 8 in self.item:
            if amulet_of_stamina == False:
                amulet_of_stamina = True               
                self.stam_max += 30
                self.stam += 30
            
        if 9 in self.item:
            if amulet_of_health == False:
                amulet_of_health = True
                self.hp_max += 50
                self.hp += 50
                                        
    def update_fog_of_war(self):        
        if torch_wielding == False:
            grid_to_remove = []
            for j in range(3):
                for i in range(3):
                    grid_to_remove.append((self.pos[0]+ j,self.pos[1]+ i))
                    grid_to_remove.append((self.pos[0]- j,self.pos[1]+ i))
                    grid_to_remove.append((self.pos[0]+ j,self.pos[1]- i))
                    grid_to_remove.append((self.pos[0]- j,self.pos[1]- i))

            for grid in grid_to_remove:
                if grid in Map_group[counter].fog_of_war:
                    Map_group[counter].fog_of_war.remove(grid)        
        else: 
            grid_to_remove = []
            for j in range(5):
                for i in range(5):
                    grid_to_remove.append((self.pos[0]+ j,self.pos[1]+ i))
                    grid_to_remove.append((self.pos[0]- j,self.pos[1]+ i))
                    grid_to_remove.append((self.pos[0]+ j,self.pos[1]- i))
                    grid_to_remove.append((self.pos[0]- j,self.pos[1]- i))

            for grid in grid_to_remove:
                if grid in Map_group[counter].fog_of_war:
                    Map_group[counter].fog_of_war.remove(grid)
        
    def Timer_counter(self):
        self.timer_counter += 1
        
    def draw(self,canvas):
        global PICK_UP, INVENTORY_FULL 
        canvas.draw_polygon(grid_to_coord(self.pos),1,'blue','blue')
        canvas.draw_text('HP: '+ str(self.hp),[920,100], 24,'red')
        canvas.draw_text('STA: '+ str(self.stam),[920,130], 24,'yellow')
        canvas.draw_text('ATTK: ' + str(self.attack), [920,160],24,'orange')
        canvas.draw_text('DEF: ' + str(self.defense),[920,190],24,'green')        
        canvas.draw_text('Inventory:', [920,220], 24, 'white')
        if self.stam <= 20: 
            canvas.draw_text('STA LOW!', [1025,135],24,'red')
        if self.poison_counter > 0:
            canvas.draw_text('POISONED', [1025,100],24,'red')
        if self.PICK_UP == True:
            self.timer.start()
            canvas.draw_polygon(([240,75],[650,75],[650,180],[240,180]),1,'blue','rgba(0, 0, 255, 0.75)')
            if self.timer_counter <= 10:
                for i in range(len(picked_up)):
                    canvas.draw_text('You Picked Up: ' + str(picked_up[i]),[250,100 + 30*i],24,'yellow')
            else:
                self.timer.stop()
                self.PICK_UP = False
                self.timer_counter = 0
        elif (self.PICK_UP == True and self.INVENTORY_FULL == True) or self.INVENTORY_FULL == True:
            self.timer.start()
            if self.timer_counter <= 10:
                if len(picked_up) != 0:
                    canvas.draw_polygon(([240,75],[650,75],[650,180],[240,180]),1,'blue','rgba(0, 0, 255, 0.75)')
                    for i in range(len(picked_up)):
                        canvas.draw_text('You Picked Up: ' + str(picked_up[i]),[250,100 + 30*i],24,'yellow')
                    canvas.draw_text('INVENTORY FULL', [250,170],24,'yellow')
                else:
                    canvas.draw_polygon(([240,75],[650,75],[650,150],[240,150]),1,'blue','rgba(0, 0, 255, 0.75)')
                    canvas.draw_text('INVENTORY FULL', [250,100],24,'yellow')
            else:
                self.timer.stop()
                self.PICK_UP = False
                self.INVENTORY_FULL = False
                self.timer_counter = 0                 
        
        if self.ALREADY_OWN == True:
            self.timer.start()
            if self.timer_counter <= 10:
                canvas.draw_polygon(([240,75],[650,75],[650,150],[240,150]),1,'blue','rgba(0, 0, 255, 0.75)')
                canvas.draw_text('You already have ' + str(already_own[0]), [250,100],24,'yellow')
            else:
                self.timer.stop()
                self.ALREADY_OWN = False
                self.timer_counter = 0               
        self.check_weapon()
                
class Monster:
    def __init__(self,grid):
        self.pos = [grid[0],grid[1]]
        self.hp = int(8 + counter/3)
        self.attack = int(6 + counter/3)
        self.defense = int(2 + counter/2)
        self.being_attacked = False
        self.timer_counter = 0
        self.timer = simplegui.create_timer(100, self.Timer_counter)
               
    def get_pos(self):
        return (self.pos[0],self.pos[1])
    
    #BFS to track the player down                              
    def update_monster_position(self,start,end):
        path = search_for_the_player(start,end)
        if len(path) > 1:
            self.pos = path[1]
        elif len(path) == 1:
            self.pos = path[0]
            self.Attack()
    
    def Timer_counter(self):
        self.timer_counter += 1
    
    def Attack(self):
        global GAME_OVER
        if My_adventurer.defense <= self.attack:
            My_adventurer.hp -= self.attack - My_adventurer.defense        
            if My_adventurer.hp <= 0:
                GAME_OVER == True
            
    def draw1(self,canvas):
        canvas.draw_polygon(grid_to_coord(self.pos),1,'red','red')        
    
    def draw2(self,canvas):
        if self.being_attacked == True: 
            self.timer.start()
            if self.timer_counter <= 12:
                if My_adventurer.attack > self.defense:
                    canvas.draw_text('-'+ str(My_adventurer.attack - self.defense),[grid_to_coord(self.pos)[0][0] + 2, grid_to_coord(self.pos)[0][1] + 15], 18,'blue')
                else:
                    canvas.draw_text('-1',[grid_to_coord(self.pos)[0][0] + 2, grid_to_coord(self.pos)[0][1] + 15], 18,'blue')
                canvas.draw_polygon(([240,75],[650,75],[650,150],[240,150]),1,'blue','rgba(0, 0, 255, 0.75)')
                if My_adventurer.attack - self.defense > 0:
                    canvas.draw_text('You dealt ' + str(My_adventurer.attack - self.defense) + ' damage to the monster', [250,100],24,'white')
                else:
                    canvas.draw_text('You dealt 1 damage to the monster', [250,100],24,'white')
                if self.attack >= My_adventurer.defense:                    
                    canvas.draw_text('The monster dealt ' + str(self.attack - My_adventurer.defense) + ' damage to you', [250,130],24,'white')
                else: 
                    canvas.draw_text('The monster dealt 0 damage to you', [250,130],24,'white')
            else:
                self.timer.stop()
                self.being_attacked = False
                self.timer_counter = 0
    
class poison_spider(Monster):
    def __init__(self, grid):
        self.pos = [grid[0],grid[1]]
        self.hp = 3 + counter
        self.attack = 2 + counter
        self.defense = 1 + counter
        self.being_attacked = False
        self.timer = simplegui.create_timer(100, self.Timer_counter)
        self.timer_counter = 0
     
    def Attack(self):
        global GAME_OVER
        if My_adventurer.poison_counter <= My_adventurer.poison_counter_max - 5:
            My_adventurer.poison_counter += 5
        elif My_adventurer.poison_counter > My_adventurer.poison_counter_max - 5:
            My_adventurer.poison_counter += My_adventurer.poison_counter_max - My_adventurer.poison_counter
        
        if My_adventurer.defense <= self.attack:
            My_adventurer.hp -= self.attack - My_adventurer.defense
            if My_adventurer.hp <= 0:
                GAME_OVER == True
    
    def Timer_counter(self):
        self.timer_counter += 1
    
    def draw1(self,canvas):
        canvas.draw_polygon(grid_to_coord(self.pos),1,'red','purple') 
        
    def draw2(self,canvas):
        if self.being_attacked == True: 
            self.timer.start()
            canvas.draw_polygon(([240,75],[825,75],[825,150],[240,150]),1,'blue','rgba(0, 0, 255, 0.75)')
            if self.timer_counter <= 12:
                if My_adventurer.attack - self.defense > 0:
                    canvas.draw_text('-'+ str(My_adventurer.attack - self.defense),[grid_to_coord(self.pos)[0][0] + 2, grid_to_coord(self.pos)[0][1] + 15], 18,'blue')
                else:
                    canvas.draw_text('-1',[grid_to_coord(self.pos)[0][0] + 2, grid_to_coord(self.pos)[0][1] + 15], 18,'blue')
                if My_adventurer.attack - self.defense > 0:
                    canvas.draw_text('You dealt ' + str(My_adventurer.attack - self.defense) + ' damage to the monster', [250,100],24,'white')
                else:
                    canvas.draw_text('You dealt 1 damage to the monster', [250,100],24,'white')
                if self.attack > My_adventurer.defense:
                    canvas.draw_text('The monster dealt ' + str(self.attack - My_adventurer.defense) + ' damage to you and poisoned you', [250,130],24,'white')
                else: 
                    canvas.draw_text('The monster dealt 0 damage to you, but poisoned you', [250,130],24,'white')            
            else:
                self.timer.stop()
                self.being_attacked = False
                self.timer_counter = 0
                
class Chest:
    def __init__(self,pos):
        self.item = list()
        for i in range(random.choice([2,3])):
            self.item.append(random.choice([1,2,3,4]))
        self.pos = pos
        
    def get_pos(self):
        return self.pos
    
    def get_item(self):
        return self.item
    
    def remove(self,item):
        self.item.remove(item)
    
    def clear(self):
        self.item = []
    
    def draw(self,canvas):
        canvas.draw_polygon(grid_to_coord(self.pos),1,'yellow','yellow')

class weapon_rack(Chest):
    def __init__(self,pos):
        #For now:
        #5 == shield(My_adventurer.defense + 3)
        #6 == sword (My_adventurer.attack + 6)
        #7 == torch (bigger field of vision)
        #8 == amulet of stamina (My_adventurer.stam_max += 30)
        #9 == amulet of health (My_adventurer.hp_max += 30)
        self.item = list()
        self.item.append(random.choice([5,6,7,8,9])) 
        self.pos = pos
    
    def draw(self,canvas):
        canvas.draw_polygon(grid_to_coord(self.pos),1,'orange','orange')
        
#Teleport to a random location in the level
def Teleport_scroll():
    Potential_teleport_point = []
    for key in type_of_terrain:
        if type_of_terrain[key]:
            Potential_teleport_point.append(key)
    Point_to_teleport = random.choice(Potential_teleport_point)
    My_adventurer.change_pos([Point_to_teleport[0],Point_to_teleport[1]])
    My_adventurer.update_fog_of_war()
        
#Illuminate the current level 
def Illumination_scroll():
    Map_group[counter].fog_of_war = []

#Instantly Restore stamina
def Healing_scroll():
    if My_adventurer.hp <= My_adventurer.hp_max - 30:
        My_adventurer.hp += 30
        
    elif My_adventurer.hp >= My_adventurer.hp_max - 30:
        My_adventurer.hp += (My_adventurer.hp_max - My_adventurer.hp)
        
    if My_adventurer.poison_counter != 0:
        My_adventurer.poison_counter = 0   

        
def destruction_scroll():
    global Monster_group
    neighbors = [] 
    if My_adventurer.pos[0] > 0:
        neighbors.append((My_adventurer.pos[0]-1,My_adventurer.pos[1]))

    if My_adventurer.pos[0] < Map_group[counter].GRID_HEIGHT:
        neighbors.append((My_adventurer.pos[0]+1,My_adventurer.pos[1]))

    if My_adventurer.pos[1] > 0:
        neighbors.append((My_adventurer.pos[0],My_adventurer.pos[1]-1))

    if My_adventurer.pos[1] < Map_group[counter].GRID_WIDTH:
        neighbors.append((My_adventurer.pos[0],My_adventurer.pos[1]+1)) 

    if (My_adventurer.pos[0] > 0) and (My_adventurer.pos[1] > 0):
        neighbors.append((My_adventurer.pos[0]-1,My_adventurer.pos[1]-1))

    if (My_adventurer.pos[0] > 0) and (My_adventurer.pos[1] < Map_group[counter].GRID_WIDTH):
        neighbors.append((My_adventurer.pos[0]-1, My_adventurer.pos[1]+1))

    if (My_adventurer.pos[0] < Map_group[counter].GRID_HEIGHT) and (My_adventurer.pos[1] > 0):
        neighbors.append((My_adventurer.pos[0]+1,My_adventurer.pos[1]+1))

    if (My_adventurer.pos[0] < Map_group[counter].GRID_HEIGHT) and (My_adventurer.pos[1] < Map_group[counter].GRID_WIDTH):
        neighbors.append((My_adventurer.pos[0]+1,My_adventurer.pos[1]-1))   
    
    Monster_to_remove = []
    for monster in Monster_group:
        monster_pos = monster.get_pos()
        for neighbor in neighbors:
            if monster_pos == neighbor:
                monster.hp -= 1000
                if monster.hp <= 0:
                    Monster_to_remove.append(monster)
    
    for dead_monster in Monster_to_remove:
        Monster_group.remove(dead_monster)

#######################################Helper Functions##################################               
def grid_to_coord(grid_num):
    row = grid_num[0]
    col = grid_num[1]
    coord = []
    coord1 = (col*INDI_GRID_SIZE, (row)*INDI_GRID_SIZE)
    coord2 = ((col+1)*INDI_GRID_SIZE, (row)*INDI_GRID_SIZE)
    coord3 = ((col+1)*INDI_GRID_SIZE, (row+1)*INDI_GRID_SIZE)
    coord4 = (col*INDI_GRID_SIZE, (row+1)*INDI_GRID_SIZE)
    coord = [coord1, coord2,coord3,coord4]
    return coord

def determine_center(coord1,coord3):
    center = [0,0]
    center[0] = (coord3[0] - coord1[0])//2 + coord1[0]
    center[1] = (coord3[1] - coord1[1])//2 + coord1[1]
    return center
    
def neighbors(grid):
    neighbors = []
    if grid[0] > 0: 
        neighbors.append((grid[0]-1,grid[1]))
    if grid[0] < GRID_HEIGHT: 
        neighbors.append((grid[0]+1,grid[1]))
    if grid[1] > 0: 
        neighbors.append((grid[0],grid[1]-1))
    if grid[0] < GRID_WIDTH: 
        neighbors.append((grid[0],grid[1]+1))       
    return neighbors 

def search_for_the_player(start,end):
    explored = []
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            explored.append(node)
            for neighbor in neighbors(node):
                if (neighbor[0],neighbor[1]) in type_of_terrain and type_of_terrain[(neighbor[0],neighbor[1])]:
                    if neighbor == end:
                        new_path = list(path)
                        return new_path
                    else: 
                        new_path = list(path)
                        new_path.append(neighbor)
                        queue.append(new_path)

def spawn_monsters():
    Potential_spawn_point = []
    for key in type_of_terrain:
        if type_of_terrain[key] == 1:
            Potential_spawn_point.append(key)
    Monster_group.append(Monster(random.choice(Potential_spawn_point)))
        

def spawn_spiders():
    Potential_spawn_point = []
    for key in type_of_terrain:
        if type_of_terrain[key] == 1:
            Potential_spawn_point.append(key)       
    Monster_group.append(poison_spider(random.choice(Potential_spawn_point)))
    
def keydown(key):
    global Cheat_Mode  
    if key == simplegui.KEY_MAP['w']:
        My_adventurer.move_up()
        
    elif key == simplegui.KEY_MAP['s']:
        My_adventurer.move_down()
        
    elif key == simplegui.KEY_MAP['a']:
        My_adventurer.move_left()
        
    elif key == simplegui.KEY_MAP['d']:
        My_adventurer.move_right()
    
    elif key == simplegui.KEY_MAP['k']:  
        if Cheat_Mode == True:
            Cheat_Mode = False
        elif Cheat_Mode == False:    
            Cheat_Mode = True
            
    elif key == simplegui.KEY_MAP['space']:
        My_adventurer.rest()
    
    elif key == simplegui.KEY_MAP['z']:
        My_adventurer.pick_up()
        

def mouse_click(pos):
    global IN_PLAY, HELP, HIGH_SCORE, GAME_OVER, Monster_group, Map_group, Chest_group, high_score, \
        sword_wielding, shield_wielding, torch_wielding, amulet_of_stamina, amulet_of_health
    
    if GAME_OVER == True and HELP == False and HIGH_SCORE == False and IN_PLAY == True:
        pos_back_button = image_coord(Back_button_info.get_dest_center(), Back_button_info.get_dest_size())
        if pos[0] > pos_back_button[0][0] and pos[0] < pos_back_button[1][0] and pos[1] > pos_back_button[0][1] and pos[1]< pos_back_button[2][1]:
            GAME_OVER = False
            IN_PLAY = False
            HIGH_SCORE = False
            HELP = False
            if counter not in high_score:
                high_score.append(counter + 1)
            high_score = sorted(high_score)
            sound_track.stop()
            soundtrack.pause()
            soundtrack.rewind()
            
            
    elif IN_PLAY == False and HELP == False and HIGH_SCORE == False and GAME_OVER == False:
        pos_play_button = image_coord(Play_button_info.get_dest_center(), Play_button_info.get_dest_size())
        pos_help_button = image_coord(Help_button_info.get_dest_center(), Help_button_info.get_dest_size())
        pos_high_score_button = image_coord(High_score_button_info.get_dest_center(), High_score_button_info.get_dest_size())
        if pos[0] > pos_play_button[0][0] and pos[0] < pos_play_button[1][0] and pos[1] > pos_play_button[0][1] and pos[1]< pos_play_button[2][1]:
            IN_PLAY = True
            clear_all()
            start_game()
            sound_track.start()
        
            
        elif pos[0] > pos_help_button[0][0] and pos[0] < pos_help_button[1][0] and pos[1] > pos_help_button[0][1] and pos[1]< pos_help_button[2][1]:
            HELP = True
        elif pos[0] > pos_high_score_button[0][0] and pos[0] < pos_high_score_button[1][0] and pos[1] > pos_high_score_button[0][1] and pos[1]< pos_high_score_button[2][1]:
            HIGH_SCORE = True
    
    elif IN_PLAY == False and HELP == True and HIGH_SCORE == False and GAME_OVER == False:
        pos_back_button = image_coord(Back_button_info.get_dest_center(), Back_button_info.get_dest_size())
        if pos[0] > pos_back_button[0][0] and pos[0] < pos_back_button[1][0] and pos[1] > pos_back_button[0][1] and pos[1]< pos_back_button[2][1]:
            HELP = False
    
    elif IN_PLAY == False and HELP == False and HIGH_SCORE == True and GAME_OVER == False:
        pos_back_button = image_coord(Back_button_info.get_dest_center(), Back_button_info.get_dest_size())
        if pos[0] > pos_back_button[0][0] and pos[0] < pos_back_button[1][0] and pos[1] > pos_back_button[0][1] and pos[1]< pos_back_button[2][1]:
            HIGH_SCORE = False
                                
    elif IN_PLAY == True and GAME_OVER == False and HELP == False and HIGH_SCORE == False:
        
        if 1 in My_adventurer.item: 
            box_to_draw1 = list(set(My_adventurer.item)).index(1)
        if 2 in My_adventurer.item:
            box_to_draw2 = list(set(My_adventurer.item)).index(2)
        if 3 in My_adventurer.item:
            box_to_draw3 = list(set(My_adventurer.item)).index(3)
        if 4 in My_adventurer.item:
            box_to_draw4 = list(set(My_adventurer.item)).index(4)
        if 5 in My_adventurer.item:
            box_to_draw5 = list(set(My_adventurer.item)).index(5)                
        if 6 in My_adventurer.item:
            box_to_draw6 = list(set(My_adventurer.item)).index(6)        
        if 7 in My_adventurer.item:
            box_to_draw7 = list(set(My_adventurer.item)).index(7)        
        if 8 in My_adventurer.item:
            box_to_draw8 = list(set(My_adventurer.item)).index(8)        
        if 9 in My_adventurer.item:
            box_to_draw9 = list(set(My_adventurer.item)).index(9)
        
        #Teleport Scroll
        if 1 in My_adventurer.item:             
            if pos[0] > box_for_inventory[box_to_draw1][0][0] and pos[0]< box_for_inventory[box_to_draw1][1][0]\
            and pos[1] > box_for_inventory[box_to_draw1][0][1] and pos[1] < box_for_inventory[box_to_draw1][2][1]: 
                Teleport_scroll()
                My_adventurer.item.remove(1)
            elif pos[0] > box_for_inventory[box_to_draw1][0][0] and pos[0]< box_for_inventory[box_to_draw1][0][0] + 70\
            and pos[1] > box_for_inventory[box_to_draw1][0][1] and pos[1] < box_for_inventory[box_to_draw1][2][1] - 20:
                My_adventurer.item.remove(1)
            
        #Illumination Scroll        
        if 2 in My_adventurer.item:        
            if pos[0] > box_for_inventory[box_to_draw2][0][0] and pos[0]< box_for_inventory[box_to_draw2][1][0]\
            and pos[1] > box_for_inventory[box_to_draw2][0][1] and pos[1] < box_for_inventory[box_to_draw2][2][1]:
                Illumination_scroll()
                My_adventurer.item.remove(2)
            elif pos[0] > box_for_inventory[box_to_draw2][0][0] and pos[0]< box_for_inventory[box_to_draw2][0][0] + 70\
            and pos[1] > box_for_inventory[box_to_draw2][0][1] and pos[1] < box_for_inventory[box_to_draw2][2][1] - 20:
                My_adventurer.item.remove(2)
                
        #Healing Scroll
        if 3 in My_adventurer.item:        
            if pos[0] > box_for_inventory[box_to_draw3][0][0] and pos[0]< box_for_inventory[box_to_draw3][1][0]\
            and pos[1] > box_for_inventory[box_to_draw3][0][1] and pos[1] < box_for_inventory[box_to_draw3][2][1]:
                Healing_scroll()
                My_adventurer.item.remove(3)
            elif pos[0] > box_for_inventory[box_to_draw3][0][0] and pos[0]< box_for_inventory[box_to_draw3][0][0] + 70\
            and pos[1] > box_for_inventory[box_to_draw3][0][1] and pos[1] < box_for_inventory[box_to_draw3][2][1] - 20:
                My_adventurer.item.remove(3)
                
        #Destruction Scroll
        if 4 in My_adventurer.item:        
            if pos[0] > box_for_inventory[box_to_draw4][0][0] and pos[0]< box_for_inventory[box_to_draw4][1][0]\
            and pos[1] > box_for_inventory[box_to_draw4][0][1] and pos[1] < box_for_inventory[box_to_draw4][2][1]:
                destruction_scroll()
                My_adventurer.item.remove(4)
            elif pos[0] > box_for_inventory[box_to_draw4][0][0] and pos[0]< box_for_inventory[box_to_draw4][0][0] + 70\
            and pos[1] > box_for_inventory[box_to_draw4][0][1] and pos[1] < box_for_inventory[box_to_draw4][2][1] - 20:
                My_adventurer.item.remove(4)
        
        #Shield
        if 5 in My_adventurer.item:
            if pos[0] > box_for_inventory[box_to_draw5][0][0]+ 50 and pos[0]< box_for_inventory[box_to_draw5][0][0] + 70\
            and pos[1] > box_for_inventory[box_to_draw5][0][1] and pos[1] < box_for_inventory[box_to_draw5][2][1] - 20:
                My_adventurer.item.remove(5)
                shield_wielding = False
                My_adventurer.defense -= 3
        
        #Sword
        if 6 in My_adventurer.item:
            if pos[0] > box_for_inventory[box_to_draw6][0][0] + 50 and pos[0]< box_for_inventory[box_to_draw6][0][0] + 70\
            and pos[1] > box_for_inventory[box_to_draw6][0][1] and pos[1] < box_for_inventory[box_to_draw6][2][1] - 20:
                My_adventurer.item.remove(6)
                sword_wielding = False
                My_adventurer.attack -= 6
        
        #Torch        
        if 7 in My_adventurer.item:
            if pos[0] > box_for_inventory[box_to_draw7][0][0] + 50 and pos[0]< box_for_inventory[box_to_draw7][0][0] + 70\
            and pos[1] > box_for_inventory[box_to_draw7][0][1] and pos[1] < box_for_inventory[box_to_draw7][2][1] - 20:
                My_adventurer.item.remove(7)
                torch_wielding = False
        
        # Amulet of Stam         
        if 8 in My_adventurer.item:
            if pos[0] > box_for_inventory[box_to_draw8][0][0]+ 50 and pos[0]< box_for_inventory[box_to_draw8][0][0] + 70\
            and pos[1] > box_for_inventory[box_to_draw8][0][1] and pos[1] < box_for_inventory[box_to_draw8][2][1] - 20:
                My_adventurer.item.remove(8)
                amulet_of_stamina = False
                My_adventurer.stam_max -= 30
                if My_adventurer.stam >= 100:
                    My_adventurer.stam = 100
        
        # Amulet of Health
        if 9 in My_adventurer.item:
            if pos[0] > box_for_inventory[box_to_draw9][0][0] + 50 and pos[0]< box_for_inventory[box_to_draw9][0][0] + 70\
            and pos[1] > box_for_inventory[box_to_draw9][0][1] and pos[1] < box_for_inventory[box_to_draw9][2][1] - 20:
                My_adventurer.item.remove(9)
                amulet_of_health = False
                My_adventurer.hp_max -= 50
                if My_adventurer.hp >= 100:
                    My_adventurer.hp = 100
                
                
def draw(canvas):
    if IN_PLAY == True and HELP == False and HIGH_SCORE == False and GAME_OVER == True:
        canvas.draw_image(You_died1,You_died_info1.get_center(),You_died_info1.get_size(),
                          You_died_info1.get_dest_center(),You_died_info1.get_dest_size())
        canvas.draw_image(You_died2, You_died_info2.get_center(),You_died_info2.get_size(),
                          You_died_info2.get_dest_center(),You_died_info2.get_dest_size())       
        canvas.draw_image(Back_button, Back_button_info.get_center(), Back_button_info.get_size(),
                          Back_button_info.get_dest_center(), Back_button_info.get_dest_size())
        
        
    elif IN_PLAY == False and HELP == False and HIGH_SCORE == False and GAME_OVER == False:
        canvas.draw_image(Title_image,Title_image_info.get_center(),Title_image_info.get_size(),
                          Title_image_info.get_dest_center(),Title_image_info.get_dest_size())
        
        canvas.draw_image(Play_button,Play_button_info.get_center(),Play_button_info.get_size(),
                          Play_button_info.get_dest_center(),Play_button_info.get_dest_size())  
        
        canvas.draw_image(Help_button,Help_button_info.get_center(), Help_button_info.get_size(),
                          Help_button_info.get_dest_center(), Help_button_info.get_dest_size())
        
        canvas.draw_image(High_score_button, High_score_button_info.get_center(), High_score_button_info.get_size(),
                          High_score_button_info.get_dest_center(), High_score_button_info.get_dest_size())
        
    elif IN_PLAY == False and HELP == True and HIGH_SCORE == False and GAME_OVER == False:
        canvas.draw_image(Help_screen, Help_screen_info.get_center(), Help_screen_info.get_size(),
                          Help_screen_info.get_dest_center(), Help_screen_info.get_dest_size())
        canvas.draw_image(Back_button, Back_button_info.get_center(), Back_button_info.get_size(),
                          Back_button_info.get_dest_center(), Back_button_info.get_dest_size())
    
    elif IN_PLAY == False and HIGH_SCORE == True and HELP == False and GAME_OVER == False:
        

        canvas.draw_image(Back_button, Back_button_info.get_center(), Back_button_info.get_size(),
                          Back_button_info.get_dest_center(), Back_button_info.get_dest_size())    
        canvas.draw_image(High_score1, High_score_info1.get_center(),High_score_info1.get_size(),
                          High_score_info1.get_dest_center(), High_score_info1.get_dest_size())
        canvas.draw_image(High_score2, High_score_info2.get_center(),High_score_info2.get_size(),
                          High_score_info2.get_dest_center(), High_score_info2.get_dest_size())
        
        canvas.draw_image(ONE, One_info.get_center(), One_info.get_size(),
                          One_info.get_dest_center(), One_info.get_dest_size())
        
        if len(high_score)>=1:
            canvas.draw_text('Level: ' + str(high_score[-1]), (200,300), 44,'white', "monospace")
        
        canvas.draw_image(Two, Two_info.get_center(), Two_info.get_size(),
                          Two_info.get_dest_center(), Two_info.get_dest_size())
        
        if len(high_score)>=2:
            canvas.draw_text('Level: ' + str(high_score[-2]),(200,400),44,'white', "monospace")
        
        canvas.draw_image(Three, Three_info.get_center(),Three_info.get_size(),
                          Three_info.get_dest_center(), Three_info.get_dest_size())
        
        if len(high_score) >=3:
            canvas.draw_text('Level: ' + str(high_score[-3]),(200,500),44,'white', "monospace")
        
    elif IN_PLAY == True and GAME_OVER == False and HELP == False and GAME_OVER == False:         
        Map_group[counter].draw(canvas)
        My_adventurer.draw(canvas)
        for i in range(len(box_for_inventory)):
            canvas.draw_polygon(box_for_inventory[i],1,'white')
        canvas.draw_text('Level: ' + str(counter + 1), (920,65),24,'white')
        #Draw the items: 
        #Teleport Scroll
        if 1 in My_adventurer.get_item():        
            item_list = My_adventurer.get_item()
            box_to_draw1 = list(set(item_list)).index(1)
            canvas.draw_polygon(box_for_inventory[box_to_draw1],1,'white','green')
            canvas.draw_text('x ' + str(My_adventurer.get_item().count(1)),
                         [box_for_inventory[box_to_draw1][0][0]+ 70, box_for_inventory[box_to_draw1][1][1] + 40],24,'white')
            canvas.draw_text('Tele',[box_for_inventory[box_to_draw1][0][0] + 5, box_for_inventory[box_to_draw1][1][1] + 25], 16,'white')  
            canvas.draw_text('port',[box_for_inventory[box_to_draw1][0][0] + 5, box_for_inventory[box_to_draw1][1][1] + 38], 16,'white')  
            #Draw Discard Box
            canvas.draw_polygon([(box_for_inventory[box_to_draw1][0][0] + 70, box_for_inventory[box_to_draw1][0][1]),
                                box_for_inventory[box_to_draw1][1],  
                                (box_for_inventory[box_to_draw1][2][0], box_for_inventory[box_to_draw1][2][1] - 30),
                                (box_for_inventory[box_to_draw1][3][0] + 70,box_for_inventory[box_to_draw1][3][1] - 30)],1,'white','red')
            canvas.draw_text('X', (box_for_inventory[box_to_draw1][0][0] + 55, box_for_inventory[box_to_draw1][0][1] + 15), 16,'green')
            
        #Illumination Scroll
        if 2 in My_adventurer.get_item():        
            item_list = My_adventurer.get_item()
            box_to_draw2 = list(set(item_list)).index(2)
            canvas.draw_polygon(box_for_inventory[box_to_draw2],1,'white','green')
            canvas.draw_text('x ' + str(My_adventurer.get_item().count(2)),
                         [box_for_inventory[box_to_draw2][0][0]+ 70, box_for_inventory[box_to_draw2][1][1] + 40],24,'white')
            canvas.draw_text('Light',[box_for_inventory[box_to_draw2][0][0] + 5, box_for_inventory[box_to_draw2][1][1] + 30], 16,'white')
            canvas.draw_polygon([(box_for_inventory[box_to_draw2][0][0] + 70, box_for_inventory[box_to_draw2][0][1]),
                                box_for_inventory[box_to_draw2][1],  
                                (box_for_inventory[box_to_draw2][2][0], box_for_inventory[box_to_draw2][2][1] - 30),
                                (box_for_inventory[box_to_draw2][3][0] + 70,box_for_inventory[box_to_draw2][3][1] - 30)],1,'white','red')
            canvas.draw_text('X', (box_for_inventory[box_to_draw2][0][0] + 55, box_for_inventory[box_to_draw2][0][1] + 15), 16,'green')
                    
        #Healing Scroll
        if 3 in My_adventurer.get_item():        
            item_list = My_adventurer.get_item()
            box_to_draw3 = list(set(item_list)).index(3)
            canvas.draw_polygon(box_for_inventory[box_to_draw3],1,'white','green')
            canvas.draw_text('x ' + str(My_adventurer.get_item().count(3)),
                         [box_for_inventory[box_to_draw3][0][0]+ 70, box_for_inventory[box_to_draw3][1][1] + 40],24,'white')
            canvas.draw_text('Heal',[box_for_inventory[box_to_draw3][0][0] + 10, box_for_inventory[box_to_draw3][1][1] + 30], 18,'white')                       
            canvas.draw_polygon([(box_for_inventory[box_to_draw3][0][0] + 70, box_for_inventory[box_to_draw3][0][1]),
                                box_for_inventory[box_to_draw3][1],  
                                (box_for_inventory[box_to_draw3][2][0], box_for_inventory[box_to_draw3][2][1] - 30),
                                (box_for_inventory[box_to_draw3][3][0] + 70,box_for_inventory[box_to_draw3][3][1] - 30)],1,'white','red')
            canvas.draw_text('X', (box_for_inventory[box_to_draw3][0][0] + 55, box_for_inventory[box_to_draw3][0][1] + 15), 16,'green')
                  
        #Destruction Scroll
        if 4 in My_adventurer.get_item():        
            item_list = My_adventurer.get_item()
            box_to_draw4 = list(set(item_list)).index(4)
            canvas.draw_polygon(box_for_inventory[box_to_draw4],1,'white','green')
            canvas.draw_text('x ' + str(My_adventurer.get_item().count(4)),
                         [box_for_inventory[box_to_draw4][0][0]+ 70, box_for_inventory[box_to_draw4][1][1] + 40],24,'white')
            canvas.draw_text('Destruc',[box_for_inventory[box_to_draw4][0][0] + 1, box_for_inventory[box_to_draw4][1][1] + 25], 16,'white')
            canvas.draw_text('tion',[box_for_inventory[box_to_draw4][0][0] + 10, box_for_inventory[box_to_draw4][1][1] + 35], 16,'white')
            canvas.draw_polygon([(box_for_inventory[box_to_draw4][0][0] + 70, box_for_inventory[box_to_draw4][0][1]),
                                box_for_inventory[box_to_draw4][1],  
                                (box_for_inventory[box_to_draw4][2][0], box_for_inventory[box_to_draw4][2][1] - 30),
                                (box_for_inventory[box_to_draw4][3][0] + 70,box_for_inventory[box_to_draw4][3][1] - 30)],1,'white','red')
            canvas.draw_text('X', (box_for_inventory[box_to_draw4][0][0] + 55, box_for_inventory[box_to_draw4][0][1] + 15), 16,'green')
          
        #Sword
        if 5 in My_adventurer.get_item():
            item_list = My_adventurer.get_item()
            box_to_draw5 = list(set(item_list)).index(5)
            canvas.draw_polygon(box_for_inventory[box_to_draw5],1,'white','orange')
            canvas.draw_text('Shield',[box_for_inventory[box_to_draw5][0][0]+ 5, box_for_inventory[box_to_draw5][1][1] + 30], 18,'white')
            canvas.draw_polygon([(box_for_inventory[box_to_draw5][0][0] + 70, box_for_inventory[box_to_draw5][0][1]),
                                box_for_inventory[box_to_draw5][1],  
                                (box_for_inventory[box_to_draw5][2][0], box_for_inventory[box_to_draw5][2][1] - 30),
                                (box_for_inventory[box_to_draw5][3][0] + 70,box_for_inventory[box_to_draw5][3][1] - 30)],1,'white','red')            
            canvas.draw_text('X', (box_for_inventory[box_to_draw5][0][0] + 55, box_for_inventory[box_to_draw5][0][1] + 15), 16,'green')        
        
        #Shield       
        if 6 in My_adventurer.get_item():
            item_list = My_adventurer.get_item()
            box_to_draw6 = list(set(item_list)).index(6)
            canvas.draw_polygon(box_for_inventory[box_to_draw6],1,'white','orange')
            canvas.draw_text('Sword',[box_for_inventory[box_to_draw6][0][0]+ 5, box_for_inventory[box_to_draw6][1][1] + 30], 18,'white')
            canvas.draw_polygon([(box_for_inventory[box_to_draw6][0][0] + 70, box_for_inventory[box_to_draw6][0][1]),
                                box_for_inventory[box_to_draw6][1],  
                                (box_for_inventory[box_to_draw6][2][0], box_for_inventory[box_to_draw6][2][1] - 30),
                                (box_for_inventory[box_to_draw6][3][0] + 70,box_for_inventory[box_to_draw6][3][1] - 30)],1,'white','red')
            canvas.draw_text('X', (box_for_inventory[box_to_draw6][0][0] + 55, box_for_inventory[box_to_draw6][0][1] + 15), 16,'green')        

        #Torch
        if 7 in My_adventurer.get_item():
            item_list = My_adventurer.get_item()
            box_to_draw7 = list(set(item_list)).index(7)
            canvas.draw_polygon(box_for_inventory[box_to_draw7],1,'white','orange')
            canvas.draw_text('Torch',[box_for_inventory[box_to_draw7][0][0]+ 5, box_for_inventory[box_to_draw7][1][1] + 30], 18,'white')
            canvas.draw_polygon([(box_for_inventory[box_to_draw7][0][0] + 70, box_for_inventory[box_to_draw7][0][1]),
                                box_for_inventory[box_to_draw7][1],  
                                (box_for_inventory[box_to_draw7][2][0], box_for_inventory[box_to_draw7][2][1] - 30),
                                (box_for_inventory[box_to_draw7][3][0] + 70,box_for_inventory[box_to_draw7][3][1] - 30)],1,'white','red')            
            canvas.draw_text('X', (box_for_inventory[box_to_draw7][0][0] + 55, box_for_inventory[box_to_draw7][0][1] + 15), 16,'green')        
        
        #Amulet of Stamina
        if 8 in My_adventurer.get_item():
            item_list = My_adventurer.get_item()
            box_to_draw8 = list(set(item_list)).index(8)
            canvas.draw_polygon(box_for_inventory[box_to_draw8],1,'white','orange')
            canvas.draw_text('Amulet',[box_for_inventory[box_to_draw8][0][0]+ 2, box_for_inventory[box_to_draw8][1][1] + 20], 16,'white')
            canvas.draw_text('of Sta',[box_for_inventory[box_to_draw8][0][0]+ 2, box_for_inventory[box_to_draw8][1][1] + 40], 16,'white')
            canvas.draw_polygon([(box_for_inventory[box_to_draw8][0][0] + 70, box_for_inventory[box_to_draw8][0][1]),
                                box_for_inventory[box_to_draw8][1],  
                                (box_for_inventory[box_to_draw8][2][0], box_for_inventory[box_to_draw8][2][1] - 30),
                                (box_for_inventory[box_to_draw8][3][0] + 70,box_for_inventory[box_to_draw8][3][1] - 30)],1,'white','red')
            canvas.draw_text('X', (box_for_inventory[box_to_draw8][0][0] + 55, box_for_inventory[box_to_draw8][0][1] + 15), 16,'green')        
        
        if 9 in My_adventurer.get_item():
            item_list = My_adventurer.get_item()
            box_to_draw9 = list(set(item_list)).index(9)
            canvas.draw_polygon(box_for_inventory[box_to_draw9],1,'white','orange')
            canvas.draw_text('Amulet',[box_for_inventory[box_to_draw9][0][0]+ 2, box_for_inventory[box_to_draw9][1][1] + 20], 16,'white')
            canvas.draw_text('of Hp',[box_for_inventory[box_to_draw9][0][0]+ 2, box_for_inventory[box_to_draw9][1][1] + 40], 16,'white')
            canvas.draw_polygon([(box_for_inventory[box_to_draw9][0][0] + 70, box_for_inventory[box_to_draw9][0][1]),
                                box_for_inventory[box_to_draw9][1],  
                                (box_for_inventory[box_to_draw9][2][0], box_for_inventory[box_to_draw9][2][1] - 30),
                                (box_for_inventory[box_to_draw9][3][0] + 70,box_for_inventory[box_to_draw9][3][1] - 30)],1,'white','red')
            canvas.draw_text('X', (box_for_inventory[box_to_draw9][0][0] + 55, box_for_inventory[box_to_draw9][0][1] + 15), 16,'green')        
                    
def music():
    soundtrack.play()
                
def start_game():
    global Map_group, My_adventurer
    Map_group.append(Map(GRID_WIDTH,GRID_HEIGHT))
    Potential_spawn_points = []
    for key in type_of_terrain:
        Potential_spawn_points.append(key)
    My_adventurer = character(random.choice(Potential_spawn_points))
    Map_group[0].generate_room(My_adventurer.get_pos())
    Map_group[0].generate_exit()
    Map_group[0].generate_treasure_chest()
    Map_group[0].generate_weapon_rack()
    for i in range(Monster_Number):
        spawn_monsters()
    
def clear_all():
    global type_of_terrain, Monster_group, Map_group, Chest_group, Monster_Number, Weapon_rack_group, counter
    type_of_terrain = dict()
    Monster_group = list()
    Map_group = list()
    Monster_Number = 2
    Chest_group = list()
    Weapon_rack_group = list()
    counter = 0
    
############################################Initiate the Program###############################################    
frame = simplegui.create_frame('Rogue:Infinitum', CANVAS_WIDTH + 250, CANVAS_HEIGHT, 0)
frame.set_canvas_background('black')
frame.set_draw_handler(draw)  
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(mouse_click)
sound_track = simplegui.create_timer(10, music)
frame.start()
