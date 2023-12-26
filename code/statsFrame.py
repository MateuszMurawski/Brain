import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
from typing import List


class StatsFrame(tk.Frame):
    """
    Class representing the statistics frame of the application.
    """
    def __init__(self, parent: tk.Frame, number_labels_on_board: int) -> None:
        """
        Initialize the StatsFrame.

        Args:
            parent (tk.Frame): The parent tkinter frame.
            number_labels_on_board (int): The number of statistics elements.
        """

        super().__init__()

        self.parent = parent
        self.triple_list = []

        style = ttk.Style()
        style.theme_use('default')
        style.configure("red.Horizontal.TProgressbar", background='#4ac5e0', foreground='#4ac5e0')

        for i in range(number_labels_on_board):
            label = tk.Label(parent, text=f"Empty", font=("Arial", 15), background="#cfcccc")
            progress_bar = Progressbar(parent, mode="determinate", length=200, style="red.Horizontal.TProgressbar")
            value_label = tk.Label(parent, text=f"{i + 1} %", font=("Arial", 15), background="#cfcccc")
            self.triple_list.append([label, progress_bar, value_label])

        for i, (label, progress_bar, value_label) in enumerate(self.triple_list):
            label.grid(row=i, column=0, pady=5, padx=20)
            progress_bar.grid(row=i, column=1, padx=10)
            value_label.grid(row=i, column=2, padx=10)

        self.update([0] * number_labels_on_board)

    def __del__(self) -> None:
        """
        Destructor to clean up frame elements.

        Returns:
            None
        """

        for i, (label, progress_bar, value_label) in enumerate(self.triple_list):
            label.destroy()
            progress_bar.destroy()
            value_label.destroy()

        self.triple_list.clear()
        super().destroy()

    def update(self, stats_data: List[int]) -> None:
        """
        Update the statistics with new data.

        Args:
            stats_data (List[int]): The list of statistics data.

        Returns:
            None
        """

        for i, (_, progress_bar, value_label) in enumerate(self.triple_list):
            progress_value = (int(stats_data[i] * 10000)) / 100
            progress_bar["value"] = progress_value
            value_label["text"] = f"{progress_value} %"

    def updateLabels(self, labels: List[str]) -> None:
        """
        Update the labels for each statistic.

        Args:
            labels (List[str]): The list of labels.

        Returns:
            None
        """

        for i, (label, _, _) in enumerate(self.triple_list):
            if i < len(labels):
                label["text"] = labels[i]