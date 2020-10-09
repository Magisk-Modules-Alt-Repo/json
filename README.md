# JSON
Magisk Manager JSON file generation for the repository list

# Why?
Magisk Manager custom repositories work by providing a JSON file with information about each of the available modules, as opposed to providing a GitHub URL. This repository is responsible for keeping the JSON file updated, and thereby keeping the Magisk Manager repostory list updated.

# How?
A simple Python script called `generate.py` takes an access token as an input, and prints a the JSON format for the Alt-Repo. We use a GitHub Action to take care of the commit process to this repository.
