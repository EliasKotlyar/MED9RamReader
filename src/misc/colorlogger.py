class ColorLogger:
    @staticmethod
    def color(data: str, color: str):
        colors = {'pink': '\033[95m', 'blue': '\033[94m', 'green': '\033[92m', 'yellow': '\033[93m', 'red': '\033[91m',
                  'ENDC': '\033[0m', 'bold': '\033[1m', 'underline': '\033[4m'}
        return colors[color] + str(data) + colors['ENDC']
