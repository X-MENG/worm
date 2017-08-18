import pygame
import json
import os.path
from glob import glob

class Converter:
	def __init__(self, unit_root):
		self.unit_list = glob(unit_root + "/" + "*.png");

		unit_dict = {};

		for unit_name in self.unit_list:
			name = unit_name.split("\\")[1];
			print("name = " + unit_name);
			p = unit_root + "/" + "mask" + "/" + "mask_" + name;
			print("mask_name = " + p);

			cur_img = pygame.image.load(p);

			for j in range(0, 128):
				for i in range(0, 128):
					clr = cur_img.get_at((i, j));				
					if clr == (255, 0, 0, 255):
						#print("anchor: (%s, %s)" % (i, j));
						n = self.get_neighbour_pixel(cur_img, i, j, (0, 255, 0, 255));
						print("cur name = " + name);
						if name in unit_dict.keys():
							unit_dict[name].append([(i, j), n]);
						else:
							unit_dict[name] = [];
							unit_dict[name].append([(i, j), n]);

		#self.width  = 800;
		#self.height = 600;

		#self.screen = pygame.display.set_mode((self.width, self.height), 0, 32);
		#pygame.display.set_caption("worm");

		json_dict = json.dumps(unit_dict);

		print(json_dict);

		wf = open("config/unit_config.json", "w");
		wf.write(json_dict);
		wf.close();

	def get_neighbour_pixel(self, img, x, y, pattern_clr):
		if x - 1 >= 0 and y - 1 >= 0:
			cur_clr = img.get_at((x - 1, y - 1));
			if cur_clr == pattern_clr:
				return (-1, -1);

		if x - 1 >= 0 and y + 1 < img.get_height():
			cur_clr = img.get_at((x - 1, y + 1));
			if cur_clr == pattern_clr:
				return (-1, 1);

		if x + 1 < img.get_width() and y - 1 >= 0:
			cur_clr = img.get_at((x + 1, y - 1));
			if cur_clr == pattern_clr:
				return (1, -1);

		if x + 1 < img.get_width() and y + 1 < img.get_width():
			cur_clr = img.get_at((x + 1, y + 1));
			if cur_clr == pattern_clr:
				return (1, 1);

		if x - 1 >= 0:
			cur_clr = img.get_at((x - 1, y));
			if cur_clr == pattern_clr:
				return (-1, 0);

		if x + 1 < img.get_width():
			cur_clr = img.get_at((x + 1, y));
			if cur_clr == pattern_clr:
				return (1, 0);

		if y - 1 >= 0:
			cur_clr = img.get_at((x, y - 1));
			if cur_clr == pattern_clr:
				return (0, -1);

		if y + 1 < img.get_height():
			cur_clr = img.get_at((x, y + 1));
			if cur_clr == pattern_clr:
				return (0, 1);

		print("failed");
		return None;

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
