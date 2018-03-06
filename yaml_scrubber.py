######################################
# Scrub YAML file for SQL tables     #
######################################

import re
from collections import defaultdict

__author__ = "jbrownlow"

sql_1 = """
INSERT INTO source.database
SELECT
    a.value_1,
    a.value_2
FROM
    white.tag a
LIMIT 100
"""

sql_2 = """
INSERT INTO stage.table
SELECT
    value_3,
    value_4
FROM
    white.label
"""

table_list = [
    'SOURCE.DATABASE',
    'STAGE.TABLE',
    'WHITE.LABEL'
]

class Dependency:

    def __init__(self):
        self.insert_tables = None
        self.dependent_tables = None

    def _get_upper(self, sql):
        return sql.upper()

    def _get_insert_tables(self, sql):
        regex_string = r'INSERT INTO (\b\w+\b\.\b\w+\b)'
        return re.findall(regex_string, sql)

    def _get_all_tables(self, sql):
        regex_string = r'\b\w+\b\.\b\w+\b'
        return re.findall(regex_string, sql)

    def _set_insert_tables(self, sql, full_list):
        potential_tables = self._get_insert_tables(sql)
        self.insert_tables = set(self._filter_tables(potential_tables, full_list))

    def _set_dependent_tables(self, sql, full_list):
        potential_tables = self._get_all_tables(sql)
        self.dependent_tables = set(self._filter_tables(potential_tables, full_list)) - self.insert_tables

    def _filter_tables(self, sub, full):
        return set(filter(lambda x: x in full, sub))

    def _get_dependency(self, sql, full_table):
        uppersql = self._get_upper(sql)
        self._set_insert_tables(uppersql, full_table)
        self._set_dependent_tables(uppersql, full_table)

        assert len(self.insert_tables) <= 1

        if self.insert_tables:
            self.insert_tables = list(self.insert_tables)
        else:
            self.dependent_tables = list()

        if self.dependent_tables:
            self.dependent_tables = list(self.dependent_tables)
        else:
            self.dependent_tables = list()

class NodeElement:

    def __init__(self):
        self.parent = None
        self.child = None

    def set_parent(self, parent):
        self.parent = parent

    def set_child(self, child):
        self.child = child

    def get_parent(self):
        return self.parent

    def get_child(self):
        return self.child

class GraphStructure(object):

    def __init__(self):
        self.graph = defaultdict(set)

    def add_edge(self, NE):
        self.graph[NE.parent].add(NE.child)

    def get_graph(self):
        return self.graph

class ProcessDependency(GraphStructure):

    def __init__(self):
        super(ProcessDependency, self).__init__()

    def _organize_dependency(self, DE):

        if DE.insert_tables and DE.dependent_tables:
            for dependent in DE.dependent_tables:
                self._set_node(DE.insert_tables[0], dependent)

        elif DE.insert_tables:
            self._set_node(DE.insert_tables[0], None)

    def _set_node(self, parent, child):
        NE = NodeElement()
        NE.set_parent(parent)
        NE.set_child(child)
        self.add_edge(NE)

D1 = Dependency()
D1._get_dependency(sql_1, table_list)

D2 = Dependency()
D2._get_dependency(sql_2, table_list)

P = ProcessDependency()
P._organize_dependency(D1)
P._organize_dependency(D2)

print(P.get_graph())




