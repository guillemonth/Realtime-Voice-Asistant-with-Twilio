import os
from dotenv import load_dotenv
load_dotenv()

class Constants():

    BASE_URL: str = os.environ.get("BASE_URL","")

    TWILIO_OUTPUT_RATE: int  = int(os.environ.get("TWILIO_OUTPUT_RATE",8000))

constants = Constants()