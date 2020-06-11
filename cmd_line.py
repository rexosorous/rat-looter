import sqlite3

conn = sqlite3.connect('loot.db')
db = conn.cursor()



# error handling for incorrect number of inputs and unable to find item



def info(item: str):
    db.execute('SELECT qty, fir_qty, full_name FROM inventory INNER JOIN items ON item=id WHERE (full_name LIKE ? OR short_name LIKE ? OR alt_name LIKE ?)', (f'%{item}%', f'%{item}%', f'%{item}%'))
    inv = list(db.fetchone())

    # get total requirements
    db.execute('SELECT qty, fir FROM recipes INNER JOIN quests ON quests.id=quest INNER JOIN items ON items.id=item WHERE completed=0 AND (full_name LIKE ? OR short_name LIKE ? OR alt_name LIKE ?)', (f'%{item}%', f'%{item}%', f'%{item}%'))
    requirements = db.fetchall()

    required = [0, 0]
    for recipe in requirements:
        required[recipe[1]] += recipe[0]

    needed = [required[0]-inv[0], required[1]-inv[1]]
    if needed[1] < 0:
        needed[0] += needed[1]
        needed[1] = 0

    print(inv[2])
    print('{space:<10} | {gen:<5} | {fir:<5}'.format(space='', gen='ANY', fir='FIR'))
    print('{needed:<10} | {gen:<5} | {fir:<5}'.format(needed='find', gen=needed[0], fir=needed[1]))
    print('{required:<10} | {gen:<5} | {fir:<5}'.format(required='required', gen=required[0], fir=required[1]))
    print('{owned:<10} | {gen:<5} | {fir:<5}'.format(owned='owned', gen=inv[0], fir=inv[1]))



def add(qty: int, fir: int, item: str):
    if not item:
        print('incorrect number of arguments. syntax is: [qty] [fir status (y/n)] [item name]')
        return

    db.execute('SELECT qty, fir_qty, id FROM inventory INNER JOIN items ON item=id WHERE (full_name LIKE ? OR short_name LIKE ? OR alt_name LIKE ?)', (f'%{item}%', f'%{item}%', f'%{item}%'))
    inv = list(db.fetchone())
    inv[fir] += qty
    if inv[fir] < 0:
        inv[fir] = 0

    db.execute('UPDATE inventory SET qty=?, fir_qty=? WHERE item=?', (inv[0], inv[1], inv[2]))

    conn.commit()
    info(item)



def set(qty: int, fir: int, item: str):
    if not item:
        print('incorrect number of arguments. syntax is: [qty] [fir status (y/n)] [item name]')
        return

    db.execute('SELECT qty, fir_qty, id FROM inventory INNER JOIN items ON item=id WHERE (full_name LIKE ? OR short_name LIKE ? OR alt_name LIKE ?)', (f'%{item}%', f'%{item}%', f'%{item}%'))
    inv = list(db.fetchone())
    inv[fir] = qty

    db.execute('UPDATE inventory SET qty=?, fir_qty=? WHERE item=?', (inv[0], inv[1], inv[2]))

    conn.commit()
    info(item)



def complete(mission: str):
    # check if the quest is laready completed
    db.execute('SELECT completed FROM quests WHERE name LIKE ? AND completed=1', (f'%{mission}%',))
    if db.fetchone():
        print('you have already completed that quest.')
        return

    db.execute('UPDATE quests SET completed=1 WHERE name LIKE ?', (f'%{mission}%',))

    # update inventory
    db.execute('SELECT item, qty, fir FROM recipes INNER JOIN quests ON id=quest WHERE name LIKE ?', (f'%{mission}%',))
    recipes = db.fetchall()
    for entry in recipes:
        db.execute('SELECT qty, fir_qty FROM inventory INNER JOIN items ON item=id WHERE id=?', (entry[0],))
        inv = list(db.fetchone())
        inv[entry[2]] -= entry[1]

        if inv[entry[2]] < 0: # make sure values don't go below zero
            if entry[2] == 0: # if we have to use fir items to finish this quest, do so
                inv[1] += inv[0]
                if inv[1] < 0:
                    inv[1] = 0
            inv[entry[2]] = 0

        db.execute('UPDATE inventory SET qty=?, fir_qty=? WHERE item=?', (inv[0], inv[1], entry[0]))

    conn.commit()



def loop():
    while True:
        try:
            command = input('enter command: ')
            args = command.split(' ')

            if args[0].lower() == 'info':
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
            elif args[0].lower() == 'stop':
                break
            else:
                print('unknown command')
        except TypeError:
            print('error: please check your spelling')
        except ValueError:
            print('error: incorrect syntax')
        finally:
            print('\n\n\n')


loop()