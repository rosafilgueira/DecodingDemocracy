from flask import Blueprint, jsonify
from api.db import get_db_connection
from functools import lru_cache # to cache the results of the functions

bp = Blueprint('questions', __name__, url_prefix='/api/questions')

"""
Define routes to handle different types of queries related to questions and word clouds in a consultation.
- For the route '/<int:consultation_id>', retrieve all questions related to a specific consultation ID.
- For the route '/<string:question_id>', retrieve a specific question based on its ID.
- For the route '/wordcloud/<string:question_id>', retrieve the word cloud associated with a specific question ID.
"""

# get all questions for a given consultation
@bp.route('/<int:consultation_id>', methods=['GET'])
@lru_cache(maxsize=32)
def questions(consultation_id):
    conn = get_db_connection()
    c = conn.cursor()    
    c.execute('SELECT id, consultation_id, question, multiplechoice FROM Question WHERE consultation_id = ?', (consultation_id,))
    questions = c.fetchall()           
    return jsonify(questions)

# get a specific question based on its ID
@bp.route('/<string:question_id>', methods=['GET'])
@lru_cache(maxsize=32)
def question(question_id):
    conn = get_db_connection()
    c = conn.cursor()    
    c.execute('SELECT id, consultation_id, question, multiplechoice FROM Question WHERE id = ?', (question_id,))
    question = c.fetchone()    
    conn.close()
    return jsonify(question)

# get the word cloud associated with a specific question ID
@bp.route('/wordcloud/<string:question_id>', methods=['GET'])
@lru_cache(maxsize=32)
def wordcloud(question_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT wordcloud FROM Question WHERE id = ?', (question_id,))
    wordcloud = c.fetchone()
    conn.close()
    return jsonify(wordcloud)
    
    