import os


class Csv_reader:

    def __init__(self, file_name):
        self.file_name = file_name
        self.fields = []

    @property
    def filename(self):
        if not self.file_name.lower().endswith('.csv'):
            raise Exception("Error! It isn't a CSV-file!")
        if not os.path.exists('./{0}'.format(self.file_name)):
            raise FileNotFoundError("Error! File don't exists!")
        return self.file_name

    def read_fields(self,csvfile):
        for field in csvfile.readline().strip().split(','):
            self.fields.append(field)
        return self.fields

    def check_value(self, value):
        if value.isdigit():
            return value
        if len(value.split(';')) > 1:
            return [int(number) for number in value.split(';')]
        return '"{}"'.format(value)

    def print_pattern_json(self, key, value):
        pattern = '\t\t"{0}" : {1},\n'.format(key, self.check_value(value))
        if key == self.fields[0]:
            return '\t{\n' + pattern 
        if key == self.fields[-1]:
            return pattern[:-2] + '\n\t},\n'
        return pattern 
    
    def parse_csv_to_json(self, results_csv):
        for j in results_csv:
            for key, value in j.items():
                yield self.print_pattern_json(key, value)

    def parse_csv_to_dict(self, csvfile):
        results_csv = []
        fields = self.read_fields(csvfile)
        for item_csv in csvfile.readlines():
            items_csv = item_csv.rstrip().split(',')
            dict_csv = {}
            for index, value in enumerate(items_csv):
                dict_csv[fields[index]] = value
            results_csv.append(dict_csv)
        return results_csv

    def parse_csv(self):
        with open(self.filename, 'r') as csvfile:
            return self.parse_csv_to_dict(csvfile)

    def write_json(self):
        json_file = os.path.splitext(self.filename)[0] +'.json'
        with open(json_file, 'wt') as f:
            str_json = ''
            f.write('[\n')
            for item in self.parse_csv_to_json(self.parse_csv()):
                str_json += item
            f.write(str_json[:len(str_json)-2])
            f.write('\n]')


Csv_reader("soccer.csv").write_json()
    