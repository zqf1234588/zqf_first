# 🧠 Comparing the Impact of Analogue versus Digital Control Panels upon Pilot’s Mental Workload

> This project implements a deep learning approach using **Unet++** for automatic segmentation of **optic disc** and **optic cup** from retinal fundus images in the **REFUGE2** dataset. The goal is to support glaucoma diagnosis by extracting accurate anatomical structures.

---

## 📌 Overview

We leverage the **Unet++** architecture, built on top of PyTorch, to segment retinal images. The project covers the full pipeline from data preprocessing, model training/testing, to result visualization and performance evaluation.

---

## 🎯 Features

- ✅ Preprocessing of REFUGE2 dataset (images + masks)
- ✅ Unet++ model implementation for segmentation
- ✅ Training and testing with performance logging
- ✅ Visualization of predictions vs ground truth
- ✅ Evaluation using standard segmentation metrics

---

## 📁 Project Structure

 ```python 
.
├── data/                     # Dataset (REFUGE2)
│   ├── images/
│   └── masks/
├── models/                   # Unet++ architecture
├── utils/                    # Data loading and preprocessing tools
├── train.py                  # Training script
├── test.py                   # Testing script
├── visualize.py              # Visualize predictions
├── evaluate.py               # Evaluation metrics
└── README.md
```
## Getting Started

### Setup Environment


### Prepare Dataset
Organize the REFUGE2 dataset under the ./data directory:

### Train the Model

### Run Inference and Visualize Results

## Evaluation Metrics
- Dice Coefficient
- Intersection over Union (IoU)
- Precision
- Pixel-wise Accuracy

## Example Visualization
![66.png…]()














