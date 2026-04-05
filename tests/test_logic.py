import pytest
import os
import httpx
from src.scraper import get_top_5_links
from src.summarizer import GroqSummarizer
from src.reporter import create_pdf

def test_scraper_logic(mocker):
    """Verify that the scraper correctly filters for news articles and limits to 5."""
    # Simulate a TechCrunch homepage with various links
    mock_html = """
    <html>
        <body>
            <a href='https://techcrunch.com/2026/04/05/ai-news/'>Article 1</a>
            <a href='https://techcrunch.com/2026/04/05/startup-funding/'>Article 2</a>
            <a href='https://techcrunch.com/author/john-doe/'>Ignore Author Page</a>
            <a href='https://techcrunch.com/2026/04/05/tech-trends/'>Article 3</a>
            <a href='https://techcrunch.com/2026/04/05/ev-market/'>Article 4</a>
            <a href='https://techcrunch.com/2026/04/05/space-exploration/'>Article 5</a>
            <a href='https://techcrunch.com/2026/04/05/extra-one/'>Article 6 (Should be ignored by limit)</a>
        </body>
    </html>
    """
    # Create a mock response object
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = mock_html
    
    # Patch the httpx Client.get to return our fake data instead of hitting the internet
    mocker.patch('httpx.Client.get', return_value=mock_response)

    links = get_top_5_links()
    
    assert len(links) == 5, f"Expected 5 links, but got {len(links)}"
    assert all("techcrunch.com/20" in link for link in links), "Non-article links found!"
    assert "author" not in " ".join(links), "Author link was not filtered out."

def test_pdf_creation_logic():
    """Verify that the PDF reporter successfully generates a file on the disk."""
    test_summaries = [("https://test.com/1", "Summary 1"), ("https://test.com/2", "Summary 2")]
    test_filename = "test_report.pdf"
    
    # Ensure a clean slate before the test
    if os.path.exists(test_filename):
        os.remove(test_filename)
        
    path = create_pdf(test_summaries, filename=test_filename)
    
    # SRE Check: File must exist and have a non-zero size
    assert os.path.exists(path), "PDF file was not created."
    assert os.path.getsize(path) > 0, "PDF file is empty."
    
    # Cleanup to keep the environment clean
    os.remove(path)

def test_summarizer_init(mocker):
    """Ensure the GroqSummarizer initializes correctly even without a real API key."""
    mocker.patch('groq.Groq', return_value=mocker.Mock())
    mocker.patch('os.getenv', return_value="fake_key_123")
    
    summarizer = GroqSummarizer()
    assert "Groq" in summarizer.name, "Summarizer name not set correctly."
