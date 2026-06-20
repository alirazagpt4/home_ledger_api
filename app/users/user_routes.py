from fastapi import APIRouter, status, HTTPException
from app.users.user_model import UserRegister
from app.users.user_services import UserServices

# APIRouter ka instance banaya taake main.py isko pehchan sakay
router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegister):
    try:
        # Request body se validated data seedha service layer ko pass kiya
        response = await UserServices.register_new_user(user)
        return response
    except HTTPException as http_ex:
        # Agar service layer se koi jana-bojha error aaye (jaise duplicate username)
        raise http_ex
    except Exception as e:
        # Agar koi unexpected database crash ya network error ho
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Route Execution Error: {str(e)}"
        )