from fastapi import FastAPI, HTTPException, status
from app.database import db, ping_database
# Dono tayar kiye hue modules ke routers ko cleanly import kiya
from app.users.user_routes import router as user_router


app = FastAPI(
    title="Home Ledger API Engine", 
    version="1.0.0",
    description="Clean Modular Core Backend Architecture"
)

# Database Startup Event Guard
@app.on_event("startup")
async def startup_db_client():
    print("🔄 Connecting to MongoDB Atlas...")
    is_connected = await ping_database()
    if is_connected:
        print("🚀 Database Engine Status: ONLINE")
    else:
        print("🚨 Database Engine Status: OFFLINE")

# Base Route
@app.get("/")
def read_root():
    return {"status": "running", "message": "Welcome to Modular API Engine"}

# Central Switchboard: Routes Register Karo
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])