from flask import Flask
from flask import Flask, jsonify, abort, request, make_response, url_for
from app import json_unpacker
from app import matching_model

app= Flask(__name__,static_folder=None)

@app.route("/match", methods=['POST']) #using the post method with /match in the url to get the required app route
def matching():
    if not request.json: #will abort the request if it fails to load the json
        abort(400)  #will have a return status of 400 in case of failure
    bidding_data = json_unpacker.JsonUnpacker(request.json) #calles the json_unpacker to get the necessary bidding_data
    model = matching_model.MatchingModel(bidding_data.student_ids,
                                bidding_data.topic_ids,
                                bidding_data.student_preferences_map,
                                bidding_data.topic_preferences_map, bidding_data.q_S) #model to get the student_ids,topic_ids,student_preference_map,topic_prefernce_map
    return jsonify(model.get_matching()) #returns a json object
