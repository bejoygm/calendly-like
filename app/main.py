from fastapi import FastAPI

app = FastAPI(debug=True)

from app.user.routes.v1 import user
from app.schedule.routes.v1 import availability

# from app.schedule.routes.v1 import schedule
from app.schedule.routes.v1 import event
