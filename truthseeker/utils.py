def check_username(username):
    if not username:
        return False
    if not username == username.strip():
        return False
    if not len(username) < 16:
        return False
    
    return True
