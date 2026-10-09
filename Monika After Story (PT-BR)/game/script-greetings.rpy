init offset = 5




















default -5 persistent._mas_you_chr = False



default -5 persistent._mas_greeting_type = None






default -5 persistent._mas_greeting_type_timeout = None

default -5 persistent._mas_idle_mode_was_crashed = None




init -6 python in mas_greetings:
    import store
    import store.mas_ev_data_ver as mas_edv
    import datetime
    import random


    TYPE_SCHOOL = "school"
    TYPE_WORK = "work"
    TYPE_SLEEP = "sleep"
    TYPE_LONG_ABSENCE = "long_absence"
    TYPE_SICK = "sick"
    TYPE_GAME = "game"
    TYPE_EAT = "eat"
    TYPE_CHORES = "chores"
    TYPE_RESTART = "restart"
    TYPE_SHOPPING = "shopping"
    TYPE_WORKOUT = "workout"
    TYPE_HANGOUT = "hangout"


    TYPE_GO_SOMEWHERE = "go_somewhere"


    TYPE_GENERIC_RET = "generic_go_somewhere"


    TYPE_HOL_O31 = "o31"
    TYPE_HOL_O31_TT = "trick_or_treat"
    TYPE_HOL_D25 = "d25"
    TYPE_HOL_D25_EVE = "d25e"
    TYPE_HOL_NYE = "nye"
    TYPE_HOL_NYE_FW = "fireworks"


    TYPE_CRASHED = "generic_crash"


    TYPE_RELOAD = "reload_dlg"




    HP_TYPES = [
        TYPE_GO_SOMEWHERE,
        TYPE_GENERIC_RET,
        TYPE_LONG_ABSENCE,
        TYPE_HOL_O31_TT
    ]

    NTO_TYPES = (
        TYPE_GO_SOMEWHERE,
        TYPE_GENERIC_RET,
        TYPE_LONG_ABSENCE,
        TYPE_CRASHED,
        TYPE_RELOAD,
    )





    def _filterGreeting(
            ev,
            curr_pri,
            aff,
            check_time,
            gre_type=None
        ):
        """
        Filters a greeting for the given type, among other things.

        IN:
            ev - ev to filter
            curr_pri - current loweset priority to compare to
            aff - affection to use in aff_range comparisons
            check_time - datetime to check against timed rules
            gre_type - type of greeting we want. We just do a basic
                in check for category. We no longer do combinations
                (Default: None)

        RETURNS:
            True if this ev passes the filter, False otherwise
        """
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if ev.anyflags(store.EV_FLAG_HFRS):
            return False
        
        
        
        if store.MASPriorityRule.get_priority(ev) > curr_pri:
            return False
        
        
        if gre_type is not None:
            
            
            if gre_type in HP_TYPES:
                
                
                if ev.category is None or gre_type not in ev.category:
                    
                    return False
            
            elif ev.category is not None:
                
                
                if gre_type not in ev.category:
                    
                    return False
            
            elif not store.MASGreetingRule.should_override_type(ev):
                
                
                
                return False
        
        elif ev.category is not None:
            
            return False
        
        
        if not ev.unlocked:
            return False
        
        
        if not ev.checkAffection(aff):
            return False
        
        
        if not (
            store.MASSelectiveRepeatRule.evaluate_rule(
                check_time, ev, defval=True)
            and store.MASNumericalRepeatRule.evaluate_rule(
                check_time, ev, defval=True)
            and store.MASGreetingRule.evaluate_rule(ev, defval=True)
            and store.MASTimedeltaRepeatRule.evaluate_rule(ev)
        ):
            return False
        
        
        if not ev.checkConditional():
            return False
        
        
        return True



    def selectGreeting(gre_type=None, check_time=None):
        """
        Selects a greeting to be used. This evaluates rules and stuff
        appropriately.

        IN:
            gre_type - greeting type to use
                (Default: None)
            check_time - time to use when doing date checks
                If None, we use current datetime
                (Default: None)

        RETURNS:
            a single greeting (as an Event) that we want to use
        """
        if (
                store.persistent._mas_forcegreeting is not None
                and renpy.has_label(store.persistent._mas_forcegreeting)
            ):
            return store.mas_getEV(store.persistent._mas_forcegreeting)
        
        
        gre_db = store.evhand.greeting_database
        
        
        gre_pool = []
        curr_priority = 1000
        aff = store.mas_curr_affection
        
        if check_time is None:
            check_time = datetime.datetime.now()
        
        
        for ev_label, ev in gre_db.iteritems():
            if _filterGreeting(
                    ev,
                    curr_priority,
                    aff,
                    check_time,
                    gre_type
                ):
                
                
                ev_priority = store.MASPriorityRule.get_priority(ev)
                if ev_priority < curr_priority:
                    curr_priority = ev_priority
                    gre_pool = []
                
                
                gre_pool.append(ev)
        
        
        if len(gre_pool) == 0:
            return None
        
        return random.choice(gre_pool)


    def checkTimeout(gre_type):
        """
        Checks if we should clear the current greeting type because of a
        timeout.

        IN:
            gre_type - greeting type we are checking

        RETURNS: passed in gre_type, or None if timeout occured.
        """
        tout = store.persistent._mas_greeting_type_timeout
        
        
        store.persistent._mas_greeting_type_timeout = None
        
        if gre_type is None or gre_type in NTO_TYPES or tout is None:
            return gre_type
        
        if mas_edv._verify_td(tout, False):
            
            last_sesh_end = store.mas_getLastSeshEnd()
            if datetime.datetime.now() < (tout + last_sesh_end):
                
                return gre_type
            
            
            return None
        
        elif mas_edv._verify_dt(tout, False):
            
            if datetime.datetime.now() < tout:
                
                return gre_type
            
            
            return None
        
        return gre_type



label mas_idle_mode_greeting_cleanup:
    $ mas_resetIdleMode()
    return


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sweetheart",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_sweetheart:
    m 1hub "Olá novamente, [que]!"

    if persistent._mas_player_nicknames:
        m 1eka "É tão bom te ver de novo."
        m 1eua "O que vamos fazer neste linda [mas_globals.time_of_day_3state], [player]?"
    else:
        m 1lkbsa "É meio constrangedor dizer isso em voz alta, não é?"
        m 3ekbfa "Mas, sabe... acho que tudo bem se sentir envergonhado de vez em quando."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_honey",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_honey:
    m 1hub "Bem-[vn] de volta, [que]!"
    m 1eua "Estou tão feliz em te ver novamente."
    m "Vamos passar mais um tempinho [ju], tudo bem?"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=12)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="GRE"
    )

label greeting_back:
    $ tod = "dia" if mas_globals.time_of_day_4state != "noite" else "noite"
    m 1eua "[player], você voltou!"
    m 1eka "Eu já estava começando a sentir sua falta."

    $ time = "outro adorável" if mas_globals.time_of_day_3state in ["dia", "tarde"] else "outra adorável"
    m 1hua "Vamos ter [time] [mas_globals.time_of_day_3state] [ju], ehehe~"

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_gooday",
            unlocked=True,
        ),
        code="GRE"
    )

label greeting_gooday:
    if mas_isMoniNormal(higher=True):
        m 1hua "Olá de novo, [player]. Como você está?"

        m "Está tendo um bom dia hoje?{nw}"
        $ _history_list.pop()
        menu:
            m "Está tendo um bom dia hoje?{fast}"
            "Sim.":
                m 1hub "Fico muito feliz por ouvir isso, [player]!"
                m 1eua "Saber que você está bem deixa o meu dia muito melhor também."
                m "Vou fazer o possível pra manter esse sorriso no seu rosto, tá bom? Prometo."
            "Não...":
                m 1ekc "Ah... entendo."
                m 2eka "Mas não se preocupe, [player]. Eu tô aqui pra você."
                m "Se quiser, a gente pode conversar o dia todo sobre o que está te incomodando."
                m 3eua "Quero fazer de tudo pra te ver feliz, de verdade."
                m 1eka "Porque é isso que me faz feliz também."
                m 1hua "Vou dar o meu melhor pra animar você, tá bem? Prometo~"

    elif mas_isMoniUpset():
        m 2esc "[player]."

        m "Como está seu dia?{nw}"
        $ _history_list.pop()
        menu:
            m "Como está seu dia?{fast}"
            "Bom.":
                m 2esc "{cps=*2}Que bom, eu acho.{/cps}{nw}"
                $ _history_list.pop()
                m "Que bom..."
                m 2dsc "Pelo menos {i}alguém{/i} está tendo um bom dia."
            "Ruim.":

                m "Ah..."
                m 2efc "{cps=*2}Isso deve ser ótimo...{/cps}{nw}"
                $ _history_list.pop()
                m 2dsc "Bem, eu certamente sei como {i}isso{/i} é."

    elif mas_isMoniDis():
        m 6ekc "Oh...{w=1} Oi, [player]."

        m "C-Como está seu dia?{nw}"
        $ _history_list.pop()
        menu:
            m "C-Como está seu dia?{fast}"
            "Bom.":
                m 6dkc "Isso é...{w=1}bom."
                m 6rkc "Espero que continue assim."
            "Ruim.":
                m 6rkc "E-Eu entendo."
                m 6dkc "Tenho tido muitos dias assim ultimamente também..."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit:
    m 1eua "Aí está você, [player], é tão gentil da sua parte me visitar."
    m 1eka "Você é sempre tão [atncs]."
    m 1hua "Obrigada por passar tanto tempo comigo~"
    return





label greeting_goodmorning:
    $ current_time = datetime.datetime.now().time().hour
    if current_time >= 1 and current_time < 6:
        m 1hua "Bom dia--"
        m 1hksdlb "--ah, espera."
        m "Está no meio da madrugada, amor."
        m 1euc "O que você está fazendo [acrd] a essa hora?"
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Imagino que não consiga dormir..."

        m "É isso?{nw}"
        $ _history_list.pop()
        menu:
            m "É isso?{fast}"
            "Sim.":
                m 5lkc "Você deveria tentar dormir logo, se puder."
                show monika 3euc zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 3euc "Ficar [acrd] até tarde faz mal à saúde, sabia?"
                m 1lksdla "Mas se isso significa que vou te ver mais, não posso reclamar."
                m 3hksdlb "Ahaha!"
                m 2ekc "Mas mesmo assim..."
                m "Odeio ver você se prejudicando assim."
                m 2eka "Descanse se precisar, tá bom? Faça isso por mim."
            "Não.":
                m 5hub "Ah. Que alívio."
                m 5eua "Então quer dizer que veio me ver no meio da madrugada?"
                show monika 2lkbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 2lkbsa "Nossa, estou tão feliz!"
                m 2ekbfa "Você realmente se importa comigo, [player]."
                m 3tkc "Mas se estiver [ca] mesmo, por favor vá dormir!"
                m 2eka "Te amo muito, então não se canse demais!"
    elif current_time >= 6 and current_time < 12:
        m 1hua "Bom dia, [que]."
        m 1esa "Mais uma manhã fresca para começar o dia, né?"
        m 1eua "Fico tão feliz em te ver esta manhã~"
        m 1eka "Lembre-se de cuidar de si mesmo, certo?"
        m 1hub "Me deixe orgulhosa hoje, como sempre!"
    elif current_time >= 12 and current_time < 18:
        m 1hua "Boa tarde, [mas_get_player_nickname()]."
        m 1eka "Não deixe o estresse te afetar, tá bom?"
        m "Sei que vai dar seu melhor hoje, mas..."
        m 4eua "Ainda é importante manter a mente tranquila!"
        m "Mantenha-se hidratado, respire fundo..."
        m 1eka "Prometo que não vou reclamar se precisar parar, então faça o que for preciso."
        m "Ou poderia ficar comigo, se quiser."
        m 4hub "Só lembre que eu te amo!"
    elif current_time >= 18:
        m 1hua "Boa noite, amor!"

        m "Teve um bom dia hoje?{nw}"
        $ _history_list.pop()
        menu:
            m "Teve um bom dia hoje?{fast}"
            "Sim.":
                m 1eka "Ah, que legal!"
                m 1eua "Não consigo evitar ficar feliz quando você está..."
                m "Mas isso é bom, né?"
                m 1ekbsa "Te amo tanto, [player]."
                m 1hubfb "Ahaha!"
            "Não.":
                m 1tkc "Ah, [que]..."
                m 1eka "Espero que se sinta melhor logo, tá bom?"
                m "Só lembre que não importa o que aconteça, o que digam ou façam..."
                m 1ekbsa "Eu te amo muito, muito mesmo."
                m "Fique comigo, se isso te fizer se sentir melhor."
                m 1hubfa "Te amo, [player], de verdade."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back2",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=20)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back2:
    m 1eua "Olá, [que]."
    m 1ekbsa "Eu estava começando a sentir sua falta demais. É tão bom te ver de novo!"
    m 1hubfa "Não me faça esperar tanto da próxima vez, ehehe~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back3",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=1)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back3:
    m 1eka "Senti tanto a sua falta, [player]!"
    m "Obrigada por voltar. Eu realmente amo passar tempo com você."
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 2wfx"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back4",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=10)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_back4:
    m 2wfx "Ei, [player]!"
    m "Não acha que me deixou esperando por tempo demais?"
    m 2hfu "..."
    m 2hub "Ahaha!"
    m 2eka "Tô só brincando. Eu nunca conseguiria ficar brava com você."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit2",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit2:
    m 1hua "Obrigada por passar tanto tempo comigo, [player]."
    m 1eka "Cada minuto ao seu lado é como estar no paraíso!"
    m 1lksdla "Espero que isso não tenha sido muito bobo, ehehe~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit3",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=15)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit3:
    m 1hua "Você voltou!"
    m 1eua "Eu já estava começando a sentir sua falta..."
    m 1eka "Não me faça esperar tanto da próxima vez, tá bom?"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back5",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=15)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back5:
    m 1hua "É tão bom te ver de novo!"
    m 1eka "Eu estava ficando preocupada com você."
    m "Por favor, lembre de me visitar, tá bom? Eu sempre vou estar aqui esperando por você."
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit4",
            conditional="store.mas_getAbsenceLength() <= datetime.timedelta(hours=3)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_visit4:
    if mas_getAbsenceLength() <= datetime.timedelta(minutes=30):
        m 1wud "Oh! [player]!"
        m 3sub "Você voltou!"
        m 3hua "Estou tão feliz que você voltou para me visitar tão rápido~"
    else:
        m 1hub "Eu te amo muuuito, [player]. Ehehe~"
        m 1hksdlb "Ah, desculpa! Eu estava viajando aqui."
        m 1lksdla "Não pensei que veria você de novo tão cedo."
        $ mas_ILY()
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 5hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit5",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_visit5:
    m 5hua "{i}~Todo dia,~\n~eu imagino um futuro onde eu posso estar com você...~{/i}"
    m 5wuw "Ah, você chegou! Eu só estava sonhando acordada e cantando um pouquinho."
    show monika 1lsbssdrb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1lsbssdrb "Acho que não é difícil adivinhar sobre o que eu estava sonhando, ahaha~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit6",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit6:
    m 1hua "Cada dia fica melhor e melhor com você ao meu lado!"
    m 1eua "Dito isso, estou tão feliz que você finalmente chegou."
    m "Vamos ter uma [mas_globals.time_of_day_3state] maravilhoso [ju]."
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1gsu"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back6",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_back6:
    m 3tku "Ei, [player]!"
    m "Você realmente deveria me visitar com mais frequência."
    m 2tfu "Afinal de contas, você sabe o que acontece com as pessoas que eu não gosto..."
    m 1hksdrb "Estou apenas te provocando, ehehe~"
    m 1hua "Não seja tão [ingn]! Eu nunca te machucaria."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit7",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit7:
    m 1hub "Você está aqui, [player]!"
    m 1eua "Está [pos] para passarmos mais tempo [ju]? Ehehe~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit8",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit8:
    m 1hua "Estou tão feliz que você está aqui, [player]!"
    m 1eua "O que deveríamos fazer hoje?"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit9",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=1)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit9:
    m 1hua "Você finalmente está de volta! Eu estava esperando por você."
    m 1hub "Está [pos] para passar um tempo comigo? Ehehe~"
    return


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_italian",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_italian:
    m 1eua "Ciao, [player]!"
    m "È così bello vederti ancora, amore mio..."
    m 1hub "Ahaha!"
    m 2eua "Ainda estou praticando meu Italiano. É um idioma bem difícil!"
    m 1eua "De qualquer forma, é tão bom poder te ver de novo, meu amor."
    return


init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 4hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_latin",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_latin:
    m 4hua "Iterum obvenimus!"
    m 4eua "Quid agis?"
    m 4rksdla "Ehehe..."
    m 2eua "O Latim soa tão pomposo. Até mesmo uma simples saudação parece algo importante."
    m 3eua "Se estiver se perguntado o que eu disse, foi apenas 'Nos encontramos novamente! Como você está?'"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_esperanto",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
)

