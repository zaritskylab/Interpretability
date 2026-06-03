# Single Cell Mask Interpreter

This folder contains the single-cell MaskInterpreter workflow for in silico labeling predictions.

The workflow applies MaskInterpreter to single-cell-resolution images in order to generate visual explanations for in silico labeling predictions.

## Workflow Overview

- **Input:** single-cell label-free microscopy images and in silico labeling model predictions.
- **Goal:** identify image regions that are important for preserving the in silico labeling prediction.
- **Output:** single-cell importance masks and visualization outputs.
- **Main use case:** interpreting in silico labeling predictions at single-cell resolution.

## Directory Structure

```text
Single_Cell_Mask_Interpreter/
├── README.md
├── requirements.txt
├── data/
│   └── Nuclear-envelope/
├── models/
│   ├── unet/
│   └── mg/
├── notebooks/
├── src/
└── outputs/
```

The `models/` directory is not tracked by GitHub and should be created after downloading the pretrained models.

## Setup

Create and activate the environment:

```bash
conda create -n single_cell_mask_interpreter python=3.9.15
conda activate single_cell_mask_interpreter
pip install -r requirements.txt
```

## Data and Models

Example data is provided in the repository for the nuclear envelope example.

Pretrained models will be made available through Zenodo.

Zenodo DOI: `TODO`

After downloading, place the model files in the following locations:

```text
Single_Cell_Mask_Interpreter/
├── models/
│   ├── unet/
│   └── mg/
```

## Configuration

Before running the notebooks, copy the example configuration file:

```bash
cp config.example.yaml config.yaml
```

Then edit `config.yaml` so that the paths point to the data, models and outputs directories on your machine or cluster.

The notebooks and scripts should read paths from `config.yaml` instead of relying on the current working directory.

## Running the Demo

After installing the environment and downloading the pretrained models, run:

```bash
jupyter notebook notebooks/inference.ipynb
```

This notebook runs MaskInterpreter on the nuclear envelope single-cell example data.

The demo does not retrain the model and does not overwrite pretrained checkpoints.

## Training and Inference

Additional notebooks are provided under:

```text
notebooks/
```

These include workflows for training and inference with or without context.

Training outputs should be saved under:

```text
outputs/checkpoints/
```

Do not save new training outputs directly into `models/` unless you intentionally want to replace a pretrained checkpoint.

## Relation to CELTIC

This workflow builds on the single-cell in silico labeling framework described in the CELTIC repository:

https://github.com/zaritskylab/CELTIC

For full reproduction or training on additional organelles, follow the CELTIC data preparation instructions and update the local paths and metadata files accordingly.
