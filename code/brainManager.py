import tkinter as tk
from PIL.Image import Image
from typing import Optional, List

from learn import Learn
from menuBar import MenuBar
from createFrame import CreateFrame
from learnFrame import LearnFrame
from paintFrame import PaintFrame
from plotFrame import PlotFrame
from startFrame import StartFrame
from statsFrame import StatsFrame


class BrainManager(tk.Tk):
    """
    The main application class for managing the brain learning process.
    """

    def __init__(self) -> None:
        """
        Initialize the main application.

        Returns:
            None
        """

        super().__init__()

        self.new_window_1: Optional[tk.Toplevel] = None
        self.new_window_2: Optional[tk.Toplevel] = None
        self.plot_frame: Optional[PlotFrame] = None
        self.learn_brain_frame: Optional[LearnFrame] = None
        self.create_window_frame: Optional[CreateFrame] = None
        self.learn: Optional[Learn] = None

        self.path_to_save_brain: Optional[str] = None
        self.number_labels_on_board: int = 10
        self.labels_list: List[str] = []

        self.title("Brain")
        self.geometry("1020x660")
        self.resizable(width=False, height=False)
        self.configure(bg="#cfcccc")

        self.menu = MenuBar(self)

        self.frame_container_left = tk.Frame(self, bg="#cfcccc")
        self.frame_container_left.grid(row=0, column=0, padx=40, pady=30, sticky="nw")

        self.frame_container_right = tk.Frame(self, bg="#cfcccc")
        self.frame_container_right.grid(row=0, column=1, padx=0, pady=30, sticky="nw")

        self.left_frame = PaintFrame(self.frame_container_left, self)
        self.right_frame = StartFrame(self.frame_container_right, self)

    def changeToStatsFrame(self) -> None:
        """
        Switch to the stats frame.

        Returns:
            None
        """

        self.right_frame.destroy()
        self.right_frame = StatsFrame(self.frame_container_right, self.number_labels_on_board)

        self.left_frame.setDisplayPaint(True)
        self.menu.view_menu.entryconfig("History", state=tk.NORMAL)
        self.menu.edit_menu.entryconfig("Learn brain", state=tk.NORMAL)
        self.menu.file_menu.entryconfig("Save brain", state=tk.NORMAL)
        self.menu.file_menu.entryconfig("Save as... brain", state=tk.NORMAL)

    def updateDataInStatsFrame(self, stats_data: List[float]) -> None:
        """
        Update the data in the stats frame.

        Args:
            stats_data (List[float]): List of statistics data.

        Returns:
            None
        """

        self.right_frame.update(stats_data)

    def updateStatsLabel(self) -> None:
        """
        Update labels in the stats frame.

        Returns:
            None
        """

        self.right_frame.updateLabels(self.labels_list)

    def newWindowCreate(self) -> None:
        """
        Open the window for creating a new brain.

        Returns:
            None
        """

        self.new_window_1 = tk.Toplevel()
        self.new_window_1.grab_set()

        self.new_window_1.title("Create new brain")
        self.new_window_1.geometry("500x270")
        self.new_window_1.resizable(width=False, height=False)
        self.new_window_1.configure(bg="#cfcccc")

        frame = tk.Frame(self.new_window_1, bg="#cfcccc")
        frame.pack()

        self.create_window_frame = CreateFrame(frame, self)

    def newWindowLearn(self) -> None:
        """
        Open the window for learning.

        Returns:
            None
        """

        self.new_window_1 = tk.Toplevel()
        self.new_window_1.grab_set()

        self.new_window_1.title("Learn brain")
        self.new_window_1.geometry("600x300")
        self.new_window_1.resizable(width=False, height=False)
        self.new_window_1.configure(bg="#cfcccc")

        frame = tk.Frame(self.new_window_1, bg="#cfcccc")
        frame.pack()

        self.learn_brain_frame = LearnFrame(frame, self)

    def newWindowPlot(self, number_epoch: Optional[int]) -> None:
        """
        Open the window for plotting.

        Args:
            number_epoch (Optional[int]): Number of epochs to study, if None, the chart does not display a progress bar.

        Returns:
            None
        """

        self.new_window_2 = tk.Toplevel()
        self.new_window_2.grab_set()

        self.new_window_2.title("History learning brain")
        if number_epoch is None:
            self.new_window_2.geometry("500x540")
        else:
            self.new_window_2.geometry("500x600")

        self.new_window_2.resizable(width=False, height=False)
        self.new_window_2.configure(bg="#cfcccc")

        frame = tk.Frame(self.new_window_2, bg="#cfcccc")
        frame.pack()

        self.plot_frame = PlotFrame(frame, self, number_epoch)

    def newCNN(self, size_output: int) -> None:
        """
        Create a new CNN.

        Args:
            size_output (int): Number of labels in the output layer.

        Returns:
            None
        """

        self.number_labels_on_board = size_output
        self.learn = Learn(self)

    def closeWindowCreate(self) -> None:
        """
        Close the window for creating a new brain.

        Returns:
            None
        """

        self.new_window_1.destroy()
        self.changeToStatsFrame()

    def closeWindowLearn(self) -> None:
        """
        Close the window for learning.

        Returns:
            None
        """

        self.new_window_1.destroy()

    def predict(self, image: Image) -> List[float]:
        """
        Make a prediction using the trained model.

        Args:
            image (PIL.Image.Image): Image to predict.

        Returns:
            List[float]: List of prediction results.
        """

        return self.learn.predict(image)

    def addLabel(self, labels: List[str]) -> None:
        """
        Add labels to the list.

        Args:
            labels (List[str]): List of labels to add.

        Returns:
            None
        """

        for label in labels:
            if label not in self.labels_list:
                self.labels_list.append(label)

    def runLearning(self, path: str, number_epoch: int) -> None:
        """
        Run the learning process.

        Args:
            path (str): Path to the dataset.
            number_epoch (int): Number of epochs to run.

        Returns:
            None
        """

        self.learn.startLearn(path, number_epoch)

    def updatePlot(self, current_epoch: int) -> None:
        """
        Update the plot with the current epoch.

        Args:
            current_epoch (int): Current epoch.

        Returns:
            None
        """

        self.plot_frame.update(current_epoch)

    def save(self, file_name: str) -> None:
        """
        Save the trained model.

        Args:
            file_name (Optional[str]): File name for saving.

        Returns:
            None
        """

        self.learn.save(file_name)

    def open(self, file_name: str) -> None:
        """
        Open a trained model.

        Args:
            file_name (str): File name to open.

        Returns:
            None
        """

        self.learn = Learn(self)
        self.learn.open(file_name)

        self.changeToStatsFrame()
        self.updateStatsLabel()

    def showHistory(self) -> None:
        """
        Open the window to show training history.

        Returns:
            None
        """

        self.newWindowPlot(None)

    def clearPaint(self) -> None:
        """
        Clear the paint on the canvas.

        Returns:
            None
        """

        self.left_frame.clearCanvas()

    def sizeHistory(self) -> int:
        """
        Get the size of the training history.

        Returns:
            int: The number of epochs in the training history.
        """

        return len(self.learn.history)

    def getHistory(self) -> List[List[float]]:
        """
        Get the training history.

        Returns:
            List[List[float]]: The list containing the training history.
        """

        return self.learn.history
