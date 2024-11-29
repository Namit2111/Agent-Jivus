@app.route("/check-availability", methods=["POST"])
def check_availability():
    global user_token
    if not user_token or "error" in user_token:
        return redirect(url_for("login"))

    data = request.get_json()
    meeting_start = data['message']['toolCalls'][0]['function']['arguments'].get('startDateTime') #format expected: 2024-11-18T16:00:00
    #print(meeting_start)
    meeting_duration = data['message']['toolCalls'][0]['function']['arguments'].get('meetingDuration') #format expected: "30 min" /"1 hr"/"0.5 hr"
    timeZone = data['message']['toolCalls'][0]['function']['arguments'].get('timeZone')
    #time_zones = [# United States
#     "America/New_York",  # UTC-05:00 / UTC-04:00 (Eastern Time)
#     "America/Chicago",   # UTC-06:00 / UTC-05:00 (Central Time)
#     "America/Denver",    # UTC-07:00 / UTC-06:00 (Mountain Time)
#     "America/Phoenix",   # UTC-07:00 (Mountain Time - no DST)
#     "America/Los_Angeles",  # UTC-08:00 / UTC-07:00 (Pacific Time)
#     "America/Anchorage",    # UTC-09:00 / UTC-08:00 (Alaska Time)
#     "Pacific/Honolulu",     # UTC-10:00 (Hawaii Time - no DST)
#
#     # Europe
#     "Europe/London",     # UTC+00:00 (Western Europe Time)
#     "Europe/Berlin",     # UTC+01:00 (Central Europe Time)
#     "Europe/Athens",     # UTC+02:00 (Eastern Europe Time)
#     "Europe/Moscow",     # UTC+03:00 (Moscow Time)
#
#     # Asia
#     "Asia/Jerusalem",    # UTC+02:00 (Israel Time)
#     "Asia/Riyadh",       # UTC+03:00 (Arabian Time)
#     "Asia/Tehran",       # UTC+03:30 (Iran Time)
#     "Asia/Dubai",        # UTC+04:00 (Gulf Time)
#     "Asia/Kabul",        # UTC+04:30 (Afghanistan Time)
#     "Asia/Karachi",      # UTC+05:00 (Pakistan Time)
#     "Asia/Kolkata",      # UTC+05:30 (Indian Standard Time)
#     "Asia/Kathmandu",    # UTC+05:45 (Nepal Time)
#     "Asia/Dhaka",        # UTC+06:00 (Bangladesh Time)
#     "Asia/Rangoon",      # UTC+06:30 (Myanmar Time)
#     "Asia/Bangkok",      # UTC+07:00 (Indochina Time)
#     "Asia/Shanghai",     # UTC+08:00 (China Time)
#     "Asia/Tokyo",        # UTC+09:00 (Japan/Korea Time)
#     "Australia/Darwin",  # UTC+09:30 (Central Australia Time)
#     "Australia/Sydney"   # UTC+10:00 (Eastern Australia Time)
# ]

    # Parse the start time and duration
    start_datetime = datetime.fromisoformat(meeting_start)
    #print(start_datetime)

    # Normalize the duration input to handle variations
    meeting_duration = meeting_duration.lower().replace("minutes", "min").replace("minute", "min").replace("hours", "hr").replace(
        "hour", "hr")

    if meeting_duration.isdigit():
        meeting_duration = f"{meeting_duration} min"

    # Extract the numeric value and time unit using regex
    match = re.match(r"(\d+)\s?(min|hr)", meeting_duration)
    if match:
        value, unit = int(match.group(1)), match.group(2)

        # Add the duration to the start time
        if unit == "min":
            end_datetime = start_datetime + timedelta(minutes=value)
        elif unit == "hr":
            end_datetime = start_datetime + timedelta(hours=value)
        else:
            # Default to 30 minutes if the unit is unrecognized
            end_datetime = start_datetime + timedelta(minutes=30)
    else:
        # Default to 30 minutes if the format is invalid
        end_datetime = start_datetime + timedelta(minutes=30)

    end_datetime = end_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    print(end_datetime)

    tool_calls = data.get('message', {}).get('toolCalls', [])
    tool_call_id = tool_calls[0].get('id', None) if tool_calls else ""

    start_datetime = meeting_start
    end_datetime = end_datetime
    timezone = timeZone
    organizer_email = app_config.ORGANIZER_EMAIL

    availability_endpoint = "https://graph.microsoft.com/v1.0/me/calendar/getschedule"
    headers = {'Authorization': 'Bearer ' + user_token['access_token']}
    payload = {
        "schedules": [organizer_email],
        "startTime": {"dateTime": start_datetime, "timeZone": timezone},
        "endTime": {"dateTime": end_datetime, "timeZone": timezone},
        "availabilityViewInterval": 30
    }

    response = requests.post(availability_endpoint, headers=headers, json=payload).json()
    schedule_info = response['value'][0]
    availability_view = schedule_info.get('availabilityView', '')
    is_free = '0' in availability_view and all(char == '0' for char in availability_view)

    response_value = {
        "results": [
            {
                "toolCallId": tool_call_id,
                "result": "Yes we can have a meeting in this time slot" if is_free else "No this time slot doesn't work for me"
            }
        ]
    }

    return response_value