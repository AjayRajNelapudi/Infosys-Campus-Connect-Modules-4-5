CREATE DATABASE Bank;

USE Bank;

CREATE TABLE Customer (
    c_id INTEGER PRIMARY KEY,
    c_password VARCHAR(20) NOT NULL,
    c_name VARCHAR(50) NOT NULL,
    c_addr VARCHAR(100) NOT NULL
);

CREATE TABLE Account (
    acc_no INTEGER PRIMARY KEY,
    acc_balance BIGINT NOT NULL,
    acc_type VARCHAR(10) NOT NULL
);

CREATE TABLE CustomerAccount (
    c_id INTEGER NOT NULL,
    acc_no INTEGER NOT NULL
);

ALTER TABLE CustomerAccount
ADD CONSTRAINT c_id_CustomerAccount FOREIGN KEY(c_id) REFERENCES Customer(c_id),
ADD CONSTRAINT acc_no_CustomerAccount FOREIGN KEY(acc_no) REFERENCES Account(acc_no);

CREATE TABLE AccountTransaction (
    acc_no INTEGER NOT NULL,
    t_type VARCHAR(10) NOT NULL,
    t_amount BIGINT NOT NULL,
    t_timestamp TIMESTAMP NOT NULL
);

ALTER TABLE AccountTransaction
ADD CONSTRAINT acc_no_AccountTransaction FOREIGN KEY(acc_no) REFERENCES Account(acc_no);

CREATE TABLE Administrator (
    admin_id INTEGER PRIMARY KEY,
    admin_password VARCHAR(20) NOT NULL
);

CREATE TABLE ClosedAccount (
    acc_no INTEGER PRIMARY KEY,
    closing_date TIMESTAMP NOT NULL
);

INSERT INTO Administrator
VALUES
(1, 'key');