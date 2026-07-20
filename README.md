# Mask Interpreter Applications for In Silico Labeling

This repository accompanies research from the [Zaritsky Lab of Computational Cell Dynamics](https://www.assafzaritsky.com/) on interpretability and confidence estimation for in silico labeling predictions. It provides two complementary applications of Mask Interpreter: a supervised confidence model that estimates patch-level in silico labeling performance using the predicted fluorescence image and its corresponding importance mask, and a single-cell workflow that generates importance masks and explanation signatures for single-cell in silico labeling predictions.

Preprint link will be added upon publication.

## Project Description

The two applications address different questions and are provided as independent workflows, each with dedicated code, configuration, environment, and documentation.


### Supervised Confidence

The supervised confidence workflow estimates patch-level in silico labeling performance from two inputs: the in silico labeling prediction and its corresponding importance mask. A 3D regression model predicts the in silico labeling error, which is converted into a confidence score for identifying predictions that may be unsuitable for downstream biological analysis.

![Supervised confidence workflow](images/overview.png)

[View the Supervised Confidence documentation](Supervised_Confidence/README.md)

### Single-Cell Mask Interpreter

The Single-Cell Mask Interpreter workflow applies Mask Interpreter to single-cell in silico labeling predictions. It generates importance masks that identify image regions important for preserving each prediction, enabling explanation signatures to be examined at single-cell resolution.

![Single-cell Mask Interpreter workflow](images/single_cell_overview.png)

[View the Single-Cell Mask Interpreter documentation](Single_Cell_Mask_Interpreter/README.md)

---

## Repository Structure

```text
MaskInterpreter-Applications/
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
> Zenodo DOI: https://doi.org/10.5281/zenodo.20522083

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
git clone https://github.com/zaritskylab/MaskInterpreter-Applications.git
cd MaskInterpreter-Applications
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
  howpublished = {\url{https://github.com/zaritskylab/MaskInterpreter-Applications}},
  doi          = {10.5281/zenodo.20522083}
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

https://github.com/zaritskylab/MaskInterpreter

The single-cell in silico labeling component builds on the CELTIC framework:

https://github.com/zaritskylab/CELTIC

## Contact

For questions, please contact:

- Gad Miller: gadmicha@post.bgu.ac.il
- Lion Ben Nedava: lionben89@gmail.com
- Prof. Assaf Zaritsky: assafzar@gmail.com

## License

This repository is intended for academic and research use and is licensed under CC BY-NC 4.0. See [LICENSE](LICENSE) for details.
