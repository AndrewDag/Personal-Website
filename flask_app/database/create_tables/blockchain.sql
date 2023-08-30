CREATE TABLE IF NOT EXISTS `blockchain` (
`blockchain_id`        int(11)       NOT NULL 	AUTO_INCREMENT              COMMENT 'Blockchain ID',
`nft_id`               int(11)       NOT NULL 	                            COMMENT 'FK:The nft id',
PRIMARY KEY (`blockchain_id`),
FOREIGN KEY (nft_id) REFERENCES nft(nft_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Blockchain data";