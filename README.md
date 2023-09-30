# Habit Tracker 
A simple Python tool for daily and weekly habits tracking and visualizing, using CLI and JSON files. 

Easy usability with python cli.py username feature option
Useful help hints with feature --help for every command

### Features:
  add-habit              add a habit with a daily or weekly frequency.
  change-habit-settings  mark habits as completed or change frequency
  delete-habit           delete a habit from the list
  get-habits             get a status for each of your habits
  monthly-scores         check last month performance: x- success
  save-user              saves user data to a json string in a file in...
  score-charts           shows performance chart for habits - default: daily
  track-habit            update your periodical progress for each habit


### Installation: 
* copy the repository
* run in bash: bash setup.sh
* example data for the user tim in folder data. 
* command get-habits for tim will be called automatically for demonstration. You can repeat it with python cli.py tim get-habits

### Requirements: 

click

jsonpickle

matplotlib

numpy

pandas

prettytabl

python-dateutil

schedule