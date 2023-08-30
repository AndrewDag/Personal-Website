CREATE TABLE IF NOT EXISTS `wallet` (
`user_key`             varchar(100)  NOT NULL 	                    COMMENT 'The user key',
`user_id`              int(11)       NOT NULL 	                    COMMENT 'FK:The user ID',
`tokens`               int(11)       NOT NULL                       COMMENT 'Token amount',
PRIMARY KEY (`user_key`),
FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Wallet of given user";