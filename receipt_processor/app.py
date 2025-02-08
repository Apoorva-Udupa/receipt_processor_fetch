import uuid
import math
from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)

#store a key-value pair of UUID-points for the each receipt calculated points (as asked in question/requirements, in-memory storing using a simple dictionary)
receipt_pts = {}


#RECEIPT VALIDATION

#checking receipt is valid, if not gives missing field error
def valid_receipt(data):
    #for any of the below fields are missing - error message for 400 BadRequest
    required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
    
    #If no items in the receipt - error message for 400 BadRequest
    if not isinstance(data["items"], list) or len(data["items"]) < 1:
        return "Receipt must have at least one item."

    #for valid receipt
    return None


#POINT CALCULATION
def calc_points(receipt):
    retailer = receipt["retailer"]
    purchase_date = receipt["purchaseDate"]  # YYYY-MM-DD format
    purchase_time = receipt["purchaseTime"]  # HH:MM format 
    total = receipt["total"]
    items = receipt["items"]

    points = 0 #initial points set to 0

    #Rule 1: points for every alphanumeric character in retailer name
    points = points+sum(c.isalnum() for c in retailer)
    try:
        amount = float(total)
    except ValueError:
        amount = 0.0  # Raise ValueError if unable to convert string

    #Rule 2: 50 points if the total is a round dollar amount with no cents.
    if amount.is_integer():
        points = points+50

    #Rule 3: 25 points if the total is a multiple of 0.25.
    if (amount * 100) % 25 == 0:  # multiply by 100 to avoid float precision issues
        points = points+25

    # Rule 4: 5 points for every two items on the receipt.
    numberOfItems = len(items)
    points = points+((numberOfItems // 2) * 5)

    #Rule 5: If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in items:
        desc_char = item["shortDescription"].strip()
        if len(desc_char) % 3 == 0:
            try:
                priceOfItem = float(item["price"])
            except ValueError:
                priceOfItem = 0.0 
            p = math.ceil(priceOfItem * 0.2)
            points += p

    #Rule 6: IGNORED this rule 

    #Rule 7: 6 points if the day in the purchase date is odd.
    try:
        purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
        day = purchase_date.day
        if day % 2 == 1:  
            points = points+6
    except ValueError:
        pass  #ValueError for invalid date format given here

    #Rule 8: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    try:
        purchase_time = datetime.strptime(purchase_time, "%H:%M")
        hour = purchase_time.hour
        if 14 <= hour < 16: #As 2pm is 14:00 hrs ad 4pm is 16:00 hrs
            points += 10
    except ValueError:
        pass  # same for time as above for date

    return points #Return the total calculated points here



#POST METHOD
@app.route("/receipts/process", methods=["POST"])
def process_receipt():
    data = request.get_json()
    #If empty reciept json given 
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400 

    # Validate receipt
    error = valid_receipt(data)
    if error:
        return jsonify({"error": error}), 400

    points = calc_points(data)
    receipt_id = str(uuid.uuid4()) #unique ID
    receipt_pts[receipt_id] = points #store ID-points pair
    return jsonify({"id": receipt_id})



#GET METHOD
@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def get_points(receipt_id):
    
    if receipt_id not in receipt_pts:
        return jsonify({"error": "No receipt found for that ID."}), 404
    return jsonify({"points": receipt_pts[receipt_id]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
