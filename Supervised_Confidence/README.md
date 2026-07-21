# Supervised Confidence

This directory contains the code and resources for training, evaluating, and applying the supervised confidence model to in silico labeling predictions.

The model receives an in silico labeling prediction and its corresponding Mask Interpreter-derived importance mask as inputs. It estimates the prediction error relative to the fluorescence ground truth, with confidence defined as one minus the predicted error. The resulting confidence score can be used to identify predictions that may be unsuitable for downstream biological analysis.

## Workflow Overview

* **Inputs:** An in silico labeling prediction and its corresponding importance mask.
* **Training target:** Patch-level in silico labeling error, defined from the Pearson correlation between the prediction and fluorescence ground truth.
* **Output:** A predicted error score.
* **Primary use:** Estimating the reliability of in silico labeling predictions before downstream analysis.

For an overview of both applications, return to the [main repository README](../README.md).

## Directory Structure

The supervised confidence workflow is organized as follows:

```text
Supervised_Confidence/
├── README.md
├── config.example.yaml
├── requirements.txt
├── notebooks/
├── src/
└── outputs/
```

* `notebooks/` contains the demonstration, training, evaluation, and analysis notebooks.
* `src/` contains reusable code for data loading, model definition, training, inference, and evaluation.
* `config.example.yaml` provides a template for specifying the locations of data, pretrained models, precomputed results, and generated outputs.
* `outputs/` is used for generated checkpoints, predictions, figures, and other workflow outputs.

Microscopy data, pretrained models, and precomputed result arrays are not intended to be stored inside the cloned repository. They are downloaded separately and referenced through the configuration file.

## Hardware Requirements

A CUDA-capable NVIDIA GPU is required for practical execution of the supervised confidence workflow. Model inference and training are computationally intensive and are not intended to run on CPU.

## Installation

Create and activate a dedicated Conda environment:

```bash
conda create -n supervised_confidence python=3.10.14
conda activate supervised_confidence
```

From the `Supervised_Confidence/` directory, install the required dependencies:

```bash
pip install -r requirements.txt
```

The environment has been installed successfully when Python can import the required packages and detect the available GPU. Exact tested framework and CUDA versions will be documented after the dependency specification is finalized.

## Data and Models

The supervised confidence demonstration requires resources from two Zenodo records.

### Shared In Silico Labeling and Mask Interpreter Resources

Download the shared resources from the [original Mask Interpreter Zenodo record](https://doi.org/10.5281/zenodo.18590674). These include:

* Pretrained in silico labeling models.
* Pretrained field-of-view Mask Interpreter models.
* Nuclear-envelope field-of-view example data.
* Train/test lists for the full datasets.

### Supervised Confidence Resources

Download the application-specific resources from the [Mask Interpreter Applications Zenodo record](https://doi.org/10.5281/zenodo.20522083). These include:

* Pretrained supervised confidence models.
* Precomputed prediction and error arrays used for evaluation and figure reproduction.

The resources may be extracted to any suitable location on the local machine or computing cluster. They do not need to be placed inside the cloned GitHub repository. Their locations are specified through the workflow configuration file.

## Configuration

Before running the notebooks, create a local configuration file from the provided template:

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` so that each path points to the appropriate location on your machine or computing cluster:

* `data_dir`: Input microscopy data.
* `model_dir`: Pretrained in silico labeling, Mask Interpreter, and supervised confidence models.
* `variables_dir`: Precomputed supervised-confidence results used for evaluation and figure reproduction.
* `output_dir`: Generated predictions, checkpoints, figures, and other outputs.
* `organelle`: Organelle used by the workflow.

The code repository, input data, pretrained models, precomputed results, and generated outputs may all be stored in separate filesystem locations. The downloaded resources do not need to be moved into the cloned GitHub repository.

`config.yaml` is machine-specific and should not be committed to GitHub.

## Running the Demonstration

Before running the demonstration, confirm that:

- The supervised confidence environment is active.
- A CUDA-capable GPU is available.
- The required resources have been downloaded.
- All paths in `config.yaml` point to the correct locations.

Start Jupyter from the `Supervised_Confidence/` directory:

```bash
jupyter notebook
```

Then open the [supervised confidence inference notebook](notebooks/inference.ipynb) and run all cells from a clean kernel.

The notebook applies the pretrained supervised confidence model to the Nuclear-envelope example data and produces a confidence map over a Field of view image. It does not retrain the model or overwrite the pretrained checkpoints.

## Training and Evaluation

The [training and evaluation notebook](notebooks/train_eval.ipynb) contains the workflow used to train and evaluate the supervised confidence model on the full datasets.

This notebook is not required for running the pretrained demonstration. Before using it, confirm that:

- The full microscopy data and corresponding split files are available.
- The required in silico labeling and Mask Interpreter models have been downloaded.
- The paths in `config.yaml` point to the full data, pretrained models, precomputed results, and output locations.
- A CUDA-capable GPU is available.

Training checkpoints, generated predictions, and evaluation outputs should be written to the configured `output_dir`. Do not save new checkpoints directly into the pretrained `model_dir` unless intentionally replacing an existing model.

Full model training is computationally intensive and is intended for users reproducing or extending the complete workflow.

## Reproducing Figures

The [plotting notebook](notebooks/plotting.ipynb) uses precomputed supervised-confidence results to generate the corresponding evaluation plots.

Before running the notebook, confirm that:

- `variables_dir` in `config.yaml` points to the downloaded supervised-confidence result arrays.
- `output_dir` points to a writable location for generated figures.
- The required result files are available for the organelles or analyses being reproduced.

Start Jupyter from the `Supervised_Confidence/` directory:

```bash
jupyter notebook
```

Then open `notebooks/plotting.ipynb` and run the relevant sections.

Generated figures are saved under the configured `output_dir`. Reproducing the full manuscript analyses requires the complete precomputed results, whereas the Nuclear-envelope example resources support only the corresponding demonstration.

## Full Data Reproduction

Full reproduction requires downloading the complete microscopy data from the Allen Institute for Cell Science:

https://www.allencell.org/data-downloading.html#sectionLabelFreeTrainingData

After downloading the full data, update the metadata CSV files under `data/` so that they point to your local data location.
