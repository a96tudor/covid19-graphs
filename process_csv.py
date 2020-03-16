import csv
import argparse
import os
import sys
import logging

import database_engine as de


def parse_arguments():
    parser = argparse.ArgumentParser('Insert data from csvs')

    parser.add_argument('data', help='Path to the data directory')
    parser.add_argument('--insert-territories', action='store_true',
                        help='Whether to insert the territories as well or '
                             'not.')
    parser.add_argument('--host', default='127.0.0.1',
                        help='Host where the neo4j server is running.')
    parser.add_argument('--port', default='7687',
                        help='Port where the neo4j server is running.')
    parser.add_argument('--user', default='neo4j',
                        help='User used to connect to the neo4j server.')
    parser.add_argument('--password', default='neo4j',
                        help='Password used to connect to the neo4j server.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Whether to log the inner workings of the '
                             'script or not.')

    return parser.parse_args()


def _insert_data(path, insert_fn):
    with open(path) as stream:
        data = csv.DictReader(stream)
        insert_fn(data)


def insert_territories(data_dir, database_handler):
    # Inserting countries first
    logging.info('Inserting countries...')
    path = os.path.join(data_dir, 'countries.csv')
    _insert_data(path, database_handler.insert_countries)

    # Inserting regions now
    logging.info('Inserting Regions...')
    path = os.path.join(data_dir, 'regions.csv')
    _insert_data(path, database_handler.insert_regions)

    # Inserting counties
    logging.info('Inserting counties...')
    path = os.path.join(data_dir, 'counties.csv')
    _insert_data(path, database_handler.insert_counties)

    # Inserting municipalities
    logging.info('Inserting municipalities...')
    path = os.path.join(data_dir, 'municipalities.csv')
    _insert_data(path, database_handler.insert_municipalities)

    logging.info('Inserting cities...')
    path = os.path.join(data_dir, 'cities.csv')
    _insert_data(path, database_handler.insert_cities)

    logging.info('Inserting communes...')
    path = os.path.join(data_dir, 'communes.csv')
    _insert_data(path, database_handler.insert_communes)

    logging.info('Finished inserting territories!')


if __name__ == '__main__':
    args = parse_arguments()

    if args.verbose:
        logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    database_handler = de.DatabaseHandler(
        host=args.host, port=args.port, user=args.user, password=args.password,
    )
    logging.info('Connected to the database hosted at {} on port {}'.format(
        args.host, args.port
    ))

    if args.insert_territories:
        insert_territories(args.data, database_handler)

    logging.info('DONE!')
