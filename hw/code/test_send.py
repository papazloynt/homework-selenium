import os

from pages.auth import AuthPage
from pages.outcomes import OutcomePage
from pages.sends import SendPage, SendInfo
from dotenv import load_dotenv


class TestSend:
    def setup_method(self):
        load_dotenv()  # LOGIN and PASSWORD
        self.longs = [SendInfo('1 test address', '1 test long long long long long long long long long theme',
                          '1 test text'),
                 SendInfo('1 test long long long long long long long long long address', '1 test theme',
                          '1 test text')]

        self.wrong_address = [SendInfo('', 'sda', ''), SendInfo('wrong_name', 'asd', '')]

        self.SAMPLE_EMPTY_MESSAGE = SendInfo(address=os.getenv('LOGIN'), theme='', text='1 test text')
        self.SAMPLE_MESSAGE = SendInfo(address=os.getenv('LOGIN'), theme='1 test theme', text='1 test text')

    def test_wrong_address_of_recipient(self, browser):
        auth_page = AuthPage(browser)
        auth_page.go_to_site()
        auth_page.login(os.getenv('LOGIN'), os.getenv('PASSWORD'))

        for wa in self.wrong_address:
            send_page = SendPage(browser)
            send_page.go_to_site()
            send_page.create_message(wa)
            assert send_page.is_wrong()

    def test_create_big_info_message_error(self, browser):
        auth_page = AuthPage(browser)
        auth_page.go_to_site()
        auth_page.login(os.getenv('LOGIN'), os.getenv('PASSWORD'))

        outcoming_page = OutcomePage(browser)
        outcoming_page.go_to_site()
        prev = outcoming_page.list_count()

        for l in self.longs:
            send_page = SendPage(browser)
            send_page.go_to_site()
            send_page.create_message(l)

        outcoming_page.go_to_site()
        after = outcoming_page.list_count()

        assert prev == after

    def test_send_with_empty_theme(self, browser):
        auth_page = AuthPage(browser)
        auth_page.go_to_site()
        auth_page.login(os.getenv('LOGIN'), os.getenv('PASSWORD'))

        send_page = SendPage(browser)
        send_page.go_to_site()
        send_page.create_message(self.SAMPLE_EMPTY_MESSAGE)
        assert send_page.is_dialog_appear()

    def test_success_send(self, browser):
        auth_page = AuthPage(browser)
        auth_page.go_to_site()
        auth_page.login(os.getenv('LOGIN'), os.getenv('PASSWORD'))

        outcoming_page = OutcomePage(browser)
        outcoming_page.go_to_site()
        prev = outcoming_page.list_count()

        send_page = SendPage(browser)
        send_page.go_to_site()
        send_page.create_message(self.SAMPLE_MESSAGE)

        outcoming_page.go_to_site()
        after = outcoming_page.list_count()

        assert prev + 1 == after
