from threading import Thread,Semaphore
from time import perf_counter
from urllib.request import urlopen

MAX_CONCURRENT_DOWNLOAD = 3
semaphore = Semaphore(MAX_CONCURRENT_DOWNLOAD)

def download(url:str):
    with semaphore:
        print(f' downloading {url}...')

        response = urlopen(url)
        data = response.read()

        print(f'finished download {url}')
        return data

def main():
    # Plain HTTP avoids CERTIFICATE_VERIFY_FAILED on some macOS Python installs
    # (missing CA bundle). For HTTPS + IETF RFCs, run Install Certificates.command
    # from the Python 3.x folder in Applications, or use a venv with certifi.
    urls = [f"http://example.com/?n={i}" for i in range(5)]

    start_time = perf_counter()
    threads = [Thread(target=download, args=(url,)) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    end_time = perf_counter()

    print(f'Total time taken: {end_time - start_time} seconds')

if __name__ == "__main__":
    main()
