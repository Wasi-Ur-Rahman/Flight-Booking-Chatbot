from typing import Any, Dict
from fastapi import Body, FastAPI
from pydantic import BaseModel
import logging

app = FastAPI()

class Intent(BaseModel):
    displayName: str

class Request(BaseModel):
    intent: Intent
    parameters: Dict[str, Any]

# Define the flight options
flight_options = [
    {"departure": "1:00 PM", "arrival": "2:00 PM"},
    {"departure": "2:00 PM", "arrival": "3:00 PM"},
    {"departure": "12:00 PM", "arrival": "1:00 PM"},
]

def handle_flight(date_from: str):
    options_text = "\n".join([f"{i+1}. Departure: {option['departure']}, Arrival: {option['arrival']}" for i, option in enumerate(flight_options)])
    return f"We found {len(flight_options)} available flights for your dates and budget. Here are the options:\n{options_text}\nPlease select your preferred option by typing 1, 2, or 3"

def handle_flight_selection(selected_option: int):
    if 1 <= selected_option <= len(flight_options):
        selected_flight = flight_options[selected_option - 1]
        return f"You have selected the flight with Departure: {selected_flight['departure']} and Arrival: {selected_flight['arrival']}. Thank you for choosing our service!"
    else:
        return "Invalid selection. Please select a valid flight by typing 1, 2, or 3."

HANDLERS = {
    "FlightBooking": handle_flight,
    "FlightSelection": handle_flight_selection,
}

@app.post("/")
async def home(queryResult: Request = Body(..., embed=True)):
    intent = queryResult.intent.displayName
    parameters = queryResult.parameters
    logging.info(f"Incoming request - Intent: {intent}, Parameters: {parameters}")
    if handler := HANDLERS.get(intent):
        if intent == "FlightSelection":
            text = handler(int(queryResult.parameters["selected_option"]))
        else:
            text = handler(queryResult.parameters)
        logging.info(f"Chatbot response: {text}")
    else:
        text = "I'm not sure how to help with that"

    return {"fulfillmentText": text}