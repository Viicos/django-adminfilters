import pytest
from demo.management.commands.init_demo import sample_data
from demo.utils import ChangeListWrapper
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

pytestmark = pytest.mark.selenium


@pytest.fixture
def data():
    sample_data()


def get_elements(selenium):
    container = selenium.find_element(By.ID, 'year_of_birth')
    return [container.find_element(By.CSS_SELECTOR, 'input[type=text]'),
            ChangeListWrapper.find_in_page(selenium)]


@pytest.mark.parametrize('value,expected', [('1955', lambda n: n == 1955),
                                            ('>1953', lambda n: n > 1953),
                                            ('<>1955', lambda n: n != 1955),
                                            ('<1947', lambda n: n != 1947),
                                            ('<=1947', lambda n: n <= 1947),
                                            ('1955,1953', lambda n: n in [1953, 1955]),
                                            ('1953..1955', lambda n: n in range(1953, 1955 + 1)),
                                            ],
                         ids=['=', '>1', '<>', '<', '<=', 'list', 'range'])
@pytest.mark.selenium
def test_number_filter(admin_site, value, expected):
    input_text, cl = get_elements(admin_site.driver)

    input_text.send_keys(value)
    input_text.send_keys(Keys.ENTER)
    input_text, cl = get_elements(admin_site.driver)
    years = list(map(int, cl.get_values(None, 6)))
    filtered = list(filter(expected, years))
    assert years == filtered
