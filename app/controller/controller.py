from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from ..schemas.schemas import URLCreate, URLResponse, APIResponse
from ..services.service import URLService
from ..dependencies import get_service
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
router = APIRouter()

error_response_schema = {
    "status": {"type": "string", "example": "failure"},
    "message": {"type": "string", "example": "Invalid input for 'original_url': Field required"},
    "data": {"type": "object", "nullable": True}
}
@router.post("/urls", status_code=status.HTTP_201_CREATED, response_model=APIResponse)
def create_url(item: URLCreate, service: URLService = Depends(get_service)):
    try:
        new_link = service.create_short_link(item)
        return {
            "status": "success",
            "data": URLResponse.from_orm(new_link).model_dump(),
            "message": "Done"
        }
    except Exception as e:
        return {"status": "failure", "message": str(e)}


@router.get("/u/{code}")
def redirect_to_original(code: str, service: URLService = Depends(get_service)):
    original_url = service.get_original_url(code)
    if not original_url:
        raise HTTPException(
            status_code=400,
            detail={"status": "failure", "message": "URL not found or has expired"}
        )
    return RedirectResponse(url=original_url, status_code=307)


@router.get("/urls", response_model=APIResponse)
def get_all_urls(service: URLService = Depends(get_service)):
    links = service.get_all_links()
    return {
        "status": "success",
        "data": [URLResponse.from_orm(link) for link in links]
    }


@router.delete("/urls/{code}", response_model=APIResponse)
def delete_url(code: str, service: URLService = Depends(get_service)):
    success = service.delete_link(code)
    if not success:
        raise HTTPException(
            status_code=400,
            detail={"status": "failure", "message": "URL not found"}
        )
    return {"status": "success", "message": "URL deleted successfully"}


@router.post("/admin/cleanup", response_model=APIResponse)
def run_cleanup_job(service: URLService = Depends(get_service)):
    """This path simulates a scheduled execution (Scheduler/Cron Job)."""
    count = service.cleanup_expired_links()
    return {
        "status": "success",
        "message": f"Cleanup finished. {count} link(s) marked as inactive."
    }
