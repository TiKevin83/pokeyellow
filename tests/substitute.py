"""Exercise Substitute battle routines in a BUGFIX=1 ROM using PyBoy.

Build with `make BUGFIX=1` in a clean build directory, install pyboy==2.8.1,
then run `python tests/substitute.py /path/to/pokeyellow.gbc`.
The matching .sym file must sit beside the ROM. Only presentation routines
and the random roll are stubbed; the assembled battle logic runs on the CPU.
"""

import argparse
from pathlib import Path
import unittest

from pyboy import PyBoy


SUBSTITUTE = 1 << 4
INVULNERABLE = 1 << 6
TRAPPING = 1 << 5
X_ACCURACY = 1
DRAIN = 3
DREAM_EATER = 8
SWIFT = 17


class BattleRoutines:
    def __init__(self, rom):
        self.game = PyBoy(
            str(rom), symbols=str(rom.with_suffix('.sym')),
            window='null', sound_emulated=False, log_level='ERROR',
        )
        self.game.symbol_lookup('wScaledPlayerMoveAccuracy')  # BUGFIX=1 build
        self.game.memory[0xff50] = 1  # Disable the boot ROM.
        self.game.memory[0, 0x100:0x102] = [0x18, 0xfe]  # Return trap: jr -2
        for label in ('DelayFrames', 'SubstituteEffect_.animationEnabled',
                      'SubstituteEffect_.printText'):
            self.patch(label, [0xc9])  # ret: omit waits, animation, and text
        self.patch('BattleRandom', [0xaf, 0xc9])  # xor a; ret: deterministic hit

    def patch(self, label, code):
        bank, address = self.game.symbol_lookup(label)
        self.game.memory[bank, address:address + len(code)] = code

    def address(self, label):
        return self.game.symbol_lookup(label)[1]

    def reset(self, turn):
        self.game.memory[0xc000:0xe000] = [0] * 0x2000
        self.game.memory[0xff80:0x10000] = [0] * 0x80  # Includes interrupt enable.
        for register in ('A', 'F', 'B', 'C', 'D', 'E', 'HL'):
            setattr(self.game.register_file, register, 0)
        self.set('hWhoseTurn', turn)

    def set(self, label, value):
        self.game.memory[self.address(label)] = value

    def get(self, label):
        return self.game.memory[self.address(label)]

    def set_hp(self, label, value):
        address = self.address(label)
        self.game.memory[address:address + 2] = [value >> 8, value & 255]

    def hp(self, label):
        address = self.address(label)
        return self.game.memory[address] * 256 + self.game.memory[address + 1]

    def run(self, label):
        bank, address = self.game.symbol_lookup(label)
        self.game.memory[0x2000] = bank
        self.game.memory[0x3000] = 0
        self.set('hLoadedROMBank', bank)
        self.game.memory[0xdff0:0xdff2] = [0, 1]  # Return address: $0100
        self.game.register_file.SP = 0xdff0
        self.game.register_file.PC = address
        self.game.tick(1, False, False)
        if (self.game.register_file.PC, self.game.register_file.SP) != (0x100, 0xdff2):
            raise AssertionError(f'{label} did not return with a balanced stack')


class SubstituteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.battle = BattleRoutines(ROM)

    @classmethod
    def tearDownClass(cls):
        cls.battle.game.stop(save=False)

    def test_hp_cost_and_boundaries(self):
        # Full health, cost +/- 1, rounding, byte borrow, and 255/256 boundaries.
        cases = [(100, 100), (100, 26), (100, 25), (100, 24),
                 (101, 26), (101, 25), (400, 356), (400, 355),
                 (400, 256), (400, 100), (400, 99), (800, 600),
                 (1023, 1023), (1023, 256), (1023, 255), (1023, 254)]
        b = self.battle
        for turn in (0, 1):
            mon, side = ('wBattleMon', 'wPlayer') if turn == 0 else ('wEnemyMon', 'wEnemy')
            other_mon, other_side = ('wEnemyMon', 'wEnemy') if turn == 0 else ('wBattleMon', 'wPlayer')
            for max_hp, hp in cases:
                with self.subTest(turn=turn, max_hp=max_hp, hp=hp):
                    b.reset(turn)
                    b.set_hp(mon + 'HP', hp)
                    b.set_hp(mon + 'MaxHP', max_hp)
                    b.set(side + 'BattleStatus2', 2)  # Preserve an unrelated flag.
                    b.set_hp(other_mon + 'HP', 500)
                    b.run('SubstituteEffect_')
                    cost = max_hp // 4
                    success = hp > cost
                    self.assertEqual(b.hp(mon + 'HP'), hp - cost if success else hp)
                    self.assertEqual(b.get(side + 'BattleStatus2'), 2 | (SUBSTITUTE if success else 0))
                    self.assertEqual(b.hp(other_mon + 'HP'), 500)
                    self.assertEqual(b.get(other_side + 'BattleStatus2'), 0)
                    if success:
                        self.assertEqual(b.get(side + 'SubstituteHP'), cost)
                    else:
                        self.assertEqual(b.game.register_file.HL, b.address('TooWeakSubstituteText'))

    def test_existing_substitute_does_not_charge_hp(self):
        b = self.battle
        for turn in (0, 1):
            with self.subTest(turn=turn):
                b.reset(turn)
                mon, side = ('wBattleMon', 'wPlayer') if turn == 0 else ('wEnemyMon', 'wEnemy')
                b.set_hp(mon + 'HP', 100)
                b.set_hp(mon + 'MaxHP', 100)
                b.set(side + 'BattleStatus2', SUBSTITUTE)
                b.set(side + 'SubstituteHP', 17)
                b.run('SubstituteEffect_')
                self.assertEqual(b.hp(mon + 'HP'), 100)
                self.assertEqual(b.get(side + 'SubstituteHP'), 17)
                self.assertEqual(b.game.register_file.HL, b.address('HasSubstituteText'))

    def test_hit_checks(self):
        b = self.battle
        for turn in (0, 1):
            attacker, target = ('wPlayer', 'wEnemy') if turn == 0 else ('wEnemy', 'wPlayer')
            status = 'wEnemyMonStatus' if turn == 0 else 'wBattleMonStatus'
            for effect in (0, DRAIN, DREAM_EATER, SWIFT):
                for substitute in (False, True):
                    for sleeping in (False, True):
                        for invulnerable in (False, True):
                            for x_accuracy in (False, True):
                                with self.subTest(turn=turn, effect=effect, substitute=substitute,
                                                  sleeping=sleeping, invulnerable=invulnerable,
                                                  x_accuracy=x_accuracy):
                                    b.reset(turn)
                                    b.set(attacker + 'MoveEffect', effect)
                                    # A different effect on the other side catches turn mixups.
                                    b.set(target + 'MoveEffect', DRAIN if effect == 0 else 0)
                                    b.set(target + 'BattleStatus2', SUBSTITUTE if substitute else 0)
                                    b.set(target + 'BattleStatus1', INVULNERABLE if invulnerable else 0)
                                    b.set(attacker + 'BattleStatus1', TRAPPING)
                                    b.set(attacker + 'BattleStatus2', X_ACCURACY if x_accuracy else 0)
                                    b.set(status, 1 if sleeping else 0)
                                    for side in ('wPlayer', 'wEnemy'):
                                        b.set(side + 'MoveAccuracy', 255)
                                        b.set(side + 'MonAccuracyMod', 7)
                                        b.set(side + 'MonEvasionMod', 7)
                                    b.set_hp('wDamage', 37)
                                    b.run('MoveHitTest')
                                    missed = effect != SWIFT and (
                                        invulnerable or (effect == DREAM_EATER and not sleeping)
                                        or (substitute and effect in (DRAIN, DREAM_EATER)))
                                    self.assertEqual(b.get('wMoveMissed'), int(missed))
                                    self.assertEqual(b.hp('wDamage'), 0 if missed else 37)
                                    self.assertEqual(b.get(attacker + 'BattleStatus1'), 0 if missed else TRAPPING)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom', type=Path)
    ROM = parser.parse_args().rom.resolve()
    unittest.main(argv=[__file__], verbosity=2)