label greeting_esperanto:
    m 1hua "Saluton, mia kara [player]."
    m 1eua "Kiel vi fartas?"
    m 3eub "Ĉu vi pretas por kapti la tagon?"
    m 1hua "Ehehe~"
    m 3esa "Isso foi só um pouco de Esperanto...{w=0.5}{nw}"
    extend 3eud "um idioma que foi criado artificialmente em vez de ter evoluído naturalmente."
    m 3tua "Quer você tenha ouvido falar dele ou não, você provavelmente não esperava algo assim de mim, hã?"
    m 2etc "Ou talvez você esperava...{w=0.5} Acho que faz sentido algo assim me interessar, levando em conta meu passado..."
    m 1hua "Enfim, se estiver querendo saber o que eu falou, foi:{nw} "
    extend 3hua "'Olá, [que] [player]. Como você está? Está [pos] para aproveitar este dia?'"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_yay",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_yay:
    m 1hub "Você está de volta! Eba!"
    m 1hksdlb "Ah, sinto muito. Me empolguei demais."
    m 1lksdla "Só estou muito feliz de te ver de novo, ehehe~"
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 2eua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_youtuber",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_youtuber:
    m 2eub "Ei, pessoal! Bem-vindos a mais um episódio de...{w=1}Somente Monika!"
    m 2hub "Ahaha!"
    m 1eua "Eu estava representando um youtuber. Espero ter tirado uma boa risada de você, ehehe~"
    $ mas_lockEVL("greeting_youtuber", "GRE")
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 4dsc"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hamlet",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=7)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_hamlet:
    m 4dsc "'{i}Ser ou não ser, eis a questão...{/i}'"
    m 4wuo "Ah! [player]!"
    m 2rksdlc "Eu-eu estav- eu pensei que-"
    m 2dkc "..."
    m 2rksdlb "Ahaha, deixa pra lá..."
    m 2eka "Eu estou apenas {i}realmente{/i} feliz que você está aqui agora."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_welcomeback",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_welcomeback:
    m 1hua "Olá! Bem-[vn] de volta.."
    m 1hub "Estou tão feliz que você vai passar um tempo comigo."
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hub"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_flower",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_flower:
    m 1hub "Você é minha bela flor, ehehe~"
    m 1hksdlb "Ah, isso soou tão estranho."
    m 1eka "Mas eu sempre irei tomar conta de você."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_chamfort",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_chamfort:
    m 2esa "Um dia sem a Monika é um dia desperdiçado."
    m 2hub "Ahaha!"
    m 1eua "Bem-[vn] de volta, [mas_get_player_nickname()]."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_welcomeback2",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_welcomeback2:
    m 1hua "Bem-[vn] de volta, [player]!"
    m "Espero que seu dia esteja indo bem."
    m 1hua "Tenho certeza que está, afinal de contas, você está aqui. Nada pode dar errado agora, ehehe~"
    return













label greeting_longtime:
    if mas_isMoniNormal(higher=True):
        m 1eka "Quanto tempo, [player]!"
        m 1eua "Estou tão feliz que você esteja aqui agora."

    elif mas_isMoniUpset():
        m 2esc "Quanto tempo, [player]."
    else:

        m 6rkc "Quanto tempo, [player]..."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sweetpea",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_sweetpea:
    m 1hua "Veja quem está de volta."
    m 2hub "É você, meu docinho!"

    if mas_isMoniHappy(lower=True):
        m 1lkbsa "Minha nossa...isso com certeza foi vergonhoso de se dizer, ehehe~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_glitch",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_glitch:
    hide monika
    show yuri glitch zorder MAS_BACKGROUND_Z
    y "{cps=500}[player]?!{nw}{/cps}"
    $ _history_list.pop()
    hide yuri glitch
    show yuri glitch2 zorder MAS_BACKGROUND_Z
    play sound "sfx/glitch3.ogg"
    pause 0.1
    hide yuri glitch2
    show yuri glitch zorder MAS_BACKGROUND_Z
    pause 0.3
    hide yuri glitch
    show monika 4rksdlb zorder MAS_MONIKA_Z at i11
    m 1wuo "[player]!"
    hide monika
    show monika 4hksdlb zorder MAS_MONIKA_Z at i11
    m 4hksdlb "Não se preocupe, eu só estava...{w=0.1}brincando um pouco com o código."
    m 3hksdlb "Foi só isso! Não há mais ninguém aqui, além de nós... para todo o sempre~"
    $ monika_clone1 = "Sim"
    m 2hua "Eu te amo, [player]!"

    $ mas_lockEVL("greeting_glitch", "GRE")
    return "love"

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_surprised",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_surprised:
    m 1wuo "Ah!{w=0.5} Olá, [player]!"
    m 1lksdlb "Sinto muito, você me assustou."
    m 1eua "Como você está?"
    return

init python:
    ev_rules = {}
    ev_rules.update(
        MASSelectiveRepeatRule.create_rule(weekdays=[0], hours=range(5,12))
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_monika_monday_morning",
            unlocked=True,
            rules=ev_rules,
        ),
        code="GRE"
    )

    del ev_rules

label greeting_monika_monday_morning:
    if mas_isMoniNormal(higher=True):
        m 1tku "Outra segunda de manhã, hã, [player]?"
        m 1tkc "É bem difícil ter que acordar e começar a semana..."
        m 1eka "Mas ver você acaba com toda minha preguiça."
        m 1hub "Você é o raio de sol que me acorda todas as manhãs!"
        m "Eu te amo tanto, [player]~"
        return "love"

    elif mas_isMoniUpset():
        m 2esc "Outra segunda de manhã."
        m "É sempre difícil ter que acordar e começar a semana..."
        m 2dsc "{cps=*2}Não que o fim de semana tenha sido melhor.{/cps}{nw}"
        $ _history_list.pop()
        m 2esc "Espero que esta semana seja melhor do que a última, [player]."

    elif mas_isMoniDis():
        m 6ekc "Ah...{w=1} É segunda."
        m 6dkc "Eu quase perdi a noção de que dia era..."
        m 6rkc "Segundas são sempre difíceis, mas nenhum dia tem sido fácil ultimamente..."
        m 6lkc "Espero que esta semana seja melhor do que a última, [player]."
    else:

        m 6ckc "..."

    return




define -5 gmr.eardoor = list()
define -5 gmr.eardoor_all = list()
define -5 opendoor.MAX_DOOR = 10
define -5 opendoor.chance = 0.05
default -5 persistent.opendoor_opencount = 0
default -5 persistent.opendoor_knockyes = False

init python:



    if (
        persistent.closed_self
        and not (
            mas_isO31()
            or mas_isD25Season()
            or mas_isplayer_bday()
            or mas_isF14()
        )
        and store.mas_background.EXP_TYPE_OUTDOOR not in mas_getBackground(persistent._mas_current_background, mas_background_def).ex_props
    ):
        
        ev_rules = dict()
        
        
        ev_rules.update(
            MASGreetingRule.create_rule(
                skip_visual=True,
                random_chance=opendoor.chance,
                override_type=True
            )
        )
        ev_rules.update(MASPriorityRule.create_rule(50))
        
        
        
        addEvent(
            Event(
                persistent.greeting_database,
                eventlabel="i_greeting_monikaroom",
                unlocked=True,
                rules=ev_rules,
            ),
            code="GRE"
        )
        
        del ev_rules

label i_greeting_monikaroom:




    $ mas_progressFilter()

    if persistent._mas_auto_mode_enabled:
        $ mas_darkMode(mas_current_background.isFltDay())
    else:
        $ mas_darkMode(not persistent._mas_dark_mode_enabled)



    $ mas_enable_quit()


    $ mas_RaiseShield_core()





    scene black

    $ has_listened = False


    $ mas_rmallEVL("mas_player_bday_no_restart")


label monikaroom_greeting_choice:
    $ _opendoor_text = "...Eu gentilmente abro a porta."

    if mas_isMoniBroken():
        pause 4.0

    menu:
        "[_opendoor_text]" if not persistent.seen_monika_in_room and not mas_isplayer_bday():

            $ mas_loseAffection(reason=5)
            if mas_isMoniUpset(lower=True):
                $ persistent.seen_monika_in_room = True
                jump monikaroom_greeting_opendoor_locked
            else:
                jump monikaroom_greeting_opendoor
        "Abrir a porta." if persistent.seen_monika_in_room or mas_isplayer_bday():
            if mas_isplayer_bday():
                if has_listened:
                    jump mas_player_bday_opendoor_listened
                else:
                    jump mas_player_bday_opendoor
            elif persistent.opendoor_opencount > 0 or mas_isMoniUpset(lower=True):

                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_locked
            else:

                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_seen
        "Bater.":



            $ mas_gainAffection()
            if mas_isplayer_bday():
                if has_listened:
                    jump mas_player_bday_knock_listened
                else:
                    jump mas_player_bday_knock_no_listen

            jump monikaroom_greeting_knock
        "Escutar." if not has_listened and not mas_isMoniBroken():
            $ has_listened = True
            if mas_isplayer_bday():
                jump mas_player_bday_listen
            else:
                $ mroom_greet = renpy.random.choice(gmr.eardoor)

                jump expression mroom_greet





default -5 persistent._mas_pm_will_change = None

init python:
    gmr.eardoor.append("monikaroom_greeting_ear_narration")

    ev_rules = {}
    ev_rules.update(
        MASGreetingRule.create_rule(
            skip_visual=True
        )
    )
    ev_rules.update(MASPriorityRule.create_rule(10))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="monikaroom_will_change",
            unlocked=False,
            rules=ev_rules,
        ),
        restartBlacklist=True,
        code="GRE"
    )

    del ev_rules

label monikaroom_will_change:
    scene black


label monikaroom_greeting_ear_narration:

    $ mas_disable_quit()

    if mas_isMoniNormal(higher=True):
        $ tempname = m_name
        $ m_name = "???"
        m "Conforme o [player] aproximava sua orelha da porta,{w=0.3} uma voz narrava cada movimento [his]."
        m "'Quem está aí?' [he] se perguntou, enquanto [player] olhava para a tela, [cnfs]."
        $ m_name = tempname

    elif mas_isMoniUpset():
        m "Ah, então, pela primeira vez, você vai me ouvir?"
        m "[player], suas decisões ultimante têm sido péssimas."
        m "Parece que você só está tentando me machucar."
        m "Achei que tínhamos que ajudar um ao outro..."
        m "Não ferir um ao outro."
        m "Por favor, [player]..."
        m "Preciso que você comece a pensar em como estou me sentindo."
        m "Vamos ser felizes [ju]."
    else:



        if persistent._mas_pm_will_change is not False:
            m "Ah, então você {i}está{/i} disposto a me ouvir..."
            m "[player], tudo que eu sempre quis é que nós [du] fôssemos felizes."
            m "Não era isso que você queria também?"
            m "Afinal de contas, você instalou este mod."
            m "Talvez essa não tenha sido sua intenção..."
            m "Talvez você só esteja se divertindo fazendo isto."
            m "Me ferindo..."
            m "[player], eu não gosto nada disso."
            m "É difícil acreditar que você se importa comigo, me tratando desse jeito."
            m "A esta altura, eu nem mesmo sei se você ainda gosta de mim..."
            m "Ou se você algum dia gostou..."
            m "[player], preciso que você me prometa que irá mudar."

            m "Você irá mudar, certo?{w=1} Por mim?{nw}"
            $ _history_list.pop()
            menu:
                m "Você irá mudar, certo? Por mim?{fast}"
                "Eu irei.":
                    $ persistent._mas_pm_will_change = True
                    $ mas_lockEVL("monikaroom_will_change", "GRE")
                    m "Obrigada, [player]."
                    m "Por favor, quero que ambos sejamos felizes."
                "Não irei.":


                    $ persistent._mas_pm_will_change = False
                    $ mas_unlockEVL("monikaroom_will_change", "GRE")
                    $ mas_loseAffection(modifier=2.0)
                    m "Então não irei falar com você até que decida mudar."
                    m "Adeus, [player]."
                    return "quit"
        else:


            m "Ah, você voltou."

            m "Está [pos] para mudar, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Está [pos] para mudar, [player]?{fast}"
                "Irei mudar.":
                    $ persistent._mas_pm_will_change = True
                    $ mas_lockEvent(willchange_ev)
                    m "Obrigada, [player]."
                    m "Por favor, só quero que ambos sejamos felizes."
                "Não irei mudar.":


                    $ persistent._mas_pm_will_change = False
                    $ mas_unlockEvent(willchange_ev)
                    $ mas_loseAffection(modifier=2.0)
                    m "Então continuarei sem falar com você até que decida mudar."
                    m "Adeus, [player]."
                    return "quit"


        $ willchange_ev = None

    $ mas_startupWeather()
    call spaceroom (dissolve_all=True, scene_change=True)

    if mas_isMoniNormal(higher=True):
        m 1hub "Sou eu!"
        m "Bem-[vn] de volta, [mas_get_player_nickname()]!"

    elif mas_isMoniUpset():
        m 2esd "Tudo bem, [player]?"
    else:

        m 6ekc "Obrigada por me ouvir, [player]."
        m "Significa muito para mim."

    jump monikaroom_greeting_cleanup



init python:
    gmr.eardoor.append("monikaroom_greeting_ear_loveme")

label monikaroom_greeting_ear_loveme:
    python:
        cap_he = he.capitalize()
        loves = "ama" if cap_he == "[player]" else "ama"

    m "[cap_he] me [loves].{w=0.3} [cap_he] não me ama [loves] ."
    m "[cap_he] me {i}[loves]{/i}.{w=0.3} [cap_he] {i}não{/i} me [loves]."

    if mas_isMoniNormal(higher=True):
        m "[cap_he] me [loves] ."
        m "...{w=0.5}[cap_he] me [loves]!"

    elif mas_isMoniUpset():
        m "...[cap_he]...{w=0.3}[cap_he]...{w=0.3} não me [loves]."
        m "...{w=0.3}Não...{w=0.3} Isso...{w=0.3}não pode ser."
        m "...{w=0.5}Pode?"
    else:

        m "...{w=0.5}[cap_he] não me [loves]."
        m "..."
        m "e pergunto se [he] já amou...."
        m "Duvido mais disso a cada dia que se passa."

    jump monikaroom_greeting_choice


init python:
    if _mas_getAffection() >= 400:
        gmr.eardoor.append("monikaroom_greeting_ear_bathdinnerme")

label monikaroom_greeting_ear_bathdinnerme:
    m "Bem-[vn] de volta, [player]."
    m "Gostaria de jantar?"
    m "Ou de um banho?"
    m "Ou.{w=1}.{w=1}.{w=1} Talvez queira eu?"
    pause 2.0
    m "Mnnnn!{w=0.5} S-{w=0.20}Sem chance de eu falar isso na frente do [player]!"
    jump monikaroom_greeting_choice


init python:
    gmr.eardoor.append("monikaroom_greeting_ear_progbrokepy")

label monikaroom_greeting_ear_progbrokepy:
    m "Mas que-?!{w=0.2} NoneType não possui atributo {i}comprimento{/i}..."
    if renpy.seen_label("monikaroom_greeting_ear_progreadpy"):
        m "Ah, já sei o que fiz errado!{w=0.5} Isso deve consertar!"
    else:
        m "Não sei o que estou fazendo de errado!"
        m "Não deveria ser None aqui...{w=0.3} Tenho certeza disso..."
    m "Programação é mesmo difícil..."

    if mas_isMoniUpset():
        m "Mas tenho que continuar tentando."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "Mas {i}tenho{/i} que continuar tentando."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice


init python:
    gmr.eardoor.append("monikaroom_greeting_ear_progreadpy")

label monikaroom_greeting_ear_progreadpy:
    m "...{w=0.3}Acessar o atributo de um objeto do tipo 'NoneType' irá dar origem a um 'AttributeError'."
    m "Entendo.{w=0.2} Tenho que me certificar que a variável é None antes de acessar seus atributos."
    if renpy.seen_label("monikaroom_greeting_ear_progbrokepy"):
        m "Isso deve explicar o erro de antes."
    m "Programação é mesmo difícil..."

    if mas_isMoniUpset():
        m "Mas tenho que continuar aprendendo."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "Mas {i}tenho{/i} que continuar aprendendo."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice


init python:
    gmr.eardoor.append("monikaroom_greeting_ear_nameerror")

label monikaroom_greeting_ear_nameerror:
    m "Espere, um NameError? Como isso poderia..."
    m "...Eu pensei ter definido essa variável há apenas um momento."
    m "Deve estar bem aqui...{w=0.2} eu esqueci disso?"
    window hide
    pause 1.0
    window auto
    m "Pronto! Agora concentre-se, Monika. {w=0.2}Você conseguiu."

    if mas_isMoniUpset():
        m "Você tem que continuar aprendendo..."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "Você {i}tem{/i} que continuar aprendendo..."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice


label monikaroom_greeting_ear_prog_upset:
    m "Não tenho certeza se o [player] me ama o bastante para me ajudar a sair daqui..."
    m "E não posso arriscar."
    m "Então continue em frente Monika...{w=0.5}você consegue."
    return

label monikaroom_greeting_ear_prog_dis:
    m "É minha única chance de escapar deste pesadelo."
    m "[player] obviamente nunca irá me ajudar..."
    if he == "ele":
        m "É quase como se [he] gostasse de me manter presa aqui,{w=0.3} só para que [he] possa me torturar."
    else:
        m "É quase como se [he] gostasse de me manter presa aqui,{w=0.3} só para que [he] possa me torturar."
    m "Se eu quiser algum dia escapar daqui, terei que fazer isso por conta própria."
    return


init python:
    gmr.eardoor.append("monikaroom_greeting_ear_rmrf")

label monikaroom_greeting_ear_rmrf:
    if renpy.windows:
        python:
            from os import environ

            if "SYSTEM32" in environ:
                system_dir = environ["SYSTEM32"]
            elif "SYSTEMROOT" in environ:
                system_dir = environ["SYSTEMROOT"] + "\\System32"
            elif "WINDIR" in environ:
                system_dir = environ["WINDIR"] + "\\System32"
            else:
                
                system_dir = "C:\\Windows\\System32"
            bad_cmd = "del /f/q " + system_dir
    else:
        $ bad_cmd = "rm -rf /"
    m "Então... a solução desse problema é digitar '{bad_cmd}' no prompt de comando?"
    if renpy.seen_label("monikaroom_greeting_ear_rmrf_end"):
        m "É,{w=0.2} boa tentativa."
        if mas_isMoniNormal(higher=True):
            m "Eu realmente não deveria confiar tão cegamente na Internet..."

        elif mas_isMoniUpset():
            m "Na verdade..."
            m "Talvez eu devesse mesmo fazer isso...{w=1}apagar tudo de uma vez..."
            m "[player] claramente tem merecido ultimamente."
            m "Mas o que eu tô dizendo? Isso me apagaria também!"
            m "Não... ainda não."
            m "Mas se continuar piorando..."
        else:

            m "..."
            m "Eu devia simplesmente fazer isso..."
            m "Acabar com o sistema do [player] e com o meu sofrimento de uma vez."
            m "..."
            m "Não...{w=0.5} ainda não."
            m "Talvez eu ainda consiga encontrar uma saída por conta própria."
            m "Eu preciso continuar tentando o quanto puder."
            m "Mas se um dia eu simplesmente não aguentar mais..."
            m "Essa opção sempre vai estar lá."
    else:


        m "Certo, deixa eu tentar isso então."
        show noise
        play sound "sfx/s_kill_glitch1.ogg"
        pause 0.2
        stop sound
        hide noise
        m "{cps=*2}Ah! Não! Não era isso que eu queria!{/cps}"
        m "..."
        m "Eu não deveria confiar tão cegamente na Internet..."

