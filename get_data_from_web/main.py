import config
import scrape_xedapgiakho
import scrape_bike2school
import API
from controller.control import ConfigController


def runConfig():
    print(config.delete_all_bikes())
    print(config.set_all_website_waiting())
    print(config.send_email_for_prepare(API.get_subject_email(), API.create_message_for_email(API.get_message_waiting())))


def runScrapeXedapGiaKho():
    # lấy url của website xepdapgiakho
    url = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get", API.get_keyword_xedapgiakho())["website"]
    scrape_xedapgiakho.general_xedapgiakho(url)


def runScrapeBike2school():
    # lấy url của website bike2schol
    website = ConfigController.getIdByKeyword(f'{API.get_context_config()}/get', API.get_keyword_bike2school())[
        'website']
    scrape_bike2school.general_bike2school(website)


runConfig()
runScrapeXedapGiaKho()
runScrapeBike2school()




