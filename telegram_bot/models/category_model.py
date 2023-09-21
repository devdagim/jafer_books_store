from telegram_bot.helpers.db import DB


class CategoryModel:
        # save category attr into category table if not exist
        # or update from the table
        def save_category(self, sub_category_parent_id, category_name):
                conn = DB()
                cursor = conn.cursor()

                # checking the category attr data in table
                if not self.is_exist(category_name):
                        sql = "INSERT INTO category (\
                                        sub_category_parent_id,category_name) \
                                        VALUES (%s, %s);"
                        cursor.execute(sql,(sub_category_parent_id,category_name))
                        conn.commit()

                # close
                cursor.close()

        # extract category_id form category table using category name
        def get_category_id(self, category_name) -> int:
                conn = DB()
                cursor = conn.cursor(buffered=True)

                sql = "SELECT category_id FROM category WHERE \
                                        category_name=%s"
                cursor.execute(sql, (category_name,))

                result = cursor.fetchone()


                # close
                cursor.close()

                return result[0] if result else None

        def get_categories(self, limit_start):
                conn = DB()
                cursor = conn.cursor()

                sql = "SELECT category_id,category_name FROM category WHERE \
                        sub_category_parent_id=0 AND category_name NOT \
                        LIKE 'Uncategorized%' LIMIT %s,8"
                cursor.execute(sql,(limit_start,))

                result = cursor.fetchall()

                # close
                cursor.close()

                return result
        
        def total_categories(self):
                conn = DB()
                cursor = conn.cursor(buffered=True)

                sql = "SELECT COUNT(*) FROM category WHERE \
                        sub_category_parent_id=0 AND category_name NOT \
                        LIKE 'Uncategorized%'"
                cursor.execute(sql)

                result = cursor.fetchone()

                # close
                cursor.close()

                return result[0] if result else 0

        # checks the existence of the category attr
        def is_exist(self, category_name) -> bool:
                conn = DB()
                cursor = conn.cursor(buffered=True)

                sql = "SELECT category_id FROM category WHERE\
                                        category_name=%s"
                cursor.execute(sql, (category_name,))

                existence = cursor.fetchone()

                # close
                cursor.close()

                return bool(existence)

        def get_book_category(self, category_id):
                conn = DB()
                cursor = conn.cursor(buffered=True)

                sql = """
                                        SELECT CONCAT(
                                        '',
                                        CASE WHEN sub_category_parent_id = 0 THEN category_name ELSE (
                                                CONCAT(
                                                (SELECT c2.category_name
                                                FROM category c2
                                                WHERE c2.category_id = c1.sub_category_parent_id),
                                                ', ',
                                                c1.category_name
                                                )
                                        ) END,
                                        ''
                                        ) AS category_name
                                        FROM category c1
                                        WHERE c1.category_id = %s;
                                        """
                cursor.execute(sql, (category_id,))

                category_name = cursor.fetchone()

                # close
                cursor.close()

                return category_name[0]
