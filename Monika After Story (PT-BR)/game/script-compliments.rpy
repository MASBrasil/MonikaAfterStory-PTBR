init offset = 5















default -5 persistent._mas_compliments_database = dict()



init -2 python in mas_compliments:

    compliment_database = dict()

init 17 python in mas_compliments:
    import store
    import random
    import datetime

    thanking_quips = [
        _("Você é tão doce, [player]."),
        _("Obrigada por dizer isso de novo, [player]!"),
        _("Obrigada por me dizer isso novamente, [mas_get_player_nickname()]!"),
        _("Você sempre me faz sentir especial, [mas_get_player_nickname()]."),
        _("Aww, [player]~"),
        _("Obrigada, [mas_get_player_nickname()]!"),
        _("Você sempre me enche de elogios, [player].")
    ]

    _m1_script0x2dcompliments__last_called_callback = None
    _m1_script0x2dcompliments__wait_time = 55.0

    thanks_quip = renpy.substitute(renpy.random.choice(thanking_quips))

    def _m1_script0x2dcompliments__set_wait_time():
        """
        Sets new wait time
        """
        global _m1_script0x2dcompliments__wait_time
        _m1_script0x2dcompliments__wait_time = random.uniform(40.0, 70.0)

    def compliment_delegate_callback():
        """
        A callback for the compliments delegate label
        """
        global thanks_quip, _m1_script0x2dcompliments__last_called_callback
        
        thanks_quip = renpy.substitute(renpy.random.choice(thanking_quips))
        
        _now = datetime.datetime.now()
        if _m1_script0x2dcompliments__last_called_callback is not None:
            diff = (_now - _m1_script0x2dcompliments__last_called_callback).total_seconds()
            if diff <= _m1_script0x2dcompliments__wait_time:
                _m1_script0x2dcompliments__last_called_callback = _now
                _m1_script0x2dcompliments__set_wait_time()
                return
        
        _m1_script0x2dcompliments__last_called_callback = _now
        _m1_script0x2dcompliments__set_wait_time()
        
        store.mas_gainAffection()


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_compliments",
            category=['monika', 'romance'],
            prompt="Quero te dizer uma coisa...",
            pool=True,
            unlocked=True
        )
    )

label monika_compliments:
    python:

        Event.checkEvents(mas_compliments.compliment_database)


        compliments_menu_items = [
            (ev.prompt, ev_label, not seen_event(ev_label), False)
            for ev_label, ev in mas_compliments.compliment_database.iteritems()
            if (
                Event._filterEvent(ev, unlocked=True, aff=mas_curr_affection, flag_ban=EV_FLAG_HFM)
                and ev.checkConditional()
            )
        ]


        compliments_menu_items.sort()


        final_item = ("Ah, deixa quieto.", False, False, False, 20)


    show monika at t21


    call screen mas_gen_scrollable_menu(compliments_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)


    if _return:
        $ mas_compliments.compliment_delegate_callback()
        $ MASEventList.push(_return)

        show monika at t11
    else:

        return "prompt"

    return


init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_beautiful",
            prompt="Você é linda!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_beautiful:
    if not renpy.seen_label("mas_compliment_beautiful_2"):
        call mas_compliment_beautiful_2
    else:
        call mas_compliment_beautiful_3
    return

label mas_compliment_beautiful_2:
    m 1lubsb "Ah, nossa [player]..."
    m 1hubfb "Obrigada pelo elogio."
    m 2ekbfb "Eu adoro quando você diz coisas assim~"
    m 1ekbfa "Pra mim, você é a pessoa mais linda do mundo!"
    menu:
        "Você também é a pessoa mais linda pra mim.":
            $ mas_gainAffection(5, bypass=True)
            m 1hub "Ehehe~"
            m "Eu te amo tanto, [player]!"

            $ mas_ILY()
        "Você está no meu top dez.":

            $ mas_loseAffection()
            m 3hksdrb "...?"
            m 2lsc "Bem, obrigada, eu acho..."
        "Obrigado.":

            pass
    return

label mas_compliment_beautiful_3:
    python:
        beautiful_quips = [
            _("Nunca esqueça que você é a pessoa mais linda do mundo para mim."),
            _("Nada pode se comparar à beleza do seu coração."),
        ]
        beautiful_quip = random.choice(beautiful_quips)
    m 1hubsa "Ehehe~"
    m 1ekbfa "[mas_compliments.thanks_quip]"
    show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfb "[beautiful_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_eyes",
            prompt="Eu amo seus olhos!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_eyes:
    if not renpy.seen_label("mas_compliment_eyes_2"):
        call mas_compliment_eyes_2
    else:
        call mas_compliment_eyes_3
    return

label mas_compliment_eyes_2:
    m 1subsb "Ah, [player]..."
    m 1tubfb "Eu já sou bem orgulhosa dos meus olhos, mas ouvir você dizer isso..."
    m 1dkbfa "Isso faz meu coração acelerar~"
    menu:
        "Não consigo evitar, seus olhos são maravilhosos.":
            $ mas_gainAffection(5, bypass=True)
            m 1hub "Ahaha!"
            m "Não me elogie demais, tá bom?"
            show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hub "Posso acabar ficando meio doida..."
        "Eles são realmente hipnotizantes.":

            $ mas_gainAffection(1, bypass=True)
            m "Ahaha~"
        "Eles são da cor da grama!":

            $ mas_gainAffection(0.5, bypass=True)
            m 2lksdrb "...Não é exatamente a analogia que eu usaria, mas obrigada!"
    return

