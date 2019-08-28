import os
import json
from BeatmapWriter import BeatmapWriter

class Abstreact:

    def __init__(self):
        self.writer = self.setup()
        self.round_name_list = self.round_info()
        self.round_counter = 1
        self.row_counter = 5
        self.forcemod = False
        self.tiebreaker = False

    def setup(self):
        with open('config.json') as config_file:
            config = json.load(config_file)

        title = raw_input('Enter tournament name: ')
        if os.path.exists('./' + title + '.xlsx'):
            os.remove(title + '.xlsx')

        return BeatmapWriter(title, config["osu_api_key"])

    def round_info(self):
        try:
            round_amount = int(raw_input("Enter amount of rounds: "))
        except:
            print('[ERROR]: Input must be an integer')
            return self.round_info()
        if round_amount == 0 or round_amount < 0:
            print('[ERROR]: Invalid amount; please enter a number above 0.')
            return self.round_info()

        round_amount = int(round_amount)
        round_name_list = []
        for rounds in range(round_amount):
            round_name_list.append(raw_input("Enter name for Round " + str(rounds+1) + ": "))
        return round_name_list

    def write_mod(self, mod, round_name):
        mod_string = ''
        if mod == 0:
            mod_string = 'NoMod'
        elif mod == 1:
            mod_string = 'Hidden'
        elif mod == 2:
            mod_string = 'HardRock'
        elif mod == 3:
            mod_string = 'DoubleTime'
        elif mod == 4:
            mod_string = 'ForceMod'

        if mod == 5:
            print('TieBreaker:')
            self.writer.write_section(5, self.row_counter, 1)
            self.writer.add_beatmap(5, self.row_counter)
            self.row_counter+=5
        else:
            try:
                map_amount = int(raw_input('Enter amount of ' + mod_string + ' maps for ' + str(round_name) + ': '))
            except:
                print('[ERROR]: Input must be an integer')
                self.write_mod(mod, round_name)
                return
            if map_amount < 0:
                print('[ERROR]: Invalid amount; please enter a number above 0.')
                self.write_mod(mod, round_name)
                return
            self.writer.write_section(mod, self.row_counter, map_amount)
            for x in range(map_amount):
                self.writer.add_beatmap(mod, self.row_counter)
                self.row_counter+=4 # Height of beatmap information

    def main(self):
        for round_name in self.round_name_list:
            self.tiebreaker = False
            self.forcemod = False
            # Write title
            self.writer.write_round(round_name,self.row_counter)

            # Space between title and map info
            self.row_counter+=3

            # Prompt whether round contains tiebreaker & forcemod
            tb_bool = ''
            fm_bool = ''
            fm_bool = raw_input('Does ' + round_name + ' contain a force/freemod section? (Y/n): ')
            if fm_bool.lower() == 'n':
                self.forcemod = False
            else:
                self.forcemod = True

            tb_bool = raw_input('Does ' + round_name + ' contain a tiebreaker? (Y/n): ')
            if tb_bool.lower() == 'n':
                self.tiebreaker = False
            else:
                self.tiebreaker = True

            # NoMod
            self.write_mod(0, round_name)

            # Hidden
            self.write_mod(1, round_name)

            # HardRock
            self.write_mod(2, round_name)

            # DoubleTime
            self.write_mod(3, round_name)

            # ForceMod
            if self.forcemod == True:
                self.write_mod(4, round_name)

            # Tiebreaker
            if self.tiebreaker == True:
                self.write_mod(5, round_name)
            else:
                self.row_counter+=2

        print('[FINISHED]: Xlsx file located in root folder.')
        self.writer.xlsx.close()

Abstreact = Abstreact()

if __name__ == '__main__':
        Abstreact.main()

