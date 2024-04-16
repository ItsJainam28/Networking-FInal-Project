"""
COMP216 - Final Project - Subscriber GUI

Group: 1
Group Members:
    Handa, Karan
    Ngan, Tsang Kwong
    Patel, Jainam
    Wong, Yu Kwan
    ZHANG, AILIN

Date: April 16, 2024
"""

import threading
import time
import tkinter as tk
from tkinter import ttk
import json
import paho.mqtt.client as mqtt
from Wk12a_subscriber import Subscriber


class SubscriberTableGUI:
    """
    A class representing the GUI for the MQTT Subscriber.

    Attributes:
        root (tkinter.Tk): The root window of the GUI.
        subscriber (Subscriber): An instance of the Subscriber class.
        frame (tkinter.Frame): A frame for organizing widgets.
        data_label (tkinter.Label): A label for displaying received data.
        tree (ttk.Treeview): A treeview widget to display data in tabular format.
        subscriber_thread_started (bool): A flag to track whether the subscriber thread has started.

    Methods:
        __init__(self, root): Initializes the SubscriberTableGUI class.
        create_widgets(self): Creates the widgets for the GUI.
        start_subscribing(self): Starts the subscriber thread.
        stop_subscribing(self): Stops the subscriber thread.
        update_data_display(self): Updates the display with new data.
        _update_data_display_thread(self): Thread function to periodically check for new data and update the display.
        display_data(self, data_dict): Displays received data in the GUI.
    """

    def __init__(self, root):
        """
        Initializes the SubscriberTableGUI class.

        Args:
            root (tkinter.Tk): The root window of the GUI.
        """
        self.root = root
        self.subscriber = Subscriber()  # Initialize an instance of your Subscriber class
        self.create_widgets()
        self.subscriber_thread_started = False  # Flag to track whether subscriber thread has started

    def create_widgets(self):
        """
        Creates the widgets for the GUI.
        """
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.data_label = tk.Label(self.frame, text="Received Data:", font=("Arial", 12))
        self.data_label.pack()

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Time", "Temperature", "Level"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Temperature", text="Temperature")
        self.tree.heading("Level", text="Level")
        self.tree.pack()

    def start_subscribing(self):
        """
        Starts the subscriber thread.
        """
        if not self.subscriber_thread_started:
            self.subscriber.create_client()
            self.subscriber.start_subscriber_thread()
            self.subscriber_thread_started = True

    def stop_subscribing(self):
        """
        Stops the subscriber thread.
        """
        self.subscriber.stop_subscriber_thread()
        self.subscriber_thread_started = False

    def update_data_display(self):
        """
        Updates the display with new data.
        """
        threading.Thread(target=self._update_data_display_thread, daemon=True).start()

    def _update_data_display_thread(self):
        """
        Thread function to periodically check for new data and update the display.
        """
        while True:
            if self.subscriber_thread_started and self.subscriber.data_points:
                data_dict = {
                    "id": self.subscriber.data_ids[0],
                    "time": time.strftime("%a %b %d %H:%M:%S %Y"),
                    "temp": self.subscriber.data_points[0],
                    "level": self.subscriber.data_level[0]
                }
                self.display_data(data_dict)
                self.subscriber.data_ids.pop(0)
                self.subscriber.data_points.pop(0)
                self.subscriber.data_level.pop(0)
            time.sleep(5)

    def display_data(self, data_dict):
        """
        Displays received data in the GUI.

        Args:
            data_dict (dict): The dictionary containing the received data.
        """
        self.tree.insert("", tk.END, values=(data_dict["id"], data_dict["time"], data_dict["temp"], data_dict["level"]))
