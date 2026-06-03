# MaskInterpreter Applications for In Silico Labeling

Preprint link will be added upon publication.

This repository accompanies an upcoming research paper from the Zaritsky Lab of Computational Cell Dynamics on confidence estimation and interpretability for in silico labeling predictions.

## Project Description

This repository contains two related applications of MaskInterpreter for in silico labeling microscopy models. Although both projects use MaskInterpreter-based explanations, they answer different questions and should be treated as separate workflows.

### 1. Supervised Confidence

The **Supervised Confidence** project uses MaskInterpreter explanation masks as part of a supervised model for estimating the reliability of in silico labeling predictions.

- **Input:** In silico labeling predictions and their corresponding MaskInterpreter explanation masks.
- **Goal:** Estimate how reliable an in silico labeling prediction is at the patch level.
- **Output:** A confidence score together with evaluation metrics and downstream analyses.
- **Main use case:** Identifying which in silico labeling predictions are reliable enough for downstream biological analysis.

This project is located under:

```text
Supervised_Confidence/
```

### 2. Single Cell Mask Interpreter

The **Single Cell Mask Interpreter** project applies MaskInterpreter to single-cell-resolution in silico labeling predictions.

- **Input:** Single-cell label-free microscopy images and in silico labeling model predictions.
- **Goal:** Generate visual explanations that highlight which regions are important for preserving the in silico labeling prediction.
- **Output:** Single-cell importance masks and visualization outputs.
- **Main use case:** Interpreting in silico labeling predictions at single-cell resolution.

This project is located under:

```text
Single_Cell_Mask_Interpreter/
```

### Relationship between the projects

The two projects are connected by their use of MaskInterpreter, but they are not the same workflow.

The **Single Cell Mask Interpreter** project focuses on generating visual explanations for single-cell in silico labeling predictions. The **Supervised Confidence** project uses in silico labeling predictions and explanation masks as inputs to a supervised model that predicts confidence or expected prediction quality.

Each project has its own environment, configuration, notebooks, data paths, and model files.

<p align="center">
  <img src="images/overview.png" alt="Project overview" width="520"/>
</p>

---

## Repository Structure

```text
Interpretability/
├── README.md
├── LICENSE
├── images/
│   └── overview.png
├── Supervised_Confidence/
│   ├── README.md
│   ├── requirements.txt
│   ├── data/
│   │   └── Nuclear-envelope/
│   ├── models/                  # not tracked; downloaded separately
│   ├── notebooks/
│   ├── src/
│   ├── variables/
│   └── outputs/
└── Single_Cell_Mask_Interpreter/
    ├── README.md
    ├── requirements.txt
    ├── data/
    │   └── Nuclear-envelope/
    ├── models/                  # not tracked; downloaded separately
    ├── notebooks/
    └── src/
```

The repository is organized as two independent project folders:

- **`Supervised_Confidence/`** contains the supervised confidence model, its notebooks, source code, example data structure, precomputed variables, and output figures.
- **`Single_Cell_Mask_Interpreter/`** contains the single-cell MaskInterpreter workflow, including notebooks, source code, and example single-cell data structure.

Large model files and full datasets are not tracked directly in the GitHub repository. They should be downloaded separately and placed in the expected directories described below.

---
## Models, Data & Access

Large data files and trained model checkpoints are not tracked directly in this GitHub repository. Example data and pretrained models should be downloaded separately and placed in the expected project folders.

> **Note:** Example data and pretrained models are available through Zenodo.  
> Zenodo DOI: `TODO: add final Zenodo DOI after publishing the record`

The Zenodo record contains the following archives:

```text
confidence_data-20260603T070348Z-3-001.zip
confidence_data-20260603T070348Z-3-002.zip
confidence_models-20260603T070310Z-3-001.zip
single_cell_models-20260603T070159Z-3-001.zip
```

The `confidence_data` archives contain example data for the **Supervised Confidence** workflow.  
The `confidence_models` archive contains pretrained models for the **Supervised Confidence** workflow.  
The `single_cell_models` archive contains pretrained models for the **Single Cell Mask Interpreter** workflow.

### Supervised Confidence

The **Supervised Confidence** project uses paired label-free microscopy volumes, in silico labeling predictions, MaskInterpreter explanation masks, and ground-truth fluorescence measurements to train and evaluate a supervised confidence model.

Example data and pretrained models for the nuclear envelope example should be organized as follows:

```text
Supervised_Confidence/
├── data/
│   └── Nuclear-envelope/
│       └── ...
├── models/
│   ├── unet/
│   ├── mg/
│   └── confidence/
├── variables/
└── outputs/
```

