<div align="center" markdown>
<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/262653323-44374612-28aa-4750-81df-c43efd561aa6.png"/>

# MMOCR Inference - Text Detection and Recognition on images

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/mmocr-inference)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/mmocr-inference)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/mmocr-inference.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/mmocr-inference.png)](https://supervise.ly)

</div>

<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/262668367-6392abe9-8176-4c87-8533-115ed537049e.png">

## Overview

ℹ️ The application can be run both on GPU and CPU agents. It will automatically detect if GPU is available and use it in case it is. **Note:** running the app on the CPU agents will be slower.

This application allows you to run the MMOCR Text Detection and Recognition models on images. The application uses the `DBNetpp` detection model and `ABINet` recognition model and can be used for automatic data pre-labeling. The application will create a new project and datasets with the results of the inference, which will include rectangle annotations with text labels.<br>

The resulting project will have:

- Rectangle annotations with name `text`
- Text labels with name `ocr` and recognized text as a value

## Related Apps

- [Object tags editor](https://ecosystem.supervisely.com/apps/object-tags-redactor) - You can use this app for easy and convenient editing of the tags after running the MMOCR Inference app.

## How To Run

To run the app you will need a project with images. The app can be launched from Ecosystem, images project and images dataset.

- [running the app from the Ecosystem](#running-the-app-from-the-ecosystem)
- [running the app from the images project](#running-the-app-from-the-images-project)
- [running the app from the images dataset](#running-the-app-from-the-images-dataset)
- [editing results](#editing-results)

### Running the app from the Ecosystem

**Step 1:** Run the app<br><br>

<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/262659619-a643c84d-1418-456e-9110-ec107dbe4601.png"/><br><br>

**Step 2:** Select a project or a dataset and press the Run button<br><br>

<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/262659634-4f0a1037-4af9-4516-9c53-fad3576b2816.png"/><br><br>

### Running the app from the images project

**Step 1:** Run the app from a context menu of the images project<br><br>

<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/262659643-f9d07c69-864d-4aaf-9331-84322d6df4ef.png"/><br><br>

**Step 2:** Press the Run button<br><br>

### Running the app from the images dataset

**Step 1:** Run the app from a context menu of the images dataset<br><br>

<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/262659651-929f09b6-35e3-4473-961f-8696fa4ba9fc.png"/><br><br>

**Step 2:** Press the Run button<br><br>

### Editing results

After running the app you have two options how to view and edit the results.

## Option 1: Editing tags and annotations in the Supervisely Labeling Tool

You can manually edit tags and annotations in the [Supervisely Labeling Tool](https://ecosystem.supervisely.com/annotation_tools/image-labeling-tool-v1) and add new annotations if needed.

**Step 1:** Select the needed object<br><br>

**Step 2:** Press the edit button in the Tags tab<br><br>

<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/262668435-80cb90e8-cba4-4eff-b59d-62d8a0710df9.png">

## Option 2: Editing tags in the Object tags editor app

You can use the [Object tags editor](https://ecosystem.supervisely.com/apps/object-tags-redactor) app for easy and convenient editing of the tags.<br>

![](https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/262675779-53362426-a306-409f-b764-25cfe70c08f5.gif)

## Acknowledgment

- This app is based on the great work `MMOCR` ([github](https://github.com/open-mmlab/mmocr)). ![GitHub Org's stars](https://img.shields.io/github/stars/open-mmlab/mmocr?style=social)
