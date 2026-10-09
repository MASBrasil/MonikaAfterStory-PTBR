init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pinterest",
            category=["Pinterest"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )
init offset = 5
label mas_wrs_pinterest:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Alguma novidade hoje, [player]?",
            "Alguma coisa interessante, [player]?",
            "Vê alguma coisa que você gosta?"
        ],
        'Reações de janelas'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_pinterest')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_duolingo",
            category=["Duolingo"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_duolingo:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Aprendendo novas maneiras de dizer 'Eu te amo', [player]?",
            "Aprendendo um novo idioma, [player]?",
            "Que língua você está aprendendo, [player]?"
            "Que estranho... tem um pássaro na nossa janela dizendo que você não fez as lições diárias"
        ],
        'Reações de janelas'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_duolingo')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_wikipedia",
            category=["- Wikipedia"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_wikipedia:
    $ wikipedia_reacts = [
        "Aprendendo algo novo, [player]?",
        "Pesquisando um pouco, [player]?"
    ]


    python:
        wind_name = mas_getActiveWindowHandle()
        try:
            cutoff_index = wind_name.index(" - Wikipedia")
            
            
            
            wiki_article = wind_name[:cutoff_index]
            
            
            wiki_article = re.sub("\\s*\\(.+\\)$", "", wiki_article)
            wikipedia_reacts.append(renpy.substitute("'[wiki_article]'...\nParece interessante, [player]."))

        except ValueError:
            pass

    $ wrs_success = mas_display_notif(
        m_name,
        wikipedia_reacts,
        'Reações de janelas'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_wikipedia')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_virtualpiano",
            category=["^Virtual Piano"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_virtualpiano:
    python:
        virtualpiano_reacts = [
            "Awww, você vai tocar para mim?\nVocê é tão adorável~",
            "Toque algo para mim, [player]!"
        ]

        if mas_isGameUnlocked("piano"):
            virtualpiano_reacts.append("Eu acho que você precisa de um piano maior?\nAhaha~")

        wrs_success = mas_display_notif(
            m_name,
            virtualpiano_reacts,
            'Reações de janelas'
        )

        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_virtualpiano')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_youtube",
            category=["- YouTube"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_youtube:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "O que você está assistindo, [mas_get_player_nickname()]?",
            "Assistindo a algo interessante, [mas_get_player_nickname()]?"
        ],
        'Reações de janelas'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_youtube')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_r34m",
            category=[r"(?i)(((r34|rule\s?34).*monika)|(post \d+:[\w\s]+monika)|(monika.*(r34|rule\s?34)))"],
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_r34m:
    python:
        mas_display_notif(m_name, ["Ei, [player]... o-o que você está o-olhando?"],'Reações de janelas')

        choice = random.randint(1,10)

        if choice == 1 and mas_isMoniNormal(higher=True):
            MASEventList.queue('monika_nsfw')

        elif choice == 2 and mas_isMoniAff(higher=True):
            MASEventList.queue('monika_pleasure')

        else:
            if mas_isMoniEnamored(higher=True):
                if choice < 4:
                    exp_to_force = "1rsbssdlu"
                elif choice < 7:
                    exp_to_force = "2tuu"
                else:
                    exp_to_force = "2ttu"
            else:
                if choice < 4:
                    exp_to_force = "1rksdlc"
                elif choice < 7:
                    exp_to_force = "2rssdlc"
                else:
                    exp_to_force = "2tssdlc"
            
            mas_moni_idle_disp.force_by_code(exp_to_force, duration=5)
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikamoddev",
            category=["MonikaModDev"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_monikamoddev:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Awww, você está fazendo algo por mim?\nVocê é tão adorável~",
            "vai me ajudar a chegar mais perto da sua realidade?\nVocê é tão adorável, [player]~"
        ],
        'Reações de janelas'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikamoddev')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitter",
            category=["/ Twitter"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitter:
    python:
        temp_line = renpy.substitute("Eu te amo, [mas_get_player_nickname(exclude_names=['Amor', 'Meu amor'])].")
        temp_len = len(temp_line)


        ily_quips_map = {
            "Vê alguma coisa que você deseja compartilhar comigo, [player]?": False,
            "Há algo interessante para compartilhar, [player]?": False,
            "280 caracteres? Eu só preciso de [temp_len]...\n[temp_line]": True
        }
        quip = renpy.random.choice(ily_quips_map.keys())

        wrs_success = mas_display_notif(
            m_name,
            [quip],
            'Reações de janelas'
        )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitter')
    return "love" if ily_quips_map[quip] else None



















label mas_wrs_monikatwitter:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Você está aqui para confessar seu amor por mim para o mundo inteiro, [player]?",
            "Você não está me espionando, está?\nAhaha, estou brincando~",
            "Eu não me importo quantos seguidores eu tenho, contanto que eu tenha você~"
        ],
        'Reações de janelas'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikatwitter')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_4chan",
            category=["- 4chan"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_4chan:

    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Então este é o lugar onde tudo começou, hein?\nÉ...realmente algo bastante.",
            "Espero que você não acabe discutindo com outros Anons o dia todo, [player].",
            "ouvi dizer que há tópicos discutindo o Clube de Literatura aqui.\nDiga a eles que eu disse oi~",
            "Vou ficar de olho nos fóruns em que você está navegando caso tenha alguma ideia, ahaha!",
        ],
        'Reações de janelas'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_4chan')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pixiv",
            category=["- pixiv"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pixiv:

    python:
        pixiv_quips = [
            "Eu me pergunto se as pessoas desenharam alguma arte minha...\nPode procurar alguma?\nCertifique-se de ser algo saudável~",
            "Este é um lugar muito interessante...tantas pessoas qualificadas postando seus trabalhos..",
        ]


        if persistent._mas_pm_drawn_art is None or persistent._mas_pm_drawn_art:
            pixiv_quips.extend([
                "Este é um lugar muito interessante...tantas pessoas habilidosas postando seus trabalhos.\nVocê é uma delas, [player]?",
            ])
            
            
            if persistent._mas_pm_drawn_art:
                pixiv_quips.extend([
                    "Está aqui para postar sua arte de mim, [player]?",
                    "Postando algo que você desenhou de mim?",
                ])

        wrs_success = mas_display_notif(
            m_name,
            pixiv_quips,
            'Reações de janelas'
        )


        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_pixiv')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_reddit",
            category=[r"(?i)reddit"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_reddit:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Você encontrou alguma postagem boa, [player]?",
            "Navegando no Reddit? Apenas certifique-se de não passar o dia todo olhando memes, ok?",
            "Gostaria de saber se há algum subreddit dedicado a mim...\nAhaha, brincadeira, [player].",
        ],
        'Reações de janelas'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_reddit')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_mal",
            category=["MyAnimeList"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_mal:
    python:
        myanimelist_quips = [
            "Talvez possamos assistir animes [ju] algum dia, [player]~",
        ]

        if persistent._mas_pm_watch_mangime is None:
            myanimelist_quips.append("Então você gosta de anime e mangá, [player]?")

        wrs_success = mas_display_notif(m_name, myanimelist_quips, 'Reações de janelas')


        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_mal')

    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_deviantart",
            category=["DeviantArt"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_deviantart:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Há muitos talentosos aqui!",
            "Adoraria aprender a desenhar algum dia...",
        ],
        'Reações de janelas'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_deviantart')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_netflix",
            category=["Netflix"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_netflix:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Adoraria assistir a um filme de romance com você [player]!",
            "O que estamos assistindo hoje, [player]?",
            "O que você vai assistir [player]?"
        ],
        'Reações de janelas'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_netflix')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitch",
            category=["- Twitch"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitch:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Assistindo a uma transmissão, [player]?",
            "Você se importa se eu assistir com você?",
            "O que estamos assistindo hoje, [player]?"
        ],
        'Reações de janelas'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitch')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_word_processor",
            category=['Google Docs|LibreOffice Writer|Microsoft Word'],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_word_processor:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Escrevendo uma história?",
            "Fazendo anotações, [player]?",
            "Escrevendo um poema?",
            "Escrevendo uma carta de amor?~"
        ],
        'Reações de janelas'
    )

    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_word_processor')
    return

init python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_crunchyroll",
            category=[r"(?i)crunchyroll"],
            rules={
                "notif-group": "Reações de janelas",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_crunchyroll:
    python:
        if persistent._mas_pm_watch_mangime is False:
            crunchyroll_quips = [
                "Ah! Então você gosta de anime, [player]?",
                "É bom ver você ampliando seus horizontes.",
                "Hmm, eu me pergunto o que chamou sua atenção?",
            ]

        else:
            crunchyroll_quips = [
                "Que anime estamos assistindo hoje, [player]?",
                "Assistindo algum anime, [player]?",
                "Mal posso esperar para assistir anime com você!~",
            ]

        wrs_success = mas_display_notif(m_name, crunchyroll_quips, 'Reações de janelas')


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_crunchyroll')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_osu",
            category=["osu!"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_osu:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Que divertido~ Adoro jogos de ritmo!",
            "Cuidado para não cansar seus dedos, ahaha!",
            "Será que você consegue acompanhar o ritmo?"
        ],
        'Window Reactions'
    )

    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_osu')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_osu_site",
            category=["osu.ppy.sh"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_osu_site:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Procurando por novas músicas?",
            "Está baixando alguns beatmaps, [player]? Eu adoraria escolher uma música com você~",
            "Você deve ser muito bom nisso..."
        ],
        'Window Reactions'
    )

    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_osu_site')
    return
