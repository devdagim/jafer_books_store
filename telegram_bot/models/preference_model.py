from telegram_bot.helpers.db import DB
from telegram_bot.models.book_model import BookModel


class PreferenceModel:
    book_model = BookModel()

    def is_set_preference(self, user_id, preference_type):
        conn = DB()
        cursor = conn.cursor()

        if preference_type == "author":
            sql = "SELECT COUNT(*) FROM author_preference WHERE user_id=%s"
        elif preference_type == "genre":
            sql = "SELECT COUNT(*) FROM genre_preference WHERE user_id=%s"

        cursor.execute(sql, (user_id,))

        result = cursor.fetchone()

        return bool(result[0])

    # tempo_author_id is the author_id alone side with book_id(it uses the book id)
    def _is_preference_exist(self, user_id, id, preference_type):
        conn = DB()
        cursor = conn.cursor()

        if preference_type == "author":
            sql = "SELECT COUNT(*) FROM author_preference WHERE user_id=%s \
                AND author_name=%s"
            author_name = self.book_model.get_author_by_book_id(id)
            second_arg = author_name

        elif preference_type == "genre":
            sql = "SELECT COUNT(*) FROM genre_preference WHERE user_id=%s \
                AND category_id=%s"
            category_id = id
            second_arg = category_id

        cursor.execute(sql, (user_id, second_arg))

        result = cursor.fetchone()

        cursor.close()

        return bool(result[0])

    def save_preference(self, user_id, id, preference_type):
        conn = DB()
        cursor = conn.cursor()

        is_preference_exist = self._is_preference_exist(
            user_id, id, preference_type
        )

        if not is_preference_exist:
            if preference_type == "author":
                sql = "INSERT INTO author_preference(user_id,author_name) VALUES(%s,%s)"
                author_name = self.book_model.get_author_by_book_id(id)
                cursor.execute(sql, (user_id, author_name))
            elif preference_type == "genre":
                sql = "INSERT INTO genre_preference(user_id,category_id) VALUES(%s,%s)"
                cursor.execute(sql, (user_id, id))

            conn.commit()

        cursor.close()

    def remove_preference(self, user_id, pref_id, preference_type):
        conn = DB()
        cursor = conn.cursor()

        if preference_type == "author":
            sql = (
                "DELETE FROM author_preference WHERE user_id=%s AND pref_id=%s"
            )
        elif preference_type == "genre":
            sql = (
                "DELETE FROM genre_preference WHERE user_id=%s AND pref_id=%s"
            )

        cursor.execute(sql, (user_id, pref_id))
        conn.commit()

        cursor.close()

    def get_pref_id_by_author_name(self, user_id, author_name):
        conn = DB()
        cursor = conn.cursor()

        sql = "SELECT pref_id FROM author_preference WHERE user_id=%s AND author_name=%s"
        cursor.execute(sql, (user_id, author_name))

        result = cursor.fetchone()

        # close
        cursor.close()

        return result[0] if result else None

    def get_pref_id_by_category_id(self, user_id, category_id):
        conn = DB()
        cursor = conn.cursor()

        sql = "SELECT pref_id FROM genre_preference WHERE user_id=%s AND category_id=%s"
        cursor.execute(sql, (user_id, category_id))

        result = cursor.fetchone()

        # close
        cursor.close()

        return result[0] if result else None

    def get_preferred_authors(self, user_id):
        conn = DB()
        cursor = conn.cursor()

        sql = "SELECT pref_id,author_name FROM author_preference WHERE user_id=%s"
        cursor.execute(sql, (user_id,))

        authors = cursor.fetchall()

        # close
        cursor.close()

        return authors

    def get_preferred_genres(self, user_id):
        conn = DB()
        cursor = conn.cursor()

        sql = "SELECT category_id FROM genre_preference WHERE user_id=%s"
        cursor.execute(sql, (user_id,))

        authors = cursor.fetchall()

        # close
        cursor.close()

        return authors
