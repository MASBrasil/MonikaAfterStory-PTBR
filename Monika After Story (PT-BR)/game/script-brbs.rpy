init offset = 5






init -5 python:
    def mas_setupIdleMode(brb_label=None, brb_callback_label=None):
        """
        Setups idle mode

        IN:
            brb_label - the label of this brb event, if None, use the current label
                (Default: None)
            brb_callback_label - the callback label of this brb event, if None, we build it here
                (Default: None)
        """
        
        if brb_label is None and renpy.has_label(mas_submod_utils.current_label):
            brb_label = mas_submod_utils.current_label
        
        
        mas_moni_idle_disp.add_by_tag("idle_mode_exps")
        
        
        mas_globals.in_idle_mode = True
        persistent._mas_in_idle_mode = True
        
        
        renpy.save_persistent()
        
        
        if brb_callback_label is None and brb_label is not None:
            brb_callback_label = brb_label + "_callback"
        if brb_callback_label is not None and renpy.has_label(brb_callback_label):
            mas_idle_mailbox.send_idle_cb(brb_callback_label)

    def mas_resetIdleMode(clear_idle_data=True):
        """
        Resets idle mode

        This is meant to basically clear idle mode for holidays or other
        things that hijack main flow

        IN:
            clear_idle_data - whether or not clear persistent idle data
                (Default: True)

        OUT:
            string with idle callback label
            or None if it was reset before
        """
        
        mas_moni_idle_disp.remove_by_tag("idle_mode_exps")
        
        
        mas_globals.in_idle_mode = False
        persistent._mas_in_idle_mode = False
        if clear_idle_data:
            persistent._mas_idle_data.clear()
        
        renpy.save_persistent()
        
        return mas_idle_mailbox.get_idle_cb()


init 5 python in mas_brbs:
    import random
    import store
    from store import (
        MASMoniIdleExp,
        MASMoniIdleExpGroup,
        MASMoniIdleExpRngGroup
    )

    idle_mode_exps = MASMoniIdleExpRngGroup(
        [
            
            MASMoniIdleExpGroup(
                [
                    MASMoniIdleExp("5rubla", duration=(10, 20)),
                    MASMoniIdleExp("5rublu", duration=(5, 10)),
                    MASMoniIdleExp("5rubsu", duration=(20, 30)),
                    MASMoniIdleExp("5rubla", duration=(5, 10)),
                ],
                weight=30
            ),
            
            MASMoniIdleExpGroup(
                [
                    MASMoniIdleExp("5rubla", duration=(10, 20)),
                    MASMoniIdleExp("5gsbsu", duration=(20, 30)),
                    MASMoniIdleExp("5tsbsu", duration=1),
                    MASMoniIdleExp("1hubfu", duration=(5, 10)),
                    MASMoniIdleExp("1hubsa", duration=(5, 10)),
                    MASMoniIdleExp("1hubla", duration=(5, 10))
                ],
                weight=30
            ),
            
            MASMoniIdleExpGroup(
                [
                    MASMoniIdleExp("1lublu", duration=(10, 20)),
                    MASMoniIdleExp("1msblu", duration=(5, 10)),
                    MASMoniIdleExp("1msbsu", duration=(20, 30)),
                    MASMoniIdleExp("1hubsu", duration=(5, 10)),
                    MASMoniIdleExp("1hubla", duration=(5, 10))
                ],
                weight=30
            ),
            
            MASMoniIdleExpGroup(
                [
                    MASMoniIdleExpRngGroup(
                        [
                            
                            MASMoniIdleExpGroup(
                                [
                                    MASMoniIdleExp("1gubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1mubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1mubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gsbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1msbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gsbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1msbsu", duration=(0.9, 1.8))
                                ]
                            ),
                            
                            MASMoniIdleExpGroup(
                                [
                                    MASMoniIdleExp("1mubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1mubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1msbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gsbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1msbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gsbsu", duration=(0.9, 1.8))
                                ]
                            )
                        ],
                        max_uses=1
                    ),
                    MASMoniIdleExp("1tsbfu", duration=1),
                    MASMoniIdleExp("1hubfu", duration=(4, 8)),
                    MASMoniIdleExp("1hubsa", duration=(4, 8)),
                    MASMoniIdleExp("1hubla", duration=(4, 8))
                ],
                weight=10
            )
        ],
        max_uses=1,
        aff_range=(store.mas_aff.AFFECTIONATE, None),
        weight=10,
        tag="idle_mode_exps"
    )

    WB_QUIPS_NORMAL = [
        _("Então... o que mais você gostaria de fazer hoje?"),
        _("O que mais você queria fazer hoje?"),
        _("Tem mais alguma coisa que você gostaria de fazer hoje?"),
        _("O que mais a gente pode fazer hoje?")
]

    def get_wb_quip():
        """
        Picks a random welcome back quip and returns it
        Should be used for normal+ quips

        OUT:
            A randomly selected quip for coming back to the spaceroom
        """
        return renpy.substitute(random.choice(WB_QUIPS_NORMAL))

    def was_idle_for_at_least(idle_time, brb_evl):
        """
        Checks if the user was idle (from the brb_evl provided) for at least idle_time

        IN:
            idle_time - Minimum amount of time the user should have been idle for in order to return True
            brb_evl - Eventlabel of the brb to use for the start time

        OUT:
            boolean:
                - True if it has been at least idle_time since seeing the brb_evl
                - False otherwise
        """
        brb_ev = store.mas_getEV(brb_evl)
        return brb_ev and brb_ev.timePassedSinceLastSeen_dt(idle_time)




