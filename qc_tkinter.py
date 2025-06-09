import os
import sys
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from PIL import Image, ImageTk

def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Select CSV file
    csv_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if not csv_path:  # If user cancels CSV selection
        sys.exit("No CSV file selected")
    
    # Select image directory
    image_dir = filedialog.askdirectory(
        title="Select image directory"
    )
    
    if not image_dir:  # If user cancels directory selection
        sys.exit("No image directory selected")
    
    return csv_path, image_dir

class DataEditorGUI:
    def __init__(self, master, csv_path, image_dir, mode='row'):
        self.master = master
        self.csv_path = csv_path
        self.image_dir = image_dir
        self.mode = mode
        self.df = self.load_data()
        self.current_row = 0
        self.editor_initials = self.get_editor_initials()
        
        self.init_ui()

    def load_data(self):
        # Load the CSV file and create a copy with 'edited' tag
        df = pd.read_csv(self.csv_path)
        new_path = self.csv_path.replace('.csv', '_edited.csv')
        df['edited'] = False
        df['editor'] = ''
        df.to_csv(new_path, index=False)
        return df

    def get_editor_initials(self):
        # Prompt for editor initials
        return simpledialog.askstring("Editor Initials", "Enter your initials:")

    def init_ui(self):
        self.master.title('Data Editor')
        self.master.geometry('1200x800')

        # Create main frame
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left side: Data display and editing
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create Treeview for data display
        self.tree = ttk.Treeview(left_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Navigation and editing buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X)

        self.prev_button = ttk.Button(button_frame, text='Previous', command=self.prev_row)
        self.next_button = ttk.Button(button_frame, text='Next', command=self.next_row)
        self.edit_button = ttk.Button(button_frame, text='Edit', command=self.edit_cell)

        self.prev_button.pack(side=tk.LEFT)
        self.next_button.pack(side=tk.LEFT)
        self.edit_button.pack(side=tk.LEFT)

        # Right side: Image display
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.image_label = ttk.Label(right_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Load initial data
        self.update_table()
        self.load_current_row()

    def update_table(self):
        # Clear existing data
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Update the table with current row data
        columns = list(self.df.columns)
        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.insert("", "end", values=list(self.df.iloc[self.current_row]))

    def load_current_row(self):
        # Load data for the current row and update UI
        self.update_table()
        
        # Load and display image
        basename = self.df.loc[self.current_row, 'img_name']
        image_path = os.path.join(self.image_dir, basename)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((400, 400))  # Resize image to fit
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        else:
            self.image_label.config(text="Image not found")

    def prev_row(self):
        if self.current_row > 0:
            self.current_row -= 1
            self.load_current_row()

    def next_row(self):
        if self.current_row < len(self.df) - 1:
            self.current_row += 1
            self.load_current_row()

    def edit_cell(self):
        selected_item = self.tree.selection()[0]
        column = self.tree.identify_column(self.tree.winfo_pointerx() - self.tree.winfo_rootx())
        col_num = int(column.replace('#', '')) - 1
        col_name = self.df.columns[col_num]

        if col_name not in ['edited', 'editor']:
            current_value = self.tree.item(selected_item)['values'][col_num]
            new_value = simpledialog.askstring("Edit Value", f"Edit {col_name}:", initialvalue=current_value)

            if new_value is not None:
                self.df.at[self.current_row, col_name] = new_value
                self.df.at[self.current_row, 'edited'] = True
                self.df.at[self.current_row, 'editor'] = self.editor_initials
                self.save_edits()
                self.update_table()

    def save_edits(self):
        # Save edits to the CSV file
        self.df.to_csv(self.csv_path.replace('.csv', '_edited.csv'), index=False)

if __name__ == '__main__':
    # Get file paths from user
    test_fpath, image_dirs = select_files()
    
    root = tk.Tk()
    editor = DataEditorGUI(root, test_fpath, image_dirs)
    root.mainloop()