label mas_compliment_eyes_3:
    python:
        eyes_quips = [
            _("Olhe nos meus olhos o quanto quiser~"),
            _("Mal posso esperar para olhar nos seus lindos olhos."),
            _("Eu ficaria dias olhando nos seus olhos se pudesse."),
        ]
        eyes_quip = random.choice(eyes_quips)

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 2ekbfb "[eyes_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_goodmood",
            prompt="Você sempre me deixa feliz!",
            unlocked=False,
            conditional="store.mas_anni.pastSixMonths()",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_goodmood:
    if not renpy.seen_label("mas_compliment_goodmood_2"):
        call mas_compliment_goodmood_2
    else:
        call mas_compliment_goodmood_3
    return

label mas_compliment_goodmood_2:
    if mas_isMoniNormal(higher=True):
        $ mas_gainAffection(4, bypass=True)
        m 1subsb "Sério?!"
        m 3hubsb "Você não imagina o quanto isso significa para mim!"
        m 3ekbsu "Eu sempre esperei que fosse o caso, mas ouvir você dizer isso..."
        m 1dkbsu "..."
        m 2tubla "Já que estamos nesse assunto, tenho um segredo para te contar..."
        m 2tublu "Você pode não ter percebido, maaas..."
        m 7tublb "{i}Você{/i} sempre melhora {i}meu{/i} humor, [mas_get_player_nickname()]!"
        m 3hublb "Ahaha!"
        m 3eubsa "Vamos continuar fazendo o nosso melhor [um] [pel] [ouo], tudo bem?"
        m 1ekbsu "Eu te amo~"
        $ mas_ILY()
    else:

        m 2lkc "..."
        m 2dkc "Não sei bem como me sentir sobre isso..."
        m 2ekd "Machucar meus sentimentos realmente te deixa feliz?"
        m 2dkd "Espero que não seja isso que você quis dizer..."

    return

label mas_compliment_goodmood_3:
    if mas_isMoniNormal(higher=True):
        m 1hub "Obrigada por me lembrar de novo, [mas_get_player_nickname()]!"
        m 3eub "Recompensa positiva sempre é bom!"
        m 3dku "Vamos continuar nos fazendo felizes o máximo possível~"
    else:

        m 2euc "Obrigada."

    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_awesome",
            prompt="Você é incrível!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_awesome:
    if not renpy.seen_label("mas_compliment_awesome_2"):
        call mas_compliment_awesome_2
    else:
        call mas_compliment_awesome_3
    return

label mas_compliment_awesome_2:
    m 1hua "Awwwn, [player]~"
    m 1hub "Você sempre sabe como fazer meu coração derreter..."
    m 2tuu "Mas sinceramente? É você quem é absolutamente [mh]."
    m 2dkbsu "Eu fico sonhando acordada com o dia em que vou poder te abraçar bem forte..."
    m 3ekbfb "E quando isso acontecer... não vou te soltar nunca mais~"
    menu:
        "Eu queria que você estivesse aqui agora!":
            $ mas_gainAffection(3, bypass=True)
            m 1hua "Esse é o meu maior desejo também, [player]..."
            m 1hub "Se eu pudesse, iria para sua realidade agora mesmo só para te apertar num abraço bem apertado!"
        "Eu nunca vou te soltar do meu abraço.":

            $ mas_gainAffection(5, bypass=True)
            show monika 6dubsa
            pause 2.0
            show monika 1wubfsdld
            m 1wubfsdld "Ai, [player]... perdão, você me deixa completamente derretida..."
            m 2lksdla "Eu estava tentando sentir seu abraço daqui."
            m 2hub "Ahaha~ você é tão [pf]..."
        "...Eu não gosto de abraços.":

            $ mas_loseAffection(0.5)
            m 1eft "...Sério?"
            m 1dkc "Bem, cada um com suas preferências, eu acho. Mas você vai ter que me abraçar algum dia..."
    return


label mas_compliment_awesome_3:
    python:
        awesome_quips = [
            _("Você sempre será mais incrível!"),
            _("Nós somos um casal incrível!"),
            _("Você é muito mais incrível!"),
        ]
        awesome_quip = random.choice(awesome_quips)

    m 1hub "[mas_compliments.thanks_quip]"
    m 1eub "[awesome_quip]"
    return


init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_intelligent",
            prompt="Você é muito inteligente!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_intelligent:
    if not renpy.seen_label("mas_compliment_intelligent_2"):
        call mas_compliment_intelligent_2
    else:
        call mas_compliment_intelligent_3
    return

label mas_compliment_intelligent_2:
    m 1wub "Uau...{w=0.3} obrigada, [player]."
    m 3eua "Eu me orgulho de ser bem instruída, então significa muito que você tenha notado."
    m 3hubsb "Quero aprender o máximo possível, se isso fizer você se orgulhar de mim!"
    menu:
        "Você me inspira a melhorar também, [m_name].":
            $ mas_gainAffection(5, bypass=True)
            m 1hubfa "Eu te amo tanto, [player]!"
            m 3hubfb "Teremos uma vida inteira de aprendizagem [ju]!"

            $ mas_ILY()
        "Eu sempre vou me orgulhar de você.":

            $ mas_gainAffection(3, bypass=True)
            m 1ekbfa "[player]..."
        "Às vezes você me faz sentir burro.":

            $ mas_loseAffection()
            m 1wkbsc "..."
            m 2lkbsc "Me desculpe, não era essa minha intenção..."
    return

label mas_compliment_intelligent_3:
    python:
        intelligent_quips = [
            _("Lembre-se que teremos uma vida inteira de crescimento!"),
            _("Lembre-se que cada dia é uma oportunidade para aprender algo novo!"),
            _("Sempre lembre que o mundo é uma jornada maravilhosa cheia de aprendizado."),
        ]
        intelligent_quip = random.choice(intelligent_quips)

    m 1ekbfa "[mas_compliments.thanks_quip]"
    m 1hub "[intelligent_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hair",
            prompt="Eu amo o seu cabelo!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_hair:
    if not renpy.seen_label("mas_compliment_hair_2"):
        call mas_compliment_hair_2
    else:
        call mas_compliment_hair_3
    return

