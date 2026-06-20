from app.database import db
from app.users.user_model import UserRegister
from fastapi import HTTPException, status
import bcrypt  # Direct raw bcrypt use kar rahe hain, passlib khatam!

class UserServices:
    
    @staticmethod
    def hash_password(password: str) -> str:
        # Plain password ko bytes mein convert karna zaroori hai bcrypt ke liye
        password_bytes = password.encode('utf-8')
        # Salt generate kiya aur hash banaya
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        # Database mein string format mein save karne ke liye decode kiya
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    @staticmethod
    async def register_new_user(user_data: UserRegister):
        username_clean = user_data.username.lower().strip()
        
        # 1. Unique Username Check
        existing_user = await db.users.find_one({"username": username_clean})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Username '{user_data.username}' pehle se registered hai."
            )
            
        # 2. Data ko dict banaya
        user_dict = user_data.model_dump()
        user_dict["username"] = username_clean
        
        # 3. THE HEAD GUARD: 'ali' ko head banao baki ko role.value do
        if username_clean == "ali":
            user_dict["role"] = "head"
        else:
            user_dict["role"] = user_data.role.value
        
        # 4. Safe Modern Password Hashing
        try:
            user_dict["password"] = UserServices.hash_password(user_data.password)
        except Exception as hash_error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Cryptography Error: {str(hash_error)}"
            )
        
        # 5. MongoDB Save
        result = await db.users.insert_one(user_dict)
        
        if result.inserted_id:
            return {
                "status": "success",
                "message": f"User '{username_clean}' registered successfully as {user_dict['role']}!",
                "user_id": str(result.inserted_id)
            }
            
        raise HTTPException(status_code=500, detail="Database insertion failed")