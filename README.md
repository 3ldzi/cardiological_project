# cardiological_project
This project is designed to automatically analyze hemodynamic data from .par files (e.g., from ICG/ECG studies). The program allows you to: filter data based on signal quality (QI-ICG), select a signal segment for analysis (time or number of beats), calculate descriptive statistics for all parameters, and generate a results table in CSV format.

# project structure
cardiological_project/
│
├── app/
│   ├── main.py               # main program logic
│   ├── file_loader.py        # loading .par files
│   ├── data_description.py   # computing N (beats) and T (duration)
│   ├── filtering.py          # QI-ICG quality filtering
│   ├── statistics.py         # descriptive statistics
│   └── __init__.py
│
├── input/                    # place .par files here (empty in repo)
├── output/                   # generated results (ignored by Git)
│
├── requirements.txt          # project dependencies
├── .gitignore                # ignored files and folders
└── README.md                 # documentation

# Features
✔ Quality Filtering
Rows below a user-defined QI‑ICG threshold are removed.

✔ Segment Selection
The user chooses one of two analysis modes:
Time-based analysis → specify number of seconds
Beat-based analysis → specify number of heartbeats
The program automatically selects the last stable segment of the signal.

✔ Descriptive Statistics
For every numerical parameter, the program computes:
Mean (MN)
Standard deviation (STD)
Median (MED)

✔ Result Export
All results are saved to:
output/results.csv
Including:
- total beats and duration
- beats/duration after filtering
- beats/seconds used for analysis
- descriptive statistics for all parameters

# Installation
Clone the repository:
git clone https://github.com/3ldzi/cardiological_project.git
cd cardiological_project

Install dependencies:
pip install -r requirements.txt

Place your .par files in:
input/

# Running the Program
Run the main script:
python3 app/main.py

The program will ask you to:
Choose analysis mode (time or beats)
Enter the number of seconds or beats
Enter the minimum QI‑ICG quality threshold

After processing, results will appear in:
output/results.csv

# Example Output (simplified)
filename	N_total	T_total	N_filtered	T_filtered	window_seconds	window_beats	HR_MN	HR_STD	HR_MED
test14.par	1403	1721.67	1200	1500.22	30	—	72.4	5.1	72<img width="569" height="72" alt="image" src="https://github.com/user-attachments/assets/9dfb4264-efa2-4fa1-8ba7-47d016f35c5e" />

# Data privacy 
This repository does not contain any medical or patient data.
Users must provide their own .par files locally.

# Contributing
Contributions, suggestions, and improvements are welcome.

Potential future enhancements include:
visualization of HR/CO/SV/MAP trends
HRV analysis
PDF report generation
artifact detection
GUI interface
