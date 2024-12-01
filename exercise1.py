import argparse
import os
import re
import threading
import time


def get_files_list(directory: str) -> list:
    if not (os.path.exists(directory) and os.path.isdir(directory)):
        raise FileNotFoundError(f"{directory} is not a valid path to directory")

    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def process_files(file_list, keywords, results, time_elapsed, lock):
    start_time = time.time()

    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    matches = re.findall(pattern, content, flags=re.IGNORECASE)

                    if matches:
                        lock.acquire()
                        if keyword not in results:
                            results[keyword] = []

                        results[keyword].append(file_path)
                        lock.release()
        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")

    lock.acquire()
    time_elapsed.append(time.time() - start_time)
    lock.release()


def main(directory: str, threads: int, keywords: list):
    files = get_files_list(directory)
    chunk_size = len(files) // threads
    chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    results = {}
    time_elapsed = []
    lock = threading.RLock()

    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=process_files, args=(chunk, keywords, results, time_elapsed, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    for keyword, files in results.items():
        print(f"Ключове слово: {keyword}, кількість файлів: {len(files)}")
        for file in files:
            print(f"\t{file}")

        print()

    return time_elapsed


if __name__ == '__main__':

    def validate_directory(directory: str) -> str:
        if not (os.path.exists(directory) and os.path.isdir(directory)):
            raise argparse.ArgumentTypeError(f"{directory} is not a valid path to directory")

        return directory


    def limit_to_5(string: str) -> int:
        value = int(string)
        if 0 < value < 6:
            return value
        raise argparse.ArgumentTypeError("Threads number must be limited positive number more than 0 limited to 5")

    def parse_keywords(keywords: str) -> list:
        return list(map(lambda keyword: keyword.strip(), keywords.split(",")))

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Path to the directory", type=validate_directory, default='./files')
    parser.add_argument("-t", "--threads", help="Threads number", type=limit_to_5, default=5)
    parser.add_argument(
        "-k",
        "--keywords",
        help="Keywords separated by comma",
        type=parse_keywords,
        default=["trees", "beauty", "green", "species"],
    )
    args = parser.parse_args()
    start_time = time.time()
    time_elapsed = main(**vars(args))
    total_time_elapsed = time.time() - start_time
    threads_time_sum = sum(time_elapsed)
    print (f"Повний час виконання {total_time_elapsed}s")
    print (f"Сумарний час виконання потоків {threads_time_sum}s")
    print (f"Паралельне виконання заощадило нам {threads_time_sum - total_time_elapsed}s")
