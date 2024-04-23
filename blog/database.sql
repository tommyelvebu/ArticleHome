CREATE TABLE category
(
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
   title VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE article
(
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
   title VARCHAR(255) NOT NULL,
   content TEXT NOT NULL,
   date DATE NOT NULL,
   category_id INTEGER NOT NULL,
   FOREIGN KEY (category_id) REFERENCES category(id)
);

INSERT INTO category(title) VALUES("Technology");
INSERT INTO category(title) VALUES("Lifestyle");
INSERT INTO category(title) VALUES("Entertainment");