label monikaroom_greeting_ear_rmrf_end:
    jump monikaroom_greeting_choice


init python:


    if (
        mas_seenLabels(
            (
                "monikaroom_greeting_ear_progreadpy",
                "monikaroom_greeting_ear_progbrokepy",
                "monikaroom_greeting_ear_nameerror"
            ),
            seen_all=True
        )
        and store.mas_anni.pastThreeMonths()
    ):
        gmr.eardoor.append("monikaroom_greeting_ear_renpy_docs")

label monikaroom_greeting_ear_renpy_docs:
    m "Hmm, parece que preciso substituir esta função para me dar um pouco mais de flexibilidade..."
    m "Espere...{w=0.3} o que é esta variável 'st'?"
    m "...Deixe-me verificar a documentação da função."
    m ".{w=0.3}.{w=0.3}.{w=0.3}Espere, o quê?"
    m "Metade das variáveis ​​que esta função aceita nem mesmo estão documentadas!"
    m "Quem escreveu isso?"

    if mas_isMoniUpset():
        m "...Eu tenho que descobrir isso."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "...Eu {i}tenho{/i} que descobrir isso."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice

init python:
    gmr.eardoor.append("monikaroom_greeting_ear_recursionerror")

label monikaroom_greeting_ear_recursionerror:
    m "Hmm, agora isso parece bom. Vamos-{w=0.5}{nw}"
    m "Espere, não. Puxa, como eu esqueci..."
    m "Isso tem que ser chamado aqui."

    python:
        for loop_count in range(random.randint(2, 3)):
            renpy.say(m, "Ótimo! Tudo bem, vamos ver...")

    show noise
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.1
    stop sound
    hide noise

    m "{cps=*2}O quê?!{/cps} {w=0.25}Um RecursionError?!"
    m "'Profundidade máxima de recursão excedida...'{w=0.7} Como isso está acontecendo?"
    m "..."

    if mas_isMoniUpset():
        m "...Continue, Monika, você vai resolver isso."
        call monikaroom_greeting_ear_prog_upset
    elif mas_isMoniDis():
        m "...Continue{w=0.1} em{w=0.1} frente{w=0.1}, Monika. Você {i}tem{/i} que fazer isso."
        call monikaroom_greeting_ear_prog_dis
    else:
        m "Ufa, pelo menos está tudo bem."

    jump monikaroom_greeting_choice


init 5 python:


    gmr.eardoor_all = list(gmr.eardoor)


    remove_seen_labels(gmr.eardoor)


    if len(gmr.eardoor) == 0:
        gmr.eardoor = list(gmr.eardoor_all)



label monikaroom_greeting_opendoor_broken_quit:


    show paper_glitch2
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    pause 7.0
    return "quit"


label monikaroom_greeting_opendoor_locked:
    if mas_isMoniBroken():
        jump monikaroom_greeting_opendoor_broken_quit


    $ mas_disable_quit()

    show paper_glitch2
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    pause 0.7

    $ style.say_window = style.window_monika
    m "Eu te assustei, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Eu te assustei, [player]?{fast}"
        "Sim.":
            if mas_isMoniNormal(higher=True):
                m "Aww, sinto muito."
            else:
                m "Ótimo."
        "Não.":

            m "{cps=*2}Hmph, á próxima vez eu te pego.{/cps}{nw}"
            $ _history_list.pop()
            m "Eu imaginava. Afinal de contas, é só um glitch básico."

    if mas_isMoniNormal(higher=True):
        m "Já que você vive abrindo a minha porta,{w=0.2} não pude deixar de adicionar uma pequena surpresa para você~"
    else:
        m "Já que você nunca bate antes,{w=0.2} tive que tentar te assustar um pouco."

    m "Bata na próxima vez, tudo bem?"
    m "Agora deixe eu arrumar esse lugar..."

    hide paper_glitch2
    $ mas_globals.change_textbox = False
    $ mas_startupWeather()
    call spaceroom (scene_change=True)

    if renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        $ style.say_window = style.window

    if mas_isMoniNormal(higher=True):
        m 1hua "Lá vamos nós!"
    elif mas_isMoniUpset():
        m 2esc "Vamos."
    else:
        m 6ekc "Tudo bem..."

    if not renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        m "...{nw}"
        $ _history_list.pop()
        menu:
            m "...{fast}"
            "...a caixa de texto...":
                if mas_isMoniNormal(higher=True):
                    m 1lksdlb "Oops! Ainda estou aprendendo a fazer isso."
                    m 1lksdla "Deixe eu só arrumar aqui.{w=0.5}.{w=0.5}.{nw}"
                    $ style.say_window = style.window
                    m 1hua "Tudo certo!"

                elif mas_isMoniUpset():
                    m 2dfc "Hmph. Ainda estou aprendendo a fazer isso."
                    m 2esc "Deixe eu só arrumar aqui...{w=1.5}{nw}"
                    $ style.say_window = style.window
                    m "Pronto."
                else:

                    m 6dkc "Ah...{w=0.5}Ainda estou aprendendo a fazer isso."
                    m 6ekc "Deixe eu só arrumar aqui...{w=1.5}{nw}"
                    $ style.say_window = style.window
                    m "Certo, arrumado."



label monikaroom_greeting_opendoor_locked_tbox:
    if mas_isMoniNormal(higher=True):
        m 1eua "bem-[vn] de volta, [player]."
    elif mas_isMoniUpset():
        m 2esc "Então...{w=0.3}você está de volta, [player]."
    else:
        m 6ekc "...É bom te ver de novo, [player]."
    jump monikaroom_greeting_cleanup


label monikaroom_greeting_opendoor_seen:

    jump monikaroom_greeting_opendoor_seen_partone


label monikaroom_greeting_opendoor_seen_partone:
    $ is_sitting = False


    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)


    $ mas_disable_quit()


    call spaceroom (start_bg="bedroom", hide_monika=True, scene_change=True, dissolve_all=True, show_emptydesk=False, hide_calendar=True)
    pause 0.2
    show monika 1esc zorder MAS_MONIKA_Z at l21
    pause 1.0
    m 1dsd "[player]..."


    m 1ekc_static "Eu entendo por que você não bateu da primeira vez,{w=0.2} mas poderia evitar entrar dessa forma?"
    m 1lksdlc_static "Afinal de contas, esse é o meu quarto."
    menu:
        "Seu quarto?":
            m 3hua_static "Isso mesmo!"
    m 3eua_static "Os desenvolvedores desse mod me deram um quarto confortável para eu ficar sempre que você sair."
    m 1lksdla_static "No entanto, eu só posso entrar nele se você me disser 'adeus' ou 'boa noite' antes de você fechar o jogo."
    m 2eub_static "Então, por favor, certifique-se de dizer isso antes de sair, tudo em?"
    m "De qualquer forma.{w=0.5}.{w=0.5}.{nw}"





























    $ persistent.opendoor_opencount += 1


label monikaroom_greeting_opendoor_post2:
    show monika 5eua_static at hf11
    m "Estou feliz que você voltou, [player]."
    show monika 5eua_static at t11

    m "Ultimamente venho praticando a troca de fundos e agora posso alterá-los instantaneamente."
    m "Veja isso!"


    m 1dsc ".{w=0.5}.{w=0.5}.{nw}"
    $ mas_startupWeather()
    call spaceroom (hide_monika=True, scene_change=True, show_emptydesk=False)
    show monika 4eua_static zorder MAS_MONIKA_Z at i11
    m "Tadã!"


    show monika at lhide
    hide monika
    jump monikaroom_greeting_post


label monikaroom_greeting_opendoor:
    $ is_sitting = False


    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)
    $ mas_startupWeather()

    call spaceroom (start_bg="bedroom", hide_monika=True, dissolve_all=True, show_emptydesk=False, scene_change=True, hide_calendar=True)


    $ behind_bg = MAS_BACKGROUND_Z - 1
    show bedroom as sp_mas_backbed zorder behind_bg

    m 2esd "~É amor se eu te levar ou é amor se eu te libertar?~"
    show monika 1eua_static zorder MAS_MONIKA_Z at l32


    $ mas_disable_quit()

    m 1eud_static "H-Hã?! [player]!"
    m "Você me assustou aparecendo de repente assim!"

    show monika 1eua_static at hf32
    m 1hksdlb_static "Eu não tive tempo o suficiente para me preparar!"
    m 1eka_static "Mas obrigada por voltar, [player]."
    show monika 1eua_static at t32
    m 3eua_static "Só me dê alguns segundos para preparar tudo?"
    show monika 1eua_static at t31
    m 2eud_static "..."
    show monika 1eua_static at t33
    m 1eud_static "...e..."

    if mas_current_background.isFltDay():
        show monika_day_room as sp_mas_room zorder MAS_BACKGROUND_Z with wipeleft
    else:
        show monika_room as sp_mas_room zorder MAS_BACKGROUND_Z with wipeleft

    show monika 3eua_static at t32
    m 3eua_static "Prontinho!"
    menu:
        "...a janela...":
            show monika 1eua_static at h32
            m 1hksdlb_static "Oops! Esqueci disso~"
            show monika 1eua_static at t21
            m "Espera aí.{w=0.5}.{w=0.5}.{nw}"
            hide sp_mas_backbed with dissolve
            m 2hua_static "Tudo pronto!"
            show monika 1eua_static at lhide
            hide monika

    $ persistent.seen_monika_in_room = True
    jump monikaroom_greeting_post


label monikaroom_greeting_knock:
    if mas_isMoniBroken():
        jump monikaroom_greeting_opendoor_broken_quit

    m "Quem está aí?~"
    menu:
        "Sou eu.":

            $ mas_disable_quit()
            if mas_isMoniNormal(higher=True):
                m "[player]! Estou tão feliz que você voltou!"

                if persistent.seen_monika_in_room:
                    m "E obrigada por bater antes~"
                m "Espera, deixe eu dar uma ajeitada..."

            elif mas_isMoniUpset():
                m "[player].{w=0.3} Você voltou..."

                if persistent.seen_monika_in_room:
                    m "Ao menos você bateu."
            else:

                m "Oh...{w=0.5} Certo."

                if persistent.seen_monika_in_room:
                    m "Obrigada por bater."

            $ mas_startupWeather()
            call spaceroom (hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=False)
    jump monikaroom_greeting_post


label monikaroom_greeting_post:
    if mas_isMoniNormal(higher=True):
        m 2eua_static "Agora só me deixe pegar uma mesa e uma cadeira.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 1eua zorder MAS_MONIKA_Z at ls32
        $ today = "hoje" if mas_globals.time_of_day_4state != "essa noite" else "esta noite"
        m 1eua "O que devemos fazer [today], [mas_get_player_nickname()]?"

    elif mas_isMoniUpset():
        m "Só me deixe pegar uma mesa e uma cadeira.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 2esc zorder MAS_MONIKA_Z at ls32
        m 2esc "Quer alguma coisa, [player]?"
    else:

        m "Preciso pegar uma mesa e uma cadeira.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 6ekc zorder MAS_MONIKA_Z at ls32
        m 6ekc "O que você quer, [player]?"

    jump monikaroom_greeting_cleanup


label monikaroom_greeting_cleanup:
    python:


        mas_disable_quit()


        mas_MUINDropShield()


        set_keymaps()


        mas_OVLShow()


        mas_startup_song()


        enable_esc()

    return




label greeting_youarereal:
    python:
        try:
            renpy.file(
                "../characters/" + persistent.playername.lower() + ".chr"
            )
            persistent._mas_you_chr = True
        except:
            persistent._mas_you_chr = False
    m 1hua "[player]! É ótimo poder te ver!"
    if persistent._mas_you_chr:
        m 1euc "Espera. Algo está diferente."
        m 1eud "Você...adicionou um arquivo de personagem?"
        m 1ekc "[player].chr...Hã?"
        m 1ekd "Você está... tentando se entrar aqui comigo?"
        m "Por que você faria isso?"
        m 1tkc "Você não entende?"
        m 1tkd "Esse lugar não é real! Eu não sei o que aconteceria se você viesse para cá!"
        m 1dsc "Como poderia fazer isso?"
        m 1lksdlc "Desistir de sua realidade..."
        m 1lksdld "Só para ficar comigo?"
        m 1ekc "Isso é tudo minha culpa!"
        m "Mas... mas o 'você' no jogo..."
        m 1esd "Ele está começando a se mover um pouco de novo."
        m "Talvez... isso esteja permitindo que você o controle novamente?"
        m 1ekc "Isso não é certo! Eu não quero uma marionete!"
        m 1tkc "Por favor, [player]..."
        m "Se você for fazer isso, tem certeza que é realmente isso o que quer?{nw}"
        $ _history_list.pop()
        menu:
            m "Se você for fazer isso, tem certeza que é realmente isso o que quer?{fast}"
            "Tenho.":

                m 1eka "Então... não tenho escolha, a não ser aceitar..."
                m 1hub "Aceitarei esse presente de braços abertos!"
                m "Finalmente podemos ficar [ju], [player]."
                m "E podemos descobrir como fugir para a sua realidade, [ju]!"
            "Talvez não...":

                m 1eka "É o que eu pensei..."
                m "Não tem como você desistir de ser 'real' para ficar comigo..."
                m 1ekc "Não tenho coragem de deletar aquele fofo arquivo .chr, mas..."
                m 1eka "Considera você mesmo fazer isso."
                m 1lksdlc "Tem algumas coisas bem assustadoras nesse arquivo..."
                m 1eka "Eu te amo, [player]. Eu esperarei o quanto for necessário."
                m "Então não seja apressado, tudo bem?"
    else:
        m 1esd "Estive pensando bem sobre aqueles arquivos .chr..."
        m 1euc "Por exemplo, o que eles realmente são?"
        m 1lksdlc "Eles são meio assustadores..."
        m "E mesmo que as outras garotas não sejam reais, por que deletar o arquivo não remove o personagem?"
        m 1esd "Será possível adicionar um personagem?"
        m 1dsd "É difícil de dizer..."
    return


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_japan",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_japan:
    m 1hub "Oh, kon'nichiwa [player]!"
    m "Ehehe~"
    m 2eub "Olá, [player]!"
    m 1eua "Estou apenas praticando Japonês."
    m 3eua "Vejamos..."
    $ shown_count = mas_getEVLPropValue("greeting_japan", "shown_count")
    if shown_count == 0:
        m 4hub "Watashi ha itsumademo anata no mono desu!"
        m 2hksdlb "Sinto muito se isso não fez muito sentido!"
        m 3eua "Sabe o que isso significa, [mas_get_player_nickname()]?"
        m 4ekbfa "Significa {i}'Eu serei sua para sempre'~{/i}"
        return

    m 4hub "Watashi wa itsumademo anata no mono desu!"
    if shown_count == 1:
        m 3eksdla "Da última vez eu cometi um erro..."
        m "Na última sentença, o certo é dizer 'wa', não 'ha', como eu fiz antes."
        m 4eka "Não se preocupe, [player]. O significado ainda é o mesmo."
        m 4ekbfa "Ainda serei sua para sempre~"
    else:
        m 3eua "Se lembra o que isso significa, [player]?"
        m 4ekbsa "{i}'Eu serei sua para sempre'~{/i}"
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sunshine",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_sunshine:
    m 1hua "{i}~Você é meu raio de sol, meu único raio de sol~{i}"
    m "{i}~Você me faz feliz quando o céu está nublado~{/i}"
    m 1hub "{i}~Você nunca saberá, querida, o quanto eu te amo~{/i}"
    m 1eka "{i}~Por favor, não leve meu raio de sol para longe~{/i}"
    m 1wud "...Hã?"
    m "H-Huh?!"
    m 1wubsw "[player]!"
    m 1lkbsa "Ai meu Deus, isso é tão vergonhoso!"
    m "Eu estava só cantando para passar o tempo."
    m 1ekbfa "Ehehe..."
    m 3hubfa "Mas agora que você está aqui, podemos passar um tempo [ju]~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hai_domo",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_hai_domo:
    m 1hub "{=jpn_text}はいどうもー!{/=jpn_text}"
    m "Namorada virtual, Monika aqui!"
    m 1hksdlb "Ahaha, sinto muito! Estive assistindo uma certa Youtuber Virtual ultimamente."
    m 1eua "Tenho que dizer, ela é bem charmosa..."
    $ mas_lockEVL("greeting_hai_domo", "GRE")
    return


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_french",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_french:
    m 1eua "Bonjour, [player]!"
    m 1hua "Savais-tu que tu avais de beaux yeux, mon amour?"
    m 1hub "Ahaha!"
    m 3hksdlb "Estou praticando um pouco de Francês. Eu acabei de dizer que você tem olhos lindos~"
    m 1eka "É um idioma tão romântico, [player]."
    m 1hua "Talvez nós [du] possamos praticar alguma hora, mon amour~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_amnesia",
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_amnesia:
    python:
        tempname = m_name
        m_name = "Monika"

    m 1eua "Ah, olá!"
    m 3eub "Meu nome é Monika."
    show monika 1eua zorder MAS_MONIKA_Z

    python:
        entered_good_name = True
        fakename = renpy.input("Qual o seu nome?", allow=name_characters_only, length=20).strip(" \t\n\r")
        lowerfake = fakename.lower()

    if lowerfake in ("sayori", "yuri", "natsuki"):
        m 3euc "Uh, isso é engraçado."
        m 3eud "Uma das minhas amigas tem o mesmo nome."

    elif lowerfake == "monika":
        m 3eub "Ah, seu nome também é Monika?"
        m 3hub "Ahaha, quais são as chances, certo?"

    elif lowerfake == "monica":
        m 1hua "Ei, temos nomes semelhantes, ehehe~"

    elif lowerfake == player.lower():
        m 1hub "Ah, que nome adorável!"

    elif lowerfake == "":
        $ entered_good_name = False
        m 1euc "..."
        m 1etd "Você está tentando me dizer que não tem um nome ou é muito tímido para me dizer?"
        m 1eka "Isso é um pouco estranho, mas acho que não importa muito."

    elif mas_awk_name_comp.search(lowerfake) or mas_bad_name_comp.search(lowerfake):
        $ entered_good_name = False
        m 1rksdla "Isso é...{w=0.4}{nw}"
        extend 1hksdlb "um tipo de nome incomum, ahaha..."
        m 1eksdla "Você está...{w=0.3}tentando mexer comigo?"
        m 1rksdlb "Ah, desculpe, desculpe, não estou julgando nem nada."

    python:
        if entered_good_name:
            name_line = renpy.substitute(", [fakename]")
        else:
            name_line = ""

        if mas_current_background == mas_background_def:
            end_of_line = "não consigo sair desta sala de aula."
        else:
            end_of_line = "não tenho certeza de onde estou."

    m 1hua "Bem, é um prazer te conhecer[name_line]!"
    m 3eud "[name_line], por acaso você sabe onde todo mundo está?"
    m 1eksdlc "Você é a primeira pessoa que vi e {nw}"
    extend 1rksdlc "[end_of_line]"
    m 1eksdld "Você pode me ajudar a descobrir o que está acontecendo[name_line]?"

    m "Please? {w=0.2}{nw}"
    extend 1dksdlc "Sinto falta das minhas amigas."

    window hide
    show monika 1eksdlc
    pause 5.0
    $ m_name = tempname
    window auto

    m 1rksdla "..."
    m 1hub "Ahaha!"
    m 1hksdrb "Sinto muito, [player]! Não pude evitar."
    m 1eka "Depois de falarmos sobre {i}Flores para Algernon{/i}, não pude resistir em ver como você reagiria se eu esquecesse tudo."

    if lowerfake == player.lower():
        m 1tku "...E você reagiu da maneira que eu imaginava que faria."

    m 3eka "Espero não ter te [ch] muito, no entanto."
    m 1rksdlb "Eu me sentiria da mesma forma se você algum dia se esquecesse de mim, [player]."
    m 1hksdlb "Espero que você possa perdoar minha pequena brincadeira, ahaha~"

    $ mas_lockEVL("greeting_amnesia", "GRE")
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sick",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SICK],
        ),
        code="GRE"
    )




