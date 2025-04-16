import sqlite3
import numpy as np
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class ActionAnswerFAQ(Action):

    # Name of the action recognised by RASA
    def name(self):
        return "action_answer_faq"

    # Calculates embeddings for each question from FAQ
    def __init__(self):
        super().__init__()

        # 1. connect with database
        self.conn = sqlite3.connect("database/faq.db")
        self.cursor = self.conn.cursor()

        # 2. Get all the records from database
        rows = self.cursor.execute("""
            SELECT question_ID, question_group, question, answer, hyperlink 
            FROM faq
        """).fetchall()
        self.questions = []
        self.answers = []
        self.hyperlinks = []
        self.question_groups = []

        # 3. Save values into separate lists
        for row in rows:
            # row = (question_ID, question_group, question, answer, hyperlink)
            q_id, q_group, q_text, ans, link = row
            self.questions.append(q_text)
            self.answers.append(ans)
            self.hyperlinks.append(link)
            self.question_groups.append(q_group)

        # 4. Load model SentenceTransformer
        #    TODO Currently used multilingual  model paraphrase for test purpose
        #    TODO Sample polish model to use in the future: 'sdadas/st-polish-paraphrase'
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

        # 5. Calculate embeddings for each question
        self.question_embeddings = self.model.encode(self.questions)

    # Tries to answer the asked question
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):

        # Gets message from user
        user_message = tracker.latest_message.get('text', '')

        # Sanitize input
        if not user_message:
            dispatcher.utter_message(response="utter_fallback")
            return []

        # Calculate user's question embedding
        user_embedding = self.model.encode([user_message])

        # Compare embeddings
        similarities = cosine_similarity(user_embedding, self.question_embeddings)[0]

        # Get the most similar question
        best_index = np.argmax(similarities)
        best_similarity = similarities[best_index]

        # Confidence threshold
        threshold = 0.65

        if best_similarity >= threshold:
            # FAQ based answer
            best_answer = self.answers[best_index]
            best_hyperlink = self.hyperlinks[best_index]
            dispatcher.utter_message(text=f"{best_answer}\n\nWięcej info: {best_hyperlink}")
        else:
            # Fallback - confidence didn't met requirements
            dispatcher.utter_message(response="utter_fallback")

        return []
