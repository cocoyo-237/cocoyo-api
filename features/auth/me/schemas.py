"""Schémas - profil utilisateur courant."""

from pydantic import BaseModel, EmailStr, Field


class MeResponse(BaseModel):
    """Profil dérivé du JWT Supabase."""

    id: str = Field(..., description="UUID utilisateur")
    email: EmailStr | None = Field(
        default=None, description="Email si disponible")
