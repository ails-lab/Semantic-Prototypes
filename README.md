# Semantic Prototypes: Enhancing Transparency Without Black Boxes


## Dependencies
* Install Jupyter Notebook/Lab [https://jupyter.org/install](https://jupyter.org/install).
* Install a Conda distribution, e.g. [Miniconda](https://docs.anaconda.com/free/miniconda/).
* Create the envirornment.
```bash
conda env create -f environment.yml
```

* Add the conda environment to Jupyter.
```bash
python -m ipykernel install --user --name=protosem
```


## Preprocess the CUB-200 Dataset like [ProtoPNet](https://github.com/cfchen-duke/ProtoPNet)

Follow these instructions to prepare the data:
1. Download the dataset CUB_200_2011.tgz from http://www.vision.caltech.edu/visipedia/CUB-200-2011.html
2. Unpack CUB_200_2011.tgz
3. Crop the images using information from bounding_boxes.txt (included in the dataset)
4. Split the cropped images into training and test sets, using train_test_split.txt (included in the dataset)
5. Put the cropped training images in the directory "./datasets/cub200_cropped/train_cropped/"
6. Put the cropped test images in the directory "./datasets/cub200_cropped/test_cropped/"

For cropping the images, you can use the `preprocessing/crop_images.py` script provided in this repository: [Explaining_Prototypes](https://github.com/M-Nauta/Explaining_Prototypes).


## Creating Class Cluster Descriptions

1. Download CUB-200 at ...
2. Copy the file `attributes.txt`  from the outer `CUB_200_2011` directory into the `attributes` subdirectory.
3. Download and unzip CLEVR-Hans3. `wget https://tudatalib.ulb.tu-darmstadt.de/bitstream/handle/tudatalib/2611/CLEVR-Hans3.zip
` 
`unzip CLEVR-Hans3.zip`
4. CLEVR-Hans3 object attributes can be found preprocessed in `CLEVR-Hans3_attributes.json`
5. Edit CUB-200 and CLEVR-Hans3 directory paths in `compute_ccds.ipynb` and then run it. The resulting CCDs will be saved in the `results` directory.

## Creating Semantic Prototypes

**For CUB-200**
Edit the CUB-200 directory path in `compute_prototypes.ipynb` and then run it. The resulting prototypes for CUB-200 will be saved in the `results` directory.

**For CLEVR-HANS3**
Execute the script by running the following command in your terminal:
```bash
python clevr_hans.py "CLEVR-Hans3/train/CLEVR_HANS_scenes_train.json" num_of_label
```
Replace `"CLEVR-Hans3/train/CLEVR_HANS_scenes_train.json"` with the actual path to your JSON file, and `num_of_label` with the label number you want to retrieve prototypes for (valid options are 0, 1, or 2).

Example:
```bash
python clevr_hans.py "CLEVR-Hans3/train/CLEVR_HANS_scenes_train.json" 1
```