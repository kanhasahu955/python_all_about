from threading import Thread
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from time import perf_counter

class CustomThread(Thread):
    def __init__(self,url):
        super().__init__()
        self.url = url
        self.status_code = None
        self.error = None
    
    def run(self)->None:
        try:
            response = urlopen(self.url)
            self.status_code = response.code
        except HTTPError as e:
            self.status_code = e.code
            self.error = str(e.reason)
        except URLError as e:
            self.error = str(e.reason)

start_time = perf_counter()

def main()->None:
    urls = [
        'https://httpstat.us/200',
        'https://httpstat.us/400'
    ]

# create new threads
    threads = [CustomThread(url) for url in urls]

# start the threads
    [thread.start() for thread in threads]

# wait for the threads to finish
    [thread.join() for thread in threads]

# print the results
    for thread in threads:
        print(f'URL: {thread.url}, Status Code: {thread.status_code}, Error: {thread.error}')

if __name__ == "__main__":
    main()
    end_time = perf_counter()
    print(f'Time taken: {end_time - start_time} seconds')