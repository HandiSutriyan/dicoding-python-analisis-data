# Dashbor Data Kualitas Udara Tiongkok 🇨🇳 🏭
Dasbor menampilkan data kulaitas udara pada 12 stasiun pengamatan di Tiongkok pada tahun 2103-2017. Stasiun pengamatan yang terdapat pada dataset yaitu:
1. Aotizhongxin = AZN
2. Changping = CGP
3. Dingling = DLG
4. Dongsi = DNS
5. Guangyuan = GNY
6. Gucheng = GCG
7. Huairo = HRO
8. Nongzhanguan = NZG
9. Shunyi = SHY
10. Tiantan = TNT
11. Wanliu = WNL
12. Wangshouxigong = WSX

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```

## Dashboard Interaktif
Anda juga dapat mengakses dashboard interaktif dataset ini pada tautan:
https://dashborad-aq-tiongkok.streamlit.app/
