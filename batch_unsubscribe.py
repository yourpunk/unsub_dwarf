import subprocess
import time

print("🌪️ SUPER UNSUBSCRIBE MODE ACTIVATED 🌪️")

try:
    repeats = int(input("🔁 Сколько раз запустить отписку подряд? Введи число: "))
    delay = int(input("⏳ Сколько секунд ждать между запусками? Введи число: "))
except ValueError:
    print("❌ Ввод должен быть числом. Попробуй снова.")
    exit(1)

for i in range(repeats):
    print(f"\n🚀 Запуск {i + 1} из {repeats}")
    result = subprocess.run(["python", "unsubscribe.py"])
    
    if result.returncode != 0:
        print(f"⚠️ Ошибка при запуске unsubscribe.py на итерации {i + 1}")
        break

    if i < repeats - 1:
        print(f"🕒 Ожидаем {delay} секунд до следующего запуска...")
        time.sleep(delay)

print("\n🏁 SUPER UNSUBSCRIBE завершён. Все циклы отработаны.")
