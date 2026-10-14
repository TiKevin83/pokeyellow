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
; State is (x, y, z, w). Return the next byte in a; clobber bc and hl.
; Random preserves the caller's registers, so no nested save is needed here.
; C notation below treats a, b, c as uint8_t and hl as uint8_t *p.
; Arithmetic/left shifts truncate to 8 bits; x, y, z, w denote the old state.
	ld hl, wRandomSeed ; p = &state[0];                      // &x
	ld a, [hli]       ; a = *p++;                           // a = x; p = &y
	ld b, a           ; b = a;                              // save x
	add a             ; a <<= 1;                            // x << 1
	add a             ; a <<= 1;                            // x << 2
	add a             ; a <<= 1;                            // x << 3
	add a             ; a <<= 1;                            // x << 4
	xor b             ; a ^= b;                             // x ^ (x << 4)
	ld b, a           ; b = a;                              // b = t
	ld a, [hld]       ; a = *p--;                           // a = y; p = &x
	ld [hli], a       ; *p++ = a;                           // state[0] = y; p = &y
	inc hl            ; ++p;                                // p = &z
	ld a, [hld]       ; a = *p--;                           // a = z; p = &y
	ld [hli], a       ; *p++ = a;                           // state[1] = z; p = &z
	inc hl            ; ++p;                                // p = &w
	ld a, [hld]       ; a = *p--;                           // a = w; p = &z
	ld [hli], a       ; *p++ = a;                           // state[2] = w; p = &w
	ld c, a           ; c = a;                              // save w for right shift
	xor b             ; a ^= b;                             // w ^ t
	srl c             ; c >>= 1;                            // w >> 1 (zero-fill)
	xor c             ; a ^= c;                             // w ^ t ^ (w >> 1)
	sla b             ; b <<= 1;                            // t << 1
	xor b             ; a ^= b;                             // w ^ t ^ (w >> 1) ^ (t << 1)
	ld [hl], a        ; *p = a;                             // state[3] = new w
	ret               ; return a;
ENDC
