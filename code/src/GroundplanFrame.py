from Tkinter import *


class GroundplanFrame(object):
    extra = 11

    MARGINLEFT = 25
    MARGINTOP = 25

    COLOR_WATER = "blue"
    COLOR_PLAYGROUND = "green"

    def __init__(self, plan):
        self.SCALE = 1
        self.root = Tk()
        self.plan = plan

        self.frame = Frame(self.root, width=1024, height=768, colormap="new")
        self.frame.pack(fill=BOTH, expand=1)

        self.label = Label(self.frame, text="Heuristics 2016 - Amstelhaege!")
        self.label.pack(fill=X, expand=1)

        self.canvas = Canvas(self.frame,
                             bg="white",
                             width=self.plan.width * self.SCALE,
                             height=self.plan.height * self.SCALE)

        self.canvas.bind("<Button-1>", self.processMouseEvent)
        self.canvas.focus_set()

        self.text = Text(self.root, bd=4, width=80, height=2)

    def draw_circumference(self, o, r, col):

        self.line(o.x1, o.y1 - r, o.x2, o.y1 - r, col)
        self.line(o.x2 + r, o.y1, o.x2 + r, o.y2, col)
        self.line(o.x1 - r, o.y1, o.x1 - r, o.y2, col)
        self.line(o.x1, o.y2 + r, o.x2, o.y2 + r, col)
        self.circular_edge(o.x1, o.y1, r, -1.0, -1.0)
        self.circular_edge(o.x1, o.y2, r, -1.0, 1.0)
        self.circular_edge(o.x2, o.y1, r, 1.0, -1.0)
        self.circular_edge(o.x2, o.y2, r, 1.0, 1.0)

    def setPlan(self):
        for r in self.plan.residences:
            self.canvas.create_rectangle(r.x1 * self.SCALE, r.y1 * self.SCALE, r.x2 * self.SCALE, r.y2 * self.SCALE,
                                         fill=r.getColor())
            self.draw_circumference(r, self.plan.getMinimumDistance(r), 'black')

        for wb in self.plan.waterbodies:
            self.canvas.create_rectangle(wb.x1 * self.SCALE,
                                         wb.y1 * self.SCALE,
                                         (wb.x1 + wb.width) *
                                         self.SCALE,
                                         (wb.y1 + wb.height) *
                                         self.SCALE,
                                         fill=self.COLOR_WATER)

        for playground in self.plan.playgrounds:
            self.canvas.create_rectangle(playground.x1 * self.SCALE,
                                         playground.y1 * self.SCALE,
                                         (playground.x1 + playground.width) *
                                         self.SCALE,
                                         (playground.y1 + playground.height) *
                                         self.SCALE,
                                         fill=self.COLOR_PLAYGROUND)

            self.draw_circumference(playground, self.plan.MAXIMUM_PLAYGROUND_DISTANCE, 'green')

        self.text.insert(INSERT, "Value of plan is: ")
        self.text.insert(INSERT, self.plan.getPlanValue())
        self.text.insert(INSERT, "\nis valid: ")
        isval = self.plan.isValid()

        self.text.insert(INSERT, isval)

        self.canvas.pack()
        self.text.pack(fill=BOTH, expand=1)

        self.root.update()

    def mark(self, x, y, c):
        self.canvas.create_line(x * self.SCALE, y * self.SCALE, x * self.SCALE, y * self.SCALE, fill=c)

    def circular_edge(self, x, y, distance, x_dir, y_dir):

        def compute_y(x, distance):
            x = float(x)
            distance = float(distance)
            assert x >= 0
            assert distance > 0
            y = abs((distance ** 2 - x ** 2)) ** 0.5
            return y

        x_dist = 0.5

        while x_dist < distance:
            y_dist = compute_y(x_dist, int(distance))
            self.mark(x + x_dist * x_dir, y + y_dist * y_dir, 'green')
            x_dist += 0.5

    def line(self, x1, y1, x2, y2, c):
        self.canvas.create_line(
            x1 * self.SCALE, y1 * self.SCALE, x2 * self.SCALE, y2 * self.SCALE, fill=c)

    def updateit(self):

        self.canvas.pack()
        self.root.update()

    def repaint(self, newPlan):
        self.text.delete(1.0, END)
        self.canvas.delete("all")
        self.plan = newPlan
        self.setPlan()

    def processMouseEvent(self, event):
        coordinates = ((event.x / self.SCALE), ",", (event.y / self.SCALE))
        self.canvas.create_text(event.x, event.y, text=coordinates)
