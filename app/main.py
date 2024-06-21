from dotenv import load_dotenv
from fastapi import FastAPI

# load_dotenv()
app = FastAPI(debug=True)
from app.user.routes.v1 import user
from app.schedule.routes.v1 import availability

# from app.schedule.routes.v1 import schedule
from app.schedule.routes.v1 import event
