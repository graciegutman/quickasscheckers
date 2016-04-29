class Checkers:
    def __init__(self):
        self.board = {}

    def init_board(self):
        for y in range(8):
            for x in range(8):
                self.board[(x, y)] = None

        for y in range(3):
            for x in range(8):
                if self._valid_position(x, y):
                    self.set_man(Man("W"), x, y)

        for y in range(5, 8):
            for x in range(8):
                if self._valid_position(x, y):
                    self.set_man(Man("R"), x, y)

    def set_man(self, man, x, y):
        self.board[(x, y)] = man

    def get_position(self, x, y):
        if self._valid_position(x, y):
            return self.board.get((x, y))

    def set_position(self, x, y, man):
        if _valid_position(x, y):
            self.board[(x, y)] = man

    def take(self, x, y):
        self.board[(x, y)] = None

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

    def mv_for_r(self, x, y):
        man = self.get_position(x, y)
        nxtx = x+1
        nxty = y+(man.direction)
        if self._valid_position(nxtx, nxty):
            obstacle = self.get_position(nxtx, nxty)
            if obstacle and obstacle.color == man.opp():
                jmpx = nxtx+1
                jmpy = nxty+(man.direction)
                if self._valid_position(jmpx, jmpy):
                    self.take(nxtx, nxty)
                    self.set_position(jmpx, jmpy, man)

            else:
                self.set_position(nxtx, nxty, man)


    def mv_for_l(self, x, y):
        pass


class Man:
    def __init__(self, color):
        self.king = False
        if not color in ["R", "W"]:
            raise Exception("Needs to be R or W")
        self.color = color
        self.direction = 1 if self.color == "R" else -1
    
    def opp(self):
        return "W" if self.color == "R" else "R"

def main():
    game = Checkers()
    game.init_board()
    game.draw()


if __name__ == "__main__":
    main()

