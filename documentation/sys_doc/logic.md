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

├── bot_instance.py
├── bot
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── features
│   │   ├── order
│   │   │   ├── __init__.py
│   │   │   ├── controllers
│   │   │   │   └── order_controller.py
│   │   │   ├── models
│   │   │   │   └── order_model.py
│   │   │   ├── routers
│   │   │   │   └── order_route.py
│   │   │   └── templates
│   │   │       ├── order_message.py
│   │   │       └── ...
│   │   ├── post
│   │   │   ├── __init__.py
│   │   │   ├── controllers
│   │   │   │   └── post_controller.py
│   │   │   ├── models
│   │   │   │   └── post_model.py
│   │   │   ├── routers
│   │   │   │   └── post_route.py
│   │   │   └── templates
│   │   │       ├── post_message.py
│   │   │       └── ...
│   │   ├── preference
│   │   │   ├── __init__.py
│   │   │   ├── controllers
│   │   │   │   └── preference_controller.py
│   │   │   ├── models
│   │   │   │   └── preference_model.py
│   │   │   ├── routers
│   │   │   │   └── preference_route.py
│   │   │   └── templates
│   │   │       ├── preference_message.py
│   │   │       └── ...
│   │   └── ...
│   ├── filters
│   │   ├── __init__.py
│   │   ├── bot_deep_link_filter.py
│   │   └── ...
│   ├── helpers
│   │   ├── __init__.py
│   │   ├── aiomysql_storage.py
│   │   ├── bot_runner.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── event_storage.py
│   │   └── ...
│   ├── middlewares
│   │   ├── __init__.py
│   │   ├── channel_joined_middleware.py
│   │   └── ...
│   ├── routers
│   │   ├── __init__.py
│   │   ├── error_route.py
│   │   ├── start_route.py
│   │   └── ...
│   ├── scheduler_events
│   │   ├── __init__.py
│   │   ├── book_event.py
│   │   └── ...
│   ├── scraper
│   │   ├── __init__.py
│   │   ├── book
│   │   │   ├── __init__.py
│   │   │   ├── book_spider.py
│   │   │   ├── items_loader.py
│   │   │   ├── items.py
│   │   │   ├── pipelines.py
│   │   │   └── settings.py
│   │   ├── category
│   │   │   ├── __init__.py
│   │   │   ├── category_spider.py
│   │   │   ├── items_loader.py
│   │   │   ├── items.py
│   │   │   ├── pipelines.py
│   │   │   └── settings.py
│   │   └── ...
│   ├── templates
│   │   ├── __init__.py
│   │   ├── messages.py
│   │   ├── order_message.py
│   │   ├── review_form_message.py
│   │   ├── review_message.py
│   │   ├── static_cmds_message.py
│   │   ├── telegram_channel_book_post.py
│   │   └── wishlist_message.py
│   └── management
│       ├── __init__.py
│       ├── commands
│       │   ├── __init__.py
│       │   └── ...
│       └── ...
├── manage.py
├── readme.md
├── requirements.txt
└── static
    ├── css
    ├── js
    └── ...

# logic
=> creating post table on trigger of the book table
=> we don\t have no longer book table
=> implement order functionality

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