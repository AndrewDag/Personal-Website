CREATE TABLE IF NOT EXISTS `hash` (
`hashes`              varchar(100)     NOT NULL 	                            COMMENT 'The actual hash',
`transaction_id`    int(11)          NOT NULL 	                                COMMENT 'FK:The transaction id',
PRIMARY KEY (`hashes`),
FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Blockchain data";