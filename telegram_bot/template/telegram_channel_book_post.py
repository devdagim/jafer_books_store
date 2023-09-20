CHANNEL_POST_BODY = """
<b><i>{book_title}</i></b>

📝 <b>Author</b>: {author_name}
🔖 <b>Genre</b>: {category_name}
💬 <b>Language</b>: {book_language}

🏷 <b>Price</b>: ETB {book_etb_price} / USD {book_usd_price}
🏷 <b>Availability</b>: {book_stock_status}

🌟 <b>Ratings</b>: ({book_total_rating}/5)⭐️ ratings

{hashtag_category_names} #{hashtag_book_name} #{hashtag_author_name}

    <b><i>"ሃገር ያለአንድነት ህሊና ያለንባብ አይበለፅግም!"</i></b>
@JaferBooksStore | @JaferBooksBot
<a href="{book_img_url}">&#8288;</a>
"""


# STOCK STATUS TEXT
IN_STOCK_TEXT = "🟢 In Stock"
OUT_OF_STOCK_TEXT = "🔴 Out of Stock"


# INLINE BTN
ORDER_NOW_BTN_TEXT = "🛒 Order Now"
ADD_TO_WISHLIST_BTN_TEXT = "📌 Add to Wishlist"
REVIEWS_BTN_TEXT = "🌟 Reviews"