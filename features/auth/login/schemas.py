"""Schémas Pydantic - connexion."""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Corps de ``POST /auth/login``."""

    email: EmailStr = Field(..., description="Email opérateur")
    password: str = Field(..., min_length=1, description="Mot de passe")


class LoginResponse(BaseModel):
    """Jetons Supabase après connexion."""

    access_token: str = Field(..., description="JWT à envoyer en Bearer")
    refresh_token: str = Field(...,
                               description="Jeton de rafraîchissement Supabase")
    token_type: str = Field(default="bearer", description="Type OAuth2")
    expires_in: int | None = Field(
        default=None, description="Durée de vie access token (s)")
