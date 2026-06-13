import random
import math

class CoupledVoid:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.v = 0.0
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

class VoidPair:
    def __init__(self, seed1=1, seed2=2):
        self.A = CoupledVoid(seed1)
        self.B = CoupledVoid(seed2)

    def step(self):
        a_state = self.A.step(self.B)
        b_state = self.B.step(self.A)
        return {
            "A": a_state,
            "B": b_state,
            "delta_v": abs(self.A.v - self.B.v)
        }

    def run(self, steps=50):
        return [self.step() for _ in range(steps)]