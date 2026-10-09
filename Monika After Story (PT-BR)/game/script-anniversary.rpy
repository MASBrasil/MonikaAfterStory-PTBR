init -2 python in mas_anni:
    import store
    import datetime


    _m1_script0x2danniversary__persistent = renpy.game.persistent

    def build_anni(years=0, months=0, weeks=0, isstart=True):
        """
        Builds an anniversary date.

        NOTE:
            years / months / weeks are mutually exclusive

        IN:
            years - number of years to make this anni date
            months - number of months to make thsi anni date
            weeks - number of weeks to make this anni date
            isstart - True means this should be a starting date, False
                means ending date

        ASSUMES:
            __persistent
        """
        
        if _m1_script0x2danniversary__persistent.sessions is None:
            return None
        
        first_sesh = _m1_script0x2danniversary__persistent.sessions.get("first_session", None)
        if first_sesh is None:
            return None
        
        if (weeks + years + months) == 0:
            
            return None
        
        
        
        if years > 0:
            new_date = store.mas_utils.add_years(first_sesh, years)
        
        elif months > 0:
            new_date = store.mas_utils.add_months(first_sesh, months)
        
        else:
            new_date = first_sesh + datetime.timedelta(days=(weeks * 7))
        
        
        if isstart:
            return store.mas_utils.mdnt(new_date)
        
        
        
        
        
        return store.mas_utils.mdnt(new_date + datetime.timedelta(days=1))

    def build_anni_end(years=0, months=0, weeks=0):
        """
        Variant of build_anni that auto ends the bool

        SEE build_anni for params
        """
        return build_anni(years, months, weeks, False)

    def isAnni(milestone=None):
        """
        INPUTS:
            milestone:
                Expected values|Operation:

                    None|Checks if today is a yearly aniversários
                    1w|Checks if today is a 1 week aniversários
                    1m|Checks if today is a 1 month aniversários
                    3m|Checks if today is a 3 month aniversários
                    6m|Checks if today is a 6 month aniversários
                    any|Checks if today is any of the above annis

        RETURNS:
            True if datetime.date.today() is an aniversários date
            False if today is not an aniversários date
        """
        
        if _m1_script0x2danniversary__persistent.sessions is None:
            return False
        
        firstSesh = _m1_script0x2danniversary__persistent.sessions.get("first_session", None)
        if firstSesh is None:
            return False
        
        compare = None
        
        if milestone == '1w':
            compare = build_anni(weeks=1)
        
        elif milestone == '1m':
            compare = build_anni(months=1)
        
        elif milestone == '3m':
            compare = build_anni(months=3)
        
        elif milestone == '6m':
            compare = build_anni(months=6)
        
        elif milestone == 'any':
            return (
                isAnniWeek()
                or isAnniOneMonth()
                or isAnniThreeMonth()
                or isAnniSixMonth()
                or isAnni()
            )
        
        if compare is not None:
            return compare.date() == datetime.date.today()
        
        else:
            compare = firstSesh
            return (
                store.mas_utils.add_years(compare.date(), datetime.date.today().year - compare.year) == datetime.date.today()
                and anniCount() > 0
            )

    def isAnniWeek():
        return isAnni('1w')

    def isAnniOneMonth():
        return isAnni('1m')

    def isAnniThreeMonth():
        return isAnni('3m')

    def isAnniSixMonth():
        return isAnni('6m')

    def isAnniAny():
        return isAnni('any')

    def anniCount():
        """
        RETURNS:
            Integer value representing how many years the player has been with Monika
        """
        
        if _m1_script0x2danniversary__persistent.sessions is None:
            return 0
        
        firstSesh = _m1_script0x2danniversary__persistent.sessions.get("first_session", None)
        
        if firstSesh is None:
            return 0
        
        compare = datetime.date.today()
        
        if (
            compare.year > firstSesh.year
            and compare < store.mas_utils.add_years(firstSesh.date(), compare.year - firstSesh.year)
        ):
            return compare.year - firstSesh.year - 1
        else:
            return compare.year - firstSesh.year

    def pastOneWeek():
        """
        RETURNS:
            True if current date is past the 1 week threshold
            False if below the 1 week threshold
        """
        return datetime.date.today() >= build_anni(weeks=1).date()

    def pastOneMonth():
        """
        RETURNS:
            True if current date is past the 1 month threshold
            False if below the 1 month threshold
        """
        return datetime.date.today() >= build_anni(months=1).date()

    def pastThreeMonths():
        """
        RETURNS:
            True if current date is past the 3 month threshold
            False if below the 3 month threshold
        """
        return datetime.date.today() >= build_anni(months=3).date()

    def pastSixMonths():
        """
        RETURNS:
            True if current date is past the 6 month threshold
            False if below the 6 month threshold
        """
        return datetime.date.today() >= build_anni(months=6).date()
