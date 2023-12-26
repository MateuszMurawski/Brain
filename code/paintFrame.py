import io
import tkinter as tk
from typing import Optional, Any

from PIL import Image, EpsImagePlugin


class PaintFrame(tk.Frame):
    """
    Class representing the canvas for drawing in the application.
    """

    def __init__(self, parent: tk.Frame, brain_manager: Any) -> None:
        """
        Initialize the PaintFrame.

        Args:
            parent (tk.Frame): The parent tkinter frame.
            brain_manager (BrainManager): The brain manager instance.
        """

        super().__init__()

        self.parent = parent
        self.brain_manager = brain_manager

        self.white_board = tk.Canvas(parent, bg='white', width=500, height=500)
        self.white_board.pack()

        self.clear_button = tk.Button(parent, text="Clear", width=20, height=2, font=("Helvetica", 15), relief=tk.FLAT, borderwidth=5, background="#4ac5e0", highlightthickness=1, bd=0, command=self.clearCanvas)
        self.clear_button.pack(pady=30)

        self.last_x: Optional[int] = None
        self.last_y: Optional[int] = None

        self.setDisplayPaint(False)

    def __del__(self) -> None:
        """
        Destructor to clean up frame elements.

        Returns:
            None
        """

        self.white_board.destroy()
        self.clear_button.destroy()
        super().destroy()

    def getStartPosition(self, event: tk.Event) -> None:
        """
        Get the starting position for drawing.

        Args:
            event (tk.Event): The tkinter event object.

        Returns:
            None
        """

        self.last_x, self.last_y = event.x, event.y

    def drawLine(self, event: tk.Event) -> None:
        """
        Draw a line on the canvas.

        Args:
            event (tk.Event): The tkinter event object.

        Returns:
            None
        """

        if self.last_x is not None and self.last_y is not None:
            self.white_board.create_line(self.last_x, self.last_y, event.x, event.y, fill='black', width=3, smooth=tk.TRUE, capstyle=tk.ROUND, joinstyle=tk.ROUND)
            self.last_x, self.last_y = event.x, event.y

    def clearCanvas(self) -> None:
        """
        Clear the canvas.

        Returns:
            None
        """

        try:
            self.white_board.delete("all")
            self.brain_manager.updateDataInStatsFrame([0] * self.brain_manager.number_labels_on_board)
        except:
            pass

    def setDisplayPaint(self, state: bool) -> None:
        """
        Set the display state for painting.

        Args:
            state (bool): If True, enable painting. If False, disable painting.

        Returns:
            None
        """

        if state:
            self.clear_button["state"] = "normal"
            self.white_board.configure(cursor="@brush.ico")
            self.white_board.bind("<Button-1>", self.getStartPosition)
            self.white_board.bind("<B1-Motion>", self.drawLine)
            self.white_board.bind("<ButtonRelease-1>", self.updateStatistic)
        else:
            self.clear_button["state"] = "disable"

    def updateStatistic(self, event: tk.Event) -> None:
        """
        Update the statistics based on the drawn image.

        Args:
            event (tk.Event): The tkinter event object.

        Returns:
            None
        """

        #EpsImagePlugin.gs_windows_binary = r'C:\Program Files\gs\gs10.01.0\bin\gswin64c'
        image = self.white_board.postscript(colormode='gray')
        image = Image.open(io.BytesIO(bytes(image, 'utf-8'))).convert('L')

        predict = self.brain_manager.predict(image)
        self.brain_manager.updateDataInStatsFrame(predict)