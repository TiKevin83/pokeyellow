Vermilion Gym Trash Can bug

The algorithm that randomizes the position of the switches in the trash cans in Vermilion Gym has been completely rewritten in Yellow to avoid the problem of the algorithm from Red/Blue being essentially predeterministic. That doesn't mean that Yellow's algorithm is bug-free, though.

If there are three adjacent trash cans (i. e. the first switch was in one of the trash cans at the borders), the algorithm that determines where the second switch should be accidentally writes its result to the wrong register, and as a result that value is never used and instead data from the rest of the table or the zero padding past the end of the ROM bank is read as the data for the second switch. As a result, the second switch will either be in the top left trash can (highest probability), in any of the other trash cans in the gym, or, if you're extremely unlucky (a 1/256 or 1/128 chance, depending on where the first switch was), the puzzle will become unsolvable as there will be no second switch whatsoever.
Battle Transition Bug

This bug only occurs in a battle without any Pokémon. The core bug was also carried forward to Pokémon Crystal. The only intended example is Professor Oak finding the Level 5 starter Pikachu and catching it, unique to Pokémon Yellow. In order to determine the battle transition, the game checks:

    Is the battle not a Trainer battle or from a dungeon map?
    After concluding that it isn't, the game checks the player's lead (non-fainted) Pokémon's level in comparison with the opposing Pokémon's level (5) in order to decide a "single circle" or "double circle" transition. A double circle is chosen if the Pokémon's level is +3 of the enemy's level, else it will be a single circle.

Due to a bug, the game will check beyond slot 6 of the party (with the player having no Pokémon at the time), while looking for the first non-fainted Pokémon. The first Pokémon beyond slot 6 will be Pokémon 12 if the rival name is greater than 5 characters long ($D34F; rival name character 6), where at least the end terminator (0x50) byte of the rival name is read as the HP (higher byte) for a Pokémon beyond slot 6. A non-00 value will mean it has remaining HP, so is not fainted. The level of Pokémon 12 is determined by the map's north connection byte, which will also be a value of 12 (0x0C; meaning the north connection is map 0x0C; Route 1. 12+3 (15) is greater than the opposing Level 5 Pikachu).

Therefore, in a nutshell; a rival name (internally ignoring terminators) greater than 5 characters long will ensure under a double circle in normal play (values 01 and above, because the map connection value of 12 is greater than the Level 5 Pikachu).

A Rival name can meet this crtieria if:

    A pre-set name is chosen. Note pre-set names have hidden characters beyond the terminator.
    A custom name was chosen for the rival, consisting of at least 5 characters (excluding the terminator, which might count as the sixth).
    On the input screen, the player entered at least 5 characters, but erased them with B, leaving stray 0x50 bytes in place after confirming the name.

For this reason, speedrunners who know about this bug may consider it as a reason (depending on the category) to choose a pre-set name/longer rival name/rival name with characters erased with B; because the 'double circle' battle transition is ~30 frame faster.


(Source: Crystal_ (documentation for Pokémon Crystal), TiKevin83 et al)
Boulder Switch Bug

This bug only applies to the Japanese versions of Yellow, and specifically for all of its revisions below Rev 3. It applies to a Pikachu that follows the player around (normally the starter Pikachu, but any with the same trainer ID and OT name as the player). Having Pikachu stand on one of the boulder switches in Victory Road will remove its corresponding wall tiles (as if the player pushed a boulder on to the switch) for all boulder switches but the one found in 1F. For an image guide, see here


(Source: Legendary Starblob, ChickasaurusGL (Rev 3 detail))
Design Flaw for Bulbasaur Gift Happiness

