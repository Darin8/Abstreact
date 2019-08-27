# _*_ coding: utf-8

import urllib2
import json
import xlsxwriter
import requests
import re
import datetime

#TODO: Download all maps and zip them

class BeatmapWriter:

    def __init__(self, title, api_key):
        self.xlsx = xlsxwriter.Workbook(title + '.xlsx')
        self.sheet = self.xlsx.add_worksheet()
        self.osu_api_key = api_key

        # Cell Widths
        self.sheet.set_column(1,1,10)
        self.sheet.set_column(2,2,13)
        self.sheet.set_column(3,3,25)

        # Round format
        self.round = self.xlsx.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 5,
            'bg_color': 'D9EAD3'
            })

    def add_beatmap(self, mod, row):
        # Create new formats, as each section needs their own formats
        # Otherwise, every section will have the same color as the last section
        empty_color = self.xlsx.add_format({})
        top_border = self.xlsx.add_format({
            'top': 5
            })
        top_right_border = self.xlsx.add_format({
            'top': 5,
            'right': 5
            })
        right_border = self.xlsx.add_format({
            'right': 5,
            'align': 'center'
            })
        bottom_right_border = self.xlsx.add_format({
            'right': 5,
            'bottom': 5,
            'align': 'center'
            })
        bottom_border = self.xlsx.add_format({
            'align': 'center',
            'bottom': 5
            })
        stats = self.xlsx.add_format({
            'align': 'center'
            })
        title = self.xlsx.add_format({
            'bold': True,
            'top': 5
            })
        thumb = self.xlsx.add_format({
            'border': 5
            })

        orig_row = row
        url = raw_input('Enter Beatmap URL: ')

        # Get ID's
        pattern = re.compile(r'\d+')
        matches = pattern.findall(url)

        beatmapset_id = matches[0]
        beatmap_id = matches[1]

        # Image URL's, use =image(${url}) function in xlsx box
        headerimage_url = 'https://assets.ppy.sh/beatmaps/' + beatmapset_id + '/covers/cover.jpg'
        thumbnail_url = 'https://b.ppy.sh/thumb/' + beatmapset_id + '.jpg'

        # Get beatmap information
        api_url = 'https://osu.ppy.sh/api/get_beatmaps'

        params = {
            "k": self.osu_api_key,
            "b": beatmap_id,
        }

        try:
            r = requests.get(url = api_url, params = params)
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)

        if r.status_code == 200:
            map_json = r.json()[0]


        # Write to sheet

        # Mod Colors (NM:0,HD:1,HR:2,DT:3,FM:4,TB:5)
        thumb_right_color = ''
        mod_color = ''
        if mod == 0:
            thumb_right_color = '#D9D9D9'
            mod_color = '#F3F3F3'
        elif mod == 1:
            thumb_right_color ='#FFE599'
            mod_color = '#FFF2CC'
        elif mod == 2:
            thumb_right_color = '#DD7E6B'
            mod_color = '#F4CCCC'
        elif mod == 3:
            thumb_right_color = '#9FC5E8'
            mod_color = '#C9DAF8'
        elif mod == 4:
            thumb_right_color = '#B6D7A8'
            mod_color = '#D9EAD3'
        elif mod == 5:
            thumb_right_color = '#D5A6BD'
            mod_color = '#EAD1DC'

        empty_color.set_bg_color(mod_color)
        thumb.set_right_color(thumb_right_color)
        title.set_bg_color(mod_color)
        top_border.set_bg_color(mod_color)
        top_right_border.set_bg_color(mod_color)
        right_border.set_bg_color(mod_color)
        bottom_right_border.set_bg_color(mod_color)
        bottom_border.set_bg_color(mod_color)
        stats.set_bg_color(mod_color)

        # THUMBNAIL
        self.sheet.merge_range(row, 2, row+3, 2, '', thumb)
        self.sheet.write_formula(row, 2, '=image(\"'+thumbnail_url+'\")')

        # TITLE
        self.sheet.write(row, 3, map_json["artist"] + ' - ' + map_json["title"], title)

        # DIFFICULTY
        self.sheet.write(row+1, 3, map_json["version"], empty_color)

        # URL
        self.sheet.write(row+2, 3, 'https://osu.ppy.sh/b/' + beatmap_id, empty_color)

        # STATS
        map_data = (
            [u'★', str(round(float(map_json["difficultyrating"]),2))],
            ['BPM', map_json["bpm"]],
            ['Length', str(datetime.timedelta(seconds=int(map_json["total_length"])))],
            ['AR', map_json["diff_approach"]],
            ['CS', map_json["diff_size"]],
            ['HP', map_json["diff_drain"]],
            ['OD', map_json["diff_overall"]],
        )

        row += 2
        col = 4

        for category, value in (map_data):
             self.sheet.write(row, col, category, stats)
             self.sheet.write(row + 1, col, value, bottom_border)
             col += 1

        '''
        Fill in color and borders (no easy way to do this since each cell
        needs its own format object)
        '''

        # Empty Cell
        for col in range(4,10):
            self.sheet.write(orig_row+1,col,'',empty_color)

        # Top Border
        for col in range(4,10):
            self.sheet.write(orig_row,col,'',top_border)

        # Top Right Corner Border
        self.sheet.write(orig_row,10,'',top_right_border)

        # Right Border
        self.sheet.write(orig_row+1,10,'',right_border)
        self.sheet.write(orig_row+2,10,'OD',right_border)

        # Bottom Right Border
        self.sheet.write(orig_row+3,10,map_json["diff_overall"],bottom_right_border)

        # Bottom Border
        self.sheet.write(orig_row+3,3,'',bottom_border)

    def write_section(self, mod, row, amount):
        section = self.xlsx.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 5
            })

        mod_string = ''
        mod_color = ''
        if mod == 0:
            mod_string = 'NoMod'
            mod_color = '#F3F3F3'
        elif mod == 1:
            mod_string = 'Hidden'
            mod_color = '#FFF2CC'
        elif mod == 2:
            mod_string = 'HardRock'
            mod_color = '#F4CCCC'
        elif mod == 3:
            mod_string = 'DoubleTime'
            mod_color = '#C9DAF8'
        elif mod == 4:
            mod_string = 'ForceMod'
            mod_color = '#D9EAD3'
        elif mod == 5:
            mod_string = 'TieBreaker'
            mod_color = '#EAD1DC'
        section.set_bg_color(mod_color)

        # One map takes 4 rows
        height = amount*4-1

        self.sheet.merge_range(row, 1, row+height, 1, mod_string, section)

    def write_round(self, name, row):
        self.sheet.merge_range(row,1,row+1,10,name,self.round)
