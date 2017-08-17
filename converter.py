import pygame
import json
from glob import glob

class Converter:
	def __init__(self, unit_root):
		self.unit_list = glob(unit_root + "/" + "*.png");

		for unit_name in self.unit_list:
			name = unit_name.split("\\")[1];
			print("name = " + unit_name);
			p = unit_root + "/" + "mask" + "/" + "mask_" + name;
			print("mask_name = " + p);

			cur_img = pygame.image.load(p);

			for i in range(0, 128):
				for j in range(0, 128):
					clr = cur_img.get_at((i, j));
					if clr == (255, 0, 0, 255):
						print((i, j));


			self.width  = 800;
			self.height = 600;
			self.screen = pygame.display.set_mode((self.width, self.height), 0, 32);
			pygame.display.set_caption("worm");

		#self.test_img = pygame.image.load(unit_root + "/" + "mask" + "/" + "mask_diamond.png");
	def update_input_process(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit();
	def update(self):
		while True:
			self.update_input_process();
			self.screen.fill((0, 0, 0));
			self.screen.blit(self.test_img, (0, 0));
			pygame.display.update();
			



if __name__ == "__main__":
	converter = Converter("units");
	#converter.update();
	print("main");
