class Area:
    def __init__(self, name: str, theme: str, doors: [[str, [int, int], [int, int, int, int]]], max_scroll_x: int, max_scroll_y: int, objects: list, npcs: list):
        """
        Creates the area and sets up objects
        :param name: The name of the area
        :param theme: The theme that will play while the player is in the area
        :param doors: The areas the area connects to, coords of the doors' hitboxes, and coords the player will go to
        :param objects: The objects that will be loaded in the area and the hitboxes of them
        :param npcs: The npcs that will be loaded in the area
        """
        import main
        #main.song = theme
        #main.music_player.load(main.f.song[theme])
        self.name = name
        self.doors = doors
        self.max_scroll_x = max_scroll_x
        self.max_scroll_y = max_scroll_y
        self.scroll_x = 0
        self.scroll_y = 0
        self.objects = objects
        self.npcs = npcs

    def set_name(self, new_name: str):
        self.name = new_name

    def load(self):
        for object in self.objects:
            object.draw()

    def scroll(self, direction: int, amount: int):
        for object in self.objects:
            if direction == 0:
                object.y += amount
                self.scroll_y += amount
            elif direction == 1:
                object.x += amount
                self.scroll_x -= amount
            elif direction == 2:
                object.y -= amount
                self.scroll_y -= amount
            else:
                object.x -= amount
                self.scroll_x += amount

    def in_hitbox(self, direction: int):
        """
        Checks if the player is in an object's hitbox
        :param direction: The direction the player is facing
        """
        import main
        for object in self.objects:
            if ((direction == 1) and (main.p.x <= object.x + object.width + 1) and (main.p.x + 40 >= object.x + 2) and (main.p.y + 72 <= object.y + object.height + 1) and (main.p.y + 72 >= object.y - 1)) or ((direction == 3) and (main.p.x <= object.x + object.width - 2) and (main.p.x + 40 >= object.x - 1) and (main.p.y + 72 <= object.y + object.height + 1) and (main.p.y + 72 >= object.y - 1)) or ((direction == 0) and (main.p.x + 40 >= object.x + 2) and (main.p.x <= object.x + object.width - 2) and (main.p.y + 72 <= object.y + object.height + 5) and (main.p.y + 72 >= object.y + 2)) or ((direction == 2) and (main.p.x + 40 >= object.x + 2) and (main.p.x <= object.x + object.width - 2) and (main.p.y + 72 <= object.y + object.height + 2) and (main.p.y + 72 >= object.y - 4)):
                return True
        return False
