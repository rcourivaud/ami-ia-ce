# Welcome / juradinfo-ia

## Description

Welcome ! juradinfo-ia is a NLP application ...

## Getting started


### Install the project

First you need to clone the repository.
  Do not forget to upload your SSH Key into gitlab and having the right access.

```bash
git clone git@srv425v.conseil-etat.fr:externe/juradinfo-ia/juradinfo-ia-data.git
```
```bash
cd juradinfo-ia-data
```

### Prerequisites

* **Anaconda environnement**

Since it's a Python-Based project, we work in Anaconda environnement. 

To install Anaconda if not already installed in your computer follow the instructions at <https://docs.anaconda.com/anaconda/install/>

Create and activate a conda environment where you will install all the librairies with following commands inside a bash shell (for Windows users, open Anaconda command prompt) :

```bash
conda create -n name_of_the_env
```
```bash
conda activate name_of_the_env
```

* **Install packages** 

You need to install some packages on your computer inside the conda environment you created :

```bash
bash install.sh
```

* **Windows specific**
 
If you are using windows OS, you will need to install Tesseract an ocr library, and Ghostscript an image management library.
you will find installation instructions and installer there : 

    * [ghostscrip,](https://www.ghostscript.com/download/gsdnld.html)
    * [Tesseract-ocr](https://github.com/UB-Mannheim/tesseract/wiki)
    * [ImageMagick](https://imagemagick.org/script/download.php)

Then, download and paste in the Tesseract-ocr folder the [fra.traineddata](https://github.com/tesseract-ocr/tessdata/blob/master/fra.traineddata) file that allows Tesseract to ocr french.

### IDE
The following IDE are installed with Anaconda

* Jupyter notebook
* Spyder

### Test the project
When everything is installed and run well, if you want to run every unit tests, do the following:

```bash
python -m unittest
```

### Run it
When everything is installed, if you want to run it, do the following:

* Data OCR pipeline :

```bash
TODO
```

* IA algorithms

### Deployment

Please read [DEPLOYMENT](DEPLOYMENT.md) for details on our deployment process on the CE server.

## Documentation
The technical documentation is located inside ./docs/build/pdf or ./docs/build/html.

Please read [README](./docs/README.md) for details about the generation process of that documentation.

## Contributing

Please read [CONTRIBUTING](./docs/CONTRIBUTING.md) for details on our code of conduct, and the process for pushing new features/patch

## Authors

* **Starclay**

## License

This project is completely private.
