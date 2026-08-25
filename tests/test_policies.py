from src.app import activities


def test_signup_blocks_when_activity_is_full(client):
    activities["Test Full Club"] = {
        "description": "Capacity test club",
        "schedule": "Fridays, 5:00 PM - 6:00 PM",
        "max_participants": 1,
        "participants": ["filled@mergington.edu"],
    }

    response = client.post(
        "/activities/Test%20Full%20Club/signup",
        params={"email": "newperson@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_signup_treats_email_as_case_insensitive(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "MICHAEL@MERGINGTON.EDU"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_normalizes_email_whitespace_and_case(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "  NewStudent@Mergington.edu  "},
    )

    assert response.status_code == 200
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_unregister_normalizes_email_whitespace_and_case(client):
    activities["Chess Club"]["participants"].append("tempstudent@mergington.edu")

    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "  TEMPSTUDENT@MERGINGTON.EDU  "},
    )

    assert response.status_code == 200
    assert "tempstudent@mergington.edu" not in activities["Chess Club"]["participants"]


def test_signup_rejects_blank_email_after_trimming(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "   "},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email is required"
