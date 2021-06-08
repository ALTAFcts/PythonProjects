# -*- coding: utf-8 -*-
"""
Simple Linkedin crawler to collect user's  profile data.

@author: idwaker

To use this you need linkedin account, all search is done through your account

Requirements:
    python-selenium
    python-click
    python-keyring

Tested on Python 3 not sure how Python 2 behaves

D:\Python\Python37-32\Lib\site-packages\selenium\webdriver\phantomjs
"""

import sys
import csv
import time
import click
import getpass
import keyring
from selenium import webdriver
from selenium.common.exceptions import (WebDriverException,
                                        NoSuchElementException)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(chrome_options=options)


LINKEDIN_URL = 'https://www.linkedin.com'


class UnknownUserException(Exception):
    pass


class UnknownBrowserException(Exception):
    pass


class WebBus:
    """
    context manager to handle webdriver part
    """

    def __init__(self, browser):
        self.browser = browser
        self.driver = None

    def __enter__(self):
        # XXX: This is not so elegant
        # should be written in better way
        if self.browser.lower() == 'firefox':
            self.driver = webdriver.Firefox()
        elif self.browser.lower() == 'chrome':
            self.driver = webdriver.Chrome()
        elif self.browser.lower() == 'phantomjs':
            self.driver = webdriver.PhantomJS()
        else:
            raise UnknownBrowserException("Unknown Browser")

        return self

    def __exit__(self, _type, value, traceback):
        if _type is OSError or _type is WebDriverException:
            click.echo("Please make sure you have this browser")
            return False
        if _type is UnknownBrowserException:
            click.echo("Please use either Firefox, PhantomJS or Chrome")
            return False

        self.driver.close()


def get_password(username):
    """
    get password from stored keychain service
    """
    password = keyring.get_password('linkedinpy', username)
    if not password:
        raise UnknownUserException("""You need to store password for this user
                                        first.""")

    return password


def login_into_linkedin(driver, username):
    """
    Just login to linkedin if it is not already loggedin
    """
    userfield = driver.find_element_by_id('login-email')
    passfield = driver.find_element_by_id('login-password')

    submit_form = driver.find_element_by_class_name('login-form')

    password = get_password(username)

    # If we have login page we get these fields
    # I know it's a hack but it works
    if userfield and passfield:
        userfield.send_keys(username)
        passfield.send_keys(password)
        submit_form.submit()
        click.echo("Logging in")


def collect_names(filepath):
    """
    collect names from the file given
    """
    names = []
    with open(filepath, 'r') as _file:
        names = [line.strip() for line in _file.readlines()]
    return names


@click.group()
def cli():
    print('inside click')
    """
    First store password

    $ python linkedin store username@example.com
    Password: **

    Then crawl linkedin for users

    $ python linkedin crawl username@example.com with_names output.csv --browser=firefox
    """
    pass


@click.command()
@click.option('--browser', default='chrome', help='Browser to run with')
@click.argument('username')
@click.argument('infile')
@click.argument('outfile')
def crawl(browser, username, infile, outfile):
    """
    Run this crawler with specified username
    """

    # first check and read the input file
    all_names = collect_names(infile)

    #fieldnames = ['fullname', 'locality', 'industry', 'current summary', 'past summary', 'education', ]
    fieldnames = ['fullname', 'profileimage', 'profilelink', 'designation', 'company', 'location', ]
    # then check we can write the output file
    # we don't want to complete process and show error about not
    # able to write outputs
    with open(outfile, 'w') as csvfile:
        # just write headers now
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    searchdivs =  './/div[@class="search-result__wrapper"]'   #'.//span[@class="name actor-name"]'  #'.//a[@data-control-name="search_srp_result"]'

    # now open the browser
    with WebBus(browser) as bus:
        bus.driver.get(LINKEDIN_URL)       
        login_into_linkedin(bus.driver, username)       

        for name in all_names:
            click.echo("Getting ...")
            #click.echo(name)
            try:
                search_input = bus.driver.find_element_by_xpath('//input[@role="combobox"]')  #find_element_by_id('main-search-box')
                click.echo(search_input)
                time.sleep(3)
            except NoSuchElementException:
                continue

            search_input.send_keys(name)           
            search_form = bus.driver.find_element_by_xpath('.//button[@data-control-name="nav.search_button"]')  #find_element_by_id('search-typeahead-v2__button typeahead-icon')            
            time.sleep(5)            
            search_form.click()
                                
            #click.echo("search result")
            
            time.sleep(5)
            bus.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")   
