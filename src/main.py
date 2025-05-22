from pipelines.DataIngestion import DataIngestion
import pandas as pd
from models.Categories import Category


categories = DataIngestion(Category)
categories.upload_data()