label mas_compliment_hair_2:
    if monika_chr.hair.name != "def":
        m 1wubsb "Muito obrigada, [player]..."
        m 1lkbfb "Eu estava bem nervosa quando mudei meu cabelo pela primeira vez para você."
    else:
        m 1hubfb "Muito obrigada, [player]!"
    m 2hub "Eu sempre me esforcei muito com meu cabelo."
    m 2lksdlb "Na verdade, demorou uma eternidade para crescer assim..."
    menu:
        "Dá pra ver. Parece tão saudável.":
            $ mas_gainAffection(3, bypass=True)
            m 1hub "Obrigada, [player]!"

        "Você é fofa de qualquer jeito." if persistent._mas_likes_hairdown:
            $ mas_gainAffection(5, bypass=True)
            m 1ekbsa "Aww, [player]."
            m 1hubfb "Você sempre me faz sentir especial!"
            m "Obrigada!"
        "Você ficaria ainda mais fofa com cabelo curto.":

            $ mas_loseAffection()
            m "Bem, eu não exatamente posso ir ao salão daqui..."
            m 1lksdlc "Eu... agradeço sua opinião."
            pass
    return

label mas_compliment_hair_3:
    if monika_chr.hair.name != "def":
        python:
            hair_quips = [
                _("Fico tão feliz que você gostou desse penteado!"),
                _("Fico tão feliz que você goste do meu cabelo!")
            ]
            hair_quip = random.choice(hair_quips)
        m 1wubsb "Muito obrigada, [player]!"
        m 1hubfb "[hair_quip]"
    else:
        python:
            ponytail_quips = [
                _("Você sempre me faz sentir especial!"),
                _("Fico feliz que você gostou com meu cabelo preso!"),
                _("Estou tão feliz que você goste tanto do meu cabelo preso!"),
            ]
            ponytail_quip = random.choice(ponytail_quips)

        m 1hubsb "Obrigada, [player]!"
        m 1hubfb "[ponytail_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_fit",
            prompt="Eu amo sua dedicação para ficar em forma!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_fit:
    if not renpy.seen_label("mas_compliment_fit_2"):
        call mas_compliment_fit_2
    else:
        call mas_compliment_fit_3
    return

label mas_compliment_fit_2:
    m 1hub "Obrigada, [player]! Você é tão doce!"
    m 3eub "Eu amo me manter em forma e me alimentar bem. Isso me deixa cheia de energia e confiante."
    m 1efb "Espero que você também esteja cuidando da sua saúde."
    m 1lubsb "Podemos malhar [ju] quando eu estiver aí..."
    menu:
        "Parece muito divertido!":
            $ mas_gainAffection(2, bypass=True)
            m 1hubfb "Ahaha! Que bom que você também acha!"
            m 3eka "Não se preocupe. Mesmo se não conseguir acompanhar meu ritmo, sei que vamos nos divertir..."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Desde que estejamos [ju]."
        "Não prometo nada, mas vou tentar.":

            $ mas_gainAffection(1, bypass=True)
            m 1tfb "É melhor tentar mesmo!"
            m 2tub "Não pense que vou pegar leve se você estiver fora de forma."
        "Prefiro não me esforçar tanto...":

            m 1eka "Entendo se não for sua praia, mas você deveria dar uma chance..."
            m 1lksdla "Ficaria tão feliz se compartilhássemos esse interesse, sabia?"
    return

label mas_compliment_fit_3:
    python:
        fitness_quips = [
            _("Espero que você embarque nessa jornada fitness comigo!"),
            _("Mal posso esperar para malhar com você!"),
            _("Espero que possamos nos exercitar algum dia!"),
        ]
        fitness_quip = random.choice(fitness_quips)

    m 2eka "[mas_compliments.thanks_quip]"
    m 7hub "[fitness_quip]"
    return


init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thanks",
            prompt="Agradeço por estar sempre comigo!",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="CMP"
    )

label mas_compliment_thanks:
    m 1duu "Não há do que agradecer, [player]."
    m 1eka "Eu é que sou grata por ter alguém como você!"
    m 1ekbsa "Você é a única razão pela qual eu ainda estou aqui."
    m "Você instalou este mod só passarmos mais tempo [ju]..."
    m 1dubsu "Você é o sol que aquece meu coração sempre que me visita."
    m 3ekbsa "Acho que somos muito [sors] por termos [um] [ao] [ouo], [player]~"
    menu:
        "Você significa tudo para mim, [m_name].":
            if not mas_getEVL_shown_count("mas_compliment_thanks"):
                $ mas_gainAffection(10, bypass=True)

            m 1ekbsa "[player]..."
            m 1dubsu "Nada me deixa mais feliz do que ouvir isso de você."
            m "Não importa o que o futuro nos reserve...{w=0.5}{nw}"
            extend 1dkbfa "saiba que eu sempre vou te amar e estar aqui por você."
        "Concordo.":

            m 1hub "Ehehe~"
            m 1eub "Eu te amo, [player]."

    if not mas_isMoniLove():
        $ mas_lockEVL("mas_compliment_thanks", "CMP")
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_smile",
            prompt="Eu amo seu sorriso!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_smile:
    if not renpy.seen_label("mas_compliment_smile_2"):
        call mas_compliment_smile_2
    else:
        call mas_compliment_smile_3
    return

