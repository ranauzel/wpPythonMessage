import yaml

# YAML dosyasını okuyan fonksiyon
def load_settings():
    try:
        with open("config.yaml", "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"YAML dosyasını okurken hata oluştu: {e}")
        return {"ayarlar": {"sicaklik_esik": "0", "phone_numbers": []}}

# Admin paneli ayarlarını işleyen fonksiyon
def admin_panel_logic(request):
    if request.method == "POST":
        sicaklik_esik = request.form.get('sicaklik_esik')
        phone_numbers = request.form.getlist('phone_numbers')

        save_settings(sicaklik_esik, phone_numbers)

    # Ayarları döndür
    return load_settings()

# YAML dosyasını güncelleyen fonksiyon
def save_settings(sicaklik_esik, phone_numbers):
    with open("config.yaml", "w") as file:
        yaml.dump({"ayarlar": {"sicaklik_esik": sicaklik_esik, "phone_numbers": phone_numbers}}, file)
