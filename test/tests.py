from datetime import (
    datetime,
    timezone,
    timedelta
)
import pytest

from main import (
    app,
    calculate_timezone_offset,
    is_valid_timezone_format,
    datetime_to_requested_string_format
)


@pytest.fixture()
def test_app():
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


@pytest.fixture()
def runner(test_app):
    return test_app.test_cli_runner()


def test_is_valid_timezone_format():
    assert is_valid_timezone_format("-04:00") is True
    assert is_valid_timezone_format("-4:00") is False
    assert is_valid_timezone_format("-:00") is False
    assert is_valid_timezone_format("-00") is False
    assert is_valid_timezone_format("-0") is False
    assert is_valid_timezone_format("-") is False
    assert is_valid_timezone_format("-04:99") is False
    assert is_valid_timezone_format("-14:99") is False
    assert is_valid_timezone_format("-14:00") is True
    assert is_valid_timezone_format("-15:00") is False


def test_calculate_timezone_offset():
    assert calculate_timezone_offset("+04:00") == timedelta(hours=4, minutes=0)
    assert calculate_timezone_offset("-04:00") == timedelta(hours=-4, minutes=0)
    assert calculate_timezone_offset("+03:30") == timedelta(hours=3, minutes=30)
    assert calculate_timezone_offset("-03:30") == timedelta(hours=-3, minutes=30)


def test_404(client):
    response = client.get("")
    assert response.text == ""
    assert response.status_code == 404


def test_405(client):
    response = client.post("/time")
    assert response.text == ""
    assert response.status_code == 405


def test_time_no_params(client):
    response = client.get("/time")
    current_time_utc = datetime.now(timezone.utc)
    response_current_time = response.json.get("currentTime")
    assert response_current_time == datetime_to_requested_string_format(current_time_utc)


def test_time_bad_params(client):
    response = client.get("/time?timezone=incorrect-timezone-offset")
    response_json = response.json
    assert response_json.get("error") is not None
    assert response.status_code == 400


def test_time_good_params(client):
    response = client.get("/time?timezone=-04:00")
    current_time_utc = datetime.now(timezone.utc)
    response_json = response.json
    assert response_json.get("currentTime") == datetime_to_requested_string_format(current_time_utc)
    assert response_json.get("adjustedTime") == datetime_to_requested_string_format(
        current_time_utc + calculate_timezone_offset("-04:00"), "-04:00")
