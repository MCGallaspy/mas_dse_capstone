Prerequisite:     Familiarity with GridMet Data and GeoMAC data and Random forest classifer/Regressor & MLP classifier
SW Requirements:  Pandas, Numpy, scikit-learn, matplotlib
Input Data:   	  https://dse-cohort5-group5.s3-us-west-1.amazonaws.com/ 'wildfire_capstone/integratedData/integratedData.pca40_and_firesonly.parquet.gz
		Integrated dataset with PCA 40 for fire only. Pls refer to 11. Re-integrate PCA components and labels with fires only .ipynb 
                 also refer to other notebooks of this project on how to retrieve GridMet data and integrate it with Fire dataset
Random forest classifier model:https://github.com/MCGallaspy/mas_dse_capstone/blob/master/notebooks/fire_prediction_results_analysis/9_Fire_risk_Classification_using%20_pcadataset_GridsearchCV_SDGE_Finalresults.ipynb
MLP classifier model:https://github.com/MCGallaspy/mas_dse_capstone/blob/master/notebooks/fire_prediction_results_analysis/10_Fire_risk_Severity_MLPClassification.ipynb
Random forest regressor model:https://github.com/MCGallaspy/mas_dse_capstone/blob/master/notebooks/fire_prediction_results_analysis/11_Fire_risk_Severity_RandomforestRegressor.ipynb

Random forest classifier Predictions:Excel sheet is created from dataframe. Will be uploaded to S3 if the notebook is run 
MLP classifier Excel sheet is created from dataframe. Will be uploaded to S3 if the notebook is run 
Random forest regressor Excel sheet is created from dataframe. Will be uploaded to S3 if the notebook is run 