from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, jsonify,render_template,request

app = Flask(__name__)


regarray = ['mm20ccsr22','mm20ccsr18', 'mm20ccsr16', 'mm20ccsr13','mm20ccsr14','mm20ccsr19','mm20ccsr30','WM20BCAR02','WM20BCAR06','WM20BCAR12','WM20BCAR01','WM20BCAR03']
aadhararray = [686185381631,578533381676, 823508626405, 783917821528,292531761206,780080049949,885417748021,331693014683,250826071094,632336907426,814114687132,373297720804]
# regarray = ['WM20BCAR02']
# aadhararray = [331693014683]


# Set Firefox options to run in headless mode
options = Options()
options.headless = True

cs = []

def scrape(link):
      cs.clear()
      driver = webdriver.Firefox(options = options)
      for i in range(len(aadhararray)):
      # Create Firefox instance with headless option
            # driver.get('http://www.exam.kannuruniversity.ac.in/UG/bsc5semresult2021/result19.php')
            # driver.get('http://www.exam.kannuruniversity.ac.in/UG/bsc4semresult2022_new/result19.php')
            driver.get(link)

            regno_ = driver.find_element("xpath", '//*[@id="regno"]')
            regno_.send_keys(regarray[i])

            aadhar = driver.find_element("xpath", '//*[@id="aadhaar"]')
            aadhar.send_keys(int(aadhararray[i]))
            
            driver.find_element("xpath",'//*[@id="cut"]')\
                  .click()
            
            # Wait for the result page to load
            wait = WebDriverWait(driver, 10)  # maximum wait time of 10 seconds
            wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@style, "left: 14") and contains(@style, "top: 31")]')))
            
            name_ = driver.find_element("xpath", '//span[contains(@style, "left: 14") and contains(@style, "top: 31")]').text
            # markp = driver.find_element("xpath",'//span[contains(@style, "left: 34.35%; top: 55.86%")]').text
            


            #scraping the percentage
            # markp = driver.find_element("xpath",'//span[contains(@style, "left: 34.35%")]').text
            markp_element = driver.find_element("xpath",'//span[contains(@style, "left: 34.35%") or contains(@style, "left: 36.17%")]')
            if markp_element.text != '-':
                  markp = markp_element.text
            else:
                  markp = 'Fail'


            
            print(name_," completed...")

            # scraping marks
            # mark_elements = driver.find_elements("xpath", '//span[contains(@style, "left: 71.38%")]')
            # marks = [mark_element.text for mark_element in mark_elements]
            mark_elements = driver.find_elements("xpath", '//span[contains(@style, "left: 71.38%")]')
            marks = []
            for mark_element in mark_elements:
                  if mark_element.text != '-':
                        marks.append(mark_element.text)
                  else:
                        marks.append('Fail')

            subject_elements = driver.find_elements("xpath", '//span[contains(@style, "left: 16.63%")]')
            subjects = [subject_element.text for subject_element in subject_elements]


            mark_dict = {}
            for j in range(len(subjects)):
                  try:
                        mark_dict[subjects[j]] = marks[j]
                  except:
                        mark_dict[subjects[j]] = '0'


            result = {"regno": regarray[i], "name": name_, "percentage": markp, "marks": mark_dict}
            #     print(result)
            cs.append(result)


      driver.quit()
      cs.sort(key=lambda x: float(x['percentage'].replace('Fail', '0')), reverse=True)

      return cs

print(cs)
@app.route('/cs')
def get_cs():
    link = request.args.get('link')
    return jsonify(scrape(link))

@app.route('/')
def index():
    
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True)