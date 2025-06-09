import os
import sys
import pandas as pd
import argparse
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, 
    QFileDialog, QScrollArea, QListWidget, QInputDialog, QMessageBox,
    QShortcut, QDialog, QHeaderView, QProgressBar
)
from PyQt5.QtGui import QPixmap, QKeySequence, QColor
from PyQt5.QtCore import Qt
import traceback

def select_files():
    app = QApplication(sys.argv)
    
    # Select CSV file
    csv_path, _ = QFileDialog.getOpenFileName(
        None,
        "Select CSV file",
        "",
        "CSV files (*.csv);;All files (*.*)"
    )
    
    if not csv_path:  # If user cancels CSV selection
        sys.exit("No CSV file selected")
    
    # Select image directory
    image_dir = QFileDialog.getExistingDirectory(
        None,
        "Select image directory"
    )
    
    if not image_dir:  # If user cancels directory selection
        sys.exit("No image directory selected")
    
    return csv_path, image_dir

class EditableTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cellChanged.connect(self.on_cell_changed)
        self.last_edited_cell = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.on_enter_pressed()
        else:
            super().keyPressEvent(event)

    def on_enter_pressed(self):
        if self.last_edited_cell:
            row, col = self.last_edited_cell
            self.cellChanged.emit(row, col)
            self.last_edited_cell = None

    def on_cell_changed(self, row, col):
        self.last_edited_cell = (row, col)

