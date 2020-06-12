import sqlite3

conn = sqlite3.connect('loot.db')
db = conn.cursor()



def items():
    '''Shows a list of every item to be looking out for.
    '''
    db.execute('''
        SELECT  items.full_name
        FROM items
        INNER JOIN inventory
        ON inventory.item=items.id
        INNER JOIN
        (
            SELECT  SUM(recipes.qty) AS qty,
                    SUM(recipes.fir) AS fir,
                    recipes.item
            FROM recipes
            INNER JOIN quests
            ON quests.id=recipes.quest
            WHERE quests.completed=0
            GROUP BY recipes.item
        ) AS temp
        ON temp.item=items.id
        WHERE
        (
            (inventory.fir < temp.fir)
            OR (inventory.qty+inventory.fir < temp.qty+temp.fir)
            OR (inventory.qty+inventory.fir-temp.fir < temp.qty)
        )
    ''')

    data = db.fetchall()
    for entry in data:
        print(entry)



def quests():
    '''Shows a list of all quests that are yet to be completed

    Note:
        Does not include quests that don't have items to turn in.
    '''
    db.execute('''SELECT name FROM quests WHERE completed=0''')
    data = db.fetchall()
    for entry in data:
        print(entry)



def info(item: str):
    '''Shows info regarding the quantities of an item.

    Shows how much you need, how much is required, and how much you currently have for one particular item.

    Args:
        item (str): the item to get info on
    '''
    db.execute('''
        SELECT  items.full_name,
                inventory.qty,
                inventory.fir,
                SUM(recipes.qty),
                SUM(recipes.fir)
        FROM items
        INNER JOIN recipes
        ON recipes.item=items.id
        INNER JOIN inventory
        ON inventory.item=items.id
        INNER JOIN quests
        ON quests.id=recipes.quest
        WHERE
        (
            quests.completed=0
            AND
            (
                full_name LIKE ?
                OR short_name LIKE ?
                OR alt_name LIKE ?
            )
        )
     ''', (f'%{item}%', f'%{item}%', f'%{item}%'))

    data = list(db.fetchone())

    need = [data[3]-data[1], data[4]-data[2]]
    if need[1] < 0:
        need[0] += need[1]
        need[1] = 0

    print(data[0])
    print('{space:<10} | {gen:<5} | {fir:<5}'.format(space='', gen='ANY', fir='FIR'))
    print('{needed:<10} | {gen:<5} | {fir:<5}'.format(needed='find', gen=need[0], fir=need[1]))
    print('{required:<10} | {gen:<5} | {fir:<5}'.format(required='required', gen=data[3], fir=data[4]))
    print('{owned:<10} | {gen:<5} | {fir:<5}'.format(owned='owned', gen=data[1], fir=data[2]))



def add(qty: int, fir: int, item: str):
    '''Adds a quantity of an item into your inventory.

    Args:
        qty (int): how much is to be added
        fir (int): whether the item is found in raid (0 for no, 1 for yes)
        item (str): the item we're adding
    '''
    if not item:
        print('incorrect number of arguments. syntax is: [qty] [fir status (y/n)] [item name]')
        return

    db.execute('''
        SELECT  inventory.qty,
                inventory.fir,
                items.id
        FROM inventory
        INNER JOIN items
        ON inventory.item=items.id
        WHERE
        (
            items.full_name LIKE ?
            OR items.short_name LIKE ?
            OR items.alt_name LIKE ?
        )
    ''', (f'%{item}%', f'%{item}%', f'%{item}%'))

    inv = list(db.fetchone())
    inv[fir] += qty
    if inv[fir] < 0:
        inv[fir] = 0

    db.execute('''UPDATE inventory SET qty=?, fir=? WHERE item=?''', (inv[0], inv[1], inv[2]))

    conn.commit()
    info(item)



def set(qty: int, fir: int, item: str):
    '''Adds a quantity of an item into your inventory.

    Args:
        qty (int): how much to set the value to
        fir (int): whether the item is found in raid (0 for no, 1 for yes)
        item (str): the item we're adding
    '''
    if not item:
        print('incorrect number of arguments. syntax is: [qty] [fir status (y/n)] [item name]')
        return

    db.execute('''
        SELECT  inventory.qty,
                inventory.fir,
                items.id
        FROM inventory
        INNER JOIN items
        ON inventory.item=items.id
        WHERE
        (
            items.full_name LIKE ?
            OR items.short_name LIKE ?
            OR items.alt_name LIKE ?
        )
    ''', (f'%{item}%', f'%{item}%', f'%{item}%'))

    inv = list(db.fetchone())
    inv[fir] = qty

    db.execute('''UPDATE inventory SET qty=?, fir=? WHERE item=?''', (inv[0], inv[1], inv[2]))

    conn.commit()
    info(item)



