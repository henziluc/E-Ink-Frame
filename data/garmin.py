import os
from garminconnect import Garmin
import datetime
from datetime import datetime, date
garmin_luca = None
garmin_jojo = None







def get_health_data(health_dict):
    if health_dict['Luca'] is None:
        request_luca = True
    elif health_dict['Jojo'] is None:
        request_luca = False
    if health_dict['Luca']['last_updated'] < health_dict['Jojo']['last_updated']:
        request_luca = True
    else:
        request_luca = False
    
    
    if request_luca:
        print("Fetching health data for Luca")
        luca_data = load_health_data(os.getenv("garmin_mail"), os.getenv("garmin_password"), 'Luca')
        jojo_data = health_dict['Jojo']
    else:
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
    activity_duration = activity.get("duration")
    activity_aerobic_effect = activity.get("aerobicTrainingEffect")
    activity_anaerobic_effect = activity.get("anaerobicTrainingEffect")
    activity_calories = activity.get("calories")
    activity_speed = activity.get("averageSpeed")

    activity_pace = speed_to_pace(activity_speed) if activity_speed else None
     
    intensity_minutes = client.get_weekly_intensity_minutes(today.isoformat(), today.isoformat())
    print(f"Intensity minutes for {person}: {intensity_minutes}")
    stress_data = client.get_weekly_stress(today.isoformat(), 1)
    print(f"Weekly stress for {person}: {stress_data}")
    training_readiness_data = client.get_training_readiness(today.isoformat())
    print(f"Training readiness for {person}: {training_readiness_data}")
    training_status_data = client.get_training_status(today.isoformat())
    print(f"Training status for {person}: {training_status_data}")
    training_load_data = client.get_training_load_data(today.isoformat())
    print(f"Training load for {person}: {training_load_data}")
    vo2_max_data = client.get_max_metrics(today.isoformat())
    print(f"VO₂ Max for {person}: {vo2_max_data}")

    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    
    healt_dict = {
        "last_updated": formatted_datetime,
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