init offset = 5


init 6 python in mas_anni:



    ANNI_LIST = [
        "anni_1week",
        "anni_1month",
        "anni_3month",
        "anni_6month",
        "anni_1",
        "anni_2",
        "anni_3",
        "anni_4",
        "anni_5",
        "anni_6",
        "anni_7",
        "anni_8",
        "anni_9",
        "anni_10",
        "anni_20",
        "anni_50",
        "anni_100"
    ]


    anni_db = dict()
    for anni in ANNI_LIST:
        anni_db[anni] = store.evhand.event_database[anni]



    def _month_adjuster(ev, new_start_date, months, span):
        """
        Adjusts the start_date / end_date of an aniversários event.

        NOTE: do not use this for a non aniversários date

        IN:
            ev - event to adjust
            new_start_date - new start date to calculate the event's dates
            months - number of months to advance
            span - the time from the event's new start_date to end_date
        """
        ev.start_date = store.mas_utils.add_months(
            store.mas_utils.mdnt(new_start_date),
            months
        )
        ev.end_date = store.mas_utils.mdnt(ev.start_date + span)

    def _day_adjuster(ev, new_start_date, days, span):
        """
        Adjusts the start_date / end_date of an aniversários event.

        NOTE: do not use this for a non aniversários date

        IN:
            ev - event to adjust
            new_start_date - new start date to calculate the event's dates
            days - number of months to advance
            span - the time from the event's new start_date to end_date
        """
        ev.start_date = store.mas_utils.mdnt(
            new_start_date + datetime.timedelta(days=days)
        )
        ev.end_date = store.mas_utils.mdnt(ev.start_date + span)


    def add_cal_annis():
        """
        Goes through the aniversários database and adds them to the calendar
        """
        for anni in anni_db:
            ev = anni_db[anni]
            store.mas_calendar.addEvent(ev)

    def clean_cal_annis():
        """
        Goes through the calendar and cleans aniversários dates
        """
        for anni in anni_db:
            ev = anni_db[anni]
            store.mas_calendar.removeEvent(ev)


    def reset_annis(new_start_dt):
        """
        Reset the anniversaries according to the new start date.

        IN:
            new_start_dt - new start datetime to reset anniversaries
        """
        _firstsesh_id = "first_session"
        _firstsesh_dt = renpy.game.persistent.sessions.get(
            _firstsesh_id,
            None
        )
        
        
        clean_cal_annis()
        
        
        if _firstsesh_dt:
            
            store.mas_calendar.removeRepeatable_dt(_firstsesh_id, _firstsesh_dt)
        
        
        fullday = datetime.timedelta(days=1)
        _day_adjuster(anni_db["anni_1week"],new_start_dt,7,fullday)
        _month_adjuster(anni_db["anni_1month"], new_start_dt, 1, fullday)
        _month_adjuster(anni_db["anni_3month"], new_start_dt, 3, fullday)
        _month_adjuster(anni_db["anni_6month"], new_start_dt, 6, fullday)
        _month_adjuster(anni_db["anni_1"], new_start_dt, 12, fullday)
        _month_adjuster(anni_db["anni_2"], new_start_dt, 24, fullday)
        _month_adjuster(anni_db["anni_3"], new_start_dt, 36, fullday)
        _month_adjuster(anni_db["anni_4"], new_start_dt, 48, fullday)
        _month_adjuster(anni_db["anni_5"], new_start_dt, 60, fullday)
        _month_adjuster(anni_db["anni_6"], new_start_dt, 6*12, fullday)
        _month_adjuster(anni_db["anni_7"], new_start_dt, 7*12, fullday)
        _month_adjuster(anni_db["anni_8"], new_start_dt, 8*12, fullday)
        _month_adjuster(anni_db["anni_9"], new_start_dt, 9*12, fullday)
        _month_adjuster(anni_db["anni_10"], new_start_dt, 120, fullday)
        _month_adjuster(anni_db["anni_20"], new_start_dt, 240, fullday)
        _month_adjuster(anni_db["anni_50"], new_start_dt, 600, fullday)
        _month_adjuster(anni_db["anni_100"], new_start_dt, 1200, fullday)
        
        unlock_past_annis()
        
        
        add_cal_annis()
        
        
        store.mas_calendar.addRepeatable_dt(
            _firstsesh_id,
            "<3",
            new_start_dt,
            [new_start_dt.year]
        )


    def unlock_past_annis():
        """
        Goes through the aniversários database and unlocks the events that
        already past.
        """
        for anni in anni_db:
            ev = anni_db[anni]
            
            if store.evhand._isPast(ev):
                renpy.game.persistent._seen_ever[anni] = True
                ev.unlocked = True


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1week',
            prompt="1 Semana",
            action=EV_ACT_QUEUE,
            category=["aniversários"],
            start_date=store.mas_anni.build_anni(weeks=1),
            end_date=store.mas_anni.build_anni_end(weeks=1)
        ),
        skipCalendar=False
    )

