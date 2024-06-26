# Grocery_shop

## Abstract
 The grocery store app is designed to provide a user-friendly platform for customers
 to browse and purchase products, and manage their shopping carts. Additionally, the
 app offers administrative functionalities, allowing the admin to manage categories,
 and products, and monitor sales and inventory. The system aims to enhance the
 shopping experience and streamline the store's operations.
 ## Models
 The app employs several models to organize and manage data effectively. The key
 models include:
 User: Represents a user of the app, which includes both regular customers and
 administrators. The User model is essential for authentication and managing
 user-specific data.
 Category: Represents product categories, which are created and managed by the
 admin. Categories provide a structured way to organize products, making it easier for
 users to find what they need.
 Product: Represents individual products available in the store. Each product has
 attributes such as name, price per unit, quantity, unit (e.g., kg, liter), and expiration
 date. The Product model is linked to the Category model to maintain categorization.
 CartItem: Tracks the items added to a user's cart. It associates the user, the product,
 and the quantity of the product in the cart.
 PurchaseHistory: Records the purchase history of users, including the purchased
 product, the quantity purchased, and the purchase date. This model helps users
 track their past purchases.
 ## Overall System Design:
 The system design focuses on providing a seamless user experience, efficient
 product management, and effective sales monitoring. Here are the key components
 of the system:
 User Authentication: The system allows users to register, log in, and log out.
 Authenticated users have access to personalized features such as viewing their cart
 and purchase history.
 Product Display: The app displays products categorized by the admin. Users can
 browse products, view product details, and search for specific items.
 Shopping Cart: Users can add products to their shopping cart, adjust quantities,
 and remove items. The cart allows users to review their selections before making a
 purchase.
 
Purchase and Inventory Management: When a user makes a purchase, the
 system updates the product quantity, records the purchase history, and adjusts the
 inventory. The admin can manage categories and products, ensuring the accuracy of
 available items.
 Sales Monitoring: The app provides sales summary information, including weekly
 sales, total sales per category, and graphical representations. The admin can
 monitor sales trends and make informed decisions.
 Expiration Tracking: The app includes an "expiration_date" field for products,
 allowing users to see the expiration date of products. Additionally, the system can
 alert users when products are close to or past their expiration dates.
 Admin Control: Administrators have access to additional functionalities, including
 category creation, product management, and monitoring sales and inventory. Admins
 can ensure the store's smooth operation.
##  Conclusion:
 The grocery store app is designed to create a user-friendly shopping experience
 while empowering the admin with tools to manage products, categories, and sales.
 The system's use of models allows for structured data management, while the
 overall design emphasizes functionality, efficiency, and data accuracy. By
 incorporating user authentication, inventory management, and sales monitoring, the
 app aims to be a comprehensive solution for both customers and administrators in
 the grocery store context.
