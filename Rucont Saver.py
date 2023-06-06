import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pathlib
import os
from selenium.webdriver.common.keys import Keys

os.chdir(pathlib.Path(__file__).parent.absolute())

login = 'lstu_s1211060013'
password = 'Bly9E5k'

options = Options()
#options.headless = True
driver = webdriver.Firefox(options=options)
driver.set_window_size(1920, 1080)

def authorization(login, password):
	print('Провожу авторизацию...')
	driver.get('https://lib.rucont.ru/search')
	time.sleep(5)
	enter = driver.find_element_by_link_text('Вход')
	driver.execute_script('arguments[0].click();', enter)
	login_field = driver.find_element_by_xpath('/html/body/application/sign-in-form/div[1]/div/div/form/div[2]/div[1]/input')
	password_field = driver.find_element_by_xpath('/html/body/application/sign-in-form/div[1]/div/div/form/div[2]/div[2]/input')
	login_field.send_keys(login)
	password_field.send_keys(password)
	enter = driver.find_element_by_xpath("//*[contains(text(), 'Войти')]")
	driver.execute_script('arguments[0].click();', enter)
	time.sleep(5)
	check_login = driver.find_elements_by_xpath("//*[contains(text(), 'Личный кабинет')]")
	if check_login:
		print('Авторизация прошла успешно!')
		return 1
	else:
		print('Неверные логин и пароль!')
		return 0

def saver():
	driver.get('https://lib.rucont.ru/efd/641040/info')
	time.sleep(5)
	read_button = driver.find_element_by_xpath("//*[contains(text(), 'Читать')]")
	driver.execute_script('arguments[0].click();', read_button)
	time.sleep(5)
	driver.switch_to.window(driver.window_handles[1])
	num_pages = int(''.join([i for i in driver.find_element_by_xpath('//*[@id="numPages"]').text if i in '0123456789']))
	book_name = driver.title
	if not os.path.isdir(book_name):
		os.makedirs(book_name)
	os.chdir(book_name)
	for i in range(1, num_pages + 1):
		page_input = driver.find_element_by_xpath('//*[(@id = "pageNumber")]')
		driver.execute_script("arguments[0].value = ''", page_input)
		page_input.send_keys(str(i))
		page_input.send_keys(Keys.ENTER)
		full_mode = driver.find_element_by_xpath('//*[@id="presentationMode"]')
		full_mode.click()
		time.sleep(2.5)
		page = driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div[4]/div/div[{i}]/div[2]')
		page.screenshot(f'{i}.png')
		time.sleep(1)
		page_input.send_keys(Keys.ESCAPE)
		time.sleep(2.5)

if __name__ == '__main__':
	if authorization(login, password):
		saver()
