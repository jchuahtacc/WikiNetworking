from pyquery import PyQuery
import time  

## Filters a PyQuery object populated from a Wiki page for links
# @param    selector    An optional DOM selector for elements containing desired links
# @return               A list of link URLs
def filter_links(page, selector=""):
    result = []
    subchildren = PyQuery(page("#mw-content-text " + selector))
    for child in subchildren:
        links = PyQuery(child)("a")
        for link in links:
            linkQuery = PyQuery(link)
            if not linkQuery.hasClass("mw-redirect"):
                href = linkQuery.attr("href")
                if "/wiki/" in href and "#" not in href:
                    result.append(linkQuery.attr("href"))
    return result

## Retrieves a list of URLs, with a 2 second delay between retrievals
# @param    selector    An optional DOM selector for elements containing desired links
# @return               A list of link URLs
def retrieve_multipage(urls, selector="", verbose=False):
    result = []
    for url in urls:
        time.sleep(2)
        if verbose:
            print "Retrieving " + url
        result.extend(filter_links(PyQuery(url=url), selector))
    return result

## Writes a list to a file with a newline separator after each list item
# @param    data        The list to be written
# @param    filename    The output filename
def write_list(data, filename):
    with open(filename, "w") as file:
        for item in data:
            file.write(item)
            file.write("\n")

## Reads a newline separated list from a file
# @param    filename    The filename to be read
# @return               A list of each line from the file
def read_list(filename):
    with open(filename, "r") as file:
        return [item.strip() for item in file.readlines()]

## Returns a list of items that exist in two lists
# @param    list1       A list containing elements
# @param    list2       A second list containing elements
# @return               A list containing elements that exist in both parameters
def intersection(list1, list2):
    return [element for element in set(list1).intersection(list2)]

## Performs a breadth-first web crawl
# @param    start           The starting URL to begin the crawl, or a list of URLs to queue for crawling
# @param    max_articles    The maximum number of articles to retrieve before ending the crawl
# @param    max_depth       The maximum depth of links from the starting article
# @param    accept          A list of URLs that the crawler will follow. Supplying an empty list will result in no data
# @param    reject          A list of URLs that the crawler will NOT follow
# @param    host            A hostname to crawl articles on
def crawl(start, max_articles=200, max_depth=3, accept=list(), reject=list(), host="https://en.wikipedia.org"):
    from collections import deque
    result = dict()
    crawl_queue = deque()
    import types
    if isinstance(start, list):
        for url in start:
            if url not in crawl_queue:
                crawl_queue.append(url)
    else:
        crawl_queue.append(start)
    count = 0
    while count < max_articles and len(crawl_queue) > 0:
        count = count + 1
        current = crawl_queue.popleft()
        print "{}: Retrieving {}, ({} left in queue)".format(count, current.encode('utf-8'), len(crawl_queue))
        try:
            page = PyQuery(url=host+current)
            
            # Make sure page exists in structure
            if current not in result:
                result[current] = dict()
                result[current]["depth"] = 0
            
            # Save page data
            result[current]["title"] = page("#firstHeading").text()
            result[current]["links"] = [link for link in filter_links(page) if link in accept and link not in reject]
            
            # Check current depth, don't want to go to deep!
            if result[current]["depth"] <= max_depth: 
                for link in result[current]["links"]:
                    if link not in result and link not in crawl_queue:
                        crawl_queue.append(link)
                        result[link] = dict()
                        result[link]["depth"] = result[current]["depth"] + 1
                        
            # Important!!!
            time.sleep(2)
        except:
            print "Error retrieving", host+current

    return result

## Creates a dictionary representing a directed graph from crawl data
# @param    data    A dictionary from the result of @link <crawl>
# @return           A dictionary where each key is an article title, and the value is a dictionary containing the source URL and a list of edges and weights
def directed_graph(data):
    result = dict()
    for item in data:
        current_title = data[item]["title"]
        result[current_title] = dict()
        result[current_title]["url"] = item
        result[current_title]["edges"] = dict()
        for link in data[item]["links"]:
            if link in data:
                link_title = data[link]["title"]
            else:
                link_title = link
            if link_title not in result[current_title]:
                result[current_title]["edges"][link_title] = data[item]["links"].count(link)
    return result 

## Creates a dictionary representing an undirected graph from crawl data
# @param    data    A dictionary from the result of @link <crawl>
# @return           A dictionary similar to @link <directed_graph>, except that edges appear exactly once, with a weight that is the sum of links between both articles connected by the edge
def undirected_graph(data):
    result = dict()
    for item in data:
        current_title = data[item]["title"]
        result[current_title] = dict()
        result[current_title]["url"] = item
        result[current_title]["edges"] = dict()
        already_counted = list()
        for link in data[item]["links"]:
            if link not in already_counted:
                if link in data:
                    link_title = data[link]["title"]
                else:
                    link_title = link
                if link_title in result and current_title in result[link_title]["edges"]:
                    result[link_title]["edges"][current_title] += data[item]["links"].count(link)
                elif link_title not in result[current_title]:
                    result[current_title]["edges"][link_title] = data[item]["links"].count(link)
                already_counted.append(link)
    return result 

## Saves a dictionary to a file in JSON format
# @param    data        The dictionary to save
# @param    filename    The output filename
# @param    pretty      If True, the output is formatted with indentation and keys are sorted
def save_dict(data, filename, pretty=True):
    import json
    with open(filename, 'w') as f:
        if pretty:
            f.write(json.dumps(data, sort_keys=True, indent=4))
        else:
            json.dump(data, f)
        f.close()

## Reads a dictionary from a file in JSON format
# @param    filename    The input filename
# @return               A dictionary from the JSON file        
def load_dict(filename):
    import json
    with open(filename, 'r') as f:
        data = json.load(f)
        return data

