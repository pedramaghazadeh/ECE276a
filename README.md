You can find the scripts needed for both parts of the project in part1 and part2 jupyter notebooks. The required packages are mentioned in requirements.txt (nothing apart from the essentials). 

For each part, you can select the dataset number and the path to the folder containing dataset based on the current working directory printed after running the first cell. After ensuring that the data is loaded correctly, simply run all cells consequitively and the results will show up.

For the test sets panoramic images, you would need to use part 1 only as it uses the optimized quaternion trajectories to determine the rotation. For all other images, this is done using the VICON dataset in the part2 but you can use the part 1 to generate panoramic images from quaternions too.