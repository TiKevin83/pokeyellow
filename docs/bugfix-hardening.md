# Bugfix hardening

These changes address memory bounds, arithmetic overflow/underflow, and state
restoration bugs described in [the TCRF bug notes](tcrf-bugs.md). All runtime
changes are conditional on `_BUGFIX`, enabled by `make BUGFIX=1`.

| Bug | Guarded behavior |
| --- | --- |
| Pikachu off-screen / Pikawalk | The 16-command buffer stops accepting commands when full without incrementing its last-entry index. It cannot wrap after 256 steps. Readers and the shifting consumer reject indices outside the allocation; `$ff` remains the empty sentinel. Queued commands are retained and space becomes reusable as Pikachu consumes them. |
| Battle transition party overread | The level comparison only scans the declared party. Empty parties, all-fainted parties, and counts above six use the stronger-enemy transition without reading unrelated RAM. |
| Binding move PP underflow | PP subtraction stops at zero and preserves PP Up bits in both battle and party data. Move indices outside 0–3 and party indices outside 0–5 cannot index past their arrays. Transformed Pokémon still only spend battle PP. |
| Reflect / Light Screen overflow | Both sides cap the defensive stat at the existing 999 stat limit before narrowing it for damage calculation. This prevents doubled defenses from wrapping around the ten-bit scaling range. |
| Damage division by zero | Damage calculation raises a zero defensive divisor to one, including when dividing a defense of 1–3 by four rounded it down to zero. |
| Safari Zone save/reset glitch | After automatic movement, the gate reconstructs its next script from the saved `EVENT_IN_SAFARI_ZONE` flag instead of unsaved scratch RAM. Game-over cleanup also clears both bytes of the remaining step count. |

The Substitute corrections are also guarded: exact-cost
Substitute fails without reducing the user to zero HP, and draining moves fail
against a Substitute. Their regression suite is retained.

This is an incremental set of fixes, not a claim that every entry in the source
notes is resolved. In particular, PP saturation does not address the separate
freeze/link move-selection desync; the screen cap does not change Reflect's
interaction with confusion. The tests execute individual ROM routines and do
not replace a full gameplay or two-console link test.

## Building both modes

```sh
make BUGFIX=1 all yellow_vc
make BUGFIX=0 compare
make BUGFIX=1 all yellow_vc
```

The build records the effective `BUGFIX` and `DEBUG` settings in an ignored
`.build-config` file. Switching either setting invalidates all ROM object
variants; repeating the same settings leaves them up to date. `BUGFIX` defaults
to off. Off builds retain the original release/debug ROM and VC patch hashes
checked by `make compare`.

## Regression tests

With RGBDS installed as described in [INSTALL.md](../INSTALL.md):

```sh
python3 -m venv /tmp/pokeyellow-tests
/tmp/pokeyellow-tests/bin/pip install pyboy==2.8.1
make BUGFIX=1 all yellow_vc
/tmp/pokeyellow-tests/bin/python tests/hardening.py pokeyellow.gbc
/tmp/pokeyellow-tests/bin/python tests/substitute.py pokeyellow.gbc
```

The matching `.sym` file must be beside each ROM. The hardening suite can also
run against `pokeyellow_debug.gbc` and `pokeyellow_vc.gbc`. It exercises actual
assembled routines with presentation calls stubbed, including 600 queued
steps, every invalid follow-buffer index, every PP byte value (including PP Up
bits), both battle sides, physical/special damage and screen boundaries,
party scan limits, and Safari state restoration with cleared/stale scratch RAM.
