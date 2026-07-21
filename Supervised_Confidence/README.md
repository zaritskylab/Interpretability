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

## Setup

Create and activate the environment:

```bash
conda create -n supervised_confidence python=3.10.14
conda activate supervised_confidence
pip install -r requirements.txt
```

## Data and Models

Example data and pretrained models are available through Zenodo.

Zenodo DOI: https://doi.org/10.5281/zenodo.20522083

Download the following archives:

```text
confidence_data-20260603T070348Z-3-001.zip
confidence_data-20260603T070348Z-3-002.zip
confidence_models-20260603T070310Z-3-001.zip
```

After downloading and extracting the archives, arrange the files under:

```text
Supervised_Confidence/
├── data/
│   └── Nuclear-envelope/
├── models/
│   ├── unet/
│   ├── mg/
│   └── confidence/
```

The `variables/` directory contains precomputed confidence predictions and ground-truth evaluation results for the nuclear envelope example. These files are used for reproducing example plots.

## Configuration

Before running the notebooks, copy the example configuration file:

```bash
cp config.example.yaml config.yaml
```

Then edit `config.yaml` so that the paths point to the data, models, outputs, and variables directories on your machine or cluster.

The notebooks and scripts should read paths from `config.yaml` instead of relying on the current working directory.

## Running the Demo

After installing the environment and downloading the example data and models, run:

```bash
jupyter notebook notebooks/inference.ipynb
```

This notebook runs inference with the pretrained confidence model on the nuclear envelope example data.

The demo does not retrain the model and does not overwrite pretrained checkpoints.

## Training and Evaluation

Training and evaluation notebooks are provided under:

```text
notebooks/
```

Training outputs should be saved under:

```text
outputs/checkpoints/
```

Do not save new training outputs directly into `models/` unless you intentionally want to replace a pretrained checkpoint.

## Reproducing Figures

Precomputed variables for the nuclear envelope example are provided under:

```text
variables/
```

Figures are saved under:

```text
outputs/
```

To reproduce example plots, run the relevant plotting notebook under:

```text
notebooks/
```

## Full Data Reproduction

Full reproduction requires downloading the complete microscopy data from the Allen Institute for Cell Science:

https://www.allencell.org/data-downloading.html#sectionLabelFreeTrainingData

After downloading the full data, update the metadata CSV files under `data/` so that they point to your local data location.
