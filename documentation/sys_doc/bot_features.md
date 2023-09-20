# icon color
- green
- yellow
- red
- white

# feature::channel Posting Book Info to Channel
- on new book stor uploaded
- on book metadata changed

[------------------channel_post_template---------------------------------------]

    📷 Book Image: [Insert Book Image]

    [availability=out: <"--------**Out of Stock**-------">]
    📕 Title: [Book Title]
    📝 Author: [Author]
    🔖 Genre: [Genre]
    🗓 Publication Date: [Publication Date]
    🏢 Publisher: [Publisher]
    💬 Language: [book_language]

    🏷 Price: ETB [book_etb_price] / USD [book_usd_price]
    🏷 Availability: [🔴 Out of Stock] / [🟢 In Stock]

    🌟 Ratings: [(3.4/5)] ratings

    [#category_name #book_name #author_name]

    Want to know more? <b>Click</b> the buttons below to take action:
        -------------------------------------
        [ [🛒 Order Now]        [📌 Add to Wishlist] ]
        -------------------------------------
        [ [⭐️ reviews ]    [⭐️ Rate]  ]
        -------------------------------------
    [availability=out: </"--------**Out of Stock**-------">]

[---------------------/channel_post-------------------------------------------]

# feature::bot Notifications and Reminders message
- on new book stor uploaded
    :based on their
        - user's preferences,
            - Author
            - Genre
        - reading history,
        - ratings
    :use channel_post_template

# feature::bot/channel searching book
    # feature::bot  inline bot @bot_name book/author: search
    - searching book by book name or author

    # feature::channel  by #hashtag,telegram search builtin method
    - by #category_hashtag #book_author

# feature::bot Book Recommendations
    # feature::bot /my_books(btn) recommended book list
            - user's preferences,
                - Author
                - Genre
            - ratings

# feature::bot Rating and Review System
on [⭐️ reviews ] button->bot?book_code=kkkkkkkk
    [-----------------customer_review_template-----------------------------------]
        --------------headline--------------------
        🌟 Reviews for [Book_Title] by [Author]
        🌟 Overall Rating: <b>3.5/5</b>

        📝 Customer Reviews:
        --------------headline--------------------

        ------------------------------------------
        1. [Reviewer Name] (@[Reviewer_userName])
            ⭐⭐⭐⭐⭐(3/5)
            Reviewed on 🗓 [Review_Date]

            💬 [Review Text]
        -----------------------------------------

        ------------------------------------------
        2. [Reviewer Name] (@[Reviewer_userName])
            ⭐⭐⭐⭐⭐(4/5)
            Reviewed on 🗓 [Review_Date]

            💬 [Review Text]
        ------------------------------------------

        ------------------------------------------
        3. [Reviewer Name] (@[Reviewer_userName])
            😍 Excellent(5/5)
            Reviewed on 🗓 [Review_Date]

            💬 [Review Text]
        ------------------------------------------

        [  [   ⏩  next   ]   [   ⏪  back   ]    ]
    [----------------/customer_review_template-----------------------------------]

on [⭐️ Rate ] button->bot?book_code=kkkkkkkk
    [--------------------bot-----------------------------]
        Please choose a rating to rate {book_name} from the following options:
        [😍 Excellent ] [ 👏Good ] [ 😐Average ] [ 😕Below Average ] [ 👎bad ]
    [--------------------bot-----------------------------]

                                    [-----------user----------------]
                                            [😍 Excellent ]
                                    [---------------------------]

    [--------------------bot-----------------------------]
        Please provide your feedback or comments about the book. You can skip this step by sending "/cancel" or typing "cancel"
    [--------------------bot-----------------------------]

                                    [-----------user----------------]
                                            feed back
                                    [---------------------------]

    [--------------------bot-----------------------------]
       your review has been successfully submitted. Thank you for sharing your feedback!
    [--------------------bot-----------------------------]

                                    [-----------user----------------]
                                            /cancel or cancel
                                    [---------------------------]

    bot>>>>canceled success

# feature::bot whilst
on add()
    [--------------------bot-----------------------------]
        you have successfully added {book_name} to ur whilst
                [view whilst button]
    [--------------------/bot-----------------------------]

on view whilst
    [--------------------bot-----------------------------]
        you have successfully added {book_name} to ur whilst
                [view whilst button]
    [--------------------/bot-----------------------------]