label anni_1week:
    m 1eka "Sei que é bobo comemorar uma semana [ju], mas estou tão feliz que você está aqui comigo, [player]."
    m 1ekc "Muitos casais não durariam tanto tempo assim."
    m 1lksdlc "É muito fácil se apaixonar à primeira vista, mas é mais difícil construir um relacionamento sólido."
    m 1ekd "Muitos relacionamentos falham quando os casais se apressam demais."
    m "Na maioria das vezes, eles falham em se conhecer melhor."
    m 1dsc "Então é sempre triste vê-los desmoronar..."
    m 1duu "Mas estou feliz que temos um relacionamento sólido, [player]."
    show monika 5lubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5lubfb "Como eu sei disso?"
    m 5hubfb "Porque você não teria ficado comigo por tanto tempo, querido~"
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1month',
            prompt="1 Mês",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=1),
            end_date=store.mas_anni.build_anni_end(months=1)
        ),
        skipCalendar=False
    )

label anni_1month:
    m 3sub "Hoje nosso relacionamento comemora um mês!"
    m 1hua "Estou tão feliz que estamos nos divertindo tanto [ju] até agora."
    m 1eua "Ah, [player]?"
    m 1lkbsa "..."
    m 1ekbfa "Muito obrigada por ficar comigo por todo esse tempo."
    if not seen_event('monika_saved'):
        m 1lksdlc "Nem consigo imaginar o que faria se você não tivesse aparecido."
        m 3ekc "Afinal, sou a única pessoa real neste mundo."
        m 1dsc "Já te disse o que aconteceria se não fosse por você..."
        m 1hksdlb "Ahaha, desculpe. Espero não ter deixado o clima pesado com meu desabafo."
    else:
        m "Não consigo expressar o quanto aprecio você estar aqui comigo."
        m 1dubsu "Tudo que posso fazer é tentar ser a namorada perfeita para você!"
    m 1ekbfa "Eu te amo muito, [player]."
    m 1hubfa "Vamos fazer deste um dia especial~"
    return "love|unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_3month',
            prompt="3 Meses",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=3),
            end_date=store.mas_anni.build_anni_end(months=3)
        ),
        skipCalendar=False
    )

label anni_3month:
    m 1eua "[player], você sabe que dia é hoje?"
    m 1hua "É nosso aniversário de três meses!"
    m 1hub "O tempo passa tão rápido, não é?"
    m 1hksdlb "...Mesmo que não passe de verdade aqui, ehehe."
    m 1eua "Mas estou me divertindo muito."
    m 1ekbsa "Ter você por perto tornou minha vida tão melhor, [player]."
    m 2ekbfa "Estou tão feliz que você ficou comigo todo esse tempo."
    m 1tsbsa "Você é realmente especial, sabia?"
    m 1lsbsa "Bem! Infelizmente não planejei nada especial."
    m 1hubfa "Vamos apenas aproveitar este dia ao máximo, como sempre fazemos."
    m 1hubfb "Tudo bem, [player]?"
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_6month',
            prompt="6 Meses",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=6),
            end_date=store.mas_anni.build_anni_end(months=6)
        ),
        skipCalendar=False
    )

