"""Check that we have Django installed."""

from selenium import webdriver


browser = webdriver.Firefox()

# Alice has heard about a cool new online app.
# She goes to check out its homepage.
browser.get('http://localhost:8000')

# She notices the page title and header mention resource lists
assert 'Recursos' in browser.title

# And the page lists last post published by another users

# Satisfied, she goes back to sleep
browser.quit()
