import matplotlib.pyplot as plt
from itertools import cycle

class VelocityProfileParser():

    def __init__(self, fname=None):
        self.filename = fname
        self.first_step = 5000
        self.step_increment = 5000
        self.count = None
        self.content = None
        self.uncommented = None
        self.titles = None
        self.step = None
        self.all_steps = None
        self.all_steps_details = None
        self.step_details = None
        self.per_step_velocity = None

        self.openfile()
        self.remove_comments()
        self.column_titles()
        self.separate_timesteps()
        self.match_column()

    def openfile(self):
        with open(self.filename, 'r') as opened:
            self.content = opened.readlines()

    def remove_comments(self):
        self.uncommented = []
        for lines in self.content:
            if 'Spatial' in lines or 'Chunk-averaged' in lines:
                continue
            else:
                self.uncommented.append(lines.strip())

    def column_titles(self):
        self.titles = []
        for lines in self.uncommented:
            if lines.startswith('# Chunk') or lines.startswith('# Bin'):
                lines = lines.strip('#')
                lines = lines.split()
                self.titles.append(lines)
        self.titles = self.titles[0]

    def separate_timesteps(self):
        self.all_steps = {}
        timesteps = None
        self.count = self.first_step
        for lines in self.uncommented:
            if lines.startswith('#'):
                continue
            if lines.startswith(str(self.count)):
                lines = lines.split()
                timesteps = int(lines[0])
                self.all_steps[timesteps] = []
                self.count = self.count + self.step_increment
            else:
                self.all_steps[timesteps].append(lines.split())

    def match_column(self):
        self.all_steps_details = {}
        for timestep in self.all_steps:
            timestep_details = self.all_steps[timestep]
            self.all_steps_details[timestep] = []
            for data in timestep_details:
                self.step_details = {}
                titles = self.titles
                for index, title in enumerate(titles):
                    self.step_details[title] = [data[index]]
                self.all_steps_details[timestep].append(self.step_details)

parser = VelocityProfileParser()
