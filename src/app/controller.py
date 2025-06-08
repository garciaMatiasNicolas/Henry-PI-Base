from ..models.Products import Product
from ..models.Categories import Category 
from ..models.Cities import City 
from ..models.Customers import Customer 
from ..models.Employees import Employee 
from ..models.Sales import Sale 
from ..models.Countries import Country
from ..database.DataBase__singleton import MySQLConnector 
from typing import Dict, Type, List, Optional
from fastapi import HTTPException, status
from ..pipelines.DataIngestion import DataIngestion
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataUploadController:

    MODEL_MAP: Dict[str, Type] = {
        "categories": Category,
        "cities": City,
        "countries": Country,
        "products": Product,
        "employees": Employee,
        "customers": Customer,
        "sales": Sale
    }

    def __init__(self, db_connector: MySQLConnector):
        self.db_connector = db_connector

    async def upload_data(self, model_name: Optional[str] = None) -> Dict[str, str]:
        """
        Uploads data for a specified model type using the DataIngestion pipeline.
        If no model name is specified, it attempts to upload data for all registered models.

        Args:
            model_name: The name of the model to upload data for.
                        If None, all models will be processed.

        Returns:
            A dictionary indicating the success or failure of the data upload,
            including warnings for individual model failures.

        Raises:
            HTTPException: If a specified model is not found or if all models fail to upload.
        """
        failed_models: List[str] = []
        successful_models: List[str] = []

        if model_name == "all":
            # Handle the case where no specific model name is provided (upload all)
            for name, model_class in self.MODEL_MAP.items():
                try:
                    logger.info(f"Attempting to upload data for model: {name}")
                    data_ingestion_pipeline = DataIngestion(
                        model_class=model_class,
                        loader_type='csv',  
                        database=self.db_connector
                    )
                    data_ingestion_pipeline.upload_data()
                    successful_models.append(name)
                    logger.info(f"Successfully uploaded data for model: {name}")
                except Exception as e:
                    logger.error(f"Error uploading data for model '{name}': {e}", exc_info=True)
                    failed_models.append(name)

            if not successful_models and failed_models:
                # All models failed
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"All models failed to upload data: {', '.join(failed_models)}. Please check server logs for details."
                )
            elif failed_models:
                # Some models failed, but at least one succeeded
                return {
                    "message": f"Data upload completed. Successfully processed models: {', '.join(successful_models)}.",
                    "warning": f"The following models failed to upload data: {', '.join(failed_models)}. Please check server logs for details."
                }
            else:
                # All models succeeded
                return {"message": "Data for all models uploaded successfully to the database."}
        else:
            # Handle the case where a specific model name is provided
            target_model_class = self.MODEL_MAP.get(model_name.lower())

            if not target_model_class:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Model '{model_name}' not found. Available models are: {', '.join(self.MODEL_MAP.keys())}"
                )

            try:
                logger.info(f"Attempting to upload data for specific model: {model_name}")
                data_ingestion_pipeline = DataIngestion(
                    model_class=target_model_class,
                    loader_type='csv',
                    database=self.db_connector
                )
                data_ingestion_pipeline.upload_data()
                logger.info(f"Successfully uploaded data for model: {model_name}")
                return {"message": f"Data for {model_name} was uploaded successfully to the database."}
            except Exception as e:
                logger.error(f"Error uploading data for {model_name}: {e}", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to upload data for {model_name}: {str(e)}"
                )
