import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from typing import Optional, Any


class PlotFrame(tk.Frame):
    """
    Class representing the frame for displaying a plot in the application.
    """

    def __init__(self, parent: tk.Frame, brain_manager: Any, number_epoch: Optional[int]) -> None:
        """
        Initialize the PlotFrame.

        Args:
            parent (tk.Frame): The parent tkinter frame.
            brain_manager (BrainManager): The brain manager instance.
            number_epoch (Optional[int]): Number of epochs to study, if None, the chart does not display a progress bar.
        """

        super().__init__()

        self.brain_manager = brain_manager
        self.parent = parent
        self.number_each = number_epoch

        frame = tk.Frame(parent, bg="#cfcccc")
        frame.pack()

        fig = Figure(figsize=(5, 5), dpi=100, facecolor='#cfcccc')

        self.plot = fig.add_subplot(111)
        self.plot.set(xlabel='Epoch', ylabel='Loss', title='Progress')

        self.canvas = FigureCanvasTkAgg(fig, master=frame)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side="top")

        toolbar = NavigationToolbar2Tk(self.canvas, parent)
        toolbar.update()

        if self.number_each is not None:
            style = ttk.Style()
            style.theme_use('default')
            style.configure("red.Horizontal.TProgressbar", background='#4ac5e0', foreground='#4ac5e0')

            self.progress_bar = ttk.Progressbar(frame, length=300, mode='determinate', style="red.Horizontal.TProgressbar")
            self.progress_bar.pack(side="left", padx=45, pady=20, anchor="e")

            self.value_label = tk.Label(frame, text=f"0 / {self.number_each}", font=("Helvetica", 16), background="#cfcccc")
            self.value_label.pack(side="left", anchor="w")

            self.plot.plot(range(1, 2), [[0, 0]])
            self.plot.legend(["Training Loss", "Testing Loss"], loc="upper right")
            self.plot.set_ylim(0, 3)
            self.plot.set_xlim(0, 5)

        else:
            self.plot.plot(range(1, self.brain_manager.sizeHistory() + 1), self.brain_manager.getHistory())
            self.plot.legend(["Training Loss", "Testing Loss"], loc="upper right")

    def __del__(self) -> None:
        """
        Destructor to clean up frame elements.

        Returns:
            None
        """

        self.canvas.get_tk_widget().destroy()
        self.progress_bar.destroy()
        self.value_label.destroy()
        super().destroy()

    def update(self, now_epoch: int) -> None:
        """
        Update the plot and progress bar.

        Args:
            now_epoch (int): The current epoch.

        Returns:
            None
        """

        self.plot.clear()
        self.plot.set(xlabel='Epoch', ylabel='Loss', title='Progress')
        self.plot.plot(range(1, self.brain_manager.sizeHistory() + 1), self.brain_manager.getHistory())
        self.plot.legend(["Training Loss", "Testing Loss"], loc="upper right")
        self.canvas.draw()

        self.progress_bar["value"] = 100 * now_epoch / self.number_each
        self.value_label["text"] = f"{now_epoch} / {self.number_each}"

        if now_epoch == self.number_each:
            self.value_label.config(foreground="#4293c2")