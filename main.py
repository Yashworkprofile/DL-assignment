from getData import getData

url = "https://parivahan.gov.in/rcdlstatus/?pur_cd=101"

dl_number = input("Enter Driving License Number: ")
dob = input("Enter Date of Birth (DD-MM-YYYY): ")

if not (len(dob) == 10 and dob.count('-') == 2):
    print("Wrong DOB, please write again in dd-mm-yyyy format")
else:
    
    data_fetcher = getData(licenseNo=dl_number, dob=dob, url=url)

   
    captcha_value=data_fetcher.get_captcha_image()

   
    scraped_data = data_fetcher.scrapeData(captcha_value)

    if scraped_data:
        print(scraped_data)
