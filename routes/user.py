from fastapi import APIRouter, HTTPException

from models.user import User
from config.db import conn
from schemas.user import userEntity, usersEntity
from bson import ObjectId
user = APIRouter()

@user.get('/')
async def find_all_users():
    return usersEntity(conn.local.user.find())

@user.get('/{id}')
async def find_one_user(id):
    try:
        # 1. Convert the ID to ObjectId
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid User ID format")

    # 2. Find the user
    user_data = conn.local.user.find_one({"_id": object_id})

    # 3. Check if user was found
    if user_data:
        # 4. Process the single user document using userEntity
        return userEntity(user_data)
    else:
        # 5. Raise a 404 Not Found error if user doesn't exist
        raise HTTPException(status_code=404, detail="User not found")
    

@user.post('/')
async def create_user(user : User):
    conn.local.user.insert_one(dict(user))
    return usersEntity(conn.local.user.find())

@user.put('/{id}')
async def update_user(id, user : User):
    try:
        # 1. Convert the ID to ObjectId
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid User ID format")

    # 2. Find the user
    conn.local.user.find_one_and_update({"_id": object_id},{
        "$set": dict(user)
    })
    user_data = userEntity(conn.local.user.find_one({"_id":object_id}))
    # 3. Check if user was found
    if user_data:
        # 4. Process the single user document using userEntity
        return user_data
    else:
        # 5. Raise a 404 Not Found error if user doesn't exist
        raise HTTPException(status_code=404, detail="User not found")
    # conn.local.user.find_one_and_update({"_id":ObjectId(id)},{
    #                                    "$set":dict(user)
    #                                    })
    # return userEntity(conn.local.user.find_one({"_id":ObjectId(id)}))

@user.delete('/{id}')
async def delete_user(id, user : User):
    try:
        # 1. Convert the ID to ObjectId
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid User ID format")

    deleted_user = conn.local.user.find_one_and_delete({"_id":object_id})
    if deleted_user:
        return userEntity(deleted_user)
    else:
        # If deleted_document is None, it means no user was found with that ID to delete
        raise HTTPException(status_code=404, detail="User not found")