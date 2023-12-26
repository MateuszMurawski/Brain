import tkinter as tk
from typing import Any


class CreateFrame(tk.Frame):
    """
    Frame for creating a new brain.
    """

    def __init__(self, parent: tk.Widget, brain_manager: Any) -> None:
        """
        Initializes the CreateFrame.

        Args:
            parent (tk.Widget): Parent widget.
            brain_manager (BrainManager): Reference to the BrainManager instance.

        Returns:
            None
        """

        super().__init__()

        self.brain_manager = brain_manager

        self.vcmd = (self.register(self.validateNumber))

        self.frame_1 = tk.Frame(parent, bg="#cfcccc")
        self.frame_1.pack(padx=30, pady=30)

        self.frame_2 = tk.Frame(parent, bg="#cfcccc")
        self.frame_2.pack(padx=30, pady=30)

        self.number_labels = tk.Label(self.frame_1, text="Size of the brain (number of patterns to be taught):", background="#cfcccc", font=("Helvetica", 12))
        self.number_labels.pack(side='left', padx=10)

        self.number_entry = tk.Entry(self.frame_1, width=10, font=("Helvetica", 13), validate='all', validatecommand=(self.vcmd, '%P'))
        self.number_entry.pack(side='left', padx=10)
        self.number_entry.insert(0, 10)

        self.ok_button = tk.Button(self.frame_2, text="Create", width=25, height=2, font=("Helvetica", 15), relief=tk.FLAT, borderwidth=5, background="#4ac5e0", highlightthickness=1, bd=0, command=self.createNewBrain)
        self.ok_button.pack(pady=30)

    def __del__(self) -> None:
        """
        Destructor for cleaning up frame elements.

        Returns:
            None
        """

        self.frame_1.destroy()
        self.frame_2.destroy()
        self.number_entry.destroy()
        self.number_labels.destroy()
        self.ok_button.destroy()
        super().destroy()

    def createNewBrain(self) -> None:
        """
        Creates a new brain with the specified size.

        Returns:
            None
        """

        if self.number_entry.get() != "" and int(self.number_entry.get()) > 0:
            self.brain_manager.newCNN(int(self.number_entry.get()))
            self.brain_manager.clearPaint()
            self.brain_manager.closeWindowCreate()

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