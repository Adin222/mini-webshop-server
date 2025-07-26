from fastapi import Request, HTTPException, status


def require_authentication(request: Request):
    access_token = request.cookies.get('access_token')

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    
    pass