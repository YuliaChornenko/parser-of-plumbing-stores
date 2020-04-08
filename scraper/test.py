from scraper.scraper_1 import Scraper
from scraper.site_links import sandi_link, antey_link


sandi_param_list = Scraper.get_param_list(Scraper.get_soup(sandi_link), 'param')
sandi_category_list = Scraper.get_category_list(Scraper.get_soup(sandi_link))

antey_param_list = Scraper.get_param_list(Scraper.get_soup(antey_link), 'parameter')
antey_category_list = Scraper.get_category_list(Scraper.get_soup(antey_link))


# n = Scraper.get_antey_products(Scraper.get_soup(antey_link))