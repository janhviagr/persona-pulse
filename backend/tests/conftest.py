import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_personapulse.db"
if os.path.exists("test_personapulse.db"):
    os.remove("test_personapulse.db")
