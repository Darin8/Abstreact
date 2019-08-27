import os
import json
from BeatmapWriter import BeatmapWriter

# Setup Writer

with open('config.json') as config_file:
    config = json.load(config_file)

title = raw_input('Enter tournament name: ')
if os.path.exists('./' + title + '.xlsx'):
    os.remove(title + '.xlsx')

writer = BeatmapWriter(title, config["osu_api_key"])


# Prompt for round information

round_amount = int(raw_input("Enter amount of rounds: "))
if round_amount == 0 or round_amount < 0:
    print('[ERROR]: Invalid amount; please enter a number above 0.')
    sys.exit(1)

round_name_list = []
for rounds in range(round_amount):
    round_name_list.append(raw_input("Enter name for Round " + str(rounds+1) + ": "))

# Start Writing
round_counter = 1
row_counter = 5
forcemod = False
tiebreaker = False
for round_name in round_name_list:
    tiebreaker = False
    forcemod = False
    # Write title
    writer.write_round(round_name,row_counter)

    # Space between title and map info
    row_counter+=3

    # Prompt whether round contains tiebreaker & forcemod
    tb_bool = ''
    fm_bool = ''
    fm_bool = raw_input('Does ' + round_name + ' contain a force/freemod section? (Y/n): ')
    if fm_bool.lower() == 'n':
        forcemod = False
    else:
        forcemod = True

    tb_bool = raw_input('Does ' + round_name + ' contain a tiebreaker? (Y/n): ')
    if tb_bool.lower() == 'n':
        tiebreaker = False
    else:
        tiebreaker = True

    # NoMod
    map_amount = int(raw_input('Enter amount of NoMod maps for ' + round_name + ': '))
    writer.write_section(0, row_counter, map_amount)
    for x in range(map_amount):
        writer.add_beatmap(0, row_counter)
        row_counter+=4 # Height of beatmap information

    # Hidden
    map_amount = int(raw_input('Enter amount of Hidden maps for ' + round_name + ': '))
    writer.write_section(1, row_counter, map_amount)
    for x in range(map_amount):
        writer.add_beatmap(1, row_counter)
        row_counter+=4

    # HardRock
    map_amount = int(raw_input('Enter amount of HardRock maps for ' + round_name + ': '))
    writer.write_section(2, row_counter, map_amount)
    for x in range(map_amount):
        writer.add_beatmap(2, row_counter)
        row_counter+=4

    # DoubleTime
    map_amount = int(raw_input('Enter amount of DoubleTime maps for ' + round_name + ': '))
    writer.write_section(3, row_counter, map_amount)
    for x in range(map_amount):
        writer.add_beatmap(3, row_counter)
        row_counter+=4

    # ForceMod
    if forcemod == True:
        map_amount = int(raw_input('Enter amount of ForceMod maps for ' + round_name + ': '))
        writer.write_section(4, row_counter, map_amount)
        for x in range(map_amount):
            writer.add_beatmap(4, row_counter)
            row_counter+=4

    # Tiebreaker
    if tiebreaker == True:
        print('TieBreaker:')
        writer.write_section(5, row_counter, 1)
        writer.add_beatmap(5, row_counter)
        row_counter+=2
    else:
        row_counter+=2

writer.xlsx.close()

