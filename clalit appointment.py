from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ZEUT_NUMBER= "311874481"
YEAR_OF_BIRTH = "1986"
PHONE_NUMBER= "0548367811"
E_MAIL = "keren.drev@gmail.com"

zeut_number = ZEUT_NUMBER
year_of_birth = YEAR_OF_BIRTH
phone_number = PHONE_NUMBER
e_mail = E_MAIL

doctor_specialization =  "אורתופדיה"
city = "חיפה"
doctor_name = "זיידמן איתן"
what_hours_are_good_for_you = [11,12]

# TODO : to add install only if its not working
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

URL = 'https://e-services.clalit.co.il/onlinewebquick/nvgq/tamuz/he-il'
driver.get(URL)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Entrance page~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# wait until the id_number box is clickable or for 10 sec
wait = WebDriverWait(driver, timeout=25)
id_number = wait.until(EC.element_to_be_clickable((By.NAME, "ctl00$ctl00$cphBody$bodyContent$ucQuickLogin$userId")))
id_number.send_keys(zeut_number)

birth_year = driver.find_element("id", "ctl00_ctl00_cphBody_bodyContent_ucQuickLogin_userYearOfBirth")
birth_year.send_keys(year_of_birth)

driver.find_element(By.ID, "ctl00_ctl00_cphBody_bodyContent_ucQuickLogin_btnLogin_lblInnerText").click()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Second page~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
time.sleep(1)
driver.get('https://e-services.clalit.co.il/OnlineWebQuick/QuickServices/Tamuz/TamuzTransferContentByService.aspx')

professionvisitbutton = driver.find_element(By.ID, "ProfessionVisitButton")
professionvisitbutton.click()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~3rd page~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Selected_specialization = driver.find_element(By.ID, 'SelectedSpecializationCode')
Selected_specialization.send_keys(doctor_specialization)  #
Selected_specialization.click()

selected_city = driver.find_element(By.ID, 'SelectedCityName')
selected_city.clear()
selected_city.send_keys(city)

try:
    # It's important to use the exact name of the doctor
    selected_doctor_name = driver.find_element(By.ID, 'SelectedDoctorName')
    selected_doctor_name.send_keys(doctor_name)
    selected_doctor_name.click()
finally:
    pass

# enter
submit_button = driver.find_element(By.CLASS_NAME, 'searchButton')
submit_button.send_keys(Keys.ENTER)

# choosing the doctor - from list , in the same page
physician_details_name = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.underline.doctorDetails')))
physician_details_name.text

# פה להוסיף עוד שיטה אחרת אם זה נכשל
# להוסיף  שיטה שלמה אחרת שבה מחפשים בתוך השמות את השם הנכון
if doctor_name == physician_details_name.text:
    try:
        submit_button_to_apointment = driver.find_element(By.CSS_SELECTOR,
                                                          '.pull-right.createVisitButton.wideButtonEnabled.diaryButton')
        submit_button_to_apointment.click()
    except NoSuchElementException:
        pass
    finally:
        # TODO AT THE FUTARE:defined a function that check if there is appointments for this dr in another clinic
        print("defined a function that check if there is appointments for this dr in another clinic")
        # find_if_their_is_appointments_available_for_this_dr()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4th page~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# enter all the available appointment at the first option (clinic) matchng the doctor name.
available_hour = driver.find_element(By.CSS_SELECTOR, ".pull-right.createVisitButton.wideButtonEnabled.diaryButton")
available_hour.click()


##~~~~~~~~~~~~~~~~~~~~move throw days~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_list_of_all_available_days_this_month():
    """creates  a list of dates in 2 forms """
    list_of_available_days = []
    available_days = driver.find_elements(By.CSS_SELECTOR, "a.ui-state-default")
    for day in available_days:
        list_of_available_days.append(day.text)
    return list_of_available_days, available_days


# list_of_available_days, available_days = create_list_of_all_available_days_this_month()

def go_to_next_day():
    """create_list_of_all_available_days_this_month() inside
        move to next day (one time every time its operated)
        retuens """
    time.sleep(3)
    current_day = driver.find_element(By.CSS_SELECTOR, '.ui-state-default.ui-state-active').text
    list_of_available_days, available_days = create_list_of_all_available_days_this_month()
    current_day_index = list_of_available_days.index(current_day)

    try:
        next_day_element = available_days[current_day_index + 1]
    except IndexError:
        print(f"out off range last day of the month ")
    else:
        wait_4_few_sec = WebDriverWait(driver, timeout=10)
        wait_4_few_sec.until(EC.element_to_be_clickable(next_day_element)).click()

    return len(list_of_available_days)


