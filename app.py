# Load .env file
from dotenv import load_dotenv
load_dotenv()

from truthinquiry.app import APP as app # the variable 'app' is detected by `flask run`

if __name__ == "__main__":
    app.run()
