from threading import Thread
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from time import perf_counter

class CustomThread(Thread):
    def __init__(self,url):
        super().__init__()
        self.url = url

    def run(self)->None:
        print(f'checking {self.url}')
        try:
            response = urlopen(self.url)
            print(response.code)
        except HTTPError as e:
            print(e.code)
        except URLError as e:
            print(e.reason)

start_time = perf_counter()

def main()->None:
    urls = [
        # 'https://www.google.com',
        # 'https://www.python.org',
        # 'https://www.github.com',
        # 'https://www.twitter.com',
        # 'https://www.facebook.com',
        # 'https://www.instagram.com',
        # 'https://www.linkedin.com',
        # 'https://www.youtube.com',
        # 'https://www.wikipedia.org',
        # 'https://www.stackoverflow.com'

        'https://httpstat.us/200',
        'https://httpstat.us/400'
    ]


    threads = [CustomThread(url) for url in urls]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]   


if __name__ == "__main__":
    main()
    end_time = perf_counter()
    print(f'Time taken: {end_time - start_time} seconds')