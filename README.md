# Pokémon Yellow Fort Knox Edition [![Build Status][ci-badge]][ci]

This is a disassembly of Pokémon Yellow.

It builds the following ROMs:

- Pokemon Yellow (UE) [C][!].gbc  `sha1: cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1`
- YELLMONS.GB (debug build) `sha1: d44e96eddfbdad633cbe4e6e64915e9e198974b0`
- Dmgapse0.h08.patch `sha1: f3346a5559d52c296b8feab0cdbbfb0e250ac161`

To set up the repository, see [**INSTALL.md**](INSTALL.md).

## Fort Knox Edition

This version includes the ability to optionally compile with a set of bugfix patches I'm calling Fort Knox Edition:

`make BUGFIX=1`

Use `make BUGFIX=0` (or plain `make`) for the original behavior. Switching
`BUGFIX` automatically rebuilds the objects, so no clean is needed. This also
applies to the debug and Virtual Console targets.

The latest memory bounds, arithmetic, and saved-state fixes are documented in
[Bugfix hardening](docs/bugfix-hardening.md), including emulator regression tests.

Many of these patches are sourced from the research done on [pokered](https://github.com/pret/pokered/wiki/%5BARCHIVED%5D-Bugs-and-Glitches) which is now defunct and archived. Some patches were also written specifically for this project (badge boosts, fast options) and some were collaborations with other Pokemon Speedrun community members including CasualPokePlayer and luckytyphlosion (statistically validated PRNG).

## See also

- [**Wiki**][wiki] (includes [tutorials][tutorials])
- [**Symbols**][symbols]
- [**Tools**][tools]

You can find us on [Discord (pret, #pokered)](https://discord.gg/d5dubZ3).

For other pret projects, see [pret.github.io](https://pret.github.io/).

[wiki]: https://github.com/pret/pokeyellow/wiki
[tutorials]: https://github.com/pret/pokeyellow/wiki/Tutorials
[symbols]: https://github.com/pret/pokeyellow/tree/symbols
[tools]: https://github.com/pret/gb-asm-tools
[ci]: https://github.com/pret/pokeyellow/actions
[ci-badge]: https://github.com/pret/pokeyellow/actions/workflows/main.yml/badge.svg