def complete(mission: str):
    '''Completes a mission so we don't have to consider its requirements.

    Not only completes the mission, but removes items from the player's inventory automatically.

    Args:
        mission (str): the mission to complete. MUST BE AS CLOSE AS POSSIBLE to the text in game
    '''
    # check if the quest is already completed
    db.execute('''SELECT name FROM quests WHERE name LIKE ? AND completed=1''', (f'%{mission}%',))
    if (quest := db.fetchone()):
        print(f'you have already completed the quest: {quest[0]}')
        return

    db.execute('''UPDATE quests SET completed=1 WHERE name LIKE ?''', (f'%{mission}%',))

    # update inventory
    db.execute('''
        SELECT  recipes.item,
                recipes.qty,
                recipes.fir
        FROM recipes
        INNER JOIN quests
        ON quests.id=recipes.quest
        WHERE quests.name LIKE ?
    ''', (f'%{mission}%',))

    recipes = db.fetchall()
    for entry in recipes:
        db.execute('''SELECT inventory.qty, inventory.fir FROM inventory INNER JOIN items ON inventory.item=items.id WHERE items.id=?''', (entry[0],))
        inv = list(db.fetchone())
        inv[entry[2]] -= entry[1]

        if inv[entry[2]] < 0: # make sure values don't go below zero
            if entry[2] == 0: # if we have to use fir items to finish this quest, do so
                inv[1] += inv[0]
                if inv[1] < 0:
                    inv[1] = 0
            inv[entry[2]] = 0

        db.execute('''UPDATE inventory SET qty=?, fir=? WHERE item=?''', (inv[0], inv[1], entry[0]))

    db. execute('''SELECT name FROM quests WHERE name LIKE ?''', (f'%{mission}%',))
    quest = db.fetchone()
    print(f'completed quest: {quest[0]}')
    conn.commit()



def ignore(mission: str):
    '''Removes a mission from the requirements consideration.

    Does this without removing items from your inventory.
    So if you wanted to no longer care about completing a certain quest like "Farming. Part 4" which requires you to turn in GPUs,
    then you can ignore it so you'll no longer be reminded about needing to collect its items.
    '''
    db.execute('''UPDATE quests SET completed=1 WHERE name LIKE ?''', (f'%{mission}%',))
    db.execute('''SELECT name FROM quests WHERE name LIKE ?''', (f'%{mission}%',))
    quest = db.fetchone()
    print(f'ignored quest: {quest[0]}')
    conn.commit()



def loop():
    '''Main logic loop.

    Continually asks for commands and calls the appropriate functions.
    '''
    while True:
        try:
            command = input('enter command: ')
            args = command.split(' ')

            if args[0].lower() in ['help', 'commands']:
                pass
            elif args[0].lower() == 'items':
                items()
            elif args[0].lower() == 'quests':
                quests()
            elif args[0].lower() == 'info':
                info(' '.join(args[1:]))
            elif args[0].lower() == 'add':
                qty = int(args[1])
                fir = 1 if args[2]=='y' else 0 # 1 for found in raid
                item = ' '.join(args[3:])
                add(qty, fir, item)
            elif args[0].lower() == 'sub':
                qty = int(args[1])
                fir = 1 if args[2]=='y' else 0 # 1 for found in raid
                item = ' '.join(args[3:])
                add(qty*-1, fir, item)
            elif args[0].lower() == 'set':
                qty = int(args[1])
                fir = 1 if args[2]=='y' else 0 # 1 for found in raid
                item = ' '.join(args[3:])
                set(qty, fir, item)
            elif args[0].lower() == 'complete':
                complete(' '.join(args[1:]))
            elif args[0].lower() == 'ignore':
                ignore(' '.join(args[1:]))
            elif args[0].lower() == 'restart':
                # restart(' '.join(args[1:]))
                pass
            elif args[0].lower() == 'wipe':
                # wipe()
                pass
            elif args[0].lower() == 'stop':
                break
            else:
                print('unknown command')
        except TypeError:
            print('error: that quest or item doesn\'t exist or you misspelled something.')
            print('       periods and spaces must be included in.')
            print('       if it\'s a quest name, it must be exactly as it appears in game.')
        except ValueError:
            print('error: incorrect syntax.')
        finally:
            print('\n\n\n')


loop()