#            search_button = bus.driver.find_element_by_xpath(search_btn)
#            search_button.click()

            profiles = []

            # collect all the profile links
            results = None
            #click.echo(profiles)
            try:
                results = bus.driver.find_element_by_xpath('//ul[@class="search-results__list list-style-none mt2"]') #find_element_by_id('results-container')
            except NoSuchElementException:
                continue
            
            #click.echo(results)            
            
            searchs = results.find_elements_by_xpath(searchdivs)
            time.sleep(5)
            # get all the links before going through each page
            #links = [link.get_attribute('href') for link in links]
            #click.echo(searchs);
            for search in searchs:

                fullname = None
                fullname_xpath = './/span[@class="name actor-name"]'
                try:
                    fullname = search.find_element_by_xpath(fullname_xpath)
                except NoSuchElementException:
                    # we store empty fullname : notsure for this
                    fullname = ''
                else:
                    fullname = fullname.text.strip()

                profileimage = None
                try:                
                    imgUrl1 = search.find_element_by_tag_name('img')
                except NoSuchElementException:
                    profileimage = ''
                else:
                    profileimage = imgUrl1.get_attribute("src")

                profilelink = None
                profile_xpath = './/div[@class="search-result__info pt3 pb4 ph0"]//a'
                try:                
                    profilelink = search.find_element_by_xpath(profile_xpath)
                except NoSuchElementException:
                    profilelink = ''
                else:
                    profilelink = profilelink.get_attribute("href")


                designation = ""
                designationDet = None
                company = ""               
                designation_xpath = './/p[@class="subline-level-1 t-14 t-black t-normal search-result__truncate"]'
                try:                
                    designationDet = search.find_element_by_xpath(designation_xpath)
                except NoSuchElementException:
                    designationDet = ''
                else:
                    designationDet = designationDet.text.strip()
                    details = designationDet.lower()
                    details = details.split(" ")
                    click.echo(details)
                    s = ""
                    index = 0
                    for i in details:
                        if(i != "at" and index == 0):
                            designation+=str(i)+str(" ")                            
                        else:
                            index = 1
                            company+=str(i)+str(" ")
                    
                    #click.echo(designation)
                    #click.echo(company)


                location = None
                location_xpath = './/p[@class="subline-level-2 t-12 t-black--light t-normal search-result__truncate"]'
                try:                
                    location = search.find_element_by_xpath(location_xpath)
                except NoSuchElementException:
                    location = ''
                else:
                    location = location.text.strip()


                #image = i.find_element_by_tag_name("img")
                #img_src = image.get_attribute("src")
                #click.echo(profileimage)
                data = {
                    'fullname': fullname,
                    'profileimage': profileimage,
                    'profilelink': profilelink,
                    'designation': designation,
                    'company': company,
                    'location': location,
                }
                profiles.append(data)
                
            
            with open(outfile, 'a+') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerows(profiles)

            click.echo("Obtained ..." + name)


@click.command()
@click.argument('username')
def store(username):
    """
    Store given password for this username to keystore
    """
    passwd = getpass.getpass()
    keyring.set_password('linkedinpy', username, passwd)
    click.echo("Password updated successfully")


cli.add_command(crawl)
cli.add_command(store)


if __name__ == '__main__':
    cli()
