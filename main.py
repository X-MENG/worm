import pygame
import json
import math

class Worm:
	def __init__(self):
		self.width = 800;
		self.height = 600;

		self.screen = pygame.display.set_mode((self.width, self.height), 0, 32);
		pygame.display.set_caption("worm");

	def init(self):
		with open("config/unit_config.json") as f:
			self.json_dict = json.load(f);

		self.root_name = "diamond.png";
		self.root_img = pygame.image.load("units/" + self.root_name);
		self.root_pos = (self.width / 2 - self.root_img.get_width() / 2, self.height / 2 - self.root_img.get_height() / 2);
		self.color_slot = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (255, 255, 0, 255), (255, 0, 255, 255), (0, 255, 255, 255)];
		self.attach("diamond.png", 3, "triangle.png", 0);

	def cross_product_test(self, a, b):
		return a[0] * b[1] - a[1] * b[0] > 0;

	def attach(self, root_name, root_anchor_index, child_name, child_index):
		root_anchors    = self.json_dict[root_name];
		root_anchor     = root_anchors[root_anchor_index][0];
		root_anchor_dir = root_anchors[root_anchor_index][1];

		self.child_img = pygame.image.load("units/" + child_name);

		mark_color = self.color_slot[child_index];

		child_anchors    = self.json_dict[child_name];
		child_anchor     = child_anchors[child_index][0];
		child_anchor_dir = child_anchors[child_index][1];
		print(child_anchor_dir);
		child_anchor_target_dir = [-root_anchor_dir[0], -root_anchor_dir[1]];
		print(child_anchor_target_dir);

		print("child_pos = (%s, %s)" % (child_anchor[0], child_anchor[1]));

		self.child_img.set_at((child_anchor[0], child_anchor[1]), mark_color);

		a_len = math.sqrt(child_anchor_target_dir[0] ** 2 + child_anchor_target_dir[1] ** 2);
		b_len = math.sqrt(child_anchor_dir[0] ** 2 + child_anchor_dir[1] ** 2);
		c = (child_anchor_target_dir[0] - child_anchor_dir[0], child_anchor_target_dir[1] - child_anchor_dir[1]);
		c_len = math.sqrt(c[0] ** 2 + c[1] ** 2);

		the_rad_angle = math.acos((a_len ** 2 + b_len ** 2 - c_len ** 2) / (2 * a_len * b_len));
		the_angle = the_rad_angle *  180.0 / math.pi
		print(the_angle);

		flag = self.cross_product_test(child_anchor_dir, child_anchor_target_dir);

		if flag > 0:
			self.child_img = pygame.transform.rotate(self.child_img, the_angle);
		else:
			self.child_img = pygame.transform.rotate(self.child_img, -the_angle);

		w, h = self.child_img.get_size();

		print("find hot point");
		hot_point = (0, 0);
		for j in range(0, h):
			for i in range(0, w):
				clr = self.child_img.get_at((i, j));
				if clr == mark_color:
					print(i, j);
					hot_point = (i, j);
					break;

		self.child_pos = (self.width / 2 - hot_point[0], self.height / 2 - hot_point[1]);

		px = self.root_pos[0] + root_anchor[0] - hot_point[0];
		py = self.root_pos[1] + root_anchor[1] - hot_point[1];

		self.child_pos = (px, py);

	def update_input_process(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit();

	def update(self):
		while True:
			self.update_input_process();
			self.screen.fill((0, 0, 0));
			self.screen.blit(self.root_img, self.root_pos);
			self.screen.blit(self.child_img, self.child_pos);
			pygame.display.update();

if __name__ == "__main__":
	worm = Worm();
	worm.init();
	worm.update();
	print("main");

