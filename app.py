from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, jsonify,render_template,request
import time
import re

def get_course_semester(url):
    # Extract the course and semester information from the URL using regex
    match = re.search(r'/(\w+\d+)semresult', url)
    if match:
        course_semester = match.group(1)
        course = re.search(r'^\D+', course_semester).group()
        semester = int(re.search(r'\d+$', course_semester).group())
        print(semester)
        return ("course : ",course,"\nsemester:", semester)
    else:
        return None

app = Flask(__name__)
# run_with_ngrok(app) 

regarray = ['mm20ccsr22','mm20ccsr18', 'mm20ccsr16', 'mm20ccsr13','mm20ccsr14','mm20ccsr19','mm20ccsr30','WM20BCAR02','WM20BCAR06','WM20BCAR12','WM20BCAR01','WM20BCAR03']
aadhararray = [686185381631,578533381676, 823508626405, 783917821528,292531761206,780080049949,885417748021,331693014683,250826071094,632336907426,814114687132,373297720804]
# # regarray = ['WM20BCAR02']
# regarray = ['WM20BCAR06']
# aadhararray = [250826071094]
# regarray = ['WM20BCAR02']
# aadhararray = [331693014683]
options = Options()
options.add_argument('-headless')
cs = []
def scrape(link):
    print("starting...")
    course, semester = get_course_semester(link)
    print(course,semester)
    cs.clear()
    marks_dict = {}
    driver = webdriver.Firefox(options=options)
    for i in range(len(aadhararray)):
        try:
            driver.get(link)
            regno_ = driver.find_element("xpath", '//*[@id="regno"]')
            regno_.send_keys(regarray[i])
            aadhar = driver.find_element("xpath", '//*[@id="aadhaar"]')
            aadhar.send_keys(int(aadhararray[i]))
            driver.find_element("xpath", '//*[@id="cut"]') \
                .click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@style, "left: 14") and contains(@style, "top: 31")]')))
            # wait.until(EC.presence_of_elements_located((By.XPATH, '//span[contains(@style, "left: 16.63%")]')))
            time.sleep(0.1)
            course_spans = driver.find_elements("xpath", '//span[contains(@style, "left: 16.63%")]')
            marks_dict = {}
            for course_span in course_spans:
                course_name = course_span.text
                marks_span = course_span.find_element('xpath', './following-sibling::span[10]')
                try:
                    marks = int(marks_span.text)
                except ValueError:
                    continue
                marks_dict[course_name] = marks
            subjects = list(marks_dict.keys())
            marks = list(marks_dict.values())
            name_ = driver.find_element("xpath", '//span[contains(@style, "left: 14") and contains(@style, "top: 31")]').text
            markp_element = driver.find_element("xpath",'//span[contains(@style, "left: 34.35%") or contains(@style, "left: 36.17%")]')
            if markp_element.text != '-':
                markp = markp_element.text
            else:
                markp = 'Fail'
            print(name_," completed...")
            result = {"regno": regarray[i], "name": name_, "percentage": markp, "marks": dict(zip(subjects, marks))}
            cs.append(result)
        except:
              print(regarray[i]," exception")
    driver.quit()
    try:
        cs.sort(key=lambda x: float(x['percentage'].replace('Fail' or '-', '0')), reverse=True)
    except:
        print('replace exception')

    return cs





# print(scrape('http://www.exam.kannuruniversity.ac.in/UG/bsc2semresult2020_new/result19.php'))

@app.route('/cs')
def get_cs():
    link = request.args.get('link')
    return jsonify(scrape(link))

@app.route('/')
def index():
    print('req')
    return render_template("test.html")

if __name__ == '__main__':
    app.run()