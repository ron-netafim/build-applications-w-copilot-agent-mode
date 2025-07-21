from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Clear existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activity.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # --- USERS ---
        users = [
            {"_id": ObjectId(), "username": "superman", "email": "superman@octofit.com", "password": "krypton123"},
            {"_id": ObjectId(), "username": "wonderwoman", "email": "wonderwoman@octofit.com", "password": "themyscira"},
            {"_id": ObjectId(), "username": "batman", "email": "batman@octofit.com", "password": "alfred"},
            {"_id": ObjectId(), "username": "flash", "email": "flash@octofit.com", "password": "speedforce"},
        ]
        db.users.insert_many(users)

        # --- TEAMS ---
        teams = [
            {"_id": ObjectId(), "name": "Justice League", "members": [users[0]["_id"], users[1]["_id"], users[2]["_id"]]},
            {"_id": ObjectId(), "name": "Speedsters", "members": [users[3]["_id"]]},
        ]
        db.teams.insert_many(teams)

        # --- WORKOUTS ---
        workouts = [
            {"_id": ObjectId(), "name": "Morning Run", "description": "5km run around the school track."},
            {"_id": ObjectId(), "name": "Strength Circuit", "description": "Push-ups, sit-ups, squats, and lunges."},
            {"_id": ObjectId(), "name": "Yoga Flex", "description": "30 minutes of yoga and stretching."},
        ]
        db.workouts.insert_many(workouts)

        # --- ACTIVITIES ---
        activities = [
            {"_id": ObjectId(), "user": users[0]["_id"], "activity_type": "run", "duration": timedelta(minutes=30)},
            {"_id": ObjectId(), "user": users[1]["_id"], "activity_type": "yoga", "duration": timedelta(minutes=45)},
            {"_id": ObjectId(), "user": users[2]["_id"], "activity_type": "strength", "duration": timedelta(minutes=40)},
            {"_id": ObjectId(), "user": users[3]["_id"], "activity_type": "run", "duration": timedelta(minutes=20)},
        ]
        # Convert timedelta to seconds for MongoDB
        for a in activities:
            a["duration"] = int(a["duration"].total_seconds())
        db.activity.insert_many(activities)

        # --- LEADERBOARD ---
        leaderboard = [
            {"_id": ObjectId(), "user": users[0]["_id"], "score": 120},
            {"_id": ObjectId(), "user": users[1]["_id"], "score": 110},
            {"_id": ObjectId(), "user": users[2]["_id"], "score": 100},
            {"_id": ObjectId(), "user": users[3]["_id"], "score": 90},
        ]
        db.leaderboard.insert_many(leaderboard)

        self.stdout.write(self.style.SUCCESS('Test data successfully populated in octofit_db!'))
