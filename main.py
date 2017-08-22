import pygame
import json
import math	
import random

class WormUnit:
	def __init__(self, worm, unit_img, unit_type):
		self.worm = worm;

		self.unit_type = unit_type;
		self.unit_img = pygame.image.load(unit_img);
		self.anchors = self.worm.main.unit_config[self.unit_type];
		self.active_anchors = [];
		self.max_anchor_count = len(self.anchors);
		self.free_anchor_count = self.max_anchor_count;
		self.child_units = {};
		self.parent_worm_unit = None;
		self.parent_anchor_index = -1;
		self.to_parent_anchor_index = -1;
		self.local_angle = 0.0;

	def is_anchor_free(self, anchor_index):
		if anchor_index in self.child_units.keys():
			return False;

		return True;

	def get_left_top_pos_after_rotating_by_anchor_world_pos(self, anchor_index, world_pos):
		w, h = self.unit_img.get_size();
		pos = self.get_anchor_pos_after_rotating(w, h, anchor_index, self.local_angle);

		px = world_pos[0] - pos[0];
		py = world_pos[1] - pos[1];

		return (px, py);

	def get_render_pos_by_parent(self, to_parent_anchor_index, parent_anchor_index):
		parent_worm_unit = self.parent_worm_unit;
		parent_active_anchor = parent_worm_unit.active_anchors[parent_anchor_index];
		render_pos = self.get_left_top_pos_after_rotating_by_anchor_world_pos(to_parent_anchor_index, parent_active_anchor[0])
		
		return render_pos;

	def get_root_to_leaf_connection_list(self):
		root_to_leaf_connection_list = [];
		cur_unit = self;

		while cur_unit.parent_worm_unit != None:
			root_to_leaf_connection_list.append([cur_unit, cur_unit.to_parent_anchor_index]);
			root_to_leaf_connection_list.append([cur_unit, cur_unit.parent_anchor_index]);

		root_to_leaf_connection_list.reverse();

		return root_to_leaf_connection_list

	def get_root_to_leaf_unit_list(self):
		root_to_leaf_unit_list = [];
		cur_unit = self;

		while cur_unit != None:
			root_to_leaf_unit_list.append(cur_unit);
			cur_unit = cur_unit.parent_worm_unit;

		root_to_leaf_unit_list.reverse();

		return root_to_leaf_unit_list;

	def get_anchor_forward(self, anchor_index):
		if self.active_anchors != []:
			return self.active_anchors[anchor_index][1];
		else:
			anchor_info = self.anchors[anchor_index];
			new_forward = self.get_rotate_forward(anchor_info[1], self.local_angle);

			return new_forward;

	def vector2_add(self, v1, v2):
		return [v1[0] + v2[0], v1[1] + v2[1]];		

	def vector2_sub(self, v1, v2):
		return [v1[0] - v2[0], v1[1] - v2[1]];

	def vector3_add(self, v1, v2):
		return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]];

	def vector3_sub(self, v1, v2):
		return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]];

	def vector3_mul(self, v, a):
		return [v[0] * a, v[1] * a, v[2] * a];

	def get_vector2_length(self, v):
		return math.sqrt(v[0] ** 2 + v[1] ** 2);

	def get_vector3_length(self, v):
		return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2);

	def normalize_vector2(self, v):
		length = self.get_vector2_length(v);
		return [v[0] / length, v[1] / length];

	def normalize_vector3(self, v):
		length = self.get_vector3_length(v);
		return [v[0] / length, v[1] / length, v[2] / length];

	def rad_to_deg(self, rad):
		return rad * 180.0 / math.pi;

	def deg_to_rad(self, deg):
		return deg * math.pi / 180.0;

	def vector2_cross_product(self, a, b):
		z = a[0] * b[1] - a[1] * b[0];
		n_z = z / abs(z);

		return (0, 0, n_z);

	def vector3_cross_procuct(self, a, b):
		#print("a = %s" % str(a));
		#print("b = %s" % str(b));

		x = a[1] * b[2] - a[2] * b[1];
		y = a[2] * b[0] - a[0] * b[2];
		z = a[0] * b[1] - a[1] * b[0];

		#print("v = %s" % [x, y, z]);
		return self.normalize_vector3([x, y, z]);

	def vector2_to_vector3(self, v):
		return [v[0], v[1], 0.0];

	def get_rotate_forward(self, forward, rotate_angle):
		x_axis = self.vector2_to_vector3(forward);
		x_axis = self.normalize_vector3(x_axis);
		z_axis = [0, 0, 1];
		y_axis = self.vector3_cross_procuct(x_axis, z_axis);
		angle = self.deg_to_rad(rotate_angle);
		rotated_forward = self.vector3_add(self.vector3_mul(x_axis, math.cos(angle)), self.vector3_mul(y_axis, math.sin(angle)));

		return rotated_forward;

	def reduce_free_anchor_count(self):
		self.free_anchor_count -= 1;
		if self.free_anchor_count < 0:
			print("wrong when reduce free anchor!");

	def get_free_anchor_count(self):
		count = self.free_anchor_count;
		for child_unit in self.child_units:
			count += child_unit.get_free_anchor_count();

		return count;

	def add_child(self, parent_anchor_index, child_worm_unit):
		self.child_units[parent_anchor_index] = child_worm_unit;
		self.reduce_free_anchor_count();

	def random_get_free_anchor_index(self):
		anchor_index_list = list(range(len(self.anchors)));

		if self.to_parent_anchor_index != -1:
			anchor_index_list.remove(self.to_parent_anchor_index);

		for k in self.child_units.keys():
			anchor_index_list.remove(k);

		r = random.randint(0, len(anchor_index_list) - 1);
		r = 0;
		return anchor_index_list[r];

	def get_anchor_pos_after_rotating(self, w, h, anchor_index, deg_angle):
		rad_angle = self.deg_to_rad(deg_angle);
		new_h = new_w = w * abs(math.cos(rad_angle)) + w * abs(math.sin(rad_angle));

		num1 = -0.5 * w * math.cos(rad_angle) + 0.5 * h * math.sin(rad_angle) + 0.5 * new_w;
		num2 = -0.5 * w * math.sin(rad_angle) - 0.5 * h * math.cos(rad_angle) + 0.5 * new_h;

		pixel = self.anchors[anchor_index][0];

		new_x = new_h - (pixel[0] * math.cos(rad_angle) - pixel[1] * math.sin(rad_angle) + num1);
		new_y = pixel[0] * math.sin(rad_angle) + pixel[1] * math.cos(rad_angle) + num2;

		return (int(new_x), int(new_y));

	def get_vector_angle(self, v1, v2):
		a_len = self.get_vector2_length(v1);
		b_len = self.get_vector2_length(v2);
		c = self.vector2_sub(v1, v2);
		c_len = self.get_vector2_length(c);

		rad_angle = math.acos((a_len ** 2 + b_len ** 2 - c_len ** 2) / (2 * a_len * b_len));
		angle = self.rad_to_deg(rad_angle);

		n = self.vector2_cross_product(v1, v2);

		if n[2] > 0:
			return angle;
		else:
			return -angle;

	def attach_to(self, parent_worm_unit, parent_anchor_index, anchor_index):
		print("attach_to");
		if parent_worm_unit.is_anchor_free(parent_anchor_index) == False:
			return False;

		if self.is_anchor_free(anchor_index) == False:
			return False;
		print("parent_anchor_index = %s" % parent_anchor_index);
		self.parent_anchor_forward = parent_worm_unit.get_anchor_forward(parent_anchor_index);
		anchor_forward = self.get_anchor_forward(anchor_index);

		anchor_target_forward = [-self.parent_anchor_forward[0], -self.parent_anchor_forward[1]];

		self.local_angle = parent_worm_unit.local_angle + self.get_vector_angle(anchor_forward, anchor_target_forward);

		print("local_angle = %s" % self.local_angle);

		self.parent_worm_unit = parent_worm_unit;
		self.parent_anchor_index = parent_anchor_index;
		self.to_parent_anchor_index = anchor_index;

		self.reduce_free_anchor_count();

		self.parent_worm_unit.add_child(self.parent_anchor_index, self);

		return True;

	def get_unit_by_step(self, step):
		cur_step = step;
		if cur_step == 1:
			return self, cur_step;
		else:
			if len(self.child_units) == 0:
				return self, cur_step - 1;
			else:
				for child_unit in self.child_units:
					self, cur_step = child_unit.get_unit_by_step(cur_step - 1);

		return None;

	def update_active_anchors(self, left_top_pos):
		self.active_anchors = [];
		for anchor in self.anchors:
			x = left_top_pos[0] + anchor[0][0];
			y = left_top_pos[1] + anchor[0][1];
			normal = self.get_rotate_forward(anchor[1], self.local_angle);
			self.active_anchors.append([[x, y], normal]);

	def update(self):
		print("--worm unit update--");

		render_pos = (0, 0);
		
		if self.parent_worm_unit == None:
			#print("self.parent_worm_unit == None");
			w, h = self.unit_img.get_size();
			render_pos = (self.worm.mid_pos[0] - w / 2, self.worm.mid_pos[1] - h / 2);
			self.update_active_anchors(render_pos);
		else:
			print("to_parent_anchor_index = %d, parent_anchor_index = %d" % (self.to_parent_anchor_index, self.parent_anchor_index));
			render_pos = self.get_render_pos_by_parent(self.to_parent_anchor_index, self.parent_anchor_index);
			self.update_active_anchors(render_pos);

		#print("(px, py) = %s" % str((px, py)));

		unit_img = pygame.transform.rotate(self.unit_img, self.local_angle);
		#unit_img.set_at((int(px), int(py)), (0, 255, 0, 255));
		self.worm.main.screen.blit(unit_img, render_pos);

		for child_unit in self.child_units.values():
			#print("update child_unit");
			child_unit.update();

