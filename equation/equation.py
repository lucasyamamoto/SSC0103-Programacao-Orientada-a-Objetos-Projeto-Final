
import pygame
from element import GameObject, CircularObject, RectangularObject
from level import LevelManager, Level
from interface import InterfaceManager, MainMenu, LevelSelection, GameInterface, InterfaceElement, TextBox, InteractiveTextBox

class Equation:
	# Colors
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	# Game settings
	FRAMERATE = 60

	def __init__(self, window):
		# Main loop variables
		self._window = window
		self._clock = pygame.time.Clock()
		self._running = True
		self._interface = MainMenu()
		self._level_manager = LevelManager()
		self._delay = 0
		count = 0
		while True:
			try:
				self._level_manager.load(f'level{count}')
				count += 1
			except FileNotFoundError:
				print(count)
				break
		self._current_level = None
		self._current_level_index = None
		pygame.display.set_caption("Equation")

	def open_main_menu(self):
		self._interface = MainMenu()

	def open_level_selection(self):
		self._interface = LevelSelection(self._level_manager.size)

	def set_current_level(self, index: int):
		self._current_level = self._level_manager.get_level(index)
		self._current_level_index = index
		self._interface = GameInterface(self._current_level)

	def get_current_level(self):
		return self._current_level

	def restart_current_level(self):
		if self._current_level_index != None:
			self._level_manager.load(f'level{self._current_level_index}', self._current_level_index)
			self.set_current_level(self._current_level_index)
			self._interface = GameInterface(self._current_level)

	def exit_current_level(self):
		self._current_level = None
		self._current_level_index = None
		self.open_main_menu()

	def quit(self):
		self._running = False

	def listen(self):
		# Check for events
		for event in pygame.event.get():
			# If window is being closed
			if event.type == pygame.QUIT:
				self._running = False
				return
			# Listen for interface events
			self._interface.listen(self, event)
		if isinstance(self._interface, GameInterface) and self._interface.attempt:
			if self._interface.move_right is None:
				self._interface.move_right = self._current_level.get_ball_pos()[0] < self._current_level.get_goal_pos()[0]
			if self._delay == 0:
				self._current_level.move_ball(self._interface.equation, self._interface.move_right)
				self._delay = 1
			else:
				self._delay -= 1
			ball_pos = self._current_level.get_ball_pos()
			screen_size = pygame.display.get_surface().get_size()
			if ball_pos[0] < 0 or ball_pos[0] > screen_size[0] or ball_pos[1] < 1 or ball_pos[1] > screen_size[1]:
				self._interface.attempt = False
				print('Fim de jogo')
				self.restart_current_level()
			if self._current_level.check_goal_collision():
				self._current_level.is_completed = True
				print('Parabéns')
				self.restart_current_level()

	def display(self):
		# Update display
		self._window.fill(self.WHITE)
		if self._current_level is not None:
			self._current_level.display(self._window)
		self._interface.display(self._window)
		pygame.display.update()

	def main(self):
		# Main loop
		while self._running:
			# Syncronize framerate
			self._clock.tick(self.FRAMERATE)
			# Display game
			self.display()
			# Listen for events
			self.listen()
			mouse_pos = pygame.mouse.get_pos()
			if self._current_level is not None:
				print(self._current_level._objects[self._current_level._ball_index].image.get_size())
				print(self._current_level._objects[self._current_level._ball_index].collision(CircularObject(x=mouse_pos[0], y=mouse_pos[1])))

if __name__ == '__main__':
	# Window variables
	width, height = 800, 600
	window = pygame.display.set_mode((width, height))
	pygame.init()
	game = Equation(window)
	game.main()
	pygame.quit()