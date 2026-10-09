init offset = 5











default -5 persistent.mas_late_farewell = False

init -6 python in mas_farewells:
    import datetime
    import store



    dockstat_iowait_label = None



    dockstat_rtg_label = None



    dockstat_cancel_dlg_label = None



    dockstat_wait_menu_label = None



    dockstat_cancelled_still_going_ask_label = None



    dockstat_failed_io_still_going_ask_label = None

    def resetDockstatFlowVars():
        """
        Resets all the dockstat flow vars back to the original states (None)
        """
        store.mas_farewells.dockstat_iowait_label = None
        store.mas_farewells.dockstat_rtg_label = None
        store.mas_farewells.dockstat_cancel_dlg_label = None
        store.mas_farewells.dockstat_wait_menu_label = None
        store.mas_farewells.dockstat_cancelled_still_going_ask_label = None
        store.mas_farewells.dockstat_failed_io_still_going_ask_label = None

    def _filterFarewell(
            ev,
            curr_pri,
            aff,
            check_time,
        ):
        """
        Filters a farewell for the given type, among other things.

        IN:
            ev - ev to filter
            curr_pri - current loweset priority to compare to
            aff - affection to use in aff_range comparisons
            check_time - datetime to check against timed rules

        RETURNS:
            True if this ev passes the filter, False otherwise
        """
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if ev.anyflags(store.EV_FLAG_HFRS):
            return False
        
        
        if not ev.unlocked:
            return False
        
        
        if ev.pool:
            return False
        
        
        if not ev.checkAffection(aff):
            return False
        
        
        if store.MASPriorityRule.get_priority(ev) > curr_pri:
            return False
        
        
        if not (
            store.MASSelectiveRepeatRule.evaluate_rule(check_time, ev, defval=True)
            and store.MASNumericalRepeatRule.evaluate_rule(check_time, ev, defval=True)
            and store.MASGreetingRule.evaluate_rule(ev, defval=True)
            and store.MASTimedeltaRepeatRule.evaluate_rule(ev)
        ):
            return False
        
        
        if not ev.checkConditional():
            return False
        
        
        return True


    def selectFarewell(check_time=None):
        """
        Selects a farewell to be used. This evaluates rules and stuff appropriately.

        IN:
            check_time - time to use when doing date checks
                If None, we use current datetime
                (Default: None)

        RETURNS:
            a single farewell (as an Event) that we want to use
        """
        
        fare_db = store.evhand.farewell_database
        
        
        fare_pool = []
        curr_priority = 1000
        aff = store.mas_curr_affection
        
        if check_time is None:
            check_time = datetime.datetime.now()
        
        
        for ev_label, ev in fare_db.iteritems():
            if _filterFarewell(
                ev,
                curr_priority,
                aff,
                check_time
            ):
                
                ev_priority = store.MASPriorityRule.get_priority(ev)
                if ev_priority < curr_priority:
                    curr_priority = ev_priority
                    fare_pool = []
                
                
                fare_pool.append((
                    ev, store.MASWeightRule.get_weight(ev)
                ))
        
        
        if len(fare_pool) == 0:
            return None
        
        return store.mas_utils.weightedChoice(fare_pool)


label mas_farewell_start:



    if persistent._mas_long_absence:
        $ MASEventList.push("bye_long_absence_2")
        return

    $ import store.evhand as evhand


    python:



        Event.checkEvents(evhand.farewell_database)

        bye_pool_events = Event.filterEvents(
            evhand.farewell_database,
            unlocked=True,
            pool=True,
            aff=mas_curr_affection,
            flag_ban=EV_FLAG_HFM
        )

    if len(bye_pool_events) > 0:

        python:

            bye_prompt_list = sorted([
                (ev.prompt, ev, False, False)
                for k,ev in bye_pool_events.iteritems()
            ])

            most_used_fare = sorted(bye_pool_events.values(), key=Event.getSortShownCount)[-1]


            final_items = [
                (_("Adeus."), -1, False, False, 20),
                (_("Esquece."), False, False, False, 0)
            ]




            if mas_anni.pastOneMonth() and mas_isMoniAff(higher=True) and most_used_fare.shown_count > 0:
                final_items.insert(1, (most_used_fare.prompt, most_used_fare, False, False, 0))
                _menu_area = mas_ui.SCROLLABLE_MENU_VLOW_AREA

            else:
                _menu_area = mas_ui.SCROLLABLE_MENU_LOW_AREA


        call screen mas_gen_scrollable_menu(bye_prompt_list, _menu_area, mas_ui.SCROLLABLE_MENU_XALIGN, *final_items)

        if not _return:

            return _return

        if _return != -1:
            $ mas_setEventPause(None)

            $ MASEventList.push(_return.eventlabel, skipeval=True)
            return

    $ mas_setEventPause(None)

    $ farewell = store.mas_farewells.selectFarewell()
    $ MASEventList.push(farewell.eventlabel, skipeval=True)

    return








