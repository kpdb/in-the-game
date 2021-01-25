from in_the_game.users import repository


def test_get_user_profile_data(test_app, monkeypatch):
    test_profile_data = {
        "id": 1,
        "user_id": 1,
        "is_active": True,
        "firstname": "Janko",
        "lastname": "Walski",
        "country_code": "pl",
        "has_weekly_notifications": True,
        "has_daily_notifications": False,
        "has_live_notifications": False,
        "notification_email": "aaa@bbb.pl",
        "notification_url": None,
    }

    async def mock_get_user_profile(user_profile_id):
        return test_profile_data

    monkeypatch.setattr(repository, "get_user_profile", mock_get_user_profile)

    response = test_app.get("/users/1/profile/")
    assert response.status_code == 200
    assert response.json()["firstname"] == test_profile_data["firstname"]


# def test_update_user_profile_data(test_app, monkeypatch):