class DataEditorGUI(QMainWindow):
    def __init__(self, csv_path, image_dir, verbose=True, show_all=False):
        super().__init__()
        self.original_csv_path = csv_path
        self.csv_path = self.get_edited_csv_path(csv_path)
        self.image_dir = image_dir
        self.verbose = verbose
        self.show_all = show_all
        self.df = self.load_data()
        self.filtered_indices = self.get_filtered_indices()
        self.current_index = 0
        self.editor_initials = self.get_editor_initials()
        
        self.init_ui()

    def get_edited_csv_path(self, original_path):
        edited_path = original_path.rsplit('.', 1)[0] + '_edited.csv'
        if os.path.exists(edited_path):
            print(f"Using existing edited file: {edited_path}")
            
        else:
            print(f"No edited file found, will create: {edited_path}")
        return edited_path

    def load_data(self):
        try:
            print(f"Attempting to load data from: {self.csv_path}")
            if not os.path.exists(self.csv_path):
                df = pd.read_csv(self.original_csv_path)
                print(f"Created new edited file: {self.csv_path}")
                df['edited'] = False
                df['editor'] = ''
                df['viewed'] = False  # Add viewed column
                df.to_csv(self.csv_path, index=False)
            else:
                df = pd.read_csv(self.csv_path)
                if 'viewed' not in df.columns:  # Add viewed column if it doesn't exist
                    df['viewed'] = False
                    df.to_csv(self.csv_path, index=False)
                print(f"Successfully loaded data, shape: {df.shape}")
            return df
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            traceback.print_exc()
            sys.exit(1)

    def get_editor_initials(self):
        initials, ok = QInputDialog.getText(self, 'Editor Initials', 'Enter your initials:')
        print(f"Editor initials: {initials}")
        return initials if ok else ''

    def get_filtered_indices(self):
        if self.show_all:
            # Show all rows if show_all is True
            return self.df.index.tolist()
        elif 'bad_vals' in self.df.columns and not self.verbose:
            # Show only bad values that haven't been viewed
            return self.df[(self.df['bad_vals'] == True) & (self.df['viewed'] == False)].index.tolist()
        else:
            # Show only unviewed rows
            return self.df[self.df['viewed'] == False].index.tolist()

    def init_ui(self):
        # Set up the main window and layouts
        self.setWindowTitle('Data Editor')
        self.setGeometry(100, 100, 1600, 900)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()  # Changed to QVBoxLayout for vertical stacking
        main_widget.setLayout(main_layout)

        # Add progress bar at the top
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat(f"%p% ({self.current_index}/{len(self.filtered_indices)} files viewed)")
        self.update_progress_bar()
        main_layout.addWidget(self.progress_bar)

        # Content layout
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Left side: Data display and editing
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        self.table = EditableTableWidget()
        self.table.cellChanged.connect(self.on_cell_edit)
        self.update_table()
        left_layout.addWidget(self.table)

        # Navigation and editing buttons
        button_layout = QHBoxLayout()
        self.prev_button = QPushButton('Previous')
        self.next_button = QPushButton('Next')
        self.edit_button = QPushButton('Edit')
        self.select_button = QPushButton('Select')
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.select_button)
        left_layout.addLayout(button_layout)

        # Right side: Image display
        right_widget = QScrollArea()
        self.image_label = QLabel()
        right_widget.setWidget(self.image_label)
        right_widget.setWidgetResizable(True)

        # Set layout proportions
        content_layout.addWidget(left_widget, 1)
        content_layout.addWidget(right_widget, 2)

        # Connect buttons to functions
        self.prev_button.clicked.connect(self.prev_item)
        self.next_button.clicked.connect(self.next_item)
        self.edit_button.clicked.connect(self.edit_cell)
        self.select_button.clicked.connect(self.select_mode)

        # Set up keyboard shortcuts
        QShortcut(QKeySequence(Qt.Key_Left), self, self.prev_item)
        QShortcut(QKeySequence(Qt.Key_Right), self, self.next_item)
        QShortcut(QKeySequence(Qt.Key_Up), self, lambda: self.move_cell('up'))
        QShortcut(QKeySequence(Qt.Key_Down), self, lambda: self.move_cell('down'))

        # Load initial data
        self.load_current_row()

    def update_table(self):
        # Update the table with current row data (transposed)
        self.table.cellChanged.disconnect(self.on_cell_edit)  # Temporarily disconnect to avoid triggering while updating
        self.table.clear()
        self.table.setRowCount(len(self.df.columns))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Field', 'Value'])

        current_row = self.filtered_indices[self.current_index]
        for row, (col_name, value) in enumerate(self.df.iloc[current_row].items()):
            self.table.setItem(row, 0, QTableWidgetItem(col_name))
            self.table.setItem(row, 1, QTableWidgetItem(str(value)))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.cellChanged.connect(self.on_cell_edit)  # Reconnect after updating

    def load_current_row(self):
        # Load data for the current row and update UI
        self.update_table()
        
        # Load and display image
        current_row = self.filtered_indices[self.current_index]
        basename = self.df.loc[current_row, 'img_name']
        image_path = os.path.join(self.image_dir, basename)
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.image_label.setFixedSize(pixmap.size())
            # Mark as viewed when loading the image
            self.df.at[current_row, 'viewed'] = True
            self.save_edits()
        else:
            self.image_label.setText("Image not found")

    def update_progress_bar(self):
        total_files = len(self.filtered_indices)
        if total_files == 0:
            progress = 100
        else:
            progress = int((self.current_index + 1) / total_files * 100)
        
        self.progress_bar.setValue(progress)
        
        # Calculate color based on progress
        if progress <= 50:
            # Red to Yellow transition (0-50%)
            ratio = progress / 50
            red = 255
            green = int(255 * ratio)
            blue = 0
        else:
            # Yellow to Green transition (50-100%)
            ratio = (progress - 50) / 50
            red = int(255 * (1 - ratio))
            green = 255
            blue = 0
        
        color = QColor(red, green, blue)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {color.name()};
            }}
        """)

    def prev_item(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_row()
            self.update_progress_bar()

    def next_item(self):
        if self.current_index < len(self.filtered_indices) - 1:
            self.current_index += 1
            self.load_current_row()
            self.update_progress_bar()

    def on_cell_edit(self, row, col):
        if col == 1:  # Only edit value column
            col_name = self.table.item(row, 0).text()
            new_value = self.table.item(row, 1).text()

            if col_name not in ['edited', 'editor']:
                print(f"Editing cell: {col_name}, New value: {new_value}")
                current_row = self.filtered_indices[self.current_index]
                self.df.at[current_row, col_name] = new_value
                self.df.at[current_row, 'edited'] = True
                self.df.at[current_row, 'editor'] = self.editor_initials
                self.save_edits()

    def edit_cell(self):
        current_item = self.table.currentItem()
        if current_item is not None and current_item.column() == 1:  # Only edit value column
            row = current_item.row()
            col_name = self.table.item(row, 0).text()

            if col_name not in ['edited', 'editor']:
                current_value = current_item.text()
                new_value, ok = QInputDialog.getText(self, f"Edit {col_name}", f"Enter new value for {col_name}:", text=current_value)

                if ok and new_value != current_value:
                    print(f"Editing cell: {col_name}, Old value: {current_value}, New value: {new_value}")
                    current_row = self.filtered_indices[self.current_index]
                    self.df.at[current_row, col_name] = new_value
                    self.df.at[current_row, 'edited'] = True
                    self.df.at[current_row, 'editor'] = self.editor_initials
                    self.save_edits()
                    self.update_table()

    def save_edits(self):
        try:
            print(f"Attempting to save edits to: {self.csv_path}")
            self.df.to_csv(self.csv_path, index=False)
            print("Edits saved successfully")
        except Exception as e:
            error_msg = f"An error occurred while saving: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            QMessageBox.critical(self, "Save Error", error_msg)

    def select_mode(self):
        # Implement select mode functionality
        select_dialog = QDialog(self)
        select_dialog.setWindowTitle("Select Basename")
        select_dialog.setGeometry(200, 200, 300, 400)

        layout = QVBoxLayout()
        listbox = QListWidget()
        layout.addWidget(listbox)

        for index in self.filtered_indices:
            basename = self.df.loc[index, 'img_name']
            listbox.addItem(basename)

        select_dialog.setLayout(layout)

        def on_select():
            selected_items = listbox.selectedItems()
            if selected_items:
                selected_basename = selected_items[0].text()
                selected_index = self.df[self.df['img_name'] == selected_basename].index[0]
                self.current_index = self.filtered_indices.index(selected_index)
                self.load_current_row()
                self.update_progress_bar()
                select_dialog.accept()

        select_button = QPushButton("Select")
        select_button.clicked.connect(on_select)
        layout.addWidget(select_button)

        select_dialog.exec_()

    def move_cell(self, direction):
        current = self.table.currentItem()
        if current is None:
            return

        row, col = current.row(), current.column()

        if direction == 'up' and row > 0:
            self.table.setCurrentCell(row - 1, col)
        elif direction == 'down' and row < self.table.rowCount() - 1:
            self.table.setCurrentCell(row + 1, col)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Editor GUI')
    parser.add_argument('--verbose', action='store_true', help='Show all rows/basenames')
    parser.add_argument('--show-all', action='store_true', help='Show all rows including viewed ones')
    args = parser.parse_args()

    # Get file paths from user
    test_fpath, image_dirs = select_files()
    
    app = QApplication(sys.argv)
    editor = DataEditorGUI(test_fpath, image_dirs, verbose=args.verbose, show_all=args.show_all)
    editor.show()
    sys.exit(app.exec_())