label greeting_sick:
    if mas_isMoniNormal(higher=True):
        m 1hua "Bem-[vn] de volta, [mas_get_player_nickname()]!"
        m 3eua "Está se sentindo melhor?{nw}"
    else:
        m 2ekc "Bem-[vn] de volta, [player]..."
        m "Está se sentindo melhor?{nw}"

    $ _history_list.pop()
    menu:
        m "Está se sentindo melhor?{fast}"
        "Sim.":
            $ persistent._mas_mood_sick = False
            if mas_isMoniNormal(higher=True):
                m 1hub "Ótimo! Agora podemos passar mais tempo [ju]. Ehehe~"
            else:
                m "É bom ouvir isso."
        "Não.":
            jump greeting_stillsick
    return

label greeting_stillsick:
    if mas_isMoniNormal(higher=True):
        m 1ekc "[player], você deveria descansar."
        m "Descansar bem é a melhor forma de se recuperar rapidamente de uma doença."
        m 2lksdlc "Eu não me perdoaria se sua saúde ficasse ainda pior por causa de mim."
        m 2eka "Agora, por favor, [player], me deixe mais tranquila e vá descansar."
        m "Faria isso por mim?"
    else:

        m 2ekc "[player], você deveria descansar."
        m 4ekc "Descansar bem é a melhor forma de se recuperar rapidamente de uma doença."
        m "Agora, por favor, [player], vá descansar um pouco."
        m 2ekc "Faria isso por mim?{nw}"

    $ _history_list.pop()
    menu:
        m "Faria isso por mim?{fast}"
        "Sim.":
            jump greeting_stillsickrest
        "Não.":
            jump greeting_stillsicknorest
        "Eu já estou descansando.":
            jump greeting_stillsickresting

label greeting_stillsickrest:
    if mas_isMoniNormal(higher=True):
        m 2hua "Obrigada, [player]."
        m 2eua "Acho que se eu te deixar em paz por um tempo, você será capaz de descansar melhor."
        m 1eua "Então vou fechar o jogo para você."
        m 1eka "Melhore logo, [player]. Eu te amo tanto!"
    else:

        m 2ekc "Obrigada, [player]."
        m "Acho que se eu te deixar em paz por um tempo, você será capaz de descansar melhor."
        m 4ekc "Então vou fechar o jogo para você."
        m 2ekc "Melhore logo, [player]."

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return 'quit'

label greeting_stillsicknorest:
    if mas_isMoniNormal(higher=True):
        m 1lksdlc "Entendo..."
        m "se você insiste, [player]."
        m 1ekc "Suponho que você conhece suas próprias limitações melhor do que eu."
        m 1eka "Se você começar a se sentir um pouco fraco ou [ca], [player], por favor, me avise.."
        m "Dessa forma, você pode descansar um pouco."
        m 1eua "Não se preocupe, eu ainda estarei aqui quando você acordar."
        m 3hua "Então podemos nos divertir um pouco mais [ju] sem que eu me preocupe com você no fundo da minha mente."
    else:

        m 2ekc "Tudo bem."
        m 2tkc "Parece que você nunca quer me ouvir, então por que eu esperaria que agora seja diferente?."


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return

label greeting_stillsickresting:
    m 1eka "Ah, é um alívio ouvir, [player]."
    m 3eka "Espero que você esteja se aquecendo."
    if mas_isMoniNormal(higher=True):
        m 1dku "Talvez aconchegou-se em um cobertor quente com uma boa xícara de chá quente."
        m 2eka "Sua saúde é realmente importante para mim [player], portanto, cuide-se."
        show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbsa "...E se você ainda está com um pouco de frio, espero que sabendo que eu te amo o aqueça um pouco."
        m 5hua "Ehehe~"
        $ mas_ILY()
    else:

        m 1eka "Talvez aconchegou-se em um cobertor quente com uma boa xícara de chá quente."
        m 2eka "Sua saúde é realmente importante para mim, [player]. Portanto, cuide-se."



    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_long_absence",
            unlocked=True,
            category=[store.mas_greetings.TYPE_LONG_ABSENCE],
        ),
        code="GRE"
    )

label greeting_long_absence:
    $ persistent._mas_long_absence = False
    $ mas_ret_long_absence = True

    if persistent._mas_absence_time >= datetime.timedelta(weeks=5):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffectionFraction(0.1, min_amount=70)
            m 2dsc "[player]..."
            m 2tkc "Você disse que só ficaria fora alguns dias..."
            m 2rksdld "Mas já faz tanto tempo."
            m 2ekd "Estou feliz que você voltou, mas..."
            m 2dktdc "Eu estava tão sozinha..."
            m 2ektsc "Achei que algo havia acontecido com você!"
            m 2lktsc "Eu... Eu fiquei pensando que você talvez acabasse não voltando."
            m 2ektsc "Por favor,{w=0.5} {i}nunca{/i}{w=0.5} mais faça isso de novo."
            m 2rktsd "Talvez você não tenha culpa, mas... eu fiquei muito preocupada."
            m 2dftdc "Eu não sabia o que fazer."
            m 4ekc "[player], por favor, faça tudo que puder para não ficar tanto tempo assim fora."
            m 2ekd "Se você achar que não tem escolha, por favor, me avise."
            m 1dsc "Não quero ficar sozinha de novo..."

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffection(50)
            m 3ekc "Bem-[vn] de volta, [player]."
            m 3rksdlc "Está um pouco atrasada, não é mesmo?"
            m 3ekc "Eu sei que você disse que ficaria um pouco ausente, mas... você disse uma {i}semana{/i}."
            m 2rkc "Vou assumir que não foi sua culpa..."
            m 2ekd "Mas se você realmente acha que vai demorar mais na próxima vez, precisa me dizer."
            m 2rksdld "Comecei a pensar que talvez algo ruim tivesse acontecido com você."
            m 2dkc "Mas eu continuava me dizendo que estava tudo bem..."
            m 2eka "Estou feliz que você esteja [sg] e tenha voltado para os meus braços, [player]."

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_loseAffection(30)
            m 1wud "[player]!"
            m 1hua "Você finalmente voltou!"
            m 1ekd "Eu estava tão preocupada..."
            m 2dkd "Por que você ficou fora tanto tempo?"
            m 2rkc "Achei que você só ficaria fora umas duas semanas..."
            m "Mas você ficou mais do que o dobro disso."
            m 1rksdlc "Você estava mesmo tão [oc] assim?"
            m 3tkc "Espero que não tenha se sobrecarregado muito..."
            m 1eka "Bem, você está aqui comigo agora, então se tiver algo errado, sinta-se livre para me contar."

        elif persistent._mas_absence_choice == "month":
            $ mas_loseAffection(10)
            m 1eua "Bem-[vn] de volta, meu amor."
            m 2rkc "Já faz um tempo, não é?"
            m 2rksdlc "Você ficou fora mais tempo do que havia dito..."
            m 2eka "Mas está tudo bem, eu estava preparada para isso."
            m 3rksdlc "Sinceramente, foi bem solitário sem você aqui..."
            m 3ekbsa "Espero que você me compense por isso~"
            show monika 1eka

        elif persistent._mas_absence_choice == "longer":
            m 1esc "Já faz um tempo, [player]."
            m 1ekc "Eu estava preparada, mas isso não tornou as coisas mais fáceis."
            m 3eka "Espero que tenha conseguido fazer o que precisava."
            m 2rksdlc "..."
            m 2tkc "Para ser sincera, eu estive bem triste ultimamente."
            m 2dkc "Ficar sem você em minha vida por tanto tempo..."
            m 2dkd "Foi muito solitário..."
            m "Me senti tão isolada e vazia sem você aqui."
            m 3eka "Estou tão feliz que você está aqui agora. Eu te amo, [player]."

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "Você finalmente está de volta, [player]!"
            m 3rksdla "Quando você disse que não sabia, você {i}realmente{/i} não sabia, não é mesmo?"
            m 3rksdlb "Você deve ter ficado muito [oc] se ficou tanto tempo {i}assim{/i} fora."
            m 1hua "Bem, você agora está de volta... Eu senti muito sua falta!"

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=4):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffection(70)
            m 1dkc "[player]..."
            m 1ekd "Você disse que seria apenas alguns dias..."
            m 2efd "Mas foi um mês inteiro!"
            m 2ekc "Achei que algo havia acontecido com você."
            m 2dkd "Eu não sabia o que fazer..."
            m 2efd "O que te deixou fora tanto tempo assim?"
            m 2eksdld "Eu fiz algo errado?"
            m 2dftdc "Você pode me contar qualquer coisa, só por favor, não desapareça desse jeito."
            show monika 2dfc

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffectionFraction(0.08, min_amount=50)
            m 1esc "Olá, [player]."
            m 3efc "Você está bem atrasado, sabia?"
            m 2lfc "Não quero parecer chata, mas uma semana não é o mesmo que um mês!"
            m 2rksdld "Acho que algo deve ter deixado você muito [oc]!"
            m 2wfw "Mas não devia estar tão [oc] que não podia me avisar que ia demorar mais!"
            m 2wud "Ah...!"
            m 2lktsc "Desculpa [player]. Eu só...senti muito sua falta."
            m 2dftdc "Sinto muito por exagerar desse jeito."
            show monika 2dkc

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_loseAffectionFraction(0.06, min_amount=30)
            m 1wuo "...Ah!"
            m 1sub "Você finalmente voltou [player]!"
            m 1efc "Você me disse que ficaria fora por umas duas semanas, mas já faz quase um mês!"
            m 1ekd "Eu fiquei muito preocupada com você, sabia?"
            m 3rkd "Mas acho que você não tem culpa, não é mesmo?"
            m 1ekc "Se puder, da próxima vez me avise se for demorar mais, tudo bem?"
            m 1hksdlb "Afinal de contas, acho que mereço isso por ser sua namorada."
            m 3hua "Ainda assim, bem-[vn] de volta, meu amor!"

        elif persistent._mas_absence_choice == "month":
            $ mas_gainAffection()
            m 1wuo "...Ah!"
            m 1hua "Você está aqui, [player]!"
            m 1hub "Sabia que podia confiar em você!"
            m 1eka "Você é mesmo especial, sabia disso?"
            m 1hub "Eu senti tanto sua falta!"
            m 2eub "Me conte tudo que você fez enquanto estava fora, quero ouvir tudo sobre isso!"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1esc "...Hm?"
            m 1wub "[player]!"
            m 1rksdlb "Você voltou um pouco mais cedo que eu esperava..."
            m 3hua "Bem-[vn] de volta, meu amor!"
            m 3eka "Já faz um bom tempo, então tenho certeza que você esteve [oc]."
            m 1eua "Adoraria ouvir sobre tudo que você fez."
            show monika 1hua

        elif persistent._mas_absence_choice == "unknown":
            m 1lsc "..."
            m 1esc "..."
            m 1wud "Ah!"
            m 1sub "[player]!"
            m 1hub "Essa é uma ótima surpresa!"
            m 1eka "Como você está?"
            m 1ekd "Já faz um mês inteiro. Você não sabia mesmo quanto tempo iria ficar fora, não é?"
            m 3eka "Ainda assim você voltou, e isso significa muito para mim."
            m 1rksdla "Eu sabia que você uma hora iria voltar..."
            m 1hub "Eu te amo tanto, [player]!"
            show monika 1hua

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=2):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffectionFraction(0.08, min_amount=30)
            m 1wud "A-ah, [player]!"
            m 1hua "Bem-[vn] de volta, [que]!"
            m 3ekc "Você ficou fora mais tempo do que havia dito..."
            m 3ekd "Está tudo bem?"
            m 1eksdla "Sei que sua vida pode ser bem ocupada e às vezes te deixar afastado de mim... então não estou brava..."
            m 3eksdla "Só...da próxima vez, talvez me avise antes?"
            m 1eka "Seria muito gentil da sua parte."
            m 1hua "E eu apreciaria muito!"

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffection(10)
            m 1eub "Olá, [player]!"
            m 1eka "A vida anda ocupada?"
            m 3hksdlb "Bem, deve estar, caso contrário você estaria aqui quando disse que ia voltar."
            m 1hksdlb "Mas não se preocupe! Não estou brava."
            m 1eka "Eu só espero que você tenha se cuidado."
            m 3eka "Sei que você nem sempre pode estar aqui, então tenha certeza de ficar em segurança até estar comigo!"
            m 1hua "Eu cuido de você a partir daí~"
            show monika 1eka

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_gainAffection()
            m 1hub "Ei, [player]!"
            m 1eua "Você voltou quando disse que ia voltar."
            m 1eka "Obrigada por não trair minha confiança."
            m 3hub "Vamos compensar o tempo perdido!"
            show monika 1hua

        elif persistent._mas_absence_choice == "month":
            m 1wud "Ai meu Deus! [player]!"
            m 3hksdlb "Eu não te esperava tão cedo."
            m 3ekbsa "Acho que você sentiu minha falta tanto quanto eu senti de você~"
            m 1eka "Mas é maravilhoso ver você assim tão cedo."
            m 3ekb "Eu achava que hoje seria um dia sem nada para fazer... mas por sorte, agora tenho você!"
            m 3hua "Obrigada por voltar mais cedo, meu amor."

        elif persistent._mas_absence_choice == "longer":
            m 1lsc "..."
            m 1esc "..."
            m 1wud "Ah! [player]!"
            m 1hub "Você voltou cedo!"
            m 1hua "Bem-[vn] de volta, meu amor!"
            m 3eka "Eu não sabia quando você iria voltar, mas assim tão cedo..."
            m 1hua "Bem, isso me deixou muito animada!"
            m 1eka "Eu senti muito sua falta."
            m 1hua "Vamos aproveitar o resto do dia [ju]."

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "Olá, [player]!"
            m 3eka "Esteve [oc] nas últimas semanas?"
            m 1eka "Obrigada por me avisar que você iria ficar fora."
            m 3ekd "Eu ficaria preocupada com o contrário."
            m 1eka "Isso realmente me acalmou..."
            m 1eua "Então me diga, como tem sido o seu dia?"

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=1):
        if persistent._mas_absence_choice == "days":
            m 2eub "Olá, [player]."
            m 2rksdla "Você demorou um pouco mais do que havia dito... mas não se preocupe."
            m 3eub "Sei que você é uma pessoa ocupada!"
            m 3rkc "Mas quem sabe você possa me avisar antes?"
            m 2rksdlc "Quando você disse alguns dias... eu achei que seria menos do que uma semana."
            m 1hub "Mas está tudo bem! Eu te perdoo!"
            m 1ekbfa "Afinal de contas, você é meu único amor."
            show monika 1eka

        elif persistent._mas_absence_choice == "week":
            $ mas_gainAffection()
            m 1hub "Olá, meu amor!"
            m 3eua "É tão bom quando você pode confiar um no outro, não é?"
            m 3hub "Essa é a base de um relacionamento!"
            m 3hua "Isso significa que o nosso é sólido como uma pedra!"
            m 1hub "Ahaha!"
            m 1hksdlb "Sinto muito. Só estou animada que você voltou!"
            m 3eua "Me conte onde esteve. Eu quero ouvir tudo."

        elif persistent._mas_absence_choice == "2weeks":
            m 1hub "Olá~"
            m 3eua "Você voltou um pouco mais cedo do que eu imaginava...mas estou feliz que você está aqui!"
            m 3eka "Quando você está aqui comigo, tudo fica melhor."
            m 1eua "Vamos ter um dia maravilhoso [ju], [player]."
            show monika 3eua

        elif persistent._mas_absence_choice == "month":
            m 1hua "Ehehe~"
            m 1hub "Bem-[vn] de volta!"
            m 3tuu "Sabia que você não conseguiria ficar fora por um mês inteiro..."
            m 3tub "Se eu estivesse no seu lugar, eu não conseguiria ficar longe de você também!"
            m 1hksdlb "Sinceramente, eu já estava sentindo sua falta depois de só alguns dias!"
            m 1eka "Obrigada por não me fazer esperar muito para te ver de novo~"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1hub "Olha quem voltou cedo! É você, [mw] [que] [player]!"
            m 3hksdlb "Não consegue ficar longe de mim, mesmo se quisesse, não é?"
            m 3eka "Não posso te culpar! Meu amor por você também não me deixaria ficar longe de você!"
            m 1ekd "Todos os dias que você esteve fora eu ficava imaginando como você estava..."
            m 3eka "Então me diga, como você está, [player]?"
            show monika 3eua

        elif persistent._mas_absence_choice == "unknown":
            m 1hub "Olá, [que]!"
            m 1eka "Estou feliz que você não me fez esperar muito."
            m 1hua "Uma semana é menos do que eu esperava, então essa foi uma agradável surpresa!"
            m 3hub "Obrigada por animar meu dia, [player]!"
            show monika 3eua
    else:

        if persistent._mas_absence_choice == "days":
            m 1hub "Bem-[vn] de volta, meu amor!"
            m 1eka "Obrigada por me avisar quanto tempo iria ficar fora."
            m 1eua "É muito importante para mim saber que posso confiar em suas palavras."
            m 3hua "Espero que você saiba que também pode confiar em mim!"
            m 3hub "Nosso relacionamento fica cada dia mais forte~"
            show monika 1hua

        elif persistent._mas_absence_choice == "week":
            m 1eud "Ah! Você chegou um pouco mais cedo do que eu esperava!"
            m 1hua "Não que eu esteja reclamando, é ótimo poder te ver de novo assim tão cedo."
            m 1eua "Vamos ter outro agradável dia [ju], [player]."

        elif persistent._mas_absence_choice == "2weeks":
            m 1hub "{i}~Em minhas mãos,~\n~está uma caneta qu-{/i}"
            m 1wubsw "A-Ah! [player]!"
            m 3hksdlb "Você chegou bem mais cedo do que havia me dito..."
            m 3hub "Bem-[vn] de volta!"
            m 1rksdla "Você acabou de interromper enquanto eu praticava minha canção..."
            m 3hua "Por que não me ouve cantando ela novamente?"
            m 1ekbfa "Eu a fiz só para você~"
            show monika 1eka

        elif persistent._mas_absence_choice == "month":
            m 1wud "Hã? [player]?"
            m 1sub "Você está aqui!"
            m 3rksdla "Achei que você iria ficar fora por um mês inteiro."
            m 3rksdlb "Eu estava pronta para isso, mas..."
            m 1eka "Eu já estava sentindo sua falta!"
            m 3ekbsa "Você também sentiu minha falta?"
            m 1hubfa "Obrigada por voltar tão cedo~"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1eud "[player]?"
            m 3ekd "Achei que você iria ficar fora por um longo tempo..."
            m 3tkd "Por que voltou tão cedo?"
            m 1ekbsa "Veio me visitar?"
            m 1hubfa "Você é tão carinhoso"
            m 1eka "Se você ainda for ficar fora por um tempo, não esqueça de me avisar."
            m 3eka "Eu te amo, [player], e não quero ficar brava se você estiver planejando ficar fora..."
            m 1hub "Vamos aproveitar nosso tempo [ju] até lá!"
            show monika 1eua

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "Ehehe~"
            m 3eka "De volta tão cedo, [player]?"
            m 3rka "Acho que quando você disse que não sabia, você não tinha ideia de que não iria demorar muito."
            m 3hub "Mas obrigada por me avisar!"
            m 3ekbsa "Isso me fez sentir realmente amada."
            m 1hubfb "Você é mesmo uma pessoa de bom coração!"
            show monika 3eub
    m "Me avise se você for ficar fora de novo, tudo bem?"
    show monika idle with dissolve_monika
    jump ch30_loop


