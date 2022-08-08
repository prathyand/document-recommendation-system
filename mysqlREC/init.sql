SET AUTOCOMMIT = 0;
START TRANSACTION;

SET time_zone = 'US/Eastern';

CREATE TABLE recom(
    keyid varchar(255) NOT NULL PRIMARY KEY,
    rec_rank DECIMAL(16,8) DEFAULT 00000000.00000000,
    itemType varchar(255) NOT NULL,
    source varchar(1000) NOT NULL,
    title text NOT NULL,
    descrptn text NOT NULL,
    dateMod datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    authors text,
    urllink text NOT NULL,
    tags text,
    bookmarkflag boolean default False,
    views int(11) default 0,
    score float(40,8) default 0,
    rating int(11) default 0,
    doc_url text,
    snoozeval_days int(11),
    snoozed_date datetime,
    snooze_priority int(11) default -1,
    deleted_tag boolean default False,
    repetitions int(11) default 0,
    quality int(11),
    nxt_interval int(11),
    previous_interval int(11) default 0,
    curr_ef DECIMAL(8,4),
    previous_ef DECIMAL(8,4) default 2.5,
    scheduled_date DATE,
    displaying_date DATE,
    curr_status text,
    needs_update_flag boolean default False
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE user_intr (
interactionID int UNSIGNED PRIMARY KEY AUTO_INCREMENT,
keyid varchar(255) NOT NULL,
CONSTRAINT FK_user_intr FOREIGN KEY (keyid) REFERENCES recom(keyid),
interaction_type text NOT NULL,
interaction_timestamp datetime NOT NULL 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

COMMIT;