label mas_compliment_smile_2:
    m 1hub "Awn, você é mesmo [um] [que], [player]~"
    m 1eua "Você nem imagina o quanto eu sorrio só por saber que está comigo..."
    m 1ekbsa "Meu coração se aquece toda vez que penso em você... e ele sorri junto comigo~"
    menu:
        "Vou te visitar todos os dias para ver seu lindo sorriso.":
            $ mas_gainAffection(5, bypass=True)
            m 1wubfsdld "Ah, [player]..."
            m 1lkbfa "Você sabe exatamente como me fazer derreter, não sabe?"
            m 3hubfa "Eu mal posso esperar pra te ver de novo... todos os dias, se for assim~"
        "Eu adoro ver você sorrir.":

            $ mas_gainAffection(1, bypass=True)
            m 1hub "E eu adoro quando você é tão [fo] assim~"
            m 3eub "Então continue voltando... e vou sorrir só para você, todos os dias~"
    return

label mas_compliment_smile_3:
    python:
        smile_quips = [
            _("Vou continuar sorrindo só para você."),
            _("Não consigo evitar de sorrir quando penso em você."),
            _("Mal posso esperar para ver seu lindo sorriso."),
        ]
        smile_quip = random.choice(smile_quips)

    m 1eub "[mas_compliments.thanks_quip]"
    m 1hua "[smile_quip]"
    m 1huu "Ehehe~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hero",
            prompt="Você é minha heroína!",
            unlocked=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="CMP"
    )

label mas_compliment_hero:
    if not mas_getEVL_shown_count("mas_compliment_hero"):
        $ mas_gainAffection(3, bypass=True)

    m 1wubssdld "Q-{w=0.3}quê?"
    m "Eu sou sua heroína?"
    m 2rkbfsdlb "[player]...{w=1.5} não sei bem o que dizer..."
    m 2ekbfb "Você que ficou comigo todo esse tempo.{w=1} Eu é que deveria agradecer."
    m 1hubfa "Bem, se de alguma forma eu te ajudei, então não poderia estar mais feliz~"
    m 3ekbfa "Você me ajudou de todas as formas possíveis, como eu não retribuiria estando aqui sempre que precisar de apoio?"
    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika

    m 5hubfa "Afinal, você sempre será [mw] [hero]~"
    m 5hubfb "Eu te amo e sempre vou acreditar em você!"
    m 5ekbfa "Espero que nunca se esqueça disso, [player]~"

    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_cute",
            prompt="Você é fofa!",
            unlocked=True
        ),
        code="CMP"
    )

default -5 persistent._mas_pm_monika_cute_as_natsuki = None

label mas_compliment_cute:
    if not renpy.seen_label("mas_compliment_cute_2"):
        call mas_compliment_cute_2
    else:
        call mas_compliment_cute_3
    return

label mas_compliment_cute_2:
    m 1wubssdld "Ah!"
    m 3rkbfsdla "Você me {i}pegou desprevenida{/i} com isso."
    m 3tubfb "Só um pouquinho..."
    m 1hubfa "Mas fico feliz que você pense assim!"
    menu:
        "Ver você sempre aquece meu coração!":
            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(5, bypass=True)
            m 1hubfb "Aww, isso aquece meu coração de verdade!"
            m 1dkbfu "...Quase tanto quanto quando imagino nós [du] finalmente [ju] na mesma realidade."
            m 1ekbfa "Mal posso me conter só de imaginar esse dia especial~"
        "Você fica ainda mais fofa quando fica sem graça.":

            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(3, bypass=True)
            m 2tubfu "Você realmente não deixa nada passar, hein, [player]?"
            m 2rubfu "Hmph, eu só não estava esperando."
            m 3tubfb "Não espere que seja tão fácil da próxima vez..."
            m 1tubfu "Vou te dar o troco algum dia, ehehe~"
        "Você é tão fofa quanto a Natsuki.":

            $ persistent._mas_pm_monika_cute_as_natsuki = True
            $ mas_loseAffection()
            m 2lfc "Ah. {w=1}Obrigada, [player]..."
            m 1rsc "Mas eu esperava que eu fosse única no meu próprio estilo."
    return