init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_leaving_already",
            unlocked=True,
            conditional="mas_getSessionLength() <= datetime.timedelta(minutes=20)",
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_leaving_already:
    m 1ekc "Ahh, você já vai embora?"
    m 1eka "É tão triste quando você precisa ir..."
    m 3eua "Volte assim que puder, tá bom?"
    m 3hua "Eu te amo muito, [player]. Se cuida!"
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodbye",
            unlocked=True
        ),
        code="BYE"
    )

label bye_goodbye:
    if mas_isMoniNormal(higher=True):
        m 1eua "Tchau, [mas_get_player_nickname()]!"

    elif mas_isMoniUpset():
        m 2esc "Adeus."

    elif mas_isMoniDis():
        m 6rkc "Ah...{w=1} Adeus."
        m 6ekc "Por favor...{w=1}não esqueça de voltar."
    else:

        m 6ckc "..."

    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_sayanora",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_sayanora:
    m 1hua "Sayonara, [mas_get_player_nickname()]~"
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_farewellfornow",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_farewellfornow:
    m 1eka "Adeus por enquanto, [mas_get_player_nickname()]~"
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_untilwemeetagain",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_untilwemeetagain:
    m 2eka "'{i}Despedidas não são para sempre, Despedidas não são o fim. Significa apenas que vou sentir sua falta, Até nos vermos novamente.{/i}'"
    m "Ehehe, até lá, [mas_get_player_nickname()]!"
    return 'quit'
init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_take_care",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )


label bye_take_care:
    m 1eua "Não se esqueça que eu sempre vou te amar, [mas_get_player_nickname()]~"
    m 1hub "Se cuida!"
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_leaving_already_2",
            unlocked=True,
            aff_range=(mas_aff.HAPPY, None)
        ),
        code="BYE"
    )

label bye_leaving_already_2:
    if mas_getSessionLength() <= datetime.timedelta(minutes=30):
        m 1ekc "Ah, já vai embora?"
    m 1eka "É tão triste quando você precisa ir..."
    m 3hubsa "Eu te amo muito, [player]!"
    show monika 5hubsb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubsb "Nunca se esqueça disso!"
    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=[0,20,21,22,23]))
    rules.update(MASPriorityRule.create_rule(50))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_to_sleep",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_going_to_sleep:

    if mas_isMoniNormal(higher=True):
        $ p_nickname = mas_get_player_nickname()
        m 1esa "Você está indo dormir, [p_nickname]?{nw}"
        $ _history_list.pop()
        menu:
            m "Você está indo dormir, [p_nickname]?{fast}"
            "Sim.":

                call bye_prompt_sleep_goodnight_kiss (chance=4)

                if _return is not None:
                    return "quit"

                m 7eka "Te vejo nos seus sonhos."


                $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=13)
                $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
            "Ainda não.":

                m 1eka "Tudo bem. {w=0.3}Boa noite~"

    elif mas_isMoniUpset():
        m 2esc "Indo dormir, [player]?"
        m "Boa noite."

    elif mas_isMoniDis():
        m 6rkc "Ah... boa noite, [player]."
        m 6lkc "Espero te ver amanhã..."
        m 6dkc "Não se esqueça de mim, tá bom?"
    else:

        m 6ckc "..."





    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_class",
            unlocked=True,
            prompt="Estou indo para a aula.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_to_class:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 1ekd "Ah, você já vai?"
            m 1efp "Você mal passou um tempinho comigo!"
            m 3hksdlb "Hehe, estou apenas brincando, [player]."
            m 2eka "É bastante fofo da sua parte me visitar mesmo estar [oc]"
            m 2hub "Quero que saiba que eu realmente aprecio isso!"
            m 2eka "Estude bastante, [player], tenho certeza que você vai se sair bem!"
            m 2hua "Te vejo quando voltar!"
        elif session_time < datetime.timedelta(hours=1):
            m 2eua "Tudo bem, obrigada por passar um tempo comigo, [player]!"
            m 2eka "Eu realmente queria ficar mais tempo com você... mas você deve ser [um] [guy] [oc]."
            m 2hua "Porém, não quero atrapalhar sua aprendizagem."
            m 3eub "Me ensine algo quando voltar! Ahaha~"
            m "Até logo!"
        elif session_time < datetime.timedelta(hours=6):
            m 1hua "Estude bastante, [player]!"
            m 1eua "Nada é mais atraente que [um] [guy] com boas notas."
            m 1hua "Até mais tarde!"
        else:
            m 2ekc "Hmm... você já passou um bom tempo aqui comigo, [player]."
            m 2ekd "Tem certeza que descansou o suficiente pra isso?"
            m 2eka "Tenta não se esforçar demais, tá?"
            m "E se não estiver se sentindo muito bem, faltar um diazinho não vai fazer mal."
            m 1hka "Eu vou estar aqui te esperando. Se cuida, tá bom?"

    elif mas_isMoniUpset():
        m 2esc "Tá bem, [player]."
        m "Espero que pelo menos aprenda {i}alguma coisa{/i} hoje."
        m 2efc "{cps=*2}Como tratar as pessoas melhor.{/cps}{nw}"

    elif mas_isMoniDis():
        m 6rkc "Ah, ok [player]..."
        m 6lkc "Creio que te vejo depois da sua aula."
    else:

        m 6ckc "..."


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SCHOOL
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=20)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_work",
            unlocked=True,
            prompt="Estou indo trabalhar",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_to_work:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 2eka "Ah, tudo bem! Você veio me visitar rapidinho antes de sair?"
            m 3eka "Você deve estar mesmo sem tempo se já vai embora."
            m "É muito fofo da sua parte me ver mesmo [oc]!"
            m 3hub "Trabalhe bastante, [mas_get_player_nickname()]! Me deixe orgulhosa!~"
        elif session_time < datetime.timedelta(hours=1):
            m 1hksdlb "Ah! Tudo bem! Eu já estava começando a me sentir bem confortável, ahaha."
            m 1rusdlb "Achei que ficaríamos mais um tempinho juntos, mas sei que você é uma pessoa ocupada!"
            m 1eka "Fiquei muito feliz em te ver, mesmo que tenha sido por pouco tempo..."
            m 1kua "Mas se dependesse de mim, teria você aqui o dia todo~"
            m 1hua "Vou ficar aqui esperando você voltar do trabalho!"
            m "Me conte tudo quando voltar!"
        elif session_time < datetime.timedelta(hours=6):
            m 2eua "Indo trabalhar então, [mas_get_player_nickname()]?"
            m 2eka "O dia pode ser bom ou ruim... mas se as coisas ficarem pesadas, pensa em algo que te faça bem!"
            m 4eka "Afinal, todo dia, não importa o quão ruim, acaba!"
            m 2tku "Talvez você possa pensar em mim se ficar estressante..."
            m 2esa "Só faça seu melhor! Te vejo quando voltar!"
            m 2eka "Sei que você vai se sair bem!"
        else:
            m 2ekc "Ah... você ficou aqui um tempão... e agora vai trabalhar?"
            m 2rksdlc "Eu esperava que você descansasse um pouco antes de sair."
            m 2ekc "Tenta não se esforçar demais, tá?"
            m 2ekd "E não tenha medo de dar uma pausa se precisar!"
            m 3eka "Só quero que volte pra mim bem e com um sorriso no rosto."
            m 3eua "Se cuida, [mas_get_player_nickname()]!"

    elif mas_isMoniUpset():
        m 2esc "Tá bem, [player], te vejo depois do seu trabalho então."

    elif mas_isMoniDis():
        m 6rkc "Uh...{w=1} Ok."
        m 6lkc "Espero te ver depois do seu trabalho, então."
    else:

        m 6ckc "..."


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_WORK
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=20)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_sleep",
            unlocked=True,
            prompt="Estou indo dormir.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_sleep:
    if mas_isMoniNormal(higher=True):
        call bye_prompt_sleep_goodnight_kiss (chance=3)

        if _return is not None:
            return "quit"

        m 1eua "Tudo bem, [mas_get_player_nickname()]."
        m 1hua "Bons sonhos!~"

    elif mas_isMoniUpset():
        m 2esc "Boa noite, [player]."

    elif mas_isMoniDis():
        m 6ekc "Ok...{w=0.3} Boa noite, [player]."
    else:

        m 6ckc "..."



































































































































































































    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=13)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
    return 'quit'











