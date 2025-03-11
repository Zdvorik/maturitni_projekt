-- Vytvoření tabulek
CREATE TABLE IF NOT EXISTS `{user_table_name}` (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL
)

CREATE TABLE IF NOT EXISTS `{score_table_name}` (
    user_id INT PRIMARY KEY,
    score INT NOT NULL,
    time INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES `{user_table_name}`(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)

-- Vložení dat
INSERT INTO `{user_table_name}` (username) VALUES ('Alice')
INSERT INTO `{user_table_name}` (username) VALUES ('Bob')
INSERT INTO `{user_table_name}` (username) VALUES ('Charlie')

INSERT INTO `{score_table_name}` (user_id, score, time) VALUES (1, 50, 300)
INSERT INTO `{score_table_name}` (user_id, score, time) VALUES (2, 35, 200)
INSERT INTO `{score_table_name}` (user_id, score, time) VALUES (3, 20, 100)


-- Výběr a výpis všech uživatelů a jejich skóre
SELECT u.username, s.score, s.time
FROM `{user_table_name}` u
JOIN `{score_table_name}` s ON u.user_id = s.user_id
