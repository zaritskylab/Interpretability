# Supervised Confidence

This folder contains the supervised confidence model workflow for in silico labeling predictions.

The model uses in silico labeling predictions together with MaskInterpreter explanation masks to estimate prediction reliability. The output is a confidence score that can be used to identify predictions that are reliable enough for downstream biological analysis.

## Workflow Overview

- **Input:** in silico labeling predictions and corresponding MaskInterpreter explanation masks.
- **Target:** prediction quality measured against fluorescence ground truth.
- **Output:** confidence score and evaluation metrics.
- **Main use case:** filtering or prioritizing in silico labeling predictions for biological analysis.

## Directory Structure

```text
Supervised_Confidence/
├── README.md
├── requirements.txt
├── data/
│   └── Nuclear-envelope/
├── models/
│   ├── unet/
│   ├── mg/
│   └── confidence/
├── notebooks/
├── src/
├── variables/
└── outputs/
```

The `models/` directory is not tracked by GitHub and should be created after downloading the pretrained models.

## Setup

Create and activate the environment:

```bash
conda create -n supervised_confidence python=3.10.14
conda activate supervised_confidence
pip install -r requirements.txt
```

## Data and Models

Example data and pretrained models will be made available through Zenodo.

Zenodo DOI: `TODO`

After downloading, place the files in the following locations:

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
