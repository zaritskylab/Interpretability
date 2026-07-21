# Single-Cell Mask Interpreter

This directory contains the code and resources for applying Mask Interpreter to single-cell in silico labeling predictions.

The workflow generates an importance mask for each single-cell prediction, identifying regions of the label-free input whose preservation is important for maintaining the corresponding in silico labeling output. These masks enable explanation signatures to be examined at single-cell resolution.

## Workflow Overview

- **Inputs:** A single-cell label-free microscopy image and its corresponding in silico labeling prediction.
- **Goal:** Identify input-image regions that are important for preserving the in silico labeling prediction.
- **Output:** A single-cell importance mask and corresponding visualization outputs.
- **Primary use:** Interpreting and comparing in silico labeling predictions at single-cell resolution.

For an overview of both applications, return to the [main repository README](../README.md).

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

Pretrained models are available through Zenodo.

Zenodo DOI: https://doi.org/10.5281/zenodo.20522083

Download the following archive:

```text
single_cell_models-20260603T070159Z-3-001.zip
```

After downloading and extracting the archive, arrange the model files under:

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
