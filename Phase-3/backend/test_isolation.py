from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import pytest
from main import app
from database import get_session
from models import User, Task
from auth import get_current_user_id

# Setup in-memory SQLite for testing isolation logic
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

def test_data_isolation(session: Session):
    # 1. Setup Mock Users and Tasks
    user_a_id = "user-a-uuid"
    user_b_id = "user-b-uuid"

    # 2. Define Dependency Overrides for Mocking Auth
    def get_user_a():
        return user_a_id

    def get_user_b():
        return user_b_id

    # 3. Inject our test session
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    # 4. Phase 1: User A creates a task
    app.dependency_overrides[get_current_user_id] = get_user_a
    response = client.post("/api/tasks", json={"title": "User A Private Task"})
    assert response.status_code == 201
    task_a_id = response.json()["id"]

    # 5. Phase 2: User B tries to list tasks
    app.dependency_overrides[get_current_user_id] = get_user_b
    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.json()
    # User B should NOT see User A's task
    assert len(tasks) == 0

    # 6. Phase 3: User B tries to access User A's task directly
    response = client.get(f"/api/tasks/{task_a_id}")
    # Should return 403 Forbidden (Ownership Isolation)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to access this resource"

    # 7. Phase 4: User B tries to delete User A's task
    response = client.delete(f"/api/tasks/{task_a_id}")
    assert response.status_code == 403

    # Clean up overrides
    app.dependency_overrides.clear()

if __name__ == "__main__":
    # Run tests using pytest logic
    import sys
    pytest.main([__file__])
