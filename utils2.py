from random import uniform, randint
from time import asctime

class Util:
    def __init__(self):
        self.start_id = 100
        
    def create_data(self) -> dict:
        # Increment ID for each data point
        self.start_id += 1
    

        # Generate temperature data
        temp = round(uniform(15, 23), 1)

        # Simulate transmitting wild data occasionally
        if self.start_id % (round(uniform(5,7), 1)) == 0:
            # Generate wild temperature data
            temp = round(uniform(30, 70), 1)  # Adjust the range as needed for wild data

        # Determine temperature level based on the value
        if temp >= 15.0 and temp < 30:
            level = 'normal'
        else:
            level = 'extreme'

        # Construct and return the data dictionary
        data = {
            'id': self.start_id,
            'time': asctime(),
            'temp': temp,
            'level': level
        }
        return data
    
    def print_data(self):
        data = self.create_data()
        if data:
            print(data)
