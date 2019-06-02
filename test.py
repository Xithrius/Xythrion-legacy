from rehasher.containers.QOL.pathing import path
import os
import datetime

for (dirpath, dirnames, filenames) in os.walk(path('repository', 'memes')):
    print(dirnames + filenames)


print()

# to timestamp
timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()))
print("timestamp =", timestamp)

# from timestamp
dt_object = datetime.datetime.fromtimestamp(timestamp)
print("dt_object =", dt_object)
