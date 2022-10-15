"""
CSSE1001 Assignment 3
Semester 2, 2020
"""
__author__ = "{{Qifeng Zhong}} ({{46045465}})"
__email__ = "q.zhong1@uqconnect.edu.au"
__date__ = "30/10/2020"

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.simpledialog import askstring

GAME_LEVELS = {
    # dungeon layout: max moves allowed
    "game1.txt": 7,
    "game2.txt": 12,
    "game3.txt": 19,
}

COLOR_INFO = {
    "#": "Dark grey",
    "O": "Medium spring green",
    "M": "Orange",
    "K": "Yellow",
    "D": "Red"
}

TXT_INFO = {
    "O": "Ibis",
    "M": "Banana",
    "K": "Trash",
    "D": "Nest"
}

IMAGE_INFO = {
    "K": "key.gif",
    "D": "door.gif",
    "#": "wall.gif",
    "M": "moveIncrease.gif",
    "O": "player.gif",
    "E": "empty.gif"
}

KEY_INFO = {
    (0, 1): "w",
    (1, 0): "a",
    (1, 1): "s",
    (1, 2): "d"
}

DIRECTIONS = {
    "w": (-1, 0),
    "s": (1, 0),
    "d": (0, 1),
    "a": (0, -1)
}
PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
SPACE = " "
time = 0
TASK_ONE = "TASK_ONE"
TASK_TWO = "TASK_TWO"


class Entity:
    """
    An entity within the game
    """

    _id = "Entity"

    def __init__(self):
        """
        Something the player can interact with
        """
        self._collidable = True

    def get_id(self):
        """
        Get the id of the Entity class.
        :return: a string representing the id of the Entity class"""
        return self._id

    def set_collide(self, collidable):
        """
        Set the collide
        :param collidable: a boolean representing whether the Entity class is collidable.
        :return: True if the Entity class is collidable; False if the Entity class is not collidable
        """
        self._collidable = collidable

    def can_collide(self):
        """
        Return a boolean representing whether the Entity class is collidable.
        :return: a boolean representing whether the Entity class is collidable

        """
        return self._collidable

    def __str__(self):
        """
        Returns the description of the Entity class.
        :return: the description of the Entity class"""
        return f"{self.__class__.__name__}({self._id!r})"

    def __repr__(self):
        """
        Converts the Entity class into a form for the interpreter to read
        :return: s string representing the Entity class"""
        return str(self)


class Wall(Entity):
    """
    A special type of an Entity within the game, which can not be collided with.
    """

    _id = "#"

    def __init__(self):
        """
        Constructor of the Wall class.
        """
        super().__init__()
        self.set_collide(False)


class Item(Entity):
    """
    An abstract class, which is also a special type of an Entity within the game.
    """

    def on_hit(self, game):
        """
        This function raises the NotImplementedError.
        :param game: the GameLogic object
        :return: None
        """
        raise NotImplementedError


class Key(Item):
    """
    A special type of Item within the game which can be collided with.
    """

    _id = "K"

    def on_hit(self, game):
        """
        When the player takes the Key the Key should be added to
        the Player’s inventory. The Key should then be removed
        from the dungeon once it’s in the Player’s inventory.
        :param game: the GameLogic object
        :return: None
        """
        player = game.get_player()
        player.add_item(self)
        game.get_game_information().pop(player.get_position())


class MoveIncrease(Item):
    """
    MoveIncrease should be constructed with MoveIncrease(moves=5: int)
    where moves describe how many extra moves the Player will be granted
    when they collect this Item.
    """

    _id = "M"

    def __init__(self, moves=5):
        """
        Constructor of the MoveIncrease class.
        :param moves: the number of movement
        """
        super().__init__()
        self._moves = moves

    def on_hit(self, game):
        """
        When the player hits the MoveIncrease item the number of moves
        for the player increases and the M item is removed from the game.
        :param game: the GameLogic object
        :return: None
        """
        player = game.get_player()
        player.change_move_count(self._moves)
        game.get_game_information().pop(player.get_position())