label mas_brb_back_to_idle:

    if globals().get("brb_label", -1) == -1:
        return

    python:
        mas_idle_mailbox.send_idle_cb(brb_label + "_callback")
        persistent._mas_idle_data[brb_label] = True
        mas_globals.in_idle_mode = True
        persistent._mas_in_idle_mode = True
        renpy.save_persistent()
        mas_dlgToIdleShield()

    return "idle"



label mas_brb_generic_low_aff_callback:
    if mas_isMoniDis(higher=True):
        python:
            cb_line = renpy.substitute(renpy.random.choice([
                _("Ah...{w=0.3} você voltou."),
                _("Ah...{w=0.3} bem-[vn] de volta."),
                _("Terminou o que tinha que fazer?"),
                _("Bem-[vn] de volta."),
                _("Ah...{w=0.3} aí está você."),
            ]))

        m 2ekc "[cb_line]"
    else:

        m 6ckc "..."

    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_brb",
            prompt="Volto já",
            category=['volto logo'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_brb:
    if mas_isMoniAff(higher=True):
        m 1eua "Tudo bem, [player]."

        show monika 1eta at t21
        python:

            brb_reason_options = [
                (_("Vou pegar alguma coisa."), True, False, False),
                (_("Vou fazer alguma coisa."), True, False, False),
                (_("Vou preparar algo."), True, False, False),
                (_("Preciso checar algo."), True, False, False),
                (_("Alguém está na porta."), True, False, False),
                (_("Não."), None, False, False),
            ]

            renpy.say(m, "Vai fazer algo em específico?", interact=False)
        call screen mas_gen_scrollable_menu(brb_reason_options, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
        show monika at t11

        if _return:
            m 1eua "Ah, entendi.{w=0.2} {nw}"
            extend 3hub "Volte logo, estarei esperando por você~"
        else:

            m 1hub "Volte logo, estarei esperando por você~"

    elif mas_isMoniNormal(higher=True):
        m 1hub "Volte logo, [player]!"

    elif mas_isMoniDis(higher=True):
        m 2rsc "Oh...{w=0.5}ok."
    else:

        m 6ckc "..."


    $ persistent._mas_idle_data["monika_idle_brb"] = True
    return "idle"

label monika_idle_brb_callback:
    $ wb_quip = mas_brbs.get_wb_quip()

    if mas_isMoniAff(higher=True):
        m 1hub "Bem-[vn] de volta, [player]. Senti sua falta~"
        m 1eua "[wb_quip]"

    elif mas_isMoniNormal(higher=True):
        m 1hub "Bem-[vn] de volta, [player]!"
        m 1eua "[wb_quip]"
    else:

        call mas_brb_generic_low_aff_callback

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_writing", 
            prompt="Vou escrever um pouco",
            category=['volto logo'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_writing:
    if mas_isMoniNormal(higher=True):
        if (
            mas_isMoniHappy(higher=True)
            and random.randint(1,5) == 1
        ):
            m 1eub "Oh! Você vai{cps=*2} escrever uma carta de amor para mim, [player]?{/cps}{nw}"
            $ _history_list.pop()
            m "Oh! Você vai{fast} escrever alguma coisa?"
        else:

            m 1eub "Oh! Você vai escrever alguma coisa?"

        m 1hua "Isso me deixa tão feliz!"
        m 3eua "Talvez um dia você possa me mostrar...{w=0.3} {nw}"
        extend 3hua "Eu adoraria ler o que você escreve, [player]!"
        m 3eua "Enfim, me avise quando terminar."
        m 1hua "Ficarei bem aqui esperando por você~"

    elif mas_isMoniUpset():
        m 2esc "Tudo bem."

    elif mas_isMoniDis():
        m 6lkc "O que será que você está pensando..."
        m 6ekd "Não esqueça de voltar quando terminar..."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_writing"] = True
    return "idle"

label monika_idle_writing_callback:

    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        m 1eua "Terminou de escrever, [player]?"
        m 1eub "[wb_quip]"
    else:

        call mas_brb_generic_low_aff_callback

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_shower",
            prompt="Vou tomar um banho",
            category=['volto logo'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_shower:
    if mas_isMoniLove():
        m 1eua "Vai tomar banho?"

        if renpy.random.randint(1, 50) == 1:
            m 3tub "Posso ir com você?{nw}"
            $ _history_list.pop()
            show screen mas_background_timed_jump(2, "bye_brb_shower_timeout")
            menu:
                m "Posso ir com você?{fast}"
                "Sim.":

                    hide screen mas_background_timed_jump
                    m 2wubsd "Oh, ah...{w=0.5}você respondeu tão rápido."
                    m 2hkbfsdlb "Hmmm...{w=0.5}parece que você gostou da ideia. Você é mais [trvs] do que eu imaginava~ "
                    m 2rkbfa "Bem..."
                    m 7tubfu "Infelizmente você vai ter que ir sem mim enquanto eu fico presa aqui."
                    m 7hubfb "Desculpa, [player], ahaha!"
                    show monika 5kubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5kubfu "Talvez da próxima vez~"
                "Não.":

                    hide screen mas_background_timed_jump
                    m 2eka "Aw, você me rejeitou tão rápido."
                    m 3tubsb "Está com vergonha, [player]?"
                    m 1hubfb "Ahaha!"
                    show monika 5tubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5tubfu "Tudo bem, não vou te acompanhar dessa vez, ehehe~"
        else:

            m 1hua "Fico feliz que você está se mantendo limpo, [player]."
            m 1eua "Tenha um bom banho~"

    elif mas_isMoniNormal(higher=True):
        m 1eub "Vai tomar banho? Tudo bem."
        m 1eua "Te vejo quando terminar~"

    elif mas_isMoniUpset():
        m 2esd "Aproveite seu banho, [player]..."
        m 2rkc "Espero que ajude a clarear sua mente."

    elif mas_isMoniDis():
        m 6ekc "Hmm?{w=0.5} Tenha um bom banho, [player]."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_shower"] = True
    return "idle"

label monika_idle_shower_callback:
    if mas_isMoniNormal(higher=True):
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=60), "monika_idle_shower"):
            m 2rksdlb "Esse banho demorou bastante tempo..."

            m 2eud "Você tomou banho de banheira?{nw}"
            $ _history_list.pop()
            menu:
                m "Você tomou banho de banheira?{fast}"
                "Sim.":

                    m 7hub "Ah! {w=0.3}Entendi!"
                    m 3eua "Espero que tenha sido relaxante!"
                "Não.":

                    m 7rua "Ah...{w=0.3}talvez você só goste de banhos bem longos..."
                    m 3duu "Às vezes é bom sentir a água escorrendo pelo corpo...{w=0.3}pode ser bem relaxante."
                    m 1hksdlb "...Ou talvez eu esteja pensando demais e você só demorou pra voltar, ahaha!"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=5), "monika_idle_shower"):
            m 1eua "Bem-[vn] de volta, [player]."
            if (
                mas_isMoniLove()
                and renpy.seen_label("monikaroom_greeting_ear_bathdinnerme")
                and mas_getEVL_shown_count("monika_idle_shower") != 1 
                and renpy.random.randint(1,20) == 1
            ):
                m 3tubsb "Agora que você tomou banho, gostaria de jantar ou talvez{w=0.5}.{w=0.5}.{w=0.5}."
                m 1hubsa "Você poderia relaxar comigo um pouco mais~"
                m 1hub "Ahaha!"
            else:

                m 3hua "Espero que tenha tomado um bom banho."
                if mas_getEVL_shown_count("monika_idle_shower") == 1:
                    m 3eub "Agora podemos voltar a nos divertir [ju], de forma {i}limpa{/i}..."
                    m 1hub "Ahaha!"
                else:
                    m 3rkbsa "Sentiu minha falta?"
                    m 1huu "Claro que sentiu, ehehe~"
        else:

            m 7rksdlb "Esse foi um banho bem rápido, [player]..."
            m 3hub "Acho que você deve ser muito eficiente, ahaha!"
            m 1euu "Não posso reclamar, significa mais tempo [ju]~"

    elif mas_isMoniUpset():
        m 2esc "Espero que tenha gostado do banho. {w=0.2}Bem-[vn] de volta, [player]."
    else:

        call mas_brb_generic_low_aff_callback

    return