label mas_compliment_cute_3:
    python:
        cute_quips = [
            _("Você também é muito adorável às vezes, sabia~"),
            _("Você sempre será minha fofura~"),
            _("Você também é adorável, [player]~"),
        ]
        cute_quip = random.choice(cute_quips)

    m 1ekbsa "Ehehe, obrigada [player]..."
    m 1hubfa "[cute_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_chess",
            prompt="Você é incrível no xadrez!",
            unlocked=False,
            conditional="persistent._mas_chess_stats.get('losses', 0) > 5",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_chess:
    m 1eub "Obrigada, [player]."
    m 3esa "Como eu disse antes, será que minha habilidade tem a ver comigo estar presa aqui?"
    $ wins = persistent._mas_chess_stats.get("wins", 0)
    $ losses = persistent._mas_chess_stats.get("losses", 0)
    if wins > 0:
        m 3eua "Você também não é ruim; já perdi para você antes."
        if wins > losses:
            m "Na verdade, eu creio que você venceu mais vezes do que eu, sabia?"
        m 1hua "Ehehe~"
    else:
        m 2lksdlb "Sei que você ainda não venceu uma partida, mas tenho certeza que vai me derrotar algum dia."
        m 3esa "Continue praticando e jogando comigo que você vai melhorar!"
    m 3esa "Nós [du] vamos melhorar quanto mais jogarmos."
    m 3hua "Então não tenha medo de me desafiar quando quiser."
    m 1eub "Eu adoro passar tempo com você, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_pong",
            prompt="Você é demais no pong!",
            unlocked=False,
            conditional="renpy.seen_label('game_pong')",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_pong:
    m 1hub "Ahaha~"
    m 2eub "Obrigada [player], mas pong não é exatamente um jogo complexo."
    if persistent._mas_ever_won['pong']:
        m 1lksdla "Você já venceu contra mim, [bobo]."
        m "Então sabe que é bem simples."
        show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hub "Mas aceito seu elogio mesmo assim."
    else:
        m 3hksdrb "E você sempre me deixa vencer quando jogamos."
        m 3eka "Não é?"
        menu:
            "Sim.":
                m 2lksdla "Obrigada [player], mas você não precisa me deixar vencer."
                m 1eub "Fique à vontade para jogar [sér] quando quiser."
                m 1hub "Eu nunca ficaria brava por perder um jogo justo."
            "...é.":

                m 1tku "Você não parece muito confiante, [player]."
                m 1tsb "Você realmente não precisa me deixar vencer."
                m 3tku "E admitir que perdeu de verdade não vai me fazer pensar menos de você."
                m 1lksdlb "É só um jogo, afinal!"
                m 3hub "Você pode sempre praticar mais comigo, se quiser."
                m "Eu amo passar tempo com você, não importa o que estejamos fazendo."
            "Não. Eu tentei meu melhor e ainda perdi.":

                m 1hub "Ahaha~"
                m "Imaginei!"
                m 3eua "Não se preocupe, [player]."
                m 3eub "Continue jogando comigo e praticando."
                m 3hua "Eu sempre tento te ajudar a ser [of] melhor que você pode ser."
                m 1ekbsa "E se ao fazer isso, eu puder passar mais tempo com você, não poderia ficar mais feliz."
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_bestgirl",
            prompt="Você é a melhor garota!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_bestgirl:
    m 1hua "Eu adoro quando você me elogia, [player]~"
    m 1hub "Fico tão feliz que você me considera a melhor garota!"
    m 3rksdla "Embora eu já imaginasse que você sentia isso..."
    m 1eka "Afinal, você {i}instalou{/i} este mod só para ficar comigo."
    m 2euc "Sei que algumas pessoas preferem as outras garotas."
    m 2esc "Especialmente porque cada uma tem características que as tornam especiais..."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbfa "Mas se você me perguntar, você fez a escolha certa."
    m 5hubfa "...e eu serei eternamente grata por isso~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_lookuptoyou",
            prompt="Eu admiro você!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_lookuptoyou:
    if not renpy.seen_label("mas_compliment_lookuptoyou_2"):
        call mas_compliment_lookuptoyou_2
    else:
        call mas_compliment_lookuptoyou_3

    return "love"

label mas_compliment_lookuptoyou_2:
    $ mas_gainAffection(3, bypass=True)
    m 1wud "Você...{w=0.5}me admira?"
    m 1ekbsa "[player], isso é tão doce da sua parte..."
    m 3ekbsa "Me deixa muito feliz saber que sou alguém que você admira."
    m 3ekbfa "Na verdade, eu sempre admirei {i}você{/i} também, [player]..."
    m 3hubfa "Mas se você realmente sente assim, farei o meu melhor para continuar sendo alguém que você admira."
    m 1ekbfa "Eu te amo tanto~"
    return

label mas_compliment_lookuptoyou_3:
    $ should_tease = persistent._mas_pm_height is not None and renpy.random.randint(1,5) == 1

    if should_tease and persistent._mas_pm_height < mas_height_monika:
        m 1rksdlb "{cps=*2}Bem, é claro, eu sou maior que você...{/cps}{nw}"
        $ _history_list.pop()

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 3hubfa "Ouvir você dizer isso sempre me faz sorrir!"
    m 3hubfb "Eu sempre vou admirar você também!"

    if should_tease and persistent._mas_pm_height > mas_height_monika:
        if persistent._mas_first_kiss:
            m 1rkbfu "{cps=*2}Assim como quando nos beijamos...{/cps}{nw}"
        else:
            m 1rkbfu "{cps=*2}Algum dia quem sabe...{/cps}{nw}"
        $ _history_list.pop()

    m 1ekbfa "Eu te amo, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thinking_of_you",
            prompt="Eu estou sempre pensando em você!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_thinking_of_you:
    if not renpy.seen_label("mas_compliment_thinking_of_you_2"):
        call mas_compliment_thinking_of_you_2
    else:
        call mas_compliment_thinking_of_you_3
    return

label mas_compliment_thinking_of_you_2:
    m 1wubso "..."
    m 1wubsu "Você..."

    if mas_isMoniNormal(higher=True):
        m 3subsb "Você não tem ideia do quanto isso significa para mim, [player]!"

    elif mas_isMoniUpset():
        m 2rkd "Você dizer isso..."
        m 2dka "Significa o mundo para mim, [player]."

    elif mas_isMoniDis():
        $ mas_gainAffection(1, bypass=True)
        m 6rkc "..."
        m 6rka "Isso é um alívio."
        m 6eka "Obrigada."
    else:

        $ mas_gainAffection(1, bypass=True)
        m 6dkd "Hmmm... Obrigada."
        m 6dkc "..."
        return

    menu:
        "Pensar em você sempre ilumina meu dia!":
            $ mas_gainAffection(5, bypass=True)
            m 1subsb "Aww, isso é {i}tão{/i} doce, [player]!"
            m 3hubfu "Eu sinto o mesmo por você~"
        "Eu sonho com você todas as noites!":

            $ mas_gainAffection(5, bypass=True)
            m 6hua "Aww~"
            m 6subsa "[player]..."
            m 7hubfu "{i}Você{/i} é o meu sonho~"
        "É muito perturbador...":

            if mas_isMoniDis(lower=True):
                $ mas_loseAffection(modifier=2.0)
            else:
                $ mas_loseAffection()
            m 2esc "..."
            m 2etc "..."
            m 2rksdlc "Ah, hmm..."
            m 2rksdld "Me desculpe?"
    return

