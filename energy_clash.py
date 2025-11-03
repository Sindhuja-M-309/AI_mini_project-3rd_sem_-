import random

NUM_CELLS = 5
START_ENERGY = 100

class Player:
    def __init__(self, name):
        self.name = name
        self.energy = START_ENERGY
        self.allocation = [0] * NUM_CELLS

    def allocate_energy(self):
        pass

class Human(Player):
    def allocate_energy(self):
        print(f"\n⚡ {self.name}, you have {self.energy} energy points.")
        allocations = []
        remaining = self.energy
        for i in range(NUM_CELLS):
            while True:
                try:
                    amt = int(input(f"Allocate energy to position {i+1} (remaining {remaining}): "))
                    if 0 <= amt <= remaining:
                        allocations.append(amt)
                        remaining -= amt
                        break
                    else:
                        print("❌ Invalid amount.")
                except ValueError:
                    print("❌ Enter a number.")
        self.allocation = allocations
        print(f"{self.name} allocation: {self.allocation}\n")

class AI(Player):
    def __init__(self, name):
        super().__init__(name)
        self.previous_alloc = [random.randint(0, 20) for _ in range(NUM_CELLS)]

    def allocate_energy(self):
        """Hill climbing: small tweaks to previous allocation"""
        new_alloc = self.previous_alloc[:]
        for i in range(NUM_CELLS):
            change = random.choice([-5, 0, 5])
            new_alloc[i] = max(0, min(new_alloc[i] + change, 40))
        total = sum(new_alloc)
        # Normalize to total energy
        if total > 0:
            new_alloc = [int(x / total * START_ENERGY) for x in new_alloc]
        else:
            new_alloc = [0]*NUM_CELLS
        self.previous_alloc = new_alloc
        self.allocation = new_alloc
        print(f"🤖 {self.name} has made its move.")
        return new_alloc

def resolve_battle(human, ai):
    print("\n🏁 Battle Results:")
    human_score = 0
    ai_score = 0

    for i in range(NUM_CELLS):
        h = human.allocation[i]
        a = ai.allocation[i]
        if h > a:
            human_score += 1
            winner = human.name
        elif a > h:
            ai_score += 1
            winner = ai.name
        else:
            winner = "Draw"
        print(f"  Cell {i+1}: {human.name}({h}) vs {ai.name}({a}) → {winner}")

    print(f"\n🔹 {human.name} controls {human_score} cells.")
    print(f"🔸 {ai.name} controls {ai_score} cells.")

    if human_score > ai_score:
        print(f"🎉 {human.name} WINS the round!\n")
    elif ai_score > human_score:
        print(f"🤖 {ai.name} WINS the round!\n")
    else:
        print("⚖️ It’s a tie!\n")

def play_game():
    print("⚔️ Welcome to ENERGY CLASH ⚔️")
    print("You and the AI allocate energy to 5 positions. Highest energy wins each cell.")
    print("Win 3 out of 5 cells to claim victory!\n")

    human = Human("Player")
    ai = AI("AI-Bot")

    play_again = "y"
    while play_again.lower() == "y":
        human.allocate_energy()
        ai.allocate_energy()
        resolve_battle(human, ai)
        play_again = input("Play again? (y/n): ")

if __name__ == "__main__":
    play_game()
