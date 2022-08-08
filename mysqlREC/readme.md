## **MySQL** database container

init.sql contains the initialization script used during the first initialization of the database

Database fields description:

| Column name       | Type          | Description                                            |
|-------------------|---------------|--------------------------------------------------------|
| keyid             | varchar(255)  | unique key                                             |
| rec_rank          | DECIMAL(16,8) | item rank (not used)                                   |
| itemType          | varchar(255)  | Type of the item                                       |
| source            | varchar(1000) | source (git,zotero, arxiv)                             |
| title             | text          | Title text                                             |
| descrptn          | text          | abstract/description                                   |
| dateMod           | datetime      | Item generation date                                   |
| authors           | text,         | authors                                                |
| urllink           | text          | link to the resource                                   |
| tags              | text,         | tags list                                              |
| bookmarkflag      | boolean       | boolean bookmark flag                                  |
| views             | int(11)       | number of views                                        |
| score             | float(40,8)   | score  based on similarity with user profile           |
| rating            | int(11)       | user rating of item                                    |
| doc_url           | text,         | document url from zotero                               |
| snoozeval_days    | int(11),      | number of days item is snoozed for                     |
| snoozed_date      | datetime,     | Date when item is snoozed                              |
| snooze_priority   | int(11)       | Snooze priority value                                  |
| deleted_tag       | boolean       | item is deleted boolean                                |
| repetitions       | int(11)       | sm2(repetition)                                        |
| quality           | int(11),      | sm2(quality)                                           |
| nxt_interval      | int(11),      | sm2(next_interval -not used)                           |
| previous_interval | int(11)       | sm2(interval)                                          |
| curr_ef           | DECIMAL(8,4), | sm2(ease facot-not used)                               |
| previous_ef       | DECIMAL(8,4)  | sm2 (previous ease factor)                             |
| scheduled_date    | DATE,         | Next scheduled date of the item based on sm2like logic |
| displaying_date   | DATE,         | Latest date on which the item was displayed            |
| curr_status       | text,         | status of the item for re-recommendation               |
| needs_update_flag | boolean       | not used                                               |