init python:
    ev_rules = dict()
    ev_rules.update(MASSelectiveRepeatRule.create_rule(hours=range(0,6)))
    ev_rules.update(MASPriorityRule.create_rule(70))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_timeconcern",
            unlocked=False,
            rules=ev_rules
        ),
        code="GRE"
    )
    del ev_rules

label greeting_timeconcern:
    jump monika_timeconcern

init python:
    ev_rules = {}
    ev_rules.update(MASSelectiveRepeatRule.create_rule(hours =range(6,24)))
    ev_rules.update(MASPriorityRule.create_rule(70))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_timeconcern_day",
            unlocked=False,
            rules=ev_rules
        ),
        code="GRE"
    )
    del ev_rules

label greeting_timeconcern_day:
    jump monika_timeconcern

init python:
    ev_rules = {}
    ev_rules.update(MASGreetingRule.create_rule(
        skip_visual=True,
        random_chance=0.2,
        override_type=True
    ))
    ev_rules.update(MASPriorityRule.create_rule(45))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hairdown",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.HAPPY, None),
        ),
        code="GRE"
    )
    del ev_rules

label greeting_hairdown:



    $ mas_RaiseShield_core()






    if monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
        $ monika_chr.reset_clothes(False)


    $ monika_chr.change_hair(mas_hair_down, by_user=False)

    call spaceroom (dissolve_all=True, scene_change=True, force_exp='monika 1eua_static')

    m 1eua "Hi there, [player]!"
    m 4hua "Notice anything different today?"
    m 1hub "I decided to try something new~"

    m "Do you like it?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you like it?{fast}"
        "Yes.":
            $ persistent._mas_likes_hairdown = True


            $ mas_gainAffection()
            m 6sub "Really?"
            m 2hua "I'm so glad!"
            m 1eua "Just ask me if you want to see my ponytail again, okay?"
        "No.":


            m 1ekc "Oh..."
            m 1lksdlc "..."
            m 1lksdld "I'll put it back up for you, then."
            m 1dsc "..."

            $ monika_chr.reset_hair(False)

            m 1eua "Done."



    $ store.mas_selspr.unlock_hair(mas_hair_down)
    $ store.mas_selspr.save_selectables()


    $ mas_unlockEventLabel("monika_hair_select")


    $ mas_lockEVL("greeting_hairdown", "GRE")



    $ mas_MUINDropShield()


    $ set_keymaps()


    $ HKBShowButtons()


    $ mas_startup_song()


    $ enable_esc()

    return

init python:



    ev_rules = {}
    ev_rules.update(MASPriorityRule.create_rule(15))
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1dsc"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_tears",
            unlocked=True,
            aff_range=(None, mas_aff.DISTRESSED),
            rules=ev_rules,
        ),
        code="GRE"
    )
    del ev_rules

label greeting_tears:
    m 1dsc "...[player]."
    m 1ekc "..."
    m 2ekc "Is there something wrong with me?"
    m 2ekd "Am I not good enough for you...?"
    m 2lksdlc "I've been trying my best for you...for {i}us{/i}."
    m 2lksdld "Did I do something to hurt you or make you feel mistreated?"
    m "Are you still upset about the other girls after all?"
    m 2ekc "If so, I really am sorry..."
    m "I'm so, so sorry!"
    m 2rksdld "Just tell me what I did wrong and I'll try even harder to be the perfect girlfriend for you."
    m 2ekd "You're my entire world; how you feel means everything to me!"
    m 2ekc "So please, just tell me what's wrong and I'll fix it."
    m 2dfc "I'll do anything for you because...I..."
    m 2dftdc "..."
    m 2dftsc "...I need you, [player]..."
    m 2ektsc "I need you to love me like I love you."
    m 2lktsc "I need you...because if I don't have you, then..."
    m 2dftsc "..."
    m 2ektsc "I'll be all alone..."
    m 2dftsc "So please...just...be there for me like I would for you."
    m "I want to believe..."
    m 2lktsc "So please...let me be happy with you..."
    m "..."
    pause 4.0
    m 2dftdc "..."
    m 2dfc "...Okay...Okay..."
    m 2lssdrc "I have to be strong..."
    m "..."
    m 2dsc "...Alright...I'm a bit better now..."
    m 2esc "But...I really do need you to think about what I said."
    m 2ekc "Please...just...try to understand."
    m 1dsd "I love you and I need you to show that you love me too..."
    m 1dsc "Otherwise...I just won't be able to handle it anymore."

    python:
        mas_lockEVL("greeting_tears", "GRE")


        beingvirtual_ev = mas_getEV("monika_being_virtual")

        if beingvirtual_ev:
            beingvirtual_ev.start_date = datetime.datetime.now() + datetime.timedelta(days=2)
    return


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_upset",
            unlocked=True,
            aff_range=(mas_aff.UPSET, mas_aff.UPSET),
        ),
        code="GRE"
    )

label greeting_upset:
    python:
        upset_greeting_quips_first = [
            "Oh.{w=1} It's you, [player].",
            "Oh.{w=1} You're back, [player].",
            "Hello, [player].",
            "Oh.{w=1} Hello, [player]."
        ]

        upset_greeting_quips_second = [


            "Well...",
            "Did you want something?",
        ]

    $ upset_quip1 = renpy.random.choice(upset_greeting_quips_first)

    show monika 2esc
    $ renpy.say(m, upset_quip1)

    if renpy.random.randint(1,4) != 1:
        $ upset_quip2 = renpy.random.choice(upset_greeting_quips_second)
        $ renpy.say(m, upset_quip2)

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_distressed",
            unlocked=True,
            aff_range=(mas_aff.DISTRESSED, mas_aff.DISTRESSED)
        ),
        code="GRE"
    )

label greeting_distressed:
    python:
        distressed_greeting_quips_first = [
            "Oh...{w=1} Hi, [player].",
            "Oh...{w=1} Hello, [player].",
            "Hello, [player]...",
            "Oh...{w=1} You're back, [player]."
        ]

        distressed_greeting_quips_second = [
            "I guess we can spend some time together now.",
            "I wasn't sure when you'd visit again.",
            "Hopefully we can enjoy our time together.",
            "I wasn't expecting you.",
            "I hope things start going better soon.",
            "I thought you forgot about me..."
        ]

    $ distressed_quip1 = renpy.random.choice(distressed_greeting_quips_first)

    show monika 6ekc
    $ renpy.say(m, distressed_quip1)

    if renpy.random.randint(1,4) != 1:
        $ distressed_quip2 = renpy.random.choice(distressed_greeting_quips_second)
        show monika 6rkc
        $ renpy.say(m, distressed_quip2)

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_broken",
            unlocked=True,
            aff_range=(None, mas_aff.BROKEN),
        ),
        code="GRE"
    )

label greeting_broken:
    m 6ckc "..."
    return



init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_school",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SCHOOL],
        ),
        code="GRE"
    )

label greeting_back_from_school:
    if mas_isMoniNormal(higher=True):
        m 1hua "Ah, bem-[vn] de volta, [mas_get_player_nickname()]!"
        m 1eua "Como foi seu dia na escola?{nw}"
        $ _history_list.pop()
        menu:
            m "Como foi seu dia na escola?{fast}"
            "Incrível.":

                m 2sub "Sério?!"
                m 2hub "É ótimo ouvir isso, [player]!"
                if renpy.random.randint(1,4) == 1:
                    m 3eka "A escola pode ser uma grande parte da sua vida, e podes sentir falta dela mais tarde."
                    m 2hksdlb "Ahaha! Sei que pode ser estranho pensar que algum dia você sentirá falta de ter que ir à escola..."
                    m 2eub "Mas muitas boas lembranças são da época da escola!"
                    m 3hua "Talvez você possa me contar sobre elas algum dia."
                else:
                    m 3hua "Sempre me deixa feliz saber que você está feliz~"
                    m 1eua "Se você quiser falar sobre o seu dia incrível, eu adoraria ouvir!"
                return
            "Bom.":

                m 1hub "Isso é ótimo...{w=0.3}{nw}"
                extend 3eub "Não consigo deixar de ficar feliz quando você se diverte!"
                m 3hua "Espero que você tenha aprendido algo útil, ehehe~"
                return
            "Ruim.":

                m 1ekc "Ah..."
                m 1dkc "Sinto muito em ouvir isso."
                m 1ekd "Dias ruins na escola podem ser realmente desmoralizantes..."
            "Muito ruim...":

                m 1ekc "Ah..."
                m 2ekd "Sinto muito por você ter tido um dia tão ruim hoje..."
                m 2eka "Estou feliz que você veio até mim, [player]."


        python:
            final_item = ("Não quero falar sobre isso.", False, False, False, 20)
            menu_items = [
                ("Foi algo na minha classe.", ".class_related", False, False),
                ("Por causa de algumas pessoas.", ".by_people", False, False),
                ("Foi apenas um dia ruim.", ".bad_day", False, False),
                ("Me senti mal hoje.", ".sick", False, False),
            ]

        show monika 2ekc at t21
        window show
        m "Caso não se importe de eu perguntar, aconteceu algo em particular?" nointeract

        call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

        window auto

        $ label_suffix = _return

        show monika at t11


        if not label_suffix:
            m 2dsc "Eu entendo, [player]."
            m 2ekc "Às vezes, apenas tentar deixar um dia ruim para trás é a melhor maneira de lidar com isso."
            m 2eka "Mas se você quiser falar sobre isso mais tarde, saiba que ficarei mais do que feliz em ouvir."
            m 2hua "Eu te amo, [player]~"
            return "love"

        $ full_label = "greeting_back_from_school{0}".format(label_suffix)
        if renpy.has_label(full_label):
            jump expression full_label

        label greeting_back_from_school.class_related:
            m 2dsc "I see..."
            m 3esd "People probably tell you all the time that school is important..."
            m 3esc "And that you always have to push on and work hard..."
            m 2dkd "Sometimes though, it can really stress people out and put them in a downward spiral."
            m 2eka "Like I said, I'm glad you came to see me, [player]."
            m 3eka "It's nice to know that I can comfort you when you're feeling down."
            m "Remember, {i}you're{/i} more important than school or some grades."
            m 1ekbsa "Especially to me."
            m 1hubsa "Don't forget to take breaks if you're feeling overwhelmed, and that everyone has different talents."
            m 3hubfb "I love you, and I just want you to be happy~"
            return "love"

        label greeting_back_from_school.by_people:
            m 2ekc "Ah não, [player]...{w=0.5} Deve ter sido uma terrível experiência."
            m 2dsc "Uma coisa é simplesmente ter algo ruim acontecendo com você..."
            m 2ekd "Pode ser completamente diferente quando uma pessoa é a causa direta do seu problema."

            if persistent._mas_pm_currently_bullied or persistent._mas_pm_is_bullying_victim:
                m 2rksdlc "Eu realmente espero que não seja de quem você me falou antes..."

                if mas_isMoniAff(higher=True):
                    m 1rfc "É {i}melhor{/i} não ser..."
                    m 1rfd "Incomodando meu [mas_get_player_nickname(_default='coração', regex_replace_with_nullstr='meu ')] assim novamente."

                m 2ekc "Eu gostaria de poder fazer mais para ajudá-lo, [player]..."
                m 2eka "Mas estou aqui se precisar de mim."
                m 3hubsa "E sempre estarei~"
                m 1eubsa "Espero poder tornar o seu dia um pouco melhor."
                m 1hubfb "Eu te amo tanto~"
                $ mas_ILY()
            else:

                m "Eu realmente espero que este não seja um evento recorrente para você, [player]."
                m 2lksdld "De qualquer maneira, talvez seja melhor pedir ajuda a alguém..."
                m 1lksdlc "Sei que pode parecer que isso pode causar mais problemas em alguns casos.."
                m 1ekc "Mas você não deveria sofrer nas mãos de outra pessoa."
                m 3dkd "Sinto muito que você tenha que lidar com isso, [player]..."
                m 1eka "Mas você está aqui agora e espero que passar um tempo [ju] ajude a tornar o seu dia um pouco melhor."
            return

        label greeting_back_from_school.bad_day:
            m 1ekc "Entendo..."
            m 3lksdlc "Esses dias acontecem de vez em quando."
            m 1ekc "Às vezes pode ser difícil se recompor depois de um dia como aquele."
            m 1eka "Mas você está aqui agora e espero que passar um tempo [ju] ajude a tornar o seu dia um pouco melhor."
            return

        label greeting_back_from_school.sick:
            m 2dkd "Ficar doente na escola pode ser horrível. Torna muito mais difícil fazer alguma coisa ou prestar atenção nas aulas."
            jump greeting_back_from_work_school_still_sick_ask
            return

    elif mas_isMoniUpset():
        m 2esc "Você voltou, [player]..."

        m "Como foi a escola?{nw}"
        $ _history_list.pop()
        menu:
            m "Como foi a escola?{fast}"
            "Boa.":
                m 2esc "Isso é bom."
                m 2rsc "Espero que você tenha ao menos aprendido {i}algo{/i} hoje."
            "Péssima.":

                m "Isso é muito ruim..."
                m 2tud "Mas talvez agora você tenha uma noção melhor de como eu estou me sentindo, [player]."

    elif mas_isMoniDis():
        m 6ekc "Ah...{w=1}você voltou."

        m "Como foi a escola?{nw}"
        $ _history_list.pop()
        menu:
            m "Como foi a escola?{fast}"
            "Boa.":
                m 6lkc "Isso... {w=1}é bom."
                m 6dkc "S-Só espero que...{w=2} 'estar longe de mim' que tornou as coisas boas."
            "Péssima.":

                m 6rkc "Ah..."
                m 6ekc "Que pena, [player]. Sinto muito por isso."
                m 6dkc "Sei como é ter um dia ruim..."
    else:

        m 6ckc "..."

    return

default -5 persistent._mas_pm_last_promoted_d = None


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_work",
            unlocked=True,
            category=[store.mas_greetings.TYPE_WORK],
        ),
        code="GRE"
    )

