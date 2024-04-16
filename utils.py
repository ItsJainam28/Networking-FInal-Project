"""
COMP216 - Final Project - Utils

Group: 1
Group Members:
    Handa, Karan
    Ngan, Tsang Kwong
    Patel, Jainam
    Wong, Yu Kwan
    ZHANG, AILIN

Date: April 16, 2024
"""

from random import uniform
from time import asctime
from json import dumps

class Util:
    """
    Utility class for creating temperature data.

    Attributes:
        start_id (int): The starting ID for the temperature data.
        _extreme_temp_interval (int): The interval at which extreme temperature is generated.

    Methods:
        create_data: Creates and returns a dictionary with temperature data.
        print_data: Prints the created temperature data.
    """

    def __init__(self):
        self.start_id = 100
        self._extreme_temp_interval = 10
        
    def create_data(self) -> dict:
        """
        Creates and returns a dictionary with temperature data.

        Returns:
            dict: A dictionary containing the temperature data.
        """
        self.start_id += 1
        self.temp = round(uniform(15, 23), 1)
        self.level = 'normal'

        if self.start_id % self._extreme_temp_interval == 0:
            self.temp = 24
            self.level = 'exteme'

        return {
            'id': self.start_id,
            'time': asctime(),
            'temp': self.temp,
            'level': self.level
        }
    
    def print_data(self):
        """
        Prints the created temperature data.
        """
        print(self.create_data())