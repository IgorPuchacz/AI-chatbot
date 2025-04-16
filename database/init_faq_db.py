import sqlite3
import os
import csv


def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'faq.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS faq
                 (question_ID INT PRIMARY KEY, question_group TEXT, question TEXT, answer TEXT, hyperlink TEXT)''')

    csv_path = os.path.join(os.path.dirname(__file__), 'Q&A base.csv')

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # pomijamy nagłówki
        faq_data = [tuple(row) for row in reader if len(row) == 5]

    c.executemany('INSERT OR REPLACE INTO faq VALUES (?, ?, ?, ?, ?)', faq_data)
    conn.commit()
    conn.close()
    print(f"Baza danych zainicjalizowana w: {db_path}")


if __name__ == '__main__':
    init_db()
