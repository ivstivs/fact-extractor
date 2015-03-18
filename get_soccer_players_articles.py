#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import requests
import sys


DEBUG = True
class DBpediaSearcher:
    """
    """
    
    def _get_dbpedia_url(self, language):
        return u'http://' + ('' if language == u'en' else language + u'.') + u'dbpedia.org'

    def query_endpoint(self, query, language):
        """
        Run a query to Virtuoso SPARQL endpoint with given language
        """
        params = {'query': query, 'format': 'json'}
        r = requests.get(self._get_dbpedia_url(language)+'/sparql', params=params)
        return r.json()['results']['bindings'] if r.ok else {'id_error': r.status_code, 'message': r.reason}

class ArticleLoader:
    """
    """
    def __init__(self):
        self.searcher = DBPediaSearcher()
        
    def extract_articles(language, ontology_class, corpus_dir, output_dir):
        """
        """
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

        for path, subdirs, files in os.walk(corpus_dir):
            for name in files:
                f = os.path.join(path, name)
                with open(f) as i:
                    content = ''.join(i.readlines())
                match = re.search('id="([^"]+)"', content)
                current_id = match.group(1)
                if DEBUG:
                    print 'File = [{0}] - Wiki ID = [{1}]'.format(f, current_id)
                if current_id in article_ids:
                    shutil.copy(f, output_dir)
                    if DEBUG:
                        print 'MATCHED! [{0}]'.format(content)


# def load_wiki_ids(filein):
#     with open(filein) as i:
#         return [l.strip() for l in i.readlines()]


# def extract_soccer_articles(soccer_ids, corpus_dir, output_dir):
#     for path, subdirs, files in os.walk(corpus_dir):
#         for name in files:
#             f = os.path.join(path, name)
#             with open(f) as i:
#                 content = ''.join(i.readlines())
#             match = re.search('id="([^"]+)"', content)
#             current_id = match.group(1)
#             if DEBUG:
#                 print 'File = [{0}] - Wiki ID = [{1}]'.format(f, current_id)
#             if current_id in soccer_ids:
#                 shutil.copy(f, output_dir)
#                 if DEBUG:
#                     print 'MATCHED! [{0}]'.format(content)
#     return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'Usage: {0} <LANGUAGE> <ONTOLOGY_CLASS> <CORPUS_DIR> <OUTPUT_DIR>'.format(__file__)
        sys.exit(1)
    else:
        loader = ArticleLoader()
        loader.extract_articles(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        # ids = load_wiki_ids(sys.argv[1])
        # extract_soccer_articles(ids, sys.argv[2], sys.argv[3])
