#!/usr/bin/env python3
import json
import os
from pprint import pprint

import click
from elasticsearch.client import Elasticsearch


def load_json_file(file: str) -> dict:
    with open(file) as fp:
        return json.load(fp)


def load_es_config() -> dict:
    es_file = os.path.join(os.path.dirname(__file__), 'es.json')
    return load_json_file(es_file)


def load_cn_settings() -> dict:
    settings_file = os.path.join(os.path.dirname(__file__), 'cn_settings.json')
    return load_json_file(settings_file)


def load_cn_mappings() -> dict:
    mappings_file = os.path.join(os.path.dirname(__file__), 'cn_mappings.json')
    return load_json_file(mappings_file)


def load_cn_index() -> dict:
    index_file = os.path.join(os.path.dirname(__file__), 'cn_index.json')
    return load_json_file(index_file)


@click.command()
@click.argument('name')
def main(name: str):
    """
    `name` Elastic App Search Name
    """
    app_search_index = f'.ent-search-engine-documents-{name}'
    es = Elasticsearch(**load_es_config())
    index = es.indices.get(app_search_index)
    pprint(index)

    # see doc:
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer.html
    cn_index = load_cn_index()

    es.indices.delete(app_search_index)
    es.indices.create(app_search_index, cn_index)

    index = es.indices.get(app_search_index)
    pprint(index)


if __name__ == "__main__":
    main()
