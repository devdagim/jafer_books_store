from telegram_bot.helpers.db import DB


class ReviewModel:
    def book_avg_rating(self, book_code):
        conn = DB()
        cursor = conn.cursor()

        sql = (
            "SELECT ROUND(AVG(rating),1) FROM book_review WHERE book_code=%s;"
        )
        cursor.execute(sql, (book_code,))

        result = cursor.fetchone()

        # close
        cursor.close()

        return result[0] if result else 0

    def save_review(self, book_code, user_id, rating, review=None):
        conn = DB()
        cursor = conn.cursor()

        if self._is_review_exist(cursor, book_code, user_id):
            sql = "UPDATE book_review SET rating=%s,review=%s WHERE \
                book_code=%s AND user_id=%s"
            cursor.execute(sql, (rating, review, book_code, user_id))

        else:
            sql = "INSERT INTO book_review(book_code, user_id, rating, review) \
            VALUES(%s,%s,%s,%s)"
            cursor.execute(sql, (book_code, user_id, rating, review))

        conn.commit()

        # close
        cursor.close()

    def _is_review_exist(self, cursor, book_code, user_id):
        sql = "SELECT COUNT(*) FROM book_review WHERE book_code=%s AND user_id=%s"
        cursor.execute(sql, (book_code, user_id))
        is_exists = cursor.fetchone()

        return bool(is_exists[0])

    def get_reviews(self, book_code, fetch_limit):
        conn = DB()
        cursor = conn.cursor(dictionary=True)

        start, end = fetch_limit
        sql = "SELECT * FROM book_review WHERE book_code=%s LIMIT %s,%s"
        cursor.execute(sql, (book_code, start, end))

        result = cursor.fetchall()

        # close
        cursor.close()

        return result if result else None

    def total_reviews(self, book_code):
        conn = DB()
        cursor = conn.cursor()

        sql = "SELECT COUNT(*) FROM book_review WHERE book_code=%s"
        cursor.execute(sql, (book_code,))

        result = cursor.fetchone()

        # close
        cursor.close()

        return result[0] if result else 0
