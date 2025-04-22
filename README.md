# Danışman Eczacım

SUT kurallarına göre reçete değerlendirmesi yapan eczane danışma programı.

## Özellikler

- Reçete yükleme ve değerlendirme
- SUT.pdf'den ilaç uygunluğu kontrolü
- İlaç raporlarının kontrolü
- Atorvastatin grubu ilaçlar için LDL değeri kontrolü
- Entekavir ve benzeri ilaçlar için SUT kontrolü
- İlaç uygunluğunu ✔, ✘ veya ❓ ile gösterme

## Kurulum

### Gereksinimler

- Python 3.8+
- PostgreSQL

### Adımlar

1. Projeyi klonlayın:

```bash
git clone https://github.com/yourusername/danisman_eczacim.git
cd danisman_eczacim
```

2. Sanal ortam oluşturun ve bağımlılıkları yükleyin:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

3. PostgreSQL veritabanı oluşturun:

```sql
CREATE DATABASE danisman_eczacim;
```

4. `.env` dosyasını düzenleyin:

```
DATABASE_URL=postgresql://yourusername:yourpassword@localhost:5432/danisman_eczacim
DEBUG=True
SECRET_KEY=your_secret_key_here
APP_NAME=Danışman Eczacım
API_PREFIX=/api/v1
```

5. Veritabanı tablolarını oluşturun:

```bash
python -m app.db.init_db
```

6. Uygulamayı çalıştırın:

```bash
python -m app.main
```

7. Tarayıcınızda `http://localhost:8000` adresine gidin.

## Kullanım

1. Ana sayfadaki formu kullanarak reçete bilgilerini girin.
2. İlaçları ekleyin ve gerekli durumlarda "Rapor Gerekli" ve "Rapor Uygun" kutularını işaretleyin.
3. Reçete dosyasını yükleyin (PDF, JPG veya PNG formatında).
4. "Reçeteyi Değerlendir" butonuna tıklayın.
5. Değerlendirme sonuçlarını görüntüleyin.

## Lisans

MIT 