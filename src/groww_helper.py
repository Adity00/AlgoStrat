import os
from dotenv import load_dotenv
from growwapi import GrowwAPI
import pyotp

# Load environment variables from .env file
load_dotenv()

class GrowwHelper:
    @staticmethod
    def get_api_client():
        """
        Initializes and returns a GrowwAPI client instance based on the environment configuration.
        Supports both the standard API key & secret flow, and the TOTP flow.
        """
        api_key = os.getenv("GROWW_API_KEY")
        secret = os.getenv("GROWW_API_SECRET")
        totp_secret = os.getenv("GROWW_TOTP_SECRET")

        if not totp_secret and (not api_key or not secret):
            raise ValueError(
                "Credentials missing! Please create a '.env' file based on '.env.template' "
                "and populate either GROWW_TOTP_SECRET or both GROWW_API_KEY and GROWW_API_SECRET."
            )

        # 1st Priority: TOTP flow (Recommended)
        if totp_secret and api_key:
            print("Attempting authentication via TOTP Flow...")
            # Generate the current TOTP code using the secret
            totp = pyotp.TOTP(totp_secret)
            current_otp = totp.now()
            print(f"Current TOTP Code Generated: {current_otp}")
            
            # Fetch access token using TOTP token (as api_key) and generated OTP
            access_token = GrowwAPI.get_access_token(api_key=api_key, totp=current_otp)
            client = GrowwAPI(access_token)
            print("Authentication successful via TOTP Flow!")
            return client
            
        # 2nd Priority: API Key & Secret Flow (Fallback if only secret is given and not TOTP secret)
        if api_key and secret:
            print("Attempting authentication via API Key & Secret Flow...")
            # Retrieve access token
            access_token = GrowwAPI.get_access_token(api_key=api_key, secret=secret)
            client = GrowwAPI(access_token)
            print("Authentication successful!")
            return client
            
        # Fallback placeholder if SDK requires customized instantiation for TOTP
        raise NotImplementedError("TOTP initialization code needs custom mapping based on SDK version.")
