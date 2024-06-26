
  
# Shopper Personas


To provide a more compelling and intuitive demo experience, each fictitious user in the Retail Demo Store is
assigned a shopper persona. The persona is represented by three categories from the Retail Demo Store’s catalog
which the user has an affinity. The affinity for each category is also weighted such that the first category is is
highest weighted and the third category is the lowest. There are sixteen combinations of categories that represent
the personas used across all users.


* furniture_homedecor_housewares
* apparel_footwear_accessories
* instruments_books_electronics
* floral_beauty_jewelry
* grocery_seasonal_wedding
* outdoors_instruments_grocery
* housewares_floral_seasonal
* tools_housewares_apparel
* electronics_outdoors_footwear
* seasonal_furniture_floral
* homedecor_electronics_outdoors
* accessories_grocery_books
* footwear_jewelry_furniture
* beauty_accessories_instruments
* housewares_tools_beauty
* books_apparel_homedecor




For example, a user assigned with a persona of "footwear_outdoors_apparel" indicates that the user, at least
historically, has been primarily interested in products from the Footwear category and to decreasing degrees of
interest in products from the Outdoors and Apparel categories. That initial weighted interest is codified in the
generation of the historical interaction dataset which is used to train Solutions in Amazon Personalize. So, for
our "footwear_outdoors_apparel" user, interaction events are generated across products in all three of those
categories to create a synthetic history of engaging in products matching that persona. Additionally, some
products are tagged with an gender affinity. This is used when generating historical events to filter products
against the gender of each user to further add realism to the recommendations.

Events for multiple event types are generated to mimic shopping behavior. For example, most generated event types
are 'View' to mimic users browsing the site. Occasional checkouts are simulated with 'AddToCart'
followed by 'ViewCart', 'StartCheckout', and 'Purchase' events. The Personalize solutions/models are
trained on the 'View' event type.

  