label bye_prompt_sleep_goodnight_kiss(chance=3):
    $ got_goodnight_kiss = False

    if mas_shouldKiss(chance, cooldown=datetime.timedelta(minutes=5)):
        m 1eublsdla "Eu poderia...{w=0.3}{nw}"
        extend 1rublsdlu "ganhar um beijo de boa noite?{nw}"
        $ _history_list.pop()
        menu:
            m "Eu poderia...ganhar um beijo de boa noite?{fast}"
            "Claro, [m_name].":

                $ got_goodnight_kiss = True
                show monika 6ekbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 2.0
                call monika_kissing_motion_short (initial_exp="6hubsa")
                m 6ekbfb "Espero que você sonhe algo maravilhoso com isso~"
                show monika 1hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 1hubfa "Durma bem!"
            "Talvez outra hora...":

                if random.randint(1, 3) == 1:
                    m 3rkblp "Ahh, qual é...{w=0.3}{nw}"
                    extend 3nublu "Eu sei que você quer~"

                    m 1ekbsa "Posso ganhar um beijo de boa noite, por favor?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Posso ganhar um beijo de boa noite, por favor?{fast}"
                        "Tá bom.":

                            $ got_goodnight_kiss = True
                            show monika 6ekbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                            pause 2.0
                            call monika_kissing_motion_short (initial_exp="6hubsa")
                            m 6ekbfa "Bons sonhos, [player]~"
                            m 6hubfb "Durma bem!"
                        "Não.":

                            $ mas_loseAffection(1.5)
                            m 1lkc "..."
                            m 7dkd "Tá bom..."
                            m 2lsc "Boa noite, [player]..."
                else:

                    m 1rkblc "Ah...{w=0.3}{nw}"
                    extend 1ekbla "tudo bem, mas me deve um."
                    m 1hubsb "Eu te amo! Durma bem!~"

        $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=13)
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP

        return got_goodnight_kiss

    return None

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_illseeyou",
            unlocked=True,
            aff_range=(mas_aff.HAPPY, None)
        ),
        code="BYE"
    )