class Door(Entity):
    """
    A special type of an Entity within the game which can be collided with.
    """
    _id = "D"

    def on_hit(self, game):
        """
        If the Player’s inventory contains a Key Entity then
        this method should set the ‘game over’ state to be True.
        :param game: the GameLogic object
        :return: None
        """
        player = game.get_player()
        for item in player.get_inventory():
            if item.get_id() == "K":
                game.set_win(True)
                return


class Player(Entity):
    """
     A special type of an Entity within the game representing the player.
    """

    _id = "O"

    def __init__(self, move_count):
        """
        Constructor of the Player class.
        :param move_count: the number represents how many
        moves a Player can have for the given dungeon
        """
        super().__init__()
        self._move_count = move_count
        self._inventory = []
        self._position = None

    def set_position(self, position):
        """
        Get the id of the Player class.
        :return: a string representing the id of the Player class
        """
        self._position = position

    def get_position(self):
        """
        Returns a tuple of ints representing the position of the Player
        :return: the position of the Player
        """
        return self._position

    def change_move_count(self, number):
        """
        Parameters:
            number (int): number to be added to move count
        """
        self._move_count += number

    def moves_remaining(self):
        """
        Returns an int representing how many moves the Player has
        left before they reach the maximum move count.
        :return: the number representing how many moves the Player
        has left before they reach the maximum move count.
        """
        return self._move_count

    def add_item(self, item):
        """
        Adds item (Item) to inventory
        :param item: the item to be added
        :return: None
        """
        self._inventory.append(item)

    def get_inventory(self):
        """
        Returns a list that represents the Player’s inventory.
        :return: a list that represents the Player’s inventory
        """
        return self._inventory


