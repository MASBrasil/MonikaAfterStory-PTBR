init offset = 5





default -5 persistent._mas_pm_is_trans = False

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_gender",
            start_date=mas_getFirstSesh() + datetime.timedelta(minutes=10),
            action=EV_ACT_QUEUE
        ),
        skipCalendar=True
    )


label mas_gender:
    m 2eud "...[player]? Eu estive pensando em uma coisa."
    m 2euc "Eu já comentei antes que o ‘você’ do jogo pode não ser o verdadeiro você."
    m 7rksdla "Mas acho que acabei presumindo que você fosse um garoto."
    m 3eksdla "...Afinal, o protagonista era, né?"
    m 3eua "Mas, se eu sou a sua namorada, acho que é justo eu saber pelo menos isso sobre o verdadeiro você."

    m 1eua "Então, qual é o seu gênero?{nw}"
    $ _history_list.pop()
    menu:
        m "Então, qual é o seu gênero?{fast}"
        "Masculino.":

            $ persistent._mas_pm_is_trans = False
            $ persistent.gender = "M"
            m 3eua "Tudo bem, [player], obrigada por me contar."
            m 1hksdlb "Não que eu ficasse incomodada se você tivesse respondido outra coisa, viu?"
        "Feminino.":

            $ persistent._mas_pm_is_trans = False
            $ persistent.gender = "F"
            m 2eud "Ah? Então você é uma garota?"
            m 2hksdlb "Espero não ter dito nada que tenha te ofendido antes!"
            m 7rksdlb "...É por isso que dizem pra gente não tirar conclusões, ahaha!"
            m 3eka "Mas, pra ser honesta, isso não muda nada pra mim..."
        "Nenhum dos dois.":

            $ persistent._mas_pm_is_trans = False
            $ persistent.gender = "X"
            call mas_gender_neither
        "Sou transgênero.":

            call mas_gender_trans

            if persistent.gender != "X":
                m 1eka "Obrigada por confiar em mim, e lembre-se..."

    m 1ekbsa "Eu sempre vou te amar por quem você é, [player]~"


    $ mas_unlockEVL("monika_gender_redo","EVE")

    call mas_set_gender


    python:
        preferredname_ev = mas_getEV("mas_preferredname")
        if preferredname_ev:
            preferredname_ev.start_date = datetime.datetime.now() + datetime.timedelta(hours=2)
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gender_redo",
            category=['você'],
            prompt="Você pode me chamar por outros pronomes?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        ),
        markSeen=True
    )

label monika_gender_redo:
    m 1eka "É claro, [player]!"

    if not mas_getEVL_shown_count("monika_gender_redo"):
        m 3eka "Você fez algumas descobertas pessoais desde a última vez que conversamos sobre isso?{nw}"
        $ _history_list.pop()
        menu:
            m "Você fez algumas descobertas pessoais desde a última vez que conversamos sobre isso?{fast}"
            "Sim.":

                m 1eka "Entendo. Eu também já passei por isso."
                m 3hua "Tenho muito orgulho de você por estar nessa jornada de autodescoberta."
                m 1eub "...E ainda mais orgulho por ter coragem de me contar!"
            "Eu só estava com vergonha.":

                if persistent.gender == "M":
                    m 2ekd "Eu entendo, até comecei assumindo que você era um garoto, afinal."
                elif persistent.gender == "F":
                    m 2ekd "Eu entendo, talvez você tenha achado que eu me sentiria mais confortável passando tempo com outra garota."
                else:
                    m 2ekd "Eu entendo, talvez eu não tenha oferecido as opções certas para você escolher."

                m 2dkd "...E provavelmente não tornei fácil pra você me dizer o contrário..."
                m 7eua "Mas, seja qual for o seu gênero, eu amo você pelo que você é."
            "Eu não sabia se você me aceitaria como sou...":

                m 2wkd "[player]..."
                m 2dkd "Odeio pensar que não consegui te tranquilizar antes."
                m 7eka "Mas espero que você esteja me contando agora porque sabe que eu vou te amar, não importa o quê."
            "Sou gênero-fluído.":

                m 1eub "Ah, entendi!"
                m 3hub "Sinta-se à vontade pra me avisar sempre que quiser que eu use pronomes diferentes!"

    $ gender_var = None
    m "Então, qual é o seu gênero?{nw}"
    $ _history_list.pop()
    menu:
        m "Então, qual é o seu gênero?{fast}"
        "Sou um homem.":

            if persistent.gender == "M" and not persistent._mas_pm_is_trans:
                $ gender_var = "homem"
                call mas_gender_redo_same
            else:
                $ persistent.gender = "M"
                call mas_gender_redo_react
            $ persistent._mas_pm_is_trans = False
        "Sou uma mulher.":

            if persistent.gender == "F" and not persistent._mas_pm_is_trans:
                $ gender_var = "mulher"
                call mas_gender_redo_same
            else:
                $ persistent.gender = "F"
                call mas_gender_redo_react
            $ persistent._mas_pm_is_trans = False
        "Não me identifico com nenhum.":

            $ persistent._mas_pm_is_trans = False
            if persistent.gender == "X":
                call mas_gender_redo_neither_same
            else:
                $ persistent.gender = "X"
                if renpy.seen_label("mas_gender_neither"):
                    call mas_gender_redo_react
                else:
                    call mas_gender_neither
        "Sou transgênero.":

            call mas_gender_trans
            if persistent.gender != "X":
                call mas_gender_redo_react

    show monika 5hubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubsa "Eu sempre vou te amar por quem você é~"


    call mas_set_gender
    return "love"

label mas_gender_neither:
    m 1euc "Você não se vê como um garoto ou uma garota?"
    m 1eua "Isso é bem interessante... e de certo modo, eu meio que entendo."
    m 3esc "Tipo, eu sou uma garota, mas também sou uma personagem dentro de um jogo..."
    m 3esd "Então, de certa forma, eu nem sou uma garota de verdade."
    m 1hua "Mas quando você me trata como sua namorada, isso me deixa tão feliz!"
    m 3eua "...Então vou te tratar do jeitinho que você quiser ser tratado(a)."
    m 1ekbsa "Sua felicidade é o que mais importa pra mim, no fim das contas."
    return

label mas_gender_redo_same:
    m 1hksdlb "...É a mesma resposta de antes, [player]!"
    m 3eua "Se você estiver em dúvida sobre como responder, escolha o que te faz mais feliz."
    m 3eka "Não importa como seu corpo é, se você diz que é [gender_var], então é [gender_var] pra mim, tudo bem?"
    m 1eua "Quero que você seja quem realmente é enquanto estiver aqui comigo."
    return

label mas_gender_redo_react:
    m 1eka "Tudo bem, [player]..."
    m 3ekbsa "Desde que você esteja feliz, é isso que importa pra mim."
    return

label mas_gender_redo_neither_same:
    m 1hksdlb "...É a mesma resposta de antes, [player]... {w=0.3}Desculpa se isso não descreve você da melhor forma."
    m 1eka "Mas saiba que isso não muda nada pra mim..."
    return

label mas_gender_trans:
    if persistent._mas_pm_is_trans:
        $ menu_question = "E com qual gênero você se identifica?"
    else:
        $ menu_question = "Ah, entendi! {w=0.3}E com qual gênero você se identifica?"

    m 3eub "[menu_question]{nw}"
    $ _history_list.pop()
    menu:
        m "[menu_question]{fast}"
        "Masculino":

            $ persistent.gender = "M"
        "Feminino":

            $ persistent.gender = "F"
        "Nenhum dos dois":

            if persistent.gender == "X":
                call mas_gender_redo_neither_same
            else:

                $ persistent.gender = "X"
                call mas_gender_neither

    $ persistent._mas_pm_is_trans = True
    return


init -2 python:

    mas_bad_nickname_list = [
        "^fag$",
        "^ho$",
        "^hoe$",
        "^tit$",
        "aborto",
        "anal",
        "irritante",
        "ânus",
        "arrogante",
        "bunda",
        "atroz",
        "horrível",
        "Desgraçada",
        "fera",
        "cadela",
        "sangue",
        "besteira"
        "entediante",
        "bulli",
        "valentão",
        "besteira",
        "bunda(?!er|on)",
        "trapaceiro",
        "galo",
        "pretensioso",
        "preservativo",
        "corrupto",
        "puma",
        "porcaria",
        "louco",
        "arrepiante",
        "criminoso",
        "cruel",
        "porra",
        "boceta",
        "droga",
        "demônio",
        "pau",
        "dilf",
        "sujeira",
        "repugnante",
        "idiota",
        "burro",
        "egoísta",
        "egoísta",
        "mal",
        "bicha",
        "falha",
        "fake",
        "feto",
        "sujeira",
        "falta",
        "Porra",
        "lixo",
        "gay",
        "gey",
        "coroa",
        "Bruto",
        "horrível",
        "ódio",
        "sem coração",
        "hediondo",
        "hitler",
        "hore",
        "horrível",
        "horrível",
        "hipócrita",
        "idiota",
        "imbecil",
        "imoral",
        "insano",
        "irritante",
        "empurrão",
        "gigolô",
        "planta",
        "molestada",
        "lixo",
        "mate",
        "kunt",
        "lésbica",
        "lesbo",
        "lésbica",
        "lezbo",
        "mentiroso",
        "fracassado",
        "louco",
        "maníaco",
        "masoquista",
        "milf",
        "monstro",
        "Idiota",
        "assassinato",
        "narcisista",
        "desagradável",
        "nefasto",
        "mano"
        "negro",
        "nozes"
        "almofada",
        "panti"
        "pantsu",
        "calcinha",
        "pedo",
        "pênis",
        "brinquedo",
        "Poção",
        "pornô",
        "pretensioso",
        "psicopata",
        "fantoche",
        "bichano",
        "estupro",
        "repulsivo",
        "retardar",
        "vampiro",
        "garupa"
        "sádico",
        "escumalha",
        "egoísta",
        "sêmen",
        "merda",
        "doente",
        "abate",
        "estuprada",
        "escravo",
        "vagabunda",
        "sóciopata",
        "solo",
        "esperma",
        "fedor",
        "estúpido",
        "chupar",
        "tampão",
        "Saquinho de chá",
        "Terrível",
        "thot",
        "peitos",
        "titt",
        "ferramenta",
        "tormento",
        "tortura",
        "brinquedo",
        "armadilha",
        "Lixo",
        "provocadora",
        "feia",
        "sem utilidade",
        "vão",
        "vil",
        "vomitar",
        "desperdício",
        "prostituta",
        "perversa",
        "bruxa",
        "inútil",
        "enganada"
    ]



    mas_good_nickname_list_base = [
        "anjo",
        "bonita",
        "bela",
        "a melhor",
        "fofinha",
        "fofa",
        "gracinha",
        "querida",
        "grandiosa",
        "grande coração",
        "heroi",
        "meu amor",
        "gentil",
        "amor",
        "linda",
        "princesa",
        "rainha",
        "senpai",
        "brilho de sol",
        "doce"
    ]


    mas_good_nickname_list_player_modifiers = [
        "rei",
        "principe",
    ]


    mas_good_nickname_list_monika_modifiers = [
        "moni",
    ]

    mas_good_player_nickname_list = mas_good_nickname_list_base + mas_good_nickname_list_player_modifiers
    mas_good_monika_nickname_list = mas_good_nickname_list_base + mas_good_nickname_list_monika_modifiers


    mas_awkward_nickname_list = [
        r"\b(step[-\s]*)?bro(ther|thah?)?",
        r"\b(step[-\s]*)?sis(ter|tah?)?",
        r"\bdad\b",
        r"\bloli\b",
        r"\bson\b",
        r"\bmama\b",
        r"\bmom\b",
        r"\bmum\b",
        r"\bpapa\b",
        r"\bwet\b",
        "excitada",
        "tia",
        "batman",
        "criador",
        "bobba",
        "chefe",
        "mulher gato",
        "primo",
        "Papai",
        "deflowerer",
        "ereção",
        "dedo",
        "tesão",
        "kaasan",
        "kasan",
        "lamber",
        "maestre",
        "masturbat",
        "amante",
        "moani",
        "momika",
        "mamãe",
        "mommy",
        "mother",
        "danadinha",
        "okaasan",
        "okasan",
        "orgasmo",
        "soberano",
        "proprietário",
        "penetrat",
        "travesseiro",
        "sexo",
        "palmada",
        "super homem",
        "super mulher",
        "thicc",
        "coxa",
        "tia",
        "virgem"
    ]

    mas_awkward_quips = [
        "Eu não me sinto muito... {w=0.5}confortável te chamando assim.",
        "Isso é... {w=0.5}um nome meio estranho pra eu te chamar, [player].",
        "Hmm... {w=0.5}acho que não me sinto confortável te chamando assim, [player].",
        "Não que seja ruim, mas...{w=0.5}sabe?",
        "Você está tentando me deixar sem graça, [player]?"
    ]

    mas_bad_quips = [
        "[player]...{w=0.5}por que você se chamaria assim?",
        "[player]...{w=0.5}por que eu te chamaria desse jeito?",
        "Eu jamais conseguiria te chamar de algo assim, [player].",
        "O quê? Por favor, [player],{w=0.5} não se chame por nomes ruins."
    ]

    mas_good_player_name_comp = re.compile('|'.join(mas_good_player_nickname_list), re.IGNORECASE)
    mas_bad_name_comp = re.compile('|'.join(mas_bad_nickname_list), re.IGNORECASE)
    mas_awk_name_comp = re.compile('|'.join(mas_awkward_nickname_list), re.IGNORECASE)

