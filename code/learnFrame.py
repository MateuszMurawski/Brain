import glob
import os
import tkinter as tk
from tkinter import filedialog
from typing import Any


class LearnFrame(tk.Frame):
    """
    LearnFrame class represents the frame for initiating the learning process.
    """

    def __init__(self, parent: tk.Widget, brain_manager: Any) -> None:
        """
        Initializes the LearnFrame.

        Args:
            parent (tk.Widget): Parent widget.
            brain_manager (BrainManager): Reference to the BrainManager instance.

        Returns:
            None
        """

        super().__init__()

        self.vcmd = (self.register(self.validateNumber))
        self.brain_manager = brain_manager

        frame_1 = tk.Frame(parent, bg="#cfcccc")
        frame_1.pack(side='top', pady=20)

        self.entry_path = tk.Entry(frame_1, width=45, font=("Helvetica", 13))
        self.entry_path.insert(0, "Folder with dataset for learning:")
        self.entry_path.config(state="disabled")
        self.entry_path.pack(side='left')

        self.button_browse = tk.Button(frame_1, text="Browse", width=10, height=1, font=("Helvetica", 13), relief=tk.FLAT, borderwidth=5, background="#4ac5e0", highlightthickness=1, bd=0, command=self.openFileDialog)
        self.button_browse.pack(side='left', padx=10)

        frame_2 = tk.Frame(parent, bg="#cfcccc")
        frame_2.pack(side='top', pady=20)

        self.label_each = tk.Label(frame_2, text="Number of epochs to study:", background="#cfcccc", font=("Helvetica", 13))
        self.label_each.pack(side="left", padx=10)

        self.entry_each = tk.Entry(frame_2, width=5, font=("Helvetica", 13), validate='all',
                                   validatecommand=(self.vcmd, '%P'))
        self.entry_each.pack(side="left", padx=10)
        self.entry_each.insert(0, 10)

        frame_3 = tk.Frame(parent, bg="#cfcccc")
        frame_3.pack(side='bottom', pady=60)

        self.button_start_learning = tk.Button(frame_3, width=25, height=2, font=("Helvetica", 15), relief=tk.FLAT, borderwidth=5, background="#4ac5e0", highlightthickness=1, bd=0, text="Start learning", command=self.runLearning)
        self.button_start_learning.pack(side="bottom", padx=10)
        self.button_start_learning.config(state="disabled")

    def __del__(self) -> None:
        """
        Destructor for cleaning up frame elements.

        Returns:
            None
        """

        self.entry_path.destroy()
        self.button_browse.destroy()
        self.label_each.destroy()
        self.entry_each.destroy()
        self.button_start_learning.destroy()
        super().destroy()

    def openFileDialog(self) -> None:
        """
        Open a file dialog to choose the dataset folder.

        Returns:
            None
        """

        folder_path = filedialog.askdirectory()

        if folder_path:
            self.entry_path.config(state="normal")
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, folder_path)
            self.entry_path.config(state="disabled")

            if self.validateData(folder_path):
                self.button_start_learning.config(state="normal")
            else:
                self.button_start_learning.config(state="disabled")

    def runLearning(self) -> None:
        """
        Initiates the learning process.

        Returns:
            None
        """

        if self.entry_each.get() != "" and int(self.entry_each.get()) > 0:
            self.brain_manager.clearPaint()
            self.brain_manager.runLearning(self.entry_path.get(), int(self.entry_each.get()))
            self.brain_manager.closeWindowLearn()

    def validateNumber(self, P: str) -> bool:
        """
        Validates if the entered value is a positive integer.

        Args:
            P (str): The value entered the entry widget.

        Returns:
            bool: True if the value is a positive integer or an empty string, False otherwise.
        """

        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def validateData(self, path: str) -> bool:
        """
        Validates if the provided path contains a valid dataset.

        Args:
            path (str): Path to the dataset.

        Returns:
            bool: True if the dataset is valid, False otherwise.
        """

        files = glob.glob(os.path.join(path, "*"))

        if not files:
            return False

        for element in os.listdir(path):
            element_path = os.path.join(path, element)

            if os.path.isfile(element_path):
                return False

        return True