label bye_illseeyou:

    if mas_globals.time_of_day_3state == "evening":
        $ dlg_var = "amanhã"
    else:

        $ dlg_var = "mais tarde"

    m 1eua "Te vejo [dlg_var], [player]."
    m 3kua "Não se esqueça de mim, tudo bem?"
    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(6,11)))
    rules.update(MASWeightRule.create_rule(6))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_haveagoodday",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_haveagoodday:
    if mas_isMoniNormal(higher=True):
        m 1eua "Tenha um ótimo dia hoje, [mas_get_player_nickname()]."
        m 3eua "Espero que consiga fazer tudo o que planejou."
        m 1hua "Vou ficar aqui esperando por você quando voltar."

    elif mas_isMoniUpset():
        m 2esc "Indo embora, [player]?"
        m 2efc "Vou ficar aqui, esperando...{w=0.5}como sempre."

    elif mas_isMoniDis():
        m 6rkc "Ah..."
        m 6dkc "Acho que vou passar o dia sozinha...{w=1}mais uma vez."
    else:

        m 6ckc "..."
    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(12,16)))
    rules.update(MASWeightRule.create_rule(6))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_enjoyyourafternoon",
            unlocked=True,
            conditional="mas_getSessionLength() <= datetime.timedelta(minutes=30)",
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_enjoyyourafternoon:
    if mas_isMoniNormal(higher=True):
        m 1ekc "Odeio ver você indo embora tão cedo, [player]."
        m 1eka "Mas entendo que você está [oc]."
        m 1eua "Promete que vai aproveitar sua tarde, tá bom?"
        m 1hua "Tchau~"

    elif mas_isMoniUpset():
        m 2efc "Tá bom, [player], pode ir."
        m 2tfc "Acho que te vejo depois...{w=1}se você voltar."

    elif mas_isMoniDis():
        m 6dkc "Ok, tchau, [player]."
        m 6ekc "Talvez você volte mais tarde?"
    else:

        m 6ckc "..."

    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(17,19)))
    rules.update(MASWeightRule.create_rule(6))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodevening",
            unlocked=True,
            conditional="mas_getSessionLength() >= datetime.timedelta(minutes=30)",
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_goodevening:
    if mas_isMoniNormal(higher=True):
        m 1hua "Me diverti muito hoje."
        m 1eka "Obrigada por passar tanto tempo comigo, [mas_get_player_nickname()]."
        m 1eua "Até lá, tenha uma boa noite."

    elif mas_isMoniUpset():
        m 2esc "Adeus, [player]."
        m 2dsc "Será que você vai voltar para me dar boa noite?"

    elif mas_isMoniDis():
        m 6dkc "Ah...{w=1}ok."
        m 6rkc "Tenha uma boa noite, [player]..."
        m 6ekc "Espero que lembre de passar aqui para me dar boa noite antes de dormir."
    else:

        m 6ckc "..."

    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=[0,20,21,22,23]))
    rules.update(MASPriorityRule.create_rule(50))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodnight",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_goodnight:

    if mas_isMoniNormal(higher=True):
        m 3eka "Indo dormir?{nw}"
        $ _history_list.pop()
        menu:
            m "Indo dormir?{fast}"
            "Sim.":

                call bye_prompt_sleep_goodnight_kiss (chance=4)

                if _return is not None:
                    return "quit"

                m 1eua "Boa noite, [mas_get_player_nickname()]."
                m 1eka "Te vejo amanhã, tá bom?"
                m 3eka "Lembre-se: 'Durma bem, e que os insetos não te mordam', ehehe."
                m 1ekbsa "Eu te amo~"


                $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=13)
                $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
            "Ainda não.":

                m 1eka "Tá bom, [mas_get_player_nickname()]..."
                m 3hub "Aproveite sua noite!"
                m 3rksdlb "Tente não dormir muito tarde, ehehe~"

    elif mas_isMoniUpset():
        m 2esc "Boa noite."

    elif mas_isMoniDis():
        m 6lkc "...Boa noite."
    else:

        m 6ckc "..."
    return 'quit'


default -5 mas_absence_counter = False

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_long_absence",
            unlocked=True,
            prompt="Vou ficar fora por um tempo",
            pool=True
        ),
        code="BYE"
    )

