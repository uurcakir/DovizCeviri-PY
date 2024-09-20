from cx_Freeze import setup, Executable
import sys
import os

# Simge dosyanızın yolunu burada belirtin (örneğin, 'icon.ico')
icon_path = "C:/Users/ugrca\PycharmProjects\ExchangeConverter\icon.ico"

# build_exe seçenekleri
build_exe_options = {
    "packages": ["tkinter", "sv_ttk", "requests"],  # Kullandığınız paketler
    "include_files": ["api.py", "currencies.py"],  # Ek dosyalar varsa buraya ekleyin
}

# base ayarı (GUI uygulaması için)
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Konsolsuz bir GUI uygulaması için

# Uygulama için Executable ayarları
executables = [
    Executable(
        script="main.py",  # Ana Python dosyanızın ismi
        base=base,
        icon=icon_path,  # Simge dosyasının yolunu burada belirtin
    )
]

# Setup ayarı
setup(
    name="Döviz Hesaplayıcı",
    version="1.0",
    description="Bir döviz hesaplayıcı uygulaması",
    options={"build_exe": build_exe_options},
    executables=executables,
)
