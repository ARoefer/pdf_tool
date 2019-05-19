Terminal PDF Tool
=================

Are you tired of there not being a simple pdf manipulation tool able to do simple operations like stiching together a couple documents? Then here you go! This is a very simple Python-tool that allows you to manipulate pdfs using the terminal. Right now it only does simple appending and inserting to files. The sturcture is modular and easy to extend. Feel free to contribute more functionality.

Prerequisites
-------------

You need at least Python 2.7 (3.x might work too) and the pdfrw package. Install it via pip:

```bash
pip install pdfrw
```

Running
-------

Just run the `pdf_manipulator.py` file on a terminal. Without giving any arguments to it, it will list all the available operations.

Some arguments support selecting individual pages from documents instead of using the entire document. These ranges work the same as Python's ranges with the added twist, that they combine individual indices and ranges. Below are some examples.

```
my.pdf[0, 2, -1]   -> Selects pages 1, 3 and the last page.
my.pdf[:5]         -> Selects the first five pages.
my.pdf[-5:]        -> Selects the last five pages.
my.pdf[5:]         -> Selects everything but the first five pages.
my.pdf[-5:]        -> Selects everything but the last five pages.
my.pdf[2, 3, 5:12] -> Selects pages 2, 4, 6, ..., 11.
```