-- create database -----------------------------------------------------------------

CREATE DATABASE auth_app;

-- connect to the database ---------------------------------------------------------

\connect auth_app;

-- create table schema ------------------------------------------------------------

CREATE SCHEMA authentication;

-- set search path to the schema

set search_path TO authentication;

-- create app credentials table ----------------------------------------------------

CREATE TABLE IF NOT EXISTS authentication.app (
    app_uid         UUID           NOT NULL    PRIMARY KEY,
    client_id       varchar( 64 )  NOT NULL,
    client_secret   varchar( 64 )  NOT NULL
);

-- create client table -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS authentication.client (
    client_uid      UUID           NOT NULL    PRIMARY KEY,
    client_status   varchar(16)    NOT NULL    DEFAULT 'ACTIVE'
);

-- create auth_token_table ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS authentication.account (
    account_uid     UUID           NOT NULL    PRIMARY KEY,
    client_uid      UUID           NOT NULL    REFERENCES client( client_uid ),
    access_token    varchar( 2044 ) NOT NULL,
    refresh_token   varchar( 2044 ) NOT NULL
);

-- create user ---------------------------------------------------------------------

CREATE ROLE true_layer_app WITH SUPERUSER CREATEDB LOGIN PASSWORD 'true_layer_app';

-- grant usage of schema to user ---------------------------------------------------

GRANT USAGE ON SCHEMA authentication TO true_layer_app;

-- grant usage on the tables to 'true_layer_app' -----------------------------------

GRANT ALL PRIVILEGES ON TABLE authentication.app TO true_layer_app;

GRANT ALL PRIVILEGES ON TABLE authentication.client TO true_layer_app;

GRANT ALL PRIVILEGES ON TABLE authentication.account TO true_layer_app;

-- insert the app credentials ------------------------------------------------------

INSERT INTO authentication.app (app_uid, client_id, client_secret) VALUES ('f3235a6e-1140-4c14-8350-aad2be7aee18', 'meowmeowcat-041410', '5938fed7-afc3-40ad-80a4-f3fe38865d7c');

------------------------------------------------------------------------------------