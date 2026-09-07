import os
from garminconnect import Garmin
import datetime


def get_health_data():
     
    
    health_dict = {
        "Luca": load_health_data(os.getenv("garmin_mail"), os.getenv("garmin_password")),
        "Jojo": load_health_data(os.getenv("garmin_mail_jojo"), os.getenv("garmin_password_jojo"))
    }
    
    return health_dict

def load_health_data(email=None, password=None):
    today = datetime.date.today()
        
    client = Garmin(email, password)
    client.login()
    
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
    activity_duration = activity.get("duration")
    activity_aerobic_effect = activity.get("aerobicTrainingEffect")
    activity_anaerobic_effect = activity.get("anaerobicTrainingEffect")
    activity_calories = activity.get("calories")
    activity_speed = activity.get("averageSpeed")

    activity_pace = speed_to_pace(activity_speed) if activity_speed else None
        
        
    healt_dict = {
        "steps": steps,
        "step_goal": step_goal,
        "body_battery": body_battery,
        "sleep_hours": sleep_hours,
        "resting_hr": resting_hr,
        "sleep_score": sleep_score,
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