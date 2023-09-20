from telegram_bot.helpers.db import DB


class WishlistModel:
    def get_wishlist(self, user_id: int, fetch_limit: tuple):
        cursor = DB.cursor(dictionary=True)
        select_sql = "SELECT b.book_code,b.book_name,b.book_author,b.book_category,\
            b.book_etb_price,b.book_usd_price FROM book b JOIN  wishlist w ON \
            b.book_code=w.book_code WHERE w.user_id=%s LIMIT %s,%s;"
        limit_start, limit_end = fetch_limit
        cursor.execute(select_sql, (user_id, limit_start, limit_end))

        result = cursor.fetchall()

        cursor.close()

        return result if result else {}

    def remove_wishlist(self, user_id: int, book_code):
        cursor = DB.cursor()
        delete_sql = "DELETE FROM wishlist WHERE user_id=%s AND book_code=%s"
        cursor.execute(delete_sql, (user_id, book_code))
        DB.commit()

        cursor.close()

    def get_total_list(self, user_id: int):
        cursor = DB.cursor()
        select_sql = "SELECT COUNT(book_code) FROM wishlist WHERE user_id=%s"
        cursor.execute(select_sql, (user_id,))

        result = cursor.fetchone()

        cursor.close()

        return result[0] if result else 0

    def save_to_wishlist(self, book_code: str, user_id: int):
        cursor = DB.cursor()
        insert_sql = "INSERT INTO wishlist(user_id, book_code) VALUES(%s, %s)\
            ON DUPLICATE KEY UPDATE book_code = VALUES(book_code)"
        cursor.execute(insert_sql, (user_id, book_code))
        DB.commit()

        cursor.close()