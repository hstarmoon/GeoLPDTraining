import sys
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(prog='plotTrainLoss')
parser.add_argument('--data_dir', type=str, default=r'D:\RD\Project\GeoLPDTraining-master\tools\train.log', required=False)

args = parser.parse_args()
lines = []
# sys.argv[1]
file = args.data_dir
file_path = os.path.dirname(file)
file_basename = os.path.basename(file)
min_loss = 10000
epoch_with_min_loss = 0

with open(file, 'r') as train_file:
    all_lines = train_file.readlines()


for line in all_lines:
    if "avg" in line:
        epoch = line.split(':')
        epoch = int(epoch[0])
        if epoch % 1000 == 0:
            lines.append(line)
            a = 0

iterations = []
avg_loss = []

print('Retrieving data and plotting training loss graph...')
for i in range(len(lines)):
    lineParts = lines[i].split(',')
    iteration_now = int(lineParts[0].split(':')[0])
    if iteration_now % 1000 == 0:
        now_loss = float(lineParts[1].split()[0])
        iterations.append(int(lineParts[0].split(':')[0]))
        avg_loss.append(now_loss)
        if now_loss < min_loss:
            min_loss = now_loss
            epoch_with_min_loss = iteration_now
            a= 0

fig = plt.figure()
for i in range(0, len(lines)):

    # new_ticks = np.linspace(-1, 2, 5)
    # plt.yticks(new_ticks)

    plt.plot(iterations[i:i+2], avg_loss[i:i+2], 'r.-')

result_name = "{}\{}.png".format(file_path, file_basename[:-4])
plt.xlabel('Batch Number')
plt.ylabel('Avg Loss')
fig.savefig(result_name, dpi=1000)
print("min_loss: " + str(min_loss))
print("epoch: " + str(epoch_with_min_loss))

print('Done! Plot saved as training_loss_plot.png')