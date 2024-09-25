#!/usr/bin/env python3

import urllib.request
import sys
import feedparser
import os
import re

def fetch_arxiv_data(query='electron', start=0, max_results=5):
    base_url = 'http://export.arxiv.org/api/query'
    params = urllib.parse.urlencode({
        'search_query': f'all:{query}',
        'start': start,
        'max_results': max_results,
        'sortBy': 'lastUpdatedDate',
        'sortOrder': 'descending'
    })
    url = f'{base_url}?{params}'
    
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
        parse_and_print_results(data, query)
    except urllib.error.URLError as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

def sanitize_filename(filename):
    # Remove or replace characters that are not suitable for filenames
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_pdf(pdf_url, filename):
    pdf_folder = 'pdfs'
    os.makedirs(pdf_folder, exist_ok=True)
    pdf_path = os.path.join(pdf_folder, filename)
    
    try:
        print(f"Downloading PDF: {filename}")
        urllib.request.urlretrieve(pdf_url, pdf_path)
        print(f"PDF downloaded successfully: {pdf_path}")
    except urllib.error.URLError as e:
        print(f"Error downloading PDF: {e}", file=sys.stderr)
    except IOError as e:
        print(f"Error saving PDF: {e}", file=sys.stderr)

def parse_and_print_results(data, query):
    feed = feedparser.parse(data)

    print(f"Feed title: {feed.feed.get('title', 'N/A')}")
    print(f"Feed last updated: {feed.feed.get('updated', 'N/A')}")
    print(f"totalResults for this query: {feed.feed.get('opensearch_totalresults', 'N/A')}")
    print(f"itemsPerPage for this query: {feed.feed.get('opensearch_itemsperpage', 'N/A')}")
    print(f"startIndex for this query: {feed.feed.get('opensearch_startindex', 'N/A')}")

    for entry in feed.entries:
        print('\ne-print metadata')
        arxiv_id = entry.id.split('/abs/')[-1]
        print(f"arxiv-id: {arxiv_id}")
        print(f"Published: {entry.get('published', 'N/A')}")
        print(f"Last Updated: {entry.get('updated', 'N/A')}")
        
        title = entry.get('title', 'N/A')
        print(f"Title: {title}")
        
        authors = entry.get('authors', [])
        if authors:
            print(f"Authors: {', '.join(author.get('name', 'N/A') for author in authors)}")
            print(f"Last Author: {authors[-1].get('name', 'N/A')}")
        else:
            print("No author information available")

        pdf_link = None
        for link in entry.get('links', []):
            if link.get('rel') == 'alternate':
                print(f"abs page link: {link.get('href', 'N/A')}")
            elif link.get('title') == 'pdf':
                pdf_link = link.get('href', 'N/A')
                print(f"pdf link: {pdf_link}")
        
        print(f"Journal reference: {entry.get('arxiv_journal_ref', 'No journal ref found')}")
        print(f"Comments: {entry.get('arxiv_comment', 'No comment found')}")
        
        tags = entry.get('tags', [])
        if tags:
            print(f"Primary Category: {tags[0].get('term', 'N/A')}")
            all_categories = [t.get('term', 'N/A') for t in tags]
            print(f"All Categories: {', '.join(all_categories)}")
        else:
            print("No category information available")
        
        print(f"Abstract: {entry.get('summary', 'N/A')}")

        if pdf_link:
            # Create filename with query and first 10 words of title
            title_words = title.split()[:10]
            title_part = ' '.join(title_words)
            filename = f"{query}_{title_part}_{arxiv_id}.pdf"
            filename = sanitize_filename(filename)  # Remove invalid characters
            download_pdf(pdf_link, filename)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python arxiv_query.py <query> [max_results]")
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    fetch_arxiv_data(query, max_results=max_results)