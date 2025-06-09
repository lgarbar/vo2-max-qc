# Data Editor GUI

## Installation

### Prerequisites

- Python 3.7 or higher
- Conda package manager

## Setting up the environment

1. Ensure you have Anaconda or Miniconda installed.
2. Clone this repository:
   ```
   git clone ##Update later
   cd vo2-max-qc
   ```
3. Create the conda environment from the provided YAML file:
   ```
   conda env create -f req.yml
   ```
4. Activate the environment:
   ```
   conda activate vo2-max-qc
   ```

You're now ready to run the application!

## Usage

To run the application:

### Command-line options:

- `--verbose`: Show all rows/basenames (default behavior is to only show rows with bad_vals=True)
- `--show-all`: Show all rows including those that have been viewed

### File Selection:

When you start the application, you will be prompted to:
1. Select a CSV file containing your data
2. Select a directory containing the corresponding image files

### Navigation:

- Use the 'Previous' and 'Next' buttons or left/right arrow keys to move between entries
- Use the 'Select' button to choose a specific entry by basename
- Use up/down arrow keys to navigate between cells in the table

### Editing:

- Double-click on a cell in the 'Value' column to edit directly in the table
- Use the 'Edit' button to open a dialog box for editing the selected cell
- Press Enter or click outside the cell to confirm edits
- Edits are automatically tracked with your initials and marked as edited

### Progress Tracking:

- A progress bar at the top of the window shows your progress through the dataset
- The progress bar changes color from red to yellow to green as you progress
- Files are automatically marked as viewed when you load them

### Saving:

Edits are automatically saved to a new CSV file with '_edited' appended to the original filename. The edited file includes additional columns:
- `edited`: Boolean flag indicating if the row has been edited
- `editor`: Initials of the person who made the edits
- `viewed`: Boolean flag indicating if the row has been viewed

## Customization

Before running the script, make sure to update the following variables in the `qc_pyqt5.py` file:

- `test_fpath`: Path to your input CSV file
- `image_dirs`: Path to the directory containing your image files

## Troubleshooting

If you encounter any issues:

1. Ensure all prerequisites are installed correctly
2. Check console output for error messages
3. Verify that the input CSV file and image directory paths are correct

For further assistance, please open an issue on the GitHub repository.