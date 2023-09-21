from telegram_bot.helpers.db import DB


class BookModel:
        # store book attr to table
        def save_book(self, book):
                is_book_exist = self.is_exist(book_code=book[0])

                changeable_columns = []
                changeable_columns.append((book[0],book[3],book[4],
                                        book[8]))
                is_book_changed = self.is_changed(changeable_columns)

                # update_book if it not exist and changed
                if is_book_exist and is_book_changed:
                        self.update_book(book)
                # add book if it not exist
                elif not is_book_exist:
                        self.add_book(book)
                        self.create_post_placeholder(book[0])

        def add_book(self, book):
                conn = DB()
                cursor = conn.cursor()

                sql = "INSERT INTO book (book_code,book_name,\
                        book_author,book_etb_price,book_usd_price,\
                        book_img_url,book_category,book_language,\
                        book_stoke_status) VALUES \
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s);"

                cursor.execute(sql,book)
                conn.commit()

                # close
                cursor.close()

        def update_book(self, book):
                conn = DB()
                cursor = conn.cursor()

                sql = f"UPDATE book SET book_code = %s, book_name = %s,\
                        book_author = %s,book_etb_price = %s, book_usd_price = %s, \
                        book_img_url = %s, book_category = %s, \
                        book_language = %s, book_stoke_status = %s,\
                        book_content_status='1' WHERE book_code={book[0]}"

                cursor.execute(sql,book)
                conn.commit()

                # close
                cursor.close()

        # creates placeholder in post table in order 
        # the book to posted in the channel
        def create_post_placeholder(self, book_code):
                conn = DB()
                cursor = conn.cursor()

                sql = "INSERT INTO post(book_code) VALUES(%s);"

                cursor.execute(sql,(book_code,))
                conn.commit()

                # close
                cursor.close()

        # check the book exist in the table
        def is_exist(self, book_code) -> bool:
                conn = DB()
                cursor = conn.cursor(buffered=True)

                sql = "SELECT book_id FROM book WHERE\
                        book_code =%s"
                cursor.execute(sql, (book_code,))

                is_exists = cursor.fetchone()

                # close
                cursor.close()

                return bool(is_exists)
        
        def get_book(self, book_code):
                conn = DB()
                cursor = conn.cursor(dictionary=True,buffered=True)

                sql = "SELECT * FROM book WHERE\
                        book_code =%s"
                cursor.execute(sql, (book_code,))

                books = cursor.fetchone()

                # close
                cursor.close()
                
                return books if books else None
        
        def get_author_by_book_id(self, book_id):
                conn = DB()
                cursor = conn.cursor(buffered=True)

                sql = "SELECT book_author FROM book WHERE\
                        book_id =%s"
                cursor.execute(sql, (book_id,))

                author = cursor.fetchone()

                # close
                cursor.close()
                
                return author[0]
        
        # check the specific columns are changed form the table
        def is_changed(self, changeable_columns) -> bool:
                conn = DB()
                cursor = conn.cursor(buffered=True)

                sql = "SELECT book_id FROM book WHERE book_code =%s AND \
                        (book_etb_price != %s OR book_usd_price != %s \
                        OR book_stoke_status != %s);"

                for column in changeable_columns:
                        cursor.execute(sql, column)

                is_their_change = cursor.fetchone()

                # close
                cursor.close()

                return bool(is_their_change)

        def check_updated_books(self):
                conn = DB()
                cursor = conn.cursor()

                sql = "SELECT * FROM book WHERE book_content_status='1';"
                cursor.execute(sql)

                updated_books = cursor.fetchall()

                # close
                cursor.close()

                return bool(updated_books)

        def search_books(self, search_term):
                conn = DB()
                cursor = conn.cursor(dictionary=True)
                
                sql = """           
                SELECT * FROM book WHERE book_name LIKE %s OR book_author
                LIKE %s OR book_category IN (
                        SELECT category_id FROM category WHERE category_name 
                        LIKE %s
                ) LIMIT 50
                """
                search_term = "%" + search_term + "%"
                cursor.execute(sql,(search_term, search_term, search_term))
                
                result = cursor.fetchall()
                
                cursor.close()
                
                return result if result else None

        def get_authors(self, limit_start):
                conn = DB()
                cursor = conn.cursor()
                sql = "SELECT book_id as author_id,book_author as \
                        author_name,COUNT(*) AS author_count FROM book \
                        WHERE book_author NOT LIKE 'unknown%' GROUP BY \
                        author_name ORDER BY author_count DESC LIMIT %s,8"
                cursor.execute(sql, (limit_start,))

                authors = cursor.fetchall()

                # close
                cursor.close()
                
                return authors
        
        def total_authors(self):
                conn = DB()
                cursor = conn.cursor(buffered=True)
                sql = "SELECT COUNT(DISTINCT book_author) AS total_authors \
                        FROM book WHERE book_author NOT LIKE 'unknown%';"
                cursor.execute(sql)

                total = cursor.fetchone()

                # close
                cursor.close()
                
                return total[0] if total else 0