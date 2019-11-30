import math

class MatchingModel:
    '''
    Base Class for the Many-to-Many Matching Problem/Model
    '''
    def __init__(self,students,topics,student_topic_map,student_preferences_map,student_timestamps_map,topic_preferences_map,q_S,q_T):
        '''

        PAREMETERS:

        ----------

        students  :  list of Strings
            A list containing all the Student IDs (order irrelevant).

        topics  :  list of Strings
            A list containing all the Topic IDs (order irrelevant).

        student_topic_map  :  dict
            {String : String, String : String, ....}
            key:   Student ID
            value: Topic ID of the topic the student is working on.

        student_preferences_map  :  dict
            {String : list of Strings, String : list of Strings, ....}
            key:    Student ID
            value:  List of topic IDs in the linear order of the student's preference.

        student_timestamps_map  :  dict
            {String : Integer, String : Integer, ....}
            key:    Student ID
            value:  Difference in seconds between the time the preferences of the student were updated and the beginning of unix time.

        topic_preferences_map  :  dict
            {String : list of Strings, String : list of Strings, ....}
            key:    Topic ID
            value:  List of student IDs in the linear order of the topic's preference.

        q_S  :  Integer
            Number of topics a student must be assigned.

        q_T  :  Integer
            Number of students a topic must be assigned to.

        '''
        self.students = students
        self.topics = topics
        self.student_topic_map = student_topic_map
        self.student_preferences_map = student_preferences_map
        self.student_timestamps_map = student_timestamps_map
        self.topic_preferences_map = topic_preferences_map
        self.q_S = q_S
        self.q_C = q_C
        self.num_students = len(self.students)
        self.num_topics = len(self.topics)
        self.p_floor = math.floor(num_students * q_S/num_topics)
        self.p_ceil = math.ceil(num_students * q_S/num_topics)

    def num_students():
        return

    def num_topics():
        return len(self.topics)

    def p_floor()


    def get_matching():
        '''

        RETURNS:

        -------

        matching  :  dict
            {String : list of Strings, String : list of Strings, ....}
            key:    Student ID
            value:  List of topic IDs corresponding to the topics assigned to the student.

        '''
        return matching