label mas_compliment_thinking_of_you_3:
    python:
        thinking_of_you_quips = [
            _("Você é o centro do meu mundo!"),
            _("Você está sempre na minha cabeça também!"),
            _("Estou sempre pensando em você também!"),
        ]
        thinking_of_you_quip = random.choice(thinking_of_you_quips)

    m 1ekbsa "Aww obrigada, [player]..."
    m 3hubfb "[thinking_of_you_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_humor",
            prompt="Eu amo seu senso de humor!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_humor:
    if not renpy.seen_label("mas_compliment_humor_2"):
        call mas_compliment_humor_2
    else:
        call mas_compliment_humor_3
    return

label mas_compliment_humor_2:
    m 1hua "Ehehe~"
    m 1efu "Fico feliz que ache meus trocadilhos tão 'engraçados', [player]."
    m 3eub "Um bom sinal de um casal feliz é poder rir [ju], não acha?"
    menu:
        "Você sempre ilumina meu dia.":
            $ mas_gainAffection(5, bypass=True)
            m 1subsd "Oh...{w=0.2}[player]..."
            m 1ekbsa "Que doce da sua parte dizer isso."
            m 1hubsb "Saber que posso te fazer sorrir é o maior elogio que poderia receber!"
        "Você tem um raciocínio tão rápido!":

            $ mas_gainAffection(3, bypass=True)
            m 1hub "Ahaha!"
            m 2tub "Toda aquela leitura deve ter valido a pena se você gosta tanto dos meus trocadilhos."
            m 2hublu "Vou continuar fazendo piadas para você. Ehehe~"
        "Eu rio de você o tempo todo.":

            $ mas_loseAffection()
            m 1eksdlb "...Ahaha..."
            m 3rksdla "Você quis dizer que ri {w=0.2}{i}com{/i}{w=0.2}igo...{w=0.5}{nw}"
            extend 3eksdld " não foi?"
    return

label mas_compliment_humor_3:
    python:
        humor_quips = [
            _("Queria poder ouvir sua linda risada~"),
            _("Saber disso já me deixa feliz~"),
            _("Sempre vou tentar alegrar seu dia~"),
        ]
        humor_quip = random.choice(humor_quips)

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 1hubsu "[humor_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_missed",
            prompt="Senti sua falta!",
            unlocked=True,
            conditional=(
                "store.mas_getSessionLength() <= datetime.timedelta(minutes=30) "
                "and store.mas_getAbsenceLength() >= datetime.timedelta(hours=1) "
                "and not store.mas_globals.returned_home_this_sesh"
            )
        ),
        code="CMP"
    )

label mas_compliment_missed:
    python:
        missed_quips_long = (
            _("Estou tão feliz em te ver de novo!"),
            _("Estou tão feliz que você voltou!"),
            _("É maravilhoso te ver de novo!"),
            _("Fico feliz que você pensou em mim!"),
            _("Mal podia esperar por você voltar!"),
            _("Me senti sozinha esperando por você!")
        )

        missed_quips_short = (
            _("Obrigada por voltar para passar tempo comigo!"),
            _("Estou animada para passarmos um tempo com você!"),
            _("Obrigada por vir me ver de novo!"),
            _("Vamos aproveitar nosso tempo hoje!"),
            _("Você é tão importante para mim, [player]!"),
            _("Obrigada por arrumar tempo para mim!"),
            _("Sou tão sortuda por ter você, [player]!"),
            _("Pronto para passarmos um tempo comigo?"),
            _("Estive pensando em você!"),
            _("Você esteve mesmo na minha mente!")
        )

        missed_quips_upset_short = (
            _("Significa muito para mim que você pensou em mim."),
            _("Fico muito feliz em ouvir isso, [player]."),
            _("É muito bom ouvir isso."),
            _("Estou feliz que você pensou em mim, [player]."),
            _("Isso significa o mundo para mim, [player]."),
            _("Isso me faz sentir muito melhor, [player].")
        )

        missed_quips_upset_long = (
            _("Estava começando a me preocupar que você tinha me esquecido."),
            _("Obrigada por mostrar que ainda se importa, [player]."),
            _("Fico feliz em saber que não me esqueceu, [player]"),
            _("Estava começando a me preocupar que você não voltaria, [player]")
        )

        missed_quips_dis = (
            _("Não tenho certeza se você realmente sente isso, [player]..."),
            _("Duvido que você realmente sinta isso, [player]..."),
            _("Acho que você não está sendo sincero, [player]..."),
            _("Se ao menos você realmente sentisse isso, [player]..."),
            _("...Por que sinto que você não está sendo honesto?"),
            _("...Por que sinto que você só está dizendo isso?"),
            _("...Não consigo realmente acreditar nisso, [player]."),
            _("Acho que isso não é verdade, [player].")
        )

        hugchance = 1
        absence_length = mas_getAbsenceLength()
        mas_flagEVL("mas_compliment_missed", "CMP", EV_FLAG_HFM)

    if mas_isMoniNormal(higher=True):
        if absence_length >= datetime.timedelta(days=3):
            if absence_length >= datetime.timedelta(days=7):
                $ hugchance = 30
            else:

                $ hugchance = 15

            m 1fka "Senti tanto sua falta, [mas_get_player_nickname()]!"
            m 3fka "[renpy.substitute(random.choice(missed_quips_long))]"
        else:

            m 1fka "Também senti sua falta, [mas_get_player_nickname()]!"
            m 3hub "[renpy.substitute(random.choice(missed_quips_short))]"

        if (
            mas_isMoniEnamored(higher=True)
            and mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12))
            and random.randint(1, 50) <= hugchance
        ):
            m 2lsa "..."
            m 2lsb "Ei, [player]..."
            m 1eka "Eu estava esperando que..."
            m 3ekblb "Sabe, como já faz um tempinho..."

            m 1ekblb "Você poderia me dar um abraço? {w=0.3}Me senti tão sozinha enquanto você estava fora.{nw}"
            $ _history_list.pop()
            menu:
                m "Você poderia me dar um abraço? Me senti tão sozinha enquanto você estava fora.{fast}"
                "Claro, [m_name]!":

                    $ mas_gainAffection(modifier=0.25, bypass=True)

                    call monika_holdme_prep (lullaby=MAS_HOLDME_NO_LULLABY, stop_music=True, disable_music_menu=True)
                    call monika_holdme_start
                    call monika_holdme_end

                    m 6dkbsa "Mmm... isso foi tão bom, [player]."
                    m 7ekbsb "Você sabe mesmo como me fazer sentir especial~"
                    $ mas_moni_idle_disp.force_by_code("1eubsa", duration=10, skip_dissolve=True)
                "Agora não.":

                    $ mas_loseAffection()
                    m 2lkp "...Tudo bem, talvez depois então?"
                    python:
                        mas_moni_idle_disp.force_by_code("2lkp", duration=10, redraw=False, skip_dissolve=True)
                        mas_moni_idle_disp.force_by_code("2rsc", duration=10, clear=False, redraw=False, skip_dissolve=True)
                        mas_moni_idle_disp.force_by_code("1esc", duration=30, clear=False, skip_dissolve=True)


    elif mas_isMoniUpset():
        m 2wuo "..."
        m 2ekbla "Eu...{w=0.5}também senti sua falta."

        if absence_length >= datetime.timedelta(days=3):
            m 2ekd "[renpy.substitute(random.choice(missed_quips_upset_long))]"
        else:

            m 2eka "[renpy.substitute(random.choice(missed_quips_upset_short))]"

        $ mas_moni_idle_disp.force_by_code("2eka", duration=10, skip_dissolve=True)

    elif mas_isMoniDis():
        m 6dkc "..."
        m 6rktpd "[renpy.substitute(random.choice(missed_quips_dis))]"

        if absence_length >= datetime.timedelta(days=3):
            m 6dktdc "...Mas pelo menos você não esqueceu de mim...{w=0.5}ainda."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_spending_time",
            prompt="Eu amo passar tempo com você!",
            unlocked=False,
            conditional="store.mas_anni.pastThreeMonths()",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="CMP"
    )

