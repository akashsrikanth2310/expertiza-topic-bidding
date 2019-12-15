import math
import random
import json

class Topic:
    """
    Base class for Assignment Topics

    ATTRIBUTES:

    ----------

    model  :  MatchingModel
        The parent matching model according to whose rules the matching will be
        done.

    id  :  String
        The topic ID corresponding to the topic.

    preferences  :  list
        {String, String, ....}
        List of student IDs in the linear order of the topic's preference.

    current_proposals  :  list
        {String, String, ....}
        The list of student_ids to which the topic has proposed in the current
        step. Initially empty.

    accepted_proposals  :  list
        {String, String, ....}
        The list of student_ids who have accepted the topic's proposal so far.
        Initially empty.

    last_proposed  :  Integer
        The position of the student_id in the topic's preference list to which
        the topic has last proposed. Initialized to -1.

    num_remaining_slots  :  Integer
        Number of students the topic can still be assigned to. Or equivalently,
        number of students the topic can still propose to. Initially
        model.p_ceil.
    """

    current_proposals = []
    accepted_proposals = []
    last_proposed = -1

    def __init__(self,model,id,preferences):
        self.id = id
        self.preferences = preferences
        self.model = model
        self.num_remaining_slots = self.model.p_ceil

    def propose(self,num):
        """
        Proposes to accept 'num' number of Students it has not yet proposed to,
        or proposes to accept all the Students it has not yet proposed to if
        they are less in number than 'num'.
        """
        if(self.last_proposed+num <= len(self.preferences)-1):
            self.current_proposals = self.preferences[self.last_proposed + 1
            :self.last_proposed+num+1]
            self.last_proposed = self.last_proposed + num
        else:
            self.current_proposals = self.preferences[self.last_proposed + 1
            :len(self.preferences)]
            self.last_proposed = len(self.preferences)-1
        for student_id in self.current_proposals:
            self.model.get_student_by_id(student_id).receive_proposal(self.id)

    def acknowledge_acceptance(self,student_id):
        """
        Acknowledges acceptance of proposal by a student.
        """
        self.accepted_proposals.append(student_id)
        self.num_remaining_slots -= 1

    def done_proposing(self):
        '''
        Returns a boolean indicating whether the topic has proposed to all the
        students in its preference list.
        '''
        return (self.last_proposed >= len(self.preferences)-1)

    def slots_left(self):
        '''
        Returns a boolean indicating whether the topic has any slots left in its
        quota of students.
        '''
        return self.num_remaining_slots > 0

class Student:
    """
    Base class for Review Participants ie., Students.

    ATTRIBUTES:

    ----------

    model  :  MatchingModel
        The parent matching model according to whose rules the matching will be
        done.

    id  :  String
        The Student ID corresponding to the student.

    preferences  :  list
        {String, String, ....}
        List of topic IDs in the linear order of the student's preference.

    current_proposals  :  list
        {String, String, ....}
        The list of topic_ids who have proposed to the student in the current
        step. Initially empty.

    accepted_proposals  :  list
        {String, String, ....}
        The list of topic_ids whose proposals the student has accepted so far.
        Initially empty.

    num_remaining_slots  :  Integer
        The number of topics the student can be still assigned.
        Initially model.q_S.
    """
    current_proposals = []
    accepted_proposals = []

    def __init__(self,model,id,preferences):
        self.model = model
        self.id = id
        self.preferences = preferences
        self.num_remaining_slots = self.model.q_S

    def receive_proposal(self,topic_id):
        """
        Receives Proposal from a topic.
        """
        self.current_proposals.append(topic_id)

    def accept_proposals(self):
        """
        Accepts no more than k = num_remaining_slots proposals according to
        their preferences, rejecting the rest.
        """
        self.current_proposals = list(set(self.current_proposals))
        self.current_proposals.sort(key=lambda x: self.preferences.index(x))
        self.accepted_proposals = self.accepted_proposals + \
                        self.current_proposals[:min(len(self.current_proposals),
                        max(self.num_remaining_slots,0))]
        self.current_proposals = []
        for topic_id in self.accepted_proposals:
            self.model.get_topic_by_id(topic_id).acknowledge_acceptance(self.id)
        self.num_remaining_slots -= len(self.accepted_proposals)

