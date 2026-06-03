from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert isinstance(activities["Chess Club"], dict)
    assert activities["Chess Club"]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"


def test_signup_for_activity_success():
    # Arrange
    activity_name = "Chess Club"
    new_student = "newstudent@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": new_student})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_student} for {activity_name}"}

    follow_up = client.get("/activities")
    assert new_student in follow_up.json()[activity_name]["participants"]


def test_signup_for_activity_duplicate_returns_400():
    # Arrange
    activity_name = "Chess Club"
    existing_student = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": existing_student})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_from_activity_success():
    # Arrange
    activity_name = "Gym Class"
    student_email = "john@mergington.edu"
    endpoint = f"/activities/{activity_name}/unregister"

    # Act
    response = client.delete(endpoint, params={"email": student_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {student_email} from {activity_name}"}

    follow_up = client.get("/activities")
    assert student_email not in follow_up.json()[activity_name]["participants"]


def test_unregister_from_activity_not_signed_up_returns_400():
    # Arrange
    activity_name = "Basketball Team"
    missing_student = "notregistered@mergington.edu"
    endpoint = f"/activities/{activity_name}/unregister"

    # Act
    response = client.delete(endpoint, params={"email": missing_student})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_signup_unknown_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Club"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_unknown_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Club"
    endpoint = f"/activities/{activity_name}/unregister"

    # Act
    response = client.delete(endpoint, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
