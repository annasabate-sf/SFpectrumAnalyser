# DIY Spectrometer Analyser
Spectrometer Analyser app using python and opencv based on [https://www.instructables.com/DIY-Low-Cost-Spectrometer/](https://www.instructables.com/DIY-Low-Cost-Spectrometer/). 

## About The Project
The basic concept of a spectrometer is that an "unknown" beam of light is flashed onto an optical element that splits the beam of light based on the wavelengths present in the "unknown" beam of light. Each wavelength is deviated a different amount, therefore by measuring the deviation, one can determine the wavelengths present in the "unknown" beam of light, which could potentially provide more information about the source of the beam of light, even if it originated millions of kilometers away.

In earlier times, scientists used prisms to split the beam of light into its components, and a pivoting eyepiece to measure the angular deviation of each wavelength component. However, more recently, the prism is replaced by a diffraction grating that serves the same purpose as the prism, and the eyepiece is replaced by an electronic photoreceptor array that is connected to a computer. 

## Getting Started

### Prerequisites
* The program was created using **Python3.7**
* OpenCV
* Matplotlib
* numpy
* screeninfo

### Installation
To install the Spectrometer Analyser app, install the required librarires and clone this repository using the following commands:

```
pip install opencv-python
pip install matplotlib
pip install numpy
pip install screeninfo
git clone https://github.com/annasabate-sf/SFpectrumAnalyser.git
```

## Usage
To run the app, open a terminal and navigate to the folder you just cloned and run the following command:
```
python3 SpectrumAnalyser-SF.py
```
Once the app is running you should see a window with the video stream from the photoreceptor.

To make an analysis, here are the steps to follow:
* Press 'n' to upload an image
* Press 'r' to rotate
* Press 's' to select ROI
* Press 'n' to upload a new image
* Press 'q' or ESC to quit
