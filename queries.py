# Shoppers
GET_SHOPPERS_QUERY = """
    SELECT * FROM shoppers WHERE shopper_id = ?;
"""

# Categories

GET_CATEGORIES_QUERY = """
    SELECT category_id, category_description 
    FROM categories 
    ORDER BY category_description ASC;
"""

# Products

GET_PRODUCTS_QUERY = """
    SELECT product_id, product_description 
    FROM products 
    WHERE category_id = ? 
    ORDER BY product_description ASC;
"""

# Sellers

GET_SELLERS_QUERY = """
    SELECT ps.seller_id, s.seller_name, ps.price
    FROM product_sellers ps
    JOIN sellers s 
        ON ps.seller_id = s.seller_id
    WHERE ps.product_id = ?
    ORDER BY s.seller_name ASC;
"""

# Shopper Baskets

GET_MOST_RECENT_BASKET_QUERY = """
    SELECT basket_id
    FROM shopper_baskets
    WHERE shopper_id = ?
        AND DATE(basket_created_date_time) = DATE('now')
    ORDER BY basket_created_date_time DESC
    LIMIT 1
"""

GET_BASKET_QUERY = """
    SELECT *
    FROM shopper_baskets
    WHERE shopper_id = ?;
"""

CREATE_BASKET_QUERY = """
    INSERT INTO shopper_baskets (shopper_id, basket_created_date_time) 
    VALUES (?, datetime('now'));
"""

ADD_TO_BASKET_QUERY = """
    INSERT INTO basket_contents (basket_id, product_id,seller_id, quantity, price)
    VALUES (?, ?, ?, ?, ?);
"""

DELETE_SHOPPER_BASKET_QUERY = """
    DELETE FROM shopper_baskets 
    WHERE basket_id = ?;
"""

# Basket Contents

GET_BASKET_CONTENTS_QUERY = """
    SELECT bc.product_id, p.product_description, s.seller_name, bc.quantity, bc.price
    FROM basket_contents bc
    JOIN products p 
        ON bc.product_id = p.product_id
    JOIN sellers s 
        ON bc.seller_id = s.seller_id
    WHERE bc.basket_id = ?;
"""

UPDATE_QUANTITY_QUERY = """
    UPDATE basket_contents
    SET quantity = ?
    WHERE basket_id = ? AND product_id = ?;
"""

DELETE_ITEM_QUERY = """
    DELETE FROM basket_contents
    WHERE basket_id = ? AND product_id = ?;
"""

DELETE_BASKET_CONTENTS_QUERY = """
    DELETE FROM basket_contents 
    WHERE basket_id = ?;
"""

GET_BASKET_CONTENTS_FOR_CHECKOUT_QUERY = """
    SELECT bc.product_id, bc.seller_id, bc.quantity, bc.price
    FROM basket_contents bc
    WHERE bc.basket_id = ?;
"""

# Orders

GET_ORDER_HISTORY_QUERY = """
    SELECT
        so.order_id,
        DATE(so.order_date) AS order_date,
        p.product_description,
        s.seller_name,
        op.price,
        op.quantity,
        op.ordered_product_status
    FROM shopper_orders so
    JOIN ordered_products op
        ON op.order_id = so.order_id
    JOIN products p
        ON p.product_id = op.product_id
    JOIN sellers s
        ON s.seller_id = op.seller_id
    WHERE shopper_id = ?
    ORDER BY so.order_date DESC;
"""

INSERT_ORDER_QUERY = """
    INSERT INTO shopper_orders (shopper_id, order_date, order_status)
    VALUES (?, datetime('now'), 'Placed');
"""

INSERT_ORDERED_PRODUCT_QUERY = """
    INSERT INTO ordered_products (order_id, product_id, seller_id, quantity, price, ordered_product_status)
    VALUES (?, ?, ?, ?, ?, 'Placed');
"""

# Extras
GET_LAST_INSERT_ID_QUERY = """
    SELECT last_insert_rowid();
"""

GET_SELLER_ID_FROM_BASKET_QUERY = """
    SELECT seller_id FROM basket_contents WHERE basket_id = ? AND product_id = ?;
"""