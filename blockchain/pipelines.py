#!/usr/bin/env python
# encoding: utf-8


class JSONFileWriterPipeline(object):
    """
    Enable persist data in JSON file.
    """

    def __init__(self, filepath):
        """
        Initialize JSON file writer class config.

        :param str filepath: json file path.
        """
        self._file = path

    def __str__(self):
        """
        Represent class via params string.

        :return str: class representation.
        """
        params = {
            'class': self.__class__.__name__,
            'path': dirname(self._file),
            'filename': basename(self._file),
        }
        return str(params)
