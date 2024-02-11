import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_papers():
    def is_within_last_week(date_str):
        publication_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        a_week_ago = datetime.now() - timedelta(days=7)
        return publication_date >= a_week_ago

    query_url = "http://export.arxiv.org/api/query?search_query=cat:cs.*&sortBy=submittedDate&sortOrder=descending&max_results=100"
    response = requests.get(query_url)
    soup = BeautifulSoup(response.content, 'xml')

    papers = []
    for entry in soup.find_all('entry'):
        if is_within_last_week(entry.published.text) and len(papers) < 50:
            paper_info = {
                'title': entry.title.text,
                'abstract': entry.summary.text,
                'published_date': entry.published.text,
                'url': entry.id.text
            }

            papers.append(paper_info)

    papers = sorted(papers, key=lambda x: x['published_date'])

    with open('prompt.json', 'w') as f:
        f.write(json.dumps(papers))
