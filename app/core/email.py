# app/core/email.py
import aiohttp

async def send_email(subject: str, message: str, to_email: str):
    async with aiohttp.ClientSession() as session:
        payload = {
            "subject": subject,
            "message": message,
            "to": to_email,
            # Additional parameters
        }
        # Replace with your email service API
        await session.post("https://email-service/send", json=payload)