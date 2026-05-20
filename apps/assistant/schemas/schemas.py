from pydantic import BaseModel, Field
from typing import List, Optional


# ==========================================
# DJANGO NINJA INBOUND DATA SCHEMAS
# ==========================================
class UserDocumentPayload(BaseModel):
    user_id: str
    extracted_text: str = Field(..., description="The OCR transcription text or voice note transcript sent by the user.")
    user_instruction: Optional[str] = Field("mre7ba, fhemna ach kayn f had l-wetiqa", description="Specific user override instruction.")
