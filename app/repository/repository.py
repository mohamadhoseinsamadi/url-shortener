from sqlalchemy.orm import Session
from ..model.models import URLItem
from typing import Optional
from datetime import datetime, timezone


class URLRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, original_url: str, expires_at: Optional[datetime] = None) -> URLItem:
        db_item = URLItem(original_url=original_url, expires_at=expires_at)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update_short_code(self, url_id: int, code: str):
        item = self.db.query(URLItem).filter(URLItem.id == url_id).first()
        if item:
            item.short_code = code
            self.db.commit()
            self.db.refresh(item)
        return item

    def get_by_code(self, short_code: str) -> URLItem:
        item = self.db.query(URLItem).filter(URLItem.short_code == short_code).first()
        return item

    def get_all(self):
        return self.db.query(URLItem).all()

    def delete(self, short_code: str) -> bool:
        item = self.db.query(URLItem).filter(URLItem.short_code == short_code).first()
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False

    def mark_expired_and_inactive(self, short_code: str) -> bool:
        """Disables the link."""
        item = self.db.query(URLItem).filter(URLItem.short_code == short_code).first()
        if item:
            item.is_active = False
            self.db.commit()
            self.db.refresh(item)
            return True
        return False

    def get_expired_links(self) -> list[URLItem]:
        """Return all active links that have expired."""

        return (
            self.db.query(URLItem)
            .filter(URLItem.is_active == True)
            .filter(URLItem.expires_at != None)
            .filter(URLItem.expires_at < datetime.now(timezone.utc))
            .all()
        )
