import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from PIL import Image, ImageTk
import os

class VO2_QC:
    def __init__(self):
        self.df = pd.DataFrame()  # Initialize an empty DataFrame
        self.current_row = 0
        self.root = tk.Tk()
        self.root.title("VO2 Quality Control")

        # Folder paths
        self.ptp_num = None
        self.folder_path = None
        self.edited_path = None

        # Create GUI components
        self.tree = ttk.Treeview(self.root, columns=('Value',), show='headings')  # Show only headings, no empty column
        self.tree.heading('Value', text='Value')
        self.label = tk.Label(self.root)
        self.import_button = tk.Button(self.root, text="Import Data", command=self.import_data)
        self.edit_button = tk.Button(self.root, text="Edit Cell", command=self.edit_cell)
        self.up_button = tk.Button(self.root, text="Up", command=lambda: self.navigate('up'))
        self.down_button = tk.Button(self.root, text="Down", command=lambda: self.navigate('down'))

        # Place GUI components
        self.tree.grid(row=0, column=0, rowspan=5, padx=10, pady=10)
        self.label.grid(row=0, column=2, padx=10, pady=10)
        self.import_button.grid(row=4, column=1, padx=10, pady=10)
        self.edit_button.grid(row=1, column=1, padx=10, pady=10)
        self.up_button.grid(row=2, column=1, padx=10, pady=10)
        self.down_button.grid(row=3, column=1, padx=10, pady=10)

        # Variable to hold the selected treeview item
        self.selected_item = None

        # Bind double click event to treeview item selection
        self.tree.bind("<Double-1>", self.on_double_click)

    def import_data(self):
        initial_dir = os.path.dirname(os.path.realpath(__file__))
        self.folder_path = filedialog.askdirectory(initialdir=initial_dir)
        self.ptp_num = self.folder_path.split('/')[-1]
        if self.folder_path:
            # If scoring a file for the first time
            if 'edited' not in self.folder_path:
                # Filter files with .txt extensions
                txt_files = [f for f in os.listdir(self.folder_path) if f.endswith('.txt') and self.ptp_num in f]

                # Assuming only one txt and one png file
                if len(txt_files) == 1:
                    txt_file = os.path.join(self.folder_path, txt_files[0])

                    # Parse and process the text file
                    data = []
                    with open(txt_file, 'r') as file:
                        for line in file:
                            line = line.strip()
                            if len(line.split(':')) > 1:
                                key, value = line.split(':')
                                key = self.format_index(key)
                                data.append([key] + [value.strip()])

                    # Store data in a DataFrame
                    self.df = pd.DataFrame(data, columns=['Index', 'Value'])
                    self.df.set_index('Index', inplace=True)

                    # Export DataFrame to CSV to the edited folder
                    self.edited_path = os.path.join("/".join(self.folder_path.split('/')[:-2]), 'edited', self.ptp_num)    
                    if not os.path.exists(self.edited_path):
                        os.makedirs(self.edited_path)
                    self.csv_file = os.path.join(self.edited_path, f'{self.ptp_num}_dataframe.csv')
                    self.df.to_csv(self.csv_file)
                
            # If rescoring an edited file  
            else:
                self.edited_path = self.folder_path
                self.csv_file = os.path.join(self.edited_path, f'{self.ptp_num}_dataframe.csv')
                self.folder_path = os.path.join("/".join(self.folder_path.split('/')[:-2]), 'data', self.ptp_num)
                
            # parse for .png files
            png_files = [f for f in os.listdir(self.folder_path) if f.endswith('.png') and self.ptp_num in f]
            if len(png_files) == 1:
                png_file = os.path.join(self.folder_path, png_files[0])

            # Display the image
            self.display_image(png_file)

            # Display the DataFrame in the treeview
            self.display_dataframe()

    def format_index(self, index):
        if 'O' in index:
            index = index.replace('O', '0') 
        if ' ' in index:
            index = index.replace(' ', '')
        return 'V' + ''.join(filter(str.isdigit, index))

    def display_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((400, 400), Image.LANCZOS)  # Resize the image with LANCZOS downsampling
        photo = ImageTk.PhotoImage(image)
        self.label.configure(image=photo)
        self.label.image = photo

    def display_dataframe(self):
        # Clear existing treeview
        self.tree.delete(*self.tree.get_children())

        # Read DataFrame from CSV
        df = pd.read_csv(self.csv_file)

        # Display DataFrame in a treeview
        self.tree["columns"] = list(df.columns)
        self.tree.heading('#0', text='Index')
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Adjust width of columns as needed
        for index, row in df.iterrows():
            self.tree.insert("", "end", text=index, values=list(row))

    def navigate(self, direction):
        if direction == 'up':
            if self.current_row > 0:
                self.current_row -= 1
        elif direction == 'down':
            if self.current_row < len(self.df) - 1:
                self.current_row += 1

        # Update GUI to reflect new current_row
        # Highlight the row in the treeview
        self.highlight_row()

    def highlight_row(self):
        # Highlight current row
        for item_id in self.tree.get_children():
            self.tree.selection_remove(item_id)
        item_id = self.tree.get_children()[self.current_row]
        self.tree.selection_add(item_id)
        self.tree.focus(item_id)
        self.tree.see(item_id)

    def on_double_click(self, event):
        # Get the selected item
        item_id = self.tree.selection()[0]

        # Get the index of the selected item
        index = self.tree.index(item_id)

        # Update current row
        self.current_row = index

        # Highlight the selected row
        self.highlight_row()

        # Edit the cell
        self.edit_cell()

    def edit_cell(self):
        # Get value of selected cell
        value = self.df.iloc[self.current_row]

        # Prompt for new value
        new_value = simpledialog.askstring("Edit Row", f"Enter new values for row {self.current_row} (comma-separated):",
                                           initialvalue=', '.join(map(str, value)))

        # Update DataFrame with new value if not None
        if new_value is not None:
            self.df.iloc[self.current_row] = [x.strip() for x in new_value.split(',')]

            # Export DataFrame to CSV in the same folder as txt and png files
            self.df.to_csv(self.csv_file)

            # Update GUI to reflect changes
            self.display_dataframe()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Create and run the VO2_QC application
    vo2_qc = VO2_QC()
    vo2_qc.run()
