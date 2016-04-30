class Checkers(object):
    def __init__(self):
        self.board = {}

    def init_board(self):
        for y in range(8):
            for x in range(8):
                self.board[(x, y)] = None

        for y in range(3):
            for x in range(8):
                if self._valid_position(x, y):
                    self.set_man(x, y, Man("W"))

        for y in range(5, 8):
            for x in range(8):
                if self._valid_position(x, y):
                    self.set_man(x, y, Man("R"))

        print self.board

    def get_position(self, x, y):
        return self.board[(x, y)]

    def set_man(self, x, y, man):
        self.board[(x, y)] = man

    def del_position(self, x, y):
        self.board[(x, y)] = None

    def take(self, x, y):
        self.board[(x, y)] = None
        # This will have more state keeping logic

    def _valid_position(self, x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False

        if (y % 2 == 0 and x % 2 == 0) or (y % 2 == 1 and x % 2 == 1):
            return False
        return True

    def draw(self):
        for y in range(8):
            print '|',
            for x in range(8):
                if self.get_position(x, y):
                    print '{} |'.format(self.get_position(x, y).color),
                else:
                    print '__|',
            print "\n"

    def mv_man_on_board(self, x, y, x2, y2):
        if not self.get_position(x, y):
            raise Exception("This is not the man you're looking for?")
        man = self.get_position(x, y)
        self.set_man(x2, y2, man)
        self.del_position(x, y)

    def mv_man_on_board_and_take(self, x, y, x2, y2, x3, y3):
        self.mv_man_on_board(x, y, x2, y2)
        self.take(x3, y3)

    def check(self, x, y, xvec, yvec, man):
        """
        Returns the next x, y coordinates and maybe obstacle x, y coordinates??!
        """
        nxtx = x+xvec
        nxty = y+yvec
        if not self._valid_position(nxtx, nxty):
            raise Exception("{},{}: Not a valid position to move".format(nxtx, nxty))

        obstacle = self.get_position(nxtx, nxty)
        if not obstacle:
            return (nxtx, nxty), None

        if not obstacle.color == man.opp():
            raise Exception("Move must be against opposition!")
        
        jmpx = nxtx + xvec
        jmpy = nxty + yvec

        if not self._valid_position(jmpx, jmpy):
            raise Exception("{},{}: Not a valid position to move".format(jmpx, jmpy))

        if self.get_position(jmpx, jmpy):
            raise Exception("Can't jump more than one piece at a time!")

        return (jmpx, jmpy), (nxtx, nxty)

    def check_for_r(self, x, y):
        man = self.get_position(x, y)
        return self.check(x, y, 1, man.direction, man)

    def check_for_l(self, x, y):
        man = self.get_position(x, y)
        return self.check(x, y, -1, man.direction, man)

    def check_back_r(self, x, y):
        man = self.get_position(x, y)
        if not man.is_king():
            raise Exception("Only kings can move backwards")
        return self.check(x, y, 1, -(man.direction), man)

    def check_back_l(self, x, y):
        man = self.get_position(x, y)
        if not man.is_king():
            raise Exception("Only kings can move backwards")
        return self.check(x, y, -1, -(man.direction), man)

    def get_direction(self, rawdir):
        return {"rf": self.check_for_r,
                "lf": self.check_for_l,
                "rb": self.check_back_r,
                "lb": self.check_back_l,
                }.get(rawdir)

    def get_input(self):
        xydraw = raw_input("Select starting coordinates and directions >>> ")
        xyd = xydraw.split() 
        x = int(xyd[0])
        y = int(xyd[1])
        d = self.get_direction(xyd[2])
        directions = [self.get_direction(x) for x in xyd[3:]]
        return x, y, d, directions

    def turn(self, x, y, init_move_fn, move_fns): 
        (nxtx, nxty), obs = init_move_fn(x, y)
        if not obs:
            return self.mv_man_on_board(x, y, nxtx, nxty)
        
        jmpx, jmpy = obs
        self.mv_man_on_board_and_take(x, y, nxtx, nxty, jmpx, jmpy)
        
        for fn in move_fns:
            (nxtx, nxty), obs = fn(x, y)
            if not obs:
                raise Exception("You can't just move in a direction without taking another piece!")
            jmpx, jmpy = obs
            self.mv_man_on_board_and_take(x, y, nxtx, nxty, jmpx, jmpy)


class Man(object):
    def __init__(self, color):
        self.king = False
        if not color in ["R", "W"]:
            raise Exception("Needs to be R or W")
        self.color = color
        self.direction = 1 if self.color == "W" else -1
    
    def opp(self):
        return "W" if self.color == "R" else "R"

    def king(self):
        self.king = True

    def is_king(self):
        return self.king

def main():
    game = Checkers()
    game.init_board()
    game.draw()
    while True:
        try:
            (x, y, d, dirs) = game.get_input()
            game.turn(x, y, d, dirs)
        except Exception as e:
            print e
        game.draw()

if __name__ == "__main__":
    main()
