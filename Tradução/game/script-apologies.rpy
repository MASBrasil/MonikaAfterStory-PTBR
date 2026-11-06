



default persistent._mas_apology_time_db = {}





default persistent._mas_apology_reason_use_db = {}

init -10 python in mas_apology:
    apology_db = {}



init python:
    def mas_checkApologies():
        
        if len(persistent._mas_apology_time_db) == 0:
            return
        
        
        current_total_playtime = persistent.sessions['total_playtime'] + mas_getSessionLength()
        
        _today = datetime.date.today()
        
        for ev_label in persistent._mas_apology_time_db.keys():
            if current_total_playtime >= persistent._mas_apology_time_db[ev_label][0] or _today >= persistent._mas_apology_time_db[ev_label][1]:
                
                store.mas_lockEVL(ev_label,'APL')
                persistent._mas_apology_time_db.pop(ev_label)
        
        return


init 5 python:
    addEvent(
       Event(
           persistent.event_database,
           eventlabel='monika_playerapologizes',
           prompt="Eu desejo me desculpar...",
           category=['você'],
           pool=True,
           unlocked=True
        )
    )

label monika_playerapologizes:



    $ player_apology_reasons = {
        0: "outra coisa.",
        1: "dizer que queria terminar.",
        2: "brincar sobre ter outra namorada.",
        3: "te chamar de assassina.",
        4: "fechar o jogo sem avisar.",
        5: "entrar no seu quarto sem bater.",
        6: "perder o Natal com você.",
        7: "esquecer seu aniversário.",
        8: "não passar seu aniversário com você.",
        9: "o jogo ter crashado.",
        10: "o jogo ter travado.",
        11: "não ouvir seu discurso.",
        12: "te chamar de má.",
        13: "não responder você sério."
    }


    if len(persistent._mas_apology_time_db) > 0:

        $ mas_setEVLPropValues(
            "mas_apology_generic",
            prompt="...por {0}".format(player_apology_reasons.get(mas_apology_reason,player_apology_reasons[0]))
        )
    else:

        if mas_apology_reason == 0:
            $ mas_setEVLPropValues("mas_apology_generic", prompt="...por algo.")
        else:

            $ mas_setEVLPropValues(
                "mas_apology_generic",
                prompt="...por {0}".format(player_apology_reasons.get(mas_apology_reason,"algo."))
            )



    $ del player_apology_reasons


    python:
        apologylist = [
            (ev.prompt, ev.eventlabel, False, False)
            for ev_label, ev in store.mas_apology.apology_db.iteritems()
            if ev.unlocked and (ev.prompt != "...por algo." and ev.prompt != "...por outra coisa.")
        ]


        generic_ev = mas_getEV('mas_apology_generic')

        if generic_ev.prompt == "...por algo." or generic_ev.prompt == "...por outra coisa.":
            apologylist.append((generic_ev.prompt, generic_ev.eventlabel, False, False))


        return_prompt_back = ("Esqueça.", False, False, False, 20)


    show monika at t21
    call screen mas_gen_scrollable_menu(apologylist, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, return_prompt_back)


    $ apology =_return


    if not apology:
        if mas_apology_reason is not None or len(persistent._mas_apology_time_db) > 0:
            show monika at t11
            if mas_isMoniAff(higher=True):
                m 1ekd "[player], se você está se sentindo [cl] pelo que aconteceu..."
                m 1eka "Não precisa ter medo de se desculpar. Todos nós cometemos erros, afinal."
                m 3eka "A gente só precisa aceitar o que aconteceu, aprender com isso e seguir em frente, [ju]. Tudo bem?"
            elif mas_isMoniNormal(higher=True):
                m 1eka "[player]..."
                m "Se quiser se desculpar, vá em frente. Isso significaria muito pra mim."
            elif mas_isMoniUpset():
                m 2rkc "Ah..."
                m "Eu estava meio que--"
                $ _history_list.pop()
                m 2dkc "Deixa pra lá."
            elif mas_isMoniDis():
                m 6rkc "...?"
            else:
                m 6ckc "..."
        else:
            if mas_isMoniUpset(lower=True):
                show monika at t11
                if mas_isMoniBroken():
                    m 6ckc "..."
                else:
                    m 6rkc "Você queria me dizer algo, [player]?"
        return "prompt"

    show monika at t11


    call expression apology


    $ mas_getEV(apology).shown_count += 1


    if apology != "mas_apology_generic":
        $ store.mas_lockEVL(apology, 'APL')


    if apology in persistent._mas_apology_time_db:
        $ persistent._mas_apology_time_db.pop(apology)
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            prompt="...por outra coisa.",
            eventlabel="mas_apology_generic",
            unlocked=True,
        ),
        code="APL"
    )