#number_of_days_with_appointments = go_to_next_day()


# #~~~~~~~~~~~~~~~~~~~~move throw hours ~~~~~~~~~~~~~~~~~~~~~~~~~~

def show_more_dates_option():
    """ In order to choose an hour with selenium the option have to be visible
    this function show all available appointment options
    #if clicked twice close additional hours PRONLAM"""
    # TODO rewrite function in more elegant way.

    try:
        show_more_hours = driver.find_elements(By.CSS_SELECTOR, "a.more")
        for time_of_the_day in show_more_hours:
            time_of_the_day.click()

            time.send_keys(Keys.PAGE_UP)
    except:
        pass


def find_appointment_on_defined_hours_of_a_certain_day(*args):
    """show_more_dates_option() inside
    exemple of use find_appointment_on_defined_hours_of_a_certen_day((7,8,9))
    """
    hours_in_which_its_good_hours = list(*args)

    # show more date options cose in selenim i need to see in order to click
    show_more_dates_option()

    # אם עובד להכניס לשואו מור

    # חסר נקודת עצירה כאשר יש כפתור הזמיני תור אבל הוא לא לחיץ
    def for_appoint_in_appointments():
        appointments = driver.find_elements(By.CSS_SELECTOR, ".margin-right .clearfix")
        for appoint in appointments:
            """here there is some that are len==0 i dont include tham"""
            try:
                if (len(appoint.text) == 16):
                    hour_str = (appoint.text[:2])
                    hour =  hour_str
                    #go 34 pixel down for every hour that is going
                    driver.execute_script("window.scrollBy(0,34)","")

                    if (int(hour) in hours_in_which_its_good_hours):
                        wait_4_few_sec = WebDriverWait(driver, timeout=10)
                        wait_4_few_sec.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".bigButtonEnabled.createVisitButton"))).click()

            except NoSuchElementException:
                print("you got NoSuchElementException and except NoSuchElementException: was operated, it happened when the appointment was "
                      "ordered ")
                break

    for_appoint_in_appointments()


# find_appointment_on_defined_hours_of_a_certen_day([7,8,9])


# #~~~~~~~~~~~~~~~~~~~~move throw month and years ~~~~~~~~~~~~~~~~~~~~~~~~~~

def change_year():
    driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-year").find_elements(By.TAG_NAME, "option")[-1].click()


def change_month():
    """change_year inside """
    select_month_of_the_year = Select(driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-month"))
    selected_month = select_month_of_the_year.first_selected_option.text
    if selected_month == "דצמבר":
        change_year()
        # chose the first option in the month dropdown
        driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-month").find_element(By.TAG_NAME, "option").click()
    else:
        months = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר',
                  'דצמבר']
        selected_month_index = months.index(selected_month)
        next_month = months[selected_month_index + 1]
        driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-month").send_keys(next_month)


# ~~~~~~~~~~~~~~~~~~~~EMAIL ADDRESS ~~~~~~~~~~~~~~~~~~~~~~~~~~
# WORKING WELL
def sent_me_appointment_details_to_mail_via_clalit():
    # find_and_fill_email_to_send_it_to_my_mail
    driver.find_element(By.ID, "EmailAddress").send_keys(e_mail)
    wait = WebDriverWait(driver, timeout=10)
    sent_email = wait.until(EC.element_to_be_clickable((By.ID, "btnSendEmailButton")))
    sent_email.click()


def running_all(hours):


    find_appointment_on_defined_hours_of_a_certain_day(hours)
    number_of_days_with_appointments = go_to_next_day()



    # range(0,5) because it's the number of month ahead Clalit show available appointments
    for month in range(0, 5):
        time.sleep(1)
        for c in range(0, number_of_days_with_appointments):
            find_appointment_on_defined_hours_of_a_certain_day(hours)
            try:
                sent_me_appointment_details_to_mail_via_clalit()
            except:
                pass

            go_to_next_day()
        change_month()


running_all(what_hours_are_good_for_you)
