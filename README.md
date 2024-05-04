# VO2 Max Data Quality Checking

This app is designed to aid in the validation of the quality of transcribed VO2 max data from NKI's CBIN AP-CNL.

## Installation

Download the latest version of of the code (*.zip file or pull from git repository), and put it somewhere convenient (e.g. ~/python)

### The project has few dependencies

    - python=3.10
    - pandas=2.2.2
    - pygame=2.5.2
    - matplotlib=3.8.4
    - pip:
        - pydub==0.25.1
        - keyboard==0.13.5

To install the necessary dependencies for this application, you can install them yourself through the command line. Or, you can create a conda environment using the `requirements.yml` file in the project directory.

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Mamba](https://mamba.readthedocs.io/en/latest/installation.html) if you haven't already.

2. Open a terminal and navigate to the directory containing the `requirements.yml` file.

3. Run the following command to create the conda environment:
```bash
conda env create -f requirements.yml
```
4. Activate the newly created environment:
``` bash
conda activate vo2-max-qc
```

## Usage

Before opening the GUI, you will want to structure your directory so that each participant data folder has 1. the .png of the raw transcribed data and 2. the .txt file with the transcriptions (optional: the original image with the raw data from the VO2-max system). Additionally, these should be stored in the folder called 'data', and each participant folder should be named the participant's anonymized ID number. Once this is done, you can open the gui with the code below

``` bash
python qc.py
```
### Importing data
Once running, you'll want to import your data. To do so, press the *Import Data* button and your file registry should appear. Navigate to the folder storing your desired participant's folder (e.g. .../VO2_max_QC/data/PTP_ID_NUM) and press *OK*. You should now see the text transcription and the image in the GUI.

### Navigating the GUI
Once the data's imported, you should simply be able to be able to use the buttons to navigate each row and the *Edit* button to edit a trascription. You can also double click on any row to edit the data. Once an edit is made, it is automatically saved to the edited file.

### Rescoring
If you need to rescore an already edited .csv file, you can simply import from the *edited* directory (e.g. .../VO2_max_QC/edited/PTP_ID_NUM).

The above code will open the gui. You will then
