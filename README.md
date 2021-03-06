[![Total alerts](https://img.shields.io/lgtm/alerts/g/ARoefer/pdf_tool.svg?style=flat-square&logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ARoefer/pdf_tool/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ARoefer/pdf_tool.svg?style=flat-square&logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ARoefer/pdf_tool/context:python)

Terminal PDF Tool
=================

Are you tired of there not being a simple pdf manipulation tool able to do simple operations like stiching together a couple documents? Then here you go! This is a very simple Python-tool that allows you to manipulate pdfs using the terminal. Right now it only does simple appending and inserting to files. The sturcture is modular and easy to extend. Feel free to contribute more functionality.

Prerequisites
-------------

You need at least Python 2.7 (3.x works too) and the pdfrw package. Install it via pip:

```bash
pip install pdfrw
```

Running
-------

Just run the `pdf_manipulator.py` file on a terminal. Without giving any arguments to it, it will list all the available operations.

Some arguments support selecting individual pages from documents instead of using the entire document. These ranges work similar to Python's ranges with the added twist, that they combine individual indices and ranges. Below are some examples.

```
my.pdf[1, 3, -1]   -> Selects pages 1, 3 and the last page.
my.pdf[:5]         -> Selects the first five pages.
my.pdf[-5:]        -> Selects the last five pages.
my.pdf[5:]         -> Selects all pages starting at page 5.
my.pdf[:-5]        -> Selects everything but the last five pages.
my.pdf[2, 3, 5:12] -> Selects pages 2, 3, 5, ..., 12.
```
Using this syntax you could create a new file `my.pdf` from the files `bla.pdf`, `bar.pdf`, `foo.pdf` like so:

```bash
./pdf_manipulator.py -an my.pdf bla.pdf[1] bar.pdf[4:6] bla.pdf[3] foo.pdf[-3:]
```
where the final file then consists of the first page of `bla.pdf` followed by pages 4-6 from `bar.pdf`, followed by the third page of `bla.pdf`, and concluded by the last three pages of `foo.pdf`.
