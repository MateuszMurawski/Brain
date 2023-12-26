import torch


class CNN(torch.nn.Module):
    """
    Convolutional Neural Network (CNN) for image classification.
    """

    def __init__(self, size_output) -> None:
        """
        Initialize the CNN model.

        Args:
            size_output (int): Number of output classes.

        Returns:
            None
        """

        super(CNN, self).__init__()

        self.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=16, kernel_size=7, stride=3)
        self.conv2 = torch.nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=1)
        self.conv3 = torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=3, padding=1)
        self.conv4 = torch.nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1)

        self.dropout1 = torch.nn.Dropout(0.5)
        self.dropout2 = torch.nn.Dropout(0.25)

        self.pool1 = torch.nn.MaxPool2d(2, 2)
        self.pool2 = torch.nn.MaxPool2d(2, 2)

        self.fc1 = torch.nn.Linear(3200, 256)
        self.fc2 = torch.nn.Linear(256, 128)
        self.fc3 = torch.nn.Linear(128, size_output)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Defines the forward pass of the CNN.

        Args:
            x (torch.Tensor): Input tensor.

        Returns:
            torch.Tensor: Output tensor.
        """

        x = torch.nn.functional.relu(self.conv1(x))
        x = torch.nn.functional.relu(self.conv2(x))
        x = self.pool1(x)
        x = torch.nn.functional.relu(self.conv3(x))
        x = self.pool2(x)
        x = torch.nn.functional.relu(self.conv4(x))
        x = torch.flatten(x, 1)

        x = torch.nn.functional.relu(self.fc1(x))
        x = self.dropout1(x)
        x = torch.nn.functional.relu(self.fc2(x))
        x = self.dropout2(x)
        x = self.fc3(x)

        x = torch.nn.functional.log_softmax(x, 1)

        return x