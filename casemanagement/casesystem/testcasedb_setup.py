import os
from collections import OrderedDict

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import ConnectionHandler
from django.test.runner import DiscoverRunner
from django.test.utils import get_unique_databases_and_mirrors

from settings.development import BASE_DIR

DEFAULT_DB_ALIAS = 'default'


class CustomConnectionHandler(ConnectionHandler):

    def databases(self):
        if self._databases is None:
            self._databases = settings.DATABASES
        if self._databases == {}:
            self._databases = {
                DEFAULT_DB_ALIAS: {
                    'ENGINE': 'django.db.backends.dummy',
                },
            }
        if DEFAULT_DB_ALIAS not in self._databases:
            raise ImproperlyConfigured("You must define a '%s' database."
                                       % DEFAULT_DB_ALIAS)
        if self._databases[DEFAULT_DB_ALIAS] == {}:
            self._databases[DEFAULT_DB_ALIAS]['ENGINE'] =\
                'django.db.backends.dummy'
        return self._databases


connections = ConnectionHandler()


def _setup_databases(verbosity, interactive, keepdb=False, debug_sql=False,
                     parallel=0, aliases=None, **kwargs):
    """Create the test databases."""
    mirrored_aliases = {}

    # overriding the test database with localsetup
    test_databases = OrderedDict([((os.path.join(BASE_DIR, 'db.sqlite3'),
                                    'test_database'),
                                   (os.path.join(BASE_DIR, 'db.sqlite3'),
                                    {'test_database'}))])

    test_databases, mirrored_aliases = get_unique_databases_and_mirrors(
                                                            aliases)
    old_names = []
    for db_name, aliases in test_databases.values():
        first_alias = None
        for alias in aliases:
            connection = connections[alias]
            old_names.append((connection, db_name, first_alias is None))

            # Actually create the database for the first connection
            if first_alias is None:
                first_alias = alias
                connection.creation.create_test_db(
                    verbosity=verbosity,
                    autoclobber=not interactive,
                    keepdb=keepdb,
                    serialize=connection.settings_dict.get('TEST', {}).get(
                        'SERIALIZE', True),
                )
                if parallel > 1:
                    for index in range(parallel):
                        connection.creation.clone_test_db(
                            suffix=str(index + 1),
                            verbosity=verbosity,
                            keepdb=keepdb,
                        )
            # Configure all other connections as mirrors of the first one
            else:
                connections[alias].creation.set_as_test_mirror(
                    connections[first_alias].settings_dict)

    # Configure the test mirrors.
    for alias, mirror_alias in mirrored_aliases.items():
        connections[alias].creation.set_as_test_mirror(
            connections[mirror_alias].settings_dict)

    if debug_sql:
        for alias in connections:
            connections[alias].force_debug_cursor = True

    return old_names


class CustomDiscoverRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        return _setup_databases(
            self.verbosity, self.interactive, self.keepdb, self.debug_sql,
            self.parallel, **kwargs
        )
