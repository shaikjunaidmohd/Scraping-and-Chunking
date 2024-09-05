import requests
from bs4 import BeautifulSoup
import re
import os
import google.generativeai as genai

# Function to chunk the article using an LLM
def chunk_with_llm(article_content, max_length=750):
    prompt = (
        "Split the following content into smaller chunks of approximately 750 characters. "
        "Ensure that headers, paragraphs, and bulleted lists stay together without breaking them. "
        "Each chunk should preserve the context as much as possible:\n\n"
    )

    full_text = "\n\n".join(article_content)
    os.environ['GOOGLE_API_KEY'] = "AIzaSyCl4RFhZGjS5VzLQdJ3sOeZ37xyXUbPlF0"
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(f"{prompt} + {full_text}")
    if response._done and response._result and response._result.candidates and len(response._result.candidates[0].content.parts) > 0:
        content_parts = response._result.candidates[0].content.parts[0].text
    else:
        return ""

    # Split the content based on double newlines
    chunks = content_parts.split('\n\n')

    return [chunk.strip() for chunk in chunks if chunk.strip()]

base_url = "https://www.notion.so/help"
final_chunks = []
# Fetch the Help Center main page
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all article links, excluding Notion Academy guides
artickLinks = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if '/help/category' in href:
        artickLinks.append(href)

artickLinks = list(set(artickLinks))  # Remove duplicates


# Display total articles
print(f"Found {len(artickLinks)} articles:")
for article in artickLinks:
    category_url = f"https://www.notion.so{article}"

    # Fetch the category page
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the "Articles" section by looking for specific class or ID
    articles_section = soup.find('div', {'class': 'oldGridItem_gridItem__PlgPJ oldGridItem_gridItemSpanXs12__IZq1P oldGridItem_gridItemOrderXs2__c0oAA oldGridItem_gridItemSpanS12__o7otG oldGridItem_gridItemOrderS2__ie65N oldGridItem_gridItemSpanM12__RraXO oldGridItem_gridItemOrderM2__wB5J7 oldGridItem_gridItemSpanL9__5cDvM oldGridItem_gridItemOrderL2__d0Xo5 oldGridItem_gridItemSpanXl9__Hj8oD oldGridItem_gridItemOrderXl2__TYU_6'})

    # Extract all links within the "Articles" section
    article_links = []
    if articles_section:
        for link in articles_section.find_all('a', href=True):
            href = link['href']
            if '/help/' in href and 'academy' not in href.lower():
                article_links.append(href)

    article_links = list(set(article_links)) 

    # Output the found article links
    print(f"Found {len(article_links)} inner articles in the {article}:")
    
    for link in article_links:
        inner_article_link = "https://www.notion.so" + link
        content = []
        article_response = requests.get(inner_article_link)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        article_soup = article_soup.find('div', {'class': 'oldGridItem_gridItem__PlgPJ oldGridItem_gridItemSpanXs12__IZq1P oldGridItem_gridItemOrderXs2__c0oAA oldGridItem_gridItemSpanS12__o7otG oldGridItem_gridItemOrderS2__ie65N oldGridItem_gridItemSpanM12__RraXO oldGridItem_gridItemOrderM2__wB5J7 oldGridItem_gridItemSpanL9__5cDvM oldGridItem_gridItemOrderL2__d0Xo5 oldGridItem_gridItemSpanXl9__Hj8oD oldGridItem_gridItemOrderXl2__TYU_6'})  

        if article_soup:
        # Extract Headings
          for header in article_soup.find_all(re.compile('^h[1-6]$')):
              content.append(header.get_text(strip=True))

          # Extract paragraphs
          for paragraph in article_soup.find_all('p'):
              content.append(paragraph.get_text(strip=True))

          # Extract bulleted lists
          for ul in article_soup.find_all('ul'):
              list_items = '\n'.join([li.get_text(strip=True) for li in ul.find_all('li')])
              content.append(list_items)
        print(f'Scraping............{link}')
        final_chunks.extend(chunk_with_llm(content[:1000]))
    
print(final_chunks)
