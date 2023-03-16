import sys

# fist sys arg is the paht to the datbase to load
db_path = sys.argv[1]

import sqlite3

# connect to the database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# read the 'lectures' table
table = c.execute('SELECT * FROM lectures')

mat = [list(row) for row in table]

# audio names are at index 1 of each row
audioFiles = [row[1] for row in mat]

# stitch together the audio files into a single file
# using the 'sox' command
import subprocess

# the output file name
output = 'output.wav'

# the command to run
cmd = f"sox {' '.join(audioFiles)} {output}"

print(cmd)


# transcripts encoded with base64 are at index 2 of each row
import base64

# decode the base64 transcripts
transcripts = [base64.b64decode(row[2]).decode('utf-8') for row in mat]

fileName = sys.argv[1].split('/')[-1].split('.')[0] + '.txt'
# write the transcripts to a file
with open(fileName, 'w') as f:
    f.write("\n".join(transcripts))
