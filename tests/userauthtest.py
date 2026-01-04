from app.auth import auth_service_reachable

if __name__ == "__main__":
    if auth_service_reachable():
        print("Authenticator service reachable")
