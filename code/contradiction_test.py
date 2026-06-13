import random
import math

class CoupledVoid:
    def __init__(self, seed=None, initial_v=0.0):
        self.rng = random.Random(seed)
        self.v = initial_v
        self.a = 0.5
        self.residue = 0.0

    def step(self, other):
        noise_v = self.rng.uniform(-1, 1) * 0.2
        noise_a = self.rng.uniform(-1, 1) * 0.1
        interaction = (other.v - self.v)
        memory = math.tanh(self.residue)
        self.v += noise_v + 0.15 * interaction + 0.1 * memory
        self.a += noise_a
        self.v = max(-2.5, min(2.5, self.v))
        self.a = max(0.0, min(1.0, self.a))
        self.residue = self.residue * 0.9 + self.v * 0.05
        return {"v": self.v, "a": self.a, "r": self.residue}

class ContradictionPair:
    def __init__(self, seed1=101, seed2=102):
        self.A = CoupledVoid(seed1, initial_v=1.0)  # Truth side
        self.B = CoupledVoid(seed2, initial_v=-1.0)  # Contradiction side

    def step(self):
        a_state = self.A.step(self.B)
        b_state = self.B.step(self.A)
        return {
            "A": a_state,
            "B": b_state,
            "delta_v": abs(self.A.v - self.B.v),
            "sum_activation": self.A.v + self.B.v
        }

    def run(self, steps=40):
        return [self.step() for _ in range(steps)]

# Demo run
if __name__ == "__main__":
    pair = ContradictionPair()
    history = pair.run(steps=40)
    print("Final delta_v:", history[-1]["delta_v"])
    print("Final sum_activation:", history[-1]["sum_activation"])