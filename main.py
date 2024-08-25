"""
~Controls~
Already added:
w/^ = move up
a/< = move left
s/v = move down
d/> = move right

Test controls:
b = enter test battle

To be added:
c/CTRL = menu
x/SHIFT = cancel / back
z/ENTER = interact / select
\ = parry
SPACE = skip text

~Variables~
stage = part of the story the player is on (e.g. intro)
mode = what mode the player is in

~Modes~
world
cutscene
battle
battle_dodging
options
"""

# imports
import pygame
import sys
import useful_code.fighter_creator as fc
import useful_code.battle_template as b
import useful_code.object_creator as ob
import useful_code.area_template as a

# setting variables (make save thingy work for this later!)
pygame.mixer.init()
screen_width = 640
screen_height = 480
tick = 0
other_tick = 0
song = "silence"
name = "Luna Stop Sleeping On My Keyboard Or I'll Name You This"
stage = "intro"
save_location = "intro"
cor = 0
max_mana = 100
inventory = ["-1", "-1", "-1", "-1", "-1", "-1"]
key_items = ["-1", "-1", "-1", "-1", "-1", "-1"]
kill_count = 0
fighting_scimi_count = 0
mana = max_mana
enemies_bested = []
side_quests_accepted = []
side_quests_finished = []
side_quests_failed = []
dir = 2
skin = "normal"
k_z = False
k_a = False
k_d = False
selection_1 = 0
selection_2 = 0
selection_3 = 0
selected_1 = -1
selected_2 = -1
selected_3 = -1
selected_fighter = 0
music_player = pygame.mixer.music
sound_player = pygame.mixer.music
mode = "world"
qtes_setting = True
p = fc.Fighter("Charlie", 100, 100, [], 100, 100, 1, 1, 1, [])

# getting settings
settings_file = open("saves/settings", "r")
saved_settings = settings_file.read().split("\n")
settings_file.close()
screen_size = int(saved_settings[1])
master_v = float(saved_settings[3])
music_v = float(saved_settings[5])
sfx_v = float(saved_settings[7])

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width * screen_size, screen_height * screen_size), pygame.RESIZABLE)
pygame.display.set_caption("Swords of Solace")
pygame.display.set_icon(pygame.image.load("assets/weapons/estoc.png"))
clock = pygame.time.Clock()