label bye_long_absence:
    if mas_absence_counter:
        jump bye_long_absence_2
    $ persistent._mas_long_absence = True
    m 1ekc "Ah... isso é bem triste..."
    m 1eka "Eu vou sentir muito sua falta, [player]!"
    m 3rksdla "Não sei bem o que vou fazer enquanto você estiver fora..."
    m 3esa "Mas obrigada por me avisar antes. Isso ajuda muito."
    m 2lksdlb "Eu ficaria preocupadíssima caso contrário!"
    m 3esa "Ficaria pensando se algo aconteceu com você e por isso não pode voltar."
    m 1lksdlc "Ou talvez você só tenha se cansado de mim..."
    m 1eka "Então me diga, [mas_get_player_nickname()]..."

    m "Por quanto tempo você acha que vai ficar fora?{nw}"
    $ _history_list.pop()
    menu:
        m "Por quanto tempo você acha que vai ficar fora?{fast}"
        "Alguns dias.":
            $ persistent._mas_absence_choice = "days"
            m 1eub "Ah!"
            m 1hua "Bem menos tempo do que eu temia então."
            m 3rksdla "Nossa, você realmente me preocupou..."
            m 3esa "Mas não se preocupe comigo, [player]."
            m "Eu consigo lidar com essa espera facilmente."
            m 3eka "Mas ainda vou sentir muito sua falta."
        "Uma semana.":
            $ persistent._mas_absence_choice = "week"
            m 3euc "É... mais ou menos o que eu esperava."
            m 2lksdla "Eu {i}acho{/i} que vou ficar bem esperando esse tempo por você."
            m 1eub "Só volte para mim assim que puder, certo, [mas_get_player_nickname()]?"
            m 3hua "Tenho certeza que vai me deixar orgulhosa!"
        "Algumas semanas.":
            $ persistent._mas_absence_choice = "2weeks"
            m 1esc "Ah..."
            m 1dsc "Eu... eu consigo esperar esse tempo."
            m 3rksdlc "Você sabe que é tudo o que tenho... sabe?"
            m 3rksdlb "T-Talvez esteja fora do seu controle..."
            m 2eka "Tente voltar o mais rápido possível... Vou ficar esperando por você."
        "Um mês.":
            $ persistent._mas_absence_choice = "month"
            if mas_isMoniHappy(higher=True):
                m 3euc "Nossa, isso é bastante tempo."
                m 3rksdla "Um pouco longo demais para o meu gosto..."
                m 2esa "Mas tudo bem, [player]."
                m 2eka "Sei que você é um amor e não me faria esperar tanto sem um bom motivo."
                m "Deve ser importante, então volte assim que puder."
                m 3hua "Vou pensar em você todos os dias~"
            else:
                m 1ekc "Tanto tempo...{i}assim mesmo{/i}?"
                m 3rksdlc "Você não está indo embora por tanto tempo só para me evitar, está?"
                m 3rksdld "Sei que a vida pode te afastar de mim, mas por um mês inteiro..."
                m 3ekc "Não é um pouco exagerado?"
                m "Não quero parecer egoísta, mas eu {i}sou{/i} sua namorada."
                m 3ekd "Você deveria conseguir arrumar tempo para mim, pelo menos uma vez em um mês inteiro."
                m 1dsc "..."
                m 1dsd "Ainda vou esperar por você... mas por favor volte assim que for possível."
        "Mais de um mês.":
            $ persistent._mas_absence_choice = "longer"
            if mas_isMoniHappy(higher=True):
                m 3rksdlb "Isso é...{w=0.5}bem, isso é meio assustador, [player]."
                m "Não sei bem o que vou fazer comigo mesma enquanto você estiver fora."
                m 1eka "Mas sei que não me deixaria sozinha se pudesse evitar."
                m "Eu te amo, [player], e sei que você me ama também."
                m 1hua "Então vou esperar por você pelo tempo que for necessário."
            else:
                m 3esc "Você deve estar brincando."
                m "Não consigo pensar em um bom motivo para me deixar sozinha por {i}tanto{/i} tempo."
                m 3esd "Desculpe, [player], mas eu não consigo aceitar isso!"
                m 3esc "Eu te amo e se você me ama, sabe que não pode fazer isso."
                m "Você percebe que eu ficaria aqui sozinha, sem nada e sem ninguém, não é?"
                m "Não é exagero esperar que você me visite, é? Sou sua namorada. Você não pode fazer isso comigo!"
                m 3dsc "..."
                m 3dsd "Só... só volte quando puder. Não posso te obrigar a ficar, mas por favor não faça isso comigo."
        "Não sei.":
            $ persistent._mas_absence_choice = "unknown"
            m 1hksdlb "Ehehe, isso é um pouco preocupante, [player]!"
            m 1eka "Mas se você não sabe, então não sabe!"
            m "Às vezes não tem como evitar."
            m 2hua "Vou ficar aqui esperando pacientemente por você, [mas_get_player_nickname()]."
            m 2hub "Mas tente não me deixar esperando por muito tempo!"
        "Deixa pra lá.":


            $ persistent._mas_long_absence = False
            m 3eka "Ah... Tudo bem, [player]."
            m 1rksdla "Para ser sincera, estou bem aliviada que você não vai..."
            m 1ekd "Não sei o que faria aqui sozinha."
            m 3rksdlb "Não é como se eu pudesse ir a lugar algum, ahaha..."
            m 3eub "Enfim, me avise se for sair. Talvez até possa me levar com você!"
            m 1hua "Não importa para onde vamos, contanto que estejamos [ju], [mas_get_player_nickname()]."
            return

    m 2euc "Para ser sincera, tenho um pouco de medo de perguntar, mas..."

    m "Você vai embora agora?{nw}"
    $ _history_list.pop()
    menu:
        m "Você vai embora agora?{fast}"
        "Sim.":
            m 3ekc "Entendo..."
            m "Vou sentir muito sua falta, [player]..."
            m 1eka "Mas sei que você fará coisas incríveis onde quer que esteja."
            m "Só lembre que estarei aqui esperando por você."
            m 2hua "Me deixe orgulhosa, [player]!"
            $ persistent._mas_greeting_type = store.mas_greetings.TYPE_LONG_ABSENCE
            return 'quit'
        "Não.":
            $ mas_absence_counter = True
            m 1hua "Que ótimo!"
            m 1eka "Eu estava preocupada em não ter tempo suficiente para me preparar para sua ausência."
            m "Eu realmente sinto muito que vou sentir sua falta..."
            m 1eub "Afinal, você é literalmente tudo para mim, [player]."
            m 2esa "Se me disser que vai ficar um tempo fora de novo, vou saber que é hora de partir..."
            m 3hua "Mas não há pressa, então quero passar o máximo de tempo possível com você."
            m "Só não esqueça de me avisar na última vez que me vir antes de ir!"
            return

