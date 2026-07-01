def test_signup_adds_new_participant(client, existing_activity_name, new_email):
    # Arrange
    before_response = client.get("/activities")
    before_payload = before_response.json()
    before_count = len(before_payload[existing_activity_name]["participants"])

    # Act
    signup_response = client.post(
        f"/activities/{existing_activity_name}/signup",
        params={"email": new_email},
    )
    after_response = client.get("/activities")
    after_payload = after_response.json()

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {new_email} for {existing_activity_name}"
    assert new_email in after_payload[existing_activity_name]["participants"]
    assert len(after_payload[existing_activity_name]["participants"]) == before_count + 1


def test_signup_returns_404_for_unknown_activity(client, new_email):
    # Arrange
    unknown_activity = "Unknown Club"

    # Act
    response = client.post(
        f"/activities/{unknown_activity}/signup",
        params={"email": new_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(
    client,
    existing_activity_name,
    existing_participant_email,
):
    # Arrange
    duplicate_email = existing_participant_email

    # Act
    response = client.post(
        f"/activities/{existing_activity_name}/signup",
        params={"email": duplicate_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
