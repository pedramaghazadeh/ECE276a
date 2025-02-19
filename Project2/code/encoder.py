import numpy as np
import matplotlib.pyplot as plt

dataset = 20

def distance_right_encoder(counts):
    return np.cumsum((counts[0, :] + counts[2, :]) / 2 * 0.0022)

def distance_left_encoder(counts):
    return np.cumsum((counts[1, :] + counts[3, :]) / 2 * 0.0022)


with np.load("../data/Encoders%d.npz"%dataset) as data:
    print(data)
    encoder_counts = data["counts"] # 4 x n encoder counts
    encoder_stamps = data["time_stamps"] # encoder time stamps

print(encoder_counts)
print(encoder_stamps)

print(distance_right_encoder(encoder_counts))

plt.plot(distance_right_encoder(encoder_counts), distance_left_encoder(encoder_counts))
plt.show()