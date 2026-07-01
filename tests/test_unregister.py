def test_unregister_removes_existing_participant(
    client,
    existing_activity_name,
    existing_participant_email,
):
    # Arrange
    before_response = client.get("/activities")
    before_payload = before_response.json()
    before_count = len(before_payload[existing_activity_name]["participants"])

    # Act
    remove_response = client.delete(
        f"/activities/{existing_activity_name}/participants",
        params={"email": existing_participant_email},
    )
    after_response = client.get("/activities")
    after_payload = after_response.json()

    # Assert
    assert remove_response.status_code == 200
    assert (
        remove_response.json()["message"]
        == f"Removed {existing_participant_email} from {existing_activity_name}"
    )
    assert existing_participant_email not in after_payload[existing_activity_name]["participants"]
    assert len(after_payload[existing_activity_name]["participants"]) == before_count - 1


def test_unregister_returns_404_for_unknown_activity(client, existing_participant_email):
    # Arrange
    unknown_activity = "Unknown Club"

    # Act
    response = client.delete(
        f"/activities/{unknown_activity}/participants",
        params={"email": existing_participant_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_missing_participant(client, existing_activity_name, new_email):
    # Arrange
    missing_email = new_email

    # Act
    response = client.delete(
        f"/activities/{existing_activity_name}/participants",
        params={"email": missing_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_then_signup_allows_reregistration(
    client,
    existing_activity_name,
    existing_participant_email,
):
    # Arrange
    email = existing_participant_email

    # Act
    unregister_response = client.delete(
        f"/activities/{existing_activity_name}/participants",
        params={"email": email},
    )
    signup_response = client.post(
        f"/activities/{existing_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