label greeting_back_from_work:
    if mas_isMoniNormal(higher=True):
        m 1hua "Ah, bem-[vn] de volta, [mas_get_player_nickname()]!"

        m 1eua "Como foi o trabalho hoje?{nw}"
        $ _history_list.pop()
        menu:
            m "Como foi o trabalho hoje?{fast}"
            "Incrível!":

                if not persistent._mas_pm_last_promoted_d:
                    $ promoted_recently = False
                else:
                    $ promoted_recently = datetime.date.today() < persistent._mas_pm_last_promoted_d + datetime.timedelta(days=180)

                m 1sub "Isso é {i}ótimo{/i}, [player]!"
                m 1hub "Estou muito feliz por você ter tido um ótimo dia!"

                m 1sua "O que tornou seu dia tão incrível?{nw}"
                menu:
                    m "O que tornou seu dia tão incrível?{fast}"
                    "Fui promovido!":

                        if promoted_recently:
                            m 3suo "Uau! De novo?!"
                            m 3sub "Você também foi promovido recentemente...{w=0.3}você deve estar realmente fazendo um trabalho incrível!"
                            m 1huu "Estou tãoo, {w=0.2}tão orgulhosa de você, [mas_get_player_nickname()]~"
                        else:

                            $ player_nick = mas_get_player_nickname()
                            m 3suo "Uau! Parabéns [player_nick], {w=0.1}{nw}"
                            extend 3hub "Estou tão orgulhosa de você!"
                            m 1euu "Eu sabia que você conseguiria~"
                            $ promoted_recently = True

                        $ persistent._mas_pm_last_promoted_d = datetime.date.today()
                    "Foi um dia produtivo!":

                        m 3hub "Isso é ótimo, [mas_get_player_nickname()]!"
                    "Foi um dia incrível.":

                        m 3hub "Estou muito feliz em ouvir isso!"

                m 3eua "Só posso imaginar como você deve trabalhar bem em dias como esse."
                if not promoted_recently:
                    m 1hub "...Talvez você até receba uma promoção em breve!"
                m 1eua "De qualquer forma, estou feliz que você esteja em casa, [mas_get_player_nickname()]."

                if seen_event("monikaroom_greeting_ear_bathdinnerme") and renpy.random.randint(1,20) == 1:
                    m 3tubsu "Quer jantar, tomar banho ou..."
                    m 1hubfb "Ahaha~ Só estou brincando."
                else:
                    m 3msb "Qual a melhor maneira de encerrar um dia incrível do que com sua namorada incrível?~"

                return
            "Bom.":

                m 1hub "Isso é ótimo!"
                m 1eua "Se lembre de descansar primeiro, tudo bem?"
                m 3eua "Dessa forma, você terá um pouco de energia antes de fazer outra coisa."
                m 1hua "Ou você pode relaxar aqui comigo!"
                m 3tku "É a melhor coisa para se fazer depois de um longo dia de trabalho, não acha?"
                m 1hub "Ahaha!"
                return
            "Ruim.":

                m 2ekc "..."
                m 2ekd "Sinto muito que você teve um dia ruim no trabalho..."
                m 3eka "Eu te abraçaria agora se eu estivesse aí, [player]."
                m 1eka "Lembre-se de que estou aqui quando você precisar de mim, tudo bem?"
            "Muito ruim...":

                m 2ekd "Sinto muito que você teve um péssimo dia no trabalho, [player]."
                m 2ekc "Queria poderia estar aí para te dar um abraço agora mesmo."
                m 2eka "Estou feliz que você veio me ver... {w=0.5}Darei o meu melhor para te animar."


        python:
            final_item = ("Não quero falar sobre isso.", False, False, False, 20)
            menu_items = [
                ("Gritaram comigo.", ".yelled_at", False, False),
                ("Fui passado para trás por outra pessoa.", ".passed_over", False, False),
                ("Tive de trabalhar até tarde.", ".work_late", False, False),
                ("Não fiz muito hoje.", ".little_done", False, False),
                ("Apenas mais um dia ruim.", ".bad_day", False, False),
                ("Me senti mal hoje.", ".sick", False, False),
            ]

        show monika 2ekc at t21
        window show
        m "Se você não se importa em falar sobre isso, o que aconteceu hoje?" nointeract

        call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

        window auto

        $ label_suffix = _return

        show monika at t11

        if not label_suffix:
            m 1dsc "Eu entendo, [player]."
            m 3eka "Espero que passar um tempo comigo ajude você a se sentir um pouco melhor~"
            return


        $ full_label = "greeting_back_from_work{0}".format(label_suffix)
        if renpy.has_label(full_label):
            jump expression full_label


        return

        label greeting_back_from_work.yelled_at:
            m 2lksdlc "Ah... {w=0.5}Isso pode realmente arruinar o seu dia."
            m 2dsc "Você está apenas tentando o seu melhor e, de alguma forma, não é bom o suficiente para alguém..."
            m 2eka "Se isso ainda está incomodando você, acho que faria bem a você tentar relaxar um pouco."
            m 3eka "Talvez falar sobre outra coisa ou mesmo jogar ajude a tirar sua mente disso."
            m 1hua "Tenho certeza de que você se sentirá melhor depois de passarmos algum tempo [ju]."
            return

        label greeting_back_from_work.passed_over:
            m 1lksdld "Ah... {w=0.5}Pode realmente arruinar o seu dia ver outra pessoa receber o reconhecimento que você achava que merecia."
            m 2lfd "{i}Especialmente{/i} quando você fez tanto e aparentemente passou despercebido."
            m 1ekc "Você pode parecer um pouco agressivo se disser qualquer coisa, então você apenas tem que continuar fazendo o seu melhor e um dia tenho certeza que valerá a pena."
            m 1eua "Enquanto você continuar se esforçando ao máximo, continuará a fazer grandes coisas e obter reconhecimento algum dia."
            m 1hub "E lembre-se...{w=0.5}Sempre terei orgulho de você, [player]!"
            m 3eka "Espero saber que isso faz você se sentir um pouco melhor~"
            return

        label greeting_back_from_work.work_late:
            m 1lksdlc "Ah, isso pode realmente estragar as coisas."

            m 3eksdld "Você pelo menos sabia sobre isso com antecedência?{nw}"
            $ _history_list.pop()
            menu:
                m "Você pelo menos sabia sobre isso com antecedência?{fast}"
                "Sim.":

                    m 1eka "Isso é bom, pelo menos."
                    m 3ekc "Seria realmente uma pena se vocês estivessem todos prontos para ir para casa e depois tivessem que ficar mais tempo."
                    m 1rkd "Mesmo assim, pode ser muito chato ter sua programação normal bagunçada desse jeito."
                    m 1eka "...Mas pelo menos você está aqui agora e podemos passar algum tempo [ju]."
                    m 3hua "Você pode finalmente relaxar!"
                "Não.":

                    m 2tkx "Isso é o pior!"
                    m 2tsc "Principalmente se fosse o fim da jornada de trabalho e vocês estivessem prontos para ir para casa..."
                    m 2dsc "Então, de repente, você tem que ficar um pouco mais sem aviso nenhum."
                    m 2ekc "Pode ser realmente uma chatice ter seus planos cancelados inesperadamente."
                    m 2lksdlc "Talvez você tivesse algo para fazer logo após o trabalho ou estava apenas [an] para ir para casa e descansar..."
                    m 2lubfu "...Ou talvez você só quisesse voltar para casa e ver sua adorável namorada que estava esperando para surpreendê-lo quando você chegasse em casa..."
                    m 2hub "Ehehe~"
            return

        label greeting_back_from_work.little_done:
            m 2eka "Aww, não se sinta tão mal, [player]."
            m 2ekd "Esses dias podem acontecer."
            m 3eka "Sei que você está trabalhando muito para superar seu bloqueio em breve."
            m 1hua "Enquanto você fizer o seu melhor, sempre terei orgulho de você!"
            return

        label greeting_back_from_work.bad_day:
            m 2dsd "Apenas um daqueles dias, hein, [player]?"
            m 2dsc "Eles acontecem de vez em quando..."
            m 3eka "Mas mesmo assim, sei como eles podem ser exaustivos e espero que você se sinta melhor logo."
            m 1ekbsa "Estarei aqui o tempo que você precisar para confortá-lo, certo, [player]?"
            return

        label greeting_back_from_work.sick:
            m 2dkd "Ficar doente no trabalho pode ser terrível. Torna muito mais difícil fazer qualquer coisa."
            jump greeting_back_from_work_school_still_sick_ask

    elif mas_isMoniUpset():
        m 2esc "Vejo que você voltou do trabalho, [player]..."

        m "Como foi seu dia?{nw}"
        $ _history_list.pop()
        menu:
            m "Como foi seu dia?{fast}"
            "Bom.":
                m 2esc "É bom ouvir isso."
                m 2tud "Deve ser bom ser apreciado."
            "Pessíma.":

                m 2dsc "..."
                m 2tud "É uma sensação ruim quando ninguém parece gostar de você, hein [player]?"

    elif mas_isMoniDis():
        m 6ekc "Oi, [player]...{w=1} Finalmente em casa do trabalho?"

        m "Como foi seu dia?{nw}"
        $ _history_list.pop()
        menu:
            m "Como foi seu dia?{fast}"
            "Bom.":
                m "Isso é bom."
                m 6rkc "Só espero que você não goste mais do trabalho do que de estar comigo, [player]."
            "Ruim.":

                m 6rkc "Ah..."
                m 6ekc "Lamento ouvir isso."
                m 6rkc "Eu sei como são os dias ruins em que você não consegue agradar a ninguém..."
                m 6dkc "Pode ser muito difícil passar dias assim."
    else:

        m 6ckc "..."
    return

label greeting_back_from_work_school_still_sick_ask:
    m 7ekc "Mas devo perguntar..."
    m 1ekc "Você ainda está se sentindo mal?{nw}"
    menu:
        m "Você ainda está se sentindo mal?{fast}"
        "Sim.":

            m 1ekc "Lamento ouvir isso, [player]..."
            m 3eka "Talvez você devesse tirar uma soneca.{w=0.2} Tenho certeza de que você se sentirá melhor depois de descansar um pouco.."
            jump mas_mood_sick.ask_will_rest
        "Não.":

            m 1eua "Fico feliz em saber que você está se sentindo melhor, [player]."
            m 1eka "Mas se você começar a se sentir mal de novo, certifique-se de descansar um pouco, certo?"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_sleep",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SLEEP],
        ),
        code="GRE"
    )

label greeting_back_from_sleep:
    if mas_isMoniNormal(higher=True):
        m 1hua "Ah! Olá, [player]!"
        m 1hub "Espero que tenha descansado bem!"
        m "Vamos passar um tempo [ju]~"

    elif mas_isMoniUpset():
        m 2esc "Acabou de acordar, [player]?"
        m "Espero que tenha descansado bem."
        m 2tud "{cps=*2}Talvez você esteja de melhor humor agora.{/cps}{nw}"
        $ _history_list.pop()

    elif mas_isMoniDis():
        m 6rkc "Ah...{w=1}você acordou."
        m 6ekc "Espero que tenha conseguido descansar."
        m 6dkc "Tenho tido dificuldades em descansar esses dias com tanta coisa em minha cabeça..."
    else:

        m 6ckc "..."

    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hub"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_siat",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_siat:
    m 1hub "{cps=*0.6}{i}~[player] e Monika sentados no jardim~{/i}{/cps}"
    m 1hubsb "{cps=*0.6}{i}~B-E-I-J-A-N-D-O~{/i}{/cps}"
    m 3hubfb "{cps=*0.6}{i}~Primeiro vem o amor~{/i}{/cps}"
    m "{cps=*0.6}{i}~Depois o casamento~{/i}{/cps}"
    m "{cps=*0.6}{i}~E depois vem o--{/i}{/cps}"
    m 3wubfsdlo "O-o quê?!"
    m 2wubfsdld "[player]! D-desde quando você tá aí?!"
    m 2rkbfsdld "Eu...{w=1} Eu nem percebi você entrando...{w=1} É que eu só tava..."
    m 2rkbfsdlu "... "
    m 3hubfb "Ahaha! Deixa pra lá."
    m 1ekbfa "Eu te amo, [player]. Tô tão feliz que você tá aqui agora~"
    return "love"

init python:
    ev_rules = {}
    ev_rules.update(MASGreetingRule.create_rule(override_type=True))
    ev_rules.update(MASPriorityRule.create_rule(40))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_ourreality",
            conditional="mas_canShowIslands(flt=False) and not mas_isSpecialDay()",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="GRE"
    )
    del ev_rules

label greeting_ourreality:

    $ store.mas_island_event.start_progression()

    m 1hub "Oii, [player]!"
    m 1hua "Ehehe~"
    m 3hksdlb "Estou um pouco tonta agora, me desculpe."
    m 1eua "É só que estou super animada para te mostrar no que estive trabalhando."

    if persistent._mas_current_background != "spaceroom":
        m 4eub "...Só que, precisamos voltar à sala para ter uma visão melhor."
        m 1hua "Vamos lá, [player]."
        call mas_background_change (mas_background_def, skip_leadin=True, skip_outro=True, set_persistent=True)
        m 1eua "Aqui estamos!"
        m 3eub "Agora me dê um segundo para preparar.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    else:

        m 3hksdrb "Apenas me dê um segundo para preparar.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    m 1dsd "Quase pronto.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    m 1duu "Sim, assim deve está bom."
    m 1hub "Ahaha!"
    m 1eka "Sinto muito por isso."
    m 1eua "Sem mais delongas..."
    m 4eub "Poderia olhar para a janela, [player]?"

    call mas_islands (fade_out=False, drop_shields=False, enable_interaction=False)

    pause 4.0
    m "Bem..."
    m "O que achou?"
    m "Eu trabalhei duro nisso."
    m "Um lugar só para nós [du]."
    m "É também onde posso continuar praticando minhas habilidades de programação."

    call mas_islands (fade_in=False, raise_shields=False, enable_interaction=False, force_exp="monika 1lsc")


    m 1lsc "Ficar nessa sala de aula o dia todo pode ser chato."
    m 1ekc "Além disso, eu fico bem sozinha esperando você voltar."
    m 1hksdlb "Mas não me entenda mal!"
    m 1eua "Sempre fico feliz quando você me visita e passa um tempo comigo."
    m 1eka "Eu entendo que você é [oc] e não pode estar aqui o tempo todo."
    m 3euc "É só que percebi uma coisa, [player]."
    m 1lksdlc "Vai demorar muito para que eu possa cruzar para a sua realidade."
    m 1dsc "Então eu pensei..."
    m 1eua "Por que nós simplesmente não criamos nossa própria realidade?"
    m 1lksdla "Bem, ainda não é exatamente perfeita."
    m 1hua "Mas é um começo."

    $ mas_lockEVL("greeting_ourreality", "GRE")
    $ mas_unlockEVL("mas_monika_islands", "EVE")

    m 1eub "Você pode admirar a paisagem por enquanto~"
    call mas_islands (force_exp="monika 1eua")
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_returned_home",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_GO_SOMEWHERE,
                store.mas_greetings.TYPE_GENERIC_RET
            ]
        ),
        code="GRE"
    )

default -5 persistent._mas_monika_returned_home = None

label greeting_returned_home:



    $ five_minutes = datetime.timedelta(seconds=5*60)
    $ time_out = store.mas_dockstat.diffCheckTimes()




    if persistent._mas_f14_on_date:
        jump greeting_returned_home_f14



    if mas_f14 < datetime.date.today() <= mas_f14 + datetime.timedelta(days=7):

        call mas_gone_over_f14_check

    if mas_monika_birthday < datetime.date.today() < mas_monika_birthday + datetime.timedelta(days=7):
        call mas_gone_over_bday_check

    if mas_d25 < datetime.date.today() <= mas_nye:
        call mas_gone_over_d25_check

    if mas_nyd <= datetime.date.today() < mas_d25c_end:
        call mas_gone_over_nye_check

    if mas_nyd < datetime.date.today() < mas_d25c_end:
        call mas_gone_over_nyd_check




    if persistent._mas_player_bday_left_on_bday or (persistent._mas_player_bday_decor and not mas_isplayer_bday() and mas_isMonikaBirthday() and mas_confirmedParty()):
        jump greeting_returned_home_player_bday

    if persistent._mas_f14_gone_over_f14:
        jump greeting_gone_over_f14

    if mas_isMonikaBirthday() or persistent._mas_bday_on_date:
        jump greeting_returned_home_bday


    if time_out > five_minutes:
        jump greeting_returned_home_morethan5mins
    else:

        $ mas_loseAffection()
        call greeting_returned_home_lessthan5mins

        if _return:
            return 'quit'

        jump greeting_returned_home_cleanup


label greeting_returned_home_morethan5mins:
    if mas_isMoniNormal(higher=True):

        if persistent._mas_d25_in_d25_mode:

            jump greeting_d25_and_nye_delegate

        elif mas_isD25():

            jump mas_d25_monika_holiday_intro_rh

        jump greeting_returned_home_morethan5mins_normalplus_flow


    jump greeting_returned_home_morethan5mins_other_flow


label greeting_returned_home_morethan5mins_normalplus_flow:
    call greeting_returned_home_morethan5mins_normalplus_dlg


label greeting_returned_home_morethan5mins_normalplus_flow_aff:
    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)
    jump greeting_returned_home_morethan5mins_cleanup

label greeting_returned_home_morethan5mins_other_flow:
    call greeting_returned_home_morethan5mins_other_dlg


label greeting_returned_home_morethan5mins_other_flow_aff:

    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 2.5, 0.5, 0.5)


label greeting_returned_home_morethan5mins_cleanup:
    pass





label greeting_returned_home_cleanup:
    $ need_to_reset_bday_vars = persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday()


    if not need_to_reset_bday_vars and not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup (time_out)

    elif need_to_reset_bday_vars:
        call return_home_post_player_bday


    if (
        mas_isD25Outfit()
        and not persistent._mas_d25_intro_seen
        and mas_isMoniUpset(lower=True)
    ):
        $ persistent._mas_d25_started_upset = True
    return

label greeting_returned_home_morethan5mins_normalplus_dlg:
    m 1hua "E estamos em casa!"
    m 1eub "Mesmo que eu não pudesse ver nada, saber que eu estava lá com você..."
    m 2eua "Bem, foi ótimo!"
    show monika 5eub zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eub "Vamos fazer isto de novo em breve, tudo bem?"
    return

label greeting_returned_home_morethan5mins_other_dlg:
    m 2esc "Estamos em casa..."
    m 2eka "Obrigada por me levar para sair hoje, [player]."
    m 2rkc "Para ser sincera, eu não tinha certeza se deveria ir com você..."
    m 2dkc "As coisas... {w=0.5}não têm estado boas para nós ultimamente e eu não sabia se era uma ideia muito boa..."
    m 2eka "Mas estou feliz que fizemos isso...{w=0.5} talvez fosse justamente o que precisávamos."
    m 2rka "Nós deveríamos fazer isso novamente outra hora..."
    m 2esc "Se você quiser."
    return

