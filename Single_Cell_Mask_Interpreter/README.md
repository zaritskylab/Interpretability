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

Register the environment as a Jupyter kernel:

```bash
python -m ipykernel install --user --name single_cell_mask_interpreter --display-name "Python (single_cell_mask_interpreter)"
```

The workflow was tested with Python 3.9.15, PyTorch 2.5.1, and torchvision 0.20.1 on an NVIDIA GeForce RTX 4090. The environment has been installed successfully when the required packages import correctly and PyTorch detects the available GPU.

## Data and Models

Download `Single_Cell_Mask_Interpreter.zip` from the [Mask Interpreter Applications Zenodo record](https://doi.org/10.5281/zenodo.20522083). The archive contains the pretrained models and example data required for the Single-Cell Mask Interpreter demonstration.

The resources may be extracted to any suitable location on the local machine or computing cluster. They do not need to be placed inside the cloned GitHub repository. Their locations are specified through the workflow configuration file.

After extracting the archive, set `data_dir` to the included `example_data/` directory and `model_dir` to the included `models/` directory. Preserve the internal folder structure and filenames provided in the archive.

The full single-cell datasets are not redistributed through this repository or its companion Zenodo record. Instructions for obtaining and preparing the full data are provided in the [CELTIC repository](https://github.com/zaritskylab/CELTIC).

## Configuration

Before running the notebooks, create a local configuration file from the provided template:

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` so that each path points to the appropriate location on your machine or computing cluster:

- `data_dir`: Single-cell example data or a prepared full dataset.
- `model_dir`: Pretrained in silico labeling and Mask Interpreter models.
- `output_dir`: Generated importance masks, figures, checkpoints, and other outputs.
- `organelle`: Organelle used by the workflow.

The code repository, input data, pretrained models, and generated outputs may all be stored in separate filesystem locations. The downloaded resources do not need to be moved into the cloned GitHub repository.

`output_dir` does not need to be located inside `Single_Cell_Mask_Interpreter/`, but it must point to an existing writable location.

`config.yaml` is machine-specific and should not be committed to GitHub.

## Running the Demonstration

Before running the demonstration, confirm that:

- The Single-Cell Mask Interpreter environment is active.
- A CUDA-capable GPU is available.
- The required example data and pretrained models have been downloaded.
- All paths in `config.yaml` point to the correct locations.

Start Jupyter from the `Single_Cell_Mask_Interpreter/` directory:

```bash
jupyter notebook
```

Then open the [single-cell inference notebook](notebooks/inference_no_context.ipynb) and run all cells from a clean kernel.

The notebook applies the pretrained in silico labeling and Mask Interpreter models to the Nuclear-envelope single-cell example data and generates the corresponding importance mask and visualization outputs. It does not retrain the models or overwrite the pretrained checkpoints.

On an NVIDIA GeForce RTX 4090, the provided Nuclear-envelope demonstration completed in under one minute. Runtime may vary depending on GPU hardware and storage performance.

## Training

The [single-cell Mask Interpreter training notebook](notebooks/train_no_context.ipynb) contains the workflow used to train Mask Interpreter without cellular context.

This notebook is not required for running the pretrained demonstration. Before using it, confirm that:

- The full prepared single-cell dataset is available.
- The pretrained in silico labeling model is available.
- The paths in `config.yaml` point to the full data, pretrained models, and output locations.
- A CUDA-capable GPU is available.

The notebook trains a new Mask Interpreter model for single-cell in silico labeling predictions. Generated checkpoints and training outputs should be written to the configured `output_dir`. Do not save new checkpoints directly into the downloaded pretrained `model_dir` unless intentionally replacing an existing model.

Full training is computationally intensive and is intended for users reproducing or extending the workflow.

## Relation to CELTIC

This workflow builds on the single-cell in silico labeling framework described in the CELTIC repository:

https://github.com/zaritskylab/CELTIC

For full reproduction or training on additional organelles, follow the CELTIC data preparation instructions and update the local paths and metadata files accordingly.
