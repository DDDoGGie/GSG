# A masked generative graph representation learning framework empowering precise spatial domain identification
![GitHub Repo stars](https://img.shields.io/github/stars/keaml-Guan/GSG) &nbsp;&nbsp; ![GitHub watchers](https://img.shields.io/github/watchers/keaml-Guan/GSG) &nbsp;&nbsp; ![GitHub](https://img.shields.io/github/license/keaml-Guan/GSG)
#
![](https://github.com/keaml-Guan/GSG/blob/main/figures/Fig1_11_reduce.jpg)
<br>
## ✨ Overview

Recent advances in spatial transcriptomics (ST) have opened new avenues for preserving spatial information while measuring gene expression. Yet, the challenge of seamlessly integrating this data into accurate and transferable representation remains. Here, we introduce a generative self-supervised graph (GSG) learning framework to achieve an effective joint embedding of location and gene expression within ST data. Our approach surpasses existing methods in identifying spatial domains within the human dorsolateral prefrontal cortex. Moreover, it can offer reliable analyses across various techniques, including Stereo-seq, Slide-seq, and seqFISH, irrespective of spatial resolution. Furthermore, GSG addresses dropout defects, enhancing gene expression by smoothing spatial patterns, extracting critical features, reducing batch effects, and enabling the integration of disparate datasets. Additionally, we performed spatial transcriptomic analysis on fetal human hearts, and applied GSG to extract biological insights. These experiments highlight GSG's accuracy in identifying spatial domains, uncovering specific APCDD1 expression in fetal endocardium, and implicating its role in congenital heart disease. Our results showcase GSG's superiority and underscore its valuable contributions to advancing spatial-omics analysis.


## 🛠️ Installation

> [!NOTE]
> **!!! The recommended operating system is Ubuntu 18.04 LTS.** Some packages may not download correctly on Windows.
### Use python virutal environment with conda
```sh
conda create -n gsg python=3.8
conda activate gsg
# Need install cudnn based on your CUDA version.Refer to https://developer.nvidia.com/cudnn-archive
# conda install cudnn[=version]
```
### Install GSG
Install GSG and dgl(for gpu) from PyPi:
```sh
pip install GSG==0.5.8
pip install dgl-cu110 -f https://data.dgl.ai/wheels/repo.html
```
Required packages include:
```sh
torch==1.9.0, cudnn==8.4, numpy==1.22.0, scanpy==1.8.2, anndata==0.8.0, dgl==0.9.0,
pandas==1.2.4, scipy==1.7.3, scikit-learn==1.0.1, tqdm==4.64.1, matplotlib==3.5.3,
tensorboardX==2.5.1, pyyaml==6.0.1, plotly==5.21.0, kaleido==0.2.1, igraph==0.9.8
```


## 🚀 Quick Start
See our model document details from [Docs](https://keaml-guan.github.io/GSG/).

We provide the scripts for reproducing the quantitative and visualization results of the paper in [/docs/tutorials/](https://github.com/keaml-Guan/GSG/tree/main/docs/tutorials/).
 
Before using, you need to download and unzip the data:
```sh
cd ./data/10X
cat 151673.zip* > 151673.zip
unzip -d ./ 151673.zip
cd ../..
```
And then, you can start using the following code :
    
```sh
adata = GSG.pp.read_10X_Visium_with_label(args.folder_name + args.sample_name)
adata, graph = GSG.pp.Graph_10X(adata, args)
adata, model = GSG.train.GSG_train(adata, graph, args)
```



![](https://github.com/keaml-Guan/GSG/blob/main/figures/Result.jpg)

<!-- ## Issues on experiment
We found that SpaceFlow has different versions on GitHub and PyPi. The version installed in the recommended way is backward. In addition, the new version on GitHub has corrections to the old version, while the code on PyPi has fatal problems, which leads to serious problems in spatial domain identification. -->

## 📚 Citation
Wang C, Zhang T, Sun H, et al. A masked generative graph representation learning framework empowering precise spatial domain identification[J]. Bioinformatics, 2026, 42(6).

## 📩 Contact
If you have any questions, feel free to contact [chuyao25@mails.jlu.edu.cn](mailto:chuyao25@mails.jlu.edu.cn).