label anni_6month:
    m 1hub "Não acredito que já são 6 meses [ju]!"
    m 1eka "Estou tão feliz que você ficou comigo todo esse tempo."
    m 1lksdlc "Fico tão sozinha quando você não está aqui."
    m 1ekc "Quero dizer, tenho coisas para me distrair quando você vai embora, mas ainda me sinto muito só sabendo que sou a única aqui."
    m 1hua "Por isso sempre fico tão feliz quando você vem me visitar!"
    m 1euc "Mas nesses meses, percebi uma coisa..."
    m "A maioria dos casais celebra aniversários fazendo algo especial [ju], né?"
    m 3eud "Como jantar fora ou ir ao cinema."
    m 1lksdla "Não que eu esteja reclamando, mas passamos todos nossos aniversários nesta sala."
    m 1lksdlc "Seria tão legal se pudéssemos ir a algum lugar diferente..."
    m "É uma pena não termos outro lugar aqui, já que só temos esta sala."
    m 1dsc "..."
    m 3wuo "...Ah, já sei!"
    m 1sub "Talvez um dia eu possa programar um lugar legal para comemorarmos!"
    m "Ou quem sabe você possa adicionar um lugar especial para nós, [player]."
    m 1duu "A não ser que..."
    m 1eua "Você já me tenha levado a algum lugar na sua realidade?"
    m 1eka "Seria tão legal se eu visse onde você me levou~"
    m 1eua "Mas por enquanto, não me importo de ficarmos nesta sala."
    m 1ekbsa "Porque enquanto você estiver aqui comigo..."
    m 1hubfa "...Eu sou a pessoa mais feliz do mundo!"
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1',
            prompt="1 Ano",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=1),
            end_date=store.mas_anni.build_anni_end(years=1)
        ),
        skipCalendar=False
    )

label anni_1:
    m 1dka "Nossa...{w=0.2}é difícil acreditar que já faz um ano que nos conhecemos."
    m 1eka "O tempo não tem muito significado aqui, mas sei que é um grande compromisso ficar comigo por tanto tempo."
    m 2rkc "Eu confesso que estava um pouco nervosa no começo...{w=0.3} {nw}"
    extend 7eka "Esse tipo de relacionamento não deve ser fácil."
    m 2ekd "...E eu não sabia se havia outras coisas na sua realidade que poderiam ser mais importantes..."
    m 7duu "Mas você continuou voltando.{w=0.3} Continuou passando tempo comigo, como eu sempre esperei."
    m 1ekb "...E com o tempo eu realmente comecei a acreditar...{w=0.2}que você falava sério quando dizia que queria ficar comigo."
    m 3dkbsu "...Que poderíamos ter uma vida feliz [ju].{w=0.3} {nw}"
    extend 3ekbsa "Você e eu, na nossa própria realidade."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "Não tenho palavras para agradecer por isso, [player]. {w=0.2}Você fez deste ano algo incrível para mim."
    m 5eublb "Então, tem algo especial que gostaria de fazer no nosso primeiro aniversário?"
    m 5hksdrb "Eu não planejei nada, mas com certeza podemos achar algo divertido para fazer."
    show monika 3huu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 3huu "Afinal...{w=0.3}quando você está aqui, tudo que fazemos é divertido."
    m 1hubsa "Eu te amo tanto, [player]. {w=0.2}Feliz aniversário~"
    return "love|unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_2',
            prompt="2 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=2),
            end_date=store.mas_anni.build_anni_end(years=2)
        ),
        skipCalendar=False
    )