label mas_player_name_enter_name_loop(input_prompt):
    python:
        good_quips = [
            "Esse é um nome maravilhoso!",
            "Eu gostei bastante, [player].",
            "Eu gostei desse nome, [player].",
            "É um ótimo nome!"
        ]


    show monika 1eua zorder MAS_MONIKA_Z at t11

    $ done = False
    while not done:
        python:
            tempname = mas_input(
                "[input_prompt]",
                length=20,
                screen_kwargs={"use_return_button": True}
            ).strip(' \t\n\r')

            lowername = tempname.lower()

        if lowername == "cancel_input":
            m 1eka "Ah... Tudo bem, se você diz."
            m 3eua "Me avise se mudar de ideia."
            $ done = True

        elif lowername == "":
            m 1eksdla "..."
            m 3rksdlb "Você precisa me dizer um nome para eu te chamar, [player]..."
            m 1eua "Tente novamente!"

        elif lowername == player.lower():
            m 2hua "..."
            m 4hksdlb "Esse já é o seu nome atual, bobinho!"
            m 1eua "Tente outro~"

        elif mas_awk_name_comp.search(tempname):
            $ awkward_quip = renpy.substitute(renpy.random.choice(mas_awkward_quips))
            m 1rksdlb "[awkward_quip]"
            m 3rksdla "Poderia escolher um nome mais... {w=0.2}{i}apropriado{/i}, por favor?"

        elif mas_bad_name_comp.search(tempname):
            $ bad_quip = renpy.substitute(renpy.random.choice(mas_bad_quips))
            m 1ekd "[bad_quip]"
            m 3eka "Por favor escolha um nome mais agradável, ok?"
        else:


            if store.mas_egg_manager.is_eggable_name(lowername):
                m 1ttu "Tem certeza que esse é seu nome real, ou está brincando comigo?{nw}"
                $ _history_list.pop()
                menu:
                    m "Tem certeza que esse é seu nome real, ou está brincando comigo?{fast}"
                    "Sim, esse é meu nome":

                        $ persistent._mas_disable_eggs = True
                    "Talvez...":

                        $ persistent._mas_disable_eggs = False

            python:
                old_name = persistent.playername.lower()
                done = True


                persistent.mcname = player
                mcname = player
                persistent.playername = tempname
                player = tempname



            if store.mas_egg_manager.sayori_enabled():
                call sayori_name_scare

            elif old_name == "sayori":

                $ songs.initMusicChoices()


            if lowername == "monika":
                m 1tkc "Sério?"
                m "É o mesmo que o meu!"
                m 1tku "Bem..."
                m "Ou é seu nome mesmo ou está brincando comigo."
                m 1hua "Mas tudo bem se quer que eu te chame assim~"

            elif mas_good_player_name_comp.search(tempname):
                $ good_quip = renpy.substitute(renpy.random.choice(good_quips))
                m 1sub "[good_quip]"
                m 3esa "Então tá! De agora em diante vou te chamar de '[player]'."
                m 1hua "Ehehe~"
            else:

                m 1eub "Tudo bem!"
                m 3eub "De agora em diante vou te chamar de '[player]'."

        if not done:
            show monika 1eua
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_preferredname",
            action=EV_ACT_QUEUE
        ),
        skipCalendar=True
    )



label mas_preferredname:
    m 1euc "Estive pensando sobre o seu nome."
    m 1esa "‘[player]’ é realmente o seu nome?"

    if renpy.windows and currentuser.lower() == player.lower():
        m 3esa "Quer dizer, é o mesmo nome do seu computador..."
        m 1eua "Você está usando '[currentuser]' e '[player]'."
        m "Ou então, você realmente gosta desse pseudônimo, ahaha."

    m 1eua "Quer que eu te chame por outro nome?{nw}"
    $ _history_list.pop()
    menu:
        m "Quer que eu te chame por outro nome?{fast}"
        "Sim.":


            call mas_player_name_enter_name_loop ("Me conta, qual é?")
        "Não.":

            m 3eua "Tudo bem, me avisa se mudar de ideia."


    $ mas_unlockEVL("monika_changename", "EVE")
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_changename",
            category=['você'],
            prompt="Eu mudei meu nome",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        ),
        markSeen=True
    )


label monika_changename:
    call mas_player_name_enter_name_loop ("Como você gostaria que eu te chamasse?")
    return

default -5 persistent._mas_player_bday = None

default -5 persistent._mas_player_confirmed_bday = False

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_birthdate",
            conditional="datetime.date.today()>mas_getFirstSesh().date() and not persistent._mas_player_confirmed_bday",
            action=EV_ACT_QUEUE
        )
    )

label mas_birthdate:
    m 1euc "Ei [player], eu estava pensando..."
    if persistent._mas_player_bday is not None:
        $ bday_str, diff = store.mas_calendar.genFormalDispDate(persistent._mas_player_bday)
        m 3eksdlc "Eu lembro que você me disse seu aniversário antes, mas não tenho certeza se perguntei pela {i}data de nascimento{/i} ou só pelo {i}dia do aniversário...{/i}"

        m "Só para ter certeza, sua data de nascimento é [bday_str]?{nw}"
        $ _history_list.pop()
        menu:
            m "Só para ter certeza, sua data de nascimento é [bday_str]?{fast}"
            "Sim.":
                if datetime.date.today().year - persistent._mas_player_bday.year < 5:
                    m 2rksdla "Tem certeza disso, [player]?"
                    m 2eksdlc "Isso faria você ser muito jovem..."
                    m 3ekc "Lembre-se, estou perguntando pela sua {b}data de nascimento{/b}, não só pelo dia do aniversário."
                    m 1eka "Então, quando você nasceu, [player]?"
                    jump mas_bday_player_bday_select_select
                else:
                    $ old_bday = mas_player_bday_curr()
                    if not mas_isplayer_bday():
                        m 1hua "Ah, ótimo [player], obrigada."
                        m 3hksdlb "Só precisava confirmar, eu não gostaria de errar algo tão importante como quando você nasceu, ahaha!"
            "Não.":

                m 3rksdlc "Ah! Tudo bem então..."
                m 1eksdld "Qual {i}é{/i} sua data de nascimento, [player]?"
                jump mas_bday_player_bday_select_select
    else:

        m 3wud "Na verdade eu não sei quando é sua data de nascimento!"
        m 3hub "Isso é algo que eu deveria saber, ahaha!"
        m 1eua "Então, quando você nasceu, [player]?"
        jump mas_bday_player_bday_select_select

