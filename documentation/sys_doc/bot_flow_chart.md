# intro
Personalized Recommendations: Set preferences to receive personalized book suggestions.
Book Suggestions: Get handpicked book recommendations based on your preferences.
Wishlist Management: Easily manage your book wishlist.
Book Search: Search books by title, author, or genre.
Online Bookstore: Explore and purchase books online.
Book Rating: Provide ratings and reviews for books you've read.

# menu
[Bot Menu]
Please choose from the following options:

📚 /preference - Set preferences for personalized book recommendations.
🔍 /recommendation - Get personalized book suggestions.
📌 /wishlist - Manage your book wishlist.
🔎 /search - Search books by title, author, or genre.
🛒 /store - Explore and purchase books online.

# /start cmd

[case=if_not_joined]
[Bot]:  hi {user_name},Welcome to our {bot_name}! To get started, 
        please join our official channel to access our collection of books. 
        Click the button below to join:
        [📚 Join Channel]->{book_store_channel}

[case=if_joined_|_on_join_to_channel]
[Bot]:  Welcome {user_name}! You're already a member of our channel. To 
        receive personalized book recommendations from our bot, you can 
        set your book preferences. 
        Simply send the command /book_preferences
        [set book preferences]->/book_preferences

# [X] /preference
[Bot]:  Step 1: Author Preference
        Please select your preferred book author from the options below:
        [Author 1]
        [Author 2]
        [Author 3]
        [➡️ Next ]
[Bot]:  Step 2: Genre Preference
        Please select your preferred book genre from the options below:
        [Genre 1]
        [Genre 2]
        [Genre 3]
        [⬅️ Back] [➡️ Next ]

[case=on_book_preference_form_submitted_successfully]
[Bot]:  Your book preferences have been submitted. Our bot will now curate
        personalized book recommendations just for you.
        
        You can retrieve your book recommendations anytime 
        by typing /book_recommendations or simply click the button below:

        [📚 Get Book Recommendations]

# [X]/book_recommendations
[Bot]:  Book recommendations based on your preferences
        3 book recommendations out of 100:

        1,"The Name of the Wind"
            By: Patrick Rothfuss
            Genre: Fantasy
            Language: English
            [See Details]->linked_to_channel_post
        2, "Educated"
            By: Tara Westover
            Genre: Memoir
            Language: English
            [See Details]->linked_to_channel_post

        [📚 Next Page][📚 back Page]

# [X]/wishlist
[case=if_list_not_empty]
[Bot]:  Your Wishlist:
        3 book out of 100:

        1, "The Name of the Wind"
            By: Patrick Rothfuss
            Genre: Fantasy
            Price: 100/12.99
            [go to book ] [Remove]

        2, "Educated"
            By: Tara Westover
            Genre: Memoir
            Price: $10.99
            [go to book] [Remove]

        [📚 Next Page][📚 back Page]

[case=book_1=remove=from_the_list]
[Bot]:  Are you sure you want to remove {"book_name"} by {book_author} from 
        your wishlist?
        \n
        Please click "Confirm" to proceed with the removal or "Cancel" to 
        keep the book in your wishlist.
        [Confirm] [Cancel]

[case=book_1=remove=confirm]
[Bot]:  The book {"book_name"} by {book_author} has been removed from your 
        wishlist.

[case=book_1=remove=Cancel]
[Bot]:  The book {"book_name"} by {book_author} will remain in your wishlist.

[case=if_list_is_empty]
[Bot]:  Your Wishlist:
        You currently don't have any books in your wishlist. To add books to
        your wishlist, follow these steps:
        \n
        1,Go to our channel: {channel_link}
        2,Browse through the available books and find the book you want to add to your wishlist.
        3,On the u get the book u want, click on the "Add to Wishlist" button

        [go to our channel]

# /search
[Bot]:  How would you like to search for books?

        Search by:
        👤 Author Name: @botusername author: [author name]
        📚 Book Name: @botusername book: [book name]

        example: to search for books by the author "Stephen King," you can use:
        @botusername author: Stephen King

        example: to search for a book with the title "The Great Gatsby," you can use:
        @botusername book: The Great Gatsby

        Alternatively, you can click on the following buttons to initiate your search:

