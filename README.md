# Microstructure quantification of in-situ experiments on nanoporous gold
Code to reproduce analysis from the paper ["Mechanical properties of nanoporous gold subjected to tensile stresses in real-time, sub-microscopic scale"](doi.org/10.1007/s10853-019-03762-8)

Code is in the python_code folder. Example video frames and analysis results are in the sample_data folder. 

Basic analysis steps:
1. Align the frames using cross-correlation. (Other techniques could be used instead).
2. Crop the video frames to the relevant area.
3. Segment the images. (Here I used basic automatic histogram thresholding and morphologoical operations to clean the results.)
4. Perform automatic quantitative measurements on each frame (diameter or length).
