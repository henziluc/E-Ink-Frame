import os
from garminconnect import Garmin
import datetime
from datetime import datetime, date, timedelta
garmin_luca = None
garmin_jojo = None







def get_health_data(health_dict):
    last_updated_luca = health_dict['Luca']['last updated']
    last_updated_jojo = health_dict['Jojo']['last updated']
    
    if len(health_dict['Luca']) == 1:
        request_luca = True
    elif len(health_dict['Jojo']) == 1:
        request_luca = False
    if last_updated_luca <= last_updated_jojo:
        request_luca = True
    else:
        request_luca = False
    
    
    if request_luca and datetime.now() - last_updated_luca >= timedelta(minutes=55):
        print("Fetching health data for Luca")
        luca_data = load_health_data(os.getenv("garmin_mail"), os.getenv("garmin_password"), 'Luca')
        jojo_data = health_dict['Jojo']
    elif not request_luca and datetime.now() - last_updated_jojo >= timedelta(minutes=55):
        print("Fetching health data for Jojo")
        luca_data = health_dict['Luca']
        jojo_data = load_health_data(os.getenv("garmin_mail_jojo"), os.getenv("garmin_password_jojo"), 'Jojo')

        
    
    health_dict = {
        "Luca": luca_data,
        "Jojo": jojo_data
    }
    
    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    
    return health_dict, formatted_datetime

def load_health_data(email=None, password=None, person=None):
    garmin_luca = None
    garmin_jojo = None
    today = date.today()
        
    if person == "Luca":
        if garmin_luca is None:
            garmin_luca = Garmin(email, password)
            garmin_luca.login()

        client = garmin_luca

    elif person == "Jojo":
        if garmin_jojo is None:
            garmin_jojo = Garmin(email, password)
            garmin_jojo.login()

        client = garmin_jojo
    
    # Steps
    steps_data = client.get_daily_steps(today.isoformat(), today.isoformat())
    steps = steps_data[0]["totalSteps"]
    step_goal = steps_data[0]["stepGoal"]
    
    # Body Battery
    body_battery_data = client.get_body_battery(today.isoformat(), today.isoformat())
    body_battery = body_battery_data[0]["bodyBatteryValuesArray"][-1][1]
    
    # Sleep
    sleep_data = client.get_sleep_daily(today.isoformat(), today.isoformat())
    sleep = sleep_data[0]["values"]

    sleep_seconds = sleep["totalSleepTimeInSeconds"]
    sleep_hours = sleep_seconds / 3600

    resting_hr = sleep["restingHeartRate"]
    sleep_score = sleep["sleepScore"]
    
    # Activities
    activity_data = client.get_activities(0,1)
    activity = activity_data[0]

    activity_type = activity.get("activityType", {}).get("typeKey")
    activity_distance = activity.get("distance")
    if activity_distance == 0:
        activity_distance = None
    activity_duration = activity.get("duration")
    activity_aerobic_effect = activity.get("aerobicTrainingEffect")
    activity_anaerobic_effect = activity.get("anaerobicTrainingEffect")
    activity_calories = activity.get("calories")
    activity_speed = activity.get("averageSpeed")

    activity_pace = speed_to_pace(activity_speed) if activity_speed else None
     
    intensity_minutes = client.get_weekly_intensity_minutes(today.isoformat(), today.isoformat())
    intensity_minutes = intensity_minutes[0]
    intensity_minutes_goal = intensity_minutes['weeklyGoal']
    intensity_minutes = intensity_minutes['moderateValue'] + intensity_minutes['vigorousValue'] * 2
    
    stress_data = client.get_all_day_stress(today.isoformat())
    stress_data = stress_data['avgStressLevel']


    now = datetime.now()
    
    
    healt_dict = {
        "last updated": now,
        "steps": steps,
        "step_goal": step_goal,
        "body_battery": body_battery,
        "sleep_hours": sleep_hours,
        "resting_hr": resting_hr,
        "sleep_score": sleep_score,
        "intensity_minutes": intensity_minutes,
        "intensity_minutes_goal": intensity_minutes_goal,
        "stress": stress_data,
        "activity_type": activity_type,
        "activity_distance": activity_distance,
        "activity_duration": activity_duration,
        "activity_aerobic_effect": activity_aerobic_effect,
        "activity_anaerobic_effect": activity_anaerobic_effect,
        "activity_calories": activity_calories,
        "activity_speed": activity_speed,
        "activity_pace": activity_pace
    }
    
    return healt_dict

def speed_to_pace(speed):
    pace_seconds = 1000 / speed
    minutes = int(pace_seconds // 60)
    seconds = int(pace_seconds % 60)

    return f"{minutes}:{seconds:02d}"