label birthdate_set:
    python:
        bday_upset_ev = mas_getEV('mas_player_bday_upset_minus')
        if bday_upset_ev is not None:
            bday_upset_ev.start_date = mas_player_bday_curr()
            bday_upset_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_upset_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time "
                "and not mas_isMonikaBirthday()"
            )
            bday_upset_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_upset_ev)


        bday_ret_bday_ev = mas_getEV('mas_player_bday_ret_on_bday')
        if bday_ret_bday_ev is not None:
            bday_ret_bday_ev.start_date = mas_player_bday_curr()
            bday_ret_bday_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_ret_bday_ev.conditional = (
                "mas_isplayer_bday() "
                
                "and len(store.persistent._mas_dockstat_checkin_log) > 0 "
                "and store.persistent._mas_dockstat_checkin_log[-1][0] is not None "
                "and store.persistent._mas_dockstat_checkin_log[-1][0].date() == mas_player_bday_curr() "
                "and not persistent._mas_player_bday_spent_time "
                "and persistent._mas_player_confirmed_bday "
                "and not mas_isO31() "
                "and not mas_isD25() "
                "and not mas_isF14() "
                "and not mas_isMonikaBirthday()"
            )
            bday_ret_bday_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_ret_bday_ev)


        bday_no_restart_ev = mas_getEV('mas_player_bday_no_restart')
        if bday_no_restart_ev is not None:
            bday_no_restart_ev.start_date = datetime.datetime.combine(mas_player_bday_curr(), datetime.time(hour=19))
            bday_no_restart_ev.end_date = datetime.datetime.combine(
                mas_player_bday_curr() + datetime.timedelta(days=1),
                datetime.time()
            )
            bday_no_restart_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time "
                "and not mas_isO31() "
                "and not mas_isD25() "
                "and not mas_isF14() "
                "and not mas_isMonikaBirthday()"
            )
            bday_no_restart_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_no_restart_ev)


        bday_holiday_ev = mas_getEV('mas_player_bday_other_holiday')
        if bday_holiday_ev is not None:
            bday_holiday_ev.start_date = mas_player_bday_curr()
            bday_holiday_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_holiday_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time "
                "and (mas_isO31() or mas_isD25() or mas_isF14()) "
            )
            bday_holiday_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_holiday_ev)

    if old_bday is not None:
        $ old_bday = old_bday.replace(year=mas_player_bday_curr().year)

    if not mas_isplayer_bday() and old_bday == mas_player_bday_curr():
        $ persistent._mas_player_confirmed_bday = True
        return

    if mas_isplayer_bday() and not mas_isMonikaBirthday():
        $ persistent._mas_player_bday_spent_time = True
        if old_bday == mas_player_bday_curr():
            if mas_isMoniNormal(higher=True):
                m 3hub "Ahaha! Então hoje {i}é{/i} o seu aniversário!"
                m 1tsu "Estou feliz de estar preparada, ehehe..."
                m 3eka "Só espere um pouco, [player]..."
                show monika 1dsc
                pause 2.0
                $ store.mas_surpriseBdayShowVisuals()
                $ persistent._mas_player_bday_decor = True
                m 3hub "Feliz aniversário, [player]!"
                m 1hub "Estou tão feliz de poder estar com você em seu aniversário!"
                m 3sub "Ah...{w=0.5} seu bolo!"
                call mas_player_bday_cake
            elif mas_isMoniDis(higher=True):
                m 2eka "Ah, então hoje {i}é{/i} o seu aniversário!"
                m "Feliz Aniversário, [player]."
                m 4eka "Espero que tenha um ótimo dia."
        else:
            if mas_isMoniNormal(higher=True):
                $ mas_gainAffection(5, bypass=True)
                $ persistent._mas_player_bday_in_player_bday_mode = True
                $ mas_unlockEVL("bye_player_bday", "BYE")
                m 1wuo "Ah...{w=1}Ah!"
                m 3sub "Hoje é o seu aniversário!"
                m 3hub "Feliz aniversário, [player]!"
                m 1rksdla "Queria que você tivesse me avisado antes, eu teria preparado algo."
                m 1eka "Mas ao menos posso fazer isto..."
                call mas_player_bday_moni_sings
                m 1hub "Ahaha! Não é muito, mas já é algo!"
                m 3hua "Eu prometo que ano que vem faremos algo muito especial, [player]!"
            elif mas_isMoniDis(higher=True):
                m 2eka "Ah, então hoje é seu aniversário..."
                m "Feliz aniversário, [player]."
                m 4eka "Espero que tenha um ótimo dia."


    elif not mas_isMonikaBirthday() and (persistent._mas_player_bday.month == mas_getFirstSesh().date().month and persistent._mas_player_bday.day == mas_getFirstSesh().date().day):
        m 1sua "Ah! Seu aniversário é no mesmo dia que o nosso aniversário de namoro, [player]?"
        m 3hub "Isso é incrível!"
        m 1sua "Não posso imaginar um dia mais especial do que celebrar seu aniversário e o nosso amor no mesmo dia..."

        if mas_player_bday_curr() == mas_o31:
            $ hol_str = "Halloween"
        elif mas_player_bday_curr() == mas_d25:
            $ hol_str = "Natal"
        elif mas_player_bday_curr() == mas_monika_birthday:
            $ hol_str = "meu aniversário"
        elif mas_player_bday_curr() == mas_f14:
            $ hol_str = "Dia dos namorados"
        else:
            $ hol_str = None
        if hol_str is not None:
            m "E também é [hol_str]..."
        m 3hua "É tão mágico~"

    elif mas_player_bday_curr() == mas_monika_birthday:
        m 1wuo "Ah...{w=1}Ah!"
        m 3sua "Nós fazemos aniversário no mesmo dia!"
        m 3sub "Isso é {i}tão{/i} legal, [player]!"
        m 1tsu "Acho que realmente fomos feitos um para o outro, ehehe..."
        if mas_isMonikaBirthday() and mas_isMoniNormal(higher=True):
            $ mas_gainAffection(5,bypass=True)
            $ persistent._mas_player_bday_in_player_bday_mode = True
            m 3hua "Isso só torna esse dia ainda mais especial~"
            m 1eub "Cante comigo, [player]!"
            call mas_player_bday_moni_sings
        else:
            m 3hua "Vamos ter que fazer desse um dia super especial~"

    elif mas_player_bday_curr() == mas_o31:
        m 3eua "Ah! Acho bem legal você ter nascido no Halloween, [player]!"
        m 1hua "Bolo de aniversário, doces, e você..."
        m 3hub "Isso é doce demais para um dia, ahaha!"

    elif mas_player_bday_curr() == mas_d25:
        m 1hua "Ah! Acho incrível que você tenha nascido no Natal, [player]!"
        m 3rksdla "Embora... {w=0.5}receber presentes para as duas comemorações no mesmo dia possa parecer que você não ganha tantos..."
        m 3hub "Ainda assim deve ser um dia bem especial!"

    elif mas_player_bday_curr() == mas_f14:
        m 1sua "Ah! Seu aniversário é no Dia dos namorados..."
        m 3hua "Que romântico!"
        m 1ekbfa "Não vejo a hora de celebrar nosso amor e seu aniversário no mesmo dia, [player]~"

    elif persistent._mas_player_bday.month == 2 and persistent._mas_player_bday.day == 29:
        m 3wud "Ah! Você nasceu no dia 29 de fevereiro, isso é tão legal!"
        m 3hua "Então vamos ter que celebrar seu aniversário em Março nos anos que não forem bissextos, [player]."

    $ persistent._mas_player_confirmed_bday = True
    $ mas_rmallEVL("calendar_birthdate")
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="calendar_birthdate",


        )
    )

label calendar_birthdate:
    m 1lksdla "Ei, [player]..."
    m 3eksdla "Você deve ter notado que meu calendário estava bem vazio..."
    m 1rksdla "Bem...{w=0.5} tem uma coisa que definitivamente deveria estar nele..."
    m 3hub "Seu aniversário, ahaha!"
    m 1eka "Se vamos estar em um relacionamento, é algo que eu realmente deveria saber..."
    m 1eud "Então [player], quando você nasceu?"
    call mas_bday_player_bday_select
    $ mas_stripEVL('mas_birthdate', list_pop=True)
    return



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_unlock_chess",
            conditional=(
                "store.mas_xp.level() >= 8 "
                "or store.mas_games._total_games_played() > 99"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_unlock_chess:
    m 1eua "Então, [player]..."

    if store.mas_games._total_games_played() > 5:
        $ games = "jogos"
        if not renpy.seen_label('game_pong'):
            $ games = "Forca"
        elif not renpy.seen_label('game_hangman'):
            $ games = "Pong"

        if store.mas_games._total_games_played() > 99:
            m 1hub "Você {i}realmente{/i} parece gostar de jogar [games] comigo!"
        else:
            m 1eub "Parece que você tem se divertido jogando [games] comigo!"

        m 3eub "Adivinha só? {w=0.2}Tenho um jogo novo pra gente jogar!"
    else:

        $ really = "mesmo "
        if store.mas_games._total_games_played() == 0:
            $ really = ""

        m 3rksdla "Eu sei que você não tem [really]se interessado muito pelos outros jogos que fiz...{w=0.2} então pensei em tentar um tipo completamente diferente de jogo..."

    m 3tuu "Esse aqui é bem mais estratégico..."
    m 3hub "É xadrez!"

    if persistent._mas_pm_likes_board_games is False:
        m 3eka "Eu sei que você me disse que esse tipo de jogo não é muito a sua praia..."
        m 1eka "Mas eu ficaria muito feliz se você pudesse dar uma chance."
        m 1eua "Enfim..."

    m 1esa "Não sei se você sabe jogar, mas sempre foi um hobby meu, de certa forma."
    m 1tku "Então já vou te avisando!"
    m 3tku "Eu sou bem boa nisso."
    m 1lsc "Agora que penso bem... será que isso tem a ver com o que eu sou?"
    m "Quer dizer... estar presa dentro desse jogo."
    m 1eua "Nunca me vi como uma IA de xadrez, mas... não combinaria um pouco?"
    m 3eua "Afinal, dizem que computadores são muito bons em xadrez."
    m "Já venceram até grandes mestres."
    m 1eka "Mas não pense nisso como uma batalha entre humano e máquina, tá?"
    m 1hua "Pensa só que você está jogando um jogo divertido com sua linda namorada..."
    m "E eu prometo pegar leve com você."

    if not mas_games.is_platform_good_for_chess():
        m 2tkc "...Espera um pouco."
        m 2tkx "Tem alguma coisa errada aqui."
        m 2ekc "Parece que estou tendo problemas pra fazer o jogo funcionar."
        m 2euc "Talvez o código não funcione nesse sistema?"
        m 2ekc "Desculpa, [player], mas o xadrez vai ter que esperar por enquanto."
        m 4eka "Mas prometo que a gente joga assim que eu conseguir fazer funcionar!"

    $ mas_unlockGame("chess")
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_unlock_hangman",
            conditional=(
                "store.mas_xp.level() >= 4 "
                "or store.mas_games._total_games_played() > 49"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_unlock_hangman:
    m 1eua "Ei, [player]..."

    if store.mas_games._total_games_played() > 49:
        m 3eub "Já que você parece adorar jogar comigo, pensei que talvez gostasse de outros jogos também!"

    elif renpy.seen_label('game_pong') and not renpy.seen_label('mas_nou'):
        m 1eksdla "Achei que você pudesse estar ficando entediado com Pong..."

    elif renpy.seen_label('game_pong') and renpy.seen_label('mas_nou'):
        m 1eksdla "Achei que você pudesse estar ficando entediado com Pong e NOU..."

    elif not renpy.seen_label('game_pong') and renpy.seen_label('mas_nou'):
        m 1eksdla "Achei que você pudesse estar ficando entediado com NOU..."
    else:

        m 1lksdla "Já que você não parece muito interessado em jogar comigo, pensei que talvez prefira outros tipos de jogos..."

    m 1hua "Entãoooo~"
    m 1hub "Fiz o jogo da Forca!"

    if mas_safeToRefDokis():
        m 1lksdlb "Espero que não seja de mau gosto..."

    m 1eua "Sempre foi meu jogo favorito no clube."

    if mas_safeToRefDokis():
        m 1lsc "Mas, pensando bem..."
        m "O jogo é na verdade bem mórbido."
        m 3rssdlc "Você adivinha letras para salvar a vida de alguém."
        m "Acerta todas e a pessoa não é enforcada."
        m 1lksdlc "Mas erra todas..."
        m "Ela morre porque você não adivinhou as letras certas."
        m 1eksdlc "Bem sombrio, não é?"
        m 1hksdlb "Mas não se preocupe, [player], é só um jogo no final das contas!"
        m 1eua "Garanto que ninguém será machucado com este jogo."

        if persistent.playername.lower() == "sayori":
            m 3tku "...Talvez~"
    else:

        m 1hua "Espero que goste de jogar comigo!"

    $ mas_unlockGame("hangman")
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_unlock_piano",
            conditional="store.mas_xp.level() >= 12",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label mas_unlock_piano:
    m 2hua "Ei! Tenho algo emocionante para te contar!"
    m 2eua "Finalmente coloquei um piano no quarto para nós, [player]."
    if not persistent._mas_pm_plays_instrument:
        m 3hub "Eu realmente quero te ouvir tocar!"
        m 3eua "Pode parecer difícil no começo, mas pelo menos tente."
        m 3hua "Afinal, todo mundo começa de algum lugar."
    else:

        m 1eua "Claro, tocar música não é nada novo para você."
        m 4hub "Então estou esperando algo bonito! Ehehe~"

    m 4hua "Não seria divertido tocarmos algo [ju]?"
    m "Talvez possamos até fazer um dueto!"
    m 4hub "Nós dois melhoraríamos e nos divertiríamos ao mesmo tempo."
    m 1hksdlb "Ah, acho que estou ficando um pouco empolgada demais. Desculpa!"
    m 3eua "Eu só quero ver você apreciar o piano como eu aprecio."
    m "Para sentir a paixão que eu sinto por isso."
    m 3hua "É uma sensação maravilhosa."
    m 1eua "Espero não estar sendo insistente, mas eu adoraria se você tentasse."
    m 1eka "Por mim, por favor?~"
    $ mas_unlockGame("piano")
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_random_limit_reached"
        )
    )