These are not really bugs, but the author decided to publish this for the sake of including design flaws. The Cerulean City Bulbasaur happiness gift does not check if starter/walking Pikachu exists, so (Pikachu's) happiness can be maniulated using the SRAM glitch/255 Pokémon glitch (swap Pokémon 1 with Pokémon 18 to obtain a happiness of 255, then wrong warp to Cerulean City (item 36 quantity swap, via expanded inventory acquisition from Pokémon 2 with Pokémon 10 swap) at the beginning of the game; for meeting the happiness criteria of 147 for obtaining it without ever receiving Pikachu.


(Source: Bulbapedia, ChickasaurusGL (method))
Design Flaws For Multiple Walking Pikachu

Since the only requirements for the starter (walking) Pikachu to spawn (after the initial rival battle) are for it to have the same Trainer ID and OT name as the player, a player with the same name and Trainer ID (via luck manipulation) can send over another walking Pikachu via Link Trade.

Details are as such:

    Only one walking Pikachu can spawn at a time.
    If the original walking Pikachu was traded away or disappeared using a glitch (such as a Trainer ID change expanded inventory manipulation), the new walking Pikachu will replace it.
    The happiness value and special emotes are shared between the two Pikachu; as is the asleep and unresponsive state by interacting with Jigglypuff in Pewter City Pokémon Center. So for instance, if the player uses a Potion on the walking Pikachu which hasn't spawned, it will raise the shared happiness value; applying it to the walking Pikachu which has spawned.


(Source: Bulbapedia)
Design Flaw For Disappearing Sleeping Pikachu At Pewter Pokémon Center

This requires another glitch to see, but is also a design flaw. Specific steps on how to do this are here. If the walking Pikachu is put to sleep from the Jigglypuff at Pewter Pokémon Center (but the Pikachu was the result of an unstable hybrid Pokémon obtained with the Pokémon merge bug), it is still possible to remove it from the party using a Thunder Stone; evolving it into Raichu; as the game only checks species byte 2 (which will be a Pokémon other than Pikachu) for the stone check. This leaves however a 'ghost' Pikachu, which responds to the Poké Flute with a sleepy sound, the "Z.....Z" speech bubble and the sleeping Pikachu box. The Pokémon Center Nurse will also say "It looks very content asleep.", even though Pikachu is gone. This is also be possible with the previously mentioned expanded inventory Trainer ID change manipulation.

It is not normally possible to place a normal sleeping Pikachu in the PC, or even view its summary from the party due to the message "There isn't any response..." but not so for a Pikachu/other Pokémon hybrid, which doesn't have these restrictions nor the omission of its menu sprite.


(Source: Paco81 (discovery), ChickasaurusGL (further information, additional video))
Freezing Pikachu's Sprite Bug

This bug causes the walking Pikachu's sprite to freeze. The player must jump off a ledge with Pikachu active. The player must keep the d-pad held down while Pikachu is turning by itself. If the glitch is performed correctly, Pikachu's sprite will not animate.


(Source: LanceAndMissingNo.)
Happiness Oversight

Using a HP recovery item, a status condition restoring item other than a Full Heal, or a vitamin will increase Pikachu's happiness, but the developers did not add a check preventing happiness from increasing if the item was unsuccessful, making it easy to max out Pikachu's happiness using an unusable item over and over again. This can be done as early as first receiving the Pikachu, using the Potion as withdrawed from the player's PC.
Initial Rival Battle Starter Pikachu Oversight

During the first Rival battle with Blue, Pikachu comes outside of its Poké Ball even though it was contained within it at the time. Though this really might have just been a design flaw and/or the developers may not have really been thinking about it, and it would be more efficient to not check and have any walking Pikachu (i.e. the same Trainer ID and OT as the player) come out from its Poké Ball all the time.
(Source: Bulbapedia)
Pikachu Link Battle Animation Oversight

Similar to above, this is probably just a design flaw for efficiency. Between two Pokémon Yellow Link Battles, the opponent's Pikachu will come out of a Poké Ball even if it is a starter/walking Pikachu, while on the user's side, it will enter battle horizontally without its Poké Ball, as usual.
(Source: Bulbapedia)
Pikachu Off-Screen Bug

This is yet another bug pertaining to the walking Pikachu. It has also referred to as Pikawalk in the English speedrunning community, or Pikachu's glitch for the user who documented the trainer corruption application, and was later adapted for arbitrary code execution. Although it is potentially a very powerful bug (like the left-facing shore tiles on Cinnabar Coast), it is lesser known and was first documented much later. Originally this bug was found as a derivative of glitch items and Glitch Cities as a means of putting Pikachu off the screen, before it was discovered it can occur in ordinary gameplay anyway.

It involves performing actions which leaves Pikachu off the screen, and known events without relying on other glitches such as glitch items, or Glitch Cities are as follows:

    Talk to the Pewter City Pokémon Center Jigglypuff to put Pikachu to sleep, then walk so Pikachu is off screen.
    Two interactions in Bill's House (before the player turns him back into a human from a Pokémon) will cause Pikachu to stay, and there is a small amount of space to put Pikachu off screen.
    There is an event in the Pokémon Fan Club where Pikachu falls in love with Clefairy, again allowing it to stay to put it off screen. This event can also be repeated, though the chances of it occurring are down to luck every time the player enters this map.

While Pikachu is off-screen memory buffer D437 (wPikachuFollowCommandBuffer) is used to store backup Pikachu follow commands which are applied when Pikachu appears back on screen again (such as 01 meaning "Pikachu walks south", 02 meaning "Pikachu walks north" and so on). The player can write to this buffer for Pikachu to take the same steps the player does after he reappears (ignoring complex commands, where the complex commands corresponding to Pikachu will be applied). However, the developers set no limit to the number of stored follow commands. Even though the written address will wrap around for D437+(x modulo 256), this is still a large enough buffer overflow to break the game.

By walking around enough, it is possible to corrupt memory in ways such as setting Pikachu's happiness, manipulating a 255:59 play time, causing a Glitch City with a glitch tileset (Super Glitch City), setting a special emote for Pikachu, corrupting trainers on the map (and turning them into Pokémon/other Trainer encounters); though this application requires a glitch item as of present, and placing "glitch signs" on the map, corresponding with a specific text box ID.


(Some other videos: Trainer/Pokémon encounters, another video for glitch item method applications)
Arbitrary Code Execution Potential

Originally for the purpose of speedrunning, two "walk south" commands are used to manipulate coordinates x=1, y=1 for a glitch sign at Vermilion Fan Club, with a "walk east" (04) command as the sign ID. In Generation I signs are not technically paired with objects like signboards, so the player can talk to these glitch signs regardless of what they're facing (and if they're not facing anything); as long they press A at the correct coordinates.

Specifically,

    Trigger the Clefairy event in the Vermilion Fan Club.
    Go to the bottom-left walkable tile (putting Pikachu off the screen), then walk up to the top and down to the bottom of the left-most column 11 times, but for the 11th time step one tile short on the final way back down.
    Step right, step left, then walk up to the top and down to the bottom of the left-most column 10 times.
    Step right, then go the top-left tile you can walk to, face right and press A.

As the location of this glitch sign is D221 in RAM (party Pokémon 5 catch rate/held item), the player can manipulate party data for a text box which causes a buffer overflow which overflows the item count of the bag, allowing for the manipulation of items past slot 20 (corresponding to memory address beyond D346); including addresses like wMapScriptPtr (D36D/D36E) for arbitrary code execution, or any of the powerful applications of manipulating them.

Technically, the player can set up arbitrary code execution directly using the text box with a catch rate/held item of 08, because 08 at the beginning of a text box marks TX_START_ASM for executing ASM after it (the contents of D222 onwards). However, while a number of these applications have been discovered (such as trading over a Pokémon from Gold/Silver/Crystal holding a Moon Stone (item 08)) most aren't efficient or legal for speedrunning.


(Source: Paco81 and Torchickens (original variants), Sally (in ordinary gameplay), stumpdotio (arbitrary code execution method with glitch signs), LanceAndMissingNo. (Trainer corruption application))
Pikachu Brightening Rock Tunnel Oversight

If Pikachu has just learned Thunderbolt or Thunder while in Rock Tunnel, talking to Pikachu will perform its special emote where it appears fierce and electrified. The flashing animation of the emote is enough to momentarily brighten up the area, without the need of HM05 Flash.
Pikachu Rock Tunnel Orange Box Oversight

Similarly, an orange box surrounds Pikachu within its emote box in Rock Tunnel when talking to it in Game Boy Color or Super Game Boy mode. Like the heading above, the developers might regard this oversight as not an issue but an emergent feature.
(Source: Neogeddon (video by ChickasaurusGL))
Pikachu Water Tile VRAM Corruption Bug

This bug was actually unearthed from the Nintendo of America bug reports from the 2020 source code leaks. Apparently thanks to those reports, it was fixed in the localisations. Chatting to Pikachu near the water many times will corrupt the water tiles. Doing this even more will corrupt them further.
Vaporeon Learnset Bug

In Yellow, Vaporeon learns both Haze and Mist at Level 42. However, the game's battle system does not allow a Pokémon to learn more than one move on levelup (via battle or Rare Candy), or evolution and as Haze comes before Mist in Vaporeon's learnset, it will not learn Mist unless it reaches Level 42 in the Day Care. Curiously, the level up box will briefly flash after learning Haze via evolution.

Overworld bugs
Safari Zone Glitch

