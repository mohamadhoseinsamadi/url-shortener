from fastapi import Depends
from sqlalchemy.orm import Session
from .database.database import get_db
from .repository.repository import URLRepository
from .services.service import URLService


# سازنده ریپوزیتوری
def get_repository(db: Session = Depends(get_db)) -> URLRepository:
    return URLRepository(db)


# سازنده سرویس (ریپوزیتوری به داخل سرویس تزریق می‌شود) [cite: 48, 52]
def get_service(repo: URLRepository = Depends(get_repository)) -> URLService:
    return URLService(repo)