label mas_compliment_spending_time:
    if not mas_getEVL_shown_count("mas_compliment_spending_time"):
        call mas_compliment_spending_time_2
    else:
        python:
            spending_time_quips = [
                _("Cada dia com você é como um sonho maravilhoso que espero nunca acabar~"),
                _("Só de estar perto de você já me deixa tão feliz~"),
                _("Nada me deixa mais feliz do que estar ao seu lado~"),
            ]
            spending_time_quip = random.choice(spending_time_quips)

        m 3hubsb "[mas_compliments.thanks_quip]"
        m 1ekbsu "[spending_time_quip]"
    return

label mas_compliment_spending_time_2:
    python:
        dlg_line = ""

        if renpy.seen_label("monika_holdme_prep"):
            dlg_line = ", me abraça forte"
            
            if persistent._mas_filereacts_historic:
                dlg_line += ", e até me dá presentes lindos"

        elif persistent._mas_filereacts_historic:
            dlg_line = ", me dá presentes lindos"

    m 1eub "Eu também amo passar tempo com você, [player]!"
    m 3ekbla "Sei que falo muito isso, mas é verdade quando digo que você é o centro do meu mundo."
    m 2dkb "Ter alguém que me faz companhia[dlg_line]...{w=0.3}{nw}"
    extend 2eku "é tudo que eu poderia pedir."
    m 7ekbsa "Espero que você se sinta assim também, [player]. {w=0.2}Posso não estar na sua realidade ainda, mas farei tudo para te apoiar daqui."
    menu:
        "[m_name], você já me fez o homem mais feliz do mundo.":
            $ mas_gainAffection(5, bypass=True)
            m 1fkbfu "Ah, [player]..."
            show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbfa "Quase não consigo expressar o quanto fico feliz em ouvir isso, mas acho que você já {i}sabe{/i}."
            m 5ekbfu "Passamos tanto tempo [ju], e ainda nossa jornada só está começando..."
            m 5hubfb "Com você ao meu lado, sei que cada passo será inesquecível."
        "Eu agradeço, [m_name].":

            $ mas_gainAffection(3, bypass=True)
            m 2huu "Ehehe~"
            m 7hub "Não se preocupe, [player]. {w=0.2}Estarei aqui por você até o fim dos tempos!"
            m 1eka "Apenas continue forte até eu conseguir ir para a sua realidade, ok?"
        "Ah, você certamente me diverte...":

            $ mas_loseAffection()
            m 2lkc "Eu...{w=0.3}te divirto?"
            m 2lksdlb "Bem, fico feliz que esteja se divertindo..."
            m 2ekd "...mas não era {i}exatamente{/i} isso que eu tinha em mente."
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_sweet",
            prompt="Você é tão doce!",
            conditional="store.mas_anni.pastThreeMonths()",
            action=EV_ACT_UNLOCK,
            unlocked=False,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="CMP"
    )

