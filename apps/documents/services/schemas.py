from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any


class DynamicProcessPayload(BaseModel):
    user_id: str
    user_instruction: str = Field(..., description="The Darija task command requested by the user.")

    # Optional parameters depending on your system's pre-extraction success
    extracted_text: Optional[str] = Field(None, description="Pre-extracted text or transcript if successful.")

    # Fallback parameters if pre-extraction fails
    file_base64: Optional[str] = Field(None, description="Raw Base64 string of the file if extraction fails.")
    mime_type: Optional[str] = Field(None,
                                     description="The file MIME type, e.g., 'application/pdf', 'image/jpeg', 'audio/ogg'.")


# ==========================================
# GEMINI ENGINE STRUCTURED OUTPUT SCHEMA
# ==========================================
# class GeminiDwiResponseSchema(BaseModel):
#     explanation: str = Field(
#         description="The primary explanation, translated document content, composed complaint, or drafted text in simple Moroccan Darija (Arabic script)."
#     )
#     missing_information: List[str] = Field(
#         default=[],
#         description="Array of missing elements, variables, or items required from the user to complete the task accurately. Leave empty if no context is missing."
#     )
#     is_unclear: bool = Field(
#         default=False,
#         description="Flag true if the user's uploaded document content or message prompt is entirely unintelligible, ambiguous, or unreadable."
#     )
#     unclear_message: str = Field(
#         default="",
#         description="If is_unclear is True, this property MUST contain exactly: 'هاد النقطة ما واضحةش فالمعطيات اللي توصلت بها.' Otherwise, keep empty."
#     )
#     disclaimer: str = Field(
#         default="",
#         description=(
#             "Mandatory exact warning block for any legal, financial, medical, tax, administrative, banking, or employment document. "
#             "Must be exactly: 'ملاحظة: هاد الشرح غير باش يعاونك تفهم، وماشي استشارة قانونية أو طبية أو مالية أو إدارية رسمية.' "
#             "Leave completely empty if the text does not touch any of these professional domains."
#         )
#     )

class GeminiDwiResponseSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')
    document_type: str = Field(description="The category of the document (e.g., 'فاتورة', 'عقد كراء', 'استمارة CNSS').")

    short_summary_darija: str = Field(
        description="A concise 1-2 sentence summary of the document in Moroccan Darija (Arabic script).")

    important_points_darija: List[str] = Field(
        description="A list of key takeaways or critical facts extracted from the document in Darija.")

    extracted_entities: List[str, Any] = Field(
        description="A dictionary of key entities like names, dates, amounts, or IDs found in the document (e.g., {'المالك': '...', 'التاريخ': '...'}).")

    unclear_points_darija: List[str] = Field(
        description="A list of ambiguous or missing points in the document. Return an empty list if everything is clear.")

    next_steps_darija: List[str] = Field(
        description="Actionable steps the user should take based on this document (e.g., 'خصك تمشي للبنك', 'خاصك توقعه').")

    disclaimer_darija: str = Field(
        description="Mandatory disclaimer: 'ملاحظة: هاد الشرح غير باش يعاونك تفهم، وماشي استشارة قانونية أو طبية أو مالية أو إدارية رسمية.'")

    full_answer_darija: str = Field(
        description="A comprehensive, conversational explanation of the document in simple Moroccan Darija (Arabic script).")


