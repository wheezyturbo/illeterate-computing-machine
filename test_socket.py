from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, jsonify,render_template,request
import bca
import bsccs
import re

def get_course_semester(url):
    # Extract the course and semester information from the URL using regex
    match = re.search(r'/(\w+\d+)semresult', url)
    if match:
        course_semester = match.group(1)
        course = re.search(r'^\D+', course_semester).group()
        semester = int(re.search(r'\d+$', course_semester).group())
        print(semester)
        return (course, semester)
    else:
        return None

# from flask_ngrok import run_with_ngrok

app = Flask(__name__)
# run_with_ngrok(app) 

regarray = ['mm20ccsr22','mm20ccsr18', 'mm20ccsr16', 'mm20ccsr13','mm20ccsr14','mm20ccsr19','mm20ccsr30','WM20BCAR02','WM20BCAR06','WM20BCAR12','WM20BCAR01','WM20BCAR03']
aadhararray = [686185381631,578533381676, 823508626405, 783917821528,292531761206,780080049949,885417748021,331693014683,250826071094,632336907426,814114687132,373297720804]
# regarray = ['WM20BCAR02']
# aadhararray = [331693014683]


# Set Firefox options to run in headless mode
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
            course_names = []
            if 'ccsr' in regarray[i].lower():
                course_names = bsccs.course_names(semester)
            elif 'bcar' in regarray[i].lower():
                course_names = bca.course_names(semester)
            regno_ = driver.find_element("xpath", '//*[@id="regno"]')
            regno_.send_keys(regarray[i])
            aadhar = driver.find_element("xpath", '//*[@id="aadhaar"]')
            aadhar.send_keys(int(aadhararray[i]))
            driver.find_element("xpath", '//*[@id="cut"]') \
                .click()

            wait = WebDriverWait(driver, 5)
            wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@style, "left: 14") and contains(@style, "top: 31")]')))

            try:
                course_spans = driver.find_elements(By.TAG_NAME,"span")
                marks_dict = {}
                for course_name in course_names:
                    for span in course_spans:
                        if course_name in span.text:
                            marks = span.find_element('xpath',"./following-sibling::span[10]").text
                            marks_dict[course_name] = marks
                            break

                print(marks_dict)
            except Exception as e:
                print(e)

            name_ = driver.find_element("xpath", '//span[contains(@style, "left: 14") and contains(@style, "top: 31")]').text
            markp_element = driver.find_element("xpath", '//span[contains(@style, "left: 34.35%") or contains(@style, "left: 36.17%")]')
            if markp_element.text != '-':
                markp = markp_element.text
            else:
                markp = 'Fail'

            print(name_, " completed...")

            result = {"regno": regarray[i], "name": name_, "percentage": markp, "marks": marks_dict}
            cs.append(result)
        except:
            print(regarray[i], 'exception')

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
    app.run(debug=True)