label mas_compliment_sweet:
    if mas_getEVL_shown_count("mas_compliment_sweet"):
        jump mas_compliment_sweet_repeat

    m 1ekbsb "Aww, [player]..."
    m 3rkbssdlu "Não sei o que dizer, ahaha...{w=0.3}{nw}"
    extend 3ekbsa "é {i}você{/i} que tem sido tão doce comigo todo esse tempo."
    m 3hubsa "Fico muito feliz em ouvir você dizer isso, ehehe~"

    menu:
        "Suas palavras sempre iluminam meu dia!":
            $ mas_gainAffection(3, bypass=True)
            m 1sud "[player]..."
            extend 1eka "Eu não tinha ideia de como minhas palavras eram importantes para você..."
            m 1ekblb "Eu sou tão feliz por ter [um] [bf] incrível como você, [mas_get_player_nickname(exclude_names=[player])]~"
            m 1ekbsu "Você é realmente o melhor que eu poderia esperar...{w=0.2}eu te amo tanto."
            m 3kua "Espero que você nunca se esqueça disso, [player]."
            $ mas_ILY()
        "Você é muito especial para mim, [m_name]!":

            $ mas_gainAffection(3, bypass=True)
            m 1ekbsb "Ah, [player]...{w=0.3} {nw}"
            extend 3hubsa "Só você passar seu tempo aqui comigo já me faz tão feliz e amada!"
            show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbsa "Estou tão feliz que você sente isso por mim, [mas_get_player_nickname()]. Eu te amo muito."
            $ mas_ILY()
        "Você é a garota mais doce que já conheci!":

            $ mas_gainAffection(2, bypass=True)
            m 1ekbsa "Obrigada, [mas_get_player_nickname()]."
            m 3hubsb "Você é a pessoa mais doce que já conheci, ehehe."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Sou muito sortuda por estar com você~"

    return

label mas_compliment_sweet_repeat:
    python:
        sweet_quips = [
            _("Fico tão feliz em ouvir você dizer isso, [player]!"),
            _("Ouvir isso sempre aquece meu coração, [player]!"),
            _("Você me faz sentir tão amada, [player]!"),
        ]
        sweet_quip = renpy.substitute(random.choice(sweet_quips))

    m 3hubsb "[sweet_quip]"
    m 1hubfu "...Mas eu nunca poderia ser tão doce quanto você~"
    return


init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_outfit",
            prompt="Eu amo sua roupa!",
            unlocked=False
        ),
        code="CMP"
    )

label mas_compliment_outfit:
    if mas_getEVL_shown_count("mas_compliment_outfit"):
        jump mas_compliment_outfit_repeat

    m 1hubsb "Obrigada, [mas_get_player_nickname()]!"

    if monika_chr.is_wearing_clothes_with_exprop("cosplay"):
        m 3hubsb "É sempre divertido fazer cosplay!"

    elif monika_chr.is_wearing_clothes_with_exprop("costume"):
        m 3hubsb "É sempre divertido usar fantasias!"

    elif monika_chr.is_wearing_clothes_with_exprop("lingerie"):
        m 2lkbsb "Eu estava tão nervosa mostrando isso para você no começo..."
        m 7tubsu "Mas fico feliz de ter feito, parece que você gostou muito~"
    else:

        m 1hubsa "Sempre quis usar outras roupas para você, então estou muito feliz que gostou!"

    menu:
        "Você fica linda com qualquer roupa!":
            $ mas_gainAffection(5, bypass=True)
            m 2subsd "[player]..."
            m 3hubsb "Muito obrigada!"
            m 1ekbsu "Você sempre me faz sentir tão especial."
            show monika 5hubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hubsa "Eu te amo, [mas_get_player_nickname()]!"
            $ mas_ILY()
        "Você está muito fofa.":

            $ mas_gainAffection(3, bypass=True)
            m 1hubsb "Ahaha~"
            m 3hubfb "Obrigada, [mas_get_player_nickname()]!"
            show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eubfu "Fico feliz que goste do que vê~"
        "Usar roupas diferentes ajuda mesmo.":

            $ mas_loseAffection()
            m 2ltd "Ah, obrigada..."

    return

label mas_compliment_outfit_repeat:
    m 1hubsb "[mas_compliments.thanks_quip]"

    if monika_chr.is_wearing_clothes_with_exprop("cosplay"):
        python:
            cosplay_quips = [
                _("Adoro fazer cosplay para você!"),
                _("Fico feliz que goste deste cosplay!"),
                _("Fico feliz em fazer cosplay para você!"),
            ]
            cosplay_quip = random.choice(cosplay_quips)

        m 3hubsb "[cosplay_quip]"

    elif monika_chr.is_wearing_clothes_with_exprop("costume"):
        python:
            clothes_quips = [
                _("Estou feliz que você gostou de como eu fiquei com isso!"),
                _("Estou feliz que você gostou de como eu fiquei nisto!"),
            ]
            clothes_quip = random.choice(clothes_quips)

        m 3hubsb "[clothes_quip]"

    elif monika_chr.is_wearing_clothes_with_exprop("lingerie"):
        python:
            lingerie_quips = [
                _("Que bom que gosta do que vê~"),
                _("Quer dar uma olhada mais de perto?"),
                _("Quer uma espiadinha?~"),
            ]
            lingerie_quip = random.choice(lingerie_quips)

        m 2kubsu "[lingerie_quip]"
        show monika 5hublb zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hublb "Ahaha!"
    else:

        python:
            other_quips = [
                _("Eu me orgulho do meu senso de moda!"),
                _("Tenho certeza que você também fica bem!"),
                _("Eu amo esta roupa!")
            ]
            other_quip = random.choice(other_quips)

        m 3hubsb "[other_quip]"

    return