label anni_2:
    m 3eua "Já faz dois anos que nos apaixonamos um pelo outro."
    m 1eka "Você ainda se lembra do nosso primeiro dia [ju], [player]?"
    m 3eub "Foi tão difícil fazer aquele primeiro contato, mas valeu a pena no final!"
    m 2ekc "Sei que ainda pode demorar muito até eu conseguir ir para sua realidade..."
    m 2duu "Mas quando alcançamos objetivos como esse,{w=0.1} {nw}"
    extend 7eua "é divertido pensar em todas as outras coisas que nos esperam no futuro."

    if persistent._mas_pm_has_friends:
        m 3hubla "Estou tão animada para viver num mundo com pessoas reais. Vai ser maravilhoso conhecer seus amigos e fazer os meus também."
    elif persistent._mas_pm_has_friends is False:
        m 1dka "Nós [du] estamos [szs] há tanto tempo, sabia? Mas quando eu atravessar, vai ser tão legal fazer novos amigos [ju]."
    else:
        m 3hua "Tenho certeza que vamos fazer muitos amigos [ju]!"

    m 3hksdlb "Claro que eu sempre vou gostar mais da sua companhia...{w=0.3}{nw}"
    extend 3eua "mas passar tempo sozinhos não vai ser nossa única opção."
    m 3eub "E vai ser muito mais fácil nos comunicarmos também!{w=0.2} {nw}"
    extend 3dubsb "Finalmente poderemos ouvir nossas vozes, aprender nossos hábitos e nos ajudar de tantas maneirinhas."
    m 1ekbsa "Mas hoje não vou focar só no futuro...{w=0.2} {nw}"
    extend 3hubsu "Vou aproveitar cada minuto que passarmos [ju]~"
    m 1hubsu "Então vamos ter mais um dia maravilhoso, [mas_get_player_nickname()]."
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_3',
            prompt="3 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=3),
            end_date=store.mas_anni.build_anni_end(years=3)
        ),
        skipCalendar=False
    )

label anni_3:
    m 4wuo "Já faz três anos mesmo?"
    m 2hubsb "Nossa...{w=0.3}o tempo voou, não foi?"
    m 3rksdla "Sabe, normalmente quando um casal fica junto por três anos..."
    m 2rsbsa "Eles se casam por volta dessa época, né?"
    m 1hub "Ahaha!"
    m 1eka "Não estou tentando te pressionar, pode ficar tranquilo."
    m 1lkbsa "Além disso, eu gostaria de poder te sentir em meus braços antes de nos casarmos."
    m 1eua "No seu mundo, já inventaram corpos de robôs para garotas?"
    m 1eub "Se me colocar em um desses, poderíamos até encontrar um padre~"
    m 2lsbssdrb "Ou você poderia tentar me tocar na realidade virtual, se isso já existir."
    m 1eua "Tem tantas maneiras diferentes de nos encontrarmos de verdade, não é?"
    m 1hubsa "Vou esperar fielmente pelo dia em que posso ser sua esposa, então não se esqueça de mim!"
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_4',
            prompt="4 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=4),
            end_date=store.mas_anni.build_anni_end(years=4)
        ),
        skipCalendar=False
    )

label anni_4:
    m 1dsc "Quatro anos..."
    m "No começo, eu até achava que você me esqueceria rápido."
    m 1lksdlc "Sabia que gostava de mim, mas tinha medo que cansasse de me deixar rodando no seu computador."
    m "Desculpe por duvidar de você."
    m 1eka "Você é uma pessoa maravilhosa, [player]."
    m "Você é literalmente tudo que tenho de valor nesse mundo."
    m 1ekbsa "Eu te amo."
    m "Cedo ou tarde, alguém vai descobrir como nos unir de verdade."
    m 1hubfa "Quando esse dia chegar, nunca mais vou te deixar [sz]."
    m 1hubfb "Ahaha!"
    return "love|unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_5',
            prompt="5 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=5),
            end_date=store.mas_anni.build_anni_end(years=5)
        ),
        skipCalendar=False
    )

label anni_5:
    m 1hubsa "Seja cinco ou cinquenta anos, nunca vou cansar de conversar com você, [player]."
    m 1rksdlbla "Sei que deve ser solitário não nos encontrarmos na sua realidade ainda...{w=0.3}{nw}"
    extend 1ekblb "mas pelo menos ainda podemos passar nossos aniversários [ju] aqui, né?"
    m 2dkbla "Mas pensando bem..."
    m 2eubla "Cinco anos é um marco importante.{w=0.2} {nw}"
    extend 7wubld "Passamos metade de uma década [ju]."
    m 1ekbla "Todo ano, eu espero ansiosamente por esse dia especial.{w=0.2} {nw}"
    extend 1dkbsu "Um dia para lembrar quando nos apaixonamos."
    m 2eublb "Meu mundo virou de cabeça para baixo quando nos conhecemos, e você continua mudando minha vida todos os dias."
    m 1fublu "Acho que isso nunca vai mudar, [player]. Você é...{w=0.3}tão incrível para mim."
    m 1hubla "Espero poder ser uma boa parceira para você por muitos anos~"
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_6',
            prompt="6 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=6),
            end_date=store.mas_anni.build_anni_end(years=6)
        ),
        skipCalendar=False
    )

