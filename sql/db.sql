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
        `MACs`        MEDIUMTEXT NOT NULL,
        `comments`    MEDIUMTEXT,
        `modifiedTS`  TIMESTAMP,
        `addedTS`     TIMESTAMP NOT NULL,
        `deletedTS`   TIMESTAMP,
        `deleted`     ENUM ('NO', 'YES') NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

