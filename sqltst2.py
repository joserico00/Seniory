#crear database

#tiene los funciones para camiar el database
import sqlite3

conn = sqlite3.connect('central.db')
query = (''' CREATE TABLE ELDERS
        (
        ID INT
        NAME  TEXT NOT NULL,
        CITY TEXT NOT NULL,
        ADRESS  TEXT,
        EMAIL TEXT,
        PHONENNUMBER TEXT,
        GENDER CHAR
        );

                ''')
query2 = ('''CREATE TABLE `Elders` 
  (
	`id` INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	`name` VARCHAR(40) NOT NULL,
	`gender` CHAR NOT NULL,
	`city` CHAR(20) NOT NULL,
	`address` TEXT NOT NULL,
	`email` VARCHAR(60),
	`phone_number` VARCHAR(16) NOT NULL,
	`need_help` BOOLEAN NOT NULL DEFAULT 0,
    `volunteer_helping` Integer DEFAULT -1
    `HELP` TEXT 
);''')

conn.execute(query2)

#conn = sqlite3.connect('caregiver.db')
query2 = ('''CREATE TABLE `caregiver` 
  (
	`id` INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	`name` VARCHAR(40) NOT NULL,
	`gender` CHAR NOT NULL,
	`city` CHAR(20) NOT NULL,
	`address` TEXT NOT NULL,
	`email` VARCHAR(60) NOT NULL,
	`phone_number` VARCHAR(16) NOT NULL,
    `availability` BOOLEAN NOT NULL  DEFAULT 1
);''')

conn.execute(query2)
conn.close()
