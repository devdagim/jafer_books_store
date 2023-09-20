# category_table
    ** column_s **
    * category_id int(11) auto_i+ 
        - used as to identify each record from the table
    * sub_category_parent_id int(11)
        - 0=for main_category category_id=form sub_categorys
    * category_name var(100)
        - the name of the category

# book_table
    ** colum_s **
    * book_id
    * book_code
    * book_name
    * book_author
    * book_etb_price
    * book_usd_price
    * book_img_url 
    * book_category
    * book_language
    * book_stoke_status
    * book_content_status=original,edited
        - this filed is used as to check for book_update status
            original= means their is no change
            edited=means their is a change
        - after event trigger
            must change the edited status into original
        event_trigger('book_content_status'):
            if =edited
             emit=book_update
                edit_the_post()
                then_change_status=original

# post_table
    ** colum_s **
    * telegram_post_id=Null,post_id
    * book_code=book_table->book_id
    * book_post_status=0(not_posted),1(posted)
        event_trigger('check for book_not_posted')
            if =not posted
             emit=new_book_release
                post()
                then_change_status=posted

# book_review
    review_id
    book_code
    user_id
    rating
    rating_feedback

# user_preference
    user_id
    author_name
    genre_id