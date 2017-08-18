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

		json_dict = json.dumps(unit_dict);

		print(json_dict);

		wf = open("config/unit_config.json", "w");
		wf.write(json_dict);
		wf.close();

	def to_center_axis_pos(self, img, x, y):
		half_width  = img.get_width() / 2;
		half_height = img.get_height() / 2;

		new_x = x - half_width;
		new_y = half_height - y;
		#print("new_pos = (%s, %s)" % (new_x, new_y));
		return (new_x, new_y);

	def get_neighbour_pixel(self, img, x, y, pattern_clr):
		#print("a0 = (%s, %s)" % (x, y));
		a0 = self.to_center_axis_pos(img, x, y);
		if x - 1 >= 0 and y - 1 >= 0:
			cur_clr = img.get_at((x - 1, y - 1));
			if cur_clr == pattern_clr:
				#print("a1 = (%s, %s)" % (x - 1, y - 1));
				a1 = self.to_center_axis_pos(img, x - 1, y - 1);
				return (a1[0] - a0[0], a1[1] - a0[1]);

		if x - 1 >= 0 and y + 1 < img.get_height():
			cur_clr = img.get_at((x - 1, y + 1));
			if cur_clr == pattern_clr:
				#print("a1 = (%s, %s)" % (x - 1, y + 1));
				a1 = self.to_center_axis_pos(img, x - 1, y + 1);
				return (a1[0] - a0[0], a1[1] - a0[1]);

		if x + 1 < img.get_width() and y - 1 >= 0:
			cur_clr = img.get_at((x + 1, y - 1));
			if cur_clr == pattern_clr:
				#print("a1 = (%s, %s)" % (x + 1, y - 1));
				a1 = self.to_center_axis_pos(img, x + 1, y - 1);
				return (a1[0] - a0[0], a1[1] - a0[1]);

		if x + 1 < img.get_width() and y + 1 < img.get_width():
			cur_clr = img.get_at((x + 1, y + 1));
			if cur_clr == pattern_clr:
				#print("a1 = (%s, %s)" % (x + 1, y + 1));
				a1 = self.to_center_axis_pos(img, x + 1, y + 1);
				return (a1[0] - a0[0], a1[1] - a0[1]);

		if x - 1 >= 0:
			cur_clr = img.get_at((x - 1, y));
			if cur_clr == pattern_clr:
				#print("a1 = (%s, %s)" % (x - 1, y));
				a1 = self.to_center_axis_pos(img, x - 1, y);
				return (a1[0] - a0[0], a1[1] - a0[1]);

		if x + 1 < img.get_width():
			cur_clr = img.get_at((x + 1, y));
			if cur_clr == pattern_clr:
				#print("a1 = (%s, %s)" % (x + 1, y));
				a1 = self.to_center_axis_pos(img, x + 1, y);
				return (a1[0] - a0[0], a1[1] - a0[1]);

		if y - 1 >= 0:
			cur_clr = img.get_at((x, y - 1));
			if cur_clr == pattern_clr:
				#print("a1 = (%s, %s)" % (x, y - 1));
				a1 = self.to_center_axis_pos(img, x, y - 1);
				return (a1[0] - a0[0], a1[1] - a0[1]);

		if y + 1 < img.get_height():
			cur_clr = img.get_at((x, y + 1));
			if cur_clr == pattern_clr:
				#print("a1 = (%s, %s)" % (x, y + 1));
				a1 = self.to_center_axis_pos(img, x, y + 1);
				return (a1[0] - a0[0], a1[1] - a0[1]);

		print("failed");
		return None;

if __name__ == "__main__":
	converter = Converter("units");

