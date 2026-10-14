"""Run compiled BUGFIX=1 bounds/arithmetic/state regressions with PyBoy.

Usage: python tests/hardening.py pokeyellow.gbc
Requires pyboy==2.8.1 and the matching .sym file. The CPU executes the actual
ROM routines; only presentation routines are stubbed by this harness.
"""

import argparse
from pathlib import Path
import unittest

from substitute import BattleRoutines


class HardeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cpu = BattleRoutines(ROM)
        for label in ('Delay3', 'UpdateSprites', 'DisplayTextID',
                      'SafariZoneEntranceAutoWalk'):
            cls.cpu.patch(label, [0xc9])

    @classmethod
    def tearDownClass(cls):
        cls.cpu.game.stop(save=False)

    def setUp(self):
        self.cpu.reset(0)

    def test_follow_buffer_saturates_without_wraparound(self):
        b = self.cpu
        start = b.address('wPikachuFollowCommandBuffer')
        end = b.address('wPikachuFollowCommandBufferEnd')
        b.game.memory[start - 8:end + 256] = [0xa5] * (end + 256 - start + 8)
        b.run('ClearPikachuFollowCommandBuffer')
        for i in range(600):
            b.game.register_file.A = i % 4 + 1
            b.run('AppendPikachuFollowCommandToBuffer')
            self.assertEqual(b.get('wPikachuFollowCommandBufferSize'), min(i, 15))
        self.assertEqual(b.game.memory[start:end], [1, 2, 3, 4] * 4)
        self.assertEqual(b.game.memory[start - 8:start - 1], [0xa5] * 7)
        self.assertEqual(b.game.memory[end:end + 256], [0xa5] * 256)
        # Space freed by the consumer must be reusable.
        b.run('Func_fcc92')
        self.assertEqual(b.game.register_file.A, 1)
        self.assertEqual(b.get('wPikachuFollowCommandBufferSize'), 14)
        b.game.register_file.A = 8
        b.run('AppendPikachuFollowCommandToBuffer')
        self.assertEqual(b.game.memory[start:end], ([1, 2, 3, 4] * 4)[1:] + [8])

    def test_follow_buffer_rejects_every_invalid_index(self):
        b = self.cpu
        start = b.address('wPikachuFollowCommandBuffer')
        b.game.memory[start:start + 256] = [0xa5] * 256
        for size in range(16, 256):
            with self.subTest(size=size):
                b.set('wPikachuFollowCommandBufferSize', size)
                for reader in ('GetPikachuFollowCommand',
                               'GetPikachuFollowCommandIfBufferSizeNonzero'):
                    b.run(reader)
                    self.assertEqual(b.game.register_file.A, 0)
                b.run('AreThereAtLeastTwoStepsInPikachuFollowCommandBuffer')
                self.assertFalse(b.game.register_file.F & 0x10)
                b.run('Func_fcc92')
                self.assertTrue(b.game.register_file.F & 0x10)
                self.assertEqual(b.get('wPikachuFollowCommandBufferSize'), size)
                self.assertEqual(b.game.memory[start:start + 256], [0xa5] * 256)
                b.game.register_file.A = 3
                b.run('AppendPikachuFollowCommandToBuffer')
                if size == 255:  # Empty sentinel is the only valid wrap to zero.
                    self.assertEqual(b.get('wPikachuFollowCommandBufferSize'), 0)
                    self.assertEqual(b.game.memory[start], 3)
                else:
                    self.assertEqual(b.get('wPikachuFollowCommandBufferSize'), size)
                    self.assertEqual(b.game.memory[start:start + 256], [0xa5] * 256)

    def test_follow_buffer_valid_readers_and_consumer(self):
        b = self.cpu
        start = b.address('wPikachuFollowCommandBuffer')
        for size in range(16):
            with self.subTest(size=size):
                b.set('wPikachuFollowCommandBufferSize', size)
                b.game.memory[start:start + 16] = list(range(1, 17))
                b.run('GetPikachuFollowCommand')
                self.assertEqual(b.game.register_file.A, size + 1)
                b.run('GetPikachuFollowCommandIfBufferSizeNonzero')
                self.assertEqual(b.game.register_file.A, size + 1 if size else 0)
                b.run('AreThereAtLeastTwoStepsInPikachuFollowCommandBuffer')
                self.assertEqual(bool(b.game.register_file.F & 0x10), size >= 2)
                b.run('Func_fcc92')
                self.assertEqual(b.get('wPikachuFollowCommandBufferSize'), max(size - 1, 0))
                if size:
                    self.assertEqual(b.game.register_file.A, 1)
                    self.assertEqual(b.game.memory[start:start + size + 1],
                                     list(range(2, size + 2)) + [255])

    def test_transition_never_scans_beyond_party(self):
        b = self.cpu
        stride = b.address('wPartyMon2') - b.address('wPartyMon1')
        for count in (0, 1, 2, 3, 4, 5, 6, 7, 255):
            with self.subTest(count=count):
                b.reset(0)
                b.set('wPartyCount', count)
                b.set('wCurEnemyLevel', 5)
                # Poison data immediately outside the declared party. The old
                # unbounded scan would find a fake, high-level conscious mon.
                offset = min(count, 6) * stride
                b.game.memory[b.address('wPartyMon1HP') + offset] = 1
                b.game.memory[b.address('wPartyMon1Level') + offset] = 100
                b.game.register_file.C = 5
                b.run('GetBattleTransitionID_CompareLevels')
                self.assertEqual(b.game.register_file.B, 0)
                self.assertEqual(b.game.register_file.C, 7)
                self.assertEqual(b.get('wBattleTransitionSpiralDirection'), 0)

    def test_transition_uses_first_conscious_member_and_level_boundary(self):
        b = self.cpu
        stride = b.address('wPartyMon2') - b.address('wPartyMon1')
        for slot in range(6):
            for enemy_level in (12, 13):
                b.reset(0)
                b.set('wPartyCount', 6)
                b.set('wCurEnemyLevel', enemy_level)
                b.game.memory[b.address('wPartyMon1HP') + slot * stride + 1] = 1
                b.game.memory[b.address('wPartyMon1Level') + slot * stride] = 10
                b.game.register_file.C = 7
                b.run('GetBattleTransitionID_CompareLevels')
                self.assertEqual(b.game.register_file.B, 0)
                self.assertEqual(b.game.register_file.C, 7 if enemy_level == 13 else 5)
                self.assertEqual(b.get('wBattleTransitionSpiralDirection'), int(enemy_level < 13))

    def decrement_pp(self):
        b = self.cpu
        b.set('wPlayerSelectedMove', 1)
        address = b.address('wPlayerSelectedMove')
        b.game.register_file.D = address >> 8
        b.game.register_file.E = address & 255
        b.run('DecrementPP')

    def test_pp_saturates_preserving_pp_ups_and_transform(self):
        b = self.cpu
        for transformed in (False, True):
            for slot in range(4):
                for pp in range(256):
                    b.reset(0)
                    b.set('wPlayerBattleStatus3', 8 if transformed else 0)
                    b.set('wPlayerMoveListIndex', slot)
                    b.set('wPlayerMonNumber', 5)
                    battle_pp = b.address('wBattleMonPP')
                    party_pp = b.address('wPartyMon6PP')
                    b.game.memory[battle_pp:battle_pp + 4] = [pp] * 4
                    b.game.memory[party_pp:party_pp + 4] = [pp] * 4
                    self.decrement_pp()
                    expected = [pp] * 4
                    expected[slot] = (pp & 0xc0) | max((pp & 63) - 1, 0)
                    self.assertEqual(b.game.memory[battle_pp:battle_pp + 4], expected)
                    self.assertEqual(b.game.memory[party_pp:party_pp + 4],
                                     [pp] * 4 if transformed else expected)

    def test_pp_invalid_move_and_party_indices_do_not_write_outside_slots(self):
        b = self.cpu
        for slot in (4, 255):
            b.set('wPlayerMoveListIndex', slot)
            # Selected move is the only expected write from the test helper.
            b.set('wPlayerSelectedMove', 1)
            before = b.game.memory[0xc000:0xdf00]
            self.decrement_pp()
            self.assertEqual(b.game.memory[0xc000:0xdf00], before)
        party_start = b.address('wPartyMon1')
        party_end = party_start + 6 * (b.address('wPartyMon2') - party_start)
        for party in (6, 255):
            b.set('wPlayerMoveListIndex', 0)
            b.set('wPlayerMonNumber', party)
            b.set('wBattleMonPP', 1)
            before = b.game.memory[party_start:party_end]
            self.decrement_pp()
            self.assertEqual(b.get('wBattleMonPP'), 0)
            self.assertEqual(b.game.memory[party_start:party_end], before)

    def test_damage_scaling_and_divisor_boundaries_on_both_sides(self):
        b = self.cpu
        for turn in (0, 1):
            attacker, target = ('wBattleMon', 'wEnemyMon') if turn == 0 else ('wEnemyMon', 'wBattleMon')
            side = 'wPlayer' if turn == 0 else 'wEnemy'
            target_side = 'wEnemy' if turn == 0 else 'wPlayer'
            for special in (False, True):
                for screen in (False, True):
                    for attack in (1, 3, 255, 256, 999):
                        for defense in (1, 2, 3, 4, 255, 256, 499, 500, 511, 512, 999):
                            with self.subTest(turn=turn, special=special, screen=screen,
                                              attack=attack, defense=defense):
                                b.reset(turn)
                                b.set_hp(attacker + ('Special' if special else 'Attack'), attack)
                                b.set_hp(target + ('Special' if special else 'Defense'), defense)
                                b.set(side + 'MovePower', 80)
                                b.set(side + 'MoveType', 20 if special else 0)
                                b.set(attacker + 'Level', 50)
                                b.set(target_side + 'BattleStatus3', (2 if special else 4) if screen else 0)
                                b.run('GetDamageVarsForPlayerAttack' if turn == 0 else 'GetDamageVarsForEnemyAttack')
                                capped = min(defense * (2 if screen else 1), 999)
                                scale = 4 if max(attack, capped) > 255 else 1
                                a, d = max(attack // scale, 1), capped // scale
                                self.assertEqual(b.game.register_file.B, a)
                                self.assertEqual(b.game.register_file.C, d)
                                b.run('CalculateDamage')
                                expected = min(((22 * 80 * a) // max(d, 1)) // 50, 997) + 2
                                self.assertEqual(b.hp('wDamage'), expected)

    def test_safari_restore_uses_saved_event_not_scratch_byte(self):
        b = self.cpu
        event = b.address('wEventFlags') + 0x24f // 8
        for active in (False, True):
            for scratch in (0, 5, 255):
                for moving in (0, 1):
                    with self.subTest(active=active, scratch=scratch, moving=moving):
                        b.reset(0)
                        b.game.memory[event] = 0x35 | (0x80 if active else 0)
                        b.set('wSafariZoneGateCurScript', 6)
                        b.set('wNextSafariZoneGateScript', scratch)
                        b.set('wSimulatedJoypadStatesIndex', moving)
                        b.run('SafariZoneGateSetScriptAfterMoveScript')
                        self.assertEqual(b.get('wSafariZoneGateCurScript'),
                                         6 if moving else (5 if active else 0))
                        self.assertEqual(b.game.memory[event], 0x35 | (0x80 if active else 0))

    def test_safari_game_over_clears_both_step_bytes(self):
        b = self.cpu
        event = b.address('wEventFlags') + 0x24f // 8
        b.game.memory[event] = 0xc0  # Game over and in Safari Zone.
        b.set_hp('wSafariSteps', 0x1234)
        b.set('wNumSafariBalls', 15)
        b.run('SafariZoneGateLeavingSafariScript')
        self.assertEqual(b.hp('wSafariSteps'), 0)
        self.assertEqual(b.get('wNumSafariBalls'), 0)
        self.assertEqual(b.game.memory[event], 0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom', type=Path)
    ROM = parser.parse_args().rom.resolve()
    unittest.main(argv=[__file__], verbosity=2)
