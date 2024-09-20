from tkinter import messagebox
import requests
import tkinter.messagebox
from tkinter import ttk
import sv_ttk


def set_theme(root):
    sv_ttk.set_theme("dark")  # "light" veya "dark" olarak değiştirebilirsiniz

    # Varsayılan ttk stil ayarları
    style = ttk.Style(root)
    style.configure("TLabel", foreground="white", background="#2e2e2e", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 11), padding=6)
    style.configure("TCombobox", font=("Arial", 11))
    style.configure("TEntry", font=("Arial", 11))


def get_exchange_rate(base_currency, target_currency):
    # Döviz kuru API'si için URL ve anahtar (ExchangeRate-API kullanabilirsiniz)
    api_key = 'YOUR_API_KEY'  # Buraya kendi API anahtarınızı girin
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"

    try:
        response = requests.get(url)

        # Yanıtın durum kodunu kontrol edelim
        if response.status_code != 200:
            messagebox.showerror("HATA", f"API isteği başarısız oldu. Durum kodu: {response.status_code}")
            return None

        # Yanıtın boş olup olmadığını kontrol et
        if not response.text:
            messagebox.showerror("HATA", "API'den boş bir yanıt alındı.")
            return None

        # Yanıtın JSON formatında olup olmadığını kontrol et
        try:
            data = response.json()
        except ValueError:
            messagebox.showerror("HATA", "Yanıt JSON formatında değil.")
            return None

        # Döviz kuru verilerini alalım
        exchange_rate = data.get('conversion_rates', {}).get(target_currency)
        if exchange_rate:
            return exchange_rate
        else:
            messagebox.showerror("HATA", f"'{target_currency}' geçerli bir hedef para birimi değil.")
            return None

    except requests.RequestException as e:
        # İstek sırasında bir hata olursa bu bloğa düşecek
        messagebox.showerror("HATA", f"API isteği sırasında bir hata oluştu: {str(e)}")
        return None


def convert_currency(amount, base_currency, target_currency):
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    if exchange_rate:
        converted_amount = amount * exchange_rate
        messagebox.showinfo("Sonuç", f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
        return converted_amount
    else:
        messagebox.showerror("HATA", "Döviz çevirme işlemi başarısız oldu.")
        return None
