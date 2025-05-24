import os
import shutil
import tempfile
import urllib.request
from tqdm import tqdm

yandex_music_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'YandexMusic', 'resources')
app_asar_path = os.path.join(yandex_music_path, 'app.asar')
backup_path = os.path.join(yandex_music_path, 'app.asar.bak')

download_url = 'https://nextcloud.lukiuwu.xyz/s/fgJyWtrPx8m5L8k/download/app.asar'
backup_restore_url = 'https://nextcloud.lukiuwu.xyz/s/eT6s6sWbJ9FwLYH/download/app.asar.bak'

def download_file(url, dest_path):
    with urllib.request.urlopen(url) as response:
        total_size = int(response.getheader('Content-Length'))
        with open(dest_path, 'wb') as out_file:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Загрузка файла") as pbar:
                while True:
                    chunk = response.read(1024)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    pbar.update(len(chunk))

def create_backup():
    if os.path.exists(app_asar_path):
        if not os.path.exists(backup_path):
            print("📦 Создание бэкапа оригинального app.asar...")
            shutil.copyfile(app_asar_path, backup_path)
        else:
            print("🔎 Бэкап уже существует, пропускаем.")
    else:
        print("❌ Оригинальный app.asar не найден.")

def install_mod():
    print("\n⬇️ Скачивание нового app.asar...")
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            download_file(download_url, temp_file.name)
            print("🛠 Замена файла...")
            shutil.copyfile(temp_file.name, app_asar_path)
            print("✅ Модификация успешно установлена!")
    except Exception as e:
        print(f"❌ Ошибка установки: {e}")

def restore_backup():
    if os.path.exists(backup_path):
        print("\n🛠 Восстановление оригинального файла из локального бэкапа...")
        shutil.copyfile(backup_path, app_asar_path)
        print("✅ Восстановление завершено!")
    else:
        print("\n⬇️ Бэкап локально не найден, скачиваем с сервера...")
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                download_file(backup_restore_url, temp_file.name)
                shutil.copyfile(temp_file.name, app_asar_path)
                print("✅ Восстановление завершено!")
        except Exception as e:
            print(f"❌ Ошибка восстановления: {e}")

def main():
    print("""
🎧 Добро пожаловать в Music Loader Installer!

Доступные действия:
1️⃣ Установить модификацию
2️⃣ Восстановить оригинальный файл
3️⃣ Выход
    """)

    choice = input("👉 Выберите действие (1/2/3): ").strip()

    if choice == '1':
        if not os.path.exists(yandex_music_path):
            print("❌ Приложение Яндекс Музыка не найдено.")
            return
        create_backup()
        install_mod()
    elif choice == '2':
        restore_backup()
    elif choice == '3':
        print("👋 Выход из установщика.")
    else:
        print("❗ Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()