The Safari Zone Glitch is probably one of the most infamous bugs due to how early it was discovered. The core of this glitch is that the Safari Zone guard will give the wrong speech if a specific set of instructions is followed. To perform the glitch:

    Go to the Safari Zone and pay to enter.
    Once inside, go right back to the gate.
    When asked if you want to leave, say no to be brought back inside the Safari Zone.
    Once there, save the game. Reset the console and load the saved game.
    Go back to the gate and this time you will be asked if you want to enter the Safari Zone.

If at this point you say no, you can leave the Safari Zone but the game thinks a Safari Zone game is still in progress. This means that all battles, including trainer battles, are replaced with the special Safari Zone battles (i. e. you can throw bait/rocks and Safari Balls, but not actually attack), but moreover, it also makes the game keep track of your steps, and sounds the bell to return you to the Safari Zone gate once you reach 500 steps.

The reason this glitch happens is actually a bit complicated and requires a bit of in-depth understanding of the game mechanics:

    Every overworld map in the game keeps track of the script ID, which is used to run various events (such as trainers walking up to the player if spotted). The script corresponding to the script ID is run every frame.
    The Safari Zone gate guard uses the script ID to keep track of which speech he should give (00 = "Welcome to the Safari Zone!", 05 = "Leaving early?")
    Normally, when you enter the Safari Zone, the script ID is set to 05, ensuring that the Safari Zone gate guard gives the correct speech for the situation. However, if you enter the gate house and say no to the "Leaving early?" question, the game makes the player auto-walk back into the Safari Zone. This is its own script (06), overwriting the script ID.
    Now, under normal circumstances, the regular script ID would be shoved into the temporary memory value CF0D. The moment you reenter the Safari Zone gate, the game will read this value and restore the script ID, ensuring everything is fine.
    However, the value of CF0D is not written to the savefile. So if you save at this point and then reset the console, that value gets initialized to 00, and if you reload the save file and go back into the Safari Zone gate, the guard will subsequently give the wrong speech.
    The flag whether a Safari Zone game is currently in progress is stored separately, so if you say no and leave the Safari Zone, the game still thinks a Safari Zone game is running.

