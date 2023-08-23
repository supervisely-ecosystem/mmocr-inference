<div align="center" markdown>
<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/262653323-44374612-28aa-4750-81df-c43efd561aa6.png"/>

# MMOCR Inference - Text Detection and Recognition on images

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/PLACEHOLDER-FOR-APP-PATH)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/PLACEHOLDER-FOR-APP-PATH)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/PLACEHOLDER-FOR-APP-PATH.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/PLACEHOLDER-FOR-APP-PATH.png)](https://supervise.ly)

</div>

## Overview

ℹ️ The application can be run both on GPU and CPU agents. It will automatically detect if GPU is available and use it in case it is. **Note:** running the app on the CPU agents will be slower.

This application allows you to run the MMOCR Text Detection and Recognition models on images. The application uses the `DBNetpp` detection model and `ABINet` recognition model. The application will create a new project and datasets with the results of the inference, which will include rectangle annotations with text labels.

## How To Run

To run the app you will need a project with images. The app can be launched from Ecosystem, images project and images dataset.

- [running the app from the Ecosystem](#running-the-app-from-the-ecosystem)
- [running the app from the images project](#running-the-app-from-the-images-project)
- [running the app from the images dataset](#running-the-app-from-the-images-dataset)

### Running the app from the Ecosystem

**Step 1:** Run the app<br><br>

<img src="placeholder for screenshot"/><br><br>

**Step 2:** Select a project or a dataset and press the Run button<br><br>

<img src="placeholder for screenshot"/><br><br>

### Running the app from the images project

**Step 1:** Run the app from a context menu of the images project<br><br>

<img src="placeholder for screenshot"/><br><br>

**Step 2:** Press the Run button<br><br>

<img src="placeholder for screenshot"/><br><br>

### Running the app from the images dataset

**Step 1:** Run the app from a context menu of the images dataset<br><br>

<img src="placeholder for screenshot"/><br><br>

**Step 2:** Press the Run button<br><br>

<img src="placeholder for screenshot"/><br><br>

## Demo

Example of running the app from Ecosystem with results:

![](placeholder for gif)
