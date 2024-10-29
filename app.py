from flask import Flask, request, jsonify
from pymongo import MongoClient
import cloudinary
import cloudinary.uploader
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection
mongo_uri = "mongodb+srv://contactzcsco:Z3r0c0575k1ll%4066202@zcsproduction.zld0i.mongodb.net/?retryWrites=true&w=majority&appName=ZCSProduction"
client = MongoClient(mongo_uri)
db = client["NCCDatabase"]
collection = db["cadets"]

# Cloudinary configuration
cloudinary.config( 
    cloud_name = "dxevrrj4j", 
    api_key = "853367529692421", 
    api_secret = "qmkkPh2MEoQCSJ2OLfHeQbaYVFk",  
    secure=True
)

# Helper function to upload image to Cloudinary
def upload_image_to_cloudinary(image_file):
    upload_result = cloudinary.uploader.upload(image_file)
    return upload_result["secure_url"]

# Route to add a new cadet profile
@app.route('/add_cadet', methods=['POST'])
def add_cadet():
    try:
        data = request.form
        name = data.get("name")
        cadet_id = data.get("cadet_id")
        rank = data.get("rank")
        year = data.get("year")
        location = data.get("location")
        achievements = data.get("achievements")
        image_file = request.files.get("profile_picture")

        if image_file:
            image_url = upload_image_to_cloudinary(image_file)
        else:
            return jsonify({"error": "Profile picture is required"}), 400

        cadet_profile = {
            "name": name,
            "cadet_id": cadet_id,
            "rank": rank,
            "year": year,
            "location": location,
            "achievements": achievements,
            "profile_picture": image_url
        }

        collection.insert_one(cadet_profile)
        return jsonify({"message": "Cadet profile added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to retrieve cadet profile by cadet_id
@app.route('/get_cadet/<cadet_id>', methods=['GET'])
def get_cadet(cadet_id):
    cadet_profile = collection.find_one({"cadet_id": cadet_id})
    if cadet_profile:
        cadet_profile["_id"] = str(cadet_profile["_id"])
        return jsonify(cadet_profile), 200
    else:
        return jsonify({"error": "Cadet not found"}), 404

if __name__ == '__main__':
    print("Server is running and MongoDB connection is OK")
    app.run(host="0.0.0.0", port=5000, debug=False)
