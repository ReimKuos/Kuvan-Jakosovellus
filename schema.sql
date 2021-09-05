CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR (50),
    name VARCHAR (50),
    password TEXT,
    UNIQUE(user_id)
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER,
    creation_time TIMESTAMP,
    visible BOOLEAN,
    group_name VARCHAR (50),
    description TEXT,
    UNIQUE(group_name)
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER,
    group_id INTEGER,
    creation_time TIMESTAMP,
    visible BOOLEAN,
    removed BOOLEAN,
    post_title VARCHAR (50),
    picture BYTEA
);


CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    visible BOOLEAN,
    commenter_id INTEGER,
    commented_id INTEGER,
    comment TEXT
);

CREATE TABLE likes (
    post_id INTEGER,
    liker_id INTEGER,
    active BOOLEAN
);
