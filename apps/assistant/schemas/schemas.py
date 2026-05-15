from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# GEMINI ENGINE STRUCTURED OUTPUT SCHEMA
# ==========================================
class GeminiDwiResponseSchema(BaseModel):
    explanation: str = Field(
        description="The primary explanation, translated document content, composed complaint, or drafted text in simple Moroccan Darija (Arabic script)."
    )
    missing_information: List[str] = Field(
        default=[],
        description="Array of missing elements, variables, or items required from the user to complete the task accurately. Leave empty if no context is missing."
    )
    is_unclear: bool = Field(
        default=False,
        description="Flag true if the user's uploaded document content or message prompt is entirely unintelligible, ambiguous, or unreadable."
    )
    unclear_message: str = Field(
        default="",
        description="If is_unclear is True, this property MUST contain exactly: 'هاد النقطة ما واضحةش فالمعطيات اللي توصلت بها.' Otherwise, keep empty."
    )
    disclaimer: str = Field(
        default="",
        description=(
            "Mandatory exact warning block for any legal, financial, medical, tax, administrative, banking, or employment document. "
            "Must be exactly: 'ملاحظة: هاد الشرح غير باش يعاونك تفهم، وماشي استشارة قانونية أو طبية أو مالية أو إدارية رسمية.' "
            "Leave completely empty if the text does not touch any of these professional domains."
        )
    )

# ==========================================
# DJANGO NINJA INBOUND DATA SCHEMAS
# ==========================================
class UserDocumentPayload(BaseModel):
    user_id: str
    extracted_text: str = Field(..., description="The OCR transcription text or voice note transcript sent by the user.")
    user_instruction: Optional[str] = Field("mre7ba, fhemna ach kayn f had l-wetiqa", description="Specific user override instruction.")