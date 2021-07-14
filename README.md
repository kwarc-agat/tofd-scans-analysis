# TOFD Scans Analysis

Classifying welding samples based on PN-EN ISO 15626. The results of ultrasonic scans are processed in order to find welding imperfections and measure them.

This app is a part of thesis project: "The analysis of the indications evaluation of welding imperfections using TOFD technic"

## Features

- image processing
    - Canny edge detecion
    - morphological transformations
- customize settings for image processing
- imperfections marked on the image
- imperfections size checked with the norm

## Technologies

- Python 3.6
    - OpenCV
    - Tkinter
    - Numpy

## Demo

![](https://github.com/kwarc-agat/tofd-scans-analysis/blob/master/demo_imgs/settings.JPG)
![](https://github.com/kwarc-agat/tofd-scans-analysis/blob/master/demo_imgs/inspected_image.JPG)
![](https://github.com/kwarc-agat/tofd-scans-analysis/blob/master/demo_imgs/show_process.JPG)

## Getting started

```sh
git clone https://github.com/kwarc-agat/skryptowe20.git
```
Make sure that libraries listed above in Technologies are installed in your environment, then run <b>program.py</b>
