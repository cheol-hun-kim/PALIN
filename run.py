import uvicorn
import os

if __name__ == "__main__":
    # Ensure folders exist
    os.makedirs("static", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    
    print("PALIN OS Central Server is starting...")
    print("Local App URL: http://127.0.0.1:8000")
    print("Director Admin Dashboard: http://127.0.0.1:8000/admin.html")
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
