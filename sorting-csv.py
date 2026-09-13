import requests

url = "https://data.wa.gov/api/views/g472-n5ph/rows.csv?accessType=DOWNLOAD"
response = requests.get(url)
#print(response.status_code)

data = response.text
#print(data[:500])

import csv
lines = data.splitlines()
reader = csv.reader(lines)

results = []
count = 0

for row in reader:
    cost_str = row[1]
    if cost_str == "Cost of Contract" or cost_str == "":
        continue
    cost = float(row[1])
    results.append((row[0].strip(), cost))
    count += 1
   # if count >= 10:
       # break
       
totals = {}
for name, cost in results:
    clean_name = name.upper().replace("/"," ").replace("-"," ").replace(","," ").replace("  "," ")
    if clean_name in totals:
        totals[clean_name] = totals[clean_name] + cost
    else:
        totals[clean_name] = cost
        
consulting_firms = []

for name, cost in totals.items():
    if "CONSULT" in name:
        consulting_firms.append((name, cost))


        
sorted_results = sorted(totals.items(), key=lambda pair: pair[1], reverse=True )

for name, cost in sorted_results[:20]:
    print(f"{name:.<40}{'-' if cost < 0 else ''}${abs(cost):,.2f}")

total = 0
for name, cost in sorted_results[:20]:
    total = total + cost
print('\n' f"{'TOTAL':.<40}${total:,.2f}")
    

    
print("\n\n\n")
    
sorted_consulting = sorted(consulting_firms, key=lambda pair: pair[1], reverse=True )

print(len(consulting_firms))
for name, cost in sorted_consulting[:20]:
    print(f"{name:.<40}{'-' if cost < 0 else ''}${abs(cost):,.2f}")
    
total = 0
for name, cost in consulting_firms:
    total = total + cost
print('\n' f"{'TOTAL':.<40}${total:,.2f}")

total = 0
for name, cost in results:
    total = total + cost
print('\n' f"{'TOTAL':.<40}${total:,.2f}")
