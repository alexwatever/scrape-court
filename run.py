# import python libraries
import mechanize
import cookielib
import csv
import time
from bs4 import BeautifulSoup


# create csv to write data to
output = csv.writer(open("data.csv", "w"))

# writer header row to csv
output.writerow(["url", "year", "casenumber", "plaintiff", "defendant", "courtroom", "time", "calltype", "sequence"])

# store url to scrape
url = 'http://www.cookcountyclerkofcourt.org/?section=CASEINFOPage&CASEINFOPage=2500'

# create number for logging lines
num = 1


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


# open list file
with open("list.csv", mode="r") as f:
    # setup csv reader to work with list
    reader = csv.reader(f)

    # loop through list row by row
    for row in reader:
        # open website in mechanize
        br.open(url)

        # create empty variables
        d_url = ''
        d_year = ''
        d_casenumber = ''
        d_plaintiff = ''
        d_defendant = ''
        d_courtroom = ''
        d_time = ''
        d_calltype = ''
        d_sequence = '' ##

        # select form
        br.select_form('Criteria')

        # fill form fields
        br.form['Year'] = row[0]
        br.form['div'] = row[1]
        br.form['number'] = row[2]

        # submit form
        br.submit()

        # store response in variable
        data = br.response().read()

        # store response in beautifulsoup
        soup = BeautifulSoup(data, "lxml")


        # store data if it exists
        data_exists = soup.find('td', width='256')

        # check if data exists and store data if it does
        if data_exists == None:
            print 'Line %d skipped' % num
        else:
            # store data in variables
            d_url = d_casenumber = soup.find('tr', bgcolor='#A8C3FF').td.a['href']
            d_year = row[0]
            d_casenumber = soup.find('tr', bgcolor='#A8C3FF').td.a.text
            d_plaintiff = soup.find('tr', bgcolor='#A8C3FF').td.find_next_sibling("td").text
            d_defendant = soup.find('tr', bgcolor='#A8C3FF').td.find_next_sibling("td").find_next_sibling("td").text
            d_courtroom = soup.find('tr', bgcolor='#A8C3FF').td.find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").text
            d_time = soup.find('tr', bgcolor='#A8C3FF').td.find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").text
            d_calltype = soup.find('tr', bgcolor='#A8C3FF').td.find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").text

            # open url found in hyperlink tag
            br.open(d_url)

            # store response in variable
            data = br.response().read()

            # store response in beautifulsoup
            soup = BeautifulSoup(data, "lxml")

            # store data if it exists
            data_exists = soup.find('table', width='85%')

            # check if data exists and store data if it does            
            if data_exists == None:
                print 'Sequence number skipped'
            else:
                # store data in variable
                d_sequence = soup.find('table', width='95%').tr.find_next_sibling("tr").td.text.replace("Sequence #: ", "")

            # write data to row
            output.writerow([d_url, d_year, d_casenumber, d_plaintiff, d_defendant, d_courtroom, d_time, d_calltype, d_sequence])


        # empty variables
        date = ''
        soup = ''

        # wait for 0.5 seconds to create delay in between requests
        time.sleep(0.5)

        # write to console
        print 'Line %d complete' % num
        num += 1


# print results
print 'All done'

