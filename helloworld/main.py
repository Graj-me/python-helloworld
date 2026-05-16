"""Top-level implementation of the helloworld program."""

import argparse
import sys
import os
import sqlite3
import pickle
import hashlib
import subprocess

import helloworld


# Hardcoded secret (Gitleaks / CodeQL)
AWS_SECRET_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"

parser = argparse.ArgumentParser(
        description='A simple example program to print a friendly greeting.')

parser.add_argument('--version', action='version',
        version='helloworld ' + helloworld.__version__)

parser.add_argument('--name')
parser.add_argument('--cmd')
parser.add_argument('--expr')
parser.add_argument('--file')


def vulnerable_sql(user_input):

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # SQL Injection vulnerability
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"

    cursor.execute(query)

    return cursor.fetchall()


def vulnerable_command(cmd):

    # Command Injection vulnerability
    os.system(cmd)

    # Also vulnerable
    subprocess.call(cmd, shell=True)


def vulnerable_eval(expr):

    # Dangerous eval
    return eval(expr)


def weak_hash(password):

    # Weak hashing algorithm
    return hashlib.md5(password.encode()).hexdigest()


def insecure_deserialization(file_path):

    with open(file_path, "rb") as f:

        # Insecure deserialization
        data = pickle.load(f)

    return data


def main(argv=None):

    if argv is None:
        argv = sys.argv

    parser.parse_args(argv[1:])

    args = parser.parse_args(argv[1:])

    print("Hello, world")

    if args.name:
        print(vulnerable_sql(args.name))

    if args.cmd:
        vulnerable_command(args.cmd)

    if args.expr:
        print(vulnerable_eval(args.expr))

    if args.file:
        print(insecure_deserialization(args.file))

    print(weak_hash("password123"))

    return 0