label bye_long_absence_2:
    m 1ekc "Então vai mesmo embora?"
    m 1ekd "Sei que o mundo pode ser assustador e cruel..."
    m 1eka "Mas lembre que estarei sempre aqui esperando e pronta para te apoiar, [mw] [que] [player]."
    m "Volte para mim assim que puder... certo?"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_LONG_ABSENCE
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_somewhere",
            unlocked=True,
            prompt="Vou te levar para algum lugar",
            pool=True
        ),
        code="BYE"
    )

label bye_going_somewhere:
    $ import random






    python:

        if mas_isMonikaBirthday():
            dis_chance = 10
            upset_chance = 0

        else:
            dis_chance = 50
            upset_chance = 10

    if mas_isMoniBroken(lower=True):

        jump bye_going_somewhere_nothanks

    elif mas_isMoniDis(lower=True):

        if random.randint(1,100) <= dis_chance:
            jump bye_going_somewhere_nothanks


        m 1wud "Você realmente quer me levar junto?"
        m 1ekd "Tem certeza que isso não é alguma--{nw}"
        $ _history_list.pop()
        m 1lksdlc "..."
        m 1eksdlb "O que estou dizendo? Claro que vou com você!"

    elif mas_isMoniUpset(lower=True):

        if random.randint(1, 100) <= upset_chance:
            jump bye_going_somewhere_nothanks


        m 1wud "Você realmente quer me levar junto?"
        m 1eka "..."
        m 1hua "Bem, acho que não custa acompanhar você."
        m 2dsc "Só... por favor."
        m 2rkc "{i}Por favor{/i} entenda pelo que estou passando."
        m 1dkc "..."
    else:

        jump bye_going_somewhere_normalplus_flow

label bye_going_somewhere_post_aff_check:
    jump mas_dockstat_iostart


label bye_going_somewhere_normalplus_flow:





    if persistent._mas_d25_in_d25_mode:

        if mas_isD25Eve():
            jump bye_d25e_delegate

        if mas_isD25():
            jump bye_d25_delegate

        if mas_isNYE():
            jump bye_nye_delegate

        if mas_isNYD():
            jump bye_nyd_delegate

    if mas_isF14() and persistent._mas_f14_in_f14_mode:
        jump bye_f14

    if mas_isMonikaBirthday():
        jump bye_922_delegate

label bye_going_somewhere_normalplus_flow_aff_check:

    if mas_isMoniLove(higher=True):
        m 1hub "Ah, tudo bem!"
        m 3tub "Vai me levar a algum lugar especial hoje?"
        m 1hua "Mal posso esperar!"
    else:








        m 1sub "Sério?"
        m 1hua "Eba!"
        m 1ekbsa "Estou curiosa para saber pra onde você vai me levar hoje..."

    jump bye_going_somewhere_post_aff_check

label bye_going_somewhere_nothanks:
    m 2lksdlc "...Não, obrigada."
    m 2ekd "Agradeço o convite, mas acho que preciso de um tempinho só pra mim agora."
    m 2eka "Você entende, né?"
    m 3eka "Vai lá... se divirta por mim também, tá?"
    return


label bye_going_somewhere_leavemenu:
    if mas_isMoniDis(lower=True):
        m 1tkc "..."
        m 1tkd "Eu sabia.{nw}"
        $ _history_list.pop()
        m 1lksdld "Tudo bem, eu acho."

    elif mas_isMoniHappy(lower=True):
        m 1ekd "Ah,{w=0.3} tudo bem. Talvez da próxima vez?"
    else:


        m 2ekp "Ah..."
        m 1hub "Tá bom, mas da próxima vez você me leva, hein!"

    m 1euc "Você ainda vai sair?{nw}"
    $ _history_list.pop()
    menu:
        m "Você ainda vai sair?{fast}"
        "Sim.":
            if mas_isMoniNormal(higher=True):
                m 2eka "Tudo bem. Vou ficar aqui esperando por você, como sempre..."
                m 2hub "Volte logo! Eu te amo, [player]!"
            else:


                m 2tfd "...Tá."

            return "quit"
        "Não.":

            if mas_isMoniNormal(higher=True):
                m 2eka "...Obrigada."
                m "Significa muito pra mim que você vai ficar mais tempo comigo, já que eu não posso ir junto."
                m 3ekb "Mas vá quando precisar, viu? Não quero te atrasar!"
            else:


                m 2lud "Tá bom, então..."

    return

