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
from SubscriberChartGUI import DisplayChart, Subscriber
from SubscriberTableGUI import SubscriberTableGUI
from wk14_email import EmailSender

class SubscriberGUI:
    """
    A GUI application for subscribing to temperature data and displaying it in a chart.

    Attributes:
        subcriberGUI (SubscriberTableGUI): The table GUI for displaying subscriber data.
        email_sender (EmailSender): The email sender for sending notifications.
        subscriber (Subscriber): The subscriber for receiving temperature data.
        chart (DisplayChart): The chart for displaying temperature data.
        _running (bool): Flag indicating if the subscription is running.
        _items_per_page (int): Number of items per page in the chart.
        _update_thread (Thread): Thread for updating data and drawing the chart.
    """

    def __init__(self, master):
        """
        Initializes the SubscriberGUI.

        Args:
            master (Tk): The root Tkinter window.
        """
        self.subcriberGUI = SubscriberTableGUI(master)
        self.create_widgets()
        self.email_sender = EmailSender()
        self.subscriber = Subscriber()
        self.subscriber.create_client()
        self.subcriberGUI.update_data_display()
        self.chart = DisplayChart(
            self.frame,
            600, 400,
            value_min=10,
            value_max=27,
        )
        self.chart.pack()
        self._running = False
        self._items_per_page = 6
        self._update_thread = None

    def create_widgets(self):
        """
        Creates the GUI widgets.
        """
        self.frame = tk.Frame(self.subcriberGUI.root)
        self.frame.pack(padx=10, pady=10)
        # Button to start subscribing
        self.start_button = tk.Button(self.frame, text="Start Subscribing", command=self.start_subscribing)
        self.start_button.pack(pady=10)

        # Button to stop subscribing
        self.stop_button = tk.Button(self.frame, text="Stop Subscribing", command=self.stop_subscribing, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def start_subscribing(self):
        """
        Starts the subscription process.
        """
        self.subcriberGUI.start_subscribing()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self._running = True
        self.subscriber.start_subscriber_thread()
        # Start the thread for updating data and drawing chart
        if not self._update_thread or not self._update_thread.is_alive():
            self._update_thread = threading.Thread(target=self._update_data_and_draw_chart)
            self._update_thread.daemon = True
            self._update_thread.start()

    def stop_subscribing(self):
        """
        Stops the subscription process.
        """
        self.subcriberGUI.stop_subscribing()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self._running = False  # Stop the thread

    def _update_data_and_draw_chart(self):
        """
        Updates the data and draws the chart periodically.
        """
        while len(self.subscriber.data_points) == 0:
            time.sleep(1)
        print("Data points:", self.subscriber.data_points)
        while self._running:
            if self.subscriber.data_points[-1] >= 24:
                self.email_sender.send_email(f"Sensor detected an extreme temperture: {self.subscriber.data_points[-1]} C")
            # Call the method to display list on the canvas
            self.draw_chart()
            # Sleep for a short while (5 seconds)
            time.sleep(5)

    def draw_chart(self, start_index: int = 0, end_index: int = None):
        """
        Draws the chart.

        Args:
            start_index (int): The start index of the data points.
            end_index (int): The end index of the data points.
        """
        end_index = end_index or min(len(self.subscriber.data_points), start_index + self._items_per_page)
        self.chart.clear()
        self.chart.draw_lines(self.subscriber.data_points[start_index:end_index], color="red")
        self.chart.draw_x_axis("Time", self.subscriber.data_ids[start_index:end_index])
        self.chart.draw_y_axis("Temperature", 1, "C")


def main():
    """
    Entry point of the application.
    """
    root = tk.Tk()
    app = SubscriberGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