The second part of this glitch occurs once the Safari Zone's bell goes off. You will warp back to the Safari Zone Gate, and depending on where you were when you reached 500 steps (most towns do not trigger this glitch), you will end up in a completely random, unplayable assortment of tiles dubbed "Glitch City" by the Pokémon community. The only way to get out is to Fly or Teleport, as doors and caves don't work and the game crashes when attempting to leave the map boundaries. This happens because exiting the gate house tries to return the player to exit 04 of the last overworld location, which under normal circumstances would be Fuchsia City, in front of the door leading into the Safari Zone. However, since the glitch allows you to freely roam the overworld, the last overworld location may be somewhere else, and if that place does not have an exit 04 (most routes don't, most towns do), the game will read garbage data instead.

Some further implications of this glitch are:

    If the 500th step is above a ledge, so the character is in mid-air when the bell sounds, you will gain the ability to walk through walls upon returning to the Safari Zone gate. This ability fades the moment you exit to (what would be) Fuchsia City, but it persists if you black out inside the gate (by having your last Pokémon faint from poison damage), allowing you to freely traverse the overworld.
    If the 500th step is during the sequence in Pewter City where the NPC guides you to the Pewter Museum of Science, upon exiting the Safari Zone gate you will appear back in Pewter City but the NPC, and the rest of the game, will glitch out completely.
    If the 500th step is on a spinning tile (such as those in Rocket Hideout), the player will be perpetually spinning upon returning to the Safari Zone gate. This can also cause the player sprite to be replaced with another NPC if the player uses the PC in this state.

In Red and Blue only, the Safari Zone Glitch could also be activated by blacking out inside the Safari Zone. This method was fixed in Yellow by checking whether the player blacked out in the Safari Zone, and resetting all Safari Zone-related flags if that is the case. However, the Save & Quit method described above works in all versions.
Trainer-Fly glitch

The Trainer-Fly glitch quickly became famous because it allowed people to catch Mew for the first time, and unlike all the schoolyard rumors it actually works.

The basic gist of the glitch is that for trainers that have a sight range that spans the entire screen, if you scroll the trainer into view and step into its sight range, the script that makes the trainer see you can be interrupted in one of the following two ways:

    Open the menu (there is a short window of input where you can open the menu before the trainer sees you), then Fly or Teleport away. Inside a cave, Dig or Escape Rope will work as well.
    Get a wild encounter on the exact tile the trainer would spot you (through tall grass or inside a cave). The wild encounter takes priority over the trainer seeing you. From there, lose the battle by blacking out.

If done correctly, the trainer will spot the player (the ! sprite will appear over his head) but the player character will warp away before the trainer gets a chance to walk up to the player character.

Because the game still thinks that a trainer battle is about to take place, the menu will be disabled. The effects of this can be remedied by fighting a different trainer (in a different area than the one where the first trainer was encountered), making sure the trainer walks to the player character (if the player character engages the trainer directly or walks right in front of him without at least a tile of space in between, the game will softlock).

Once that is taken care of, walking back to the map where the first trainer was will open the menu automatically, then start a wild battle.

    The species of the wild Pokémon is determined by the Special stat of the last Pokémon fought. As such, if the Special stat of the last Pokémon fought was 21 (hex 15), you will fight a Mew.
        The easiest way to get the desired special stat is to have it on one of your own Pokémon, encounter a wild Ditto, have it use Transform on said Pokémon, then knock it out or run away.
    The level is determined by that Pokémon's attack modifier, which defaults to 7. By using Growl (or another Attack-lowering move) six times before ending the battle, you will fight a level 1 Pokémon, which causes various glitches as no Pokémon were ever intended to be encountered at level 1.

In Red and Blue, the earliest point in the game this can be used to catch a Mew is if the Jr. Trainer♂ on Route 24, directly west of Nugget Bridge is used as the first trainer, and the Swimmer inside Cerulean Gym, whose last Pokémon is a level 16 Shellder (Special of 21) is used as the second trainer. In Yellow, a Mew can be caught even earlier, using the Yellow-exclusive Bug Catcher in Viridian Forest as the first trainer, and the Super Nerd that protects the fossils in Mt. Moon as the second trainer.

A second, lesser known consequence of this glitch is that the game will remove one sprite from the overworld, because it makes the assumption that the wild Pokémon fought comes from a special one-time event (like the legendary birds or Mewtwo). This can be used to remove the sleeping Snorlax from route 12, eliminating the need to enter the Pokémon Tower and acquire the Poké Flute.
Unwinnable Game

Due to an oversight, it is possible to create an unwinnable game in all versions of Red, Green, and Blue. Around halfway through the game, you are required to pay 500 Poké Dollars to enter the Safari Zone in order to find HM03 Surf and the Gold Teeth (to give to the Warden for HM04 Strength), both of which are necessary to progress further into the game. If your money, the cumulative sell value of all your items, and the cumulative money yields of all available trainer battles total to less than 500 Poké Dollars, and you have no Meowth that can use Pay Day, the game becomes unwinnable.

This was fixed in Yellow by allowing you to enter the Safari Zone with fewer than 500 Poké Dollars:

    If you have some money, you'll be given fewer Safari Balls proportional to the amount you paid.
    If you have no money at all, bug the guard enough times and he'll let you in with one Safari Ball.

(Source: Pikasprey Yellow)
Man on the Roof Glitch
Pokemon RB man on roof.png

Under certain circumstances, an NPC's initialization script can be interrupted by opening a dialog box. The NPC will then appear in a random position on the screen (usually in the top left corner), facing down until the dialog box is closed. There are currently three known ways to trigger this bug:

    Transition to a new area and press Start to open the menu as soon as possible. If done correctly, the menu will open and the NPC will appear in the top left corner. This can be done e. g. with the first trainer on Nugget Bridge when coming from Cerulean City, the trainer on Route 6 when coming from Vermilion City, or with the NPC in Pallet Town when surfing from Cinnabar Island.
    Trigger a hidden object that opens a dialog box on the same tile an NPC is loaded. The NPC will then appear in a random location on the screen, based on the number of steps the player took since entering the map. This is the most well-known variant of this bug as it can easily be seen with the locked Cinnabar Island Gym door (when the player does not have the Secret Key), but it also works e. g. with the bicycles that are on exhibit in the Bicycle Shop (approach the bicycle and press A as soon as possible).
    The guard in the gate house on Route 16 (west of Celadon) that blocks passage to Cycling Road if you do not have a Bicycle calls its own function that is also suspectible to this bug. Simply try to enter Cycling Road and the bug will manifest itself when the guard stops you.

This glitch was partially fixed in the Italian and Spanish versions: The NPCs will load in their correct position, but their orientation is still not initialized properly, so they will face down until the dialog box is closed. The glitch was fully fixed in Yellow.
Escape Rope bug
Gen1EscapeClub.gif

In all versions of Red, Green, and Blue, you can use an Escape Rope to escape the Pokémon Fan Club in Vermilion City as if it were a cave. This was unfortunately patched in Yellow.
Invisible PC bug
Gen1SecretPC.png

In Celadon Hotel, there's an invisible PC that can be used by walking to where the PC would be in a Pokémon Center (go to the very right of the room, stand one tile away from the counter and face up). Three of the four rest houses in the Safari Zone also have invisible PCs, though they cannot be accessed without using a walk-through-walls code.

Yellow removed all invisible PCs.
Vermilion Gym Trash Can bug

The algorithm that randomizes the position of the switches in the trash cans in Vermilion Gym is very broken in these games.

The original intent of the algorithm was to have the second switch always be directly adjacent to the first switch. To achieve this, the game has a table of possible positions for the second switch based on the position of the first switch, as well as the number of adjacent trash cans. The game then rolls a random number and performs an AND instruction between the random number and the number of adjacent trash cans to determine which trash can will have the second switch.

This has a number of unfortunate implications:

    If there are only two adjacent trash cans (i. e. the first switch was in one of the corners) or four adjacent trash cans (i. e. the first switch was in one of the three trash cans in the center), an AND with that number will only ever yield that number, making the position of the second switch seemingly guaranteed.
    However, the game fails to catch the case where the AND operation yields zero (i. e. there was no match between the random number and the trash can table). This makes the algorithm point to the zero padding past the end of the ROM bank instead, placing the second switch in the top left trash can.

The result is the following:

    If the first switch is in one of the two corners on the right side, the second switch can only be above/below the first switch (50% of the time).
    If the first switch is in one of the two corners on the left side, or is in one of the three center trash cans, the second switch can only be to the right of the first switch (50% of the time).
    Only the trash cans at the borders work like the algorithm was intended to work, giving each adjacent trash can an equal chance to have the second switch (25% of the time).
    In addition to all that, the top left trash always has a chance to have the second switch, no matter where the first switch was (50% of the time, or 25% if the first switch was in one of the border trash cans)

Yellow uses a different algorithm that is, however, bugged in another way.


(Source: https://www.youtube.com/watch?v=dyFA3gZMxrs)
Cable Club Escape glitch

If the player blacks out inside the Cable Club by having their last Pokémon faint from poison damage, they will return to the last Pokémon Center but the game still thinks the player is in the Cable Club.

The effect of this is that items can't be used and the Save option in the menu is disabled (though the game can still be saved by switching boxes in the PC). Also, if the player traded Pokémon or battled in the Cable Club prior to blacking out, all in-game trainers will display Red's sprite and have their Pokémon replaced with the team of the linked game. If there was no trade or battle prior to blacking out, the in-game trainers will be glitched instead.

This was fixed in Yellow by preventing Pokémon from taking poison damage inside the Cable Club.
Vending Machine bug
Gen1LemonadeTrick.gif

The vending machines in Celadon Department Store only check if you have enough money to buy a Fresh Water, even if you pick the Soda Pop or the Lemonade instead. This means you can buy those items even if you do not have enough money to cover their cost, as long as you have enough money to buy a Fresh Water.
Statue bug
A screenshot of the player fishing in one of Cerulean Gym's statues.

The bottom tile of the statues that can be found in Gyms behaves like a water tile when faced from the left or right. This means you can fish in the statues (though only the Old Rod and Good Rod will pull up any Pokémon, since Gyms don't have any wild encounter data) and also Surf into the statue. This was fixed in Yellow.
Game Corner bugs

    As soon as the Game Corner is entered, an RNG script selects one of the slot machines to be the lucky slot machine, which has a much higher likelihood of winning. However, due to an off-by-one error in said script, it's possible that none of the slot machines in the Game Corner will end up being the lucky one.
    The lucky slot machine itself is also bugged. The original intent was that the first wheel will always stop at a 7, but the condition that checks this can never be true due to the wrong type of conditional jump being used ("jump if carry" instead of "jump if zero"). The second wheel was supposed to stop when that would yield a 7-7 or a BAR-BAR, but that code doesn't work either.

Cycling Road save bug

If the player saves the game on Cycling Road, then resets and starts a new game, the player will be unable to use a bicycle or surf until entering Cycling Road again. This is because the memory value D732, which stores the flag that determines whether the player is on Cycling Road, is not reset when starting a new game. Since that value also holds several debug flags, this may actually be a leftover from development.
Lift Key bug
LiftKeyBug.gif

The Rocket Grunt that drops the Lift Key is programmed to always drop it on the tile to his left. If the player stands in that position and interacts with the Rocket Grunt, he will drop the Lift Key right on top of the player. This was fixed in Yellow by making the Rocket Grunt drop the Lift Key immediately after the battle ends, rather than having to interact with him a second time.

A similar bug occurs if you are standing above Giovanni after defeating him in the Rocket Hideout. He will drop the Silph Scope on the tile above him, even if the player is standing there.
LiftKeyBugGiovanni.gif
Silph Co. 11F bug

Exiting the elevator on Silph Co. 11F will make the player appear right on top of the elevator door, rather than walking down as on all the other floors. This can lead to a glitch where the elevator exit will not work if you hold Down as soon as you appear inside the elevator.


11F Exit 	2F Exit
Gen1SilphElevatorBug.png 	Gen1SilphElevatorComparison.png

This bug was fixed in Yellow.
Surf glitch

Walk towards a water tile, open the menu and save in the middle of the walking animation, then reset the game. If done correctly, the player character should be facing the direction he walked after reloading the saved game. If you now use Surf, the player character will surf down instead of the direction he's facing.

This can be used to bypass barriers, since there is no collision check for the Surf animation. The most common application is to reenter the S.S. Anne after acquiring Surf and reach the infamous truck. It can also be used to reach an otherwise inaccessible piece of land next to Bill's house, commonly titled "Bill's Secret Garden" due to the once rampant rumors surrounding this piece of land.
Trapped glitches

There are two instances in the game where the player character can get trapped, with no way to get out:

    In Pokémon Mansion 3F, in the room in the bottom left corner there's a trainer who walks back and forth horizontally. If you go into the narrow gap between the table and the rubble and then interact with the trainer from below to battle him once he passes by, once the battle ends the trainer will block the only way out of the gap. Since trainer positions are preserved when you save the game, the only way out is to either use Dig or Escape Rope or, failing that, black out to a wild Pokémon by repeatedly walking back and forth. This bug became infamous because it affected the initial playthrough of Twitch Plays Pokémon.
    In Cerulean City, the police officer in front of the burgled house will normally only move after you see Bill. If you trade in a Pokémon that knows Cut from another game, and cut the tree to battle the Rocket Grunt behind the house, once you receive TM28 the police officer will move as well as a failsafe. However, if your bag is full at this point, so you cannot receive TM28, the police officer will not move, and if you go through the burgled house from behind, once you exit you will be stuck on top of the door tile with the police officer blocking your path, with no way to get back in the house. Saving at this point creates an unwinnable game.

Fainted party walk glitch

If you deposit your party Pokémon to the PC so that only fainted party members remain, the game will normally force a blackout after 4 steps. This can be circumvented by saving and resetting the game every 3 steps, as the counter for this check gets reset to 4 when the game boots.

This occurs because the check for a fainted party was tied with the check that applies poison damage on the overworld, which operates on the (incorrect) assumption that a poisoned Pokémon fainting is the only way to get a party of only fainted Pokémon.

This glitch was fixed in Yellow, which runs the fainted party check every step instead.
Battle Engine bugs
1/256 Miss Bug

Rather infamously, any move in the game, including those that have 100% accuracy, may miss at a rate of 1/256.

This happens due to a quirk in how the game determines whether a move should miss or hit. The algorithm rolls a random number and then checks if that random number is less than the move's accuracy (taking into account accuracy modifiers and such) to determine whether the move should hit. However, if the RNG rolls an FF, this condition can never hold true because there is no number higher than that, so any move will miss if that number is rolled by the game's RNG. The only move that is impervious to this bug is Swift because it bypasses the accuracy check to always hit, however this applies only to the international (non-Japanese) versions of the games.

The same bug also affects critical hits: even if a Pokémon would be guaranteed to land a critical hit (by having a high base speed and using a move with an increased critical hit chance), there's a 1/256 chance the Pokémon will only score a normal hit.
Lorelei Softlock

In Red and Blue, it is possible to end up in a practically infinite battle if you challenge Lorelei with certain Pokémon that know the move Rage while all of its other moves have zero PP.

The reason for this is twofold: first is how the AI in Red and Blue works. While the AI used by wild Pokémon is fairly simple (it just selects any of its available moves at random), trainer AI on the other hand is forced to take type effectiveness into account and always chooses a move of a type super effective against the player's Pokémon, if available, even if that move is a status move (which will not deal damage).

In Lorelei's case, if the player sends out a Fighting- or Poison-type Pokémon (the two types weak to Psychic), Lorelei's Dewgong will use Rest continuously, because Rest is Psychic-type, and therefore the trainer AI is forced to select it (unless the Pokémon in question is also weak to the Ice-type Aurora Beam (which Lorelei's Dewgong knows), such as Nidoking (Poison/Ground), as there is a chance that the trainer AI will instead select that move). If the player's Pokémon cannot do enough damage to compensate for the amount restored by Rest, this results in the battle being unwinnable. Enemy trainers cannot run out of PP in these games, and there is no way to end the battle other than winning or losing. However, your Pokémon would eventually run out of PP, and trying to attack after this causes the Pokémon to use Struggle, which causes recoil damage, and this would eventually cause your Pokémon to knock itself out, ending the battle and causing the player to black-out, returning them to the last used Pokémon Center.

This is where Rage comes in, the second key necessary for this softlock. In Generation I games, when selecting Rage, one PP is consumed, and then the Pokémon is forced to continuously use Rage thereafter as long as the move doesn't miss the first time (bare in mind that Rage has 100% accuracy); however, these forced uses of Rage do not consume PP, even if a forced use of Rage misses, rendering the Struggle problem moot. Saving the game before entering the battle under these conditions effectively dooms the save file, as leaving the room Lorelei is in is only possible by winning or losing the battle against her.

That said, the above situation is technically escapable due to an infamous bug in Generation I where every move in the game, even ones with 100% accuracy, have a 1/256 chance of missing, including Rage. Therefore, triggering this miss 20 times in a row will deplete Rage's PP, causing the Pokémon to knock itself out with Struggle. Don't count on it, though, as the chance of missing 20 times in a row at these odds is astronomically unlikely (1/25620).

Yellow fixed this conundrum by programming in a special case for Lorelei's Dewgong, which allows the AI to break out of the above logic and select a random move from its move pool 40% of the time.
(Source: Pikasprey Yellow)
Evolution Stone bug

Pokémon that normally evolve by Evolution Stone will also evolve if they level up in battle and the last Pokémon sent out in that battle has the same index number as the evolution stone. The Pokémon correspond to the Evolution Stones as follows:

    Moon Stone (0A): Exeggutor
    Fire Stone (20): Missingno. (not normally obtainable)
    Thunderstone (21): Growlithe
    Water Stone (22): Onix
    Leaf Stone (2F): Psyduck

This bug was fixed in Yellow.
Ghost type

In the Generation I games, Psychic-type Pokémon are completely immune to Ghost-type moves. As this contradicts every piece of Pokémon-related media released at the time, including Nintendo's official strategy guides and the anime, as well as a trainer in Saffron Gym who mentions that Psychic-type Pokémon are weak to Ghosts, this is very likely a programming bug and not intentional. However, the only Ghost-type move that takes typing into account is the pathetically weak Lick, making it highly unlikely to encounter this bug in practice (which is likely why it was missed).

Starting from Generation II, Ghost-type moves are super effective against Psychic-type Pokémon, matching the depiction in official media.
Ghost bugs
The player identifying a Ghost without a Silph Scope by checking the stats of their Pokémon.
The player escaping from the ghost Marowak using a Poké Doll.

The fights with the ghosts in Pokémon Tower, when their identities haven't been revealed with the Silph Scope, are particularly buggy in this game.

    Just triggering these fights will register Gastly, Haunter, Cubone, or Marowak as seen in the Pokédex.
    If you check out one of your Pokémon's stats during battle, the ghost will then display the sprite of its true form instead of the generic ghost sprite. This is a purely visual bug; you still can't attack or catch the Pokémon, and they will still never attack you.
    Using a Poké Doll on the Marowak ghost ends the battle as if you won, progressing the game's storyline. This completely eliminates the need to acquire the Silph Scope and skips the entire Rocket Hideout in the process.

Psywave bug

The special RNG algorithm that calculates Psywave's damage will discard a 0 if the player is the user but not if the player is the target. If this occurs in a link battle, the link battle will desync.
Fly/Dig Invulnerability bug

If a Pokémon uses Fly or Dig and the attacking turn fails due to confusion or paralysis, the Pokémon will become invulnerable for the rest of the battle until they use Fly/Dig or a charging move (Razor Wind, Skull Bash or SolarBeam).
Healing Moves bug

Healing moves (Recover, Rest, or Softboiled) will fail if the difference between the current HP and max HP is exactly 255 or 511. That is because the algorithm that determines if the move should fail due to the Pokémon already being fully healed erroneously doesn't take the upper bits of the HP value into account and only checks the lower bits.
Focus Energy bug

The move Focus Energy is completely broken in these games; instead of increasing the critical hit chance, it reduces it to a quarter of its original value.

The game's code reveals that the two branches that determine critical hit chance may have been accidentally swapped; if so, the reduced critical hit chance might have been the originally intended critical hit chance and the critical hit chance of the final game would have been the one after using Focus Energy. Thus, critical hits would have been a lot less common than they ended up being in the final game.

This bug also applies to the Dire Hit item, which uses the same function as the Focus Energy move.
Hyper Beam bugs

The move Hyper Beam comes with another set of bugs:

    If the player's Pokémon uses Hyper Beam, then gets frozen before it gets to its recharge turn, the player will stop getting turns altogether, allowing the enemy to attack endlessly until the player's Pokémon faints or gets thawed from a Fire-type move. The move Haze will thaw the Pokémon but not end the glitch, so the player will still not get any turns.
    If the player's Pokémon uses Hyper Beam, and the opponent attempts to use a binding move (Bind, Clamp, Fire Spin or Wrap) and it misses before the player's Pokémon gets to its recharge turn, the player's Pokémon will automatically use Hyper Beam again instead of recharging. If the move has 0 PP at this point, it will roll over to 63 PP.
    Hyper Beam does not need to recharge if it knocks out the opposing Pokémon. If the user flinches or gets put to sleep, the recharge turn is skipped altogether.

Mirror Move bug

In a link battle, if the player uses a binding move (Bind, Clamp, Fire Spin or Wrap) by way of Mirror Move, and the opponent switches out the Pokémon while trapped, on the user's side the Pokémon will continue using the binding move against the Pokémon that switches in, while on the opponent's side the game will say that the Mirror Move failed. This causes the link battle to desync.
Transform bugs

The move Transform is particularly buggy in these games:

    If the player's Ditto uses Transform, and then you use the Select button to swap the first move with a different move in the transformed Pokémon's moveset, once the battle ends the Ditto will have Transform replaced with the glitch move -- (two dashes), which corrupts the game when used. This was fixed in Yellow.
    If a wild Pokémon uses Transform and is caught while transformed, it will become a Ditto even if it was originally a different species. This can only happen when a Pokémon uses Transform by way of Mimic, Mirror Move or Metronome, as the only Pokémon that learn Transform are Ditto and Mew, and the latter cannot be legitimately encountered in the wild.
    If a Pokémon that used Transform levels up during battle and learns a new move, the transformed moveset will be replaced by its own moveset, even though the Pokémon will otherwise stay transformed.
    If a transformed Pokémon uses Metronome or Mirror Move, the Pokémon will gain 1 PP in the moveslot corresponding to its own moveset. If there is no move in that moveslot, the Pokémon is effectively locked out of Struggle forever. This can also lead to a softlock if the Pokémon has no usable moves and the enemy Pokémon attempts to use Disable.
    In SGB mode, any Pokémon that is not Ditto and uses Transform will have its sprite's palette replaced with Ditto's if the sprite is refreshed by opening the menu and checking out a Pokémon's stats.
    Critical hits involving a player's transformed Pokémon will incorrectly be calculated based off the Pokémon's stats before transforming. Wild Pokémon and Pokémon of in-game trainers are not affected by this bug.
    When an opponent's Pokémon uses Transform and adopts the target's IVs, its own IVs will be stored in a temporary value. If the Pokémon then uses Transform again while transformed, its own IVs will be overwritten by the IVs the Pokémon had right before using Transform. This can be used to manipulate a Ditto to have specific IVs as long as the player has a Pokémon with these IVs and access to Transform (either natively, or through Mimic/Metronome). If the player's Pokémon has the correct IVs to become Shiny if traded to a Generation II game, the caught Ditto will be Shiny as well.

Substitute bugs

The move Substitute comes with its own set of bugs:

    If the user's current HP is exactly 25% of its maximum HP, using Substitute will leave the Pokémon with 0 HP, fainting immediately.
    If both the player and the opponent have a Substitute up and the player's Pokémon hurts itself due to confusion, the opponent's Substitute will take the confusion damage instead. If the opponent does not have a Substitute, the damage gets discarded entirely, although the text will still claim that the Substitute took damage for the opponent. This can also cause a minor graphical glitch if the damage dealt would be enough to break the user's Substitute, causing the opponent's sprite to fall down (as if the Pokémon fainted), only to reappear a split second later.
    A Substitute protects against stat-altering moves, burn, freeze, poison, moves that cause confusion (Confuse Ray and Supersonic) and moves that have paralysis as their secondary effect (Body Slam, Lick, Thunderbolt, Thunderpunch, Thundershock). It does not protect against moves that have confusion as their secondary effect (Confusion and Psybeam), moves that cause paralysis (Glare, Stun Spore, Thunder Wave) or any kind of sleep move. This was fixed in Stadium so a Substitute protects against all status effects.
    If a move breaks a Substitute, any secondary effects of the move are skipped, leading to some very unintended side effects:
        If Explosion or Selfdestruct break a Substitute, the user will not faint, but its sprite will vanish and it will be invisible for the remainder of the battle. This (and only this) was fixed in Stadium.
        If a move that hits with recoil breaks a Substitute, the user will not take any recoil damage.
        (In the localized versions only) Absorb, Mega Drain, Leech Life and Dream Eater will not restore any HP to the user if they break a Substitute.
        If Hyper Beam breaks a substitute, the user will not need to recharge.
        Pay Day will not scatter any money if it breaks a Substitute.
        Psybeam and Confusion will not confuse the target if they break a Substitute.
        Moves that hit multiple times will end immediately after the hit that breaks the substitute.

Toxic bugs

    The damage multipliers used by Toxic and Leech Seed will stack with one another if both are inflicted on the same Pokémon. This is because both moves use the same variable for determining how many turns have passed since the move was used.
    If a Pokémon affected by Toxic uses Rest, it will no longer be badly poisoned but the turn counter will not be reset. If the Pokémon then gets affected by Toxic or Leech Seed again, the damage multiplier will pick up where it left off. Additionally, if the Pokémon gets burned instead, the burn damage will behave like Toxic and increase with each successive turn. This is because burn, poison and Toxic call the same function for dealing damage (which also explains why burn damage uses the same animation as poison damage if battle animations are turned on).

Blaine AI bug

Blaine has two Super Potions that he can use on his Pokémon. However, because there is no check for the Pokémon's HP, he will try to use the Super Potions even on Pokémon that have full HP.

This was fixed in Yellow, so it was very likely not intentional.
Cooltrainer AI bug

The Cooltrainer♀ has special programming where if its Pokémon's current HP is between 10% and 20% of its max HP, it will switch it out. If two of its Pokémon meet that condition, it will switch them with one another every turn and never attack. This behavior was supposed to only happen 25% of the time, but due to a programming bug, the RNG roll is completely discarded and the behavior will always happen as long as the conditions are met.
Counter bugs

    Normally Counter will only hit if the opponent uses an attacking move on the same turn Counter is used, however turns where the opponent did not select a move (by being frozen, asleep, being switched out or using an item) do not count against this, and thus Counter will counter the attack used on the turn before in these cases, no matter who used the attack. The result is that Counter can "counter" a move used by the user, including Counter itself and recoil damage the user took as a result of using a move that hits with recoil. Counter can even "counter" a move that was used in a previous battle if it is used on the first turn.
    Counter is supposed to only counter damage dealt by Normal- or Fighting-type moves. However, the memory value that the game uses to determine the move (and thus its type) the opponent used last is updated when the cursor is moved in the movelist - not when the move is actually used. The effect of this is that if the player selects Fight, moves the cursor to a move that is Normal- or Fighting type, then backs out with B and switches out, Counter may counter a move that is not Normal- or Fighting-type. Doing this in a link battle will cause the link battle to desync. This bug also occurs if the player selects a move, but the Pokémon fails to execute the move due to being fully paralyzed.
    If a Pokémon uses Counter to counter an attack that hit (and broke) the user's Substitute, Counter's damage will be calculated based on the damage the user would have taken were it not for the Substitute, instead of the actual damage taken.
    Counter can be called by Metronome, but will always fail no matter what.
    Even though Counter can be a critical hit, it will always do the same amount of damage; the damage calculation is not altered by Counter being a critical hit.

Dual-type effectiveness bug

If a move hits a dual-type Pokémon whose two types are weak and strong in a way that cancel each other out, the game may erroneously use the wrong message and claim that the move is super effective or not very effective when it's not. This is because the game runs both types of the opponent against an internal table of type matchups to determine which string to use, and if there are two matches the second match will simply overwrite the first.
Bide bugs

    If the opponent uses Bide, and the Pokémon faints before Bide goes off, the game will erroneously only clear the low byte of the Bide damage counter and not the high byte. The result is that if the first Pokémon took more than 255 damage during Bide before fainting, and the next Pokémon uses Bide again, the move may deal more damage than intended. If this happens in a link battle, the link battle will desync.
    Bide can hit Pokémon that are in the invulnerable turn of Fly/Dig. If Bide hits a Pokémon that has used Dig, on the subsequent turn the Pokémon's sprite will scroll up and then loop back to its original position.

Victory music bug

In a wild battle, if the battle ends in a draw (e. g. by having the player's last Pokémon use Explosion on the wild Pokémon and fainting it), the victory music will play as the player blacks out. This is because the function that plays the victory music is called before the game checks whether to black out the player.
Jump Kick bug

The moves Jump Kick and Hi Jump Kick were intended to apply crash damage equivalent to 1/8 of the damage they would have done to the target if they miss. However, when a move misses the game sets the damage dealt to zero before the routine that deals with Jump Kick/Hi Jump Kick is called, so the recoil damage will always be calculated based off a damage of zero, and thus will always be exactly 1 HP.
Reflect/Light Screen bug

    The moves Reflect and Light Screen do not have any boundary checks at all. If Reflect or Light Screen would cause the user's accumulated Defense/Special to rise above 1023, the stat will wrap around to 0.
    Using Reflect will reduce the damage the opponent takes if it hurts itself due to confusion.

Division by zero bug

Stats in this game are stored in 10 bits, which means they can have a maximum value of 1023. However, presumably to make calculations a bit easier, the damage formula divides the Pokémon's stats by 4 if either of the stats involved in the damage calculation is above 255, so the damage calculation can proceed with single byte math, at the cost of slight precision loss.

However, this causes a problem if a Pokémon's accumulated Defense is lower than 4. This can happen on an already low-level Pokémon that has also had stat debuffs applied to it. In this case, the division step will set the Pokémon's defense to 0. At a later step, the game tries to divide the user's attack by the opponent's defense, and if the defense is 0, the game will softlock to a division by zero error.

As such, if the user's accumulated attack is higher than 256, and the opponent's accumulated defense is lower than 4, the game is guaranteed to softlock as soon as the user attacks.

Amusingly enough, the game does have a failsafe if the division step would make Attack equal zero (it will be bumped to 1 if this happens), but there is no similar failsafe for Defense even though the dividend being zero is a lot less problematic than the divisor being zero. Make of that what you will.
Exp. All bug

The Exp. All calculates the experience to be distributed among the player's party only based on the experience the last Pokémon received. If more than one Pokémon participated in the battle, the experience that would normally go to the other Pokémon who participated in the battle is completely discarded, effectively reducing the total amount of experience the player receives from the battle. The game also doesn't take fainted party members into account, so if one or more party members are fainted, the experience they would receive is also discarded.
Stat modification bugs

Stat modifications are particularly messy in this game.

    Every time the player's stats are altered in any way (boosted by an own move, or debuffed by an opponent's move), all badge boosts are reapplied to the player's Pokémon, stacking with one another infinitely until the stat cap is reached.
    If the opponent is burned or paralyzed, every time a stat-altering move is used in battle (either boosting the Pokémon's own stats or lowering the opponent's), the Attack and Speed drop from burn and paralysis (respectively) are applied to the opponent again, similarly stacking with one another until the stat reaches 1.
    A Pokémon that is burned or paralyzed can remove its Attack and Speed drop from burn and paralysis (respectively) by using a move that raises Attack or Speed, such as Swords Dance or Agility.
    If a status-healing item such as Burn Heal is used (no matter which status was cured), all stat changes are removed and the Pokémon also loses its badge boosts.

The first three bugs suggest the game at one point used to recalculate all stats from the ground up whenever a stat modification was applied, but this was changed (presumably for performance reasons) and the stat modification code was not changed to compensate. The fourth bug is nothing more than a programming goof.

But wait! There's more!

While stats in the game are stored in 10 bits, and thus can store a maximum value of 1023, all stats are effectively capped at 999 by the game's code. When a stat is boosted (for example by using a stat raising move) the game checks if the accumulated stat would exceed 999 after boosting, and if so it will set it to 999, preventing any further boosts to this stat. The code, however, doesn't take into account the existence of moves that raise a stat by two stages (such as Swords Dance, Agility, or Amnesia), leading to the following bugs:

    When a stat is debuffed (as opposed to boosted), the stat cap is not enforced. This means that if a Pokémon's stat is at a point where raising the stat by another stage would hit the stat cap, the Pokémon uses a move like Swords Dance to raise the stat by two stages (setting the stat to 999), then gets hit by a move that lowers the stat by one stage (such as Growl), the stat is recalculated but the stat cap is not enforced, so the stat will now be above 999. If the stat exceeds 1023, it will wrap around to 0.
    The code that applies stat boosts first raises the current stat stage, then checks if the stat is already capped at 999, and if so lowers the stat stage by one, even if the move used is one that raises the stat stage by two. The effect is that trying to use the move over and over raises the stat stage by one every time without actually changing the stat in any way.


(Source: https://www.dragonflycave.com/mechanics/gen-i-stat-modification)
Levelup learnset glitch

If a Pokémon gains enough experience from a single battle to skip a level completely, the Pokémon loses out on any moves that it would normally learn on the level(s) skipped. For example, a level 4 Pidgey that gains enough experience to directly level up to level 6 will not learn Sand-Attack, normally learned at level 5.
Mimic bugs

    Moves copied by Mimic will use Mimic's PP, but the maximum PP displayed will erroneously be based on the move copied. This can lead to a visual glitch where the current PP will appear to be higher than the maximum PP (e. g. when Mimic copies a move with 5 PP like Horn Drill).
    Mimic's effect will revert if the user learns a new move by leveling up in battle.

Binding move PP overflow bug

If a binding move (Bind, Clamp, Fire Spin or Wrap) is used and the target switches out before the end of the duration, the binding move will automatically be used again on the Pokémon that switches in, deducting 1 PP in the process. If the move has 0 PP at this point, it will roll over to 63 PP.
Freeze desync bug

In a link battle, if a slower Pokémon that is frozen gets thawed by a faster Pokémon's attack before its turn would have come up, the Pokémon will automatically use a move, despite the game not having given that option beforehand.

On the user's side, it will be the last move that the cursor was moved over in the move list. This can be a move from another Pokémon's movelist, if the Pokémon was switched in and frozen before its turn came up. If the move list was never opened since the battle started, the Pokémon will use the glitch move -- (two dashes). On the opponent's side, the Pokémon will use its last move it used in battle, or failing that, the topmost move from its movelist. This causes the link battle to desync.

PP will always be deducted from the move that was used on the opponent's side. If the move has 0 PP at this point, it will roll over to 63 PP.
Minimize/Substitute bug

If you use Minimize or Substitute, then open the Pokémon menu, look at the stats of any of your party Pokémon and go back to battle, the enemy Pokémon sprite will glitch up. In the case of Minimize, it will turn into a garbled version of the Pokémon sprite from the stats screen, in the case of Substitute, it will turn into the Substitute doll.

This glitch was fixed in Yellow.
Battle Transition bug

The Generation I games have a total of 7 (technically 8, but two are identical) different battle transitions. The game determines the battle transition by these three factors:

    whether it's a wild Pokémon battle or a trainer battle
    whether the opponent's Pokémon is at least three levels higher than your lead Pokémon
    whether the player is inside a dungeon or on the overworld

The following maps are incorrectly not recognized as dungeons and so they do not play the correct battle transition:

    Victory Road 2F and 3F (1F is fine)
    Silph Co. 9F to 11F (2F to 8F is fine, and there are no battles on 1F)
    Pokémon Mansion 1F (all other floors are fine)
    Seafoam Islands B1F to B4F (1F is fine)
    all of Rocket Hideout, the Power Plant, and Diglett's Cave

Endless Battle Bugs

    If two Pokémon who only know Transform transform into each other, the battle will become endless. This is because using Transform resets PP on all moves, so the Pokémon get stuck in an infinite loop and can never fall back to using Struggle. English Stadium (notably not Japanese Stadium) tried to fix this by preventing Transform from being used if the target is Ditto, but the bug can still be exploited by using a Mew with Transform, or by using a Pokémon with Mimic to copy Transform.
    Struggle is treated as a Normal-type move in Generation I games, which means, among other things, that Struggle cannot hit a Ghost-type Pokémon. If two Ghost-type Pokémon run out of PP and fall back to using Struggle, the battle becomes endless as these two Pokémon can never hurt each other. This also works with a Pokémon that can change its type to Ghost via Transform or Conversion.

Multi-Turn Move Accuracy Bug

Multi-turn moves (Rage, Thrash and Petal Dance) reapply all accuracy and evasion modifiers every turn. The effect of this is, for example, if the player selects Rage and the opponent uses Double Team to raise its Evasion, Rage's accuracy will drop continuously every turn until it reaches 1. 