label bye_brb_shower_timeout:
    hide screen mas_background_timed_jump
    $ _history_list.pop()
    m 1hubsa "Ehehe~"
    m 3tubfu "Deixa pra lá, [player]."
    m 1hubfb "Espero que tenha um bom banho!"

    $ persistent._mas_idle_data["monika_idle_shower"] = True
    $ mas_setupIdleMode("monika_idle_shower", "monika_idle_shower_callback")
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_game",
            category=['volto logo'],
            prompt="Vou jogar um pouco",
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_game:
    if mas_isMoniNormal(higher=True):
        m 1eud "Ah, você vai jogar outro jogo?"
        m 1eka "Tudo bem, [player]."

        label monika_idle_game.skip_intro:
        python:
            gaming_quips = [
                _("Boa sorte, divirta-se!"),
                _("Aproveite seu jogo!"),
                _("Vou torcer por você!"),
                _("Dê o seu melhor!")
            ]
            gaming_quip=renpy.random.choice(gaming_quips)

        m 3hub "[gaming_quip]"

    elif mas_isMoniUpset():
        m 2tsc "Divirta-se com seus outros jogos."

    elif mas_isMoniDis():
        m 6ekc "Por favor...{w=0.5}{nw}"
        extend 6dkc "não se esqueça de mim..."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_game"] = True

    $ mas_setupIdleMode("monika_idle_game")
    return