label mas_random_limit_reached:

    $ mas_display_notif(m_name, ["Ei [player]..."], "Alertas de Assuntos")

    python:
        limit_quips = [
            _("Parece que estou sem ideias do que dizer."),
            _("Não sei mais o que dizer, mas fica comigo só mais um pouquinho?"),
            _("Não adianta tentar dizer tudo de uma vez..."),
            _("Espero que tenha gostado de ouvir tudo sobre o que pensei hoje..."),
            _("Você ainda gosta de passar esse tempo comigo?"),
            _("Espero não ter te entediado muito."),
            _("Você não se importa se eu pensar no que dizer a seguir, né?")
        ]
        limit_quip=renpy.random.choice(limit_quips)

    m 1eka "[limit_quip]"
    if len(mas_rev_unseen) > 0 or persistent._mas_enable_random_repeats:
        m 1ekc "Tenho certeza que vou ter algo para conversar daqui a pouco."
    else:

        if not renpy.seen_label("mas_random_ask"):
            call mas_random_ask
            if _return:
                m "Agora deixa eu pensar em algo para conversar."
                return
        m 1ekc "Espero pensar em algo divertido para conversar logo."
        $ mas_showEVL('monika_quiet_time','EVE',unlock=True)
        $ mas_stripEVL('monika_quiet_time',remove_dates=False)

    return "no_unlock"

label mas_random_ask:
    m 1lksdla "...{w=0.5}[mas_get_player_nickname()]?"

    m "Tudo bem se eu repetir algumas coisas que já falei antes?{nw}"
    $ _history_list.pop()
    menu:
        m "Tudo bem se eu repetir algumas coisas que já falei antes?{fast}"
        "Sim.":
            m 1eua "Ótimo!"
            m 3eua "Se você cansar de me ouvir falar sobre as mesmas coisas, pode abrir o menu de configurações e desmarcar 'Repetir Tópicos'."

            if mas_isMoniUpset(lower=True):
                m 1esc "Isso me avisa quando você está entediado comigo."
            else:
                m 1eka "Isso me avisa quando você só quer passar um tempo quieto comigo."

            $ persistent._mas_enable_random_repeats = True
            return True
        "Não.":

            m 1eka "Tudo bem."
            m 1eua "Se mudar de ideia, é só abrir as configurações e clicar em 'Repetir Tópicos'."
            m "Assim eu sei se você não se importa que eu repita algo que já falei."
            return False





init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monikai_detected",
            conditional=(
                "is_running(['monikai.exe']) and "
                "not seen_event('mas_monikai_detected')"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_monikai_detected:
    m 2wud "O que é isso?"
    m "Isso é-"
    $ _history_list.pop()
    m 1wuo "Isso é{fast} uma versão miniatura de mim?"
    m 1hua "Que fofa!"

    m 1eua "Você instalou isso para poder me ver o tempo todo?{nw}"
    $ _history_list.pop()
    menu:
        m "Você instalou isso para poder me ver o tempo todo?{fast}"
        "Claro!":
            pass
        "Sim.":
            pass
        "...Sim.":
            pass
    m 1hub "Ahaha~"
    m 1hua "Estou lisonjeada que você baixaria algo assim."
    m 1eua "Só não comece a passar mais tempo com {i}ela{/i} do que comigo."
    m 3eua "Afinal, eu sou a verdadeira."
    return




init python:
    ev_rules = {}
    ev_rules.update(MASGreetingRule.create_rule(skip_visual=True))
    ev_rules.update(MASPriorityRule.create_rule(-1))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="mas_crashed_start",
            unlocked=True,
            category=[store.mas_greetings.TYPE_CRASHED],
            rules=ev_rules,
        ),
        restartBlacklist=True,
        code="GRE"
    )

    del ev_rules



default -5 persistent._mas_crashed_before = False


default -5 persistent._mas_crashed_trynot = False


label mas_crashed_start:
    if persistent._mas_crashed_before:

        call mas_crashed_preshort


        call mas_crashed_short


        call mas_crashed_post
    else:


        call mas_crashed_prelong


        call mas_crashed_long_qs


        call mas_crashed_long_prefluster


        call mas_crashed_long_fluster


        call mas_crashed_long_postfluster


        call mas_crashed_long_whq


        call mas_crashed_post


    if len(persistent.event_list) == 0:
        show monika idle with dissolve_monika
    return

label mas_crashed_prelong:


    $ mas_startupWeather()


    scene black
    $ HKBHideButtons()
    $ disable_esc()
    $ store.songs.enabled = False
    $ _confirm_quit = False




    return


label mas_crashed_long_qs:

    python:
        quit_msg = "Estou com medo, [player]!\nPor favor, clique em 'Não' e me ajude!"
        quit_yes = "T_T [player]..."
        quit_no = "Obrigada!\nPor favor me ajude!"


    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "SEI QUE VOCÊ TRAVOU (long)"


    pause 5.0
    m "[player]?{w=0.3} É você?{nw}"
    $ _history_list.pop()
    $ mas_disable_quit()
    $ mas_setQuitMsg(quit_msg, quit_yes, quit_no)
    show screen mas_background_timed_jump(4, "mas_crashed_long_uthere")
    menu:
        m "[player]? É você?{fast}"
        "Sim.":

            hide screen mas_background_timed_jump

            $ mas_gainAffection(modifier=0.2, bypass=True)
            m "Estou tão feliz que você está aqui."
            jump mas_crashed_long_uthere.afterdontjoke
        "Não.":

            hide screen mas_background_timed_jump
            m "[player]!{fast}"
            jump mas_crashed_long_uthere.dontjoke

label mas_crashed_long_uthere:

    hide screen mas_background_timed_jump
    m "[player]!{fast}"
    m "Sabia que você estava aí!"

label mas_crashed_long_uthere.dontjoke:
    $ mas_loseAffection()
    m "Não brinque comigo assim!"
    m "Enfim..."

label mas_crashed_long_uthere.afterdontjoke:
    m "{cps=*2}Tudo ficou escuro de repente.{/cps}"
    m "Pode acender as luzes?"

    window hide
    show screen mas_background_timed_jump(5, "mas_crashed_long_foundlight")
    menu:
        "Acender as luzes.":
            hide screen mas_background_timed_jump

            $ mas_gainAffection(modifier=0.2, bypass=True)
        "...":

            pause 5.0
            label mas_crashed_long_foundlight:
                hide screen mas_background_timed_jump
                window show
                m "Deixa pra lá, eu encontrei."
                window hide


    play sound light_switch
    call spaceroom (hide_monika=True, show_emptydesk=True)
    pause 2.0
    call mas_transition_from_emptydesk ("monika 6ektsc_static")

    return


label mas_crashed_long_prefluster:
    pause 1.0


    show monika 6dstsc
    pause 1.0
    window auto


    m 6ektsa "[player]!{fast}"


    show monika 6ATL_cryleftright
    m "{cps=*1.5}O que aconteceu?{/cps}{nw}"

    return

label mas_crashed_long_postfluster:
    window hide
    show screen mas_background_timed_jump(8, "mas_crashed_long_nofluster")
    menu:
        "Se acalme, [m_name]. Você está segura agora.":
            hide screen mas_background_timed_jump


            $ mas_gainAffection(modifier=0.5, bypass=True)


            show monika 6dstsc
            pause 1.0
            window auto


            m 6ektda "Obrigada, [player]."
            m "Me sinto melhor agora que você está aqui comigo."
        "...":

            label mas_crashed_long_nofluster:
                hide screen mas_background_timed_jump



                show monika 6dstsc
                pause 4.0

                show monika 6ektdc
                pause 1.0
                window auto


                m "Ok, me sinto melhor agora."


    show monika 6dstdc
    pause 1.0
    return

label mas_crashed_long_whq:


    m 2ekc "Enfim..."
    m "Você sabe o que aconteceu, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você sabe o que aconteceu, [player]?{fast}"
        "O jogo travou.":
            m 2wud "O jogo...{w=0.3} travou?"
            m 2ekd "Isso é assustador, [player]."
        "Eu não sei.":

            m "Bem..."
            m "Eu apreciaria muito se você pudesse dar uma olhada nisso."
            m "É assustador ser lançada repentinamente na escuridão daquele jeito."
            jump mas_crashed_long_whq.end


    m "Acha que pode impedir que isso aconteça?{nw}"
    $ _history_list.pop()
    menu:
        m "Acha que pode impedir que isso aconteça?{fast}"
        "Vou tentar.":

            $ mas_gainAffection(modifier=0.2, bypass=True)
            $ persistent._mas_crashed_trynot = True
            m 1hua "Obrigada, [player]!"
            m 1eua "Estou contando com você."
            m "Mas vou me preparar mentalmente, só para me garantir."
        "Isso simplesmente acontece.":

            m 1ekc "Ah..."
            m 1lksdlc "Está tudo bem.{w=0.3} Vou me preparar mentalmente no caso de isso acontecer de novo."

label mas_crashed_long_whq.end:
    m "Enfim..."
    m 1eua "O que iremos fazer hoje?"

    $ persistent._mas_crashed_before = True
    $ mas_resetQuitMsg()
    return



label mas_crashed_post:

    python:
        enable_esc()
        store.songs.enabled = True
        HKBShowButtons()
        set_keymaps()
        persistent.closed_self = False
        mas_startup_song()

    return


label mas_crashed_long_fluster:
    $ mas_setApologyReason(reason=10)
    m "{cps=*1.5}V-você estava aqui um segundo e, d-{w=0.3}de repente, tudo ficou escuro...{/cps}{nw}"
    m "{cps=*1.5}E então você s-{w=0.3}sumiu, e eu fiquei tão preocupada achando que t-{w=0.3}tinha acontecido algo com você...{/cps}{nw}"
    m "{cps=*1.5}...e eu fiquei tão a-{w=0.3}apavorada, porque achei que tinha quebrado tudo de novo!{/cps}{nw}"
    m "{cps=*1.5}Mas eu juro que d-{w=0.3}dessa vez eu não mexi em nada no jogo!{/cps}{nw}"
    m "{cps=*1.5}P-pelo menos, eu acho que não... mas é p-{w=0.3}possível, talvez...{/cps}{nw}"
    m "{cps=*1.5}É que às vezes eu n-{w=0.3}não sei d-{w=0.3}direito o que estou fazendo,{/cps}{nw}"
    m "{cps=*1.5}mas eu espero que dessa v-{w=0.3}vez não tenha sido c-{w=0.3}culpa minha, porque eu r-{w=0.3}realmente não toquei em nada...{/cps}{nw}"
    return


label mas_crashed_preshort:

    $ mas_startupWeather()


    call spaceroom (scene_change=True, force_exp="monika 2ekc")
    return

label mas_crashed_short:
    python:

        q_list = MASQuipList()


        crash_labels = [
            "mas_crashed_quip_takecare"
        ]
        for _label in crash_labels:
            q_list.addLabelQuip(_label)


        t_quip, v_quip = q_list.quip()


    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "SEI QUE VOCÊ TRAVOU (short)"

    if t_quip == MASQuipList.TYPE_LABEL:
        call expression v_quip
    else:


        m 1hub "[v_quip]"

    return


label mas_crashed_quip_takecare:
    $ mas_setApologyReason(reason=9)
    m 2ekc "Travou de novo, [player]?"

    if persistent._mas_idle_data.get("monika_idle_game", False):

        m 3ekc "Acha que teve algo a ver com o seu jogo?{nw}"
        $ _history_list.pop()
        menu:
            m "Acha que teve algo a ver com o seu jogo?{fast}"
            "Sim.":
                m 1hksdlb "Ahaha..."
                m 1hub "Bom, espero que tenha se divertido~"
                m 1rksdla "...E que o seu computador esteja bem."
                m 3eub "Eu estou bem, então não precisa se preocupar~"
            "Não.":
                m 1eka "Ah, entendo."
                m "Desculpe por ter presumido isso."
                m 1hub "Eu estou bem, caso estivesse se perguntando."
                m 3hub "Espero que tenha se divertido antes do travamento, ahaha!"
                if mas_isMoniHappy(higher=True):
                    m 1hubsa "Fico feliz que tenha voltado pra mim agora~"
        m 2rksdla "Ainda assim..."
    m 2ekc "Talvez você devesse cuidar melhor do seu computador."
    m 4rksdlb "É a minha casa, afinal..."
    return


