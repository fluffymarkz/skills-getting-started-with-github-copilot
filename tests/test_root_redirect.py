def test_root_redirects_to_static_index(client):
    # Arrange
    target_path = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == target_path
