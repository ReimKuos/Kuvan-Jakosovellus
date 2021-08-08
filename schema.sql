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
    public BOOLEAN,
    visible BOOLEAN,
    group_name VARCHAR (50),
    description TEXT,
    num_posts INTEGER,
    UNIQUE(group_name)
);

CREATE TABLE members (
    member_id INTEGER,
    group_id INTEGER
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

CREATE TABLE adminastrators (
    group_id INTEGER,
    adminastrator_id INTEGER
);

CREATE TABLE banned_members (
    banned_from_id INTEGER,
    banned_id INTEGER,
    state BOOLEAN
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    comment_on_post BOOLEAN,
    visible BOOLEAN,
    removed BOOLEAN,
    commenter_id INTEGER,
    commented_id INTEGER,
    comment TEXT
);
