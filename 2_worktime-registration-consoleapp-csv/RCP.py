"""
Module which is taking a list of tasks of the construction worker, tagged by client, project and additional remarks.
Script sums up the task times for each tag (ex. for every customer, every project, every delegation etc.)
Generate raport on which tasks employee spend his work time for example for analytic purposes

Usage:  RCP.py filename.csv

"""

import csv
from dataclasses import dataclass
from typing import Any

import click


@dataclass
class Entry:
    description : str
    time : int
    tags : list[str]


def make_entrys_from_file(filename :str) -> list[Entry]:
    with open (filename, 'r') as stream:
        tasks = csv.DictReader (stream)
        entrys = [construct_entry(task) for task in tasks]
    return entrys


def construct_entry(task :dict[str,Any]) -> Entry:
    desc = task["desc"]
    time = int(task["time"])
    tags = task['tags'].split()
    tags = ['# ' + tag for tag in tags]
    entry = Entry(desc,time,tags)
    return entry


def sum_times_for_tags(entrys :Entry) -> dict[str,int]:
    """Sum time for every tag in tasks in entry. Return dict of tag and time. """
    tags_dict={}
    for entry in entrys:
        for tag in entry.tags:
            if tag in tags_dict:
                tags_dict[tag] = tags_dict[tag] + entry.time
            else:
                tags_dict[tag] = entry.time
    return tags_dict


def print_raport(tags_dict):
    print("--------------------------------------------------")
    print(f"{'TAG:':25}{'czas[h]:'}")
    print("--------------------------------------------------")
    print_tags_and_time(tags_dict)
    print("---------------------------------------------------")


def print_tags_and_time(tags_dict):
    for key,value in tags_dict.items():
        print(f"{key:25}{value:>}")


@click.command
@click.argument('filename')
def main(filename):
    entrys = make_entrys_from_file(filename)
    tags_dict = sum_times_for_tags(entrys)
    print_raport(tags_dict)


if __name__ == "__main__":
    main()