# rat-looter
a utility tool to keep track of the items needed for quests in escape from tarkov.
this tool will tell you what items you need to hold on to, how much of them you'll need, 
and keep track of your progress all the way through (as long as you keep up with it).

# notes
* DOES NOT keep track of quest only items. ex: will not keep track of the [bronze pocket watch](https://escapefromtarkov.gamepedia.com/Checking)
* DOES NOT keep track of the items needed for [the collector](https://escapefromtarkov.gamepedia.com/Collector). mostly because i'm lazy.
* DOES NOT keep track of any guns that need to be turned in for quests because often times 
  the traders are rather ambiguous on what they want.
* DOES NOT keep track of any attachments needed for the gunsmith questline because there
  are multiple ways you can build those guns.
* DOES NOT keep track of keys that need to be turned in.
* DOES NOT keep track of keys that are needed to open doors to quest rooms.
* DOES NOT keep track of "specific gear" items that don't need to be turned in. ex:
  rat-looter will not tell you to keep UNTAR armor for the quest [Peackeeping mission](https://escapefromtarkov.gamepedia.com/Peacekeeping_mission)
* DOES NOT automatically assume you'll get items from quest rewards. ex: rat-looter will not automatically
  add the gold chains obtained as a quest reward from [chumming](https://escapefromtarkov.gamepedia.com/Chumming)
* for every instance of `<quest>` in the command arguments below, the name MUST be EXACTLY how it appears
  in your game, including all periods and spaces.
* for every instance of `<item>` in the command arguments below, you can use the full name shown in the
  inspect screen or the short name used on the icons in your inventory. rat-looter will try to figure out
  which item you're looking for if you don't type it in exactly, but is very bad at it
* specifically for the items "can of beef stew" and "can of delicious beef stew", you should use the
  full names from the inspect screen since they both appear as "tushonka" in the inventory screen.

# commands
```
help                             shows this message
items                            lists all items that you should be looking out for in your raids
quests                           lists all quests that have not been completed
info <item>                      gives you information on how much of <item> you still need to collect
add <qty> <fir (y/n)> <item>     adds <qty> of <item> with <fir> status to your inventory
sub <qty> <fir (y/n)> <item>     removes <qty> of <item> with <fir> status to your inventory
set <qty> <fir (y/n)> <item>     sets <qty> of <item> with <fir> status to your inventory
complete <quest>                 completes <quest> and removes appropriate items from your inventory
ignore <quets>                   completes <quest> without removing any items from your inventory
restart <quest>                  re-activates a <quest> in case you miss-typed
wipe                             COMPLETELY removes all progres. to be used when there\'s a wipe in tarkov
stop                             stops the program
```

# usage
in raid, if you're not sure if you need to collect a certain item or if you're unsure how many
more of a certain item you'll need, use the `info` command to check how much is needed, how much
you have, and how many more you still need to collect.

after every raid, you should use the `add` command to add items into rat-looter's inventory so rat-looter
can accurately keep track of how many more a each item you'll need to collect. note: this will
only work for items that are actually needed for quests. so don't go using the ``add`` command
for [toothpaste](https://escapefromtarkov.gamepedia.com/Toothpaste) as it's not used for any quests.

if you make a mistake, sell items, or use items in trades or hideout productions, you can use the
`sub` command to remove items from rat-looter's inventory. note: DON'T use this command whenever you
turn in items for your quest, instead use the `complete` command (explained in the below paragraph).

whenever you complete a quest, you should use the `complete` command which will remove the quest items
from rat-looter's inventory so you can accurately double check your inventory against rat-looter's (explained below).

if you don't want to do a certain quest, you should use the `ignore` command so rat-looter knows
not to bother with that quest's requirements. note: this will not also ignore quests that are locked
behind the one you ignored. for example, if you don't want to do [farming part 4](https://escapefromtarkov.gamepedia.com/Farming_-_Part_4)
because you'd rather sell off those graphics cards, then you should use `ignore Farming. Part 4'
so rat-looter doesn't constantly remind you to collect graphics cards and cpu fans for it. but doing
this will not ignore [fertilizers](https://escapefromtarkov.gamepedia.com/Fertilizers) or
[import](https://escapefromtarkov.gamepedia.com/Import).

if you make a mistake when completing or ignoring a quest, you can use the `restart` command
to re-enable the quest.

if you keep up with adding/removing items and completing quests in rat-looter, then the quantities
of items in your inventory should always reflect the quantities in rat-looter's inventory. so whenever
you use the `info` command, it'll tell you how much of that item is in rat-looter's inventory and that
should accurately reflect how much you have in your tarkov inventory. this way, you can double-check
what's in rat-looter's inventory with what's in yours in case you've forgotten to add/remove items or
complete quests.
