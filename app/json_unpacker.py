import json
import operator

class JsonUnpacker:
    """
    Class for unpacking bidding data from JSON Object.

    ATTRIBUTES:

    ----------

    json_dict  :  dict
        The JSON object represented as a python dictionary.

    topic_ids  :  list
        {String, String, ....}
        A list of the topic_ids of all the topics in the assignment.

    student_ids  :  list
        {String, String, ....}
        A list containing all the Student IDs.

    student_preferences_map  :  dict
        {String : [String, String, ....], String : [String, String, ....], ....}
        A dictionary that maps a student ID to a list of topic IDs in the linear
        order of the student's preference.
        key : Student ID
        value : list of topic IDs in the linear order of student's preference.

    topic_preferences_map  :  dict
        {String : [String, String, ....], String : [String, String, ....], ....}
        A dictionary that maps a topic ID to a list of students in the linear
        order of the topic's preference.
        key : Topic ID
        value : list of student IDs in the linear order of topic's preference.
    """
    def __init__(self,data):
        self.json_dict = data
        self.topic_ids = self.json_dict['tids']
        self.student_ids = list(self.json_dict['users'].keys())
        self.student_preferences_map = self.gen_stud_pref_map(self.json_dict)
        self.topic_preferences_map = self.gen_topic_pref_map(self.json_dict)

    def gen_stud_pref_map(self,json_dict):
        student_preferences_map = dict()
        for student_id in self.student_ids:
            chosen_topic_ids = json_dict['users'][student_id]['tid']
            chosen_topic_priorities = json_dict['users'][student_id]['priority']
            student_preferences_map[student_id] = [x for x,_ in
                                                   sorted(zip(chosen_topic_ids,
                                                   chosen_topic_priorities))]
            unchosen_topic_ids = list(set(self.topic_ids).difference(set(
                                 chosen_topic_ids)))
            self_topic = json_dict['users'][student_id]['otid']
            if self_topic in unchosen_topic_ids:
                unchosen_topic_ids.remove(self_topic)
            student_preferences_map[student_id] += unchosen_topic_ids
            student_preferences_map[student_id].append(self_topic)
        return student_preferences_map

    def gen_topic_pref_map(self,json_dict):
        topic_preferences_map = dict()
        for topic_id in self.topic_ids:
            topic_preferences_map[topic_id] = []
            for student_id in self.student_ids:
                if(topic_id in self.student_preferences_map[student_id]):
                    timestamp = max(json_dict['users'][student_id]['time'])
                    topic_priority = self.student_preferences_map[
                                     student_id].index(topic_id)
                    num_chosen_topics = len(json_dict['users'][student_id][
                                        'tid'])
                    topic_preferences_map[topic_id].append((student_id,
                                                    topic_priority,
                                                    num_chosen_topics,
                                                    timestamp))
            topic_preferences_map[topic_id].sort(key = operator.itemgetter(1,2,
                                                 3))
            topic_preferences_map[topic_id] = [x for x,_,_,_ in
                                              topic_preferences_map[topic_id]]
        return topic_preferences_map
