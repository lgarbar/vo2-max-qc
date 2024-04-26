import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt

class DataFrameViewer(QMainWindow):
    def __init__(self, dataframe):
        super().__init__()

        self.dataframe = dataframe
        self.current_row = 0
        self.current_col = 0

        self.setWindowTitle("DataFrame Viewer")
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget()
        self.table.setRowCount(dataframe.shape[0])
        self.table.setColumnCount(dataframe.shape[1])

        for i, column_name in enumerate(dataframe.columns):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(column_name))
            for j, value in enumerate(dataframe[column_name]):
                self.table.setItem(j, i, QTableWidgetItem(str(value)))

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        # Add navigation buttons
        self.button_up = QPushButton("Up")
        self.button_down = QPushButton("Down")
        self.button_left = QPushButton("Left")
        self.button_right = QPushButton("Right")

        self.button_up.clicked.connect(self.move_up)
        self.button_down.clicked.connect(self.move_down)
        self.button_left.clicked.connect(self.move_left)
        self.button_right.clicked.connect(self.move_right)

        layout.addWidget(self.button_up)
        layout.addWidget(self.button_down)
        layout.addWidget(self.button_left)
        layout.addWidget(self.button_right)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Highlight the initial cell
        self.highlight_current_cell()

    def keyPressEvent(self, event):
        # Handle arrow key presses
        if event.key() == Qt.Key_Up:
            self.move_up()
        elif event.key() == Qt.Key_Down:
            self.move_down()
        elif event.key() == Qt.Key_Left:
            self.move_left()
        elif event.key() == Qt.Key_Right:
            self.move_right()

    def move_up(self):
        if self.current_row > 0:
            self.clear_highlight()
            self.current_row -= 1
            self.highlight_current_cell()

    def move_down(self):
        if self.current_row < self.dataframe.shape[0] - 1:
            self.clear_highlight()
            self.current_row += 1
            self.highlight_current_cell()

    def move_left(self):
        if self.current_col > 0:
            self.clear_highlight()
            self.current_col -= 1
            self.highlight_current_cell()

    def move_right(self):
        if self.current_col < self.dataframe.shape[1] - 1:
            self.clear_highlight()
            self.current_col += 1
            self.highlight_current_cell()

    def highlight_current_cell(self):
        # Highlight current cell
        self.table.setCurrentCell(self.current_row, self.current_col)
        self.current_item = self.table.item(self.current_row, self.current_col)

        # Store original background color if it's not already stored
        if not hasattr(self, 'original_color'):
            self.original_color = self.current_item.background()

        self.current_item.setBackground(Qt.blue)

    def clear_highlight(self):
        # Clear previous cell's highlighting
        if self.current_item:
            self.current_item.setBackground(self.original_color)  # Set back to original background color

if __name__ == "__main__":
    # Create a sample DataFrame
    import pandas as pd
    data = {'A': [1, 2, 3, 4],
            'B': [5, 6, 7, 8],
            'C': [9, 10, 11, 12]}
    df = pd.DataFrame(data)

    # Create the application
    app = QApplication(sys.argv)

    # Create and show the DataFrameViewer
    viewer = DataFrameViewer(df)
    viewer.show()

    # Run the application
    sys.exit(app.exec_())
