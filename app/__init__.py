from flask import Flask
from flask import Flask, jsonify, abort, request, make_response, url_for
from app import json_unpacker
from app import matching_model

app= Flask(__name__,static_folder=None)

@app.route("/match", methods=['POST'])
def matching():
    if not request.json:
        abort(400)
    bidding_data = json_unpacker.JsonUnpacker(request.json)
    model = matching_model.MatchingModel(bidding_data.student_ids,
                                bidding_data.topic_ids,
                                bidding_data.student_preferences_map,
                                bidding_data.topic_preferences_map, 2)
    return jsonify(model.get_matching())

if __name__ == "__main__":
    app.run(debug=True)
