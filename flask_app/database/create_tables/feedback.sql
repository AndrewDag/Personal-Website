CREATE TABLE IF NOT EXISTS `feedback` (
`comment_id`         int(11)       NOT NULL AUTO_INCREMENT	COMMENT 'The comment id',
`name`               varchar(100)  DEFAULT NULL             COMMENT 'Commenter name',
`email`              varchar(100)  DEFAULT NULL             COMMENT 'Commenter email',
`comment`            varchar(1000)  NOT NULL                 COMMENT 'Comment text',
PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="User feedback about website";