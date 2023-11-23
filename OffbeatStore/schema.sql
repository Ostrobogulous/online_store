DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS reaction;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS notification;


CREATE TABLE user(
    id integer PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL COLLATE NOCASE,
    password TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE product(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER NOT NULL,
    label TEXT NOT NULL,
    category TEXT NOT NULL,
    brand TEXT NOT NULL,
    description TEXT,
    quantity INTEGER NOT NULL CHECK(quantity >= 1),
    price FLOAT NOT NULL,
    published TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP,
    image TEXT DEFAULT '/static/media/default.jpg',
    CONSTRAINT fk_user FOREIGN KEY (seller_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE INDEX idx_product_label ON product(lower(label));
CREATE INDEX idx_product_category ON product(lower(category));
CREATE INDEX idx_product_brand ON product(lower(brand));
CREATE INDEX idx_product_user ON product(seller_id);

CREATE TABLE reaction(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    type INTEGER NOT NULL, /* 1 if like -1 if dislike */
    reacted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE INDEX idx_reaction_product ON reaction(product_id);

CREATE TABLE review(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT,
    rating INTEGER NOT NULL CHECK (rating >= 0 AND rating <= 5),
    reviewed TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE INDEX idx_review_product ON review(product_id);
CREATE INDEX idx_review_user ON review(user_id);

CREATE TABLE notification(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    notifier_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    notification_type TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    seen BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    CONSTRAINT fk_notifier FOREIGN KEY (notifier_id) REFERENCES user(id) ON DELETE CASCADE,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

CREATE INDEX idx_notification_user ON notification(user_id);
CREATE INDEX idx_notification_notifier ON notification(notifier_id);
CREATE INDEX idx_notification_product ON notification(product_id);
