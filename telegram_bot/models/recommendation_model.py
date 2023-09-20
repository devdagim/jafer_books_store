from telegram_bot.helpers.db import DB


class RecommendationModel:
    def recommended_books(self, user_id, fetch_limit):
        cursor = DB.cursor(dictionary=True)

        books_rated_by_slimier_book_rater = (
            self._books_rated_by_slimier_book_rater(current_user_id=user_id)
        )
        books_wished_by_slimier_book_wisher = (
            self._books_wished_by_slimier_book_wisher(current_user_id=user_id)
        )
        books_by_user_preference = self._books_by_user_preference(
            current_user_id=user_id
        )

        sql = f"""
        {books_rated_by_slimier_book_rater} UNION 
        {books_wished_by_slimier_book_wisher} UNION 
        {books_by_user_preference} LIMIT %s,%s
        """
        limit_start, end = fetch_limit
        cursor.execute(sql, (limit_start, end))

        result = cursor.fetchall()

        return result if result else None

    def total_recommended_books(self, user_id):
        recommended_books = self.recommended_books(user_id, (0, 100000000000))

        return len(recommended_books)

    def _books_rated_by_slimier_book_rater(self, current_user_id):
        return f"""
        SELECT book_code FROM book_review WHERE user_id IN (
            SELECT user_id FROM book_review WHERE rating > 2 AND book_code IN (
                SELECT book_code FROM book_review WHERE rating > 2 AND user_id={current_user_id}
            )
        )
        """

    def _books_wished_by_slimier_book_wisher(self, current_user_id):
        return f"""
        SELECT book_code FROM wishlist WHERE user_id IN (
            SELECT user_id FROM wishlist WHERE book_code IN (
                SELECT book_code FROM wishlist WHERE user_id={current_user_id}
            )
        )
        """

    def _books_by_user_preference(self, current_user_id):
        return f"""
        SELECT book_code FROM book WHERE book_author IN (
            SELECT author_name FROM author_preference WHERE user_id={current_user_id}
        ) OR book_category IN (
            SELECT category_id FROM genre_preference WHERE user_id={current_user_id}
        )
        """
