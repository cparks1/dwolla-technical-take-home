from flask import Flask, jsonify, request
from datetime import datetime, timezone, timedelta
from common.common import get_env_bool

app = Flask(__name__)


def is_valid_timezone_format(timezone_str: str) -> bool:
    """
    Checks if the provided string represents a valid timezone offset format.

    Args:
        timezone_str: String representing the timezone offset (e.g., "+07:00" or "-05:30").

    Returns:
        True if the format is valid, False otherwise.
    """
    if not timezone_str:
        return False

    try:
        offset_hours = int(timezone_str[:3])
        offset_minutes = int(timezone_str[4:])
        # Check for valid hour and minute range
        if abs(offset_hours) > 14 or abs(offset_minutes) > 59:
            return False
        return True
    except (IndexError, ValueError):
        return False


def calculate_timezone_offset(timezone_str: str) -> timedelta:
    """
    Calculates the timedelta object representing the provided timezone offset.

    Args:
        timezone_str: String representing the timezone offset (e.g., "+07:00" or "-05:30").

    Returns:
        timedelta object representing the timezone offset.
    """
    offset_hours = int(timezone_str[:3])
    offset_minutes = int(timezone_str[4:])
    return timedelta(hours=offset_hours, minutes=offset_minutes)


def datetime_to_requested_string_format(datetime_in: datetime, delta: str = None) -> str:
    """
    Returns the datetime in the format requested for this take home assessment,
    which is UTC format: "2050-01-24T15:06:26Z" for UTC times, and
    ex: "2050-01-24T15:06:26-04:00" for times that are UTC offsets

    Args:
        datetime_in: datetime object representing a date and time
        delta: string representing the timezone delta (ex: -04:00 or +13:00)

    Returns:
        string representing the datetime in the requested format
    """
    ret = datetime_in.strftime("%Y-%m-%dT%H:%M:%S")
    if delta is None:
        return ret + "Z"
    return ret + delta


@app.errorhandler(404)
def error_handler_404(_):
    return '', 404


@app.errorhandler(405)
def error_handler_405(_):
    return '', 405


@app.route("/time", methods=['GET'])
def get_current_time():
    current_time_utc = datetime.now(timezone.utc)

    # Prepare response object
    response = {
        "error": None,
        "currentTime": datetime_to_requested_string_format(current_time_utc)
    }

    # Check if timezone parameter is provided
    timezone_offset = request.args.get("timezone")
    if timezone_offset:
        if not is_valid_timezone_format(timezone_offset):
            return jsonify({"error": "Invalid timezone format. Use format '+/-HH:MM'"}), 400

        try:
            timezone_delta = calculate_timezone_offset(timezone_offset)
            adjusted_time = current_time_utc + timezone_delta
            response["adjustedTime"] = datetime_to_requested_string_format(adjusted_time, timezone_offset)
        except (ValueError, Exception) as e:
            print(e)  # If this was paid work, I'd have this running to a logging system
            return jsonify({"error": "Internal server error"}), 500

    return jsonify(response)


if __name__ == "__main__":
    debug_mode = get_env_bool("DEBUG_MODE", default=True)
    app.run(debug=debug_mode)
