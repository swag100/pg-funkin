import json

class ChartReader(object):
    def __init__(self, song_name, difficulty):
        self.song_name = song_name

        #Load metadata
        self.metadata = self.load_metadata()

        time_changes = self.metadata['timeChanges']
        play_data = self.metadata['playData']

        self.start_bpm = time_changes[0]['bpm']
        self.bpm = self.start_bpm
        
        self.difficulty = play_data['difficulties'][0] #Default to first item
        if difficulty in play_data['difficulties']: 
            self.difficulty = difficulty
        else:
            print(f'Difficulty \'{difficulty}\' not found')

        #Load chart
        self.chart = self.load_chart(self.song_name, self.difficulty)

    def load_metadata(self):
        metadata_path = f'assets/data/songs/{self.song_name}/{self.song_name}-metadata.json'
        with open(metadata_path) as metadata_file:
            metadata = json.loads(metadata_file.read())
        metadata_file.close()

        return metadata
    def load_chart(self, song_name, difficulty): #Returns list of Note objects from given song name and difficulty
        #Read from data file
        with open(f'assets/data/songs/{song_name}/{song_name}-chart.json') as song_chart:
            chart_dict = json.loads(song_chart.read())
        song_chart.close()

        self.speed = 1
        if difficulty in chart_dict['scrollSpeed']: 
            self.speed = chart_dict['scrollSpeed'][difficulty]
        else:
            if 'default' in chart_dict['scrollSpeed']: 
                self.speed = chart_dict['scrollSpeed']['default']

        #t: Time; d: direction; l (optional): length
        #direction will be 0-7; 4-7 are opponent strums and 0-3 are player strums
        #length is optional; if length is specified, the note is given that attribute. FOR NOW, IGNORE LENGTH
        self.notes = chart_dict['notes'][difficulty]

        #Returns a chart dictionary sorted by strumlines.
        chart = {}
        for note in self.notes:
            strumline = int(note['d'])

            if not strumline in chart:
                chart[strumline] = []

            chart[strumline].append(note)
        return chart