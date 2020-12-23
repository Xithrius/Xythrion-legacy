\c xythrion;

CREATE TABLE IF NOT EXISTS Dates(
    identification serial PRIMARY KEY,
    t TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    id BIGINT,
    name TEXT
);

CREATE TABLE IF NOT EXISTS Notes(
    identification serial PRIMARY KEY,
    user_id BIGINT,
    readers BIGINT[],
    writers BIGINT[],
    content TEXT[]
);

CREATE TABLE IF NOT EXISTS Blocked_Guilds(
    identification serial PRIMARY KEY,
    guild_id BIGINT
);

CREATE TABLE IF NOT EXISTS Blocked_Users(
    identification serial PRIMARY KEY,
    user_id BIGINT
);
