import logging
from uuid import uuid4, UUID
from fastapi import FastAPI, Header
from typing import List
from models import User, Role, Gender, UserUpdate
from fastapi import HTTPException

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


app = FastAPI()

# Temproary Database
db : List[User] = [
    User(
        name="Salman",
        email="salman@salman.com",
        gender="male",
        roles=[Role.admin],
        password="s3cret_p@ss"
    ),
        User(
        name="Kevin",
        email="kevin@salman.com",
        gender=Gender.male,
        roles=[Role.student],
        password="s3cret_p@ss"
    ),
        User(
        id=uuid4(),
        name="Ghost",
        email="ghost@salman.com",
        gender=Gender.male,
        roles=[Role.user],
        password="s3cret_p@ss"
    )
]

# Create Route
@app.post("/api/v1/users", tags=["User"])
async def create_user(user: User):  
    logger.info(f"Creating user: {user.name} with user id {user.id}")
    db.append(user)
    return {"id": user.id}

# Read Route
@app.get("/api/v1/users", tags=["User"])
async def fetch_all_users(user_agent: str = Header(None)):
    logger.info(f"Fetching all users, for USER_AGENT {user_agent}")
    return db

# Update Route
# Complete Update
@app.put("/api/v1/users/{user_id}", tags=["User"])
async def update_user(user_id: str, update_user: UserUpdate):
    for user in db:
        if user.id == UUID(user_id):
            for key,value in update_user.dict(exclude_unset=True).items():
                setattr(user, key, value)
            logger.info(f"User {user.id} updated successfully")
            return {"message": "User updated successfully", "id": user.id}
        
    raise HTTPException(status_code=404, detail="User not found")

# Partial Update
@app.patch("/api/v1/users/{user_id}", tags=["User"])
async def update_user(user_id: str, update_user: UserUpdate):
    for user in db:
        if user.id == UUID(user_id):
            for key, value in update_user.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            logger.info(f"[!] User {user.id} updated")
            return {"message":"User updated"}

    raise HTTPException(status_code=404, detail="User not found")
    

# Delete Route
@app.delete("/api/v1/users/{user_id}", tags=["User"])
async def delete_user(user_id: str):
    for user in db:

        logger.debug(f"Checking user: {user.id}")
        logger.debug(f"User id: {user_id == user.id} with {user.id}")

        if user.id == UUID(user_id):
            db.remove(user)
            logger.info(f"User {user.name} deleted successfully")
            return {"message": "User deleted successfully"}
        
    logger.warning(f"User {user.name} not found in the database")
    return {"message": "User not found"}