# import python libraries
import mechanize
import cookielib
from bs4 import BeautifulSoup

# setup mechanize browser
br = mechanize.Browser()

# setup cookie handler
ch = cookielib.LWPCookieJar()
br.set_cookiejar(ch)

# browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# browser refresh setup
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# setup user-agent to seem like a human
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# open website
br.open('http://www.cookcountyclerkofcourt.org/?section=CASEINFOPage&CASEINFOPage=2500')

# select form
br.select_form('Criteria')

# fill form fields
br.form['Year'] = '1997'
br.form['div'] = 'M1'
br.form['number'] = '155682'

# submit form
br.submit()

# store response
response = br.response()

# print response
print response.read()