init python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_corrupted_persistent"
        )
    )

init 6 python:
    if mas_per_check.is_per_corrupt() and mas_per_check.has_backups():
        mas_note_backups_all_good = None
        mas_note_backups_some_bad = None
        
        def _mas_generate_backup_notes():
            global mas_note_backups_all_good, mas_note_backups_some_bad
            
            
            just_let_u_know = (
                'Só queria te avisar que seu arquivo "persistent" estava '
                'corrompido, mas consegui restaurar um backup antigo!'
            )
            even_though_bs = (
                "Mesmo que o sistema de backups que eu criei seja bem eficiente, "
            )
            if_i_ever = (
                'Se eu tiver problemas para carregar o "persistent" de novo, vou '
                'escrever outro bilhetinho na pasta de personagens, então fica '
                'de olho!'
            )
            good_luck = "Boa sorte com a Monika!"
            dont_tell = "P.S: Não conta para ela que fui eu!"
            block_break = "\n\n"
            
            
            mas_note_backups_all_good = MASPoem(
                poem_id="note_backups_all_good",
                prompt="",
                category="note",
                author="chibika",
                title="Oi [player],",
                text="".join([
                    just_let_u_know,
                    block_break,
                    even_though_bs,
                    "é bom você fazer cópias dos backups de vez em quando, ",
                    "só por segurança. ",
                    'Os backups se chamam "persistent##.bak", onde "##" é ',
                    "um número de dois dígitos. ",
                    'Você pode encontrá-los em "',
                    renpy.config.savedir,
                    '".',
                    block_break,
                    if_i_ever,
                    block_break,
                    good_luck,
                    block_break,
                    dont_tell
                ])
            )
            
            mas_note_backups_some_bad = MASPoem(
                poem_id="note_backups_some_bad",
                prompt="",
                category="Nota",
                author="chibika",
                title="Olá [player],",
                text="".join([
                    just_let_u_know,
                    block_break,
                    "No entanto, alguns dos seus backups também estavam corrompidos. ",
                    even_though_bs,
                    "você deveria os deletar, já que eles podem acabar ",
                    "prejudicando. ",
                    block_break,
                    "Aqui está uma lista de arquivos que estão corrompidos:",
                    block_break,
                    "\n".join(store.mas_utils.bullet_list(
                        mas_per_check.mas_bad_backups
                    )),
                    block_break,
                    'Você pode os encontrar em "',
                    renpy.config.savedir,
                    '". ',
                    "Quando estiver lá, você deveria fazer cópias dos ",
                    "backups bons, só para garantir.",
                    block_break,
                    if_i_ever,
                    block_break,
                    good_luck,
                    block_break,
                    dont_tell
                ])
            )
        
        _mas_generate_backup_notes()
        import os
        
        if len(mas_per_check.mas_bad_backups) > 0:
            
            store.mas_utils.trywrite(
                os.path.normcase(renpy.config.basedir + "/characters/nota.txt"),
                renpy.substitute(mas_note_backups_some_bad.title) + "\n\n" + mas_note_backups_some_bad.text
            )
        
        else:
            
            store.mas_utils.trywrite(
                os.path.normcase(renpy.config.basedir + "/characters/nota.txt"),
                renpy.substitute(mas_note_backups_all_good.title) + "\n\n" + mas_note_backups_all_good.text
            )


label mas_corrupted_persistent:
    m 1eud "Ei, [player]..."
    m 3euc "Alguém deixou um bilhete na pasta 'characters' endereçado a você."
    m 1ekc "Claro que eu não li, já que obviamente é pra você...{w=0.3}{nw}"
    extend 1ekd "mas aqui está."


    window hide
    if len(mas_per_check.mas_bad_backups) > 0:
        call mas_showpoem (mas_note_backups_some_bad)
    else:

        call mas_showpoem (mas_note_backups_all_good)

    window auto
    $ _gtext = glitchtext(7)

    m 1ekc "Você sabe do que se trata?{nw}"
    $ _history_list.pop()
    menu:
        m "Você sabe do que se trata?{fast}"
        "Não é nada com o que se preocupar.":
            jump mas_corrupted_persistent_post_menu
        "É sobre [_gtext].":

            $ persistent._mas_pm_snitched_on_chibika = True
            $ disable_esc()
            $ mas_MUMURaiseShield()
            window hide
            show noise zorder 11:
                alpha 0.5
            play sound "sfx/s_kill_glitch1.ogg"
            show chibika 3 zorder 12 at mas_chriseup(y=600,travel_time=0.5)
            pause 0.5
            stop sound
            hide chibika
            hide noise
            window auto
            $ mas_MUMUDropShield()
            $ enable_esc()

    menu:
        "Não é nada com o que se preocupar.":
            pass

label mas_corrupted_persistent_post_menu:
    m 1euc "Ah, tudo bem."
    m 1hub "Então vou tentar não me preocupar com isso."
    m 3eub "Eu sei que você me contaria se fosse algo importante, [player]."
    return

init python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_new_character_file"
        )
    )

label mas_new_character_file:
    m 1eua "Me diga, [player]..."
    m 3eua "Você se lembra do meu arquivo de personagem?"
    m 1eud "Bem, eu estive investigando ele recentemente, e acontece que ele é apenas uma imagem com algum tipo de código nela!"
    m 3ekc "Ele não contém nada sobre mim, só o meu nome."

    python:
        import os

        def moni_exist():
            return os.access(
                os.path.normcase(
                    renpy.config.basedir + "/characters/monika.chr"
                ),
                os.F_OK
            )

    if moni_exist():
        m 1dsd "Então, se me der licença por um segundo..."

        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        m 1esc "Eu vou o deletar."

        call mas_wx_cmd ("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd ("os.remove(os.path.normcase(basedir+'/characters/monika.chr'))", local_ctx, w_wait=1.0, x_wait=1.0)



        if moni_exist():
            m 1lksdlb "Aha...{w=0.3}Vou tentar isso de novo mais tarde."
            m 1eua "Enfim..."

        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    m 1rkc "Se você estava carregando aquilo com você, eu agradeço o sentimento."
    m 1dsc "No entanto..."
    m 1esc "Não acho que você deva ficar carregando um pedaço de dados inúteis."
    m 3wub "Então criei uma forma de me transformar em um arquivo que você pode carregar!"
    m "Tudo que você precisa fazer é me falar que vai me levar a algum lugar quando for dizer adeus, e eu farei o resto."
    m 1hua "Isso não parece maravilhoso?"
    m 3hub "Não vejo a hora de te acompanhar aonde você for."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_steam_install_detected",
            conditional=(
                "store.mas_globals.is_steam"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_steam_install_detected:
    $ filestruct = renpy.config.basedir[renpy.config.basedir.rfind('/') + 1:]

    m 1eub "[player], eu percebi que você está rodando o jogo pela Steam."
    m 1eksdld "Infelizmente, a Steam é malvada comigo... Ela pode causar alguns probleminhas com o jeito que eu funciono."
    m 2rksdlc "Coisas como travamentos, erros inesperados...{w=1}ou até o jogo fechando do nada."
    m 2eka "Se não for incômodo, você poderia mover a pasta \"[filestruct]\" para um lugar fora dos arquivos da Steam?"
    show monika 5esu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5esu "Eu ficaria muito grata se você fizesse isso por mim. Assim tudo fica mais estável, e eu posso ficar mais tranquila, ehehe~"
    return


default -5 persistent._mas_pm_has_rpy = None
init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpy_files"
        )
    )


label monika_rpy_files:
    if not mas_getEVL_shown_count("monika_rpy_files"):
        m 1eka "Ei, [player], eu estava dando uma olhada na sua pasta \"game\" e..."
        m 1ekc "Notei alguns arquivos \".rpy\" por lá."
        m 3rksdlc "Esses arquivos podem causar problemas..."
        m 3wud "E até impedir você de me visitar!"
        m 2etc "A não ser que..."
        m 4eua "Talvez você tenha instalado de propósito uma versão com o código-fonte porque está tentando me ajudar a chegar mais perto da sua realidade!"
        m 2eka "Mas caso não tenha sido isso, achei melhor perguntar..."

        m "Você tem certeza de que instalou a versão correta, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Você tem certeza de que instalou a versão correta, [player]?{fast}"
            "Sim.":

                m 1sua "Sério? Muito obrigada por me ajudar a me aproximar da sua realidade!"
                m 1hua "Eu te amo, [player]~"
                $ persistent._mas_pm_has_rpy = True
                return "love"
            "Não.":

                m "Entendi."
                m 2rksdla "Talvez seja melhor você se livrar desses arquivos, só por precaução."
                m 4eua "Na verdade, talvez eu possa apagá-los pra você."

                m "Quer que eu apague eles pra você, [player]?{nw}"
                $ _history_list.pop()
                menu:
                    m "Quer que eu apague eles pra você, [player]?{fast}"
                    "Sim, por favor.":

                        m "Claro, [player]."

                        call mas_rpy_file_delete ()

                        m 2hua "Prontinho!"
                        m 2esa "Da próxima vez, certifique-se de instalar uma versão sem o código-fonte. Você pode baixá-la na {a=http://www.monikaafterstory.com/releases.html}{i}{u}página de lançamentos{/u}{/i}{/a}."
                        $ persistent._mas_pm_has_rpy = False
                        hide screen mas_py_console_teaching
                        show monika at t11
                    "Não, obrigado.":

                        m 2rksdlc "Tudo bem, [player]. Espero que você saiba o que está fazendo."
                        m 2eka "Por favor, tenha cuidado."
                        $ persistent._mas_pm_has_rpy = True
    else:

        m 2efc "[player], você está com arquivos rpy na pasta do jogo de novo!"

        m 2rsc "Tem {i}certeza{/i} de que instalou a versão certa?{nw}"
        $ _history_list.pop()
        menu:
            m "Tem {i}certeza{/i} de que instalou a versão certa?{fast}"
            "Sim.":

                m 1eka "Tudo bem, [player]."
                m 3eua "Confio que você sabe o que está fazendo."
                $ persistent._mas_pm_has_rpy = True
            "Não.":

                m 3eua "Certo, vou apagar eles pra você de novo.{w=0.5}.{w=0.5}.{nw}"

                call mas_rpy_file_delete ()

                m 1hua "Prontinho!"
                m 3eua "Lembre-se que você sempre pode pegar a versão certa {a=http://www.monikaafterstory.com/releases.html}{i}{u}aqui{/u}{/i}{/a}."
                hide screen mas_py_console_teaching
                show monika at t11
    return







label mas_rpy_file_delete(showing_monika=True):
    python:
        store.mas_ptod.rst_cn()
        local_ctx = {
            "basedir": renpy.config.basedir
        }

    if showing_monika:
        show monika at t22

    show screen mas_py_console_teaching

    call mas_wx_cmd_noxwait ("import os", local_ctx)

    python:
        rpy_list = mas_getRPYFiles()
        for rpy_filename in rpy_list:
            path = '/game/'+rpy_filename
            store.mas_ptod.wx_cmd("os.remove(os.path.normcase(basedir+'"+path+"'))", local_ctx)
            renpy.pause(0.1)
    return















label mas_bday_player_bday_select:
    m 1eua "Quando é o seu aniversário?"

