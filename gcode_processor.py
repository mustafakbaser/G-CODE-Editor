import json
import re

class GCodeProcessor:
    def __init__(self):
        self.start_params = []
        self.route_start_params = []
        self.route_end_params = []
        self.end_params = []
        self.thread_cut_params = []
        self.safe_route_params = []
        self.current_route = 1
        self.is_first_process = True
        
    def load_parameters(self, filename):
        with open(filename, 'r') as file:
            params = json.load(file)
            self.start_params = params.get('start_params', [])
            self.route_start_params = [
                "F10000",
                "M114",
                "G04 P200",
                "M118",
                "Z3",
                "Z30",
                "M119"
            ]
            self.route_end_params = params.get('route_end_params', [])
            self.end_params = params.get('end_params', [])

    def is_coordinate_line(self, line):
        pattern = r'^X\d+\.?\d*\s+Y\d+\.?\d*\s*$'
        return bool(re.match(pattern, line.strip()))

    def process_gcode(self, content):
        lines = content.split('\n')
        processed_lines = []
        coordinates = []
        start_coordinates = set()
        
        if self.is_first_process:
            for line in self.start_params:
                if self.is_coordinate_line(line):
                    start_coordinates.add(line.strip())
        
        for line in lines:
            line = line.strip()
            if self.is_coordinate_line(line) and line not in start_coordinates:
                coordinates.append(line)
        
        if coordinates:
            if self.is_first_process:
                processed_lines.extend(self.start_params)
                self.is_first_process = False
            
            processed_lines.append(f"% Rota No {self.current_route}")
            
            processed_lines.extend(self.route_start_params)
            
            processed_lines.extend(coordinates)
            
            processed_lines.extend(self.route_end_params)
            
            processed_lines.extend(self.end_params)
            
            self.current_route += 1
        
        return '\n'.join(processed_lines)

    def reset_route_counter(self):
        self.current_route = 1
        self.is_first_process = True