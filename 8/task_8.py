from __future__ import unicode_literals

from selenium import webdriver
import time
import json
import sys

website = "onliner.by"


def test1():
    # Create a new instance of the Firefox driver
    driver = webdriver.Chrome()
    # go to the google home page
    driver.get('http://{}/'.format(website))

    key = 'samsung'

    search_class = driver.find_element_by_id('fast-search')
    input_element = search_class.find_element_by_css_selector('.fast-search__input')
    input_element.send_keys(key)

    submit_element = search_class.find_element_by_css_selector('.fast-search__submit')
    submit_element.submit()

    for element in driver.find_elements_by_css_selector('.result__wrapper'):
        a = element.find_element_by_css_selector('.product__title-link')
        assert(a.text.contains(key))

    driver.quit()
    

def test2():
    driver = webdriver.Chrome()

    driver.get("http://{}/".format('catalog.onliner.by'))

    navigations = driver.find_elements_by_class_name('catalog-navigation-classifier__item')
    navigation = navigations[1]

    navigation.click()

    items = driver.find_elements_by_class_name('catalog-navigation-list__link-inner')

    i = None

    for item in items:
        it = item.find_element_by_css_selector('a')
        i = it if it.get_attribute('title') == 'Компьютеры' else i

    i.click()

    assert(driver.current_url == 'https://catalog.onliner.by/desktoppc')

    driver.quit()


def test3():
    driver = webdriver.Chrome()

    driver.get('http://{}/'.format('catalog.onliner.by/desktoppc'))

    elements = driver.find_elements_by_class_name('schema-filter__checkbox-text')
    items = []
    for item in elements:
        if item.text == 'Apple':
            items.append(item)

    item = items[0]

    item.click()

    elements = driver.find_elements_by_class_name('schema-product__group')
    it = None

    for el in elements[:2]:
        span = el.find_elements_by_class_name('i-checkbox')[0]
        span.click()

    btn = driver.find_elements_by_class_name('compare-button__sub')
    btn.click()

    assert('https://catalog.onliner.by/compare/md878rua+mgem2rua' == driver.current_url)

    driver.quit()


test1()

test2()

test3()