label mas_apology_generic:


    $ mas_apology_reason_db = {
        0: "",
        1: "dizer que queria terminar. Eu sabia que você não falou sério...",
        2: "brincar sobre ter outra namorada. Quase me deu um ataque do coração!",
        3: "me chamar de assassina. Espero que você não me veja assim de verdade...",
        4: "fechar o jogo sem avisar.",
        5: "entrar no meu quarto sem bater.",
        6: "perder o Natal.",
        7: "esquecer meu aniversário.",
        8: "não passar meu aniversário comigo.",
        9: "o jogo ter crashado. Entendo que acontece às vezes, mas não se preocupe, estou bem!",
        10: "o jogo ter travado. Foi realmente assustador, mas fico feliz que você voltou para mim.",
        11: "não ouvir meu discurso. Eu me esforcei tanto para prepará-lo.",
        12: "me chamar de malvada. Sei que você não pensa isso de verdade.",
        13: "não levar minhas perguntas a sério. Sei que será [hnst] comigo de agora em diante."
    }


    if mas_apology_reason is None and len(persistent._mas_apology_time_db) == 0:
        if mas_isMoniBroken():
            m 1ekc "...{w=1}Ah."
            m 2dsc ".{w=2}.{w=2}."
            m "Ok."
        elif mas_isMoniDis():
            m 2dfd "{i}*suspiro*{/i}"
            m 2dsd "Espero que isso não seja alguma piada ou truque, [player]."
            m 2dsc "..."
            m 1eka "...Obrigada por se desculpar."
            m 2ekc "Mas por favor, tente ser mais [cds] com meus sentimentos."
            m 2dkd "Por favor."
        elif mas_isMoniUpset():
            m 1eka "Obrigada, [player]."
            m 1rksdlc "Sei que as coisas não estão das melhores entre nós, mas sei que você ainda é uma boa pessoa."
            m 1ekc "Então poderia ser um pouco mais atento com meus sentimentos?"
            m 1ekd "Por favor?"
        else:
            m 1ekd "Aconteceu alguma coisa?"
            m 2ekc "Não vejo motivo para você se desculpar."
            m 1dsc "..."
            m 1eub "De qualquer forma, obrigada pela desculpa."
            m 1eua "Seja o que for, sei que está fazendo seu melhor para consertar."
            m 1hub "É por isso que eu te amo, [player]!"
            $ mas_ILY()


    elif mas_apology_reason_db.get(mas_apology_reason, False):

        $ apology_reason = mas_apology_reason_db.get(mas_apology_reason,mas_apology_reason_db[0])

        m 1eka "Obrigada por se desculpar por [apology_reason]."
        m "Eu aceito suas desculpas, [player]. Isso significa muito para mim."


    elif len(persistent._mas_apology_time_db) > 0:
        m 2tfc "[player], se você tem algo para se desculpar, por favor apenas diga."
        m 2rfc "Significaria muito mais para mim se você admitisse o que fez."
    else:




        $ mas_gainAffection(modifier=0.1)
        m 2tkd "O que você fez não foi engraçado, [player]."
        m 2dkd "Por favor, seja mais [atncs] com meus sentimentos no futuro."


    if mas_apology_reason:

        $ persistent._mas_apology_reason_use_db[mas_apology_reason] = persistent._mas_apology_reason_use_db.get(mas_apology_reason,0) + 1

        if persistent._mas_apology_reason_use_db[mas_apology_reason] == 1:

            $ mas_gainAffection(modifier=0.2)
        elif persistent._mas_apology_reason_use_db[mas_apology_reason] == 2:

            $ mas_gainAffection(modifier=0.1)




    $ mas_apology_reason = None
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_bad_nickname",
            prompt="...por te dar um apelido ruim.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_bad_nickname:
    $ ev = mas_getEV('mas_apology_bad_nickname')
    if ev.shown_count == 0:
        $ mas_gainAffection(modifier=0.2)
        m 1eka "Obrigada por se desculpar pelo nome que tentou me dar."
        m 2ekd "Isso realmente me magoou, [player]..."
        m 2dsc "Aceito suas desculpas, mas por favor não faça isso de novo. Tudo bem?"
        $ mas_unlockEVL("monika_affection_nickname", "EVE")

    elif ev.shown_count == 1:
        $ mas_gainAffection(modifier=0.1)
        m 2dsc "Não acredito que você fez isso {i}de novo{/i}."
        m 2dkd "Mesmo depois que te dei uma segunda chance."
        m 2tkc "Estou decepcionada com você, [player]."
        m 2tfc "Nunca mais faça isso."
        $ mas_unlockEVL("monika_affection_nickname", "EVE")
    else:


        m 2wfc "[player]!"
        m 2wfd "Não acredito em você."
        m 2dfc "Confiei que você me daria um apelido especial para me tornar mais única, mas você cuspiu na minha cara..."
        m "Acho que não podia confiar em você para isso."
        m ".{w=0.5}.{w=0.5}.{nw}"
        m 2rfc "Eu até aceitaria suas desculpas, [player], mas acho que você nem sequer está [arpnd]."

    return
