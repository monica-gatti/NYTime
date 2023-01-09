# Copyright (c) 2013, Daniel Gamez
# with the guidance of Israel Herraiz at URJC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1) Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
# 
# 2) Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#

import urllib2
from bs4 import BeautifulSoup as Soup
from urlparse import urlparse, urljoin


### URL's Retriever
def retrieve_links (url):
    """This function retrieve links from the URL provided.
  
    The URL must be in any of these formats:
    http://www.domain.org
    https://www.domain.net
    ftp://64.139.197.1
    """
    # Define opener for the URL
    opener = urllib2.build_opener ()
  
    # Catch exceptions related to the URL opening
    try:
        # Read content from URL
        t = opener.open (url).read ()
    
        # Parse content read
        parser = Soup(t)
    
        # Obtain only links from URL provided
        return [x['href'] for x in parser.findAll('a') if x.has_attr('href')]

    # Capture possible message exceptions related to the URL opening
    except urllib2.URLError:
        return []
    

### Obtain links list by depth per URL
def links_list (url, depth):
    """This function obtains the list of links from the URL provided.
    It is a recursive function which dive into indicated DEPTH.  
    It assumes "DEPTH = 0" is the current URL with no deep.
  
    Execution call example:
    links_list ('http://www.domain.org/index.html', 2)
    """
    # Base case in the recursion
    if depth == 0:

        # Retrieve links list from URL provided
        l = retrieve_links (url)
    
        # Print links list founded
        for each in l:
            print " - %s" % each

        # Return list with the links founded
        return l

    # Recursive case
    else:
        # Get URL base on b
        b = validate_url (url)
    
        l = retrieve_links (url)
    
        for each in l:
      
            # Get URL base on e
            e = validate_url (each)
      
            # Correct list URL item in the proper position of the list
            if not e:
	            l[l.index(each)] = urljoin(b, each)

        # Re-iterate over the list to call the next recursive level
        for each in l:
            # On recursive level return, print a level identificator
            print " %s %s" % ("*"*depth, each)
      
            # Recursive call with DEPTH-1
            l2 = links_list (each, depth-1)

    print ""

  
### URL Validator
def validate_url (url):
    """This function validates the URL provided.
  
    In TRUE condition, it returns the spected URL with proper format.
    In FALSE condition, it returns FALSE.
  
    Execution call example:
    validate_url ('http://www.domain.org')
      Will return: http://www.domain.org/index.html
     
    validate_url ('domain.org')
      Will return: FALSE
    """
    # Parse URL provided
    v = urlparse(url)

    # Verify if protocol (http, https, ftp) and hostname are present 
    # in the URL provided.
    if v.scheme and v.hostname:
    
        # Get URL base and hostname to form the correct URL base
        u = v.scheme + '://' + v.hostname + '/'
        return u

    else:
        # Not a valid URL
        return False
