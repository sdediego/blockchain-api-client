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
