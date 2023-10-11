# JIRA Project Burn Down Checker
A simple tool to check if the current rate of work will be completed by a target date.
Applicable for longer running projects

## Steps to use
1. Download CSV from JIRA (the following columns: Issue key,Issue id,Parent id,Status,Updated,Resolution)
2. Install the requirements `pip3 install -r requirements.txt`
3. Run the python script `python3 create_burndown.py /path/to/input.csv --target 2024-01-15 --save`
   1. The `--save` command save the file to the input folder
   2. The `--target YYYY-MM-DD` command is where you put the target date of the project

This currently produces a burn down based upon tickets closed, it doesn't take into account size. 

It also assumes that the number of tickets has already been roughly created - i.e. there isn't going to be a material increase in total number of tickets on the project

=======

### Good use 
Alongside discussions with Product and Engineering using this to sense check whether any expectations that have been set are realistic or not.

### Bad use
Making this the forefront of your discussion with engineering and using it to apply pressure to delivery.