-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
        `id`            INT NOT NULL AUTO_INCREMENT,
        `username`      VARCHAR(64),
        `name`          VARCHAR(64),
        `email`         VARCHAR(64),
        `password_hash` VARCHAR(128),
        `member_since`  TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        `last_seen`     TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        `confirmed`     BOOL DEFAULT FALSE,
        `role_id`       INT NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


INSERT INTO `users` (
        username, name, email, role_id
)
VALUES
        ('steve','Steve Clement','steve@localhost.lu',2),
        ('john','John Appleseed','john@example.com',1);

-- --------------------------------------------------------

--
-- Table structure for table `ipv4s`
--

CREATE TABLE `ipv4s` (
        `id`          INT NOT NULL AUTO_INCREMENT,
        `ip`          INT UNSIGNED NOT NULL,
        `subnet`      TINYINT UNSIGNED NOT NULL,
        `hostname`    VARCHAR(255),
        `aliases`     VARCHAR(255),
        `vlan`        SMALLINT,
        `services`    TEXT,
        `v6`          ENUM ('NO', 'YES') NOT NULL,
        `dns`         ENUM ('NO', 'YES') NOT NULL,
        `ptr`         ENUM ('NO', 'YES') NOT NULL,
        `dhcp`        ENUM ('NO', 'YES') NOT NULL,
        `munin`       ENUM ('NO', 'YES') NOT NULL,
        `wiki`        ENUM ('NO', 'YES') NOT NULL,
        `vm`          ENUM ('NO', 'YES') NOT NULL,
        `backup`      ENUM ('NO', 'YES') NOT NULL,
        `mailOut`     ENUM ('NO', 'YES') NOT NULL,
        `syslogOut`   ENUM ('NO', 'YES') NOT NULL,
        `pingeable`   ENUM ('NO', 'YES') NOT NULL,
        `MACs`        MEDIUMTEXT NOT NULL,
        `comments`    MEDIUMTEXT,
        `modifiedTS`  TIMESTAMP NULL DEFAULT NULL,
        `addedTS`     TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        `deletedTS`   TIMESTAMP NULL DEFAULT NULL,
        `deleted`     ENUM ('NO', 'YES') NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- 127.0.0.1 sample entry
--

INSERT INTO `ipv4s` (
        ip, subnet, hostname, v6, dns, ptr, dhcp, munin, wiki, vm, backup, mailOut, syslogOut, pingeable, MACs, comments, deleted
)
VALUES (
        INET_ATON('127.0.0.1'), 8, 'localhost', 'NO', 'NO', 'NO', 'NO', 'NO', 'NO','NO','NO','NO','NO', 'YES', 'MAC-lo|00:00:00:00:00:01', 'Sample localhost entry', 'NO'
);
