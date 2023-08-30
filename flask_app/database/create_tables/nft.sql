CREATE TABLE IF NOT EXISTS `nft` (
`nft_id`            int(11)            NOT NULL AUTO_INCREMENT	     COMMENT 'The NFT ID',
`user_id`           int(11)            NOT NULL  	                 COMMENT 'FK:The user ID',
`name`              varchar(100)       NOT NULL	                     COMMENT 'Name of NFT',
`description`       varchar(1000)       NOT NULL                      COMMENT 'Description of NFT',
`token_amount`      int(11)            NOT NULL                      COMMENT 'Token Amount of NFT',
PRIMARY KEY (`nft_id`),
FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="NFT Image Data";