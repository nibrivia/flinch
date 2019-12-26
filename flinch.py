import random
import math
import statistics
import sys

CARDS = [(i%15)+1 for i in range(150)]

_pause_enabled = False
def pause():
    global _pause_enabled
    if _pause_enabled:
        user_str = input("Press Enter to continue, (c) to continue, (x) to exit...")
        if user_str == "c":
            _pause_enabled = False
        if user_str == "x":
            print("exit")
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
        #print(self)
        pause()

        # Play off the flinch
        if len(self.f_piles[player]) == 0:
            self.winner = player
            return
        top_flinch = self.f_piles[player][0]

        if top_flinch == 1:
            self.c_piles.append([1])
            self.f_piles[player].pop(0)

            # Start over
            return self.turn(player)

        for cp in self.c_piles:
            if (cp[0] + 1) == top_flinch:
                self.f_piles[player].pop(0)
                cp.insert(0, top_flinch)

                # Restart from the beginning
                return self.turn(player)

        # Clear completed piles
        for i, cp in enumerate(self.c_piles):
            if cp[0] == 15:
                self.center.extend(self.c_piles.pop(i))
                random.shuffle(self.center)

        if len(self.h_piles[player]) == 0:
            if len(self.center) == 0:
                self.winner = player
                return
            self.h_piles[player] = [c for c in sorted([self.center.pop() for _ in range(5)])]

        # Play off hand
        # 1s first
        for i, h in enumerate(self.h_piles[player]):
            if h == 1:
                self.c_piles.append([1])
                self.h_piles[player].pop(i)
                # Start over
                return self.turn(player)

        # Anything else next
        for i, h in enumerate(self.h_piles[player]):
            for cp in self.c_piles:
                if (cp[0] + 1) == h:
                    self.h_piles[player].pop(i)
                    cp.insert(0, h)

                    # Start over
                    return self.turn(player)

        # Play off reserve
        for i, rp in enumerate(self.r_piles[player]):
            for cp in self.c_piles:
                if (cp[0] + 1) == rp[-1]:
                    card = self.r_piles[player][i].pop()
                    cp.insert(0, card)

                    # Remove that reserve pile
                    if len(self.r_piles[player][i]) == 0:
                        self.r_piles[player].pop(i)

                    # Start over
                    return self.turn(player)

        # Turn is done, add to reserve
        card = self.h_piles[player].pop()
        if len(self.r_piles[player]) < 5:
            self.r_piles[player].append([card])
        else:
            p = int(random.random()*5)
            self.r_piles[player][p].append(card)


        return

    def initial_shuffle(self):
        # Flinch piles
        random.shuffle(CARDS)
        self.center = [c for c in CARDS]

        for player in range(self.n_players):
            # Flinch
            self.f_piles[player] = []
            for _ in range(10):
                self.f_piles[player].append(self.center.pop())

            # Hand
            self.h_piles[player] = []
            for _ in range(5):
                self.h_piles[player].append(self.center.pop())

    def game(self):

        # Initial shuffle might leave no player with 1 in hand
        found = False
        while not found:
            self.initial_shuffle()
            for player, hand in enumerate(self.h_piles):
                for i, h in enumerate(self.h_piles[player]):
                    if h == 1:
                        self.c_piles.append([1])
                        self.h_piles[player].pop(i)
                        found = True
                        break
                if found:
                    break

        self.player = player

        self.n_turn = 0
        while self.winner == -1:
            self.n_turn = self.n_turn + 1
            self.turn(self.player)
            self.player = (self.player + 1) % self.n_players

        return self.n_turn

    def __str__(self):
        s = "Round %d, Turn %d (%d)\n" % (self.n_turn // self.n_players, self.n_turn % self.n_players, self.n_turn)

        s += "Center piles\n"
        for cp in self.c_piles:
            s += "   %s" % cp

        s += "\n"
        for p in range(self.n_players):
            if p == self.player:
                s += "\033[3;1m"
            s += "Player %d\n" % (p+1)
            s += "   hand:   %s\n" % self.h_piles[p]
            s += "   flinch: %s\n" % self.f_piles[p]
            s += "   resrvs: %s\n" % self.r_piles[p]
            if p == self.player:
                s += "\033[0;0m"

        s += "Center\n"
        s += "%s" % self.center

        return s



if __name__ == "__main__":

    for n in range(2,8):
        ts = []
        for _ in range(10000):
            g = Game(n)
            ts.append(g.game())

        mean = sum(ts)/len(ts)
        sd   = statistics.stdev(ts)
        sderr = sd/math.sqrt(len(ts))
        print("%d players: avg=%.1f (%2d) sd=%.1f  sderr=%.1f  n=%d" % (n, mean, mean/n, sd, sderr, len(ts)))




