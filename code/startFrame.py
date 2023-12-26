import tkinter as tk
from typing import Any


class StartFrame(tk.Frame):
    """
    Class representing the start frame of the application.
    """

    def __init__(self, parent: tk.Frame, brain_manager: Any) -> None:
        """
        Initialize the StartFrame.

        Args:
            parent (tk.Frame): The parent tkinter frame.
            brain_manager (BrainManager): The brain manager instance.
        """

        super().__init__()

        self.parent = parent

        self.create_button = tk.Button(parent, text="Create new brain", width=30, height=2, font=("Helvetica", 15), relief=tk.FLAT, borderwidth=5, background="#4ac5e0", highlightthickness=1, bd=0, command=brain_manager.newWindowCreate)
        self.create_button.grid(row=0, column=0, padx=35)

        self.open_button = tk.Button(parent, text="Open brain", width=30, height=2, font=("Helvetica", 15), relief=tk.FLAT, borderwidth=5, background="#4ac5e0", highlightthickness=1, bd=0, command=brain_manager.menu.openSavedParametersCNN)
        self.open_button.grid(row=2, column=0, pady=15, padx=35)

    def __del__(self) -> None:
        """
        Destructor to clean up frame elements.

        Returns:
            None
        """

        self.open_button.destroy()
        self.create_button.destroy()
        super().destroy()