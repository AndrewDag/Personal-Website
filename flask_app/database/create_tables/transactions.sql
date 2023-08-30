CREATE TABLE IF NOT EXISTS `transactions` (
`transaction_id`          int(11)            NOT NULL AUTO_INCREMENT	     COMMENT 'Transaction ID',
`blockchain_id`           int(11)            NOT NULL  	                     COMMENT 'FK:The blockchain ID',
`cost`                    int(11)            NOT NULL	                     COMMENT 'Cost of Transaction   ',
`sellerID`                int(11)            NOT NULL                        COMMENT 'ID of seller',
`buyerID`                 int(11)            NOT NULL                        COMMENT 'Token Amount of NFT',
`date`                    varchar(100)            NOT NULL                   COMMENT 'Date of transaction',
PRIMARY KEY (`transaction_id`),
FOREIGN KEY (blockchain_id) REFERENCES blockchain(blockchain_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Transaction data";