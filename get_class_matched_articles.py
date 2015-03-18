#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import requests
import sys

class DBpediaSearcher:
    """
    Run query to Virtuoso SPARQL endpoint
    """
    
    def _get_dbpedia_url(self, language):
        return u'http://' + ('' if language == u'en' else language + u'.') + u'dbpedia.org'

    def query_endpoint(self, query, language):
        """
        Run a query to Virtuoso SPARQL endpoint with given language.
        Returns results when success, otherwise error stutus and message
        """
        params = {'query': query, 'format': 'json'}
        r = requests.get(self._get_dbpedia_url(language)+'/sparql', params=params)
        return r.json()['results']['bindings'] if r.ok else {'id_error': r.status_code, 'message': r.reason}

class ArticleExtractor:
    """
    Load Wikipedia articles with specific language and ontology class on DBpedia
    """
    
    def __init__(self, debug=True):
        self.searcher = DBPediaSearcher()
        self.debug = debug

    def _get_article_ids(language, ontology_class):
        query = """\
        SELECT ?id WHERE { 
          ?s a <http://dbpedia.org/ontology/%s> ;
          <http://dbpedia.org/ontology/wikiPageID> ?id .
        }\
        """ % (ontology_class) 
        r = self.searcher.run_query(qury, language)
        if r.has_key(id_error):
            print 'ERROR: Cannot access SPARQL endpoint'
            return 1
        article_ids = [i['id']['value'] for i in r]
        return article_ids
        
    def extract_articles(language, ontology_class, corpus_dir, output_dir):
        """
        Extract Wikipedia articles matching given ontology class on DBpedia with specific language.
        Matched articles are copied to `output_dir`
        """
        article_ids = self._get_article_ids(language, ontology_class)
        for path, subdirs, files in os.walk(corpus_dir):
            for name in files:
                f = os.path.join(path, name)
                with open(f) as i:
                    content = ''.join(i.readlines())
                match = re.search('id="([^"]+)"', content)
                current_id = match.group(1)
                if self.debug:
                    print 'File = [{0}] - Wiki ID = [{1}]'.format(f, current_id)
                if current_id in article_ids:
                    shutil.copy(f, output_dir)
                    if self.debug:
                        print 'MATCHED! [{0}]'.format(content)
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'Usage: {0} <LANGUAGE> <ONTOLOGY_CLASS> <CORPUS_DIR> <OUTPUT_DIR>'.format(__file__)
        sys.exit(1)
    else:
        loader = ArticleExtractor()
        loader.extract_articles(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
