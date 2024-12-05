import sys

sys.path.append(".")
import uvicorn
from fastapi import FastAPI

from routers.cat_routers import cat
from routers.health import health
from routers.mission_routers import mission

app = FastAPI()


app.include_router(cat, prefix="/cat", tags=["Cats"])
app.include_router(health, tags=["DB"])
app.include_router(mission, tags=["Missions"])
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
