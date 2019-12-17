import json

with open('input.json') as json_file:
    data = JsonUnpacker(json.loads(json_file))
model = matching_model.MatchingModel(bidding_data.student_ids,
                        bidding_data.topic_ids,
                        bidding_data.student_preferences_map,
                        bidding_data.topic_preferences_map, bidding_data.q_S)
with open('output.json') as json_file:
    json.dump(model.get_matching(),json_file)
