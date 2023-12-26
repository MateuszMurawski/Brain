import threading
from typing import Optional, List, Any

import torch
from PIL.Image import Image
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

from cnn import CNN


class Learn:
    """
    The Learn class manages the training and prediction processes for the neural network model.
    """

    def __init__(self, brain_manager: Any):
        """
        Initialize the Learn object.

        Args:
            brain_manager (BrainManager): Reference to the BrainManager instance.

        Returns:
            None
        """

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.brain_manager = brain_manager
        self.brain_manager.title(f"Brain   ( program use: {self.device} )")

        self.train_data: Optional[datasets.ImageFolder] = None
        self.cnn = CNN(brain_manager.number_labels_on_board).to(self.device)
        self.optimer: torch.optim = torch.optim.Adam(self.cnn.parameters(), lr=0.0001)
        self.criterion = torch.nn.CrossEntropyLoss()

        self.history: List[List[float, float]] = []

    def predict(self, image: Image) -> List[float]:
        """
        Make predictions using the trained model.

        Args:
            image (PIL.Image.Image): Image to predict.

        Returns:
            List[float]: List of prediction probabilities.
        """

        transform = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])
        image = transform(image)
        image = torch.unsqueeze(image, 0)

        self.cnn.eval().to(self.device)
        with torch.no_grad():
            return torch.exp(self.cnn(image))[0].tolist()

    def fit(self, train_data: DataLoader, test_data: DataLoader, epochs: int) -> None:
        """
        Train the model using the provided data.

        Args:
            train_data (DataLoader): DataLoader object containing training data.
            test_data (DataLoader): DataLoader object containing testing/validation data.
            epochs (int): Number of training epochs.

        Returns:
            None
        """

        self.cnn.train().to(self.device)

        for epoch in range(epochs):
            train_loss = 0.0
            test_loss = 0.0

            for inputs, labels in train_data:
                self.optimer.zero_grad()

                inputs, labels = inputs.to(self.device), labels.to(self.device)

                outputs = self.cnn(inputs)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimer.step()
                train_loss += loss.item()

            train_loss = train_loss / len(train_data)

            for inputs, labels in train_data:
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                outputs = self.cnn(inputs)
                loss = self.criterion(outputs, labels)
                test_loss += loss.item()

            test_loss = test_loss / len(test_data)

            self.history.append([train_loss, test_loss])
            self.brain_manager.updatePlot(epoch + 1)

    def loadData(self, path: str) -> None:
        """
        Load and preprocess the training data.

        Args:
            path (str): Path to the training data.

        Returns:
            [DataLoader, DataLoader]: DataLoader objects containing training and test data.
        """

        train_transforms = transforms.Compose([transforms.RandomRotation(30),
                                               transforms.Grayscale(),
                                               transforms.Resize((256, 256)),
                                               transforms.ToTensor()])

        self.train_data = datasets.ImageFolder(path, transform=train_transforms)

        if len(self.train_data.classes) > self.brain_manager.number_labels_on_board:
            self.train_data.classes = self.train_data.classes[:self.brain_manager.number_labels_on_board]
            self.train_data.samples = [sample for sample, target in zip(self.train_data.samples, self.train_data.targets) if target < self.brain_manager.number_labels_on_board]
            self.train_data.targets = self.train_data.targets[:self.brain_manager.number_labels_on_board]

        self.train_data.class_to_idx = {cls: idx for idx, cls in enumerate(self.train_data.classes)}
        self.brain_manager.addLabel(self.train_data.classes)

        train_data, test_data = random_split(self.train_data, [int(len(self.train_data)*0.8), int(len(self.train_data)*0.2)])

        return [torch.utils.data.DataLoader(train_data, batch_size=64, shuffle=True, num_workers=4, pin_memory=True),
                torch.utils.data.DataLoader(test_data, batch_size=64, num_workers=4, pin_memory=True)]

    def startLearn(self, path: str, number_each: int) -> None:
        """
        Start the learning process.

        Args:
            path (str): Path to the training data.
            number_each (int): Number of epochs.

        Returns:
            None
        """

        data_set, test_set = self.loadData(path)
        self.brain_manager.newWindowPlot(number_each)

        fit_thread = threading.Thread(target=self.fit, args=(data_set, test_set, number_each))
        fit_thread.start()

        self.brain_manager.updateStatsLabel()

    def save(self, file_name: Optional[str] = 'brain_model') -> None:
        """
        Save the trained model and related information.

        Args:
            file_name (Optional[str]): Name of the file to save.

        Returns:
            None
        """

        torch.save({
            'model_state_dict': self.cnn.state_dict(),
            'labels': self.train_data.classes if self.train_data is not None else [],
            'model_architecture': self.cnn,
            'learn_history': self.history,
            'size_output': self.brain_manager.number_labels_on_board
        }, f'{file_name}')

    def open(self, file_name: str) -> None:
        """
        Open a saved model and related information.

        Args:
            file_name (str): Name of the file to open.

        Returns:
            None
        """

        checkpoint = torch.load(file_name)

        self.cnn = checkpoint['model_architecture']
        self.cnn.load_state_dict(checkpoint['model_state_dict'])
        self.brain_manager.labels_list = checkpoint['labels']
        self.history = checkpoint['learn_history']
        self.brain_manager.number_labels_on_board = checkpoint['size_output']