import tkinter as tk
from tkinter import Menu, filedialog, DISABLED


class MenuBar:
    """
    Class representing the menu bar of the application.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """
        Initialize the menu bar.

        Args:
            parent (tk.Tk): The parent tkinter window.
        """

        self.parent = parent

        self.menu_bar = Menu(parent)

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New brain", command=self.parent.newWindowCreate)
        self.file_menu.add_command(label="Open brain", command=self.openSavedParametersCNN)
        self.file_menu.add_command(label="Save brain", state=DISABLED, command=lambda: self.saveParametersCNN(False))
        self.file_menu.add_command(label="Save as... brain", state=DISABLED, command=lambda: self.saveParametersCNN(True))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit program", command=parent.quit)
        self.menu_bar.add_cascade(label="Program manager", menu=self.file_menu)

        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Learn brain", state=DISABLED, command=self.parent.newWindowLearn)
        self.menu_bar.add_cascade(label="Learn", menu=self.edit_menu)

        self.view_menu = Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="History", state=DISABLED, command=self.parent.showHistory)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        parent.config(menu=self.menu_bar)

    def openSavedParametersCNN(self) -> None:
        """
        Open a dialog to choose a file with trained Brain parameters and load it.

        Returns:
            None
        """

        self.parent.path_to_save_brain = filedialog.askopenfilename(
            title="Choose a file with a trained Brain",
            filetypes=[("Brain", "*.pth")]
        )

        if self.parent.path_to_save_brain != "":
            try:
                self.parent.open(self.parent.path_to_save_brain)
                self.parent.clearPaint()
            except:
                pass

    def saveParametersCNN(self, state: bool) -> None:
        """
        Save the current Brain parameters to a file.

        Args:
            state (bool): If True, prompts the user for a new file name.

        Returns:
            None
        """

        if state or self.parent.path_to_save_brain is None:
            self.parent.path_to_save_brain = filedialog.asksaveasfilename(
                defaultextension=".pth",
                filetypes=[("Brain", "*.pth")]
            )

            if self.parent.path_to_save_brain == "":
                self.parent.path_to_save_brain = None
            else:
                self.parent.save(self.parent.path_to_save_brain)

        else:
            self.parent.save(self.parent.path_to_save_brain)