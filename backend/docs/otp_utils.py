import pyotp
import secrets

def generate_otp_secret() -> str:
    """Generate a new OTP secret."""
    return pyotp.random_base32()

def get_otp_uri(secret: str, username: str, issuer: str = "SecureDocs") -> str:
    """Generate OTP URI for QR code."""
    return pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer)

def verify_otp(secret: str, token: str) -> bool:
    """Verify OTP token."""
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
