import os

class Constants():

    BASE_URL = "t2c26bmb-8000.uks1.devtunnels.ms"

    TWILIO_OUTPUT_RATE:int  = int(os.environ.get("TWILIO_OUTPUT_RATE",8000))