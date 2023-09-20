SUCCESS_MESSAGE = """
✨ <b>{book_name}</b> has been successfully added to your wishlist. Thank you \
for using our wishlist feature! 🌟

To view your wishlist, simply use the command "/wishlist"
"""

Wishlist_header = """  
📌 <b>Your Wishlist:</b>
🔹 <i>{total_list} books in your wishlist</i>
"""



LIST_EMPTY = """
You currently don't have any books in your wishlist. To add books to your \
wishlist, follow these steps:

1️⃣ Go to {channel_username} channel
2️⃣ Browse through the available books and find the book you want to add to your wishlist.
3️⃣ Once you get the book you want, click on the <b>"📌 Add to Wishlist"</b> button
"""


BOOK_LIST = """
{list_number}, <b>"{book_name}"</b>
    <b>By:</b> {book_author}
    <b>Genre:</b> {book_category}
    <b>Price:</b> Etb {etb_price}/ usd {usd_price}
    🛒 <a href="{order_page_link}">Order</>\t\t\t\t➖ <a \
    href="{remove_from_wishlist_link}">Remove</>
"""

Recommended_Book_Template = """
{list_number}, <b>"{book_name}"</b>
    <b>By:</b> {book_author}
    <b>Genre:</b> {book_category}
    <b>Price:</b> Etb {etb_price}/ usd {usd_price}
    🛒 <a href="{order_page_link}">Order</>\t\t\t\t➖ <a 
    href="{book_channel_post_link}">View detail</>
"""

LIST_REMOVED_SUCCESS_MESSAGE = """
The book <b>"{book_name}"</b> by {book_author} has been removed from your wishlist.

"/wishlist" view remained books in your wishlist
"""
