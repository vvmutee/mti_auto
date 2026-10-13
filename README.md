# Учёт автомобилей в автопарке

EXE добавил в релиз
Приложение для учета автомобилей в автопарке на PyQt6.

```bash
python -m pip install -r requirements.txt
python main.py
```

## Структура
- `main.py` — запуск программы.
- `models.py` — абстрактный класс Entity, базовый Car и три дочерних класса.
- `collection.py` — Fleet, список автомобилей, поиск, добавление и удаление.
- `widgets.py` — собственные виджеты PyQt6.
- `windows.py` — окно входа, основное окно и форма добавления.
- `report.py` — сеанс пользователя и текстовый отчёт.

```bash
Так же при закрытии главного окна создается report.txt:
+------------------------------------+
| login | time_in | time_out |
|---------|------------|-------------|
|UserName | <datetime> | <datetime> |
+------------------------------------+
```
<img width="847" height="510" alt="Screenshot_3" src="https://github.com/user-attachments/assets/69e10e94-c2f4-495d-b654-e49db0580660" />
<img width="848" height="514" alt="Screenshot_2" src="https://github.com/user-attachments/assets/1ae034a2-33a8-4c62-8210-7363bf4b9df6" />
<img width="314" height="210" alt="Screenshot_1" src="https://github.com/user-attachments/assets/18751f5f-fbd8-489b-a1b5-6ea714eb0dd8" />
