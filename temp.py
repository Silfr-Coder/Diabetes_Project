from diabetes_dataset import DiabetesDataset

#  Create an instance of the DiabetesDataset class
dataset = DiabetesDataset("./data/processed/diabetes_cleaned.csv")
# print the first few rows of the dataset
print(f"Record count is: {dataset.get_record_count()}")
print(f"Feature count is: {dataset.get_feature_count()}")
print(f"Data quality is: {dataset.get_data_quality()}%")
print(dataset.get_preview(3))
