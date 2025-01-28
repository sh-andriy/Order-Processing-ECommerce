# Order processing for e-commerce

<hr/>

## Main directories/modules:

- `products/` — contains the `Product` and `Promotion` models and logic related to products and promotions.
- `cart/` — contains the shopping cart logic: `Cart` and `CartItem` models, main view functions for adding items, applying promotions, calculating total cost, etc.
- `orders/` — manages the order checkout process: `Order`, `PaymentTransaction`, `DeliveryTracking` models, view functions (`checkout_order`, `process_payment`, etc.), as well as Celery tasks for synchronizing with external systems.
- `core/` (if present) — shared services, configurations, and Celery settings.

## Project setup

1. Clone the repository:
   ```bash
   git clone https://github.com/example/online_store.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
5. (Optional) Run Celery (for background tasks):
   ```bash
   celery -A online_store worker -l info
   ```

## Logic overview

- **Shopping Cart (Cart)**: Created for a user, supports multiple statuses (`active`, `converted`, etc.). It can store items (`CartItem`) and apply promotions (`Promotion`).
- **Order**: Created after `checkout`, storing the total order amount, payment methods, and delivery details. The status may change from `new` to `paid`, `shipped`, `delivered`, etc.
- **Background tasks (Celery)**:
  - `send_order_to_external_system(order_id)`: sends order data to an external service without blocking the user.
  - `sync_from_external_system()`: periodically or manually updates order statuses (e.g., if the external system changes statuses or adds new orders).

## Future enhancements could include:
- Advanced error handling
- Data caching
- More detailed user roles and permissions
- Test coverage (unit tests, integration tests)
- CI/CD (GitHub Actions, GitLab CI, etc.)
- A Dockerfile or docker-compose for containerization
