# shob books listing page
url=https://www.jaferbooks.com/shop-grid.php
->total book number at uper row from the book listing
->book detalie url
->next book listing page url 16b/page

# catg
https://www.jaferbooks.com/category.php?category_name=Art%20and%20Music
https://www.jaferbooks.com/category.php?sub_category=Music


# single book page
url=https://www.jaferbooks.com/single-product.php?jbook_code=jb_1596
->book_author
response.css('.product__info__main span > h6::text').get()
->name
response.css('.product__info__main h1::text').get()
->price(in etb,usd)
etb=response.css('.price-box h5::text').get()
usd=response.css('.product__info__main div b::text').get()
->imgUrl
response.css('.modal-body img::attr(src)').get()
->Categorie(main catg,sub catg)
main + sub=response.css('.product_meta a::text').get()
->Language
//span[contains(text(),'Language:')]/text()
->Publish Date
//span[contains(text(),'Publish Date:')]/text()
->status
.product__info__main div > span b

# label page
url=https://www.jaferbooks.com/shop-grid.php
->lablename
//div[@class='megamenu mega02']/ul[3]/li/a[contains(@href,'label')]
url=https://www.jaferbooks.com/explore-books.php?label={All%20Time%20Great}
->bookId


# add to cart
url=https://www.jaferbooks.com/single-product.php?action=add&jbook_code=jb_1592
payload={'quantity':init}
method=post

# checkout page 
url=https://www.jaferbooks.com/checkout.php

# contact
url=https://www.jaferbooks.com/contact.php#mailmsg
GET OFFICE INFO.
La Gare, At The Side of NOC, Tewolde Bldg, Ground

ADDRESS:
Lagare, Addis Ababa, Ethiopia

PHONE NUMBER:
251-919-369844 / 251-91112-5324

EMAIL ADDRESS:
info@jaferbooks.com

WEBSITE ADDRESS:
