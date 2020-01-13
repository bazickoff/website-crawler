import os
import urllib.request
import logging

import pandas as pd
from collections import defaultdict


class FiFiCrawler(object):
  """
   A crawler to download Find it Fix it (FiFi) images using URLs from the dataset
   """
  # Constants
  NAME_SEPARATOR = '_'

  def __init__(self, filename, image_column_name, service_request_column_name, parent_dir):
    """
    Initialize variables and create a dictionary containing categories.

    :param filename: Name of the file that will be used for crawling.
    :param image_column_name: Column name of the field that has URLs of images.
    :param service_request_column_name: Column name of the Service Request Number.
    :param parent_dir: Name of the parent directory where images for each category will be downloaded.
    """
    self.logger = logging.getLogger(__name__)

    self.parent_dir = parent_dir
    self.image_column_name = image_column_name
    self.service_request_column_name = service_request_column_name
    self.xls = pd.ExcelFile(filename)
    self.fifi_dict = defaultdict.fromkeys(self.xls.sheet_names) # Excel file sheet names map to categories


  def crawl(self):
    """
    Crawls all images in all categories
    """

    self.load_dataframes()
    self.create_directories()
    self.download_images_by_category()


  def load_dataframes(self):
    """
    Populates dataframes of each category into the fifi dictionary
    """

    for name in self.fifi_dict.keys():
      self.fifi_dict[name] = pd.read_excel(self.xls, name)


  def create_directories(self):
    """
    Creates separate folders for each category if it does not exist.
    """

    for key, df in self.fifi_dict.items():
      i = 0
      directory_path = os.path.join(self.parent_dir, key)

      try:
        if not os.path.exists(directory_path):
          os.makedirs(directory_path)
      except os.error:
        self.logger.error('Error while trying to create directory', exc_info=True)


  def download_images_by_category(self):
    """
    Downloads images in every category.
    """

    for category, df in self.fifi_dict.items():
      df = df[df['Photo'].notnull()] # removes rows without URLs
      i = 0
      for (idx, row) in df.iterrows():
          self.download_image(category, row[self.image_column_name], row[self.service_request_column_name], i)
          i = i + 1

  def download_image(self, category, image_url, service_request_number, index):
      """
      Downloads image to a local directory using the given URL.
      :param category: category of the image
      :param image_url: URL that is used to download the image
      :param service_request_number: Service request number generated for the given compliant/request.
      :param index:
      """

      file_extension = self.get_file_extension(image_url)
      if file_extension:
        local_file_path = self.build_local_file_path(category, service_request_number, index, file_extension)

        try:
          urllib.request.urlretrieve(image_url, local_file_path)
        except (urllib.error.URLError, IOError) as e:
          self.logger.error("Error downloading image " + image_url +  " from category: "
                            +  category + " with service request number: " + service_request_number)
          # raise e
        except (Exception) as e:
          self.logger.error("Error downloading image " + image_url +  " from category: "
                            +  category + " with service request number: " + service_request_number + local_file_path, exc_info=True)


  def get_file_extension(self, url):
    """
    Extracts extension of the image from the URL

    :param url: Link to download the image.
    :return file_extension: A string containing the extension of file. Ex" '.jpg'
    """

    filename_with_extension = os.path.basename(url)
    filename, file_extension = os.path.splitext(filename_with_extension)
    return file_extension

  def build_local_file_path(self, category, service_request_number, index, file_extension):
    """
    Generates a file name and builds a relative path.

    :param category: The category of the request.
    :param service_request_number: Unique identifier of the request
    :param index: An index to make sure there are no duplicate filenames.
    :param file_extension: Extension of the file. Ex. "jpg"
    :return: A string containing relative path with filename.
    """

    file_name = category \
                + FiFiCrawler.NAME_SEPARATOR \
                + service_request_number \
                + FiFiCrawler.NAME_SEPARATOR \
                + str(index) \
                + file_extension

    return os.path.join(self.parent_dir, category, file_name)

if __name__ == '__main__':
  # TO-DO: Put the config in a json file and read from it. Refer: https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
  logging.basicConfig(filename='fifi_crawler.log',
                      filemode='w',
                      level=logging.DEBUG,
                      format='%(levelname)s:%(asctime)s:%(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p')

  crawler = FiFiCrawler('fifi_data.xlsx', 'Photo', 'Service Request Number', 'data')
  crawler.crawl()


