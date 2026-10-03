from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3

app = FastAPI()

# ✅ Enable CORS so frontend (React) can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server / Nginx container
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],  # allow all headers
)

# DynamoDB connection (uses AWS creds from env or IAM role)
dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-1")
table = dynamodb.Table("Habits")

# Root health check
@app.get("/")
def root():
    return {"message": "Habit Tracker API is running"}

@app.get("/habits/{user_id}/{habit_id}")
def get_habit(user_id: str, habit_id: str):
    item = table.get_item(Key={"user_id": user_id, "habit_id": habit_id}).get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Habit not found")
    return item

@app.post("/habits")
def create_habit(habit: dict):
    table.put_item(Item=habit)
    return {"message": "Habit created"}

@app.put("/habits/{user_id}/{habit_id}")
def update_habit(user_id: str, habit_id: str, habit: dict):
    table.update_item(
        Key={"user_id": user_id, "habit_id": habit_id},
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": habit["status"]}
    )
    return {"message": "Habit updated"}

@app.delete("/habits/{user_id}/{habit_id}")
def delete_habit(user_id: str, habit_id: str):
    table.delete_item(Key={"user_id": user_id, "habit_id": habit_id})
    return {"message": "Habit deleted"}