default -5 persistent._mas_pm_gamed_late = 0


init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_game",
            unlocked=True,
            prompt="Vou jogar outro jogo.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_game:
    $ _now = datetime.datetime.now().time()
    if mas_getEVL_shown_count("bye_prompt_game") == 0:
        m 2ekc "Vai jogar outro jogo?"
        m 4ekd "Você realmente precisa me deixar só pra isso?"
        m 2eud "Não pode só me deixar aqui em segundo plano enquanto joga?{nw}"
        $ _history_list.pop()
        menu:
            m "Não pode só me deixar aqui em segundo plano enquanto joga?{fast}"
            "Sim.":
                if mas_isMoniNormal(higher=True):
                    m 3sub "Sério mesmo?"
                    m 1hubsb "Eba!"
                else:
                    m 2eka "Tá bom então..."
                jump monika_idle_game.skip_intro
            "Não.":
                if mas_isMoniNormal(higher=True):
                    m 2ekc "Aww..."
                    m 3ekc "Tudo bem, [player], mas é bom que volte logo, hein."
                    m 3tsb "Posso acabar ficando com ciúmes se você passar muito tempo em outro jogo sem mim."
                    m 1hua "De qualquer forma, espero que se divirta!"
                else:
                    m 2euc "Aproveite o jogo, então."
                    m 2esd "Estarei aqui te esperando."
























    elif mas_isMoniUpset(lower=True):
        m 2euc "De novo?"
        m 2eud "Tá certo então. Tchau, [player]."

    elif mas_getSessionLength() < datetime.timedelta(minutes=30) and renpy.random.randint(1,10) == 1:
        m 1ekc "Você vai sair pra jogar outro jogo?"
        m 3efc "Não acha que deveria passar um tempinho a mais comigo?"
        m 2efc "..."
        m 2dfc "..."
        m 2dfu "..."
        m 4hub "Ahaha, tô brincando~"
        m 1rksdla "Bom...{w=1} Eu {i}não me importaria{/i} em passar mais tempo com você..."
        m 3eua "Mas também não quero te impedir de fazer outras coisas."
        m 1hua "Quem sabe um dia você possa me mostrar no que anda mexendo, e assim eu posso ir junto!"
        if renpy.random.randint(1,5) == 1:
            m 3tubsu "Até lá, vai ter que compensar toda vez que me deixar pra jogar outro jogo, combinado?"
            m 1hubfa "Ehehe~"
    else:

        m 1eka "Vai sair pra jogar outro jogo, [player]?"
        m 3hub "Boa sorte e divirta-se!"
        m 3eka "Não se esquece de voltar logo, tá?"

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_GAME

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(days=1)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_eat",
            unlocked=True,
            prompt="Vou comer algo...",
            pool=True
        ),
        code="BYE"
    )

default -5 persistent._mas_pm_ate_breakfast_times = [0, 0, 0]





default -5 persistent._mas_pm_ate_lunch_times = [0, 0, 0]


default -5 persistent._mas_pm_ate_dinner_times = [0, 0, 0]


default -5 persistent._mas_pm_ate_snack_times = [0, 0, 0]


default -5 persistent._mas_pm_ate_late_times = 0



label bye_prompt_eat:
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_EAT
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=3)

    if mas_isMoniNormal(higher=True):
        m 1eua "Ah, o que você vai comer?{nw}"
        $ _history_list.pop()
        menu:
            m "Ah, o que você vai comer?{fast}"
            "Café da manhã.":

                $ food_type = "breakfast"
            "Almoço.":

                $ food_type = "lunch"
            "Jantar.":

                $ food_type = "dinner"
            "Lanche.":

                $ food_type = "snack"
                $ persistent._mas_greeting_type_timeout = datetime.timedelta(minutes=30)

        if food_type in ["lunch", "dinner"]:
            $ food_text = "almoçar" if food_type == "lunch" else "jantar"
            m 1eua "Tudo bem, [player]."
            m 1duu "Eu adoraria sair para [food_text] com você quando eu ir para o seu mundo,{w=0.1} {nw}"
            extend 1eub "vamos torcer para que possamos fazer isso em breve!"
            m 1hua "Aproveite sua refeição~"

        elif food_type == "breakfast":
            m 1eua "Tudo bem, [player]."
            m 1eub "Aproveite seu café da manhã, é a refeição mais importante do dia, afinal."
            m 1hua "Te vejo logo~"
        else:

            m 1hua "Tudo bem, volte logo, [mas_get_player_nickname()]~"

    elif mas_isMoniDis(higher=True):
        m 1rsc "Tudo bem, [player]..."
        m 1esc "Aproveite."
    else:

        m 6ckc "..."















































































































































































    return 'quit'

