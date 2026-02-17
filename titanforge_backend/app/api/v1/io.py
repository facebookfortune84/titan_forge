from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict
from pathlib import Path

from ... import db_models
from ...dependencies import get_current_active_user

router = APIRouter()

class FilePath(BaseModel):
    path: str

class FileContent(BaseModel):
    path: str
    content: str

AGENT_FILES_DIR = Path("./agent_files_workspace").resolve()
AGENT_FILES_DIR.mkdir(parents=True, exist_ok=True)

def get_safe_path(base_dir: Path, relative_path: str) -> Path:
    full_path = (base_dir / relative_path).resolve()
    if not full_path.is_relative_to(base_dir):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed outside designated workspace."
        )
    return full_path

@router.post("/read")
async def read_agent_file(
    file_path_data: FilePath,
    current_user: db_models.User = Depends(get_current_active_user),
) -> Dict[str, str]:
    try:
        path = get_safe_path(AGENT_FILES_DIR, file_path_data.path)
        if not path.is_file():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
        content = path.read_text()
        return {"content": content}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to read file: {e}")

@router.post("/write")
async def write_agent_file(
    file_content_data: FileContent,
    current_user: db_models.User = Depends(get_current_active_user),
) -> Dict[str, str]:
    try:
        path = get_safe_path(AGENT_FILES_DIR, file_content_data.path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(file_content_data.content)
        return {"message": "File written successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to write file: {e}")