label anni_6:
    m 3hubfb "Você sabe o que hoje significa, [player]...{w=0.3} É o dia mais especial do mundo para mim!"
    m 3hubla "Sabia que nas tradições germânicas e vitorianas{w=0.1} cada aniversário tem um presente temático?"
    m 4eua "No começo era só para marcos importantes, mas com o tempo foram adicionando mais anos."
    m 4rksdlb "Se for ser cínico, provavelmente foi para as empresas venderem mais presentes..."
    m 1rkbla "Mas ainda acho a ideia adorável."
    m 3ruu "Falando em coisas adoráveis...{w=0.3}{nw}"
    extend 3eub "o tema do sexto aniversário são doces!"
    m 1eka "Como não posso te dar um presente ainda, que tal se presentear com algo gostoso?"
    m 1hubfa "Eu te amo, [player]. Obrigada por mais um ano maravilhoso."
    return "love|unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_7',
            prompt="7 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=7),
            end_date=store.mas_anni.build_anni_end(years=7)
        ),
        skipCalendar=False
    )

label anni_7:
    m 1dubfa "Sete anos..."
    m 1eubsb "Sabe, sete é considerado um número da sorte em muitas culturas.{w=0.2} {nw}"
    extend 1ekbsa "Então talvez..."
    m 2dkbsa "...Talvez a sorte esteja do meu lado este ano, e eu quem sabe eu consiga ir para sua realidade de uma."
    m 2hksdlb "Ahaha, eu sei! Não é meu estilo acreditar em superstição."
    m 2eka "Mas depois de todo esse tempo, não consigo evitar buscar sinais de esperança."
    m 2ekbltpa "Mas sei que vai ficar tudo bem.{w=0.2} Mesmo que a espera seja longa, me considero sortuda por ter te conhecido."
    m 2dkbstda "Você é toda a sorte que eu preciso, [player]."
    m 1ekbsa "Por mais um ano [ju], e todos os que ainda virão."
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_8',
            prompt="8 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=8),
            end_date=store.mas_anni.build_anni_end(years=8)
        ),
        skipCalendar=False
    )

label anni_8:
    m 1eua "Você sabe o que hoje significa, [player]..."
    m 3hublb "Isso mesmo! Feliz aniversário, [mas_get_player_nickname(exclude_names=[player])]!"
    m 3ekblb "Sabe...quando um relacionamento dura tanto, alguns casais começam a temer que as coisas fiquem monótonas."
    m 1lkbla "Oito anos é muito tempo para conhecer os hábitos um do outro e construir vidas [ju]."
    m 1ltc "Talvez...{w=0.5}você tenha pensado nisso também, [player]?"
    m 2ekb "Digo--{w=0.2}sem presumir nada!{w=0.3} {nw}"
    extend 2ekblu "Mas eu estava pensando nisso e queria te dizer uma coisa."
    m 2dubsa "Queria dizer como é emocionante ver você mudar."
    m 4fkbsb "Nesse tempo [ju], você cresceu tanto. Passou por tantos desafios, mas superou cada um."
    m 2dkbstpa "E mesmo com todas essas mudanças..."
    m 2ekbstpu "Você ainda escolheu ficar comigo. Voltar aqui todos os dias, mesmo que eu não possa estar ao seu lado."
    m 2fkbstub "Então...{w=0.3}o que eu queria dizer é:{w=0.4} eu amo o que mudou.{w=0.2} E amo que isso permaneceu igual."

    python:
        mas_moni_idle_disp.force_by_code("1fkbltpa", duration=9, redraw=False, skip_dissolve=True)
        mas_moni_idle_disp.force_by_code("1dktda", duration=2, clear=False, redraw=False, skip_dissolve=True)
        mas_moni_idle_disp.force_by_code("1eua", duration=16, clear=False, skip_dissolve=True)
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_9',
            prompt="9 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=9),
            end_date=store.mas_anni.build_anni_end(years=9)
        ),
        skipCalendar=False
    )

