import jwt

key = "rGPGTRvizFHqOpLRMNJbqmXlycZtQZbTvJnWdKyRJZDxwqIDEi"
payload = {"id": "admin", "isAdmin": True}

token = jwt.encode(payload, key, algorithm="HS256")
if not isinstance(token, str): 
    token = token.decode()

print("JWT token:", token)