class MatchingModel:
    """
    Base Class for the Many-to-Many Matching Problem/Model

    ATTRIBUTES:

    ----------

    student_ids  :  list
        {String, String, ....}
        A list containing all the Student IDs.

    topic_ids  :  list
        {String, String, ....}
        A list containing all the Topic IDs.

    students  :  list
        {Student, Student, ....}
        A list containing objects of the 'Student' class, corresponding to the
        student IDs in student_ids.

    topics  :  list
        {Topic, Topic, ....}
        A list containing objects of the 'Topic' class, corresponding to the
        topic IDs in topic_ids.

    q_S  :  Integer
        Number of topics a student must be assigned.

    num_students  :  Integer
        Total number of students.

    num_topics  :  Integer
        Total number of topics in the assignment.

    p_floor  :  Integer
        Floor of average number of students assigned each topic.

    p_ceil  :  Integer
        Ceil of average number of students assigned each topic.
    """
    def __init__(self,student_ids,topic_ids,student_preferences_map,
                topic_preferences_map,q_S):

        self.student_ids = student_ids
        self.topic_ids = topic_ids
        self.q_S = q_S
        self.num_students = len(self.student_ids)
        self.num_topics = len(self.topic_ids)
        self.p_floor = math.floor(self.num_students * q_S/self.num_topics)
        self.p_ceil = math.ceil(self.num_students * q_S/self.num_topics)
        self.students = list(map(lambda student_id: Student(self,student_id,
                        student_preferences_map[student_id]), student_ids))
        self.topics = list(map(lambda topic_id: Topic(self,topic_id,
                        topic_preferences_map[topic_id]), topic_ids))

    def get_student_by_id(self,student_id):
        """
        Returns Student object corresponding to the given student_id.
        """
        student_id_index = self.student_ids.index(student_id)
        return self.students[student_id_index]

    def get_topic_by_id(self,topic_id):
        """
        Returns Topic object corresponding to the given topic_id.
        """
        topic_id_index = self.topic_ids.index(topic_id)
        return self.topics[topic_id_index]

    def stop_condition(self):
        """
        Returns a boolean indicating whether the stop condition to the algorithm
        has been met.
        """
        flag = True
        for topic in self.topics:
            if (topic.slots_left()):
                if not topic.done_proposing():
                    flag = False
                    break
        return flag

    def get_matching(self):
        """
        Runs the Many-to-Many matching algorithm on the students and students
        according to the specified quotas and returns a stable matching.

        RETURNS:

        -------

        matching  :  dict
            {String : list of Strings, String : list of Strings, ....}
            key:    Student ID
            value:  List of topic IDs corresponding to the topics assigned to
                    the student.

        """

        #   Highly Recommended: Read the algorithm in the wiki page to better
        #   understand the following code.
        #   Wiki Link: http://wiki.expertiza.ncsu.edu/index.php/CSC/ECE_517_Fall_2019_-_E1986._Allow_reviewers_to_bid_on_what_to_review

        #   Step 1: Each topic proposes to accept the first p_ceil students in
        #   its preference list.
        #   Each student accepts no more than q_S proposals according to their
        #   preferences, rejecting the rest.
        for topic in self.topics:
            topic.propose(self.p_ceil)

        for student in self.students:
            student.accept_proposals()

        #   Step k: Each course that has z < p_ceil students proposes to accept
        #   p_ceil - z students it has not yet proposed to.
        #   Each student accepts no more than qS proposals according to their
        #   preferences, rejecting the others.
        #   The algorithm stops when every topic that has not reached the
        #   maximum quota p_ceil has proposed acceptance to every student.
        while(self.stop_condition() == False):
            for topic in self.topics:
                topic.propose(num = topic.num_remaining_slots)

            for student in self.students:
                student.accept_proposals()
        #   Return a dictionary that represents the resultant stable matching.
        matching = dict()
        for student in self.students:
            matching[student.id] = student.accepted_proposals
        return matching
