from telegram_bot.helpers.db import DB


class PostModel:
    def check_unposted_books(self):
        conn = DB()
        cursor = conn.cursor()

        sql = "SELECT COUNT(book_code) FROM post WHERE book_post_status='0';"
        cursor.execute(sql)

        unposted_books = cursor.fetchall()

        # close
        cursor.close()

        return bool(unposted_books)

    def get_unposted_books(self, fetch_limit):
        conn = DB()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT book.book_code,book_name,book_author,book_etb_price,\
                book_usd_price,book_img_url,book_category,book_language,\
                book_stoke_status FROM book JOIN post ON \
                book.book_code=post.book_code WHERE book_post_status='0'\
                LIMIT %s,%s;"
        cursor.execute(sql, fetch_limit)
        unposted_books = cursor.fetchall()

        # close
        cursor.close()

        return unposted_books

    def get_updated_books(self, fetch_limit):
        conn = DB()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT b.book_code,b.book_name,b.book_author,b.book_etb_price,\
                b.book_usd_price,b.book_img_url,b.book_category,\
                b.book_language,b.book_stoke_status,p.telegram_post_id as \
                post_id FROM book b LEFT JOIN post p ON b.book_code=p.book_code\
                WHERE b.book_content_status='1' LIMIT %s,%s;"
        cursor.execute(sql, fetch_limit)
        updated_books = cursor.fetchall()

        # close
        cursor.close()

        return updated_books

    def updated_books_count(self):
        conn = DB()
        cursor = conn.cursor()

        sql = (
            "SELECT COUNT(book_code) FROM book WHERE book_content_status='1';"
        )
        cursor.execute(sql)

        unposted_books = cursor.fetchone()

        # close
        cursor.close()

        if unposted_books:
            return unposted_books[0]
        else:
            return 0

    def unposted_books_count(self):
        conn = DB()
        cursor = conn.cursor()

        sql = "SELECT COUNT(book_code) FROM post WHERE book_post_status='0';"
        cursor.execute(sql)

        unposted_books = cursor.fetchone()

        # close
        cursor.close()

        if unposted_books:
            return unposted_books[0]
        else:
            return 0

    def save_post(self, post_id, book_code):
        conn = DB()
        cursor = conn.cursor()

        sql = "UPDATE post SET telegram_post_id=%s ,book_post_status='1'\
                WHERE book_code=%s;"
        cursor.execute(sql, (post_id, book_code))
        conn.commit()

        # close
        cursor.close()

    def get_post_id(self, book_code):
        conn = DB()
        cursor = conn.cursor()

        sql = "SELECT telegram_post_id FROM post WHERE book_code=%s"
        cursor.execute(sql, (book_code,))
        result = cursor.fetchone()

        # close
        # cursor.close()

        return result[0] if result else " "

    def update_book_content_status(self, book_code):
        # UPDATE book SET book_content_status='1' WHERE book_code=
        conn = DB()
        cursor = conn.cursor()

        sql = "UPDATE book SET book_content_status='0' WHERE book_code=%s;"
        cursor.execute(sql, (book_code,))
        conn.commit()

        # close
        cursor.close()