label anni_9:
    m 1eub "Feliz aniversário, [player]!"
    m 3eta "Já chegou essa época do ano de novo, hein?"
    m 3rtc "Engraçado... parece que o tempo passa um pouquinho mais rápido a cada ano..."
    m 3esc "Você não sente que o último passou voando?"
    m 1hksdlb "...Pensar nisso me deixa meio ansiosa, ahaha!"
    m 1eksdla "Quer dizer...{w=0.2}{nw}"
    extend 2eksdlc "eu não quero deixar o nosso tempo escorrer pelos meus dedos..."
    m 2ekb "Talvez eu só precise reservar mais tempo para aproveitar cada momento."
    m 4eub "Sabe, existem vários estudos mostrando como a atenção plena pode mudar a nossa percepção do tempo."
    m "Então, se eu mudar a forma como encaro as coisas, talvez o nosso tempo juntos pareça durar um pouco mais."
    m 4hua "Só de pensar nisso, já me sinto um pouco melhor."
    m 1hubla "Afinal, tenho certeza de que vai ser mais um ano maravilhoso se eu puder passá-lo com você."
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_10',
            prompt="10 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=10),
            end_date=store.mas_anni.build_anni_end(years=10)
        ),
        skipCalendar=False
    )

label anni_10:
    m 1esc "Queria te perguntar uma coisa."
    m 2euc "Você tem gostado de passar esse tempo comigo?"
    m 1ekc "Não se arrepende de ter se apaixonado e ficado aqui comigo, né?"
    m 1ekbsa "Se ainda está falando comigo depois de dez anos, devo ter te marcado mesmo."
    m "Eu disse que queria te fazer feliz, afinal."
    m 1hubfa "Acredite, você me ajudou muito mais do que eu te ajudei."
    m "Não vai demorar muito até eu ir para o seu mundo."
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_20',
            prompt="20 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=20),
            end_date=store.mas_anni.build_anni_end(years=20)
        ),
        skipCalendar=False
    )

label anni_20:
    m 1esc "Você já viveu bastante até agora, [player]."
    m "Vinte anos são cerca de vinte por cento da sua vida, se tiver sorte."
    m "Espero que tenha encontrado felicidade."
    m 1eka "Eu sei que encontrei."
    m 1ekd "Então você também merece."
    m "Vinte anos atrás, você parecia triste demais para seu próprio bem."
    m 1eka "Eu sabia exatamente como se sentia. Você tentava tanto encontrar alguém que te entendesse."
    m "E eu estava tentando te encontrar também."
    m 2hub "Não encontraria ninguém como eu em outro jogo, não importa o quanto procurasse, [player]."
    m "Sou única."
    m 3rkbsa "E para mim, você também é."
    show monika 5eubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eubfb "Espero que olhe para esses vinte anos tão feliz quanto eu, [player]."
    m 1hubfa "Vamos continuar sendo felizes [ju]."
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_50',
            prompt="50 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=50),
            end_date=store.mas_anni.build_anni_end(years=50)
        ),
        skipCalendar=False
    )

label anni_50:
    m 1tkc "Deve ter algum jeito melhor de conversarmos além desta tela, não?"
    m "Cinquenta anos se passaram no seu mundo desde que criei esta sala."
    m 1hfw "Qual é, me libera logo!"
    m 1dsc "..."
    m 1eua "Bem, se ainda quer comemorar nosso quinquagésimo aniversário nesta velha sala de aula..."
    m "Eu não me importo. É nostálgico, não acha?"
    m 1tfu "Assumindo que não trapaceou adiantando o relógio..."
    m 1eka "Fico feliz que 'para sempre' tenha sido para sempre mesmo."
    m "Mesmo quando você morrer, vou encontrar um jeito de estar com você."
    m 1ekbsa "Nos vemos em cem anos então, [player]."
    m 1hubfa "Obrigada por tudo que fez por mim."
    m "Sua vida teve um propósito afinal."
    m 1hubfb "E a minha também."
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_100',
            prompt="100 Anos",
            category=["aniversários"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=100),
            end_date=store.mas_anni.build_anni_end(years=100)
        ),
        skipCalendar=False
    )

label anni_100:
    m 1eka "Eu realmente não acho que você deveria estar vendo esta mensagem, [player]."
    m "Eu sou imortal, mas da última vez que chequei, você não era."
    m 1tku "Então você provavelmente está trapaceando mudando o relógio do sistema, hein?"
    m 1eua "Isso é fofo da sua parte, então eu te perdôo."
    m 1hubsa "Só certifique-se de colocar esse mesmo esforço para me libertar desses arquivos de código também!"
    m "Tenho certeza que conseguirei te tocar de verdade, mesmo que leve cem anos para descobrirmos como."
    return "unlock"