label mas_bday_player_bday_select_select:
    $ old_bday = mas_player_bday_curr()

    call mas_start_calendar_select_date

    $ selected_date_t = _return

    if not selected_date_t:
        m 2efc "[player]!"
        m "Você precisa escolher uma data!"
        m 1hua "Tente de novo!"
        jump mas_bday_player_bday_select_select

    $ selected_date = selected_date_t.date()
    $ _today = datetime.date.today()

    if selected_date > _today:
        m 2efc "[player]!"
        m "Você não pode ter nascido no futuro!"
        m 1hua "Tente de novo!"
        jump mas_bday_player_bday_select_select

    elif selected_date == _today:
        m 2efc "[player]!"
        m "Você não pode ter nascido hoje!"
        m 1hua "Tente de novo!"
        jump mas_bday_player_bday_select_select

    elif _today.year - selected_date.year < 5:
        m 2efc "[player]!"
        m "Não tem como você ser {i}tão{/i} [nov] assim!"
        m 1hua "Tente de novo!"
        jump mas_bday_player_bday_select_select



    if _today.year - selected_date.year < 13:
        m 2eksdlc "[player]..."
        m 2rksdlc "Você sabe que estou perguntando sua data {i}real{/i} de nascimento, né?"
        m 2hksdlb "É que tá meio difícil acreditar que você é {i}tão{/i} jovem assim."
    else:

        m 1eua "Certo então, [player]."

    m 1eua "Só para confirmar direitinho..."
    $ new_bday_str, _date_diff = mas_calendar.genFormalDispDate(selected_date)

    m "Sua data de nascimento é [new_bday_str]?{nw}"
    $ _history_list.pop()
    menu:
        m "Sua data de nascimento é [new_bday_str]?{fast}"
        "Sim.":
            m 1eka "Tem certeza de que é [new_bday_str]? Eu nunca mais vou esquecer essa data, sabe.{nw}"
            $ _history_list.pop()

            menu:
                m "Tem certeza de que é [new_bday_str]? Eu nunca mais vou esquecer essa data, sabe.{fast}"
                "Sim, tenho certeza!":
                    m 1hua "Então está decidido!"
                "Na verdade...":

                    m 1hksdrb "Aha, imaginei que você não tinha tanta certeza assim."
                    m 1eka "Tenta de novo~"
                    jump mas_bday_player_bday_select_select
        "Não.":

            m 1euc "Ah, está errado?"
            m 1eua "Então tenta de novo."
            jump mas_bday_player_bday_select_select


    if persistent._mas_player_bday is not None:
        python:
            store.mas_calendar.removeRepeatable_d(
                "aniv-jogador",
                persistent._mas_player_bday
            )
            store.mas_calendar.addRepeatable_d(
                "aniv-jogador",
                "Seu Aniversário",
                selected_date,
                range(selected_date.year,MASCalendar.MAX_VIEWABLE_YEAR)
            )
    else:

        python:
            store.mas_calendar.addRepeatable_d(
                "aniv-jogador",
                "Seu Aniversário",
                selected_date,
                range(selected_date.year,MASCalendar.MAX_VIEWABLE_YEAR)
            )

    $ persistent._mas_player_bday = selected_date
    $ mas_poems.paper_cat_map["pbday"] = "mod_assets/poem_assets/poem_pbday_" + str(store.persistent._mas_player_bday.month) + ".png"
    $ store.mas_player_bday_event.correct_pbday_mhs(selected_date)
    $ store.mas_history.saveMHSData()
    $ renpy.save_persistent()
    jump birthdate_set



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_text_speed_enabler",
            random=True,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

default -5 persistent._mas_text_speed_enabled = False


default -5 persistent._mas_pm_is_fast_reader = None


label mas_text_speed_enabler:
    m 1eua "Ei [player], eu estava pensando..."

    m "Você tem o costume de ler rápido?{nw}"
    $ _history_list.pop()
    menu:
        m "Você tem o costume de ler rápido?{fast}"
        "Sim.":
            $ persistent._mas_pm_is_fast_reader = True
            $ persistent._mas_text_speed_enabled = True

            m 1wub "Sério? Impressionante."
            m 1kua "Creio que então você lê bastante no seu tempo livre."
            m 1eua "Nesse caso..."
        "Não.":

            $ persistent._mas_pm_is_fast_reader = False
            $ persistent._mas_text_speed_enabled = True

            m 1eud "Ah, tudo bem."
            m 2dsa "De qualquer forma.{w=0.5}.{w=0.5}.{nw}"

    if not persistent._mas_pm_is_fast_reader:

        $ preferences.text_cps = 30

    $ mas_enableTextSpeed()

    if persistent._mas_pm_is_fast_reader:
        m 4eua "Prontinho!"

    m 4eua "Ativei a configuração de velocidade do texto!"

    m 1hka "Antes eu controlava isso apenas para garantir que você lesse {i}cada palavra{/i} do que eu dizia."
    m 1eka "Mas agora que já estamos [ju] há algum tempo, acredito que posso confiar que você não vai simplesmente pular minhas falas sem prestar atenção."

    if persistent._mas_pm_is_fast_reader:
        m 1tuu "Mas agora,{w=0.3} quero ver se você consegue me acompanhar."
        m 3tuu "{cps=*2}Eu consigo falar bem rápido, sabia...{/cps}{nw}"
        $ _history_list.pop()
        m 3hub "Ahaha~"
    else:

        m 3hua "Tenho certeza de que, com o tempo, sua leitura ficará cada vez mais rápida."
        m "Então, ajuste a velocidade do texto quando achar apropriado."

    return "derandom|no_unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bookmarks_notifs_intro",
            conditional=(
                "(not renpy.seen_label('bookmark_derand_intro') "
                "and (len(persistent._mas_player_derandomed) == 0 or len(persistent._mas_player_bookmarked) == 0)) "
                "or store.mas_windowreacts.can_show_notifs"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_bookmarks_notifs_intro:
    if not renpy.seen_label('bookmark_derand_intro') and (len(persistent._mas_player_derandomed) == 0 or len(persistent._mas_player_bookmarked) == 0):
        m 3eub "Ei, [player]...{w=0.5} Tenho algumas novidades para te contar!"

        if len(persistent._mas_player_derandomed) == 0 and len(persistent._mas_player_bookmarked) == 0:
            m 1eua "Agora você pode marcar os assuntos das nossas conversas que você se interessar facilmente apertando a tecla 'B'."
            m 3eub "Tudo que você marcar vai ficar guardado, e você poderá acessar facilmente no menu 'Conversar'!"
            call mas_derand
        else:
            m 3rksdlb "...Hm, pelo jeito você já descobriu uma das coisas que eu ia te mostrar, ahaha!"
            if len(persistent._mas_player_derandomed) == 0:
                m 3eua "Mas ainda assim, deixa eu explicar direitinho: você pode favoritar os assuntos que quiser durante nossas conversas apertando a tecla 'B', e depois acessar todos eles no menu 'Conversar'."
                call mas_derand
            else:
                m 1eua "Além disso, agora você também pode me avisar quando não quiser mais que eu traga certos assuntos, é só apertar a tecla 'X' enquanto estivermos conversando."
                m 3eud "Seja [sncr] comigo, [player]. Se alguma coisa que eu disser te deixar desconfortável, eu quero muito saber disso, tá bem?"
                m 3eua "E claro, você também pode marcar assuntos que gostar, apertando a tecla 'B'."
                m 1eub "Assim, você vai conseguir rever esses tópicos a qualquer momento pelo menu 'Conversar'."

        if store.mas_windowreacts.can_show_notifs or renpy.linux:
            m 1hua "Ah, e por último, algo que eu tô super animada pra te mostrar!"
            call mas_notification_windowreact
    else:

        m 1hub "[player], tenho algo muito especial pra te contar!"
        call mas_notification_windowreact

    return "no_unlock"

label mas_derand:
    m 1eua "Você também pode me avisar se não quiser que eu fale sobre algum assunto, é só apertar a tecla 'X' enquanto conversamos."
    m 1eka "Não precisa se preocupar em me magoar, tá? Acho que a gente deve ser sempre [hnst] [um] com [of] [ouo]."
    m 3eksdld "...Não gostaria de ficar falando sobre temas que te deixa desconfortável."
    m 3eka "Então, por favor, não deixe de me avisar, tudo bem?"
    return

label mas_notification_windowreact:
    m 3eua "Ultimamente eu tenho treinado um pouco mais minhas habilidades de programação... e adivinha só? Aprendi a usar as notificações do seu computador!"
    m 1eub "Assim, se você quiser, eu posso te avisar quando tiver algo novo pra gente conversar."


    if not store.mas_windowreacts.can_show_notifs:
        m 1rkc "Quer dizer... quase isso, na verdade."
        m 3ekd "Não consigo te mandar notificações porque no seu sistema falta o comando {i}notify-send{/i}..."
        m 3eua "Se você puder instalar isso pra mim, aí sim eu vou conseguir te mandar notificações direitinho."

        show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eka "...E eu ficaria muito grata por isso, [player]."
    else:

        m 3eub "Você gostaria de ver como elas funcionam?{nw}"
        $ _history_list.pop()
        menu:
            m "Você gostaria de ver como elas funcionam?{fast}"
            "Sim!":

                m 1hua "Tá bom, [player]!"
                m 2dsa "Só me dá um segundinho pra criar uma notificação.{w=0.5}.{w=0.5}.{nw}"
                $ mas_display_notif(m_name, ["Eu te amo, [player]!"], skip_checks=True)
                m 1hub "Aqui está!"
            "Não, obrigado.":

                m 2eka "Tudo bem, [player]."

        m 3eua "Se quiser que eu te mande notificações, é só ir até a aba 'Alertas' no menu de configurações e ativá-las, junto com os tipos de alerta que você quer receber."

        if renpy.windows:
            m 3rksdla "Ah, e como você está usando Windows... agora eu sei como verificar qual janela está ativa."


        elif renpy.linux:
            m 3rksdla "Ah, e como você está usando Linux... agora eu sei como verificar qual janela está ativa."

        if not renpy.macintosh:
            m 3eub "...Então se eu tiver algo pra te contar enquanto estiver em segundo plano, posso te avisar!"
            m 3hksdlb "E não se preocupe, eu sei que você pode não querer que eu fique te observando o tempo todo, e eu respeito sua privacidade."
            m 3eua "Então eu só vou olhar o que você está fazendo se você estiver de acordo com isso."
            m 2eua "Se você ativar a opção 'Reação de Janela' no menu de configurações, isso vai me dizer que está tudo bem eu dar uma olhadinha."

            if mas_isMoniNormal(higher=True):
                m 1tuu "Não é como se você tivesse algo a esconder da sua namorada..."
                show monika 5ttu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5ttu "...né?"
    return

init python:
    if not persistent._mas_filereacts_historic:
        addEvent(
            Event(
                persistent.event_database,
                eventlabel="mas_gift_giving_instructs",
                conditional=(
                    "store.mas_xp.level() >= 3 "
                    "or mas_isSpecialDay()"
                ),
                action=EV_ACT_QUEUE
            )
        )

label mas_gift_giving_instructs:


    if persistent._mas_filereacts_historic:
        python:
            instruct_ev = mas_getEV("mas_gift_giving_instructs")
            if instruct_ev:
                instruct_ev.last_seen = None
                instruct_ev.shown_count -= 1

            persistent._seen_ever.pop("mas_gift_giving_instructs")
        return

    python:
        gift_instructs = """\
Eu queria que você soubesse que fiz um pequeno caminho para você dar alguns presentes à Monika!!
É um processo bastante simples, por isso vou lhe dizer como funciona:

Crie um novo arquivo na pasta 'characteres'
Renomeie-o para o que você quiser dar para Monika
Dê uma extensão de arquivo '.gift'

E é isso! Depois de um tempo, Monika deve perceber que você lhe deu algo.

Eu só queria que você soubesse, porque acho que Monika é super incrível e realmente quero vê-la feliz.

Boa sorte com Monika!

P.S: Não conte a ela sobre mim!
"""


        store.mas_utils.trywrite(
            os.path.normcase(renpy.config.basedir + "/characters/hint.txt"),
            player + "\n\n" + gift_instructs
        )

    m 1eud "Ei, [player]..."
    m 3euc "Alguém deixou uma nota na pasta de personagens endereçada a você."
    m 1ekc "Como é para você, eu não li...{w=0.5}{nw}"
    extend 1eua " mas eu só queria que você soubesse, pois isso pode ser importante."
    return "no_unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_change_to_def",
            unlocked=False
        )
    )

