## Renjuu
Японская игра, в которой необходимо поставить пять камней в ряд.

#### Установка:
```bash
git clone https://github.com/Ferocius-Gosling/renjuu.git
# установка зависимостей
pip install -r requirements.txt 
```

#### Для запуска:
```
python main.py
```
Запустится меню игры, где необходимо выбрать цвет камней, которыми вы будете играть.
 

### API 

Приложение работает на основе библиотеки pygame. Игра происходит в окне pygame.
Можно выбрать цвет игрока. Первыми ходят чёрные. Игра происходит против бота, который
ставит камни в случайные клетки. Для победы необходимо поставить пять камней своего цвета
в ряд.