import random
import sys

CARDS = [(i%15)+1 for i in range(105)]

_pause_enabled = True
def pause():
    global _pause_enabled
    if _pause_enabled:
        user_str = input("Press Enter to continue, (c) to continue, (x) to exit...")
        if user_str == "c":
            _pause_enabled = False
        if user_str == "x":
            sys.exit()

class Game:
    def __init__(self, n_players):
        self.n_players = n_players
        self.player = -1
        self.winner = -1

        self.f_piles = [[] for _ in range(n_players)]
        self.h_piles = [[] for _ in range(n_players)]
        self.r_piles = [[] for _ in range(n_players)]
        self.c_piles = []

        self.center = []


    def turn(self, player):
        print(player)
        print(self)
        pause()

        # Play off the flinch
        top_flinch = self.f_piles[player][0]

        for cp in self.c_piles:
            if (cp[0] + 1) == top_flinch:
                self.f_piles[player].pop(0)
                cp.insert(0, top_flinch)

                if len(self.f_piles) == 0:
                    self.winner = player

                # Restart from the beginning
                return self.turn(player)

        # Clear completed piles
        for i, cp in enumerate(self.c_piles):
            if cp[0] == 15:
                CARDS.append(self.c_piles.pop(i))
                random.shuffle(CARDS)

        if len(self.h_piles[player]) == 0:
            self.h_piles[player] = [self.center.pop() for _ in range(5)]

        # Play off hand
        # 1s first
        for i, h in enumerate(self.h_piles[player]):
            if h == 1:
                self.c_piles.append([1])
                self.h_piles[player].pop(i)
                # Start over
                return self.turn(player)

        for i, h in enumerate(self.h_piles[player]):
            for cp in self.c_piles:
                if (cp[0] + 1) == h:
                    self.h_piles[player].pop(i)
                    cp.insert(0, h)

                    # Start over
                    return self.turn(player)

        # Play off reserve
        pass

        return

    def initial_shuffle(self):
        # Flinch piles
        random.shuffle(CARDS)

        for player in range(self.n_players):
            # Flinch
            for _ in range(10):
                self.f_piles[player].append(CARDS.pop())

            # Hand
            for _ in range(5):
                self.h_piles[player].append(CARDS.pop())

        self.center = [c for c in CARDS]

    def game(self):
        self.initial_shuffle()
        found = False

        for player, hand in enumerate(self.h_piles):
            for i, h in enumerate(self.h_piles[player]):
                if h == 1:
                    self.c_piles.append([1])
                    self.h_piles[player].pop(i)
                    found = True
                    break
            if found:
                break

        else:
            raise ValueError("no player has 1 in hand")

        self.player = player
        print("starting player: %d" % player)

        while self.winner == -1:
            self.turn(self.player)
            self.player = (self.player + 1) % self.n_players

    def __str__(self):
        s = ""

        s += "Center piles\n"
        for cp in self.c_piles:
            s += "   %s" % cp

        s += "\n"
        for p in range(self.n_players):
            if p == self.player:
                s += "\033[3;1m"
            s += "Player %d\n" % p
            s += "   hand:   %s\n" % self.h_piles[p]
            s += "   flinch: %s\n" % self.f_piles[p]
            if p == self.player:
                s += "\033[0;0m"

        return s



if __name__ == "__main__":
    g = Game(7)
    g.game()




