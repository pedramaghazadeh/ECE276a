import os
import subprocess

# Set the directory where your PNG frames are stored
data_ind = 21

frames_dir = f"./../dataRGBD/RGB{data_ind}"  # Change this to your actual folder path
output_video = f"{data_ind}.mp4"  # Change this to your desired output filename

# Ensure ffmpeg is installed
try:
    subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except FileNotFoundError:
    print("ffmpeg is not installed. Install it with 'brew install ffmpeg'.")
    exit(1)

# Construct the ffmpeg command
ffmpeg_cmd = [
    "ffmpeg",
    "-framerate", "30",  # Change this to your desired frame rate
    "-i", os.path.join(frames_dir, f"rgb{data_ind}_%d.png"),  # Ensure the filename format matches your frames
    "-c:v", "libx264",
    "-preset", "slow",
    "-crf", "18",  # Adjust quality (lower is better, 18-23 is good)
    "-pix_fmt", "yuv420p",
    output_video
]

# Run the ffmpeg command
subprocess.run(ffmpeg_cmd)

print(f"Video saved as {output_video}")