# files
class Files:
	def normal(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/normal/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/normal/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/normal/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/normal/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/normal/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/normal/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/normal/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/normal/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/normal/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/normal/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/normal/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/normal/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"acts_menu_label": pygame.image.load("assets/ui/other/acts_menu_label.png"),
			"armour_equip_icon_1": pygame.image.load("assets/ui/other/armour_equip_icon_1.png"),
			"armour_equip_icon_2": pygame.image.load("assets/ui/other/armour_equip_icon_2.png"),
			"armour_label": pygame.image.load("assets/ui/other/armour_label.png"),
			"armours_menu_label": pygame.image.load("assets/ui/other/armours_menu_label.png"),
			"equipment_icon": pygame.image.load("assets/ui/normal/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/normal/equipment_menu.png"),
			"items_icon": pygame.image.load("assets/ui/normal/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/normal/items_menu.png"),
			"magic_label": pygame.image.load("assets/ui/other/magic_label.png"),
			"party_icon": pygame.image.load("assets/ui/normal/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/normal/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/normal/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/normal/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/normal/shop_ui_1.png"),
			"sword_equip_icon": pygame.image.load("assets/ui/other/sword_equip_icon.png"),
			"sword_label": pygame.image.load("assets/ui/other/sword_label.png"),
			"text_box": pygame.image.load("assets/ui/normal/text_box.png"),
			"trance_ability_icon": pygame.image.load("assets/ui/other/trance_ability_icon.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/normal/charlie_act_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/normal/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/normal/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/normal/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/normal/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/normal/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/normal/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/normal/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/normal/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/normal/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/normal/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/normal/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/normal/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/normal/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/normal/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/normal/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/normal/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/normal/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/normal/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/normal/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/normal/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/normal/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/normal/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/normal/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/normal/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/normal/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/normal/battle_box/bb18.png"),
			"battle_text_box": pygame.image.load("assets/battle/other/battle_text_box.png"),
            "miss_label": pygame.image.load("assets/battle/other/miss_label.png"),
            "down_label": pygame.image.load("assets/battle/other/down_label.png"),
            "fled_label": pygame.image.load("assets/battle/other/fled_label.png"),
            "slain_label": pygame.image.load("assets/battle/other/slain_label.png"),
            "spared_label": pygame.image.load("assets/battle/other/spared_label.png"),
            "bg1": pygame.image.load("assets/battle/other/background/b0001.png"),
            "bg2": pygame.image.load("assets/battle/other/background/b0002.png"),
            "bg3": pygame.image.load("assets/battle/other/background/b0003.png"),
            "bg4": pygame.image.load("assets/battle/other/background/b0004.png"),
            "bg5": pygame.image.load("assets/battle/other/background/b0005.png"),
            "bg6": pygame.image.load("assets/battle/other/background/b0006.png"),
            "bg7": pygame.image.load("assets/battle/other/background/b0007.png"),
            "bg8": pygame.image.load("assets/battle/other/background/b0008.png"),
            "bg9": pygame.image.load("assets/battle/other/background/b0009.png"),
		    "bg10": pygame.image.load("assets/battle/other/background/b0010.png"),
            "bg11": pygame.image.load("assets/battle/other/background/b0011.png"),
            "bg12": pygame.image.load("assets/battle/other/background/b0012.png"),
            "bg13": pygame.image.load("assets/battle/other/background/b0013.png"),
            "bg14": pygame.image.load("assets/battle/other/background/b0014.png"),
            "bg15": pygame.image.load("assets/battle/other/background/b0015.png"),
            "bg16": pygame.image.load("assets/battle/other/background/b0016.png"),
            "bg17": pygame.image.load("assets/battle/other/background/b0017.png"),
            "bg18": pygame.image.load("assets/battle/other/background/b0018.png"),
            "bg19": pygame.image.load("assets/battle/other/background/b0019.png"),
            "bg20": pygame.image.load("assets/battle/other/background/b0020.png"),
            "bg21": pygame.image.load("assets/battle/other/background/b0021.png"),
            "bg22": pygame.image.load("assets/battle/other/background/b0022.png"),
            "bg23": pygame.image.load("assets/battle/other/background/b0023.png"),
            "bg24": pygame.image.load("assets/battle/other/background/b0024.png"),
            "bg25": pygame.image.load("assets/battle/other/background/b0025.png"),
            "bg26": pygame.image.load("assets/battle/other/background/b0026.png"),
            "bg27": pygame.image.load("assets/battle/other/background/b0027.png"),
            "bg28": pygame.image.load("assets/battle/other/background/b0028.png"),
            "bg29": pygame.image.load("assets/battle/other/background/b0029.png"),
            "bg30": pygame.image.load("assets/battle/other/background/b0030.png"),
            "bg31": pygame.image.load("assets/battle/other/background/b0031.png"),
            "bg32": pygame.image.load("assets/battle/other/background/b0032.png"),
            "bg33": pygame.image.load("assets/battle/other/background/b0033.png"),
            "bg34": pygame.image.load("assets/battle/other/background/b0034.png"),
            "bg35": pygame.image.load("assets/battle/other/background/b0035.png"),
            "bg36": pygame.image.load("assets/battle/other/background/b0036.png"),
            "bg37": pygame.image.load("assets/battle/other/background/b0037.png"),
            "bg38": pygame.image.load("assets/battle/other/background/b0038.png"),
            "bg39": pygame.image.load("assets/battle/other/background/b0039.png"),
            "bg40": pygame.image.load("assets/battle/other/background/b0040.png"),
            "bg41": pygame.image.load("assets/battle/other/background/b0041.png"),
            "bg42": pygame.image.load("assets/battle/other/background/b0042.png"),
            "bg43": pygame.image.load("assets/battle/other/background/b0043.png"),
            "bg44": pygame.image.load("assets/battle/other/background/b0044.png"),
            "bg45": pygame.image.load("assets/battle/other/background/b0045.png"),
            "bg46": pygame.image.load("assets/battle/other/background/b0046.png"),
            "bg47": pygame.image.load("assets/battle/other/background/b0047.png"),
            "bg48": pygame.image.load("assets/battle/other/background/b0048.png"),
            "bg49": pygame.image.load("assets/battle/other/background/b0049.png"),
            "bg50": pygame.image.load("assets/battle/other/background/b0050.png"),
            "bg51": pygame.image.load("assets/battle/other/background/b0051.png"),
            "bg52": pygame.image.load("assets/battle/other/background/b0052.png"),
            "bg53": pygame.image.load("assets/battle/other/background/b0053.png"),
            "bg54": pygame.image.load("assets/battle/other/background/b0054.png"),
            "bg55": pygame.image.load("assets/battle/other/background/b0055.png"),
            "bg56": pygame.image.load("assets/battle/other/background/b0056.png"),
            "bg57": pygame.image.load("assets/battle/other/background/b0057.png"),
            "bg58": pygame.image.load("assets/battle/other/background/b0058.png"),
            "bg59": pygame.image.load("assets/battle/other/background/b0059.png"),
            "bg60": pygame.image.load("assets/battle/other/background/b0060.png"),
            "bg61": pygame.image.load("assets/battle/other/background/b0061.png"),
            "bg62": pygame.image.load("assets/battle/other/background/b0062.png"),
            "bg63": pygame.image.load("assets/battle/other/background/b0063.png"),
            "bg64": pygame.image.load("assets/battle/other/background/b0064.png"),
            "bg65": pygame.image.load("assets/battle/other/background/b0065.png"),
            "bg66": pygame.image.load("assets/battle/other/background/b0066.png"),
            "bg67": pygame.image.load("assets/battle/other/background/b0067.png"),
            "bg68": pygame.image.load("assets/battle/other/background/b0068.png"),
            "bg69": pygame.image.load("assets/battle/other/background/b0069.png"),
            "bg70": pygame.image.load("assets/battle/other/background/b0070.png"),
            "bg71": pygame.image.load("assets/battle/other/background/b0071.png"),
            "bg72": pygame.image.load("assets/battle/other/background/b0072.png"),
            "bg73": pygame.image.load("assets/battle/other/background/b0073.png"),
            "bg74": pygame.image.load("assets/battle/other/background/b0074.png"),
            "bg75": pygame.image.load("assets/battle/other/background/b0075.png"),
            "bg76": pygame.image.load("assets/battle/other/background/b0076.png"),
            "bg77": pygame.image.load("assets/battle/other/background/b0077.png"),
            "bg78": pygame.image.load("assets/battle/other/background/b0078.png"),
            "bg79": pygame.image.load("assets/battle/other/background/b0079.png"),
            "bg80": pygame.image.load("assets/battle/other/background/b0080.png"),
            "bg81": pygame.image.load("assets/battle/other/background/b0081.png"),
            "bg82": pygame.image.load("assets/battle/other/background/b0082.png"),
            "bg83": pygame.image.load("assets/battle/other/background/b0083.png"),
            "bg84": pygame.image.load("assets/battle/other/background/b0084.png"),
            "bg85": pygame.image.load("assets/battle/other/background/b0085.png"),
            "bg86": pygame.image.load("assets/battle/other/background/b0086.png"),
            "bg87": pygame.image.load("assets/battle/other/background/b0087.png"),
        	"bg88": pygame.image.load("assets/battle/other/background/b0088.png"),
            "bg89": pygame.image.load("assets/battle/other/background/b0089.png"),
            "bg90": pygame.image.load("assets/battle/other/background/b0090.png"),
            "bg91": pygame.image.load("assets/battle/other/background/b0091.png"),
            "bg92": pygame.image.load("assets/battle/other/background/b0092.png"),
            "bg93": pygame.image.load("assets/battle/other/background/b0093.png"),
            "bg94": pygame.image.load("assets/battle/other/background/b0094.png"),
            "bg95": pygame.image.load("assets/battle/other/background/b0095.png"),
            "bg96": pygame.image.load("assets/battle/other/background/b0096.png"),
            "bg97": pygame.image.load("assets/battle/other/background/b0097.png"),
            "bg98": pygame.image.load("assets/battle/other/background/b0098.png"),
            "bg99": pygame.image.load("assets/battle/other/background/b0099.png"),
            "bg100": pygame.image.load("assets/battle/other/background/b0100.png"),
		}

	def __init__(self):
		self.normal()
		self.objects = {
			"test_object": pygame.image.load("assets/objects/test_object.png").convert_alpha(),
			"big_bush": pygame.image.load("assets/objects/big_bush.png").convert_alpha(),
			"small_bush": pygame.image.load("assets/objects/small_bush.png").convert_alpha(),
			"flowers_1": pygame.image.load("assets/objects/flowers_1.png").convert_alpha(),
			"flowers_2": pygame.image.load("assets/objects/flowers_2.png").convert_alpha(),
			"flowers_3": pygame.image.load("assets/objects/flowers_3.png").convert_alpha(),
			"flowers_4": pygame.image.load("assets/objects/flowers_4.png").convert_alpha(),
			"grass_1": pygame.image.load("assets/objects/grass_1.png").convert_alpha(),
			"grass_2": pygame.image.load("assets/objects/grass_2.png").convert_alpha(),
			"grass_3": pygame.image.load("assets/objects/grass_3.png").convert_alpha(),
			"grass_4": pygame.image.load("assets/objects/grass_4.png").convert_alpha(),
			"grass_5": pygame.image.load("assets/objects/grass_5.png").convert_alpha(),
			"mushrooms_1": pygame.image.load("assets/objects/mushrooms_1.png").convert_alpha(),
			"mushroom_2": pygame.image.load("assets/objects/mushrooms_2.png").convert_alpha(),
			"sign": pygame.image.load("assets/objects/sign.png").convert_alpha(),
			"sussy_egg_tree": pygame.image.load("assets/objects/sussy_egg_tree.png").convert_alpha(),
			"tree_1": pygame.image.load("assets/objects/tree_1.png").convert_alpha(),
			"tree_2": pygame.image.load("assets/objects/tree_2.png").convert_alpha(),
			"trees_left": pygame.image.load("assets/objects/trees_left.png").convert_alpha(),
			"trees_middle": pygame.image.load("assets/objects/trees_middle.png").convert_alpha(),
			"trees_right": pygame.image.load("assets/objects/trees_right.png").convert_alpha(),
			"lg_1": pygame.image.load("assets/objects/long_grass/lg_1.png").convert_alpha(),
			"lg_2": pygame.image.load("assets/objects/long_grass/lg_2.png").convert_alpha(),
			"lg_3": pygame.image.load("assets/objects/long_grass/lg_3.png").convert_alpha(),
			"lg_4": pygame.image.load("assets/objects/long_grass/lg_4.png").convert_alpha(),
			"lg_5": pygame.image.load("assets/objects/long_grass/lg_5.png").convert_alpha(),
			"lg_6": pygame.image.load("assets/objects/long_grass/lg_6.png").convert_alpha(),
			"lg_7": pygame.image.load("assets/objects/long_grass/lg_7.png").convert_alpha(),
			"lg_8": pygame.image.load("assets/objects/long_grass/lg_8.png").convert_alpha(),
			"lg_9": pygame.image.load("assets/objects/long_grass/lg_9.png").convert_alpha(),
			"lg_outline_corner_bl": pygame.image.load("assets/objects/long_grass/lg_outline_corner_bl.png").convert_alpha(),
			"lg_outline_corner_br": pygame.image.load("assets/objects/long_grass/lg_outline_corner_br.png").convert_alpha(),
			"lg_outline_corner_tl": pygame.image.load("assets/objects/long_grass/lg_outline_corner_tl.png").convert_alpha(),
			"lg_outline_corner_tr": pygame.image.load("assets/objects/long_grass/lg_outline_corner_tr.png").convert_alpha(),
			"lg_outline_edge_b": pygame.image.load("assets/objects/long_grass/lg_outline_edge_b.png").convert_alpha(),
			"lg_outline_edge_l": pygame.image.load("assets/objects/long_grass/lg_outline_edge_l.png").convert_alpha(),
			"lg_outline_edge_r": pygame.image.load("assets/objects/long_grass/lg_outline_edge_r.png").convert_alpha(),
			"lg_outline_edge_t": pygame.image.load("assets/objects/long_grass/lg_outline_edge_t.png").convert_alpha(),
			"lg_outline_end_b": pygame.image.load("assets/objects/long_grass/lg_outline_end_b.png").convert_alpha(),
			"lg_outline_end_l": pygame.image.load("assets/objects/long_grass/lg_outline_end_l.png").convert_alpha(),
			"lg_outline_end_r": pygame.image.load("assets/objects/long_grass/lg_outline_end_r.png").convert_alpha(),
			"lg_outline_end_t": pygame.image.load("assets/objects/long_grass/lg_outline_end_t.png").convert_alpha(),
			"path_corner": pygame.image.load("assets/objects/paths/path_corner.png").convert_alpha(),
			"path_crossroad": pygame.image.load("assets/objects/paths/path_crossroad.png").convert_alpha(),
			"path_edge": pygame.image.load("assets/objects/paths/path_edge.png").convert_alpha(),
			"path_edgeless": pygame.image.load("assets/objects/paths/path_edgeless.png").convert_alpha(),
			"path_end": pygame.image.load("assets/objects/paths/path_end.png").convert_alpha(),
			"path_straight": pygame.image.load("assets/objects/paths/path_straight.png").convert_alpha(),
			"path_t_junction": pygame.image.load("assets/objects/paths/path_t_junction.png").convert_alpha(),
			"path_turn": pygame.image.load("assets/objects/paths/path_turn.png").convert_alpha(),
			"box_broken": pygame.image.load("assets/objects/puzzles/box_broken.png").convert_alpha(),
			"box": pygame.image.load("assets/objects/puzzles/box.png").convert_alpha(),
			"button": pygame.image.load("assets/objects/puzzles/button.png").convert_alpha(),
			"hole": pygame.image.load("assets/objects/puzzles/hole.png").convert_alpha(),
			"rock": pygame.image.load("assets/objects/puzzles/rock.png").convert_alpha(),
			"spike_off": pygame.image.load("assets/objects/puzzles/spike_off.png").convert_alpha(),
			"spike_on": pygame.image.load("assets/objects/puzzles/spike_on.png").convert_alpha(),
		}
		self.weapon = {
			"estoc": pygame.image.load("assets/weapons/estoc.png").convert_alpha(),
			"scimitar": pygame.image.load("assets/weapons/scimitar.png").convert_alpha(),
			"recurve_normal": pygame.image.load("assets/weapons/recurve_normal.png").convert_alpha(),
			"recurve_shooting": pygame.image.load("assets/weapons/recurve_shooting.png").convert_alpha()
		}
		self.song = {
			"silence": "sounds/music/silence.mp3",
			"cliche_village_theme": "sounds/music/cliche_village_theme.mp3",
			"tune_for_winners": "assets/objects/tune_for_winners.mp3"
		}
		self.sound = {}

	def good_blue(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/good/blue/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/good/blue/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/good/blue/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/good/blue/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/good/blue/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/good/blue/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/good/blue/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/good/blue/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/good_route/blue/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/good/blue/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/good/blue/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/good/blue/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/good/blue/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/good/blue/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/good/blue/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/good/blue/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/good/blue/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/good/blue/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/good/blue/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/good/blue/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/good/blue/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/good/blue/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/good/blue/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/good/blue/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/good/blue/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/good/blue/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/good/blue/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/good/blue/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/good/blue/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/good/blue/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/good/blue/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/good/blue/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/good/blue/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/good/blue/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/good/blue/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/good/blue/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/good/blue/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/good/blue/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/good/blue/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/good/blue/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/good/blue/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/good/blue/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/good/blue/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/good/blue/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/good/blue/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/good/blue/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/good/blue/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/good/blue/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/good/blue/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/good/blue/battle_box/bb18.png")
		}

	def good_both(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/good/both/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/good/both/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/good/both/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/good/both/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/good/both/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/good/both/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/good/both/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/good/both/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/good/both/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/good/both/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/good/both/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/good/both/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/good/both/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/good/both/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/good/both/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/good/both/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/good/both/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/good/both/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/good/both/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/good/both/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/good/both/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/good/both/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/good/both/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/good/both/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/good/both/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/good/both/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/good/both/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/good/both/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/good/both/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/good/both/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/good/both/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/good/both/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/good/both/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/good/both/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/good/both/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/good/both/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/good/both/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/good/both/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/good/both/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/good/both/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/good/both/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/good/both/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/good/both/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/good/both/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/good/both/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/good/both/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/good/both/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/good/both/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/good/both/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/good/both/battle_box/bb18.png")
		}

	def good_all(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/good/all/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/good/all/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/good/all/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/good/all/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/good/all/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/good/all/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/good/all/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/good/all/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/good/all/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/good/all/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/good/all/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/good/all/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/good/all/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/good/all/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/good/all/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/good/all/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/good/all/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/good/all/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/good/all/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/good/all/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/good/all/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/good/all/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/good/all/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/good/all/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/good/all/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/good/all/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/good/all/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/good/all/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/good/all/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/good/all/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/good/all/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/good/all/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/good/all/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/good/all/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/good/all/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/good/all/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/good/all/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/good/all/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/good/all/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/good/all/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/good/all/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/good/all/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/good/all/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/good/all/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/good/all/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/good/all/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/good/all/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/good/all/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/good/all/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/good/all/battle_box/bb18.png")
		}

	def neutral_blue(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/normal/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/neutral/blue/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/neutral/blue/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/neutral/blue/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/neutral/blue/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/neutral/blue/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/normal/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/normal/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/neutral/blue/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/neutral/blue/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/neutral/blue/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/neutral/blue/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/normal/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/neutral/blue/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/normal/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/neutral/blue/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/good/blue/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/neutral/blue/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/good/blue/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/neutral/blue/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/neutral/blue/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/neutral/blue/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/neutral/blue/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/normal/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/neutral/blue/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/normal/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/neutral/blue/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/neutral/blue/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/good/blue/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/good/blue/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/neutral/blue/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/neutral/blue/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/neutral/blue/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/neutral/blue/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/neutral/blue/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/neutral/blue/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/neutral/blue/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/neutral/blue/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/neutral/blue/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/neutral/blue/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/neutral/blue/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/neutral/blue/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/neutral/blue/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/neutral/blue/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/neutral/blue/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/neutral/blue/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/neutral/blue/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/neutral/blue/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/neutral/blue/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/neutral/blue/battle_box/bb18.png")
		}

	def neutral_red(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/normal/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/neutral/red/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/neutral/redredred/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/neutral/red/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/neutral/red/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/neutral/red/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/normal/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/normal/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/neutral/red/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/neutral/red/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/neutral/red/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/neutral/red/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/normal/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/neutral/red/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/normal/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/neutral/red/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/evil/red/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/neutral/red/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/evil/red/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/neutral/red/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/neutral/red/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/neutral/red/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/neutral/red/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/normal/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/neutral/red/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/normal/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/neutral/red/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/neutral/red/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/evil/red/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/evil/red/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/neutral/red/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/neutral/red/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/neutral/red/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/neutral/red/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/neutral/red/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/neutral/red/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/neutral/red/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/neutral/red/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/neutral/red/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/neutral/red/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/neutral/red/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/neutral/red/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/neutral/red/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/neutral/red/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/neutral/red/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/neutral/red/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/neutral/red/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/neutral/red/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/neutral/red/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/neutral/red/battle_box/bb18.png")
		}

	def neutral_both(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/normal/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/neutral/both/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/neutral/both/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/neutral/both/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/neutral/both/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/neutral/both/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/normal/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/normal/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/neutral/both/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/neutral/both/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/neutral/both/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/neutral/both/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/normal/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/neutral/both/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/normal/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/neutral/both/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/good/both/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/neutral/both/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/good/both/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/neutral/both/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/neutral/both/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/neutral/both/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/neutral/both/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/normal/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/neutral/both/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/normal/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/neutral/both/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/neutral/both/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/good/both/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/good/both/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/neutral/both/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/neutral/both/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/neutral/both/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/neutral/both/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/neutral/both/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/neutral/both/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/neutral/both/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/neutral/both/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/neutral/both/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/neutral/both/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/neutral/both/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/neutral/both/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/neutral/both/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/neutral/both/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/neutral/both/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/neutral/both/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/neutral/both/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/neutral/both/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/neutral/both/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/neutral/both/battle_box/bb18.png")
		}

	def evil_red(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/evil/red/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/evil/red/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/evil/red/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/evil/red/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/evil/red/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/evil/red/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/evil/red/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/evil/red/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/evil/red/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/evil/red/walking/walking/vwalk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/evil/red/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/evil/red/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/evil/red/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/evil/red/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/evil/red/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/evil/red/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/evil/red/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/evil/red/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/evil/red/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/evil/red/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/evil/red/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/evil/red/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/evil/red/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/evil/red/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/evil/red/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/evil/red/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/evil/red/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/evil/red/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/evil/red/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/evil/red/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/evil/red/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/evil/red/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/evil/red/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/evil/red/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/evil/red/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/evil/red/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/evil/red/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/evil/red/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/evil/red/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/evil/red/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/evil/red/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/evil/red/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/evil/red/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/evil/red/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/evil/red/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/evil/red/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/evil/red/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/evil/red/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/evil/red/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/evil/red/battle_box/bb18.png")
		}

	def evil_red_cor(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/evil/red_cor/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/evil/red/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/evil/red/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/evil/red/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/evil/red/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/evil/red/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/evil/red/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/evil/red/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/evil/red/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/evil/red/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/evil/red/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/evil/red/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/evil/red/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/evil/red/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/evil/red/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/evil/red/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/evil/red/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/evil/red/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/evil/red/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/evil/red/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/evil/red/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/evil/red/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/evil/red/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/evil/red/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/evil/red/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/evil/red/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/evil/red/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/evil/red/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/evil/red/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/evil/red/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/evil/red/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/evil/red/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/evil/red/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/evil/red/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/evil/red/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/evil/red/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/evil/red/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/evil/red/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/evil/red/battle_box/bb18.png")
		}

	def evil_cloak(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/evil/red/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/evil/red/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/evil/red/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/evil/red/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/evil/red/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/evil/red/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/evil/red/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/evil/red/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/evil/red/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/evil/red/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/evil/red/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/evil/red/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/evil/red/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/evil/red/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/evil/red/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/evil/red/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/evil/red/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/evil/red/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/evil/red/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/evil/red/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/evil/red/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/evil/red/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/evil/red/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/evil/red/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/evil/red/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/evil/red/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/evil/red/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/evil/red/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/evil/red/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/evil/red/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/evil/red/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/evil/red/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/evil/red/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/evil/red/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/evil/red/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/evil/red/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/evil/red/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/evil/red/battle_box/bb18.png")
		}

	def evil_cloak_cor(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/evil/cloak_cor/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/evil/cloak_cor/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/evil/cloak_cor/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/evil/cloak_cor/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/evil/cloak_cor/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/evil/cloak_cor/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/evil/cloak_cor/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/evil/cloak_cor/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/evil/cloak_cor/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/evil/red/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/evil/red/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/evil/red/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/evil/red/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/evil/red/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/evil/red/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/evil/red/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/evil/red/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/evil/red/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/evil/red/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/evil/red/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/evil/red/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/evil/red/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/evil/red/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/evil/red/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/evil/red/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/evil/red/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/evil/red/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/evil/red/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/evil/red/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/evil/red/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/evil/red/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/evil/red/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/evil/red/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/evil/red/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/evil/red/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/evil/red/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/evil/red/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/evil/red/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/evil/red/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/evil/red/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/evil/red/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/evil/red/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/evil/red/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/evil/red/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/evil/red/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/evil/red/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/evil/red/battle_box/bb18.png")
		}

	def evil_both(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/evil/both/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/evil/both/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/evil/both/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/evil/both/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/evil/both/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/evil/both/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/evil/both/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/evil/both/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/evil/both/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/evil/both/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/evil/both/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/evil/both/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/evil/both/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/evil/both/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/evil/both/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/evil/both/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/evil/both/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/evil/both/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/evil/both/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/evil/both/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/evil/both/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/evil/both/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/evil/both/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/evil/both/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/evil/both/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/evil/both/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/evil/both/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/evil/both/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/evil/both/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/evil/both/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/evil/both/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/evil/both/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/evil/both/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/evil/both/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/evil/both/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/evil/both/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/evil/both/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/evil/both/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/evil/both/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/evil/both/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/evil/both/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/evil/both/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/evil/both/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/evil/both/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/evil/both/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/evil/both/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/evil/both/battle_box/bb18.png")
		}

	def evil_both_cor(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/evil/both_cor/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/evil/both_cor/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/evil/both_cor/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/evil/both_cor/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/evil/both_cor/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/evil/both_cor/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/evil/both_cor/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/evil/both_cor/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/evil/both_cor/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/evil/both/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/evil/both/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/evil/both/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/evil/both/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/evil/both/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/evil/both/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/evil/both/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/evil/both/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/evil/both/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/evil/both/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/evil/both/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/evil/red/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/evil/red/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/evil/red/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/evil/red/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/evil/red/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/evil/red/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/evil/red/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/evil/red/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/evil/red/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/evil/red/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/evil/red/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/evil/red/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/evil/red/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/evil/red/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/evil/red/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/evil/red/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/evil/red/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/evil/red/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/evil/red/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/evil/red/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/evil/red/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/evil/red/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/evil/red/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/evil/red/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/evil/red/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/evil/red/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/evil/red/battle_box/bb18.png")
		}

	def demon(self):
		self.player = {
			"stand_up": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/stand_up.png").convert_alpha(),
			"stand_right": pygame.image.load("assets/sprites/charlie/evil/demon/walking/stand_right.png").convert_alpha(),
			"stand_left": pygame.image.load("assets/sprites/charlie/evil/demon/walking/stand_left.png").convert_alpha(),
			"stand_down": pygame.image.load("assets/sprites/charlie/evil/demon/walking/stand_down.png").convert_alpha(),
			"walk_down_1": pygame.image.load("assets/sprites/charlie/evil/demon/walking/walk_down_1.png").convert_alpha(),
			"walk_down_2": pygame.image.load("assets/sprites/charlie/evil/demon/walking/walk_down_2.png").convert_alpha(),
			"walk_up_1": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_up_1.png").convert_alpha(),
			"walk_up_2": pygame.image.load("assets/sprites/charlie/evil/cloak/walking/walk_up_2.png").convert_alpha(),
			"walk_left_1": pygame.image.load("assets/sprites/charlie/evil/demon/walking/walk_left_1.png").convert_alpha(),
			"walk_right_1": pygame.image.load("assets/sprites/charlie/evil/demon/walking/walk_right_1.png").convert_alpha(),
			"walk_left_2": pygame.image.load("assets/sprites/charlie/evil/demon/walking/walk_left_2.png").convert_alpha(),
			"walk_right_2": pygame.image.load("assets/sprites/charlie/evil/demon/walking/walk_right_2.png").convert_alpha()
		}
		self.ui = {
			"equipment_icon": pygame.image.load("assets/ui/evil/red/equipment_icon.png"),
			"equipment_menu": pygame.image.load("assets/ui/evil/red/equipment_menu.png"),
			"item_icon": pygame.image.load("assets/ui/evil/red/items_icon.png"),
			"items_menu": pygame.image.load("assets/ui/evil/red/items_menu.png"),
			"party_icon": pygame.image.load("assets/ui/evil/red/party_icon.png"),
			"party_menu": pygame.image.load("assets/ui/evil/red/party_menu.png"),
			"settings_icon": pygame.image.load("assets/ui/evil/red/settings_icon.png"),
			"settings_menu": pygame.image.load("assets/ui/evil/red/settings_menu.png"),
			"shop_ui_1": pygame.image.load("assets/ui/evil/red/shop_ui_1.png"),
			"shop_ui_2": pygame.image.load("assets/ui/evil/red/shop_ui_2.png"),
			"text_box": pygame.image.load("assets/ui/evil/red/text_box.png")
		}
		self.battle = {
			"charlie_act_selected": pygame.image.load("assets/battle/evil/red/charlie_magic_selected.png"),
			"charlie_attack_qte": pygame.image.load("assets/battle/evil/red/charlie_attack_qte.png"),
			"charlie_attack_selected": pygame.image.load("assets/battle/evil/red/charlie_attack_selected.png"),
			"charlie_battle_ui_closed": pygame.image.load("assets/battle/evil/demon/charlie_battle_ui_closed.png"),
			"charlie_battle_ui_open": pygame.image.load("assets/battle/evil/demon/charlie_battle_ui_open.png"),
			"charlie_defend_selected": pygame.image.load("assets/battle/evil/red/charlie_defend_selected.png"),
			"charlie_item_selected": pygame.image.load("assets/battle/evil/red/charlie_item_selected.png"),
			"tp_gauge": pygame.image.load("assets/battle/evil/red/tp_gauge.png"),
			"bb_normal": pygame.image.load("assets/battle/evil/red/battle_box/bb_normal.png"),
			"bb1": pygame.image.load("assets/battle/evil/red/battle_box/bb1.png"),
			"bb2": pygame.image.load("assets/battle/evil/red/battle_box/bb2.png"),
			"bb3": pygame.image.load("assets/battle/evil/red/battle_box/bb3.png"),
			"bb4": pygame.image.load("assets/battle/evil/red/battle_box/bb4.png"),
			"bb5": pygame.image.load("assets/battle/evil/red/battle_box/bb5.png"),
			"bb6": pygame.image.load("assets/battle/evil/red/battle_box/bb6.png"),
			"bb7": pygame.image.load("assets/battle/evil/red/battle_box/bb7.png"),
			"bb8": pygame.image.load("assets/battle/evil/red/battle_box/bb8.png"),
			"bb9": pygame.image.load("assets/battle/evil/red/battle_box/bb9.png"),
			"bb10": pygame.image.load("assets/battle/evil/red/battle_box/bb10.png"),
			"bb11": pygame.image.load("assets/battle/evil/red/battle_box/bb11.png"),
			"bb12": pygame.image.load("assets/battle/evil/red/battle_box/bb12.png"),
			"bb13": pygame.image.load("assets/battle/evil/red/battle_box/bb13.png"),
			"bb14": pygame.image.load("assets/battle/evil/red/battle_box/bb14.png"),
			"bb15": pygame.image.load("assets/battle/evil/red/battle_box/bb15.png"),
			"bb16": pygame.image.load("assets/battle/evil/red/battle_box/bb16.png"),
			"bb17": pygame.image.load("assets/battle/evil/red/battle_box/bb17.png"),
			"bb18": pygame.image.load("assets/battle/evil/red/battle_box/bb18.png")
		}