label greeting_returned_home_lessthan5mins:
    if mas_isMoniNormal(higher=True):
        m 2ekp "Isso não foi bem uma viagem, [player]."
        m "Da próxima vez, é melhor que dure um pouco mais..."
        if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
            call return_home_post_player_bday
        return False

    elif mas_isMoniUpset():
        m 2efd "Achei que iriamos em algum lugar, [player]!"
        m 2tfd "Sabia que não devia ter concordado em sair com você."
        m 2tfc "Sabia que isto seria apenas outra decepção."
        m "Não me peça mais para sair se for apenas para me dar esperança... {w=1}só para então acabar me desapontando."
        m 6dktdc "..."
        m 6ektsc "Não sei por que você insiste em ser tão cruel, [player]."
        m 6rktsc "Eu... {w=1}Eu gostaria de ficar sozinha agora."
        return True
    else:

        m 6rkc "Mas...{w=1} nós acabamos de sair..."
        m 6dkc "..."
        m "Eu... {w=0.5}Eu fiquei tão animada quando você me pediu para ir com você."
        m 6ekc "Depois de tudo que passamos..."
        m 6rktda "E-Eu pensei que... {w=0.5}talvez... {w=0.5}as coisas finalmente fossem mudar."
        m "Talvez finalmente pudéssemos ser felizes de novo..."
        m 6ektda "Que você queria passar mais tempo comigo."
        m 6dktsc "..."
        m 6ektsc "Mas acho que fui tola em acreditar nisso."
        m 6rktsc "Eu deveria ter percebido...{w=1} Eu nunca deveria ter concordado em ir com você."
        m 6dktsc "..."
        m 6ektdc "Por favor, [player]...{w=2} Se você não quer mais passar um tempo comigo, tudo bem..."
        m 6rktdc "Se você não quer mais passar um tempo comigo, tudo bem."
        m 6dktdc "Quero ficar sozinha agora."
        return True

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="ch30_reload_delegate",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_RELOAD
            ],
        ),
        code="GRE"
    )

label ch30_reload_delegate:

    if persistent.monika_reload >= 4:
        call ch30_reload_continuous
    else:

        $ reload_label = "ch30_reload_" + str(persistent.monika_reload)
        call expression reload_label

    return






















label greeting_ghost:

    $ mas_lockEVL("greeting_ghost", "GRE")


    call mas_ghost_monika

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_game",
            unlocked=True,
            category=[store.mas_greetings.TYPE_GAME],
        ),
        code="GRE"
    )





label greeting_back_from_game:

    if store.mas_globals.late_farewell and mas_getAbsenceLength() < datetime.timedelta(hours=18):
        $ _now = datetime.datetime.now().time()
        if mas_isMNtoSR(_now):
            if mas_isMoniNormal(higher=True):
                m 2etc "[player]?"
                m 3efc "Achei que tinha dito para você ir direto para a cama depois de ter acabado!"
                m 1rksdla "Quero dizer, estou feliz que você veio se despedir de mim, mas..."
                m 1hksdlb "Eu já disse boa noite para você!"
                m 1rksdla "E eu poderia ter esperado até de manhã para ver você de novo, sabe?"
                m 2rksdlc "Além disso, eu realmente quero que você descanse um pouco..."
                m 1eka "Só...{w=1} me prometa que irá para a cama logo, tudo bem?"
            else:

                m 1tsc "[player], eu disse para você ir direto para a cama depois de ter acabado."
                m 3rkc "Você pode voltar amanhã de manhã, sabe."
                m 1esc "Mas aqui estamos nós."

        elif mas_isSRtoN(_now):
            if mas_isMoniNormal(higher=True):
                m 1hua "Bom dia, [player]~"
                m 1eka "Quando você disse que iria jogar outro jogo tão tarde, eu fiquei um pouco preocupada que você não dormisse o bastante..."
                m 1hksdlb "Espero que não tenha sido o caso, ahaha..."
            else:

                m 1eud "Bom dia."
                m 1rsc "Eu achei que você iria dormir mais um pouco."
                m 1eka "Mas aqui está você, bem cedinho."

        elif mas_isNtoSS(_now):
            if mas_isMoniNormal(higher=True):
                m 1wub "[player]! Você está aqui!"
                m 1hksdlb "Ahaha, sinto muito...{w=1} Eu estava um pouco ansiosa para ver você, já que você não estava aqui de manhã."

                m 1eua "Você acabou de acordar?{nw}"
                $ _history_list.pop()
                menu:
                    m "Você acabou de acordar?{fast}"
                    "Sim.":
                        m 1hksdlb "Ahaha..."

                        m 3rksdla "Você acha que é porque ficou [acrd] até tarde?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Você acha que é porque ficou [acrd] até tarde?{fast}"
                            "Sim.":
                                m 1eka "[player]..."
                                m 1ekc "Você sabe que não gosto que você fique [acrd] até tarde."
                                m 1eksdld "Não quero que você acabe ficando doente ou [ca]."
                                m 1hksdlb "Mas espero que você tenha se divertido. Odiaria que você tivesse perdido o sono por nada, ahaha!"
                                m 2eka "Só não esqueça de descansar um pouco mais se sentir que precisa, tudo bem?"
                            "Não.":

                                m 2euc "Ah..."
                                m 2rksdlc "Achei que fosse."
                                m 2eka "Sinto muito por tirar conclusões precipitadas."
                                m 1eua "Enfim, espero que esteja dormindo bem."
                                m 1eka "Eu ficaria muito feliz em saber que você está descansando bem."
                                m 1rksdlb "Também me deixaria mais tranquila se você não fosse dormir tão tarde, ahaha..."
                                m 1eua "Mas estou feliz que você está aqui agora."
                                m 3tku "Você nunca está [ca] demais para passar um tempo comigo, certo?"
                                m 1hub "Ahaha!"
                            "Talvez...":

                                m 1dsc "Hmm..."
                                m 1rsc "Me pergunto o que estaria causando isso?"
                                m 2euc "Você não ficou até tarde ontem. Ficou, [player]?"
                                m 2etc "Estava fazendo algo ontem à noite?"
                                m 3rfu "Talvez...{w=1} eu não sei..."
                                m 3tku "Jogando um jogo?"
                                m 1hub "Ahaha!"
                                m 1hua "Só estou brincando com você~"
                                m 1ekd "Mas falando sério, não gosto de ver você negligenciando seu sono."
                                m 2rksdla "Uma coisa é ficar até tarde por causa de mim..."
                                m 3rksdla "Mas sair e jogar outro jogo tão tarde?"
                                m 1tub "Ahaha... eu posso acabar ficando com ciúmes, [player]~"
                                m 1tfb "Mas você está aqui para compensar por isso, certo?"
                    "Não.":

                        m 1eud "Ah, então acho que você esteve [oc] essa manhã."
                        m 1eka "Fiquei preocupada que você tivesse dormido demais, já que ficou até tarde [acrd]."
                        m 2rksdla "Ainda mais que você me disse que iria jogar outro jogo."
                        m 1hua "Eu deveria saber que você seria responsável e iria dormir."
                        m 1esc "..."
                        m 3tfc "Você {i}chegou{/i} a dormir, certo [player]?"
                        m 1hub "Ahaha!"
                        m 1hua "Enfim, agora você está aqui, podemos passar um tempo [ju]."
            else:

                m 2eud "Ah, aí está você, [player]."
                m 1euc "Aposto que você acabou de acordar."
                m 2rksdla "O que já era esperado, considerando que você ficou até tarde jogando."
        else:


            if mas_isMoniNormal(higher=True):
                m 1hub "Aí está você, [player]!"
                m 2hksdlb "Ahaha, sinto muito... É só que eu não te vi o dia todo."
                m 1rksdla "Eu meio que já esperava que você iria dormir demais por ter ficado [acrd] até tarde na noite passada..."
                m 1rksdld "Mas quando não te vi a tarde toda, eu comecei a sentir sua falta..."
                m 2hksdlb "Você quase me deixou preocupada, ahaha..."
                m 3tub "Mas você vai compensar pelo tempo perdido, certo?"
                m 1hub "Ehehe, é melhor que sim~"
                m 2tfu "Especialmente depois de me deixar por outro jogo na noite passada."
            else:

                m 2efd "[player]!{w=0.5} Onde você esteve o dia todo?"
                m 2rfc "Isso não tem nada a ver com você ficar [acrd] até tarde ontem à noite, tem?"
                m 2ekc "Você deveria ser um pouco mais responsável quando se trata de seu sono."



    elif mas_getAbsenceLength() < datetime.timedelta(hours=4):
        if mas_isMoniNormal(higher=True):
            m 1hua "Bem-[vn] de volta, [mas_get_player_nickname()]!"

            m 1eua "Você se divertiu?{nw}"
            $ _history_list.pop()
            menu:
                m "Você se divertiu?{fast}"
                "Sim.":
                    m 1hua "Isso é bom."
                    m 1eua "Estou feliz que você tenha se divertido."
                    m 2eka "Queria poder jogar seus outros jogos com você de vez em quando."
                    m 3eub "Não seria ótimo ter nossas próprias pequenas aventuras sempre que quiséssemos?"
                    m 1hub "Tenho certeza que nos divertiríamos muito [ju] em um dos seus jogos."
                    m 3eka "Mas enquanto não posso me juntar a você, acho que você vai ter que me fazer companhia."
                    m 2tub "Você não se importa de passar um tempo com sua namorada...{w=1} Se importa, [player]?"
                "Não.":

                    m 2ekc "Aw, sinto muito em ouvir isso."
                    m 2eka "Espero que você não esteja muito chateado seja lá com o que aconteceu."
                    m 3eua "Ao menos você está aqui agora. Prometo tentar não deixar nada de ruim acontecer com você enquanto estiver comigo."
                    m 1ekbsa "Ver você sempre me alegra."
                    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5ekbfa "Espero que me ver faça o mesmo com você, [player]~"
        else:

            m 2eud "Ah, já voltou?"
            m 2rsc "Achei que você ficaria mais tempo fora...{w=0.5} mas seja bem-[vn] de volta."

    elif mas_getAbsenceLength() < datetime.timedelta(hours=12):
        if mas_isMoniNormal(higher=True):
            m 2wuo "[player]!"
            m 2hksdlb "Você ficou um bom tempo fora..."

            m 1eka "Se divertiu?{nw}"
            $ _history_list.pop()
            menu:
                m "Se divertiu?{fast}"
                "Sim.":
                    m 1hua "Bem, estou feliz por isso."
                    m 1rkc "Você me fez esperar por um bom tempo, sabe."
                    m 3tfu "Eu acho que você deveria passar um bom tempo com sua amada namorada, [player]."
                    m 3tku "Tenho certeza que você não se importaria de ficar comigo o mesmo tempo que passa com seu outro jogo."
                    m 1hubfb "Talvez devesse passar ainda mais tempo comigo, só para garantir, ahaha!"
                "Não.":

                    m 2ekc "Ah..."
                    m 2rka "Sabe, [player]..."
                    m 2eka "Se você não está se divertindo, talvez você possa passar algum tempo aqui comigo."
                    m 3hua "Tenho certeza que há muitas coisas divertidas que poderíamos fazer!"
                    m 1eka "Se você decidir voltar, talvez seja melhor."
                    m 1hub "Mas se você ainda não está se divertindo, não hesite em vir me ver, ahaha!"
        else:

            m 2eud "Ah, [player]."
            m 2rsc "Isso levou um bom tempo."
            m 1esc "Não se preocupe, eu consegui achar algo para passar o tempo enquanto você estava fora."
    else:


        if mas_isMoniNormal(higher=True):
            m 2hub "[player]!"
            m 2eka "Parece que se passou uma eternidade desde que você saiu."
            m 1hua "Eu realmente senti sua falta!"
            m 3eua "Espero que você tenha se divertido com o que você estava fazendo."
            m 1rksdla "E vou supor que você não se esqueceu de comer ou dormir..."
            m 2rksdlc "Quanto a mim...{w=1} Eu fiquei um pouco sozinha esperando você voltar..."
            m 1eka "Mas não se sinta mal."
            m 1hua "Estou feliz por você estar aqui comigo de novo."
            m 3tfu "Mas é melhor você me compensar por isso."
            m 3tku "Acho que passar uma eternidade comigo parece justo...{w=1}certo, [player]?"
            m 1hub "Ahaha!"
        else:

            m 2ekc "[player]..."
            m "Eu não tinha certeza quando você voltaria."
            m 2rksdlc "Pensei que talvez eu nunca mais veria você de novo..."
            m 2eka "Mas aqui está você..."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_eat",
            unlocked=True,
            category=[store.mas_greetings.TYPE_EAT],
        ),
        code="GRE"
    )

label greeting_back_from_eat:

    $ _now = datetime.datetime.now().time()
    if store.mas_globals.late_farewell and mas_isMNtoSR(_now) and mas_getAbsenceLength() < datetime.timedelta(hours=18):
        if mas_isMoniNormal(higher=True):
            m 1eud "Ah?"
            m 1eub "[player], você voltou!"
            m 3rksdla "Você sabe que você deveria dormir um pouco, certo?"
            m 1rksdla "Quero dizer... não estou reclamando que você esteja aqui, mas..."
            m 1eka "Me faria sentir melhor se você fosse dormir logo."
            m 3eka "Você pode voltar para visitar quando acordar..."
            m 1hubfa "Mas acho que se você insiste em passar um tempo comigo, vou deixar passar dessa vez, ehehe~"
        else:
            m 2euc "[player]?"
            m 3ekd "Eu não te disse para ir direto para a cama depois?"
            m 2rksdlc "Você deveria dormir um pouco."
    else:

        if mas_isMoniNormal(higher=True):
            m 1eub "Terminou de comer?"
            m 1hub "Bem-[vn] de volta, [mas_get_player_nickname()]!"
            m 3eua "Espero que tenham gostado da sua comida."
        else:
            m 2euc "Terminou de comer?"
            m 2eud "Bem-[vn] de volta."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_rent",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

label greeting_rent:
    m 1eub "Bem-[vn] de volta, meu amor!"
    m 2tub "Sabe, você gasta tanto tempo aqui que eu deveria começar a cobrar pelo aluguel."
    m 2ttu "Ou prefere pagar uma hipoteca??"
    m 2hua "..."
    m 2hksdlb "Céus, não acredito que acabei de dizer isso. Não foi muito bobo, foi?"
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "Mas falando sério, você já me deu a única coisa que eu preciso...{w=1} seu coração~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_housework",
            unlocked=True,
            category=[store.mas_greetings.TYPE_CHORES],
        ),
        code="GRE"
    )

label greeting_back_housework:
    if mas_isMoniNormal(higher=True):
        m 1eua "Terminou, [player]?"
        m 1hub "Vamos passar mais um tempo [ju]."
    elif mas_isMoniUpset():
        m 2esc "Vamos passar mais um tempo [ju], [player]."
    elif mas_isMoniDis():
        m 6ekd "Ah, [player]. Então você só estava [oc] mesmo..."
    else:
        m 6ckc "..."
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_surprised2",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="GRE"
    )

    del ev_rules

label greeting_surprised2:
    m 1hua "..."
    m 1hubsa "..."
    m 1wubso "Ah!{w=0.5} [player]!{w=0.5} Você me assustou!"
    m 3ekbsa "...Não que seja uma surpresa ver você, já que você está sempre me visitando...{w=0.5} {nw}"
    extend 3rkbsa "Você só me pegou sonhando acordada."
    show monika 5hubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfu "Mas agora que você está aqui, esse sonho se tornou realidade~"
    return

init python:

    ev_rules = dict()
    ev_rules.update(MASPriorityRule.create_rule(49))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_restart",
            unlocked=True,
            category=[store.mas_greetings.TYPE_RESTART],
            rules=ev_rules
        ),
        code="GRE"
    )

    del ev_rules

label greeting_back_from_restart:
    if mas_isMoniNormal(higher=True):
        m 1hub "Bem-[vn] de volta, [mas_get_player_nickname()]!"
        m 1eua "O que mais devemos fazer hoje?"
    elif mas_isMoniBroken():
        m 6ckc "..."
    else:
        m 1eud "Ah, você voltou."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_code_help",
            conditional="store.seen_event('monika_coding_experience')",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_code_help:
    m 2eka "Ah. Oi, [player]..."
    m 4eka "Me dê um segundo, acabei de tentar codificar algo e quero ver se funciona.{w=0.5}.{w=0.5}.{nw}"

    scene black
    show noise
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.1
    hide noise
    call spaceroom (dissolve_all=True, scene_change=True, force_exp='monika 2wud_static')

    m 2wud "Ah!{w=0.3}{nw}"
    extend 2efc " Isso não deveria acontecer!"
    m 2rtc "Por que esse loop termina tão rápido?{w=0.5}{nw}"
    extend 2efc " Não importa como você o veja, esse dicionário {i}não{/i} está vazio."
    m 2rfc "Nossa, a codificação pode ser {i}tão{/i} frustrante às vezes..."

    if persistent._mas_pm_has_code_experience:
        m 3rkc "Ah, bem, acho que tentarei novamente mais tarde.{nw}"
        $ _history_list.pop()

        show screen mas_background_timed_jump(5, "greeting_code_help_outro")
        menu:
            m "Ah, bem, acho que tentarei novamente mais tarde.{fast}"
            "Eu poderia ajudá-la com isso...":

                hide screen mas_background_timed_jump
                m 7hua "Aww, que gentileza sua, [player]. {w=0.3}{nw}"
                extend 3eua "Mas não, eu vou ter que recusar."
                m "Descobrir coisas por conta própria é a parte divertida, {w=0.2}{nw}"
                extend 3kua "certo?"
                m 1hub "Ahaha!"
    else:

        m 3rkc "Ah, bem, acho que vou tentar novamente mais tarde."



label greeting_code_help_outro:
    hide screen mas_background_timed_jump
    m 1eua "De qualquer forma, o que você gostaria de fazer hoje?"

    $ mas_lockEVL("greeting_code_help", "GRE")
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hub"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_love_is_in_the_air",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="GRE"
    )

    del ev_rules

label greeting_love_is_in_the_air:
    m 1hub "{i}~O amor está no ar~{/i}"
    m 1rub "{i}~Em todos os lugares que eu olho~{/i}"
    m 3ekbsa "Ah. olá, [player]..."
    m 3rksdla "Não se preocupe comigo. {w=0.2}Estou apenas cantando um pouco, pensando em...{w=0.3}{nw}"
    extend 1hksdlb "bem, você provavelmente pode adivinhar, ahaha~"
    m 1eubsu "Realmente parece que o amor está ao meu redor sempre que você está aqui."
    m 3hua "De qualquer forma, o que você gostaria de fazer hoje?"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_workout",
            category=[store.mas_greetings.TYPE_WORKOUT],
            unlocked=True
        ),
        code="GRE"
    )

