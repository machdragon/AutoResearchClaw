# Improving Remote Sensing Scene Classification with Multi-Size Training, Triplet Loss, and Dropout Without Inference Overhead

## Cite_Key
zhang2020training

## Problem
Many remote sensing scene classification methods boost accuracy by adding modules that increase model size and computational cost at inference. There is a need for training-time strategies that improve classification accuracy without adding parameters or overhead during deployment.

## Method
Use ResNet-18 as a baseline CNN and modify only the training procedure: (1) Train with multi-size images to improve scale robustness. (2) Add a training-only branch supervised by triplet loss to encourage better metric structure in the embedding space. (3) Insert dropout between the feature extractor and classifier to reduce overfitting. These components are active only during training and are removed or inactive during inference, keeping the deployed network identical to the baseline in size and complexity.

## Data
Three remote sensing scene classification datasets: AID, NWPU-RESISC45, and OPTIMAL. OPTIMAL is further used for detailed ablation studies of the proposed modules.

## Metrics
Primary metric: Overall classification accuracy on test sets. Ablation metrics: change in overall accuracy (percentage points) on OPTIMAL when adding each module individually and in combination.

## Findings
1) The proposed ResNet-18 model with multi-size training, triplet-loss branch, and dropout outperforms many existing scene classification algorithms on AID, NWPU-RESISC45, and OPTIMAL, despite having no additional parameters at inference. 2) On OPTIMAL, individual contributions to overall accuracy are: +0.53% from dropout, +0.38% from triplet loss, and +0.70% from multi-size training. 3) Combining all three modules yields a total accuracy improvement of 1.61% over the baseline, indicating complementary benefits. 4) The approach demonstrates that careful training-time design can significantly enhance performance without increasing inference-time model size or complexity.

## Limitations
1) Study is limited to a single backbone (ResNet-18); generalization of the training strategy to larger or more modern architectures is not empirically validated in the abstract. 2) Reported gains, while consistent, are modest in absolute terms and may depend on dataset characteristics (e.g., scene diversity, scale variation). 3) Computational training cost may increase due to multi-size inputs and additional triplet-loss branch, which is not quantified. 4) Robustness to domain shifts and real-world deployment conditions (e.g., varying sensors or atmospheric effects) is not addressed.

## Citation
Zhang, J., Lu, C., Wang, J., Yue, X.-G., Lim, S.-J., Al-Makhadmeh, Z., & Tolba, A. (2020). Training Convolutional Neural Networks with Multi-Size Images and Triplet Loss for Remote Sensing Scene Classification. Sensors. https://doi.org/10.3390/s20041188