def play_sound(sound: str, volume: float):
	sound_player.load(sound)
	sound_player.play()
	sound_player.set_volume(volume * master_v * sfx_v)

# other important pregame setters
f = Files()
if skin == "good_blue":
	f.good_blue()
elif skin == "good_both":
	f.good_both()
elif skin == "good_all":
	f.good_all()
elif skin == "neutral_blue":
	f.neutral_blue()
elif skin == "neutral_red":
	f.neutral_red()
elif skin == "neutral_both":
	f.neutral_both()
elif skin == "evil_red":
	f.evil_red()
elif skin == "evil_red_cor":
	f.evil_red_cor()
elif skin == "evil_cloak":
	f.evil_cloak()
elif skin == "evil_cloak_cor":
	f.evil_cloak_cor()
elif skin == "evil_both":
	f.evil_both()
elif skin == "evil_both_cor":
	f.evil_both_cor()
elif skin == "demon":
	f.demon()
music_player.load(f.song[song])
ally1 = fc.Fighter("Test Ally 1", 100, 100, [], 100, 100, 1, 1, 1, [])
ally2 = fc.Fighter("Test Ally 2", 100, 100, [], 100, 100, 1, 1, 1, [])
area = a.Area("area_template", "silence", [[None]], 200, 200,
			  [ob.ObjectCreator(f.objects["test_object"], 0, 0, 1),
				ob.ObjectCreator(f.objects["test_object"], 400, 50, 1),
			   	ob.ObjectCreator(f.objects["test_object"], 200, 200, 1)], [])

