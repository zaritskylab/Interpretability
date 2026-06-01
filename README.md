# MaskInterpreter Applications for In Silico Labeling

[Preprint (TODO)](#)

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
│   ├── requirements.txt
│   ├── data/
│   │   └── Nuclear-envelope/
│   ├── models/                  # not tracked; downloaded separately
│   ├── notebooks/
│   ├── src/
│   ├── variables/
│   └── outputs/
└── Single_Cell_Mask_Interpreter/
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

- **`Supervised_Confidence/`**  
  - Paired unlabeled→labeled microscopy volumes for in silico labeling (e.g., brightfield → fluorescence).  
  - Trained to produce confidence scores for in silico labeling predictions; can be used in 2D/3D.
  - We provide sample data for the nuclear envelope and suitable models in the "confidence data" and "confidence models" folders here:     https://drive.google.com/drive/u/0/folders/1hph8I6x4LdCaC2cbFjj9emrgGqDD2L98.
  - The data should be downloaded and added to to appropriate folder (Supervised_Confidence/data/Nuclear-envelope). The folders under "confidence models" (unet, mg, confidence) should be downloaded and added under a new folder named models (Supervised_Confidence/models).
  - Full data used in this paper can be downloaded from the Allen Institute for Cell Science: https://www.allencell.org/data-downloading.html#sectionLabelFreeTrainingData.
  - If the goal is to replicate results full data should be downloaded and csv files in the data folder should be updated. If the goal is to understand the method we recommend downloading the sample data and using the Jupyter Notebooks to follow the pipeline.
  - "variables" folder includes confidence predictions and ground truth results for the nuclear envelope. These are used for creating the plots that appear in the "outputs" folder.

- **`Single_Cell_Mask_Interpreter/`**  
  - Paired unlabeled→labeled microscopy volumes for in silico labeling, in the single cell resolution.  
  - Typical sample contains: label-free volume, cell mask and fluorescense volume.
  - Trained to produce importance masks for an organelle in a single cell.
  - We provide sample data for the nuclear envelope as part of the repository. Suitable models can be downloaded from the "single cell models" folder here:     https://drive.google.com/drive/u/0/folders/1hph8I6x4LdCaC2cbFjj9emrgGqDD2L98.
  - The folders under "single cell models" (unet, mg) should be downloaded and added under a new folder named models (Single_Cell_Mask_Interpreter/models).
  - This work is based on the work of Nitsan Elmalam. Further training instructions, examples and access to full data are well documented here: https://github.com/zaritskylab/CELTIC/tree/main.
  - If the goal is to replicate results full data should be downloaded and csv files in the data folder should be updated. If the goal is to understand the method we recommend using the Jupyter Notebooks to follow the pipeline.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/zaritskylab/Interpretability
cd Interpretability

# --- Confidence model ---
cd interpretability
conda create -n confidence python=3.10.14
conda activate confidence
pip install -r requirements.txt

# --- Single-cell model ---
cd ../single_cell
conda create -n single_cell python=3.9.15
conda activate single_cell
pip install -r requirements.txt
```

After downloading sample data and models, cloning the repository and installing the packages, you should be able to run the pipeline on the sample data.

---

## Citation & Credit (TODO)

If you use this **code** or **data**, please **cite** the associated paper and this repository.

**BibTeX (repo):**
```bibtex
@misc{isl_confidence_repo,
  title        = {ISL-Confidence: Single-Cell Confidence & Interpretability for In-Silico Labeling},
  author       = {Your Name and Collaborators},
  year         = {2025},
  howpublished = {\url{https://github.com/<org>/<repo>}}
}
```

**BibTeX (paper/preprint placeholder):**
```bibtex
@article{isl_confidence_paper,
  title   = {Quantifying Uncertainty in In-Silico Labeling via Single-Cell Confidence and Mask-Based Interpretability},
  author  = {Your Name and Collaborators},
  journal = {Preprint},
  year    = {2025}
}
```

---

**License**  
This repository (data, documentation, and figures) is intended for academic and research use, and is licensed under CC BY-NC 4.0. See [License](LICENSE) for details.
