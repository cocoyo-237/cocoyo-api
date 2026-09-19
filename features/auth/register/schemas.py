"""Schémas Pydantic — inscription Supabase Auth."""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Corps de ``POST /auth/register``.

    Contexte:
        Slice ``features/auth/register`` — création compte back-office.
    """

    email: EmailStr = Field(..., description="Adresse email de l'opérateur", examples=["ops@cocoyo.com"])
    password: str = Field(
        ...,
        min_length=8,
        description="Mot de passe (min. 8 caractères)",
        examples=["SecretPass123"],
    )


class RegisterResponse(BaseModel):
    """Réponse après inscription réussie."""

    user_id: str = Field(..., description="UUID utilisateur Supabase")
    email: EmailStr = Field(..., description="Email confirmé")
    message: str = Field(default="Inscription réussie", description="Message informatif")
