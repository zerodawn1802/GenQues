import requests

pdf_id = "2025_07_29_47d081451627ccc70240g"
headers = {
  "app_key": "17e5ae7263bff41511a104740e7467dd087b6cabc340b58727946cdc69548c00",
  "app_id": "companyname_edmicroeducationcompanylimited_taxcode_0108115077_address_5thfloor_tayhabuilding_no_19tohuustreet_trungvanward_namtuliemdistrict_hanoicity_vietnam_d72a10_14edb5"
}

# get mmd response
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".md"
response = requests.get(url, headers=headers)
with open(pdf_id + ".md", "w", encoding='utf-8') as f:
    f.write(response.text)