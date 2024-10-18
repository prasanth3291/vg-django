# VogueVilla E-commerce Website

## Introduction
**VogueVilla** is an academic e-commerce website built entirely using **Django** for both the frontend and backend. It is designed to replicate all the essential features of a modern e-commerce platform, including product management, inventory control, order processing, cart functionality, and much more. The project demonstrates an understanding of full-stack web development while incorporating advanced features such as payment integration and user management.

## Features
VogueVilla provides a wide range of e-commerce functionalities, including:

### Core E-commerce Features:
- **Storefront**: Displays a variety of products with detailed information.
- **Inventory Management**: Admin can manage stock levels, product details, and variants.
- **Orders and Cart**: Customers can add products to their cart, place orders, and track purchases.
- **Favorites/Wishlist**: Users can save products to their favorite list for future purchases.
- **Payment Gateway**: Integrated with **PayPal** for seamless online payments.
- **PDF Invoice Generation**: Users receive a downloadable invoice for each purchase.
- **Profile Management**: Users can create and edit their profiles, view order history, and manage account settings.
- **Coupons and Offers**: Admin can create various discounts, offers, and referral systems for users.

### Security and Authentication:
- **Email Authentication**: Users must verify their email addresses to activate their accounts.
- **OTP Verification**: Added security through one-time password (OTP) verification for critical actions.
- **Session and Cookie Authentication**: Ensures secure user sessions while maintaining seamless interaction with the platform.

### Admin Panel:
- **Admin Dashboard**: Comprehensive admin panel to manage users, products, and orders.
- **Product Management**: Admin can add, edit, or delete products, manage categories, and create variants.
- **User Management**: Admin can manage user roles, monitor account activities, and more.
- **Reports and Analytics**: Generate sales reports, order summaries, and product performance insights.

## Technologies Used
### Backend
- **Django**: The entire application is built using the Django framework, which handles both the frontend and backend logic.
- **PostgreSQL**: The relational database used for managing and storing all application data, including users, products, and orders.

### Frontend
- **HTML, CSS, JavaScript**: Traditional web development languages for structuring, styling, and adding interactivity to the frontend.

### Payment Integration
- **PayPal**: Integrated for processing online payments securely.

### Security and Hosting
- **Session and Cookie Authentication**: Ensures secure and persistent sessions across the platform.
- **SSL Certificates**: Implements SSL encryption for secure communication and data protection.
- **AWS (Amazon Web Services)**: Used for hosting the application and database.
- **NGINX**: A high-performance web server used to serve the application.
- **Gunicorn**: A Python WSGI HTTP server used in combination with NGINX for serving Django applications.
- **HTTPS**: Ensures secure, encrypted connections to the application.

## Additional Features
- **PDF Bill Generation**: Users receive a downloadable bill after completing a purchase.
- **OTP Verification**: Secures important actions like registration and password recovery.
- **Coupon and Referral System**: Allows users to apply discounts and earn rewards through referrals.

## Conclusion
VogueVilla is a complete e-commerce solution that demonstrates full-stack development skills using Django. It integrates essential e-commerce features such as payment gateways, inventory management, user authentication, and more, providing a robust platform for users and administrators alike.
