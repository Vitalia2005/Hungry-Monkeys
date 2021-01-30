import datetime
import pygame, sys, sqlite3, time, os, pygame_gui
import random as rd
from load_image import load_image

FPS = 70
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 450


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('фон.jpg'), WINDOW_SIZE)
    screen.blit(fon, (0, 0))
    font_name = pygame.font.match_font('Icegirl Regular', bold=True)

    # это текст, который мы выведем на приветственный экран
    intro_text = ["              Hungry Monkeys",
                  '', '', '', '', '', '',
                  '                                       УСПЕЙ НАКОРМИТЬ ВСЕХ ОБЕЗЬЯН',
                  '                       КЛИКНИ МЫШКОЙ, ЧТОБЫ НАЧАТЬ']
    text_coord = 160
    for i, line in enumerate(intro_text):
        if i == 0:
            font = pygame.font.Font(font_name, 60)
            string_rendered = font.render(line, 1, pygame.Color('#06590b'))
        elif i == len(intro_text) - 1:
            font_name = pygame.font.match_font("Icegirl Regular", bold=True)
            font = pygame.font.Font(font_name, 30)
            string_rendered = font.render(line, 1, pygame.Color('#0F8010'))
        else:
            font_name = pygame.font.match_font("Icegirl Regular", bold=True)
            font = pygame.font.Font(font_name, 22)
            string_rendered = font.render(line, 1, pygame.Color('#0F8010'))

        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    # вставляем картинки обезьянок
    fon = pygame.transform.scale(load_image('fon1.png'), (97, 133))
    screen.blit(fon, (350, 250))
    fon = pygame.transform.scale(load_image('fon2.png'), (80, 50))
    screen.blit(fon, (20, -2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def print_text(screen, text):
    # печатаем результат
    font_name = pygame.font.match_font('Icegirl Regular', bold=True)
    font = pygame.font.Font(font_name, 35)
    for i in range(len(text)):
        string_rendered = font.render(text[i], 1, pygame.Color('#06590b'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 80 + i * 40
        intro_rect.x = 220
        screen.blit(string_rendered, intro_rect)
    f = open("data/score.txt", mode="r")
    text = f'   Ваш рекорд: {f.readline()[:-1:]}'
    f.close()
    string_rendered = font.render(text, 1, pygame.Color('#06590b'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 390
    intro_rect.x = 280
    screen.blit(string_rendered, intro_rect)

    f = open("data/dates.txt", mode="r")
    intro_text = [el.rstrip() for el in f.readlines()]
    f.close()
    text_coord = 250
    font_name = pygame.font.match_font("Icegirl Regular", bold=True)
    font = pygame.font.Font(font_name, 30)

    for i, line in enumerate(intro_text):
        string_rendered = font.render(line, 1, pygame.Color('#06590b'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 220
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


class SpriteMonkey(pygame.sprite.Sprite):
    def __init__(self, image, x, y, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)


def end_screen(screen, score):  # окно после конца игры, проигрыша
    fon = pygame.transform.scale(load_image('фон.jpg'), WINDOW_SIZE)
    screen.blit(fon, (0, 0))
    m = False
    sprites = pygame.sprite.Group()

    # скроем системный курсор
    pygame.mouse.set_visible(False)
    # создадим спрайт своего курсора (банана)
    cursor_sprite = pygame.sprite.Sprite()
    cursor_sprite.image = load_image("banana_cursor.png")
    cursor_sprite.rect = cursor_sprite.image.get_rect()
    cursor_sprite.mask = pygame.mask.from_surface(cursor_sprite.image)  # маска курсора-банана
    sprites.add(cursor_sprite)
    x, y = pygame.mouse.get_pos()

    manager = pygame_gui.UIManager(WINDOW_SIZE)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)
    switch = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((270, 180), (250, 50)),
        text='Сыграть еще раз',
        manager=manager)

    print_score(score, screen)
    if score < 100:
        s = pygame.mixer.Sound('data/game_over.mp3')  # загружаем звук проигрыша
        text = ['         Вы проиграли,', 'набрав меньше 100 очков!']
    else:
        s = pygame.mixer.Sound('data/game_win.mp3')  # загружаем звук выигрыша
        text = ['         Вы выиграли,', 'набрав больше 100 очков!']

    img = pygame.transform.scale(load_image('fon1.png'), (97, 133))
    m = SpriteMonkey(img, 120, 250, sprites)

    s.set_volume(0.2)  # звук проигрыша или выигрыша
    s.play()

    sound1 = pygame.mixer.Sound('data/обезьяны.mp3')
    sound1.set_volume(0.15)

    run = True
    while run:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == switch:
                        m = True
                        run = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.collide_mask(m, cursor_sprite):
                    sound1.play()
            manager.process_events(event)
        cursor_sprite.rect.x = x - 25
        cursor_sprite.rect.y = y - 25
        manager.update(time_delta)
        screen.blit(fon, (0, 0))
        manager.draw_ui(screen)
        sprites.draw(screen)
        sprites.update()
        print_text(screen, text)
        pygame.display.update()
        pygame.display.flip()
    if m:
        main()
    else:
        pygame.display.quit()  # закрываем игру


def minus_point(t):
    global fail, banana_sprites, pol, left_tree, top, right_tree, palma
    if t == 'pol':
        pol = False
    elif t == 'left_tree':
        left_tree = False
    elif t == 'top':
        top = False
    elif t == 'right_tree':
        right_tree = False
    elif t == 'palma':
        palma = False
    fail -= 1
    if len(banana_sprites) > 0:
        banana_sprites.sprites()[0].kill()


def print_score(score, screen):
    #  Функция отображения счёта очков
    font_name = pygame.font.match_font('Icegirl Regular',
                                       bold=True)
    font = pygame.font.Font(font_name, 60)
    string_rendered = font.render(str(score), 1,
                                  pygame.Color('#06590b'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 20
    intro_rect.x = 380
    screen.blit(string_rendered, intro_rect)


# функция создания обезьяны
def generation_monkey(cur, all_sprites, monkeys):
    global pol, left_tree, top, right_tree, palma
    d = {1: pol, 2: left_tree, 3: right_tree, 4: palma, 5: top}
    if False not in [pol, left_tree, right_tree, palma, top]:
        return
    while True:
        a = rd.randint(1, 5)
        if not d[a]:
            break
    if a == 1:
        # если на полу еще нет обезьяны
        if not pol:
            k = rd.choice(['1-pol1', '2-pol2', '1-pol2', '2-pol1'])
            p = cur.execute("""SELECT list FROM names
                    WHERE which=?""", (k,)).fetchall()[0][0].split(',')
            if k == '1-pol2' or k == '2-pol2':
                m = Monkey(p, 100, 300, all_sprites, 'pol', run=True)
            else:
                m = Monkey(p, rd.randint(100, 450), 300, all_sprites, 'pol')
            pol = True
            all_sprites.add(m)
            monkeys.add(m)

    if a == 2:
        # если слева еще нет обезьяны
        if not left_tree:
            k = rd.choice(['1-left_tree', '2-left_tree'])
            p = cur.execute("""SELECT list FROM names
                    WHERE which=?""", (k,)).fetchall()[0][0].split(',')
            m = Monkey(p, rd.randint(0, 30), 0, all_sprites, 'left_tree')
            left_tree = True
            all_sprites.add(m)
            monkeys.add(m)

    if a == 3:
        # если наверху еще нет обезьяны
        if not top:
            k = rd.choice(['1-top', '2-top'])
            p = cur.execute("""SELECT list FROM names
                    WHERE which=?""", (k,)).fetchall()[0][0].split(',')[::-1]
            m = Monkey(p, rd.randint(400, 450), 12, all_sprites, 'top')
            top = True
            all_sprites.add(m)
            monkeys.add(m)

    if a == 4:
        # если справа еще нет обезьяны
        if not right_tree:
            k = rd.choice(['1-right_tree', '2-right_tree'])
            p = cur.execute("""SELECT list FROM names
                    WHERE which=?""", (k,)).fetchall()[0][0].split(',')[::-1]
            m = Monkey(p, 0, 400, all_sprites, 'right_tree')
            right_tree = True
            all_sprites.add(m)
            monkeys.add(m)

    if a == 5:
        # если за пальмой еще нет обезьяны
        if not palma:
            k = '1-palma'
            p = cur.execute("""SELECT list FROM names
                    WHERE which=?""", (k,)).fetchall()[0][0].split(',')[::-1]
            m = Monkey(p, 640, 295, all_sprites, 'palma')
            palma = True
            all_sprites.add(m)
            monkeys.add(m)


class BananaPoints(pygame.sprite.Sprite):
    # спрайт бананов-попыток (правый верхний угол)
    def __init__(self, i, *group):
        super().__init__(*group)
        im = load_image('b1.png')
        self.image = im
        self.rect = im.get_rect()
        self.rect.x = 590 + i * 40
        self.rect.y = 10


class Monkey(pygame.sprite.Sprite):
    def __init__(self, images, x, y, all_sprites, type, run=False):
        # images - список изображений анимированного спрайта
        # columns, rows - число столбцов и строк соответственно
        # x, y - координаты изображения
        # all_sprites - список всех спрайтов
        # run - этот необязательный параметр отвечает за бег. По умолчанию False

        super().__init__(all_sprites)
        self.type_name = type
        self.run = run
        self.images = images

        if type != 'left_tree' and type != 'right_tree' and type != 'palma':
            # выбираем случайный размер
            koeff = rd.choice([0.5, 0.55, 0.6, 0.65,
                               0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1])
        elif type == 'palma':
            koeff = 0.8

        else:
            # для определенных обезьян выбрать случайный размер нельзя
            # потому что нарушатся пропорции
            koeff = 1

        for i in range(len(self.images)):  # загружаем избражения
            img = load_image(self.images[i])
            image1 = pygame.transform.scale(img,
                                            (int(img.get_width() * koeff),
                                             int(img.get_height() * koeff)))
            self.images[i] = image1

        # определяем размер изображения
        if len(self.images) >= 4:
            self.rect = pygame.Rect(0, 0, self.images[3].get_width(),
                                    self.images[3].get_height())

        else:
            self.rect = pygame.Rect(0, 0, self.images[0].get_width(),
                                    self.images[0].get_height())
        self.rect = self.rect.move(x, y)  # размещаем изображение
        self.counter = 0  # это счетчик для корректировки скорости
        self.cur_frame = 0
        self.image = self.images[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.start_time = time.time()

    def update(self):
        global running, fail, end
        if self.counter < 7:  # регулировка скорости
            self.counter += 1

        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.images)
            self.image = self.images[self.cur_frame]
            self.counter = 0

        if self.run:  # если обезьяна бегущая
            if self.rect.x + 2 <= 540:  # реализация бега
                self.rect.x = self.rect.x + 2

            else:
                # если обезьяна добежала - удаляем ее и отнимаем попытку
                minus_point(self.type_name)
                self.kill()
                if fail <= 0:  # если попыток осталось 0 - завершаем игру
                    running = False
                    end = True
        else:
            # если прошло 3 секунды после появления обезьяны - удаляем ее и отнимаем попытку
            if time.time() - self.start_time >= 3:
                minus_point(self.type_name)
                self.kill()

                if fail <= 0:  # если попыток осталось 0 - завершаем игру
                    running = False
                    end = True


def main():
    global pol, fail, banana_sprites, left_tree, top, right_tree, palma, running, end
    pol, top, left_tree, right_tree, palma = False, False, False, False, False

    # фоновая музыка
    fullname = os.path.join('data', 'music.mp3')
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)

    end = False
    fail = 5  # количество допустимых пропусков обезьян
    pygame.display.set_caption('Hungry Monkeys')  # Изменяем заголовок окна
    # подключаемся к базе данных
    con = sqlite3.connect("data/images.db")
    cur = con.cursor()
    clock = pygame.time.Clock()  # Счётчик времени

    MYEVENTTYPE = pygame.USEREVENT + 1  # создаем свое событие - появление новых обезьян
    # время, через которе они появятся, выбирается случайно
    pygame.time.set_timer(MYEVENTTYPE, rd.choice([2000, 3000]))

    # Настраиваем внешний вид окна
    fon = pygame.transform.scale(load_image('фон.jpg'), WINDOW_SIZE)
    screen.blit(fon, (0, 0))

    score = 0  # Счётчик очков
    print_score(score, screen)  # Пишем счёт на экран

    all_sprites = pygame.sprite.Group()  # Группа всех спрайтов
    monkeys = pygame.sprite.Group()  # Группа спрайтов обезьян
    banana_sprites = pygame.sprite.Group()  # Группа спрайтов бананов-попыток

    for i in range(5):  # создаем 5 дананов-попыток (правый верхний угол)
        BananaPoints(i, all_sprites, banana_sprites)

    for _ in range(rd.randint(1, 5)):  # создаем случайное количество обезьян (от 1 до 5)
        generation_monkey(cur, all_sprites, monkeys)

    # скроем системный курсор
    pygame.mouse.set_visible(False)
    # создадим спрайт своего курсора (банана)
    cursor_sprite = pygame.sprite.Sprite()
    cursor_sprite.image = load_image("banana_cursor.png")
    cursor_sprite.rect = cursor_sprite.image.get_rect()
    cursor_sprite.mask = pygame.mask.from_surface(cursor_sprite.image)  # маска курсора-банана
    all_sprites.add(cursor_sprite)
    x, y = pygame.mouse.get_pos()

    # игровой цикл
    running = True
    while running:
        if fail < 0:  # если очков меньше 0 - завершаем игру
            pygame.mixer.music.stop()
            end = True
            running = False

        clock.tick(FPS)  # держим игровой цикл на нужной скорости
        for event in pygame.event.get():
            if event.type == MYEVENTTYPE:
                i = rd.randint(1, 4)  # выбираем случайное количество новых обезьян (от 1 до 4)
                for _ in range(i):
                    generation_monkey(cur, all_sprites, monkeys)  # создаем обезьяну

                a = cursor_sprite  # передобавляем спрайт курсора-банана
                # это сделано, чтобы обезьяны не закрывали курсор
                cursor_sprite.kill()
                all_sprites.add(a)

                # снова выбираем случайное время, через которе появится следующая обезьяна
                pygame.time.set_timer(
                    MYEVENTTYPE, rd.choice([2000, 3000]))

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos

            if event.type == pygame.QUIT:

                running = False  # Если закрыли окно - заканчиваем игру
            if event.type == pygame.MOUSEBUTTONDOWN:
                for el in monkeys:
                    if pygame.sprite.collide_mask(el, cursor_sprite):
                        if el.type_name == 'pol':
                            pol = False
                        if el.type_name == 'left_tree':
                            left_tree = False
                        if el.type_name == 'top':
                            top = False
                        if el.type_name == 'right_tree':
                            right_tree = False
                        if el.type_name == 'palma':
                            palma = False
                        score += 1
                        el.kill()

        if True not in [pol, left_tree, right_tree, top, palma]: # если нет ни одной обезьяны на карте
            i = rd.randint(1, 4)  # выбираем случайное количество новых обезьян (от 1 до 4)
            for _ in range(i):
                generation_monkey(cur, all_sprites, monkeys)  # создаем обезьяну

        cursor_sprite.rect.x = x - 25
        cursor_sprite.rect.y = y - 25
        all_sprites.update()  # обновляем
        screen.blit(fon, (0, 0))  # Заливаем фон
        print_score(score, screen)  # Пишем счёт на экран

        all_sprites.draw(screen)  # отрисовываем
        pygame.display.flip()
    con.close()  # закрываем курсор базы данных
    pygame.mixer.music.stop()

    if end:  # если игрок проиграл или выиграл - запускаем окно конца игры
        data = open("data/score.txt", mode="r")

        if score > int(data.readline()):  # если счет больше рекорда записываем его в файл
            f = open("data/score.txt", mode="w")
            print(score, file=f)
            f.close()
        data.close()
        data = open("data/dates.txt", mode="r")
        t = data.readlines()

        if len(t) >= 3:
            f = open("data/dates.txt", mode="w")
            for el in t[1::]:
                print(el.rstrip(), file=f)
            f.close()
        f = open("data/dates.txt", mode="a")
        print(f'{datetime.datetime.now()} - {score}', file=f)
        data.close()
        f.close()
        end_screen(screen, score)
    pygame.display.quit()  # закрываем игру


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    start_screen(screen)
    main()
