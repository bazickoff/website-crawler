import os
import urllib.request
import logging

import pandas as pd
from collections import defaultdict

<<<<<<< HEAD
from fifi_log import start_logging

=======
>>>>>>> 74b5f874cafe3fee806cc964559997a60cae2ada

class FiFiCrawler(object):
  """
   A crawler to download Find it Fix it (FiFi) images using URLs from the dataset
   """
  # Constants
<<<<<<< HEAD
  UNDERSCORE = '_'
  logger = logging.getLogger(__name__)
=======
  NAME_SEPARATOR = '_'
>>>>>>> 74b5f874cafe3fee806cc964559997a60cae2ada

  def __init__(self, filename, image_column_name, service_request_column_name, parent_dir):
    """
    Initialize variables and create a dictionary containing categories.

    :param filename: Name of the file that will be used for crawling.
    :param image_column_name: Column name of the field that has URLs of images.
    :param service_request_column_name: Column name of the Service Request Number.
<<<<<<< HEAD
    :param parent_dir: Parent directory where images for each category will be downloaded.
    """

    self.parent_dir = parent_dir  # To DO: If ends with /, remove /
    self.image_column_name = image_column_name
    self.service_request_column_name = service_request_column_name
    self.xls = pd.ExcelFile(filename)
    self.fifi_dict = defaultdict.fromkeys(xls.sheet_names) # Excel file sheet names map to categories
=======
    :param parent_dir: Name of the parent directory where images for each category will be downloaded.
    """
    self.logger = logging.getLogger(__name__)

    self.parent_dir = parent_dir
    self.image_column_name = image_column_name
    self.service_request_column_name = service_request_column_name
    self.xls = pd.ExcelFile(filename)
    self.fifi_dict = defaultdict.fromkeys(self.xls.sheet_names) # Excel file sheet names map to categories
>>>>>>> 74b5f874cafe3fee806cc964559997a60cae2ada


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

<<<<<<< HEAD
    for name in self.fifi_dict.keys(self):
      self.fifi_dict[name] = pd.read_excel(xls, name)
=======
    for name in self.fifi_dict.keys():
      self.fifi_dict[name] = pd.read_excel(self.xls, name)
>>>>>>> 74b5f874cafe3fee806cc964559997a60cae2ada


  def create_directories(self):
    """
    Creates separate folders for each category if it does not exist.
    """

<<<<<<< HEAD
    for key, df in fifi_dict.items():
      i = 0
      directory_path = self.parent_dir + key
=======
    for key, df in self.fifi_dict.items():
      i = 0
      directory_path = os.path.join(self.parent_dir, key)
>>>>>>> 74b5f874cafe3fee806cc964559997a60cae2ada

      try:
        if not os.path.exists(directory_path):
          os.makedirs(directory_path)
<<<<<<< HEAD
      except OSERROR:
        logger.error('Error while trying to create directory', exc_info=True)
=======
      except os.error:
        self.logger.error('Error while trying to create directory', exc_info=True)
>>>>>>> 74b5f874cafe3fee806cc964559997a60cae2ada


  def download_images_by_category(self):
    """
    Downloads images in every category.
    """

<<<<<<< HEAD
    for category, df in fifi_dict.items():
      df = df[df['Photo'].notnull()] # removes rows without URLs
      for row in df:
          self.download_image(category, row[self.image_column_name], row[self.service_request_column_name])
=======
    for category, df in self.fifi_dict.items():
      df = df[df['Photo'].notnull()] # removes rows without URLs
      i = 0
      for (idx, row) in df.iterrows():
          self.download_image(category, row[self.image_column_name], row[self.service_request_column_name], i)
>>>>>>> 74b5f874cafe3fee806cc964559997a60cae2ada
          i = i + 1

  def download_image(self, category, image_url, service_request_number, index):
      """
      Downloads image to a local directory using the given URL.
      :param category: category of the image
      :param image_url: URL that is used to download the image
      :param service_request_number: Service request number generated for the given compliant/request.
      :param index:
      """

<<<<<<< HEAD
      file_extension = get_file_extension(image_url)
      if file_extension:
        local_file_path = FiFiCrawler.build_local_file_path(category, service_request_number, index, file_extension)

        try:
          urllib.request.urlretrieve(image_url, local_file_path)
        except (urllib2.URLError, IOError) as e:
          logger.error("Error downloading image " + image_url +  "with filename: " + file_name, , exc_info=True)
          # raise e
        except e:
          logger.error("Error while downloading image with service_request_number " + service_request_number " and category " + category, exc_info=True)
=======
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
>>>>>>> 74b5f874cafe3fee806cc964559997a60cae2ada


  def get_file_extension(self, url):
    """
    Extracts extension of the image from the URL
<<<<<<< HEAD
    :param url:
=======

    :param url: Link to download the image.
>>>>>>> 74b5f874cafe3fee806cc964559997a60cae2ada
    :return file_extension: A string containing the extension of file. Ex" '.jpg'
    """

    filename_with_extension = os.path.basename(url)
    filename, file_extension = os.path.splitext(filename_with_extension)
    return file_extension

<<<<<<< HEAD
  @staticmethod
  def build_local_file_path(category, service_request_number, index, file_extension):
    """

    """

    file_name = category \
                + self.UNDERSCORE \
                + service_request_number \
                + self.UNDERSCORE \
                + index \
                + self.UNDERSCORE \
                + file_extension

    return os.path.join(category, file_name)

if __name__ == '__main__':
  # TO-DO: Put the config in a json file and read from it. Refer: https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
  logging.basicConfig(filename='fifi_crawler.log', 
                      filemode='w', 
                      level=logging.DEBUG, 
                      format='%(levelname)s:%(asctime)s:%(message)s', 
                      datefmt='%m/%d/%Y %I:%M:%S %p')

  crawler = FiFiCrawler('fifi_data.xlsx', 'Photo', 'Service Request Number', 'data')
=======
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
>>>>>>> 74b5f874cafe3fee806cc964559997a60cae2ada