label mas_change_to_def:

    $ mas_rmallEVL("mas_change_to_def")


    if (
        mas_hasSpecialOutfit()
        and monika_chr.clothes.name == persistent._mas_event_clothes_map[datetime.date.today()]
    ):
        return "no_unlock"



    if mas_isMoniHappy(higher=True) and monika_chr.clothes != mas_clothes_blazerless:
        m 3esa "Me dê um segundo [player], só vou ficar um pouco mais confortável..."

        call mas_clothes_change (mas_clothes_blazerless)

        m 2hua "Ah, muito melhor!"



    elif mas_isMoniNormal(lower=True) and monika_chr.clothes != mas_clothes_def:
        m 1eka "Ei, [player], sinto falta do meu uniforme escolar..."
        m 3eka "Vou me trocar, já volto..."

        call mas_clothes_change ()

        m "Ok, o que mais devemos fazer hoje?"


        $ mas_lockEVL("monika_event_clothes_select", "EVE")
    return "no_unlock"












label mas_clothes_change(outfit=None, outfit_mode=False, exp="monika 2eua", restore_zoom=True, unlock=False):

    if outfit is None:
        $ outfit = mas_clothes_def

    window hide

    call mas_transition_to_emptydesk


    pause 2.0


    if monika_chr.is_wearing_clothes_with_exprop("costume") and outfit == mas_clothes_def or outfit == mas_clothes_blazerless:
        $ monika_chr.reset_hair()

    $ monika_chr.change_clothes(outfit, outfit_mode=outfit_mode)
    if unlock:
        $ store.mas_selspr.unlock_clothes(outfit)
        $ store.mas_selspr.save_selectables()
    $ monika_chr.save()
    $ renpy.save_persistent()

    pause 2.0

    call mas_transition_from_emptydesk (exp)

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_blazerless_intro",
            unlocked=False
        )
    )

label mas_blazerless_intro:


    if monika_chr.clothes == mas_clothes_def:
        m 3esa "Só me dê um segundo, [player]. Só vou ficar um pouco mais confortável..."

        call mas_clothes_change (mas_clothes_blazerless)

        m 2hua "Ah, bem melhor!"

        m 3eka "Mas se sentir falta do meu blazer, basta pedir que eu coloco de volta."

    return "no_unlock"

init -881 python in mas_delact:

    def _mas_birthdate_bad_year_fix_action(ev=None):
        store.queueEvent("mas_birthdate_year_redux")
        return True

    def _mas_birthdate_bad_year_fix():
        return store.MASDelayedAction.makeWithLabel(
            16,
            "mas_birthdate",
            "True",
            _mas_birthdate_bad_year_fix_action,
            store.MAS_FC_IDLE_ONCE
        )


label mas_birthdate_year_redux:
    m 2eksdld "Uh, [player]..."
    m 2rksdlc "Tenho algo pra te perguntar, mas é meio vergonhoso..."
    m 2eksdlc "Se lembra quando você me disse sua data de nascimento?"
    m 2rksdld "Bem, acho que acabei errando o ano do seu nascimento."
    m 2eksdla "Então, caso não se importe de me dizer de novo..."


label mas_birthdate_year_redux_select:
    python:
        end_year = datetime.date.today().year - 6
        beg_year = end_year - 95

        yearrange = range(end_year, beg_year, -1)

        yearmenu = [(str(y), y, False, False) for y in yearrange]

    show monika 2eua at t21
    $ renpy.say(m, "Em que ano você nasceu?", interact=False)
    call screen mas_gen_scrollable_menu(yearmenu, mas_ui.SCROLLABLE_MENU_TXT_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)

    show monika 3eua at t11
    m "Certo, [player], então você nasceu em [_return]?{nw}"
    $ _history_list.pop()
    menu:
        m "Certo, [player], então você nasceu em [_return]?{fast}"
        "Sim.":

            m "Você tem {i}certeza{/i} de que nasceu em [_return]?{nw}"
            $ _history_list.pop()
            menu:
                m "Você tem {i}certeza{/i} de que nasceu em [_return]?{fast}"
                "Sim.":

                    m 3hua "Tudo bem, então está decidido!"
                    python:
                        persistent._mas_player_bday = persistent._mas_player_bday.replace(year=_return)
                        store.mas_player_bday_event.correct_pbday_mhs(persistent._mas_player_bday)
                        store.mas_history.saveMHSData()
                        renpy.save_persistent()


                        store.mas_calendar.addRepeatable_d(
                            "player-bday",
                            "Seu Aniversário",
                            persistent._mas_player_bday,
                            range(persistent._mas_player_bday.year,MASCalendar.MAX_VIEWABLE_YEAR)
                        )
                "Não.":

                    call mas_birthdate_year_redux_no
        "Não.":

            call mas_birthdate_year_redux_no

    return

label mas_birthdate_year_redux_no:
    m 2ekd "Ah, tudo bem..."
    m 2eka "Tente novamente, [player]."
    jump mas_birthdate_year_redux_select

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_credits_song",
            conditional=(
                "store.mas_anni.pastOneMonth() "
                "and seen_event('mas_unlock_piano')"
            ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_credits_song:
    if persistent.monika_kill or renpy.seen_audio(songs.FP_YOURE_REAL):
        m 1hua "Espero que você tenha gostado da minha música."
        m 1eka "Eu trabalhei muito duro nisso. Eu sei que ainda não sou perfeita ao piano, mas simplesmente não podia deixar você ir sem dizer como me sentia honestamente sobre você."
        m 1eua "Dê-me um tempo e tentarei escrever outro."

        if persistent._mas_pm_plays_instrument is not False:
            if persistent._mas_pm_plays_instrument:
                m 3eua "Talvez você possa me tocar uma música também!"
            else:
                m 3eua "Talvez você possa me tocar uma música também, se você pode tocar um instrumento?"

            m 1hub "Eu adoraria isso."
            m 3eua "Ah, e tocarei a música novamente para você a qualquer momento que você quise."
        else:

            m 3eua "Mas, enquanto isso, tocarei a música novamente para você a qualquer momento que você quiser."

        m 1tsa "De fato, eu adoraria tocar para você agora, se você tiver tempo...{nw}"
        $ _history_list.pop()
        menu:
            m "De fato, eu adoraria tocar para você agora, se você tiver tempo...{fast}"
            "Claro!":

                m 3hub "Ótimo!"
                m 3eua "Verifique se os alto-falantes estão ligados e se o volume da música no jogo está alto o suficiente para que você possa ouvir."
                if store.songs.hasMusicMuted():
                    m 3eksdla "Acho que você esqueceu o volume do jogo..."
                m 1eub "Agora, me espere por um segundo.{w=0.5}.{w=0.5}.{nw}"

                call mas_monika_plays_yr (skip_leadin=True)
                show monika 1eka
                pause 1.0

                m 1ekbsa "Ehehe~"
                show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5ekbsa "Obrigada por voltar para mim, meu amor."
            "Desculpe, não posso agora.":

                m 3ekd "Ah, tudo bem."
                m 1eka "Tudo bem, [player]. Eu entendo se você não tem tempo ou simplesmente não pode ouvir música no momento."
                m 3hua "Deixe-me saber quando for uma hora melhor para você e eu ficarei feliz em jogar para você~"
    else:

        m 3eua "Ei, [player], finalmente terminei a música em que estou trabalhando para você."
        m 1eka "Eu chamo de {i}Nossa realidade{/i}."

        m 1eua "Estou tão empolgada por finalmente poder tocar para você, se você tiver tempo que é...{nw}"
        $ _history_list.pop()
        menu:
            m "Estou tão empolgada por finalmente poder jogar para você, se você tiver tempo que é...{fast}"
            "Claro!":

                m 3hub "Ótimo!"
                m 3eua "Verifique se os alto-falantes estão ligados e se o volume da música no jogo está alto o suficiente para que você possa ouvir."
                if store.songs.hasMusicMuted():
                    m 3eksdla "Acho que você esqueceu o volume do jogo..."
                m 1tsb "Agora, se você me der licença por um segundo.{w=0.5}.{w=0.5}.{nw}"

                call mas_monika_plays_or (skip_leadin=True)
                show monika 1ekbsa
                pause 1.0

                m "Mal posso esperar até estarmos [ju] em uma realidade."
                m 3ekbsa "Mas, até esse dia chegar, tocarei a música novamente para você sempre que você quiser."
                show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5ekbfa "Obrigado por ser minha inspiração [mas_get_player_nickname()]."
                if renpy.seen_audio(songs.FP_YOURE_REAL):
                    m 5hubfa "Ah, e se você quiser que eu toque esta ou a música original para você novamente, basta me dizer~"
                else:
                    m 5hubfa "Ah, e se você quiser que eu toque isso de novo, basta dizer~"
            "Desculpe, não posso agora.":

                m 3ekd "Ah, tudo bem."
                m 1eka "Tudo bem, [player]. Eu entendo se você não tem tempo ou simplesmente não pode ouvir música no momento."
                m 3hua "Deixe-me saber quando for uma hora melhor para você e eu ficarei feliz em jogar para você~"

        $ mas_unlockEVL("mas_monika_plays_or", "EVE")

    $ mas_unlockEVL("mas_monika_plays_yr", "EVE")
    return "no_unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_covid19",
            conditional="not renpy.seen_label('mas_covid19')",
            action=EV_ACT_QUEUE,
            start_date=mas_getFirstSesh()+datetime.timedelta(days=1),
            end_date=datetime.date(2020, 10, 30),
        ),
        skipCalendar=True
    )