class AbstractGrid(tk.Canvas):
    """
    This class is a abstract class，inherit the class tk.Canvas
    """

    def __init__(self, master, rows, cols, width, height, **kwargs):
        """Constructor of the AbstractGrid class.
        Parameters:
            master (str): parent
            rows (int): The number of squares in the horizontal direction
            cols (int): The number of squares in the vertical direction
            width (int): The pixel width of the current master
            height (int): The pixel height of the current master
            kwargs: Key value parameter pass to parent
        """

        tk.Canvas.__init__(self, master, width=width, height=height, **kwargs)
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height

    def get_bbox(self, position):
        """ Returns a tuple containing  The corresponding pixel position of the current coordinate
            Convert coordinates to pixels, eg:(1,0) -> (0,100,100,100)
        :param position: (tuple): Current coordinate
        :return: tuple<int, int, int, int>: Returns the pixel position according to the current coordinate
        """
        w = (self.width // self.cols)
        h = (self.height // self.rows)
        x = position[1] * w
        y = position[0] * h
        x1 = position[1] * w + w
        y1 = position[0] * h + h
        return x, y, x1, y1

    def get_position_center(self, position):
        """ Returns the pixel center of the grid corresponding to the current coordinate according to the coordinates
            eg: (0,0) -> (50,50)
        :param position (tuple): current coordinate
        :return: tuple<int, int>: The corresponding grid center point, pixel coordinates
        """
        rect = self.get_bbox(position)
        center_x = (rect[0] + rect[2]) // 2
        center_y = (rect[1] + rect[3]) // 2
        return center_x, center_y

    def annotate_position(self, position, text):
        """
        Draw on the Canvas according to the given coordinates and text.
        If there is no text, return directly.
        :param position: given coordinates
               text: given text
        :return: None
        """
        if text == None:
            return
        center = self.get_position_center(position)
        self.create_text(center[0], center[1], text=text, tags=text)


class DungeonMap(AbstractGrid):
    """
    This is a game map class, inherit from AbstractGrid class
    """

    def __init__(self, master, size, width=600, **kwargs):
        """Constructor of the DungeonMap class

        :param master: parent
               size: The number of rows in the canvas and the rows and columns in the grid are same
               width: The width of the map, the width and height of the canvas are the same
        :return: None
        """
        AbstractGrid.__init__(self, master, size, size, width, width, **kwargs)

    def draw_grid(self, dungeon, player_position):
        """
        According to the given rectangle's coordinates data dictionary and player coordinates drawn on the canvas
        :param dungeon:  A dictionary of map,contain the coordinates of key, movementincrease,door, and wall.
        :param player_position: coordinate of player
        :return: None
        """
        for pos, entity in dungeon.items():
            rect = self.get_bbox(pos)
            self.create_rectangle(rect[0], rect[1], rect[2], rect[3], fill=COLOR_INFO[entity.get_id()])
            self.annotate_position(pos, TXT_INFO.get(entity.get_id()))
        person_rect = self.get_bbox(player_position)
        self.create_rectangle(person_rect[0], person_rect[1], person_rect[2], person_rect[3], fill=COLOR_INFO["O"])
        self.annotate_position(player_position, "Ibis")


class AdvancedDungeonMap(AbstractGrid):
    """
    This is a class in the form of pictures on the canvas.
    Show images of movementincrease, key, door, wall, player, empty
    """

    def __init__(self, master, size, width, **kwargs):
        """Constructor of the AdvancedDungeonMap class
        :param master: parent
        :param size: The number of rows in the canvas and the rows and columns in the grid are same
        :param width: The width of the map, the width and height of the canvas are the same
        :param kwargs: Key value parameter pass to parent
        """
        AbstractGrid.__init__(self, master, size, size, width, width, **kwargs)
        self.size = size
        self.width = width
        self.img_player = self.loadimg("images/player.gif")
        self.img_empty = self.loadimg("images/empty.gif")
        self.img_key = self.loadimg("images/keys.gif")
        self.img_m_increase = self.loadimg("images/moveIncrease.gif")
        self.img_door = self.loadimg("images/door.gif")
        self.img_wall = self.loadimg("images/wall.gif")

    def loadimg(self, filename):
        """
        method for loading pictures
        :param filename: The name of the picture
        :return: the picture
        """
        file = Image.open(filename)
        img_deal = file.resize((self.width // self.size, self.width // self.size), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image=img_deal)
        return img

    def get_ad_map(self):
        """
        Gets the center coordinates of all squares in the map
        :return: A list contain coordinates of all squares in the map
        """
        lst = []
        for width_x in range(self.size):
            for height_y in range(self.size):
                image_pos = (width_x, height_y)
                lst.append(image_pos)
                height_y += 1
            width_x += 1
        return lst

    def draw_grid(self, dungeon, player_position):  # key_pos,mv_in_pos,door_pos
        """
        According to the given position information,
        draw pictures of walls, movementincrease, key, door, people and empty on the canvas.
        :param dungeon: The coordinate information of key, movementincrease, door, walls in the map（dict）
        :param player_position: Coordinates of player
        :return: None
        """
        for pos in self.get_ad_map():
            self.create_image(self.get_position_center(pos), image=self.img_empty)
            if pos in dungeon.keys():
                if dungeon[pos].get_id() == "K":
                    self.create_image(self.get_position_center(pos), image=self.img_key)
                elif dungeon[pos].get_id() == "M":
                    self.create_image(self.get_position_center(pos), image=self.img_m_increase)
                elif dungeon[pos].get_id() == "D":
                    self.create_image(self.get_position_center(pos), image=self.img_door)
                else:
                    self.create_image(self.get_position_center(pos), image=self.img_wall)
        self.create_image(self.get_position_center(player_position),
                          image=self.img_player)


class KeyPad(AbstractGrid):
    """
        The class that show the keyboard
    """

    def __init__(self, master, width=200, height=100, **kwargs):
        """ Constructor of the AdvancedDungeonMap class

        :param master: parent
        :param width: The width of the keyboard
        :param height: The height of the keyboard
        :param kwargs: Key value parameter pass to parent
        """

        AbstractGrid.__init__(self, master, 2, 3, width, height, **kwargs)

    def draw_key(self, info):
        """
        Draw keyboard according to key coordinate information
        :param info: Keyboard coordinate information
        :return:
        """

        for pos, txt in info.items():
            rect = self.get_bbox(pos)
            self.create_rectangle(rect[0], rect[1], rect[2], rect[3], fill="Dark grey", tags=txt)
            self.annotate_position(pos, txt)


class GameLogic:
    """
        Game control class
    """

    def __init__(self, dungeon_name):
        """
        Constructor of the GameLogic class
        :param dungeon_name: name of game map
        """

        self._dungeon_name = dungeon_name
        self._dungeon = self.load_game()
        self._dungeon_size = len(self._dungeon)
        self._player = Player(GAME_LEVELS[dungeon_name])
        self._game_information = self.init_game_information()
        self.f = None
        self._win = False

    def load_game(self):
        """
        Create a 2D array of string representing the dungeon to display.
        Parameters:
            filename (str): A string representing the name of the level.
        Returns:
            (list<list<str>>): A 2D array of strings representing the
                dungeon.
        """
        dungeon_layout = []

        with open(self._dungeon_name, 'r') as file:
            file_contents = file.readlines()

        for i in range(len(file_contents)):
            line = file_contents[i].strip()
            row = []
            for j in range(len(file_contents)):
                row.append(line[j])
            dungeon_layout.append(row)
        return dungeon_layout

    def save_game(self, time):
        """
         Save a the dungeon represented by a 2D array and save the player's remaining steps and game time in game Archive.
         Parameters:
             filename (str): A string representing the name of the level.
         Returns: True
         """

        var_string = askstring(title="Create an archive",
                               prompt="Please enter the name of the archive：")
        if var_string == "" or var_string == None:
            tk.messagebox.showinfo(title="Tips", message="Please enter something ")
            return True
        play_pos = self._player.get_position()
        lst = []
        for i in range(self._dungeon_size):
            lst.append([])
            for j in range(self._dungeon_size):
                lst[i].append(" ")

        for key, item in self._game_information.items():
            x = key[0]
            y = key[1]
            lst[x][y] = item.get_id()
        lst[play_pos[0]][play_pos[1]] = "O"
        with open(var_string + ".txt", "w") as f:
            for item in lst:
                s = "".join(item)
                s += "\n"
                f.write(s)
            f.write("-------------\n")
            f.write("t-" + str(time) + "\n")
            f.write("s-" + str(self._player.moves_remaining()) + "\n")
        return True

    def file_load_game(self):
        """
         Create 2D array of string representing the dungeon and game information to display.
         If there are no steps and times in the archive, they are the initial values
         Parameters:
             filename (str): A string representing the name of the Game Archive.
         Returns:
             (lst<list<str>>): A 2D array of strings representing the
                 dungeon.
             step: Player's remaining steps in game Archive
             time: Game time in archive
             True:If there are no steps and times in the archive
         """

        game_txt = askstring(title="Load an archive",
                             prompt="Please enter the name of the archive：")
        if game_txt == None:
            return True

        try:
            with open(game_txt + ".txt", 'r') as self.f:
                tag = True
                lst = []

                step = 0
                time = 0
                lins = self.f.readlines()

                for item in lins:
                    if tag:
                        if item[0] == "-":
                            tag = False
                            continue
                        item = list(item)
                        del (item[-1])
                        lst.append(item)
                    else:
                        rLst = item.split("-")
                        if (rLst[0] == "s"):

                            step = int(rLst[1])
                        elif (rLst[0] == "t"):
                            time = int(rLst[1])
            self._dungeon = lst
            self._dungeon_size = len(self._dungeon)
            self._player = Player(step)
            self._game_information = self.init_game_information()
            self._win = False
            return lst, step, time
        except:
            tk.messagebox.showinfo(title="Archive does not exist", message="Archive does not exist")
        return True

    def get_positions(self, entity):
        """
        Get the corresponding coordinate information according to the entity
        :param entity: Entity object
        :return: Coordinate information of Entity in the map
        """

        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row, col))

        return positions

    def init_game_information(self):
        """
        Initialize game information, get player position, key position, door position, wall position, movementincrease position
        :return: a dictionary containing the position and the corresponding Entity
            eg: {
                    (0,0) : "Entity(Wall)"
                    (0,1) : "Entity(Wall)"
                }
        """

        player_pos = self.get_positions(PLAYER)[0]
        key_position = self.get_positions(KEY)[0]
        door_position = self.get_positions(DOOR)[0]
        wall_positions = self.get_positions(WALL)
        move_increase_positions = self.get_positions(MOVE_INCREASE)

        self._player.set_position(player_pos)

        information = {
            key_position: Key(),
            door_position: Door(),
        }

        for wall in wall_positions:
            information[wall] = Wall()

        for move_increase in move_increase_positions:
            information[move_increase] = MoveIncrease()

        return information

    def get_player(self):
        """
        Get the player of the game.
        :return: the player object
        """
        return self._player

    def get_entity(self, position):
        """
        Get the entity on the given position
        :param position: the position of the entity
        :return: the entity on the given position
        """
        return self._game_information.get(position)

    def get_entity_in_direction(self, direction):
        """
        Returns an Entity at a given position in the dungeon.
        :param direction: the given position
        :return: an Entity at a given position in the dungeon
        """
        new_position = self.new_position(direction)
        return self.get_entity(new_position)

    def get_game_information(self):
        """
        Get the information of the game.
        :return: the information of the game
        """
        return self._game_information

    def get_dungeon_size(self):
        """
        Get the size of the dungeon.
        :return: a number representing the size of the dungeon
        """
        return self._dungeon_size

    def move_player(self, direction):
        """ """
        new_pos = self.new_position(direction)
        self.get_player().set_position(new_pos)

    def collision_check(self, direction):
        """
        Returns True if a player can travel in the given direction, False otherwise
        :param direction: the given direction
        :return: True if a player can travel in the given direction; False otherwise
        """
        new_pos = self.new_position(direction)
        entity = self.get_entity(new_pos)
        if entity is not None and not entity.can_collide():
            return True

        return not (0 <= new_pos[0] < self._dungeon_size and 0 <= new_pos[1] < self._dungeon_size)

    def new_position(self, direction):
        """According to the direction given by the user, the corresponding new coordinates are obtained"""
        x, y = self.get_player().get_position()
        dx, dy = DIRECTIONS[direction]
        return x + dx, y + dy

    def check_game_over(self):
        """
        Return True if the game has been won and False otherwise.
        :return: True if the game has been won and False otherwise
        """
        return self.get_player().moves_remaining() <= 0

    def set_win(self, win):
        """
        Set the status of the game
        :param win: the status of the game
        :return: None
        """
        self._win = win

    def won(self):
        """
        Get the status of the game
        :return: the status of the game
        """
        return self._win


class Image_text(tk.Frame):
    """
        Encapsulate a common weight and use it on the Statusbar，
        A weight Contains a picture and two line text
    """

    def __init__(self, mast, img_name, top_txt, buttom_txt):
        """
        Constructor of the Image_text class
        :param mast: parent
        :param img_name: name of picture
        :param top_txt: text on the top
        :param buttom_txt: text on the bottom
        """
        tk.Frame.__init__(self, mast)
        self.img = Image.open(img_name)
        self.img = self.img.resize((40, 60), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image=self.img)
        image_label = tk.Label(self, image=self.img)
        image_label.pack(side=tk.LEFT)
        self.f = tk.Frame(self)
        self.t_txt = tk.Label(self.f, text=top_txt)
        self.t_txt.pack(side=tk.TOP)
        self.b_txt = tk.Label(self.f, text=buttom_txt)
        self.b_txt.pack()
        self.f.pack(side=tk.LEFT)


class StatusBar(tk.Frame):
    """
        A weight of game state weight, including the remaining game steps, game time, and button can restart the game and exit.
    """

    def __init__(self, master, width, height, gameapp, **kwargs):
        """
        Constructor of the StatusBar class
        :param master: parent
        :param width: The width of weight
        :param height: The height of weight
        :param gameapp: Game control class
        :param kwargs: Key value parameter pass to parent
        """

        tk.Frame.__init__(self, master, width=width, height=height, **kwargs)
        self.gameapp = gameapp
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.LEFT, ipadx=80, ipady=5)
        self.button_new = tk.Button(self.button_frame, text="new game", command=self.new_game_func)
        self.button_new.pack(side=tk.TOP, expand=True)
        self.button_quit = tk.Button(self.button_frame, text="quit", command=self.ask_game_func)
        self.button_quit.pack(side=tk.BOTTOM, expand=True)
        self.timer = Image_text(self, "images/clock.gif", "Time elapsed", "0m0s")
        self.timer.pack(side=tk.LEFT, ipady=5)
        self.mv_left = Image_text(self, "images/lightning.gif", "Moves left", "12 moves remaining")
        self.mv_left.pack(side=tk.RIGHT, padx=130, ipady=5)

    def new_game_func(self):
        """
        Restart the game
        :return: None
        """
        self.gameapp.new_game()

    def ask_game_func(self):
        """
        Quit the game
        :return: None
        """
        self.gameapp.ask_quit()


class GameApp:
    """
        GameApp acts as a communicator between the View and the Model.
    """

    def __init__(self, master, task=TASK_ONE, dungeon_name="game3.txt"):
        """
        Constructor of the GameApp class
        :param master: parent
        :param task: Task name
        :param dungeon_name: The name of the map
        """
        self.master = master
        self.master.title("Key Cave Adventure Game")
        self.task = task
        self.dungeom_name = dungeon_name
        self.logic = GameLogic(self.dungeom_name)

        self.title = tk.Label(self.master, bg="#72F5A2", text="Key Cave Adventure Game", font="15")
        self.title.pack(side=tk.TOP, fill="x")
        self.dmkp = tk.Frame(self.master)
        self.dmkp.pack(side=tk.TOP)
        self.dm = DungeonMap(self.dmkp, self.logic._dungeon_size, 600)
        self.suspend = False

        if self.task == TASK_TWO:
            self.dm = AdvancedDungeonMap(self.dmkp, self.logic._dungeon_size, 600)
            self.bot_frame = StatusBar(self.master, 800, 700, self)
            self.bot_frame.pack(side=tk.TOP, anchor="w")
            self.menubar = tk.Menu(self.master)
            filemenu = tk.Menu(self.menubar, tearoff=0)
            self.menubar.add_cascade(label='Flie', menu=filemenu)
            filemenu.add_command(label='Save game ', command=self.save_game)
            filemenu.add_command(label='Load game ', command=self.file_load_game)
            filemenu.add_command(label='New game', command=self.new_game)
            filemenu.add_command(label='Quit', command=self.ask_quit)
            self.master.config(menu=self.menubar)
            self.time = 0
            self.master.after(1000, self.run)
        self.draw()
        self.dm.pack(side=tk.LEFT)
        self.kp = KeyPad(self.dmkp, 200, 100)
        self.kp.pack(side=tk.RIGHT)
        self.kp.draw_key(KEY_INFO)
        self.action = None
        self.dm.bind_all("<Key>", self.play)
        self.kp.tag_bind("w", '<ButtonPress-1>', self.direct_north)
        self.kp.tag_bind("a", '<ButtonPress-1>', self.direct_west)
        self.kp.tag_bind("s", '<ButtonPress-1>', self.direct_south)
        self.kp.tag_bind("d", '<ButtonPress-1>', self.direct_east)
        self.direct_tag = False

    def draw(self):
        self.dm.draw_grid(self.logic._game_information, self.logic._player.get_position())

    def get_bot_frame(self):
        return self.bot_frame

    def save_game(self):
        self.direct_tag = True
        save = self.logic.save_game(self.time)
        if save == True:
            self.direct_tag = False
            self.master.after(1000, self.run)

    def file_load_game(self):
        self.direct_tag = True
        load = self.logic.file_load_game()
        if load != True:
            self.direct_tag = False
            self.time = load[2]
            self.get_bot_frame().mv_left.b_txt.pack_forget()
            self.get_bot_frame().mv_left.b_txt = tk.Label(self.get_bot_frame().mv_left.f,
                                                          text=f"{self.logic.get_player().moves_remaining()}" + " moves remaining")
            self.get_bot_frame().mv_left.b_txt.pack()
            self.get_bot_frame().timer.b_txt.pack_forget()
            self.get_bot_frame().timer.b_txt = tk.Label(self.get_bot_frame().timer.f,
                                                        text=f"{self.secToTime(self.time)}")
            self.get_bot_frame().timer.b_txt.pack()
            self.master.after(1000, self.run)

            self.draw()

    def direct_north(self, a):
        """
        Game button northward
        :param a: Event information
        :return: None
        """
        if self.direct_tag == True:
            return
        a.char = "w"
        self.play(a)

    def direct_west(self, a):
        """
        Game button westward
        :param a: Event information
        :return: None
        """
        if self.direct_tag == True:
            return
        a.char = "a"
        self.play(a)

    def direct_south(self, a):
        """
        Game button southward
        :param a: Event information
        :return: None
        """
        if self.direct_tag == True:
            return
        a.char = "s"
        self.play(a)

    def direct_east(self, a):
        """
        Game button eastward
        :param a: Event information
        :return: None
        """
        if self.direct_tag == True:
            return
        a.char = "d"
        self.play(a)

    def new_game(self):
        """
        Restart the game
        :return: None
        """
        self.logic = GameLogic(self.dungeom_name)
        self.time = 0
        self.get_bot_frame().mv_left.b_txt.pack_forget()
        self.get_bot_frame().mv_left.b_txt = tk.Label(self.get_bot_frame().mv_left.f,
                                                      text=f"{self.logic.get_player().moves_remaining()}" + " moves remaining")
        self.get_bot_frame().mv_left.b_txt.pack()
        self.get_bot_frame().timer.b_txt.pack_forget()
        self.get_bot_frame().timer.b_txt = tk.Label(self.get_bot_frame().timer.f,
                                                    text=f"{self.secToTime(self.time)}")
        self.get_bot_frame().timer.b_txt.pack()
        self.draw()

    def ask_quit(self):
        """
        quit game
        :return: None
        """
        self.suspend = True
        quit = tk.messagebox.askquestion(title="Are you sure to quit", message="Are you sure to quit")
        if quit == "yes":
            quit()
        else:
            self.suspend = False
            self.master.after(1000, self.run)

    def secToTime(self, time):
        """
        Time format conversion eg:65->1:05
        :param time:
        :return: How many minutes and seconds
        """
        m = self.time // 60
        s = self.time % 60
        return str(m) + "m" + str(s) + "s"

    def run(self):
        """
        Game time calculation
        :return: None
        """
        if self.direct_tag == True:
            return
        if self.logic.check_game_over():
            return
        if self.logic.won() == True:
            return
        if self.suspend == True:
            return
        self.time += 1
        self.get_bot_frame().timer.b_txt.pack_forget()
        self.get_bot_frame().timer.b_txt = tk.Label(self.get_bot_frame().timer.f, text=f"{self.secToTime(self.time)}")
        self.get_bot_frame().timer.b_txt.pack()
        self.master.after(1000, self.run)

    def play(self, direct):
        """
        Adjust the game according to the direction command input
        :param direct: Game direction entered
        :return:None
        """
        if self.direct_tag == True:
            return
        self.dm.delete(tk.ALL)
        self.action = direct.char
        direction = self.action
        if self.action not in ["w", "a", "s", "d"]:
            pass
        elif self.logic.check_game_over():
            self.draw()
            return
        elif not self.logic.collision_check(direction):
            self.logic.move_player(direction)
            entity = self.logic.get_entity(self.logic._player.get_position())
            if entity is not None:
                entity.on_hit(self.logic)
                if self.logic.won():
                    self.draw()
                    if self.task == TASK_ONE:
                        tk.messagebox.showinfo(title="you won", message="you won")
                    elif self.task == TASK_TWO:
                        if tk.messagebox.askquestion(title="you won",
                                                     message=" You have finish a level of a score of" + f"{self.time}" + ".\n" + "Would you like play again") == "yes":
                            self.logic = GameLogic(self.dungeom_name)
                            self.time = 0
                            self.get_bot_frame().mv_left.b_txt.pack_forget()
                            self.get_bot_frame().mv_left.b_txt = tk.Label(self.get_bot_frame().mv_left.f,
                                                                          text=f"{self.logic.get_player().moves_remaining()}" + " moves remaining")
                            self.get_bot_frame().mv_left.b_txt.pack()
                            self.get_bot_frame().timer.b_txt.pack_forget()
                            self.get_bot_frame().timer.b_txt = tk.Label(self.get_bot_frame().timer.f,
                                                                        text=f"{self.secToTime(self.time)}")
                            self.get_bot_frame().timer.b_txt.pack()
                            self.master.after(1000, self.run)
                            self.draw()
                        else:
                            quit()
                    return
            self.logic._player.change_move_count(-1)
            if self.task == TASK_TWO:
                self.get_bot_frame().mv_left.b_txt.pack_forget()
                self.get_bot_frame().mv_left.b_txt = tk.Label(self.get_bot_frame().mv_left.f,
                                                              text=f"{self.logic.get_player().moves_remaining()}" + " moves remaining")
                self.get_bot_frame().mv_left.b_txt.pack()
            if self.logic.check_game_over():
                self.draw()
                if self.task == TASK_ONE:
                    tk.messagebox.showinfo(title="you lose", message="you lose")
                elif self.task == TASK_TWO:
                    if tk.messagebox.askquestion(title="you lose",
                                                 message="Would you like play it again?") == "yes":
                        self.logic = GameLogic(self.dungeom_name)
                        self.time = 0
                        self.get_bot_frame().mv_left.b_txt.pack_forget()
                        self.get_bot_frame().mv_left.b_txt = tk.Label(self.get_bot_frame().mv_left.f,
                                                                      text=f"{self.logic.get_player().moves_remaining()}" + " moves remaining")
                        self.get_bot_frame().mv_left.b_txt.pack()
                        self.get_bot_frame().timer.b_txt.pack_forget()
                        self.get_bot_frame().timer.b_txt = tk.Label(self.get_bot_frame().timer.f,
                                                                    text=f"{self.secToTime(self.time)}")
                        self.get_bot_frame().timer.b_txt.pack()
                        self.master.after(1000, self.run)
                        self.draw()
                    else:
                        quit()

        self.draw()
        self.kp.draw_key(KEY_INFO)


if __name__ == '__main__':
    window = tk.Tk()
    window.geometry("820x700")
    app = GameApp(master=window, task=TASK_TWO)
    window.mainloop()
