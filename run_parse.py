import pandas
import os
import re

import glob

from bs4 import BeautifulSoup

if not os.path.exists("parsed_files"):
  os.mkdir("parsed_files")

dataset = pandas.DataFrame()  


for file_name in glob.glob("html_files/*.html"):
  # file_name = "html_files/20230928114413.html"

  file = open(file_name, "r")
  soup = BeautifulSoup(file.read(), 'html.parser')
  file.close()

  meta = soup.find("meta", {"name": "Description" })
  meta_content = meta["content"]
  gas = meta_content.split("-")[1].split("|")
  low_gas = gas[0].split(" ")[2] 
  avg_gas = gas[1].split(" ")[2]
  high_gas = gas[2].split(" ")[2]
  print(low_gas)
  print(avg_gas)
  print(high_gas)

  tbody = soup.find("tbody", {"class": "align-middle text-nowrap"})

  tr_list = tbody.find_all("tr")

  wallet_list = []
  gas_value_usd_list = []
  gas_value_eth_list = []

  for tr in tr_list[0:3]:
    a_list = tr.find_all("a", {"data-bs-toggle-gg": "tooltip"})
    wallet_list.append(a_list[0].text)
    td_list = tr.find_all("td")
    gas_value_usd_list.append(td_list[2].text.split(" ")[0].replace("$","").replace(",",""))
    gas_value_eth_list.append(td_list[2].text.split(" ")[1].replace("(",""))

  print(wallet_list)
  print(gas_value_usd_list)
  print(gas_value_eth_list)
    
  scrape_time = file_name.split("/")[1].replace(".html", "")
  scrape_time_year = scrape_time[0:4]
  scrape_time_month = scrape_time[5:6]
  scrape_time_day = scrape_time[7:8]

  dataset = pandas.concat([dataset,
    pandas.DataFrame.from_records([{
      "scrape_time": scrape_time,
      "scrape_time_year": scrape_time_year,
      "scrape_time_month": scrape_time_month,
      "scrape_time_day": scrape_time_day,
      "low_gas": low_gas,
      "avg_gas": avg_gas,
      "high_gas": high_gas,
      "first_wallet": wallet_list[0],
      "first_gas_value_usd": gas_value_usd_list[0],
      "first_gas_value_eth": gas_value_eth_list[0],
      "sec_wallet": wallet_list[1],
      "sec_gas_value_usd": gas_value_usd_list[1],
      "sec_gas_value_eth": gas_value_eth_list[1],
      "third_wallet": wallet_list[2],
      "third_gas_value_usd": gas_value_usd_list[2],
      "third_gas_value_eth": gas_value_eth_list[2]
      }])
    ])

dataset.to_csv("parsed_files/dataset.csv", index=False)


  
  


