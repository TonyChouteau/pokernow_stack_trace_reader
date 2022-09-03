from datetime import datetime
import matplotlib.pyplot as plt

class Player:
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.timestamps = []
        self.stacks = []

    def add_stack(self, stack, timestamp):
        self.timestamps.append(timestamp)
        self.stacks.append(stack)

    def add0(self):
        self.timestamps.append(self.timestamps[-1])
        self.stacks.append(0)

    def sort(self):
        entries = [(self.timestamps[i], self.stacks[i]) for i in range(len(self.stacks))]
        entries.sort(key=lambda x: x[0])
        entries = list(zip(*entries))
        self.timestamps = entries[0]
        self.stacks = entries[1]


class PlayerList:
    def __init__(self):
        self.players = {}

    def add_stack(self, username, stack, timestamp):
        if username not in self.players:
            self.players[username] = Player(username)
        self.players[username].add_stack(stack, timestamp)

    def add_line(self, line):
        print(line)
        split = line.split(",")
        timestamp = split[1].split(".")[0]
        if "in this table" in line:
            return
        content = split[0].split(":")[1].split("|")

        date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        for player_content in content:
            username = player_content.split("\"\"")[1].split("@")[0].strip()
            stack = int(player_content.split("(")[1].split(")")[0])
            self.add_stack(username, stack, date.timestamp())
            pass

    def draw(self):
        plt.figure(figsize=(20, 10))
        # plt.xticks(range(10))
        min_stack = 10**10
        max_stack = 0
        min_timing = 10**10
        max_timming = 0
        for username in self.players:
            player = self.players[username]
            player.add0()
            player.sort()

            min_s = min(player.stacks)
            max_s = max(player.stacks)
            min_stack = min_s if min_s < min_stack else min_stack
            max_stack = max_s if max_s > max_stack else max_stack

            min_t = min(player.timestamps)
            max_t = max(player.timestamps)
            min_timing = min_t if min_t < min_timing else min_timing
            max_timming = max_t if max_t > max_timming else max_timming
            plt.plot(player.timestamps, player.stacks, label=username)

        plt.legend()
        # plt.yticks(range(10), [min_stack + (max_stack - min_stack) * i / 10 for i in range(10)])
        plt.ylim((0, 10000))

        plt.plot()
        # plt.xticks(range(20), [min_timing + (max_timming - min_timing) * i / 20 for i in range(20)])

        # xfmt = md.AutoDateFormatter('%Y-%m-%d %H:%M:%S')
        # ax = plt.gca()
        # ax.xaxis.set_major_formatter(xfmt)

        plt.show()

files = ["log.csv", "log2.csv"]

content = []
for file_name in files:
    file = open(file_name, "r")
    for line in file:
        if "Player stacks" in line or "will start to play in this table" in line and "stack of 1000" not in line:
            content.append(line)

player_list = PlayerList()
for line in content:
    player_list.add_line(line)

player_list.draw()

pass