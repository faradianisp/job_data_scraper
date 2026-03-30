import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_jobstreet():
    url = "https://id.jobstreet.com/id/Data-Analyst-jobs/remote"
    
    # Header sangat penting agar permintaan kita tidak diblokir (seolah-olah dari browser)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []

        # Looking for main container (selector ini bisa berubah sewaktu-waktu)
        job_cards = soup.find_all('article')

        for card in job_cards:
            title = card.find('h3').get_text(strip=True) if card.find('h3') else "N/A"
            
            company_tag = card.find('a', {'data-automation': 'jobCompany'})
            company = company_tag.get_text(strip=True) if company_tag else "N/A"
            
            location_tag = card.find('a', {'data-automation': 'jobLocation'})
            
            if not location_tag:
                spans = card.find_all('span')
                location = "N/A"
                for s in spans:
                    txt = s.get_text(strip=True)
                    if any(loc in txt for loc in ["Remote", "Jakarta", "Indonesia", "Jawa"]):
                        location = txt
                        break
            else:
                location = location_tag.get_text(strip=True)

            salary_tag = card.find('span', {'data-automation': 'jobSalary'})
            salary = salary_tag.get_text(strip=True) if salary_tag else "Gaji tidak dicantumkan"

            jobs.append({
                "Job Title": title,
                "Company": company,
                "Location": location,
                "Salary": salary
            })

        return pd.DataFrame(jobs)
    else:
        print(f"Gagal mengakses halaman. Status code: {response.status_code}")
        return None

#simpan ke CSV
df_jobs = scrape_jobstreet()
if df_jobs is not None:
    print(df_jobs.head())
    df_jobs.to_csv("lowongan_remote.csv", index=False, encoding='utf-8-sig')
    print("\nData berhasil disimpan ke lowongan_remote.csv")