The `models/` directory is not included in the repository and should be created after downloading the pretrained models.

The `variables/` directory contains precomputed confidence predictions and ground-truth evaluation results for the nuclear envelope example. These files are used for generating the plots provided in `outputs/`.

For full reproduction of the paper results, the full microscopy data should be downloaded from the Allen Institute for Cell Science:

https://www.allencell.org/data-downloading.html#sectionLabelFreeTrainingData

After downloading the full data, update the relevant CSV files under `Supervised_Confidence/data/` so that they point to the local data location on your machine or cluster.

### Single Cell Mask Interpreter

The **Single Cell Mask Interpreter** project uses single-cell-resolution label-free microscopy volumes, cell masks, and fluorescence measurements to generate MaskInterpreter explanation masks for single-cell in silico labeling predictions.

Example nuclear envelope data is provided in the repository. Pretrained models should be downloaded separately and organized as follows:

```text
Single_Cell_Mask_Interpreter/
├── data/
│   └── Nuclear-envelope/
│       └── ...
├── models/
│   ├── unet/
│   └── mg/
└── outputs/
```

The `models/` directory is not included in the repository and should be created after downloading the pretrained models.

This project builds on the single-cell in silico labeling framework described in the CELTIC repository:

https://github.com/zaritskylab/CELTIC

For full reproduction or training on additional organelles, follow the CELTIC data preparation instructions and update the local paths and metadata files accordingly.

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/zaritskylab/Interpretability.git
cd Interpretability
```

Then choose one of the two project workflows below.

### Supervised Confidence

```bash
cd Supervised_Confidence

conda create -n supervised_confidence python=3.10.14
conda activate supervised_confidence

pip install -r requirements.txt
```

After installing the environment:

1. Download `confidence_data-20260603T070348Z-3-001.zip`, `confidence_data-20260603T070348Z-3-002.zip`, and `confidence_models-20260603T070310Z-3-001.zip` from Zenodo.
2. Place the files under the expected `data/` and `models/` directories described above.
3. Open the demonstration notebook:

```bash
jupyter notebook notebooks/inference.ipynb
```

The demonstration notebook runs inference with the pretrained confidence model on the nuclear envelope example data. It does not retrain the model and does not overwrite downloaded checkpoints.

Additional notebooks are provided for training, evaluation, and figure generation. See the local project instructions in `Supervised_Confidence/README.md`.

### Single Cell Mask Interpreter

From the repository root:

```bash
cd Single_Cell_Mask_Interpreter

conda create -n single_cell_mask_interpreter python=3.9.15
conda activate single_cell_mask_interpreter

pip install -r requirements.txt
```

After installing the environment:

1. Download `single_cell_models-20260603T070159Z-3-001.zip` from Zenodo.
2. Place the files under the expected `models/` directory described above.
3. Open the demonstration notebook:

```bash
jupyter notebook notebooks/inference.ipynb
```

The demonstration notebook runs MaskInterpreter on the nuclear envelope single-cell example data. It does not retrain the model and does not overwrite downloaded checkpoints.

Additional notebooks are provided for training and inference with or without context. See the local project instructions in `Single_Cell_Mask_Interpreter/README.md`.

---

## Citation

If you use this repository, please cite the associated paper and repository.

### Repository

```bibtex
@misc{Trustworthy_in_silico_labeling_2026,
  title        = {Trustworthy in silico labeling via semantic visual interpretability of image-to-image translation},
  author       = {Miller, Gad and Ben Nedava, Lion and Zaritsky, Assaf},
  year         = {2026},
  howpublished = {\url{https://github.com/zaritskylab/Interpretability}},
  doi          = {TODO}
}
```

### Paper

```bibtex
@article{Trustworthy_in_silico_labeling_2026,
  title   = {TODO},
  author  = {TODO},
  journal = {Preprint},
  year    = {2026},
  doi     = {TODO}
}
```

## Related Repositories and Credits

This work was carried out in collaboration with Lion Ben Nedava. Related MaskInterpreter code can be found here:

https://github.com/lionben89/cell_generator/tree/MaskInterpreter2.0

The single-cell in silico labeling component builds on the CELTIC framework:

https://github.com/zaritskylab/CELTIC

## Contact

For questions, please contact:

- Gad Miller: `TODO`
- Prof. Assaf Zaritsky: `TODO`

## License

This repository is intended for academic and research use and is licensed under CC BY-NC 4.0. See [LICENSE](LICENSE) for details.
