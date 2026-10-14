"""Check the compiled BUGFIX=1 PRNG's sequence and public register contract.

Build with `make BUGFIX=1`, install pyboy==2.8.1, then run
`python tests/xorshift.py pokeyellow.gbc`. The matching .sym file is required.
The shared harness stubs presentation and BattleRandom, but these tests execute
the real XorshiftRandom, Random_, and Random routines without patching them.
"""

import argparse
from pathlib import Path
import random
import unittest

from substitute import BattleRoutines


def next_state(state):
    x, y, z, w = state
    t = x ^ ((x << 4) & 255)
    return [y, z, w, (w ^ (w >> 1) ^ t ^ (t << 1)) & 255]


class XorshiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cpu = BattleRoutines(ROM)

    @classmethod
    def tearDownClass(cls):
        cls.cpu.game.stop(save=False)

    def prepare(self, state):
        cpu = self.cpu
        cpu.reset(0)
        address = cpu.address('wRandomSeed')
        cpu.game.memory[address - 1:address + 5] = [0xa5] + state + [0x5a]
        cpu.set('hRandomAdd', 0x34)
        cpu.set('hRandomSub', 0x56)
        return address

    def test_state_and_outputs_through_all_entry_points(self):
        rng = random.Random(0)
        # Every basis bit checks the linear transformation, supplemented by
        # mixed-bit inputs and the zero/all-ones boundaries.
        seeds = [0, 0xffffffff] + [1 << bit for bit in range(32)]
        seeds += [rng.getrandbits(32) for _ in range(1000)]
        cpu = self.cpu
        for entry in ('XorshiftRandom', 'Random_', 'Random'):
            for seed in seeds:
                with self.subTest(entry=entry, seed=seed):
                    state = list(seed.to_bytes(4, 'little'))
                    address = self.prepare(state)
                    first = next_state(state)
                    second = next_state(first)
                    cpu.run(entry)
                    expected = first if entry == 'XorshiftRandom' else second
                    self.assertEqual(cpu.game.memory[address:address + 4], expected)
                    output = second[3] if entry == 'Random_' else first[3]
                    self.assertEqual(cpu.game.register_file.A, output)
                    self.assertEqual(cpu.get('hRandomAdd'),
                                     0x34 if entry == 'XorshiftRandom' else first[3])
                    self.assertEqual(cpu.get('hRandomSub'),
                                     0x56 if entry == 'XorshiftRandom' else second[3])
                    self.assertEqual(cpu.game.memory[address - 1], 0xa5)
                    self.assertEqual(cpu.game.memory[address + 4], 0x5a)

    def test_sequence_captured_before_optimization(self):
        self.prepare([0x12, 0x34, 0x56, 0x78])
        expected = bytes.fromhex(
            '12 87 9e d9 e3 8b 4c b1 9c 9f 44 85 23 83 ce d6 '
            '88 19 67 8e d1 22 0a bd a0 f6 73 fd 63 e8 59 02'
        )
        actual = []
        for _ in expected:
            self.cpu.run('XorshiftRandom')
            actual.append(self.cpu.game.register_file.A)
        self.assertEqual(bytes(actual), expected)

    def test_public_random_preserves_registers_across_repeated_calls(self):
        state = [0x12, 0x34, 0x56, 0x78]
        address = self.prepare(state)
        registers = {'B': 0x12, 'C': 0x34, 'D': 0x56, 'E': 0x78, 'HL': 0xabcd}
        for register, value in registers.items():
            setattr(self.cpu.game.register_file, register, value)
        for _ in range(256):
            first = next_state(state)
            state = next_state(first)
            self.cpu.run('Random')
            self.assertEqual(self.cpu.game.register_file.A, first[3])
            self.assertEqual(self.cpu.game.memory[address:address + 4], state)
            for register, value in registers.items():
                self.assertEqual(getattr(self.cpu.game.register_file, register), value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom', type=Path)
    ROM = parser.parse_args().rom.resolve()
    unittest.main(argv=[__file__], verbosity=2)
