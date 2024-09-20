# coding:utf-8

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import currencies
import api
import sv_ttk

# Global değişkenler
global tgt  # Hedef döviz
global bse  # Ana döviz


# Modern tema ve stil
def set_theme(root):
    sv_ttk.set_theme("dark")  # "light" veya "dark" olarak değiştirebilirsiniz

    # Varsayılan ttk stil ayarları
    style = ttk.Style(root)
    style.configure("TLabel", foreground="white", background="#2e2e2e", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 11), padding=6)
    style.configure("TCombobox", font=("Arial", 11))
    style.configure("TEntry", font=("Arial", 11))


# Pencere oluşturma
root = tk.Tk()
root.title("Döviz Hesaplayıcı")
root.geometry("400x300")  # Pencere boyutları
root.resizable(False, False)


# Temayı yükleme
set_theme(root)

# Ana çerçeve (Frame) oluşturma
main_frame = ttk.Frame(root, padding="20 20 20 20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Etiket oluşturma
title_label = ttk.Label(main_frame, text="Döviz Hesaplayıcı", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# ComboBox (Açılır Liste) oluşturma - Ana Para Birimi
base_currencies = currencies.currency_list

base_label = ttk.Label(main_frame, text="Ana Döviz Kodu:")
base_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

base_combo = ttk.Combobox(main_frame, values=base_currencies, state="readonly")
base_combo.set("Ana Döviz Kodu Seçin")
base_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

# ComboBox (Açılır Liste) oluşturma - Hedef Para Birimi
target_label = ttk.Label(main_frame, text="Hedef Döviz Kodu:")
target_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

target_currencies = currencies.currency_list
target_combo = ttk.Combobox(main_frame, values=target_currencies, state="readonly")
target_combo.set("Hedef Döviz Kodu Seçin")
target_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

# Tutar Etiketi
amount_label = ttk.Label(main_frame, text="Tutar Girin:")
amount_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)


# Sayı girişi (Entry widget)
def validate_numeric_input(input):
    return input == "" or input.replace(".", "", 1).isdigit()


vcmd = (root.register(validate_numeric_input), '%P')
amount = ttk.Entry(main_frame, validate="key", validatecommand=vcmd)
amount.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)


# Seçilen değeri alma fonksiyonları
def get_selected_base():
    global bse
    selected_base_currency = base_combo.get()
    if not selected_base_currency:
        return messagebox.showwarning("Uyarı", "Lütfen geçerli bir döviz seçin!")
    bse = selected_base_currency[:3].upper()
    return bse


def get_selected_target():
    global tgt
    selected_target_currency = target_combo.get()
    if not selected_target_currency:
        return messagebox.showwarning("Uyarı", "Lütfen geçerli bir döviz seçin!")
    tgt = selected_target_currency[:3].upper()
    return tgt


# Kurları değiştiren fonksiyon
def swap_currencies():
    base = base_combo.get()
    target = target_combo.get()
    base_combo.set(target)
    target_combo.set(base)


# Kontrol fonksiyonu
def control():
    value = amount.get()
    try:
        money = float(value)
    except ValueError:
        return messagebox.showwarning("UYARI", "Lütfen geçerli bir sayı girin!")

    if get_selected_base() == get_selected_target():
        messagebox.showwarning("UYARI", "Seçtiğiniz Döviz Kodları Aynı Olmamalıdır!")
    elif money <= 0:
        messagebox.showwarning("UYARI", "Tutar Sıfırdan Büyük Olmalıdır!")
    else:
        api.convert_currency(money, bse, tgt)


# Düğmeleri oluşturma
swap_button = ttk.Button(main_frame, text="Değiştir", command=swap_currencies)
swap_button.grid(row=4, column=0, pady=10)

calculate_button = ttk.Button(main_frame, text="Hesapla", command=control)
calculate_button.grid(row=4, column=1, pady=10)

# Ana döngüyü başlat
root.mainloop()
