[shopspace_readme.md](https://github.com/user-attachments/files/34872580/shopspace_readme.md)
# 🛍️ ShopSpace — Modern Django E-Commerce Platform

ShopSpace is a full-stack e-commerce web application built with **Django** and styled with a custom, responsive **Warm & Vibrant Design System**. It features a storefront catalog with live stock indicators, client-side cart management, user authentication, customer support messaging, and a color-coded staff order fulfillment dashboard.

---

## ✨ Key Features

### 🛒 Customer Storefront
* **Modern Product Catalog:** Responsive grid layout featuring dynamic discount badges, star ratings, low-stock urgency meters, and smooth micro-interactions.
* **Search & Pagination:** Instant product search by item name with clean pagination controls.
* **Interactive Shopping Cart:** Live cart counter and floating popover preview with quick checkout access.
* **Product Detail Views:** Dedicated item pages showcasing product imagery, pricing breakdowns, stock availability, and store guarantees.
* **User Accounts & Profiles:** Registration, login, and personal profile dashboards where customers can view order history and support messages.
* **Customer Support:** Integrated contact form allowing users to submit inquiries directly to store administrators.

### 📦 Staff & Order Management Dashboard
* **Order Overview Table:** Searchable and filterable order list by Order ID, customer name, email, or fulfillment status (`Pending`, `Processing`, `Shipped`, `Delivered`, `Cancelled`).
* **Color-Coded Order Detail Zones:**
  * **Slate Zone:** Itemized purchase breakdown with quantities and unit pricing.
  * **Emerald Zone:** Financial summary and payment verification status.
  * **Amber Zone:** Quick-action fulfillment stage updater.
  * **Sky Zone:** Customer contact profile and modal-based shipping address editor.

---

## 🛠️ Tech Stack

* **Backend:** Python 3, Django
* **Frontend:** HTML5, CSS3 (Custom CSS Variables & Design System), Bootstrap 4.6, FontAwesome 6, JavaScript / jQuery
* **Typography:** *Plus Jakarta Sans* & *Space Mono* (Google Fonts)
* **Database:** SQLite (default for development; easily configurable for PostgreSQL/MySQL)

---

## 📁 Project Structure

```text
shopspace/
├── manage.py
├── shop/                       # Main storefront & order management app
│   ├── migrations/
│   ├── static/
│   │   └── shop/
│   │       ├── index.css       # Consolidated custom design system
│   │       └── images/         # Static banners, logos, and fallbacks
│   ├── templates/
│   │   └── shop/
│   │       ├── base.html           # Shared floating glass navbar & footer
│   │       ├── index.html          # Storefront hero banner & product grid
│   │       ├── product_detail.html # Single product view
│   │       ├── order_list.html     # Staff order management table
│   │       ├── order_detail.html   # Staff color-coded order inspector
│   │       └── contactus.html      # Customer support form
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
└── useraccounts/               # Authentication & customer profile app
    ├── templates/
    │   └── useraccounts/
    │       ├── login.html
    │       ├── register.html
    │       └── profile.html
    ├── urls.py
    └── views.py
```

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/shopspace.git
cd shopspace
```

### 2. Create & Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django pillow
```
*(If you have a `requirements.txt` file, run `pip install -r requirements.txt` instead.)*

### 4. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Staff / Superuser Account
To access the Django Admin panel and the Staff Order Management dashboard:
```bash
python manage.py createsuperuser
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --no-input
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 🎨 Customizing the Theme

All core colors, shadows, border radii, and fonts are controlled via CSS custom properties at the top of `shop/static/shop/index.css`:

```css
:root {
    --color-canvas:    #E2E8F0;  /* Background slate canvas */
    --color-surface:   #FFFFFF;  /* Card surface */
    --brand-primary:   #2B2D42;  /* Primary dark anchor */
    --warm-cta:        #FF5A36;  /* Vibrant coral CTA buttons */
    --warm-checkout:   #F59E0B;  /* Honey amber checkout accents */
    --warm-price:      #0F766E;  /* Spruce green pricing */
}
```
After modifying `index.css` or adding new images to `shop/static/shop/images/`, remember to run `python manage.py collectstatic --no-input` and hard-refresh your browser (`Ctrl + Shift + R`).

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
