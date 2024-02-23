from storage import DictItem, Database

class Service:
    def __init__(self, db: Database):
        self.db = db
        self.username = "unknown"

    def add_new_word(self, topic, word, meaning, pos):
        new_item = DictItem(topic=topic, word=word, meaning=meaning, pos=pos)
        new_item.validate_input()

        self.db.add_new_word(self.username, new_item)

    def get_sorted_topics(self):
        topics = self.db.get_topic_names(self.username)
        return list(sorted(topics))

    # Filter words by specific topic
    def get_words_by_topic(self, topic):
        return self.db.get_words(self.username, topic)

    #Settings for goal
    def update_goal(self, new_goal):
        settings = self.db.get_settings(self.username)
        settings["goal"] = new_goal
        self.db.update_settings(self.username, settings)

    def get_progress(self):
        settings = self.db.get_settings(self.username)
        goal = int(settings.get("goal", 0))

        words_learned = 0
        for topic in self.db.get_topic_names(self.username):
            words_learned += len(self.db.get_words(self.username, topic))
        return words_learned, goal
