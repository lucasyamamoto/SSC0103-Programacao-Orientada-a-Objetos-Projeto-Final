
import pygame
from element import GameObject, CircularObject, RectangularObject
from level import LevelManager, Level
from interface import InterfaceManager, MainMenu, LevelSelection, GameInterface, LevelCompletedInterface, PopUp, InterfaceElement, TextBox, InteractiveTextBox

class Equation:
	# Colors
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	# Game settings
	FRAMERATE = 60

	def __init__(self, window):
		"""
		Inicialize game class while loading levels and menus
		
		:param window: Superfície da janela
		"""

		# Main loop variables
		self._window = window
		self._clock = pygame.time.Clock()
		self._running = True
		self._interface = MainMenu()
		self._level_manager = LevelManager()
		self._extra_menus = []
		self._delay = 0
		count = 0
		while True:
			try:
				self._level_manager.load(f'level{count}')
				count += 1
			except FileNotFoundError:
				break
		self._current_level = None
		self._current_level_index = None
		pygame.display.set_caption("Equation")

	def open_main_menu(self):
		"""Load main menu. Doesn't reset level configurations"""
		self._extra_menus = []
		self._interface = MainMenu()

	def open_level_selection(self):
		"""Load level selection menu. Doesn't reset level configurations"""
		self._extra_menus = []
		self._interface = LevelSelection(self._level_manager.size)

	def set_current_level(self, index: int):
		"""
		Start level. Doesn't reset level configurations

		:param int index: Index of the level
		"""
		self._current_level = self._level_manager.get_level(index)
		self._current_level_index = index
		self._interface = GameInterface(self._current_level)

	def get_current_level(self):
		"""
		Returns currently running level

		:return:
		Level: Current level
		"""
		return self._current_level

	def restart_current_level(self):
		"""Restart current level resetting level configurations"""
		if self._current_level_index != None:
			self._level_manager.load(f'level{self._current_level_index}', self._current_level_index)
			self.set_current_level(self._current_level_index)
			self._interface = GameInterface(self._current_level)

	def exit_current_level(self):
		"""Exit current level to level selection menu while resetting level configurations"""
		self._level_manager.load(f'level{self._current_level_index}', self._current_level_index)
		self._current_level = None
		self._current_level_index = None
		self._extra_menus = []
		self.open_level_selection()

	def open_new_menu(self, interface: InterfaceManager):
		"""
		Open a new extra menu on top of the current one

		:param InterfaceManager interface: New menu
		"""
		self._extra_menus.append(interface)

	def quit_menu(self):
		"""Quit extra menu on top of the main interface"""
		if len(self._extra_menus) > 0:
			self._extra_menus.pop()

	def quit(self):
		"""Quit game"""
		self._running = False

	def listen(self):
		"""Listen for events and update game state"""

		# Check for events
		for event in pygame.event.get():
			# If window is being closed
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			# Listen for interface events
			if len(self._extra_menus) == 0:
				self._interface.listen(self, event)
			else:
				# Listen events for the latest open menu
				self._extra_menus[-1].listen(self, event)

		mouse_pos = pygame.mouse.get_pos()

		# Lock features during attempt
		if isinstance(self._interface, GameInterface) and self._interface.attempt:
            # Deactivate all text boxes
			InteractiveTextBox.deactivate_all()
			for elem in self._interface._elements:
                # Search for clickable text boxes
				if isinstance(elem, TextBox) and elem.hover(mouse_pos) and elem.clickable:
					if elem.text == 'Sair':
						if event.type == pygame.MOUSEBUTTONDOWN:
							game.exit_current_level()
						else:
							# Hover animation
							elem.color = (255, 255, 255)
							elem.background = self._interface.FONTCOLOR
					else:
						# Disable hover animation
						elem.color = self._interface.FONTCOLOR
						elem.background = None

            # Execute attempt
			if self._interface.move_right is None:
				self._interface.move_right = self._current_level.get_ball_pos()[0] < self._current_level.get_goal_pos()[0]
			
			# Check for delay, if necessary
			if self._delay == 0:
				self._current_level.move_ball(self._interface.equation, self._interface.move_right)
				self._delay = 0
			else:
				self._delay -= 1

            # Check for collisions
			ball_pos = self._current_level.get_ball_pos()
			screen_size = pygame.display.get_surface().get_size()

            # If ball goes out of the screen or hit a wall, end the self
			if ball_pos[0] < 0 or ball_pos[0] > screen_size[0] or ball_pos[1] < 0 or ball_pos[1] > screen_size[1] or self._current_level.check_wall_collision():
				self._interface.attempt = False
				self.open_new_menu(PopUp(['Você perdeu. Tente novamente.']))
				self.restart_current_level()
            # if ball reaches goal, end the self
			elif self._current_level.check_goal_collision():
				self._interface.attempt = False
				self.open_new_menu(LevelCompletedInterface())

	def display(self):
		"""Display all current elements in game"""

		# Update display
		self._window.fill(self.WHITE)
		if self._current_level is not None:
			self._current_level.display(self._window)
		self._interface.display(self._window)
		if len(self._extra_menus) > 0:
			for menu in self._extra_menus:
				menu.display(self._window)
		pygame.display.update()

	def main(self):
		"""Start game loop"""

		# Main loop
		while self._running:
			# Syncronize framerate
			self._clock.tick(self.FRAMERATE)
			# Display game
			self.display()
			# Listen for events
			self.listen()

if __name__ == '__main__':
	"""Allow game to run from this file"""

	# Window variables
	width, height = 800, 600
	window = pygame.display.set_mode((width, height))
	pygame.init()
	game = Equation(window)
	game.main()
	pygame.quit()