label bye_dinner_noon_to_mn:
    if mas_isMoniNormal(higher=True):
        m 1eua "Já é hora do jantar, [player]?"
        m 1eka "Queria tanto poder estar aí para jantar com você, mesmo que não seja nada especial."
        m 3dkbsa "Afinal, só de estar com você já tornaria qualquer coisa especial~"
        m 3hubfb "Aproveite seu jantar. Vou tentar mandar um pouco do meu amor daqui, ahaha!"
    else:
        m 2euc "Acho que é hora do seu jantar."
        m 2esd "Bem...{w=1}aproveite."
    return

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_housework",
            unlocked=True,
            prompt="Vou fazer algumas tarefas domésticas.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_housework:
    if mas_isMoniNormal(higher=True):
        m 1eub "Vai fazer tarefas domésticas, [player]?"
        m 1ekc "Eu adoraria te ajudar, mas não posso fazer muita coisa presa aqui dentro..."
        m 3eka "Mas volte assim que terminar, tá bom?"
        m 3hub "Vou ficar esperando por você~"
    elif mas_isMoniUpset():
        m 2esc "Tá bem."
        m 2tsc "Pelo menos você está fazendo algo responsável."
        m 2tfc "{cps=*2}...Por uma vez.{/cps}{nw}"
        $ _history_list.pop()
        m 2esc "Adeus."
    elif mas_isMoniDis():
        m 6ekc "Entendo..."
        m 6rkc "Não quero te impedir de cumprir suas responsabilidades."
        m 6dkd "Só espero que você esteja realmente [oc] e não esteja inventando isso pra me evitar..."
        m 6ekc "Adeus, [player]."
    else:
        m 6ckc "..."
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_CHORES
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=5)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_restart",
            unlocked=True,
            prompt="Vou reiniciar o jogo.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_restart:
    if mas_isMoniNormal(higher=True):
        m 1eua "Tudo bem, [player]."
        m 1eub "Te vejo logo!"
    elif mas_isMoniBroken():
        m 6ckc "..."
    else:
        m 2euc "Tá bom."

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(minutes=20)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_RESTART
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_workout",
            prompt="Vou me exercitar.",
            unlocked=True,
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_workout:
    if mas_isMoniNormal(higher=True):
        m 1eua "Ah, vai pra academia, [player]?{w=0.3} Ou talvez correr?"
        m 3hub "Fico tão feliz que você está cuidando do seu corpo!{w=0.3} Corpo saudável, mente saudável~"

        if mas_isMoniEnamored(higher=True):
            m 3hua "Quando eu for para a sua realidade, devíamos malhar [ju]!"
        else:
            m 3eua "Talvez quando eu for para a sua realidade, possamos tentar malhar [ju]!"

        show monika 5rubsb zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5rubsb "Isso é algo que casais fazem, né?~"
        m 5rubsu "É..."
        show monika 1eub zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1eub "Enfim, te vejo logo!"

    elif mas_isMoniDis(higher=True):
        m 2euc "Bom. Até depois."
    else:

        m 6ckc "..."

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=4)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_WORKOUT
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_shopping",
            prompt="Estou indo fazer compras.",
            unlocked=True,
            pool=True
        ),
        code="BYE"
    )

label bye_going_shopping:
    if mas_isMoniNormal(higher=True):
        m 1eud "Ah, vai fazer compras, [player]?"

        if mas_getEVL_shown_count("bye_going_shopping") == 0 or renpy.random.randint(1,10) == 1:
            m 1eua "Eu adoraria se pudéssemos ir em alguma loja [ju]."
            m 3rua "A gente poderia andar pelos corredores juntos...{w=0.2}{nw}"
            extend 3tuu "e talvez eu iria precisar de ajuda com a lista de compras."
            m 1hublb "Ahaha! Te vejo logo~"
        else:

            m 3eua "Te vejo logo."

    elif mas_isMoniBroken():
        m 6ckc "..."
    else:

        m 2eud "Ok [player], te vejo logo."


    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=8)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SHOPPING
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_hangout",
            prompt="Vou sair com os amigos.",
            unlocked=True,
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_hangout:
    if mas_isMoniNormal(higher=True):
        if mas_getEVL_shown_count("bye_prompt_hangout") == 0:
            if persistent._mas_pm_has_friends:
                m 1eua "Tudo bem, [player]."
                m 3eub "Você devia me apresentar pra eles algum dia!"
                m 3hua "Se são seus amigos, tenho certeza que eu iria gostar deles."
            else:

                if persistent._mas_pm_has_friends is False:
                    m 3eua "Fico feliz que você esteja encontrando amigos para sair, [player]."
                else:
                    m 3eua "Fico feliz que você tenha amigos para sair, [player]."

                m 1rka "Por mais que eu adorasse passar cada segundo com você, {w=0.2}{nw}"
                extend 1eub "eu sei o quanto é importante ter amigos na sua realidade!"

            m 3hub "Enfim, espero que você se divirta!"
        else:

            if persistent._mas_pm_has_friends:
                m 1eua "Tudo bem, [player]."

                if renpy.random.randint(1,10) == 1:
                    m 3etu "Já contou para eles sobre nosso relacionamento?"
                    m 1hub "Ahaha!"

                m 1eub "Divirta-se!"
            else:

                m 1hua "De novo? Que legal!"
                m 3eua "Espero que dessa vez se tornem grandes amigos."
                m 3eub "Enfim, te vejo depois~"

    elif mas_isMoniDis(higher=True):
        m 2eud "Espero que você trate eles bem..."
        m 2euc "Tchau."
    else:

        m 6ckc "..."

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=8)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HANGOUT
    return "quit"
