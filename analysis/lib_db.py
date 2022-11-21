import toml
import os
import json
import psycopg2
import hashlib


def cache():
    def decorator(func):
        def wrapper(*args, **kwargs):

            filename = func.__name__

            if not os.path.isdir(".cache"):
                os.mkdir(".cache")
            client: DBClient = args[0]
            hash_str = str(client.config) + str(args[1:])
            digest = hashlib.sha256(str.encode(hash_str)).hexdigest()
            cache_file = f'.cache/{filename}-{digest}.json'

            if os.path.isfile(cache_file):
                print(f"Using cache file {cache_file} for {filename}...")
                with open(cache_file, 'r') as f:
                    return json.load(f)

            result = func(*args, **kwargs)

            with open(cache_file, 'w') as f:
                json.dump(result, f)

            return result

        return wrapper

    return decorator


class DBClient:
    config = None
    conn = None

    def __init__(self, config_file: str = "./db.toml"):
        print("Initializing database client...")

        self.config = toml.load(config_file)['psql']
        self.conn = psycopg2.connect(
            host=self.config['host'],
            port=self.config['port'],
            database=self.config['database'],
            user=self.config['user'],
            password=self.config['password'],
        )
        cur = self.conn.cursor()
        cur.execute("SET TIMEZONE='Europe/Berlin';")

    @cache()
    def query(self, query):
        print("Running custom query...")
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()
