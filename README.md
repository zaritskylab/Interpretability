# Confidence Prediction for In-Silico Labeling
[Preprint (TODO)](#)

---

## Project Description

This repository hosts two tightly related but **separable** projects:

- **`interpretability/`** — Patch level confidence model for in silico labeling with detailed analysis pipelines.
- **`single_cell/`** — Single-cell model for in silico labeling prediction and visual explanation generation.  

Each folder has **its own Python environment** and **paths/configs**. Keep them isolated.

In addition, this repository is part of a research paper done by the Zaritsky Lab of Computational Cell Dynamics that is set to be published. This research is done in collaboration with Lion Ben Nedava and his work can be found here: https://github.com/lionben89/cell_generator/tree/MaskInterpreter2.0.

### Brief research & code overview

- **Goal**: Quantify confidence for in silico labeling predictions and provide a tool for for deciding which predictions are reliable for biological analysis.  
- **Significance**: Improves trust and deployment of in silico labeling in biological imaging by telling **where** and **why** a prediction is reliable.  
- **Key features**
  - *3D confidence model* that ingests in silico labeling predictions + explanation masks and regresses a per-cell/per-patch quality target.
  - *Detailed analysis* to understand cell-level or FOV-level mistakes.
  - *Example applications* that can be performed using this method.


<p align="center">
  <img src="images/overview.png" alt="Project overview" width="520"/>
</p>

---
## Models, Data & Access

- **`interpretability/`**  
  - Paired unlabeled→labeled microscopy volumes for in silico labeling (e.g., brightfield → fluorescence).  
  - Trained to produce confidence scores for in silico labeling predictions; can be used in 2D/3D.
  - We provide sample data for the nuclear envelope and suitable models in the "confidence data" and "confidence models" folders here:     https://drive.google.com/drive/u/0/folders/1hph8I6x4LdCaC2cbFjj9emrgGqDD2L98.
  - The data should be downloaded and added to to appropriate folder (interpretability/data/Nuclear-envelope). The folders under "confidence models" (unet, mg, confidence) should be downloaded and added under a new folder named models (interpretability/models).
  - Full data used in this paper can be downloaded from the Allen Institute for Cell Science: https://www.allencell.org/data-downloading.html#sectionLabelFreeTrainingData.
  - If the goal is to replicate results full data should be downloaded and csv files in the data folder should be updated. If the goal is to understand the method we recommend downloading the sample data and using the Jupyter Notebooks to follow the pipeline.
  - "variables" folder includes confidence predictions and ground truth results for the nuclear envelope. These are used for creating the plots that appear in the "outputs" folder.

- **`single_Cell/`**  
  - Paired unlabeled→labeled microscopy volumes for in silico labeling, in the single cell resolution.  
  - Typical sample contains: label-free volume, cell mask and fluorescense volume.
  - Trained to produce importance masks for an organelle in a single cell.
  - We provide sample data for the nuclear envelope as part of the repository. Suitable models can be downloaded from the "single cell models" folder here:     https://drive.google.com/drive/u/0/folders/1hph8I6x4LdCaC2cbFjj9emrgGqDD2L98.
  - The folders under "single cell models" (unet, mg) should be downloaded and added under a new folder named models (single_cell/models).
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