class Worm:
	def __init__(self, main, root_unit_img, root_unit_type, mid_pos):
		self.main = main;
		self.root_unit = WormUnit(self, root_unit_img, root_unit_type);
		self.mid_pos = mid_pos;
		w, h = self.root_unit.unit_img.get_size();
		print("update root anchors");
		self.root_unit.update_active_anchors((mid_pos[0] - w / 2, mid_pos[1] - h / 2));

	def get_free_anchor_count(self):
		return self.root_unit.get_free_anchor_count();

	def random_attach_child(self, child_worm_unit, child_anchor_index):
		free_anchor_count = self.get_free_anchor_count();
		r = random.randint(1, free_anchor_count);
		r = 1;
		worm_unit, _ = self.root_unit.get_unit_by_step(r);
		parent_anchor_index = worm_unit.random_get_free_anchor_index();
		print("parent_anchor_index = %s" % parent_anchor_index);
		print("child_anchor_index = %s" % child_anchor_index);
		child_worm_unit.attach_to(worm_unit, parent_anchor_index, child_anchor_index);

	def update(self):
		print("----------------");
		self.root_unit.update();

class Main:
	def __init__(self):
		self.width = 800;
		self.height = 600;

		with open("config/unit_config.json") as f:
			self.unit_config = json.load(f);

		self.screen = pygame.display.set_mode((self.width, self.height), 0, 32);
		pygame.display.set_caption("worm");

		worm_mid_pos = (self.width / 2, self.height / 2);
		self.worm = Worm(self, "units/diamond.png", "diamond.png", worm_mid_pos);
		worm_unit1 = WormUnit(self.worm, "units/triangle.png", "triangle.png");
		self.worm.random_attach_child(worm_unit1, 0);
		worm_unit2 = WormUnit(self.worm, "units/circle.png", "circle.png");
		worm_unit2.attach_to(worm_unit1, 1, 0);

	def update_input_process(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit();

	def update(self):
		while True:
			self.update_input_process();
			self.screen.fill((0, 0, 0));

			self.worm.update();

			pygame.display.update();

if __name__ == "__main__":
	main = Main();
	main.update();