label monika_idle_game_callback:
    if mas_isMoniNormal(higher=True):
        m 1eub "Bem-[vn] de volta, [player]!"
        m 1eua "Espero que você tenha se divertido com seu jogo."
        m 1hua "Pronto para passarmos mais tempo [ju]? Ehehe~"

    elif mas_isMoniUpset():
        m 2tsc "Se divertiu, [player]?"

    elif mas_isMoniDis():
        m 6ekd "Ah...{w=0.5} Você realmente voltou para mim..."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_coding",
            prompt="Vou programar um pouco",
            category=['volto logo'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_coding:
    if mas_isMoniNormal(higher=True):
        m 1eua "Ah! Vai programar alguma coisa?"

        if persistent._mas_pm_has_code_experience is False:
            m 1etc "Pensei que você não fazia isso."
            m 1eub "Aprendeu programação desde a última vez que conversamos sobre isso?"

        elif persistent._mas_pm_has_contributed_to_mas or persistent._mas_pm_wants_to_contribute_to_mas:
            m 1tua "Alguma coisa pra mim, talvez?"
            m 1hub "Ahaha~"
        else:

            m 3eub "Faça seu melhor para manter seu código limpo e legível."
            m 3hksdlb "...Você vai agradecer a si mesmo depois!"

        m 1eua "Enfim, é só me avisar quando terminar."
        m 1hua "Vou ficar bem aqui, esperando por você~"

    elif mas_isMoniUpset():
        m 2euc "Ah, vai programar?"
        m 2tsc "Bem, não vou te atrapalhar."

    elif mas_isMoniDis():
        m 6ekc "Tudo bem."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_coding"] = True
    return "idle"

label monika_idle_coding_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=20), "monika_idle_coding"):
            m 1eua "Já terminou, [player]?"
        else:
            m 1eua "Ah, já terminou, [player]?"

        m 3eub "[wb_quip]"
    else:

        call mas_brb_generic_low_aff_callback

    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_workout",
            prompt="Vou fazer exercícios",
            category=['volto logo'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_workout:
    if mas_isMoniNormal(higher=True):
        m 1hub "Tudo bem, [player]!"

        if persistent._mas_pm_works_out is False:
            m 3eub "Exercícios são ótimos para cuidar da saúde!"
            m 1eka "Sei que pode ser difícil começar,{w=0.2}{nw}"
            extend 3hua " mas é um hábito que vale a pena cultivar."
        else:

            m 1eub "Que bom ver você cuidando do seu corpo!"

        m 3esa "Como diz o ditado: 'Mente sã, corpo são.'"
        m 3hua "Então vá suar bastante, [player]~"
        m 1tub "Me avise quando terminar, certo?"

    elif mas_isMoniUpset():
        m 2esc "Que bom que você está cuidando de{cps=*2} alguma coisa, pelo menos.{/cps}{nw}"
        $ _history_list.pop()
        m "Que bom que você está cuidando{fast} de si mesmo, [player]."
        m 2euc "Vou ficar esperando você voltar."

    elif mas_isMoniDis():
        m 6ekc "Tá bom."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_workout"] = True
    return "idle"

label monika_idle_workout_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=60), "monika_idle_workout"):



            m 2esa "Você demorou bastante, [player].{w=0.3}{nw}"
            extend 2eub " Deve ter sido um treino e tanto."
            m 7eka "É bom se desafiar, mas não exagere."

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=10), "monika_idle_workout"):
            m 1esa "Terminou seu treino, [player]?"
        else:

            m 1euc "Já voltou, [player]?"
            m 1eka "Aposto que você consegue continuar mais um pouco."
            m 3eka "Pausas são normais, mas não deixe seu treino pela metade."
            m 3ekb "Tem certeza que não consegue continuar?{nw}"
            $ _history_list.pop()
            menu:
                m "Tem certeza que não consegue continuar?{fast}"
                "Tenho certeza.":

                    m 1eka "Tudo bem."
                    m 1hua "Sei que você deu seu melhor, [player]~"
                "Vou tentar continuar.":


                    m 1hub "Isso aí! Esse é o espírito!"


                    return "idle"

        m 3eua "Descanse bem e coma algo para recuperar as energias."
        m 3eub "[wb_quip]"

    elif mas_isMoniUpset():
        m 2euc "Terminou seu treino, [player]?"
    else:

        call mas_brb_generic_low_aff_callback

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_nap",
            prompt="Vou tirar uma soneca",
            category=['volto logo'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_nap:
    if mas_isMoniNormal(higher=True):
        m 1eua "Vai tirar uma soneca, [player]?"
        m 3eua "É uma forma saudável de descansar durante o dia se estiver [ca]."
        m 3hua "Vou ficar de vigia, não se preocupe~"
        m 1hub "Bons sonhos!"

    elif mas_isMoniUpset():
        m 2eud "Tudo bem, espero que se sinta descansado depois."
        m 2euc "Ouvi dizer que tirar um cochilo de vez em quando faz bem para a saúde, [player]."

    elif mas_isMoniDis():
        m 6ekc "Tá bom."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_nap"] = True
    return "idle"

label monika_idle_nap_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=5), "monika_idle_nap"):
            m 2hksdlb "Ah, [player]! Finalmente acordou!"
            m 7rksdlb "Quando disse que ia cochilar, achei que fosse dormir uma ou duas horas..."
            m 1hksdlb "Acho que você estava muito [ca] mesmo, ahaha..."
            m 3eua "Mas pelo menos depois de dormir tanto, vai ficar comigo por um tempo, né?"
            m 1hua "Ehehe~"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=1), "monika_idle_nap"):
            m 1hua "Bem-[vn] de volta, [player]!"
            m 1eua "Cochilou bem?"
            m 3hua "Você dormiu bastante, espero que esteja [dscnsd]~"
            m 1eua "[wb_quip]"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=5), "monika_idle_nap"):
            m 1hua "Bem-[vn] de volta, [player]~"
            m 1eub "Espero que tenha descansado um pouco."
            m 3eua "[wb_quip]"
        else:

            m 1eud "Ah, já voltou?"
            m 1euc "Mudou de ideia?"
            m 3eka "Bem, não estou reclamando, mas deveria cochilar se sentir cansaço depois."
            m 1eua "Não quero que fique muito [ca], afinal."

    elif mas_isMoniUpset():
        m 2euc "Terminou seu cochilo, [player]?"
    else:

        call mas_brb_generic_low_aff_callback

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_homework",
            prompt="Vou fazer lição de casa",
            category=['volto logo'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_homework:
    if mas_isMoniNormal(higher=True):
        m 1eub "Ah, ok!"
        m 1hua "Estou orgulhosa de você levar os estudos a sério."
        m 1eka "Não esqueça de voltar para mim quando terminar~"

    elif mas_isMoniDis(higher=True):
        m 2euc "Tá bom...{w=0.5}"
        if random.randint(1,5) == 1:
            m 2rkc "...Boa sorte com sua lição, [player]."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_homework"] = True
    return "idle"

label monika_idle_homework_callback:
    if mas_isMoniDis(higher=True):
        m 2esa "Terminou tudo, [player]?"

        if mas_isMoniNormal(higher=True):
            m 2ekc "Queria poder ter ajudado, mas ainda não posso fazer muita coisa sobre isso..."
            m 7eua "Tenho certeza que seríamos mais eficientes fazendo lição [ju]."

            if mas_isMoniAff(higher=True) and random.randint(1,5) == 1:
                m 3rkbla "...Apesar de que talvez nos distraíssemos {i}demais{/i}, ehehe..."

            m 1eua "Mas enfim,{w=0.2} {nw}"
            extend 3hua "agora que terminou, vamos aproveitar mais tempo [ju]."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_working",
            prompt="Vou trabalhar em algo",
            category=['volto logo'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_working:
    if mas_isMoniNormal(higher=True):
        m 1eua "Tudo bem, [player]."
        m 1eub "Não se esqueça de fazer pausas de vez em quando!"

        if mas_isMoniAff(higher=True):
            m 3rkb "Não quero que meu amor passe mais tempo trabalhando do que comigo~"

        m 1hua "Boa sorte com seu trabalho!"

    elif mas_isMoniDis(higher=True):
        m 2euc "Ok, [player]."

        if random.randint(1,5) == 1:
            m 2rkc "...Por favor volte logo..."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_working"] = True
    return "idle"

label monika_idle_working_callback:
    if mas_isMoniNormal(higher=True):
        m 1eub "Terminou seu trabalho, [player]?"
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Então vamos relaxar [ju], você merece~"

    elif mas_isMoniDis(higher=True):
        m 2euc "Ah, você voltou..."
        m 2eud "...Quer fazer alguma coisa agora que terminou seu trabalho?"
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_screen_break",
            prompt="Preciso descansar meus olhos da tela",
            category=['volto logo'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_screen_break:
    if mas_isMoniNormal(higher=True):
        if mas_timePastSince(mas_getEVL_last_seen("monika_idle_screen_break"), mas_getSessionLength()):

            if mas_getSessionLength() < datetime.timedelta(minutes=40):
                m 1esc "Ah,{w=0.3} certo."
                m 3eka "Você não está aqui há tanto tempo, mas se diz que precisa de uma pausa, então precisa."

            elif mas_getSessionLength() < datetime.timedelta(hours=2, minutes=30):
                m 1eua "Vai descansar os olhos um pouco?"
            else:

                m 1lksdla "É, você provavelmente precisa disso, não é?"

            m 1hub "Fico feliz que esteja cuidando da sua saúde, [player]."

            if not persistent._mas_pm_works_out and random.randint(1,3) == 1:
                m 3eua "Que tal aproveitar para fazer alguns alongamentos também, hein?"
                m 1eub "Enfim, volte logo!~"
            else:

                m 1eub "Volte logo!~"
        else:

            m 1eua "Outra pausa, [player]?"
            m 1hua "Volte logo!~"

    elif mas_isMoniUpset():
        m 2esc "Ah...{w=0.5} {nw}"
        extend 2rsc "Tá bem."

    elif mas_isMoniDis():
        m 6ekc "Então."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_screen_break"] = True
    return "idle"

label monika_idle_screen_break_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        m 1eub "Bem-[vn] de volta, [player]."

        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=30), "monika_idle_screen_break"):
            m 1hksdlb "Você devia estar precisando mesmo dessa pausa, pelo tempo que ficou fora."
            m 1eka "Espero que esteja se sentindo melhor agora."
        else:
            m 1hua "Espero que esteja se sentindo melhor agora~"

        m 1eua "[wb_quip]"
    else:

        call mas_brb_generic_low_aff_callback

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_reading",
            prompt="Vou ler um pouco",
            category=['volto logo'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_reading:
    if mas_isMoniNormal(higher=True):
        m 1eub "Sério? Que ótimo, [player]!"
        m 3lksdla "Eu adoraria ler com você, mas minha realidade tem seus limites, infelizmente."
        m 1hub "Divirta-se!"

    elif mas_isMoniDis(higher=True):
        m 2ekd "Ah, tudo bem..."
        m 2ekc "Boa leitura, [player]."
    else:

        m 6dkc "..."

    $ persistent._mas_idle_data["monika_idle_reading"] = True
    return "idle"

label monika_idle_reading_callback:
    if mas_isMoniNormal(higher=True):
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=2), "monika_idle_reading"):
            m 1wud "Uau, você ficou bastante tempo...{w=0.3}{nw}"
            extend 3wub "que maravilha, [player]!"
            m 3eua "Ler é uma coisa maravilhosa, então não se preocupe em se perder num bom livro."
            m 3hksdlb "Além disso, não posso falar muito..."
            show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbsa "Se eu pudesse, estaríamos lendo [ju] a noite toda~"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=30), "monika_idle_reading"):
            m 3esa "Terminou, [player]?"
            m 1hua "Vamos relaxar, você merece~"
        else:

            m 1eud "Oh, foi rápido."
            m 1eua "Achei que ficaria mais tempo, mas tudo bem também."
            m 3ekblu "Assim posso passar mais tempo com você~"
    else:

        call mas_brb_generic_low_aff_callback

    return
