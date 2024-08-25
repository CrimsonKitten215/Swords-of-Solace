import pygame
import sys
import useful_code.object_creator as ob

class BattleTemplate:
	"""
	A template for easily creating a battle between the player's team and one or more enemies
	"""
	def ui_maker_2000(self):
		import main
		from main import f

		# temp ui maker until trash code works
		ui1 = ob.ObjectCreator(f.battle["charlie_battle_ui_open"], 0, 409, 1)
		ui2 = ob.ObjectCreator(f.battle["charlie_battle_ui_closed"], 213, 442, 1)
		ui3 = ob.ObjectCreator(f.battle["charlie_battle_ui_closed"], 426, 442, 1)

		# FIX THIS FAULTY RUSHED BS CODE!!!!!!
		"""
		if main.selected_fighter == 0:
			ui1 = ob.ObjectCreator(f.battle["charlie_battle_ui_open"], 0, 409, 1)
			if main.selection_1 == 0:
				selected_thingy = ob.ObjectCreator(f.battle["charlie_attack_selected"], 10, 1, 1)
			elif main.selection_1 == 1:
				selected_thingy = ob.ObjectCreator(f.battle["charlie_act_selected"], 51, 1, 1)
			elif main.selection_1 == 2:
				selected_thingy = ob.ObjectCreator(f.battle["charlie_item_selected"], 92, 1, 1)
			else:
				selected_thingy = ob.ObjectCreator(f.battle["charlie_defend_selected"], 133, 1, 1)
		else:
			ui1 = ob.ObjectCreator(f.battle["charlie_battle_ui_closed"], 0, 442, 1)
		if len(self.team) == 2:
			if main.selected_fighter == 1:
				ui2 = ob.ObjectCreator(f.battle["charlie_battle_ui_open"], 213, 409, 1)
				if main.selection_1 == 0:
					selected_thingy = ob.ObjectCreator(f.battle["charlie_attack_selected"], 223, 1, 1)
				elif main.selection_1 == 1:
					selected_thingy = ob.ObjectCreator(f.battle["charlie_act_selected"], 264, 1, 1)
				elif main.selection_1 == 2:
					selected_thingy = ob.ObjectCreator(f.battle["charlie_item_selected"], 205, 1, 1)
				else:
					selected_thingy = ob.ObjectCreator(f.battle["charlie_defend_selected"], 346, 1, 1)
			else:
				ui2 = ob.ObjectCreator(f.battle["charlie_battle_ui_closed"], 213, 442, 1)
		elif len(self.team) == 3:
			if main.selected_fighter == 2:
				ui3 = ob.ObjectCreator(f.battle["charlie_battle_ui_open"], 426, 409, 1)
				if main.selection_1 == 0:
					selected_thingy = ob.ObjectCreator(f.battle["charlie_attack_selected"], 436, 1, 1)
				elif main.selection_1 == 1:
					selected_thingy = ob.ObjectCreator(f.battle["charlie_act_selected"], 477, 1, 1)
				elif main.selection_1 == 2:
					selected_thingy = ob.ObjectCreator(f.battle["charlie_item_selected"], 518, 1, 1)
				else:
					selected_thingy = ob.ObjectCreator(f.battle["charlie_defend_selected"], 559, 1, 1)
			else:
				ui3 = ob.ObjectCreator(f.battle["charlie_battle_ui_closed"], 426, 442, 1)
		"""

	# make these work later!!!
	def attack(self):
		"""
		Runs when the player selects attack
		"""
		import main
		from main import f

	def defend(self):
		"""
		Runs when the player selects defend
		"""
		import main
		from main import f

	def act(self):
		"""
		Runs when the player selects act
		"""
		import main
		from main import f

	def magic(self):
		"""
		Runs when the player selects magic
		"""
		import main
		from main import f

	def item(self):
		"""
  		Runs when the player selects item
		"""
		import main
		from main import f

	def dodge(self):
		"""
		Runs when the player needs to FKING DODGE OMFG!!!
		"""
		import main
		from main import f

	def selectornator_500(self):
		import main
		# MOVE THE SPAM CHECKER CODE TO MAIN FILE LATER!!!
		if main.keys[pygame.K_KP_ENTER] or main.keys[pygame.K_z]:
			main.k_z = True
		if main.k_z and not (main.keys[pygame.K_KP_ENTER] or main.keys[pygame.K_z]):
			main.k_z = False
			main.selected_1 = main.selection_1
		if main.selected_1 == 0:
			self.attack()
		elif main.selected_1 == 1:
			if main.selected_fighter == 0 and main.skin != "normal":
				self.magic()
			else:
				self.act()
		elif main.selected_1 == 2:
			self.item()
		elif main.selected_1 == 3:
			self.defend()

		if main.selected_1 != -1:
			if main.keys[pygame.K_a] or main.keys[pygame.K_LEFT]:
				main.k_a = True
			if main.keys[pygame.K_d] or main.keys[pygame.K_RIGHT]:
				main.k_d = True
			if main.k_a and not (main.keys[pygame.K_LEFT] or main.keys[pygame.K_a]):
				main.k_a = False
				main.selection_1 -= 1
				if main.selection_1 < 0:
					main.selection_1 = 2
			if main.k_d and not (main.keys[pygame.K_RIGHT] or main.keys[pygame.K_d]):
				main.k_d = False
				main.selection_1 += 1
				if main.selection_1 > 3:
					main.selection_1 = 0

	def __init__(self, team: list, enemies: list, theme: str):
		"""
		Sets up the battle
		:param team: Player's team of fighters
		:param enemies: A list of objects of all enemies fighting the player
		:param theme: The theme that will play during the battle
		"""
		import main
		import pygame

		from main import f

		# setting variables
		self.team = team
		self.enemies = enemies
		main.song = theme

		self.ui_maker_2000()
		self.selectornator_500()