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


def load_cn_index() -> dict:
    index_file = os.path.join(os.path.dirname(__file__), 'cn_index.json')
    return load_json_file(index_file)


@click.command()
@click.argument('name')
def main(name: str):
    """
    `name` Elastic App Search Name

    使用针对中文优化 index 配置替换 Elastic App Search 的默认配置

    此脚本仅允许在创建 Elastic App Search 之后立即使用。
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
