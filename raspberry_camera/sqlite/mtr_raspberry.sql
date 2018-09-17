

DROP TABLE IF EXISTS mra_portfolio_photos;
DROP TABLE IF EXISTS mra_portfolios;
DROP TABLE IF EXISTS mra_photo_hashtag_ids;
DROP TABLE IF EXISTS mra_photos;
DROP TABLE IF EXISTS mra_cache_counter;
DROP TABLE IF EXISTS mra_hashtags;

CREATE TABLE `mra_hashtags`
 (`hashtag_id_local` INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT,
  `hashtag` text DEFAULT NULL, 
   `created_at` INTEGER DEFAULT CURRENT_TIMESTAMP );



CREATE TABLE `mra_cache_counter` 
( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
 `created_at` INTEGER DEFAULT NULL,  -- should be in number of day or just 20180818
 `action` text DEFAULT NULL, --  COMMENT 'photo_taken,uploaded'
  `counter` INTEGER DEFAULT NULL);

CREATE UNIQUE INDEX `cache_counter_unique` ON mra_cache_counter (`created_at`,`action`);

CREATE TABLE `mra_photos` 
(  `id_local` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	`day_taken_at` INTEGER DEFAULT NULL, 
 `hour_taken_at` text DEFAULT NULL,  
 `filename` text DEFAULT NULL,  
 `uploaded_at` text DEFAULT NULL, 
  `photo_id_global` INTEGER DEFAULT NULL, 
 `deleted_at` text DEFAULT NULL,
  `to_upload` integer DEFAULT 1);

CREATE UNIQUE INDEX `photo_filename_unique` ON mra_photos (`filename`);



CREATE TABLE `mra_photo_hashtag_ids`
 (  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
  `photo_id_local` INTEGER DEFAULT NULL,  
  `hashtag_id` INTEGER DEFAULT NULL, 
   `type` INTEGER DEFAULT NULL,  
   FOREIGN KEY(photo_id_local) REFERENCES mra_photos(id_local), 
    FOREIGN KEY(hashtag_id) REFERENCES mra_hashtags(hashtag_id_local));



CREATE TABLE `mra_portfolios` ( 
 `mtr_portfolio_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
 `name` text DEFAULT NULL, 
  `created_at` text DEFAULT NULL,
   `datou_ids` text DEFAULT NULL, -- COMMENT 'Empty if no data to treat',
  `datou_launched_at` text DEFAULT NULL);

CREATE UNIQUE INDEX `mra_portfolios_unique` ON mra_portfolios (`name`);



CREATE TABLE `mra_portfolio_photos` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `id_local_photo` INTEGER DEFAULT NULL,
  `portfolio_id` INTEGER DEFAULT NULL,
  `created_at` text DEFAULT NULL,
   FOREIGN KEY(id_local_photo) REFERENCES mra_photos(id_local), 
    FOREIGN KEY(portfolio_id) REFERENCES mra_portfolios(mtr_portfolio_id));

CREATE UNIQUE INDEX `mra_portfolio_photos_unique` ON mra_portfolio_photos (`id_local_photo`,`portfolio_id`);



-- On dirait que cette syntaxe convient, ce serait peut etre mieux :
-- CREATE TABLE contact_groups (contact_id integer,group_id integer,PRIMARY KEY (contact_id, group_id),FOREIGN KEY (contact_id) REFERENCES contacts (contact_id) ON DELETE CASCADE ON UPDATE NO ACTION,FOREIGN KEY (group_id) REFERENCES groups (group_id) ON DELETE CASCADE ON UPDATE NO ACTION);



-- SELECT * FROM sqlite_master;