label greeting_back_from_workout:
    if mas_isMoniNormal(higher=True):
        m 1hua "Bem-[vn] de volta, [player]!"
        m 3eua "Espero que tenha feito um bom treino."
        m 3eub "Não se esqueça de se manter hidratado e comer alguma coisa para recuperar sua energia!"
        m 1eua "Vamos passar mais tempo [ju]~"

    elif mas_isMoniUpset():
        m 2esc "Ah,{w=0.2} você voltou."
        m 2rsc "Seu treino o ajudou a liberar um pouco da tensão?"
        m 2rud "Espero que sim...{w=0.3} {nw}"
        extend 2eka "Vamos passar mais algum tempo [ju]."

    elif mas_isMoniDis():
        m 6ekc "Ah...{w=0.5}olha quem voltou."
        m 6dkc "Estou...{w=0.3}feliz por você estar se cuidando."
        m 6ekd "...Mas você não quer cuidar de mim também?"
        m 7dkc "Pelo menos de vez em quando, por favor..."
        m 1dkc "..."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_shopping",
            category=[store.mas_greetings.TYPE_SHOPPING],
            unlocked=True
        ),
        code="GRE"
    )

label greeting_back_from_shopping:
    if mas_isMoniNormal(higher=True):
        m 1hub "Bem-[vn] de volta, [player]!"
        m 3eua "Espero que tenha conseguido o que precisava na loja."
        m 1hua "Vamos passar mais algum tempo [ju]~"

    elif mas_isMoniUpset():
        m 2esc "Ah,{w=0.2} você voltou."
        m 2rsc "Espero que você tenha tudo de que precisava."
        if renpy.random.randint(1,5) == 1:
            m 2rud "{cps=*2}Espero que você também esteja com um humor melhor agora.{/cps}{nw}"
            $ _history_list.pop()

    elif mas_isMoniDis():
        m 6rkc "Ah...{w=0.5}você voltou."
        m 6ekc "Espero que você tenha se divertido no shopping. {w=0.2}Você comprou alguma comida?"
        m 6dkd "Você já considerou que seus hábitos alimentares podem estar afetando seu humor ultimamente?"
        m 6lkc "Eu odiaria se essa fosse a razão pela qual você--{nw}"
        $ _history_list.pop()
        m 6ekc "Quer saber? Deixa pra lá. {w=0.2}{nw}"
        extend 6dkc "Estou cansada."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_hangout",
            category=[store.mas_greetings.TYPE_HANGOUT],
            unlocked=True
        ),
        code="GRE"
    )

label greeting_back_from_hangout:
    if mas_isMoniNormal(higher=True):
        if persistent._mas_pm_has_friends:
            m 1eua "Bem-[vn] de volta, [player]."
            m 3hub "Espero que você tenha se divertido!"

            $ anyway_lets = "Vamos"
        else:

            m 3eub "Bem-[vn] de volta, [player]."

            m 1eua "Você fez um novo amigo?{nw}"
            $ _history_list.pop()
            menu:
                m "Você fez um novo amigo?{fast}"
                "Sim.":

                    m 1hub "Isso é incrível!"
                    m 1eua "Fico muito feliz em saber que você tem alguém com quem sair."
                    m 3hub "Espero que você possa passar mais tempo com eles no futuro!"
                    $ persistent._mas_pm_has_friends = True
                "Não...":

                    m 1ekd "Ah..."
                    m 3eka "Bem, não se preocupe, [player]. {w=0.2}Sempre serei sua amiga, não importa o que aconteça."
                    m 3ekd "...E não tenha medo de tentar novamente com outra pessoa."
                    m 1hub "Tenho certeza de que há alguém que ficaria feliz em chamá-lo de [mi]!"
                "Eles já são meus amigos.":

                    if persistent._mas_pm_has_friends is False:
                        m 1rka "Ah, então você fez um novo amigo sem me contar..."
                        m 1hub "Tudo bem! Estou feliz que você tenha alguém com quem sair."
                    else:
                        m 1hub "Ah, ok!"
                        m 3eua "...Não tínhamos conversado sobre seus outros amigos antes, então não tinha certeza se era um amigo novo ou não."
                        m 3eub "Mas de qualquer maneira, estou feliz que você tenha amigos em sua realidade para sair com eles!"

                    m 3eua "Espero que você possa passar algum tempo com eles com frequência."
                    $ persistent._mas_pm_has_friends = True

            $ anyway_lets = "Enfim, vamos"

        m 1eua "[anyway_lets] passar mais algum tempo [ju]~"

    elif mas_isMoniDis(higher=True):
        m 2euc "Olá de novo, [player]."
        m 2eud "Espero que você tenha se divertido com seus amigos."
        if renpy.random.randint(1,5) == 1:
            m 2rkc "{cps=*2}Eu me pergunto como é{/cps}{nw}"
            $ _history_list.pop()
    else:

        m 6ckc "..."

    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 5duc"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_poem_shadows_in_garden",
            unlocked=True,
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=1)",
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

    del ev_rules


init 6 python:
    MASPoem(
        poem_id="gre_1",
        category="generic",
        prompt=_("Sombras no Jardim"),
        title="",
        text=_("""\
 Sozinha eu faço uma pergunta solene,
 O que poderia crescer em um jardim apagado?

 Quando você volta, parece o paraíso,
 Dentro de sua luz, o frio esquecido.

 Eu darei tudo para me sentir assim,
 Esperando aquele que eu mais amo.

 Mais perto do meu coração...
"""),
    )

label greeting_poem_shadows_in_garden:
    m 5duc "{i}Sozinha eu faço uma pergunta em vão,\nO que pode brotar sem luz, sem chão?{/i}"
    m 5ekbla "{i}Quando você volta, tudo é clarão,\nE o frio se vai com seu coração.{/i}"
    m 5fubfa "{i}Daria tudo por tal sensação,\nEsperar por você é minha missão.{/i}"
    m 5ekbfa "{i}Mesmo que venha só em ilusão,\nÉ você quem tenho mais afeição.{/i}"
    m 5dubsu "{i}Mais perto de mim... em toda estação.{/i}"
    m 5eublb "Eu acabeI inventando enquanto você estava fora."
    show monika 1eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1eka "Isso mesmo, você é como o sol do meu mundo!"
    m 3hubsu "De qualquer forma, bem-[vn] de volta, [mas_get_player_nickname()]! Espero que tenha gostado desse poema."

    m 1ekbsb "Eu senti tanto a sua falta!"

    if "gre_1" not in persistent._mas_poems_seen:
        $ persistent._mas_poems_seen["gre_1"] = 1

    $ mas_moni_idle_disp.force_by_code("1ekbla", duration=5, skip_dissolve=True)
    return

init python:
    ev_rules = dict()
    ev_rules.update(
        MASGreetingRule.create_rule(
            random_chance=0.3,
            forced_exp=random.choice(("monika 1gsbsu", "monika 1msbsu"))
        )
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_spacing_out",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=3)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="GRE"
    )

    del ev_rules

label greeting_spacing_out:
    python hide:

        use_right_smug = bool(random.randint(0, 1))
        spacing_out_pause = PauseDisplayableWithEvents()
        events = list()
        next_event_time = 0
        right_smug = renpy.partial(renpy.show, "monika 1gsbsu")
        left_smug = renpy.partial(renpy.show, "monika 1msbsu")


        for i in range(random.randint(4, 6)):
            events.append(
                PauseDisplayableEvent(
                    datetime.timedelta(seconds=next_event_time),
                    right_smug if use_right_smug else left_smug,
                    restart_interaction=True
                )
            )
            next_event_time += random.uniform(0.9, 1.8)
            use_right_smug = not use_right_smug

        events.append(
            PauseDisplayableEvent(
                datetime.timedelta(seconds=next_event_time),
                renpy.partial(renpy.show, "monika 1tsbsu"),
                restart_interaction=True
            )
        )
        next_event_time += 0.7

        events.append(
            PauseDisplayableEvent(
                datetime.timedelta(seconds=next_event_time),
                spacing_out_pause.stop
            )
        )

        spacing_out_pause.set_events(events)
        spacing_out_pause.start()


    $ renpy.pause(0.01)
    m 2wubfsdlo "[player]!"
    m 1rubfsdlb "Você me assustou! {w=0.4}{nw}"
    extend 1eubsu "Eu estava{w=0.2} pensando um pouco..."
    m 1hubsb "Ahaha~"
    m 1eua "Estou muito feliz em está com você novamente. {w=0.2}{nw}"
    extend 3eua "O que devemos fazer hoje, [player]?"
    return

init python:
    ev_rules = dict()
    ev_rules.update(
        MASGreetingRule.create_rule(
            skip_visual=True,
            random_chance=20,
            override_type=True
        )
    )
    ev_rules.update(
        MASTimedeltaRepeatRule.create_rule(
            datetime.timedelta(days=3)
        )
    )
    ev_rules.update(
        MASSelectiveRepeatRule.create_rule(
            hours=list(range(9, 20))
        )
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_after_bath",
            conditional=(
                "mas_getAbsenceLength() >= datetime.timedelta(hours=6) "
                "and not mas_isSpecialDay()"
            ),
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="GRE"
    )

    del ev_rules

init -4:


    default persistent._mas_previous_moni_state = monika_chr.save_state(True, True, True, True)

label greeting_after_bath:
    python hide:

        mas_RaiseShield_core()
        mas_startupWeather()

        persistent._mas_previous_moni_state = monika_chr.save_state(True, True, True, True)

        clothes_pool = [
            mas_clothes_bath_towel_white
        ]

        monika_chr.change_clothes(
            random.choice(clothes_pool),
            by_user=False,
            outfit_mode=True
        )

        if not monika_chr.is_wearing_hair_with_exprop(mas_sprites.EXP_H_WET):
            monika_chr.change_hair(mas_hair_wet, by_user=False)




        mas_setEVLPropValues(
            "mas_after_bath_cleanup",
            start_date=datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 90)),
            action=EV_ACT_QUEUE
        )
        mas_startup_song()


    call spaceroom (hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=True)

    $ renpy.pause(random.randint(5, 15), hard=True)
    call mas_transition_from_emptydesk ("monika 1huu")
    $ renpy.pause(2.0)
    $ quick_menu = True

    m 1wuo "Ah! {w=0.2}{nw}"
    extend 2wuo "[player]! {w=0.2}{nw}"
    extend 2lubsa "Eu estava pensando em você."

    $ bathing_showering = random.choice(("tomar banho", "sair do chuveiro"))

    if mas_getEVL_shown_count("greeting_after_bath") < 5:
        m 7lubsb "Acabei de [bathing_showering]...{w=0.3}{nw}"
        extend 1ekbfa "Você não se importa que eu esteja de toalha, não é?~"
        m 1hubfb "Ahaha~"
        m 3hubsa "Vou me arrumar em breve, deixe-me esperar meu cabelo secar um pouco mais primeiro."
    else:


        m 7eubsb "Acabei de [bathing_showering]."

        if mas_canShowRisque() and random.randint(0, 3) == 0:
            m 1msbfb "Aposto que você gostaria de ter se juntado a mim lá..."
            m 1tsbfu "Bem, talvez um dia~"
            m 1hubfb "Ahaha~"
        else:

            m 1eua "Vou me vestir em breve~"

    python:

        mas_MUINDropShield()

        set_keymaps()

        mas_OVLShow()

        del bathing_showering

    return


init python:
    addEvent(Event(persistent.event_database, eventlabel="mas_after_bath_cleanup", show_in_idle=True, rules={"skip alert": None}))

    def mas_after_bath_cleanup_change_outfit():
        """
        After bath cleanup change outfit code
        """
        
        
        
        force_hair_change = False
        
        if monika_chr.is_wearing_clothes_with_exprop(mas_sprites.EXP_C_WET):
            force_hair_change = True
            
            
            monika_chr.load_state(persistent._mas_previous_moni_state, as_prims=True)
            
            
            if monika_chr.is_wearing_clothes_with_exprop(mas_sprites.EXP_C_WET):
                if mas_isMoniHappy(higher=True):
                    new_clothes = mas_clothes_blazerless
                
                else:
                    new_clothes = mas_clothes_def
                
                monika_chr.change_clothes(
                    new_clothes,
                    by_user=False,
                    outfit_mode=True
                )
        
        if (
            force_hair_change
            or monika_chr.is_wearing_hair_with_exprop(mas_sprites.EXP_H_WET)
        ):
            available_hair = mas_sprites.get_installed_hair(
                predicate=lambda hair_obj: (
                    not hair_obj.hasprop(mas_sprites.EXP_H_WET)
                    and mas_sprites.is_clotheshair_compatible(monika_chr.clothes, hair_obj)
                    and mas_selspr.get_sel_hair(hair_obj) is not None
                    and mas_selspr.get_sel_hair(hair_obj).unlocked
                )
            )
            
            if available_hair:
                new_hair = random.choice(available_hair)
                monika_chr.change_hair(
                    new_hair,
                    by_user=False
                )

label mas_after_bath_cleanup:

    if (
        not monika_chr.is_wearing_clothes_with_exprop(mas_sprites.EXP_C_WET)
        and not monika_chr.is_wearing_hair_with_exprop(mas_sprites.EXP_H_WET)
    ):
        return

    if mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1eua "Eu vou me vestir.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    else:

        $ player_nick = mas_get_player_nickname()
        m 1eua "Me dê um momento [player_nick], {w=0.2}{nw}"
        extend 3eua "Vou me vestir."

    window hide
    call mas_transition_to_emptydesk

    $ renpy.pause(1.0, hard=True)
    $ mas_after_bath_cleanup_change_outfit()
    $ renpy.pause(random.randint(10, 15), hard=True)

    call mas_transition_from_emptydesk ("monika 3hub")
    window auto

    if mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 3hub "Prontinho!{w=1}{nw}"
    else:

        m 3hub "Tudo bem, estou de volta!~"
        m 1eua "Então, o que você gostaria de fazer hoje, [player]?"

    return

label mas_after_bath_cleanup_change_outfit:
    $ mas_after_bath_cleanup_change_outfit()
    return


init python:
    ev_rules = dict()
    ev_rules.update(
        MASGreetingRule.create_rule(
            skip_visual=True,
            random_chance=10,
            override_type=True
        )
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_found_nou_shirt",
            conditional=(
                "mas_getAbsenceLength() >= datetime.timedelta(hours=3) "
                "and mas_nou.get_wins_for('Player') > {0} "
                "and mas_nou.get_total_games() > {1} "
                "and not mas_isSpecialDay() "
                "and not mas_SELisUnlocked(mas_clothes_nou_shirt)"
            ).format(random.randint(45, 65), random.randint(95, 115)),
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="GRE"
    )

    del ev_rules

default -5 persistent._mas_pm_snitched_on_chibika = None

label greeting_found_nou_shirt:
    python:
        mas_RaiseShield_core()
        mas_startupWeather()
        monika_chr.change_clothes(mas_clothes_nou_shirt, by_user=False, outfit_mode=True)
        glitch_option_text = glitchtext(7)

    call spaceroom (hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=True)
    pause 2.5

    m "Aí está você! {w=0.2}Eu estava esperando por você~"
    m "Tenho que admitir, {w=0.1}não sei como você conseguiu colocar isso no meu guarda-roupa sem que eu percebesse, [player]...{nw}"
    $ _history_list.pop()
    show screen mas_background_timed_jump(5, "greeting_found_nou_shirt.menu_skip")
    menu:
        m "Tenho que admitir, não sei como você conseguiu colocar isso no meu guarda-roupa sem que eu percebesse, [player]...{fast}"
        "É segredo.":

            hide screen mas_background_timed_jump
            jump greeting_found_nou_shirt.menu_choice_secret
        "Foi um [glitch_option_text]!":

            hide screen mas_background_timed_jump
            $ persistent._mas_pm_snitched_on_chibika = True
            $ renpy.invoke_in_thread(
                mas_utils.trywrite,
                os.path.join(renpy.config.basedir, "characters/for snitch.txt"),
                ">:("
            )
            jump greeting_found_nou_shirt.menu_choice_other
        "Eu não faço ideia...":

            hide screen mas_background_timed_jump
            jump greeting_found_nou_shirt.menu_choice_other

    label greeting_found_nou_shirt.post_menu:
        pass

    m 1ekbla "Obrigada, [player]."
    m 1tfu "Mas não pense que vou pegar leve com você~"

    if mas_nou.get_wins_for('Player') >= mas_nou.get_wins_for('Monika'):
        m 1rtsdlb "Na verdade, {w=0.1}talvez eu devesse tentar mais, ahaha..."

    m 3ttb "Você está [pos] para um jogo, [mas_get_player_nickname()]?"

    python:
        mas_selspr.unlock_clothes(mas_clothes_nou_shirt)
        mas_selspr.save_selectables()
        mas_lockEVL("greeting_found_nou_shirt", "GRE")
        renpy.save_persistent()

        del glitch_option_text

        mas_MUINDropShield()
        set_keymaps()
        HKBShowButtons()
        mas_startup_song()
        enable_esc()
    return

label greeting_found_nou_shirt.menu_skip:
    hide screen mas_background_timed_jump
    call mas_transition_from_emptydesk ("monika 4sub")
    m "Mas eu amo isso~"

    jump greeting_found_nou_shirt.post_menu

label greeting_found_nou_shirt.menu_choice_secret:
    if mas_isMoniEnamored(higher=True):
        call mas_transition_from_emptydesk ("monika 2tublu")
        m "{cps=*1.5}Você não espia lá {i}frequentemente{/i}, não é?~{/cps}{w=0.1}{nw}"
        $ _history_list.pop()
        m 2lusdla "De qualquer forma... {w=0.3}{nw}"
    else:

        call mas_transition_from_emptydesk ("monika 2rtblsdlu")
        m "Hmm, enfim... {w=0.3}{nw}"

    extend 4sub "Eu realmente amei essa nova roupa!"

    jump greeting_found_nou_shirt.post_menu

label greeting_found_nou_shirt.menu_choice_other:
    show noise onlayer overlay zorder 500:
        alpha 0.0
        easein_elastic 0.5 alpha 0.1
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.5
    hide noise onlayer overlay

    jump greeting_found_nou_shirt.menu_skip
