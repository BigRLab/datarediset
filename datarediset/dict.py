from uuid import uuid4
from weakref import finalize

from redis import StrictRedis

from datarediset.exceptions import *

class Dict:
    def __init__(self, name=None, conn=None, db=None, **kwargs):
        if db is not None and conn is not None:
            raise ConnectionAmbiguity('You must provide a redis connection OR a\
                                      database, not both')
        if db is None and conn is None:
            self.conn = StrictRedis(db=0, **kwargs)
            self.temporary = True
        elif db is None and conn is not None:
            self.conn = conn
        elif db is not None and conn is None:
            self.conn = StrictRedis(db=db, **kwargs)
            self.temporary = True
        if name is None:
            self.name = uuid4()
        else:
            self.name = name

    def keys(self):
        return [x.decode('utf-8') for x in self.conn.hkeys(self.name)]

    def delete(self, val):
        if isinstance(val, str):
            if self.conn.hexists(self.name, val):
                self.conn.hdel(self.name, val)
            else:
                raise KeyError()
        else:
            raise TypeError

    def __hash__(self):
        return hash(self.name, self.conn)

    def __getitem__(self, item):
        if isinstance(item, str):
            if self.conn.hexists(self.name, item):
                return self.conn.hget(self.name, item).decode('utf-8')
            else:
                raise KeyError('deleting non-existent key')
        else:
            raise TypeError('key and value must be utf-8 strings')

    def __setitem__(self, key, value):
        if isinstance(key, str) and isinstance(value, str):
            if key != '' and value != '':
                self.conn.hset(self.name, key, value)
            elif key == '' and value == '':
                raise TypeError('key and value strings are empty')
            elif key == '':
                raise EmptyKey('key is an empty string')
            elif value == '':
                raise EmptyValue('value is an empty string')
        else:
            raise TypeError('key and value must be utf-8 strings')

    def __repr__(self):
        return '<datarediset.Dict(name={}, conn={})>'.format(
            self.name,
            self.conn,
        )

    def __contains__(self, item):
        if isinstance(item, str):
            return self.conn.hexists(self.name, item)
        else:
            raise TypeError

    def __len__(self):
        return len(self.get_keys)

    def __enter__(self):
        if self._temporary:
            return self
        else:
            raise RuntimeError('dict must not have a foreign connection in a\
                               "with" statement.')
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.conn.delete(self.name)