# /contact
[Bot]:  Here is the contact information for our store:
        📍 Physical Location:
            Store 1:
            link=https://maps.google.com/?q=<lat>,<lng>
            link_text{123 Main Street, City A, Country A}

            Store 2:
            link_text{456 Elm Street, City B, Country B}

            Store 3:
            link_text{789 Oak Street, City C, Country C}

        📞 Phone Number:
            +1 234 567 890

        📧 Email:
            store1@example.com

        💻 Website:
            www.store1.com


# [X]/start=order_now&book_code={book_code}
[Bot]:  Thank you for choosing to order with us! 
        please select your preferred method of ordering from the options below:
        1,🏢 Visit our physical store
        2,📞 Place an order by phone call
        3,💻 Order online through our website
        \n
        Please select one of the options by tapping the corresponding button
        on the keyboard.

        reply_kbd([1,2,3])
[case=option=1]
[Bot]:  Great! You've chosen to visit our physical store. Here's the store 
        location information along with details about the book you're interested in:

        📚 Book Information:
        Title: [Book Title]
        Author: [Book Author]
        Book Code: [Book Code]

        📍 Store Location:
        123 Main Street, City, Country

        📍 Store Location:
        123 Main Street, City, Country

        📍 Store Location:
        123 Main Street, City, Country

        Please visit our store at the provided location to make your purchase. 
        Our friendly staff will be happy to assist you in finding the book 
        you're looking for.

[case=option=1]
[Bot]:  Wonderful! You've chosen to place an order by phone call. Here's the 
        detailed instructions on how to place your order by phone call:
        \n
        1,Dial our dedicated phone line at [Phone Number].
        2,When connected, inform the customer service representative that you 
        would like to place an order for a book.
        3,Provide the following details about the book:
            Book Title: [Title]
            Book Author: [Author]
            Book Code: [Code]

[case=option=3]
[Bot]:  Fantastic! You've chosen to order the book online through our website.
        Here's how you can proceed with your online order:
        book_page_link: { book_page_link}

        1,Click on the provided book page link and select "Add to Cart."
        2,Access your cart by clicking on the cart icon in the web header.
        3,Proceed to checkout and provide shipping details.
        4,Fill out billing information and review the order summary.
        5,Complete the payment verification process.

# [X]/start=add_to_wishlist&book_code={book_code}
[Bot]:  [book_name] has been successfully added to your wishlist.Thank you for 
        using our wishlist feature!

        To view your wishlist, simply use the command "/wishlist" or click 
        the button below:
        [View Wishlist]

# [X]/start=reviews&book_code={book_code}
[Bot]:  # -----------------------------------------
        🌟 Reviews for [Book_Title] by [Author]
        🌟 Overall Rating: <b>3.5/5</b>

        📝 Customer Reviews:
        -----------------------------------------
        \n
        ------------------------------------------
        1. [Reviewer Name] (@[Reviewer_userName])
            ⭐️⭐️⭐️⭐️⭐️(5/5)
            Reviewed on 🗓 [Review_Date]

            💬 [Review Text]
        \n
        2. [Reviewer Name] (@[Reviewer_userName])
            ⭐️(1/5)
            Reviewed on 🗓 [Review_Date]

            💬 [Review Text]
        ------------------------------------------

        [  [   ⏩  next   ]   [   ⏪  back   ]    ]
        [  /rate?book_code={book_code}            ]

[case=reviews=empty]
[Bot]:  # -----------------------------------------
        🌟 Reviews for [Book_Title] by [Author]
        🌟 Overall Rating: <b>0/5</b>

        📝 Customer Reviews:
        -----------------------------------------

        No reviews available for this book yet. Be the first one to review it!

        ------------------------------------------

        [  /rate?book_code={book_code}            ]

# [X]/rate?book_code={book_code}
[Bot]: Please rate the book "{book_name}" using one of the following options:
        [⭐️⭐️⭐️⭐️⭐️(Excellent) ] [ ⭐️⭐️⭐️⭐️(Good) ] 
        [ ⭐️⭐️⭐️(Average) ] [ ⭐️⭐️(Below Average) ] [ ⭐️(Bad) ]

[case=rating_option]
[Bot]:  Please provide your feedback or comments about the book "{book_name}". 
        You can skip this step by sending "/cancel" or typing "cancel".

[case=sended_feedback]
[Bot]: Thank you for sharing your feedback and for rating the book "{book_name}".

[case=/cancel_or_cancel]
[Bot]: You have successfully submitted your review\nThank you for rating.