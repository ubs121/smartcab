
class Agent:
    def __init__(self):
        self.location = (0, 0)
        self.heading = (0, -1)

    def forward(self):
        self.location = ((self.location[0] + self.heading[0]),
            (self.location[1] + self.heading[1]))

    def turn_right(self):
        self.heading = (-self.heading[1], self.heading[0])
        self.forward()

    def turn_left(self):
        self.heading = (self.heading[1], -self.heading[0])
        self.forward()

    def loc(self):
        print "loc={}, head={}".format( self.location, self.heading)

if __name__ == '__main__':
  headings = [(-1, 0), (0, -1), (1, 0), (0, 1)] # WNES
  a = Agent()

  a.forward()
  a.turn_left()
  a.turn_right()
  a.turn_right()

  print a.loc()
