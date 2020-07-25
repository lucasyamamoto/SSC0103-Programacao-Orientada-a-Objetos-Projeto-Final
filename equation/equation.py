
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
		count = 0
		while True:
			try:
				self._level_manager.load(f'level{count}')
				count += 1
			except FileNotFoundError:
				print(count)
				break
		self._current_level = None
		pygame.display.set_caption("Equation")

	def open_main_menu(self):
		self._interface = MainMenu()

	def open_level_selection(self):
		self._interface = LevelSelection(self._level_manager.size)

	def set_current_level(self, index: int):
		self._current_level = self._level_manager.get_level(index)
		self._interface = GameInterface()

	def exit_current_level(self):
		self._current_level = None
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

if __name__ == '__main__':
	# Window variables
	width, height = 800, 600
	window = pygame.display.set_mode((width, height))
	pygame.init()
	game = Equation(window)
	game.main()
	pygame.quit()