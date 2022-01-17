import argparse
import os
import pathlib
import re
import subprocess
import sys
import zipfile

import papermill as pm
import requests
from bs4 import BeautifulSoup

import config


class ReturnURLS:
    """Get and clean the urls listed in urls.txt"""

    def get_urls(self):
        urls_path = pathlib.Path.cwd() / "processor/inputs/urls.txt"
        with open(urls_path, mode="r") as f:
            urls = [line.strip() for line in f if not line.startswith("#")]

        for url in urls:
            cleaned_urls = []
            try:
                response = requests.get(url)
                cleaned_urls.append(url)
            except requests.ConnectionError:
                pass
            except requests.exceptions.MissingSchema:
                pass

        return cleaned_urls


class DatasetTitle:
    """Get the dataset name from the url"""

    def get_dataset_titles(self):
        urls = ReturnURLS().get_urls()
        names = []
        pattern = "([^/]*$)"
        for url in urls:
            if url[-1] == "/":
                url = url[:-1]
            dataset_name = re.search(pattern, url)
            dataset_parent_directory = (
                str(pathlib.Path.cwd()) + "/data/" + dataset_name[0]
            )
            jupyter_notebook_filename = dataset_name[0] + ".ipynb"
            jupyter_notebook_parent_directory = str(pathlib.Path.cwd() / "outputs/")
            names.append(
                (
                    dataset_name[0],
                    jupyter_notebook_filename,
                    dataset_parent_directory,
                    jupyter_notebook_parent_directory,
                )
            )
        return names


class ReturnDownloadLinks:
    """Get the download links for each url returned by ReturnURLS"""

    def get_links(self):

        download_links = []
        urls = ReturnURLS().get_urls()
        for l in urls:
            r = requests.get(l)
            html = r.content.decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            links = [link for link in soup.find_all("a") if "." in link.get("href")]
            links = [link.get("href") for link in links]
            for link in links:
                download_links.append(l + link)
        return download_links


class DownloadDataset:
    """Fetch all datafiles for each dataset"""

    def __init__(self) -> None:
        self.datasets = DatasetTitle().get_dataset_titles()
        self.urls = ReturnDownloadLinks().get_links()

    def get_data(self):
        for dataset in self.datasets:
            dir_name = dataset[2]
            file_name = dataset[0]
            for url in self.urls:
                file = self.extract_download_filename(url)
                a = "wget"
                p = "-P"
                # download only if file doesn't already exist
                if os.path.isfile(dir_name + "/" + file):
                    print(f"Dataset file {file} has previously been downloaded")
                    continue
                subprocess.run([a, p, dir_name, url])
                print(f"Dataset file {file} successfully downloaded")

    def extract_download_filename(self, url: str):
        pattern = "([^/]*$)"
        return re.search(pattern, url)[1]

    def return_filenames(self):
        dataset_filenames = []
        for dataset in self.datasets:
            file_names = []
            for url in self.urls:
                filename = self.extract_download_filename(url)
                file_names.append(filename)
            dataset_filenames.append((dataset[0], file_names))
        return dataset_filenames


class ExecutePapermill:
    """Execute the papermill .ipnby template and save for each url"""

    def __init__(self, filenames: list) -> None:
        self.filenames = filenames  # this is a list of tuples(dataset, [filenames])

    def execute_papermill(self):

        for dataset in self.filenames:
            pm.execute_notebook(
                "/home/randall/Dev/uci_dataset_processor/processor/inputs/uci_template.ipynb",
                "/home/randall/Dev/uci_dataset_processor/processor/outputs/"
                + dataset[0]
                + ".ipynb",
                parameters={"inputs": dataset[1]},
            )


def main():
    datasets_processor = DownloadDataset()
    datasets_processor.get_data()
    papermill = ExecutePapermill(datasets_processor.return_filenames())
    papermill.execute_papermill()


if __name__ == "__main__":
    main()