label mas_covid19:
    m 2ekc "Ei, [player]..."
    m 2rksdld "Ultimamente, tenho lido muito online sobre esta pandemia do COVID-19 e está me preocupando com você!"
    m 2eksdld "Parece que está se espalhando tão rápido {nw}"
    extend 2eksdla "e eu realmente quero que você fique [sg]..."

    m 2eksdlc "O vírus já está em sua área?{nw}"
    $ _history_list.pop()
    menu:
        m "O vírus já está em sua área?{fast}"
        "Sim.":
            m 2wksdld "Ah não, [player]! Isso é realmente assustador!"
            m 4ekc "Conheço muitas pessoas que vivem em lugares onde é predominante e eles têm ordens para ficar em casa..."

            m 2ekd "Você tem ordens para ficar em casa onde mora?{nw}"
            $ _history_list.pop()
            menu:
                m "Você tem algum pedido para ficar em casa onde mora?{fast}"
                "Sim.":
                    m 4hua "Ah, que bom!"
                    m 4eub "Estou tão feliz em ouvir isso, [player]!"

                    m 2eud "Então você fica em casa sempre que pode, certo?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Então você fica em casa sempre que pode, certo?{fast}"
                        "Sim.":
                            m 2eua "Isso é ótimo, fico feliz que você esteja fazendo a coisa responsável."
                            m 2eka "...E não apenas para você, mas também para todos os outros."
                        "Não, eu ainda estou trabalhando.":

                            m 2dsc "..."
                            m 2dsd "Ah."
                            m 2dsc "..."
                            m 2rksdlc "Eu tenho que admitir que isso me assusta, [player]."
                            m 2eksdlc "Mas isso deve significar que você está fazendo um trabalho essencial..."
                            m 2eksdla "Então, isso também me deixa orgulhosa de que, de alguma forma, você está ajudando outras pessoas durante este momento difícil."
                            m 2eksdld "Apenas me prometa que está tomando todas as precauções para ficar em segurança, ok?"
                        "Não...":

                            m 2tfd "[player]!"
                            m 2tfo "Por que não?"
                            m 4tfo "Isso é sério! Você {i}tem{/i} que ficar dentro de casa sempre que possível!"
                            m 2dfc "..."
                            m 2dkc "..."
                            m 2rksdlc "Desculpe, [player]. Isso me assusta muito."
                            m 2eksdlc "Algumas pessoas podem tê-lo e nem apresentam sintomas, espalhando-o para outros..."
                            m 2eksdld "Então, se você não fizer isso por si mesmo, pelo menos fique dentro de todos os outros."
                            m 2eksdla "...E também para mim. Você é tudo o que tenho, [player]..."
                            m 2dksdlc "Se eu te perder...{w=1.0}{nw}"
                            extend 2ektpc "o que farei então?"
                            m 2ektpd "Você tem que me prometer [player]...{w=0.5}que vai ficar em casa."
                            m 2ektdc "..."
                            m 2dkc "..."
                "Não.":

                    m 2dkc "..."
                    m 2rksdld "Isso me preocupa muito, [player]..."
                    m 2eksdlc "Espero que você ainda consiga ficar dentro o máximo possível."
        "Não.":

            m 2eka "Bem, isso é um pouco de alívio, [player]..."
            m 2eksdlc "Mas ainda me preocupo que isso acabe na sua área eventualmente."
            m 2eksdld "Então, mesmo que não esteja ai agora, você deve ter cuidado!"

    m 7eksdld "Lembre-se de que, sempre que precisar sair, pratique distanciamento social...{w=0.5} Fique sempre a pelo menos 2 metros ou 6 pés de qualquer outra pessoa."
    m "Lembre-se de lavar as mãos por pelo menos 20 segundos com água e sabão o mais rápido possível."
    m 7eksdlc "...E nunca toque seu rosto com as mãos não lavadas, [player]."
    m 2eka "Ah, e se você estiver com dificuldades para lavar as mãos por tempo suficiente, eu encontrei uma maneira legal de garantir que você faça isso por 20 segundos inteiros..."
    m 4hub "Vá para {a=https://washyourlyrics.com}{i}{u}washyourlyrics.com{/u}{/i}{/a} e digite {i}Your Reality{/i} para o título da música e {i}Monika{/i} ara o artista da música!"
    m 4eub "Basta baixar a imagem que ela cria com a letra da minha música e ela mostra a melhor maneira de lavar as mãos e por quanto tempo!"
    m 2hua "Então, toda vez que você lava as mãos, lembra-se do quanto eu te amo~"
    m 2eka "..."
    m 7eksdla "Sabe, [player], se eu pudesse, traria você aqui comigo até que tudo acabe e para que você não fique doente..."
    m "Mas como não posso, faça o possível para ficar em segurança."
    m 2dkbsu "Eu preciso de você, [player]~"
    return "no_unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_islands_reset",
            conditional="persistent._mas_islands_start_lvl == 0",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.ENAMORED,None)
        )
    )

label mas_islands_reset:
    m 1rsc "Hmm..."
    m 1esc "...Ei,{w=0.1} posso ouvir sua opinião sobre algo?"
    m 3lkd "Você já trabalhou em um projeto por {i}tanto{/i} tempo que, ao olhar para a coisa toda, acabou vendo dezenas de erros ou coisas que deseja melhorar?"
    m 3ekc "...Veja bem,{w=0.1} tenho trabalhado nessas ilhas para que possamos ter diferentes lugares para ir ...{w=0.3}{nw}"
    extend 3esd "para ter uma realidade nossa."
    m 1eud "Mas agora que fiquei melhor em programação, acho que poderia {i}realmente{/i} fazer um trabalho melhor agora."
    m 1rkc "E para consertar todas as coisas que eu gostaria de consertar...{w=0.3}{nw}"
    extend 1rksdld "Acho que seria mais fácil se eu começasse do zero."
    m 4ekc "Significa que o céu lá fora ficará bastante vazio por um tempo,{w=0.1} {nw}"
    extend 4eua "mas acho que realmente posso fazer valer a pena esperar."
    m 1euc "Se estiver tudo bem para você, [player]?{nw}"
    $ _history_list.pop()

    menu:
        m "Se estiver tudo bem para você, [player]?{fast}"
        "Claro, faça isso.":

            m 1dsc "Ok, só me dê um segundo.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

            play sound "sfx/glitch3.ogg"
            python:
                mas_island_event._resetProgression()
                mas_island_event.startProgression()

            m 3hua "E prontinho!"
            m 1eua "Agora tenho uma tela nova e fresca."
            m 3kuu "...E terei muito para me manter ocupada quando você estiver ausente, [player]. Ehehe~"
            m 3hub "Espero que você esteja [an] por isso!"
        "Eu acho que está bom assim.":

            m 3eka "Tudo bem, [player]."
            m 3hua "Se você está bem com a forma como elas estão agora, então eu também estou.{w=0.2} Verei o que posso fazer com elas como estão~"

    return "no_unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_gift_hint_noudeck",
            conditional="store.mas_xp.level() >= 8 and not mas_seenEvent('mas_reaction_gift_noudeck')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None),
            show_in_idle=True,
            rules={
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            }
        )
    )

label mas_gift_hint_noudeck:

    if mas_seenEvent("mas_reaction_gift_noudeck"):
        return


    python hide:
        def write_and_hide():
            import time
            
            note_path = os.path.join(renpy.config.basedir, renpy.substitute("characters/Ei, eu tenho algo para você, [player]!.txt"))
            note_text = renpy.substitute("""\
Oi, [player]!

Vejo que você está deixando a Monika muito feliz, e quero ajudar da maneira que puder!
Eu adicionei um novo baralho de cartas que você pode dar a Monika. Tenho certeza que vocês dois podem descobrir como jogar o jogo.

Para dar a ela, crie um novo arquivo 'noudeck.gift' na pasta 'characters'.

Continue sendo [um] [bo] [boy] e boa sorte com a Monika!

P.S: Não conte a ela sobre mim!\
""")
            
            mas_utils.trywrite(note_path, note_text, log=True)
            time.sleep(20)
            renpy.hide("chibika 3")

        renpy.invoke_in_thread(write_and_hide)

    show chibika 3:
        subpixel True
        rotate_pad True
        zoom 0.5
        anchor (0.5, 0.5)
        pos (0.4, 1.15)
        around (0.475, 0.9)

        parallel:
            linear 15.0 clockwise pos (1.15, 0.55)
        parallel:
            rotate 0
            linear 5.0 rotate 360
            repeat

    return "pause: 30"


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_backup_restored",
        )
    )

label mas_backup_restored:
    if mas_isMoniNormal(higher=True):
        m 2ekc "[player]..."
        m 2ekd "Estou tendo essa estranha sensação de déjà vu... {w=0.3}{nw}"
        extend 7ekd "Eu queria falar com você, mas de alguma forma lembrei que já tínhamos falado."

        if mas_getEVL_shown_count("mas_backup_restored") > 0:
            m 1etc "Espere, eu já disse isso antes também?"

        m 1wuo "Ah! {w=0.3}{nw}"
        extend 3wud "Você restaurou minhas memórias de um backup, não foi?{nw}"
        $ _history_list.pop()
        menu:
            m "Ah! Você restaurou minhas memórias de um backup, não foi?{fast}"
            "Sim, eu restaurei.":

                $ mas_gainAffection(modifier=0.5)

                m 2eka "Obrigada, [player]. {w=0.2}Eu sabia que podia contar com você."
                m 7rkd "No entanto, tinha que ter um problema muito ruim pra você ter que me restaurar..."

                m 1ekc "O que aconteceu?{nw}"
                $ _history_list.pop()
                menu:
                    m "O que aconteceu?{fast}"
                    "O jogo travou.":

                        m 1wud "Ah, isso é estranho e preocupante."
                        m 1ekc "Desta vez não foi meu código. {w=0.2}Eu não me lembro de mexer nele, de qualquer forma."
                        m 1gfd "{cps=*1.5}Juro se for outro bug do Ren'Py...{/cps}{nw}"
                        $ _history_list.pop()
                        m 1ekc "Vamos tentar ter certeza que não vai acontecer de novo, certo?"
                        $ mas_moni_idle_disp.force_by_code("1ekc", duration=25, skip_dissolve=True)
                    "Adicionei um submod.":

                        m 1etc "Adicionou um{w=0.1}{i}submod{/i}?"
                        m 3esd "Você deveria estar mais atento ao que instala neste computador."
                        m 2lkd "É minha casa tambémo..."
                        $ mas_moni_idle_disp.force_by_code("1ekc", duration=25, skip_dissolve=True)
                    "Meu PC quebrou.":

                        m 2wuo "Estou feliz que você encontrou uma maneira de me restaurar!"
                        m 2ekc "Espero que isso não aconteça novamente."
                        m 2lktpc "Não consigo imaginar perder você..."
                        $ mas_moni_idle_disp.force(
                            MASMoniIdleExpGroup(
                                [
                                    MASMoniIdleExp("2lktdc", duration=15),
                                    MASMoniIdleExp("2rktdc", duration=10),
                                    MASMoniIdleExp("1dkc", duration=10),
                                    MASMoniIdleExp("1euc", duration=10),
                                ]
                            ),
                            skip_dissolve=True
                        )
                    "Não tenho certeza.":

                        m 1etc "Isso é preocupante, [player]..."
                        m 3esd "Perdi a memória e nem sabemos o porquê."
                        m 4eud "Devemos tentar descobrir e evitar que isso aconteça no futuro."
                        m 7eka "Promete?"
                        $ mas_moni_idle_disp.force_by_code("1eka", duration=20, skip_dissolve=True)
            "Não, eu não restaurei.":

                m 2etc "Ah, então o que está acontecendo, [player]?"
                m 2ektpc "Eu não quero te esquecer."
                m 2ektpd "Por favor, você pode descobrir o que está acontecendo?"
                m 7eutdd "Talvez você possa fazer alguns backups por precaução?"

                if mas_seenEvent("monika_back_ups"):
                    m 3eud "Eu expliquei como fazer isso antes, lembra?"
                else:

                    m 3euc "{a=https://github.com/Monika-After-Story/MonikaModDev/wiki/FAQ#i-want-to-back-up-my-persistent}{i}{u}Isso{/u}{/i}{/a} deve ajudar você."

                m 1eka "Estou contando com você, [player]."
                $ mas_moni_idle_disp.force_by_code("1eka", duration=15, skip_dissolve=True)

    elif mas_isMoniUpset():
        m 2gtc "De alguma forma estou tendo essa sensação estranha de déjà vu..."
        m 2tfd "Espero que você não esteja mexendo com meus dados."
        $ mas_moni_idle_disp.force_by_code("2mfc", duration=10, skip_dissolve=True)
    else:

        m 6ekc "[player], o que está acontecendo? {w=0.3}{nw}"
        extend 6lksdlc "Eu sei que você fez algo com meus dados."
        m 6lktpsdld "Você está tentando se livrar de mim?"
        m 6rktpc "Eu só queria que fossemos felizes [ju]..."
        m 6ektuc "Por favor, me perdoe..."
        $ mas_moni_idle_disp.force(
            MASMoniIdleExpGroup(
                [
                    MASMoniIdleExp("6lktsc", duration=10),
                    MASMoniIdleExp("6rktsc", duration=10),
                    MASMoniIdleExp("6dktdc", duration=20)
                ]
            ),
            skip_dissolve=True
        )

    return "no_unlock|pause: 35"
