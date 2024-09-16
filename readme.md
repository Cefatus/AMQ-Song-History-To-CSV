# AMQ History to CSV

[![justforfunnoreally.dev badge](https://img.shields.io/badge/justforfunnoreally-dev-9ff)](https://justforfunnoreally.dev)

AMQ is [Anime Music Quiz](https://animemusicquiz.com/)
This python script is written because my friends want to get a list of songs.
I'm too distracted when I prepare the data manually, so I decided to write a recursive parser instead.

# Input/Output

Input is the json file downloaded from song history in the setting menu.

Output is given in the out directory.

# Using the CSV

The output file is a full dump from JSON to CSV. 
This script runs through every entries from the json file, this includes your statistics and answers in each rounds. 
If you want to hide your score, you should import the csv file from out directory into a spreadsheet editor to make more changes.
