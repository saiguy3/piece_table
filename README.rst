===========
Piece Table
===========

.. image:: https://api.travis-ci.com/saiguy3/piece_table.svg?branch=master
   :target: https://travis-ci.com/github/saiguy3/piece_table
   :alt: piece-table on TravisCI

.. image:: https://img.shields.io/pypi/v/piece-table.svg
   :target: https://pypi.org/project/piece-table
   :alt: piece-table on PyPI

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/saiguy3/piece_table/blob/master/LICENSE
   :alt: MIT License badge


About piece_table
-----------------

Early implementation of the piece table data structure in Python. 


A piece table is an efficient data structure to represent a series of edits to a text document. A more detailed discussion can be found here_. Inspired by the JavaScript implementation_.

.. _here: https://darrenburns.net/posts/piece-table/
.. _implementation: https://github.com/sparkeditor/piece-table/blob/master/index.js


Installation
------------

To install the package, run the following:

.. code:: bash

    pip install piece-table


Usage
-----

Current usage is very basic, but will hopefully improve in the future. 

Basic use is demonstrated below.

.. code:: python

    from piece_table import PieceTable

    document = PieceTable("Initialize a document with some text.")

    document.insert("Add some text to the start of the document. ", 0)

    # Delete the inserted text
    document.delete(0, 44)

    text_sequence = document.get_text()
    # text_sequence == "Initialize a document with some text."

    sub_string = document[13:21]
    # sub_string == "document"


Testing
-------

To test the package, run the following:

.. code:: bash

    python -m unittest discover -s tests