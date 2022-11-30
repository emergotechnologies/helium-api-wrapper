"""Result Handler.

.. module:: ResultHandler

:synopsis: Functions to export the data from Helium API to a file

.. moduleauthor:: DSIA21

"""

import logging
import os
import types

import pandas as pd


class ResultHandler:
    """Object to handle the result of the API calls.

    :param data: The data to be written.
    :type data: Union[dict, list, types.GeneratorType]

    :param file_format: The file format to be written.
    :type file_format: str

    :param file_name: The name of the file to be written.
    :type file_name: str

    :param path: The path to the file to be written.
    :type path: str

    :param logger: The logger to be used, defaults to None
    :type logger: logging.Logger

    :return: None
    """

    def __init__(
        self, data, file_format, file_name, path, logger: logging.Logger = None
    ):
        self.data = data
        self.file_format = file_format
        self.file_name = file_name
        self.path = path
        os.makedirs(self.path, exist_ok=True)
        self.logger = logger
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger
        # self.check_data()
        # self.data = pd.DataFrame(self.data)

    def append(self, obj):
        """Apppends a dataframe to the existing data."""
        self.data = pd.concat([self.data, pd.DataFrame(obj)])

    def write(self):
        """Write the data to a file."""
        # @todo: implement data checks
        self.check_data()
        if self.file_format == "csv":
            self.write_csv()
        elif self.file_format == "json":
            self.write_json()
        elif self.file_format == "pickle":
            self.write_pickle()
        elif self.file_format == "feather":
            self.write_feather()
        elif self.file_format == "parquet":
            self.write_parquet()
        else:
            self.logger.error(f"File format {self.file_format} not supported.")
        self.logger.info(f"File {self.file_name} saved to {self.path}")

    def write_csv(self):
        """Write the data to a csv file."""
        self.data.to_csv(os.path.join(self.path, self.file_name + ".csv"))

    def write_json(self):
        """Write the data to a json file."""
        self.data.to_json(
            os.path.join(self.path, self.file_name + ".json"), orient="records"
        )

    def write_pickle(self):
        """Write the data to a pickle file."""
        self.data.to_pickle(os.path.join(self.path, self.file_name + ".pkl"))

    def write_feather(self):
        """Write the data to a feather file."""
        self.data.to_feather(os.path.join(self.path, self.file_name + ".feather"))

    def write_parquet(self):
        """Write the data to a parquet file."""
        self.data.to_parquet(
            os.path.join(self.path, self.file_name + ".parquet"),
        )

    def check_data(self):
        """Check the data for potential problems."""
        if self.data is None:
            self.logger.error("No data given.")
            raise ValueError("No data given.")
        if isinstance(self.data, dict):
            self.data = pd.DataFrame(self.data)
            return
        if isinstance(self.data, list):
            return
        if isinstance(self.data, types.GeneratorType):
            self.logger.info("Generator given. Start scraping ...")
            self.data = pd.DataFrame(self.data)
            return
        if isinstance(self.data, pd.DataFrame):
            return
        else:
            self.logger.error("Data is not usable.")
            raise ValueError("Data is not usable.")
