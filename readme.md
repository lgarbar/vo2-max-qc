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
   ```

## Usage

To run the application:

### Command-line options:

- `--verbose`: Show all rows/basenames (default behavior is to only show rows with bad_vals=True)

### Navigation:

- Use the 'Previous' and 'Next' buttons or left/right arrow keys to move between entries
- Use the 'Select' button to choose a specific entry by basename

### Editing:

- Double-click on a cell in the 'Value' column to edit directly in the table
- Use the 'Edit' button to open a dialog box for editing the selected cell
- Press Enter or click outside the cell to confirm edits

### Saving:

Edits are automatically saved to a new CSV file with '_edited' appended to the original filename.

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