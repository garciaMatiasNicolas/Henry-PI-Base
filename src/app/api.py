from fastapi import APIRouter
from typing import Optional
from .controller import DataUploadController
from ..database.DataBase__singleton import MySQLConnector 
from typing import Dict

db_connector = MySQLConnector()
data_upload_controller = DataUploadController(db_connector=db_connector)
router = APIRouter(
    prefix="/pipeline"
)

@router.post("/upload/{model_name}")
async def upload_data_endpoint(model_name: Optional[str] = None) -> Dict[str, str]:
    """
    Endpoint to trigger data upload for a specific model or all models.
    """
    return await data_upload_controller.upload_data(model_name=model_name)
   