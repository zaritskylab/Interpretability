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

The Single-Cell Mask Interpreter workflow is organized as follows:

```text
Single_Cell_Mask_Interpreter/
├── README.md
├── config.example.yaml
├── requirements.txt
├── notebooks/
└── src/
```

- `notebooks/` contains the demonstration, training, and inference workflows.
- `src/` contains reusable code for data loading, model definition, Mask Interpreter execution, and visualization.
- `config.example.yaml` provides a template for specifying the locations of example or full data, pretrained models, and generated outputs.

Single-cell example data and pretrained models are not stored inside the cloned repository. They are downloaded separately and referenced through the configuration file.

## Hardware Requirements

A CUDA-capable NVIDIA GPU is required for practical execution of the Single-Cell Mask Interpreter workflow. Generating importance masks across a full three-dimensional image volume is computationally intensive and is not intended to run on CPU.

## Installation

Create and activate a dedicated Conda environment:

```bash
conda create -n single_cell_mask_interpreter python=3.9.15
conda activate single_cell_mask_interpreter
```

From the `Single_Cell_Mask_Interpreter/` directory, install the required dependencies:

```bash
pip install -r requirements.txt
```

The environment has been installed successfully when Python can import the required packages and detect the available GPU. Exact tested framework and CUDA versions will be documented after the dependency specification is finalized.

## Data and Models

The pretrained models and example data required for the Single-Cell Mask Interpreter demonstration are distributed through the [Mask Interpreter Applications Zenodo record](https://doi.org/10.5281/zenodo.20522083).

The single-cell resources include:

- Nuclear-envelope single-cell example data.
- The pretrained in silico labeling model used by the single-cell workflow.
- The pretrained Mask Interpreter model used to generate single-cell importance masks.

The resources may be extracted to any suitable location on the local machine or computing cluster. They do not need to be placed inside the cloned GitHub repository. Their locations are specified through the workflow configuration file.

The full single-cell datasets are not redistributed through this repository or its companion Zenodo record. Instructions for obtaining and preparing the full data are provided in the [CELTIC repository](https://github.com/zaritskylab/CELTIC).

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
