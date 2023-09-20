# check for new_product
    from post_table
        get_post_status=0
            :means its new product and its not posted
        post_it()
        =>post to channel
        =>save the post_id to the table
        =>change_post_status=1
            :means its posted

# check for updated product
    from book_table
        get_booK_content_status=1
            :means its updated product
        edit_post()
        =>get post id using book_code
        =>edit the post form the channel
        =>change booK_content_status=0
            :means its original not updated or edited product

# Recommendation System Steps:

1,Find users in the review table who have rated the same book as the current user(who rated rating > 2).

- Select similar_book_rater_user_id from the review table who have rated the book.
```sql
SELECT user_id FROM book_review WHERE rating > 2 AND book_code in (SELECT book_code FROM book_review WHERE rating > 2 AND user_id="6288799554")
```

- Select books that have been rated by those other users(similar_book_rater_user_id).
```sql
SELECT book_code FROM book_review WHERE user_id IN (SELECT user_id FROM book_review WHERE rating > 2 AND book_code in (SELECT book_code FROM book_review WHERE rating > 2 AND user_id="6288799554"))
```
2,Identify users in the wishlist who have added the same book as the current user.

- Select other users from the wishlist who have added the book to their list.
```sql
SELECT user_id FROM wishlist WHERE book_code in (SELECT book_code FROM wishlist WHERE user_id="6288799554")
```
- Select books that have been listed by those other users.
```sql
SELECT book_code FROM wishlist WHERE user_id IN (SELECT user_id FROM wishlist WHERE book_code IN (SELECT book_code FROM wishlist WHERE user_id="6288799554"))
```
3.Consider books that match the user's preferences based on genre and author.

- Select books where the genre ID is in the user's genre preferences.
- Select books where the author's name is in the user's author preference.
```sql
SELECT book_code FROM book WHERE book_author IN (SELECT author_name FROM author_preference WHERE user_id="6288799554") OR book_category IN (SELECT category_id FROM genre_preference WHERE user_id="6288799554")
```