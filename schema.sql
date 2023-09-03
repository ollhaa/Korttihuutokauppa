DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS auctions;
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS feedbacks;
DROP TABLE IF EXISTS bids;
DROP TABLE IF EXISTS messages;

CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username VARCHAR(12) NOT NULL, 
    password TEXT NOT NULL,
    mail TEXT NOT NULL,
    created_at TIMESTAMP, 
    last_modified TIMESTAMP, 
    admin BOOLEAN DEFAULT False
);

CREATE TABLE auctions (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	title VARCHAR(40) NOT NULL,
	content VARCHAR(200),
	_class VARCHAR(20),
	condition VARCHAR(20),
	city VARCHAR(20),
	bid_start NUMERIC DEFAULT 1,
	created_at TIMESTAMP, 
	ending_time TIMESTAMP NOT NULL,
	active BOOLEAN DEFAULT True,
	winner_id INTEGER, 
	solved  BOOLEAN DEFAULT False
);

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
	auction_id INTEGER REFERENCES auctions, 
	name TEXT, 
	data BYTEA);
	
CREATE TABLE feedbacks (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	feedback VARCHAR(200),
	feedback_time TIMESTAMP 
);

CREATE TABLE bids (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	auction_id INTEGER REFERENCES auctions,
	bid NUMERIC NOT NULL,
	bid_time TIMESTAMP 
);


CREATE TABLE messages (
	id SERIAL PRIMARY KEY,
	user_id_from INTEGER REFERENCES users,
	user_id_to INTEGER REFERENCES users,
	message VARCHAR(100),
	message_sent TIMESTAMP
);

INSERT INTO users (username, password,mail, created_at, last_modified, admin) VALUES ("Huuto", "Kauppa", "admin@korttihuutokauppa.fi", NOW(), NOW(), False);