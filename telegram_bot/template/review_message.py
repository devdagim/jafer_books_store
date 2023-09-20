BOOK_REVIEWS_HEADER = """
🌟 Reviews for <b>{book_name}</b>
🌟 Average Rating: <b>{average_rating}</b>

📝 <b>Customer Reviews</b>:
"""


REVIEW_BODY = """
{review_num}. <a href="tg://user?id={reviewer_id}"><b>{reviewer_name}</b></a>
    {rating_star}({rating}/5)
    Reviewed on 🗓 <i>{review_date}</i>

    {review}
"""

EMPTY_REVIEW_BODY = """
No reviews available for this book yet. Be the first one to review it!
"""
