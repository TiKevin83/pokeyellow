Random_::
IF DEF(_BUGFIX)
; use the more thorough prng to minimize rng correlation effects
	call XorshiftRandom
	ldh [hRandomAdd], a
	call XorshiftRandom
	ldh [hRandomSub], a
	ret
ELSE
; Generate a random 16-bit value.
	ldh a, [rDIV]
	ld b, a
	ldh a, [hRandomAdd]
	adc b
	ldh [hRandomAdd], a
	ldh a, [rDIV]
	ld b, a
	ldh a, [hRandomSub]
	sbc b
	ldh [hRandomSub], a
	ret
ENDC

IF DEF(_BUGFIX)
; luckytyphlosion implementation of xorshift prng
; ported from https://github.com/edrosten/8bit_rng
XorshiftRandom:
    push bc
    ldh a, [rDIV]
    rra ; shift into carry
    ld hl, wRandomSeed
    ld a, [hl] ; read in x
    ; x << 4
    add a
    add a
    add a
    adc a ; this mixes in 1 bit of rDIV into RNG
    xor [hl]
    ld b, a ; t = x ^ (x << 4)
    ld hl, wRandomSeed + 3
    ld a, [hld] ; read in a ; hl = +2
    ld c, [hl] ; read in z ; hl = +2
    ld [hld], a ; z = a ; hl = +1
    ld a, c
    ld c, [hl] ; read in y
    ld [hld], a ; y = old z
    ld [hl], c ; x = y 
    ld c, a
    ; hl = y
    ; vars
    ; b contains t
    ; a/c contains z
    xor b ; z ^ t
    rr c ; (z >> 1)
    xor c ; z ^ t ^ (z >> 1)
    rl b ; (t << 1)
    xor b ; z ^ t ^ (z >> 1) ^ (t << 1)
    ld [wRandomSeed + 3], a
    pop bc
    ret
ENDC
