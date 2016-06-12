from scrapy.link import Link
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import logging
import urlparse


class WordpressApiDiggerExtractor(LxmlLinkExtractor):
    def extract_links(self, response, *args, **kwargs):
        body = response._body
        if type(body) is not dict:
            raise Exception('Response not a dict , probably json not loaded')

        links = []
        link_current = Link(response.url)
        links.append(link_current)
        if 'posts' in body and body['posts'] and len(body['posts']) > 0:
            urls_parts = urlparse.urlparse(response.url)
            query_parts = urlparse.parse_qs(urls_parts.query)
            if 'page' in query_parts:
                query_parts['page'][0] = str(int(query_parts['page'][0]) + 1)
                link_url = urls_parts[0] + '://' + urls_parts[1] + urls_parts[2] + '?'
                query_parts_reconstructed = '';
                for key, value in query_parts.iteritems():
                    if len(query_parts_reconstructed) > 0:
                        query_parts_reconstructed += '&'
                    query_parts_reconstructed += key + '=' + value[0]
                link_url = link_url + query_parts_reconstructed
                link = Link(link_url)
                links.append(link)
            else:
                logging.warning('can not find [page] in url query')
        else:
            logging.info('No posts found in api response , no more calling')
        return links
