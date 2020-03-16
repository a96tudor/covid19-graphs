import json

import neo4j


class DatabaseEntry:

    def __init__(self, name, labels, data):
        self.name = name if name else ''
        self.data = data
        self.labels = labels

    def __str__(self):
        if self.name != '':
            query_template = '`{name}`:{labels}{data}'
        else:
            query_template = '{name}:{labels}{data}'
        return query_template.format(
            name=self.name,
            labels=':'.join(self.labels),
            data='{{{}}}'.format(
                ', '.join(['{}:"{}"'.format(k, v)
                           for k, v in self.data.items()],
                          )
            ),
        )


class DatabaseHandler:
    URI_TEMPLATE = 'bolt://{host}:{port}'
    INSERT_QUERY_TEMPLATE = 'create {}'
    RELATION_QUERY_TEMPLATE = (
        'match (n{left}), (m{right}) create (n)-[:{rel}]->(m)'
    )

    def __init__(self, host, port, user, password):
        self.uri = self.URI_TEMPLATE.format(host=host, port=port)
        self.auth = (user, password)

    def _get_query_insert(self, entries):
        return self.INSERT_QUERY_TEMPLATE.format(
            '({})'.format('), ('.join([str(e) for e in entries])
        ))

    def _insert(self, entries):
        query = self._get_query_insert(entries)

        driver = neo4j.GraphDatabase.driver(
            self.uri, auth=neo4j.basic_auth(*self.auth), encrypted=False,
        )

        with driver.session() as session:
            session.run(query)

    def _get_query_add_relation(self, entry_left, entry_right, rel_type):
        return self.RELATION_QUERY_TEMPLATE.format(
            left=str(entry_left), right=str(entry_right), rel=rel_type,
        )

    def _add_relationship(self, left, right, rel_type):
        query = self._get_query_add_relation(left, right, rel_type)

        driver = neo4j.GraphDatabase.driver(
            self.uri, auth=neo4j.basic_auth(*self.auth), encrypted=False,
        )

        with driver.session() as session:
            session.run(query)

    def _insert_territories(self, data, keys_to_consider, label):
        entries = []

        for d in data:
            entries.append(DatabaseEntry(
                name=None,
                labels=[label, 'Territory'],
                data={k: d[k] for k in keys_to_consider}
            ))

        self._insert(entries)

    def insert_countries(self, countries):
        self._insert_territories(countries, countries.fieldnames, 'Country')

    def insert_regions(self, regions):
        regions = list(regions)
        self._insert_territories(
            regions, ['name', 'local_name', 'nuts', 'plus_id'],
            'Region'
        )

        # And now connections to countries
        for r in regions:
            left = DatabaseEntry(None, ['Region'], {'nuts': r['nuts']})
            right = DatabaseEntry(
                None, ['Country'], {'nuts': r['IS_IN.country']},
            )
            rel_type = 'IS_IN_COUNTRY'

            self._add_relationship(left, right, rel_type)

    def insert_counties(self, counties):
        counties = list(counties)

        self._insert_territories(
            counties, ['name', 'local_name', 'nuts', 'plus_id'], 'County',
        )

        # And now add the connections to regions
        for c in counties:
            left = DatabaseEntry(None, ['County'], {'nuts': c['nuts']})
            right = DatabaseEntry(
                None, ['Region'], {'nuts': c['IS_IN.region']},
            )
            rel_type = 'IS_IN_REGION'

            self._add_relationship(left, right, rel_type)

    def insert_municipalities(self, municipalities):
        municipalities = list(municipalities)

        self._insert_territories(
            municipalities, ['name', 'local_name', 'siruta', 'plus_id'],
            'Municipality',
        )

        # And now add the connections to counties
        for m in municipalities:
            left = DatabaseEntry(None, ['Municipality'],
                                 {'siruta': m['siruta']})
            right = DatabaseEntry(
                None, ['County'], {'nuts': m['IS_IN.county']},
            )
            rel_type = 'IS_IN_COUNTY'

            self._add_relationship(left, right, rel_type)

    def insert_cities(self, cities):
        cities = list(cities)

        self._insert_territories(
            cities, ['name', 'local_name', 'siruta', 'plus_id'], 'City',
        )

        # And now add the connections to counties
        for c in cities:
            left = DatabaseEntry(None, ['City'],
                                 {'siruta': c['siruta']})
            right = DatabaseEntry(None, ['County'],
                {'nuts': c['IS_IN.county']}, )
            rel_type = 'IS_IN_COUNTY'

            self._add_relationship(left, right, rel_type)

    def insert_communes(self, communes):
        communes = list(communes)

        self._insert_territories(
            communes, ['name', 'local_name', 'siruta', 'plus_id'], 'Commune',
        )

        # And now add the connections to counties
        for c in communes:
            left = DatabaseEntry(None, ['Commune'],
                                 {'siruta': c['siruta']})
            right = DatabaseEntry(None, ['County'],
                                  {'nuts': c['IS_IN.county']},
                                  )
            rel_type = 'IS_IN_COUNTY'

            self._add_relationship(left, right, rel_type)
