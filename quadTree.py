from GUI import *



class Container:
	allContainers = []

	def __init__(self, rect, color):
		self.rect = pg.Rect(rect)
		self.color = color

		self.parent = None

		Container.allContainers.append(self)

	def Draw(self):
		pg.draw.rect(screen, self.color, self.rect)


class QuadTree:
	allQuads = []

	def __init__(self, rect, maxBucket=4, parent=None):
		self.rect = pg.Rect(rect)
		self.maxBucket = Constrain(maxBucket, 1, len(Container.allContainers))
		self.parent = parent

		QuadTree.allQuads.append(self)

		self.children = []
		self.CreateTree()

	def Draw(self):
		pg.draw.line(screen, white, (self.rect.x + self.rect.w // 2, self.rect.y), (self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h))
		pg.draw.line(screen, white, (self.rect.x, self.rect.y + self.rect.h // 2), (self.rect.x + self.rect.w, self.rect.y + self.rect.h // 2))

	def CreateTree(self):
		nw_objs = []
		ne_objs = []
		sw_objs = []
		se_objs = []

		self.minSize = max(self.rect.w, self.rect.h)
		for container in Container.allContainers:
			self.minSize = min(container.rect.w, container.rect.h, self.minSize)

		nw = pg.Rect(self.rect.x, self.rect.y, self.rect.w // 2, self.rect.h // 2)
		ne = pg.Rect(self.rect.x + self.rect.w // 2, self.rect.y, self.rect.w // 2, self.rect.h // 2)
		sw = pg.Rect(self.rect.x, self.rect.y + self.rect.h // 2, self.rect.w // 2, self.rect.h // 2)
		se = pg.Rect(self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2, self.rect.w // 2, self.rect.h // 2)

		for container in Container.allContainers:
			if nw.colliderect(container.rect):
				nw_objs.append(container)

			elif ne.colliderect(container.rect):
				ne_objs.append(container)

			elif sw.colliderect(container.rect):
				sw_objs.append(container)

			elif se.colliderect(container.rect):
				se_objs.append(container)

		objs = []
		if len(nw_objs) > self.maxBucket:
			self.CreateBranch(nw)
		else:
			objs = nw_objs

		if len(ne_objs) > self.maxBucket:
			self.CreateBranch(ne)
		else:
			objs = ne_objs

		if len(sw_objs) > self.maxBucket:
			self.CreateBranch(sw)
		else:
			objs = sw_objs

		if len(se_objs) > self.maxBucket:
			self.CreateBranch(se)
		else:
			objs = se_objs

		self.objs = []

		for obj in objs:
			self.objs.append(Container.allContainers.index(obj))

	def CreateBranch(self, direction):
		if min(direction.w, direction.h) >= self.minSize:
			self.children.append(QuadTree(direction, self.maxBucket, self))

	def CheckChildForPos(self, parent, pos):
		c = None
		a = None
		
		for child in parent.children:
			if child.rect.contains((pos[0], pos[1], 1, 1)):
				c = self.CheckChildForPos(child, pos)

			if len(child.children) == 0:
				return parent

		return a if a != None else c

	def TopDownTraverse(self, pos):
		c = self.CheckChildForPos(self, pos)
		if c == None:
			return self
		else:
			return c



for i in range(500):
	Container((randint(0, width - 10), randint(0, height - 10), 10, 10), red)


root = QuadTree((0, 0, width, height), 1)


def DrawLoop():
	screen.fill(darkGray)

	DrawAllGUIObjects()
	
	for container in Container.allContainers:
		container.Draw()

	for q in QuadTree.allQuads:
		q.Draw()
	
	DrawRectOutline(blue, root.TopDownTraverse(pg.mouse.get_pos()).rect, 5)

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)


def Update():
	pass

while running:
	clock.tick_busy_loop(fps)

	deltaTime = clock.get_time()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	Update()

	DrawLoop()
