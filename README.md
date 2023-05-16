# sandik
oy ve ötesi sitesi üzerinden sandık verilerini toplamak için script. .exe dosyası olarak dist klasöründe mevcuttur.

orijinal temiz kodu yazan "kiliczsh"a çok teşekkürler, bu bir FORK'tur. Acilen girip verilerin sıradan kullanıcılar tarafından da çekilebilmesi için dist klasöründe scrape_from_city.exe dosyası oluşturulmuştur. Bu dosyayı çalıştırınca sizden plaka kodu ister, girince o ile dair tüm seçim bilgilerini .xlsx (excel), .jpg (resim) ve .json dosyaları olarak çeker. "scrape_from_city-resimli.exe" imzalı belgeleri de çektiğinden daha yavaş çalışmaktadır, ayrıca onu kullanınca bazı kullanıcılarda oyların boş gelmeye başladığını gördük (bot engellemesi olarak düşünüyoruz, ip değiştirince bir süreliğine düzeliyor).

.exe dosyasının çalışabilmesi için cities.json dosyası GEREKLIDIR, yoksa çalışmaz.

# Run Distribution Without Install
```
Click and run "dist/scrape_from_city-resimsiz.exe",
Enter city plate: 69
# 69 is the plate of Bayburt
# Folders with .jpg, .xlsx and .json files get created
```

# Install
```console
git clone https://github.com/kiliczsh/sandik.git
cd sandik
python -m venv .venv
pip install - requirements.txt
```

# Run
```console
# To get city, district, neighborhood and school list

python main.py
Enter city plate: 69
# 69 is the plate of Bayburt
# Check sample/BAYBURT.json for sample output

# To get results of a school

python tutanak.py
python tutanak.py
Enter school id: 184742
# 184742 is the id of the school
# Check sample/school_184742.json for sample output

# To do all above

python scrape_from_city.py
Enter city plate: 69
# 69 is the plate of Bayburt
# Folders with .jpg, .xlsx and .json files get created

```

# Notes
`SLEEP_TIME = 1` in `main.py` and `tutanak.py` is the sleep time between requests. You can change it if you want.


# Contribution
Feel free to contribute ☘️