# main game
while True:
	# setting up game
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	screen.fill((255, 255, 255))

	if mode == "world":
		# key presses
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			dir = 1
			if not area.in_hitbox(1):
				if p.x <= 100 and area.scroll_x >= 0:
					area.scroll(1, 3)
				else:
					p.x -= 4
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			dir = 3
			if not area.in_hitbox(3):
				if p.x >= 400 and area.scroll_x <= area.max_scroll_x:
					area.scroll(3, 3)
				else:
					p.x += 4
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			dir = 0
			if not area.in_hitbox(0):
				if p.y <= 60 and area.scroll_y <= area.max_scroll_y:
					area.scroll(0, 3)
				else:
					p.y -= 4
		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			dir = 2
			if not area.in_hitbox(2):
				if p.y >= 190 and area.scroll_y >= 0:
					area.scroll(2, 3)
				else:
					p.y += 4

		# test battle
		if keys[pygame.K_b]:
			mode = "battle"

		area.load()

		# movement
		if dir == 0:
			if keys[pygame.K_w] or keys[pygame.K_UP]:
				if other_tick == 0:
					ob.ObjectCreator(f.player["stand_up"], p.x, p.y, 2)
				if other_tick == 1:
					ob.ObjectCreator(f.player["walk_up_1"], p.x, p.y, 2)
				if other_tick == 2:
					ob.ObjectCreator(f.player["stand_up"], p.x, p.y, 2)
				if other_tick == 3:
					ob.ObjectCreator(f.player["walk_up_2"], p.x, p.y, 2)
			else:
				ob.ObjectCreator(f.player["stand_up"], p.x, p.y, 2)
		if dir == 1:
			if keys[pygame.K_a] or keys[pygame.K_LEFT]:
				if other_tick == 0:
					ob.ObjectCreator(f.player["stand_left"], p.x, p.y, 2)
				if other_tick == 1:
					ob.ObjectCreator(f.player["walk_left_1"], p.x, p.y, 2)
				if other_tick == 2:
					ob.ObjectCreator(f.player["stand_left"], p.x, p.y, 2)
				if other_tick == 3:
					ob.ObjectCreator(f.player["walk_left_1"], p.x, p.y, 2)
			else:
				ob.ObjectCreator(f.player["stand_left"], p.x, p.y, 2)
		if dir == 2:
			if keys[pygame.K_s] or keys[pygame.K_DOWN]:
				if other_tick == 0:
					ob.ObjectCreator(f.player["stand_down"], p.x, p.y, 2)
				if other_tick == 1:
					ob.ObjectCreator(f.player["walk_down_1"], p.x, p.y, 2)
				if other_tick == 2:
					ob.ObjectCreator(f.player["stand_down"], p.x, p.y, 2)
				if other_tick == 3:
					ob.ObjectCreator(f.player["walk_down_2"], p.x, p.y, 2)
			else:
				ob.ObjectCreator(f.player["stand_down"], p.x, p.y, 2)
		if dir == 3:
			if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
				if other_tick == 0:
					ob.ObjectCreator(f.player["stand_right"], p.x, p.y, 2)
				if other_tick == 1:
					ob.ObjectCreator(f.player["walk_right_1"], p.x, p.y, 2)
				if other_tick == 2:
					ob.ObjectCreator(f.player["stand_right"], p.x, p.y, 2)
				if other_tick == 3:
					ob.ObjectCreator(f.player["walk_right_2"], p.x, p.y, 2)
			else:
				ob.ObjectCreator(f.player["stand_right"], p.x, p.y, 2)

		# no going off screen
		if p.x > screen_width - 45:
			p.x = screen_width - 45
		elif p.x < 5:
			p.x = 5
		if p.y > screen_height - 77:
			p.y = screen_height - 77
		elif p.y < 5:
			p.y = 5

	# battle mechanics
	elif mode == "battle":
		enemy = fc.Fighter("Test Enemy", 100, 100, [], 100, 100, 1, 1, 1, [])
		battle = b.BattleTemplate([p, ally1, ally2], [enemy, enemy, enemy], f.song["silence"])

	# music
	if not music_player.get_busy():
		music_player.play()
		music_player.set_volume(music_v * master_v)

	# border
	pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(screen_width * screen_size, 0, 3000, 3000))
	pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, screen_height * screen_size, 3000, 3000))

	# tick
	tick += 1
	if tick % 5 == 0:
		other_tick += 1
		if other_tick >= 4:
			other_tick = 0
	pygame.display.update()
	clock.tick(30)