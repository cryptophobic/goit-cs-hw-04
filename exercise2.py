import argparse
import multiprocessing
import os
import re
import time


def get_files_list(directory: str) -> list:
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def process_files(file_list, keywords, result_queue, time_elapsed):
    local_results = {}
    start_time = time.time()

    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    matches = re.findall(pattern, content, flags=re.IGNORECASE)

                    if matches:
                        if keyword not in local_results:
                            local_results[keyword] = []

                        local_results[keyword].append(file_path)
        except Exception as e:
            print(f"Error file processing {file_path}: {e}")

    time_elapsed.put(time.time() - start_time)
    result_queue.put(local_results)

def main(directory: str, processes: int, keywords: list):
    files = get_files_list(directory)
    chunk_size = len(files) // processes
    chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    time_elapsed_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    processes_list = []
    start_time = time.time()

    for chunk in chunks:
        process = multiprocessing.Process(target=process_files, args=(chunk, keywords, result_queue, time_elapsed_queue))
        processes_list.append(process)
        process.start()

    for process in processes_list:
        process.join()

    total_time_elapsed = time.time() - start_time


    results = {}
    while not result_queue.empty():
        for keyword, files_list in result_queue.get().items():
            if keyword not in results:
                results[keyword] = files_list
            else:
                results[keyword] += files_list

    for keyword, files in results.items():
        print(f"Ключове слово: {keyword}, кількість файлів: {len(files)}")
        for file in files:
            print(f"\t{file}")

        print()

    process_time_elapsed = 0
    while not time_elapsed_queue.empty():
        process_time_elapsed += time_elapsed_queue.get()

    return process_time_elapsed, total_time_elapsed


if __name__ == '__main__':

    def validate_directory(directory: str) -> str:
        if not (os.path.exists(directory) and os.path.isdir(directory)):
            raise argparse.ArgumentTypeError(f"{directory} is not a valid path to directory")

        return directory


    def limit_to_5(string: str) -> int:
        value = int(string)
        if 0 < value < 6:
            return value
        raise argparse.ArgumentTypeError("Process number must be limited positive number more than 0 limited to 5")

    def parse_keywords(keywords: str) -> list:
        return list(map(lambda keyword: keyword.strip(), keywords.split(",")))

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Path to the directory", type=validate_directory, default='./files')
    parser.add_argument("-p", "--processes", help="Processes number", type=limit_to_5, default=5)
    parser.add_argument(
        "-k",
        "--keywords",
        help="Keywords separated by comma",
        type=parse_keywords,
        default=["trees", "beauty", "green", "species"],
    )
    args = parser.parse_args()
    start_time = time.time()
    processes_time_sum, total_time_elapsed = main(**vars(args))
    print (f"Повний час виконання {total_time_elapsed}s")
    print (f"Сумарний час виконання процесів {processes_time_sum}s")
    print (f"Паралельне виконання заощадило нам {processes_time_sum - total_time_elapsed}s")
