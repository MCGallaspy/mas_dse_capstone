# About

This is the capstone project for gropu 5 of the University of California San Diego's Masters of Advance Studies in Data Science and Engineering program (UCSD MAS DSE) cohort 5. 
The group consists of Michael Gallaspy, Kevin Kannappan, Sofean Maeouf, Sathish Masilamani, Martin La Pierre.
The goal of this project is to integrate historical weather, economic, and wildfire data in order to answer some of the following questions:

* What ways are there to quantify the characteristics of wildfires? E.g. frequency, area burned and economic impact.
* How have the characteristics of wildfires changed over the past few years?
* Can weather be used to characterise wildfire risk?

This README attempts to document the work in case others wish to replicate or adapt it, but it does not attempt to exhaustively document the various decisions for pursuing one course of action over another. For example, we explored several sources of weather data before deciding to rely on gridMET, due primarily to the ease of access and organization of that dataset, however similar decisions are generally not explained in this document or repository. For more information about the decisions and results of this project, the associated reports may be consulted.

## Approach

Data exploration, integration, and results are primarily presented through a series of Jupyter notebooks intended to be run on a personal laptop, or for more computationally intensive notebooks on an Amazon EMR cluster that is running Jupyter Hub, Spark, and potentially other software packages.
Many notebooks depend on the results generated from a previous notebook -- in some cases (but not all) we have attempted to document it by numbering notebooks in the order they should be run.
In some cases, the notebooks read or write data from Amazon's S3 service in order to facilitate sharing of large data files.
For such notebooks Amazon credentials must be supplied according to the library in use.

## Organization

The `data` directory primarily contains notebooks for obtaining primary data and minimal pre-processing for further analysis. Regarding the subdirectories:

* In `data/gridMet`, notebooks 1 and 2 demonstrate downloading gridMET data from where it is hosted for the region of San Diego, and uploading that data in parquet format to Amazon S3.
  Downloading from gridMET's servers can be error prone, so notebook 1 in particular may need to be run interactively in several sessions to download all desired data.


The `notebooks` directory contains both exploratory data analysis (EDA) of several data sets, notebooks integrating datasets, and analysis of the integrated data sets. In `notebooks/gridMet` in particular:

* Notebooks 1 through 3 demonstrate obtaining gridMET data previously uploaded to S3 in another notebook, and EDA through some basic plots.
* Notebook 4 integrates