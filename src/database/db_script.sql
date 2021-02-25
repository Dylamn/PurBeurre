SET NAMES utf8;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS products_categories;
DROP TABLE IF EXISTS users_substitutes;
DROP TABLE IF EXISTS blacklist_tokens;


CREATE TABLE users
(
    id         INT UNSIGNED AUTO_INCREMENT,
    username   VARCHAR(128)        NOT NULL,
    email      VARCHAR(255) UNIQUE NOT NULL,
    password   VARCHAR(255)        NOT NULL,
    created_at DATETIME,
    updated_at DATETIME,

    CONSTRAINT pk_users PRIMARY KEY (id)
);

CREATE TABLE products
(
    id               INT UNSIGNED AUTO_INCREMENT,
    name             VARCHAR(255) NOT NULL,
    generic_name     VARCHAR(255),
    brands           VARCHAR(128),
    stores           VARCHAR(128),
    nutriscore_grade CHAR(1),
    url              VARCHAR(255),
    created_at       DATETIME,
    updated_at       DATETIME,

    CONSTRAINT pk_products PRIMARY KEY (id)
);

CREATE TABLE categories
(
    id   INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(128)        NOT NULL,
    tag  VARCHAR(128) UNIQUE NOT NULL,

    CONSTRAINT pk_categories PRIMARY KEY (id),
    CONSTRAINT uq_categories_tag UNIQUE (tag)
);

CREATE TABLE products_categories
(
    product_id  INT UNSIGNED,
    category_id INT UNSIGNED,

    CONSTRAINT pk_products_categories PRIMARY KEY (product_id, category_id),
    CONSTRAINT fk_products_categories_products FOREIGN KEY (product_id) REFERENCES products (id),
    CONSTRAINT fk_products_categories_categories FOREIGN KEY (category_id) REFERENCES categories (id)
);

CREATE TABLE users_substitutes
(
    user_id               INT UNSIGNED NOT NULL,
    original_product_id   INT UNSIGNED NOT NULL,
    substitute_product_id INT UNSIGNED NOT NULL,

    CONSTRAINT pk_users_substitutes PRIMARY KEY (user_id, original_product_id, substitute_product_id),
    CONSTRAINT fk_users_substitutes_users FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT fk_users_substitutes_products_original FOREIGN KEY (original_product_id) REFERENCES products (id),
    CONSTRAINT fk_users_substitutes_products_substitute FOREIGN KEY (substitute_product_id) REFERENCES products (id)
);

CREATE TABLE blacklist_tokens
(
    jwt_id         VARCHAR(36) PRIMARY KEY,
    blacklisted_at DATETIME NOT NULL
);
