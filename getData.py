import requests
from bs4 import BeautifulSoup
from extractData import extractData 
from PIL import Image
from io import BytesIO



class getData:
  def __init__(self, licenseNo, dob,url):
    self.licenseNo = licenseNo
    self.dob = dob
    self.url = url
    self.session = requests.Session()

  def authentiCate(self, tableList):
    if len(tableList) < 4:
      print("Wrong DOB or License number. Please try again")
      return False
    return True
  
  def get_captcha_image(self):
        response = self.session.get("https://parivahan.gov.in/rcdlstatus/DispplayCaptcha?txtp_cd=1&bkgp_cd=2&noise_cd=2&gimp_cd=3&txtp_length=5&pfdrid_c=true?-928690818&pfdrid_c=true")
        img = Image.open(BytesIO(response.content))
        img.show()  

  def scrapeData(self,captcha_value):
    formData = {
          'javax.faces.partial.ajax': 'true',
          'javax.faces.source': 'form_rcdl:j_idt46',
          'javax.faces.partial.execute': '@all',
          'javax.faces.partial.render': 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
          'form_rcdl:j_idt46': 'form_rcdl:j_idt46',
          'form_rcdl': 'form_rcdl',
          'form_rcdl:tf_dlNO': self.licenseNo,
          'form_rcdl:tf_dob_input': self.dob,
          'form_rcdl:j_idt39:CaptchaID':captcha_value
      }
    session = requests.Session()
    pageData = session.get(self.url)
    soup = BeautifulSoup(pageData.content, features= 'xml')
    viewStateCode = soup.find('input', attrs = {'name': 'javax.faces.ViewState'})['value']
    formData['javax.faces.ViewState'] = viewStateCode 
    response = session.post(self.url, data = formData) 
    responseData = BeautifulSoup(response.text, features='xml')
    tableList = responseData.find_all('table')
    authentication = self.authentiCate(tableList)
    if authentication:  
      try:
        jsonData = extractData(tableList).getJSON()
        return jsonData
      except Exception as error:
        print("Some error occurred while fetching data, please report at yourCompany@Email.com")
        return False
    else:
      return False
