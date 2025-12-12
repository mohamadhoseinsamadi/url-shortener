import random
import string
from ..repository.repository import URLRepository
from ..schemas.schemas import URLCreate
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()
try:
    TTL_SECONDS = int(os.environ.get("LINK_TTL_SECONDS", 0))
except ValueError:
    TTL_SECONDS = 0


class URLService:
    def __init__(self, repository: URLRepository):
        self.repository = repository
        self.ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def _generate_short_code(self, length: int = 6) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def create_short_link(self, url_data: URLCreate):
        expires_at = None
        if TTL_SECONDS > 0:
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=TTL_SECONDS)

        new_record = self.repository.create(str(url_data.original_url), expires_at=expires_at)

        code = self._generate_short_code()
        print(code)
        final_record = self.repository.update_short_code(new_record.id, code)
        return final_record

    def get_original_url(self, short_code: str):
        link = self.repository.get_by_code(short_code)

        if link and link.is_active:
            if link.expires_at and link.expires_at < datetime.now(timezone.utc):
                self.repository.mark_expired_and_inactive(short_code)
                return None

            return link.original_url

        return None

    def get_all_links(self):
        return self.repository.get_all()

    def delete_link(self, short_code: str):
        return self.repository.delete(short_code)

    def cleanup_expired_links(self) -> int:
        """Finds and disables expired links."""
        expired_links = self.repository.get_expired_links()

        count = 0
        for link in expired_links:
            if self.repository.mark_expired_and_inactive(link.short_code):
                count += 1

        return count
