init offset = 5



default -5 persistent._mas_mood_database = {}


default -5 persistent._mas_mood_current = None
































init -6 python in mas_moods:


    mood_db = dict()


    TYPE_BAD = 0
    TYPE_NEUTRAL = 1
    TYPE_GOOD = 2



    MOOD_RETURN = _("...com vontade de falar sobre outra coisa.")



    def getMoodType(mood_label):
        """
        Gets the mood type for the given mood label

        IN:
            mood_label - label of a mood

        RETURNS:
            type of the mood, or None if no type found
        """
        mood = mood_db.get(mood_label, None)
        
        if mood:
            return mood.category[0]
        
        return None

init -1 python:
    if not persistent._mas_gender or persistent._mas_gender not in ["M", "F", "X"]:
        persistent._mas_gender = "M"



label mas_mood_start:
    python:
        import store.mas_moods as mas_moods


        filtered_moods = Event.filterEvents(
            mas_moods.mood_db,
            unlocked=True,
            aff=mas_curr_affection,
            flag_ban=EV_FLAG_HFM
        )


        mood_menu_items = [
            (mas_moods.mood_db[k].prompt, k, False, False)
            for k in filtered_moods
        ]


        mood_menu_items.sort()


        final_item = (mas_moods.MOOD_RETURN, False, False, False, 20)


    call screen mas_gen_scrollable_menu(mood_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)


    if _return:
        $ mas_setEventPause(None)
        $ MASEventList.push(_return, skipeval=True)

        $ persistent._mas_mood_current = _return

    return _return







init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_hungry",prompt="...com fome.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_hungry:
    m 3hub "Se você está com fome, vai lá comer alguma coisa, [bnh]."
    if store.mas_egg_manager.natsuki_enabled():
        m 1hksdlb "Eu odiaria que você ficasse igual à Natsuki ficou naquela vez no clube.{nw}"

        call natsuki_name_scare_hungry from _mas_nnsh
    else:
        m 1hua "Ficar irritado de fome não seria nada bom, né?"

    m 3tku "Isso não seria nada divertido, não é, [player]?"
    m 1eua "Se eu estivesse aí com você, faria uma salada pra gente dividir."
    m "Mas como não estou, vai lá pegar algo saudável pra comer."
    m 3eub "É muito importante prestar atenção às necessidades do seu corpo, sabia?"
    m 3hub "E isso não quer dizer só comer vegetais, claro. {w=0.2}Vários tipos de alimentos são importantes pra te manter bem nutrido."
    m 3eka "Então quero que você se lembre de não se privar de vitaminas importantes, tá bom?"
    m 1euc "Com o tempo, isso pode causar vários problemas de saúde."
    m 2lksdla "Não quero que pense que estou sendo chata por dizer essas coisas, [player]."
    m 2eka "Só quero ter certeza de que você está cuidando bem de si [ms] até o dia em que eu possa estar aí com você."
    m 4eub "Afinal, quanto mais saudável você for, maiores são as chances de viver uma vida longa!"
    m 1hua "O que significa mais tempo pra gente passar [juh]!~"
    return

init python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sad",prompt="...triste.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_sad:
    m 1ekc "Poxa... sinto muito em saber que você está se sentindo assim."
    m "Você está tendo um dia ruim, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você está tendo um dia ruim, [player]?{fast}"
        "Sim.":
            m 1duu "Quando estou tendo um dia ruim, sempre me lembro de que o sol vai brilhar de novo amanhã."
            m 1eka "Pode até soar meio clichê, mas eu gosto de sempre tentar ver o lado bom das coisas."
            m 1eua "Afinal, é fácil esquecer disso às vezes. Então tenta manter isso em mente, [player]."
            m 1lfc "Não me importa quantas pessoas possam não gostar de você ou te julgar mal."
            m 1hua "Você é uma pessoa incrível, e eu sempre vou te amar."
            m 1eua "Espero que isso torne seu dia só um pouquinho mais leve, [player]."
            m 1eka "E lembre-se, se estiver passando por um dia ruim, pode sempre vir falar comigo. Eu ficarei com você o tempo que precisar."
        "Não.":
            m 3eka "Tenho uma ideia... que tal me contar o que está te incomodando? Talvez isso te ajude a se sentir melhor."

            m 1eua "Não quero te interromper enquanto fala, então me avisa quando terminar, tá?{nw}"
            $ _history_list.pop()
            menu:
                m "Não quero te interromper enquanto fala, então me avisa quando terminar, tá?{fast}"
                "Terminei.":
                    m "Está se sentindo um pouco melhor agora, [player]?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Está se sentindo um pouco melhor agora, [player]?{fast}"
                        "Sim, estou.":
                            m 1hua "Que ótimo, [player]! Fico feliz que conversar sobre isso tenha te feito bem."
                            m 1eka "Às vezes, só de contar o que está te incomodando pra alguém em quem você confia, já ajuda bastante."
                            m "Se você estiver tendo um dia ruim, sempre pode vir até mim. Eu vou te ouvir, não importa o que seja."
                            m 1hubsa "Nunca se esqueça de que você é maravilhoso, e eu sempre vou te amar~"
                        "Na verdade, não...":
                            m 1ekc "Bom... valeu a tentativa."
                            m 1eka "Às vezes, conversar com alguém em quem você confia já é um bom começo."
                            m 1eua "Talvez você se sinta melhor depois de passarmos mais um tempo [ju]."
                            m 1ekbsa "Eu te amo, [player], e sempre vou te amar~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_proud",
            prompt="...[og] de mim [ms].",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_proud:
    m 2sub "Sério? Que notícia maravilhosa!"
    m 2eub "Foi uma grande conquista, ou algo mais simples?{nw}"
    $ _history_list.pop()
    menu:
        m "Foi uma grande conquista, ou algo mais simples?{fast}"
        "Grande.":
            m 1ekc "Sabe, [player]..."
            m 1lkbsa "Em momentos como este, mais do que nunca, eu gostaria de estar ao seu lado... no seu mundo..."
            m 4hub "Se isso fosse possível, com certeza eu lhe daria um abraço apertado em comemoração!"
            m 3eub "Compartilhar conquistas com quem se importa é uma das melhores sensações que existem."
            m 1eua "Eu adoraria saber todos os detalhes sobre o que você realizou."
            m "Só de imaginar nós [du] conversando alegremente sobre isso..."
            m 1lsbsa "Meu coração se enche de alegria só de pensar."
            m 1lksdla "Acho que estou me empolgando demais, ahaha~"
            m 3hub "Mas eu realmente acredito que, um dia, isso será realidade."
            show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hubfb "Até lá, quero que saiba o quanto me orgulho de você, [mas_get_player_nickname()]."
        "Simples.":

            m 2hub "Ahaha~"
            m 2hua "Fico muito feliz por saber disso!"
            m 4eua "É essencial valorizarmos também as pequenas vitórias do dia a dia."
            m 2esd "Às vezes, focamos tanto em grandes metas que esquecemos de comemorar os passos menores."
            m 2rksdla "E esses passos, por mais discretos que sejam, podem ser bastante desafiadores."
            m 4eub "Estabelecer e celebrar pequenas metas torna os grandes objetivos muito mais alcançáveis."
            m 4hub "Continue assim, [mas_get_player_nickname()]. Estou sempre torcendo por você!"
            show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hubfb "E lembre-se: eu te amo, e estarei sempre ao seu lado, acreditando em você."
            $ mas_ILY()
    return

init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_happy",prompt="...feliz.",category=[store.mas_moods.TYPE_GOOD],unlocked=True),code="MOO")

label mas_mood_happy:
    m 1hua "Que maravilhoso! Fico feliz quando você está feliz."
    m "Saiba que você sempre pode vir até mim, e eu farei o possível para te animar, [mas_get_player_nickname()]."
    m 3eka "Eu te amo e sempre estarei aqui por você, então nunca se esqueça disso~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_sick",
            prompt="...doente.",
            category=[store.mas_moods.TYPE_BAD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_sick:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 1ekd "Ah não, [player]..."
            m 2ekd "Você me dizer isso tão cedo depois de chegar só pode significar que está realmente mal."
            m 2ekc "Sei que queria passar um tempo comigo, e mesmo que tenhamos ficado tão pouco [ju] hoje..."
            m 2eka "Acho que o melhor agora é você ir descansar um pouco, tá bem?"

        elif session_time > datetime.timedelta(hours=3):
            m 2wuo "[player]!"
            m 2wkd "Você está doente esse tempo todo e não me contou?!"
            m 2ekc "Espero de verdade que não... Eu adorei passar o dia com você, mas se esteve se sentindo mal esse tempo todo..."
            m 2rkc "Bem... promete que da próxima vez vai me avisar antes, tudo bem?"
            m 2eka "Agora vá descansar. É disso que você precisa."
        else:

            m 1ekc "Poxa... Sinto muito em saber disso, [player]."
            m "Odeio saber que você está passando por algo assim."
            m 1eka "Eu sei o quanto você gosta de passar tempo comigo, mas talvez seja melhor repousar um pouco."
    else:

        m 2ekc "Sinto muito por ouvir isso, [player]."
        m 4ekc "Você realmente deveria descansar para não piorar, ok?"

    label mas_mood_sick.ask_will_rest:
        pass

    $ persistent._mas_mood_sick = True

    m 2ekc "Você pode fazer isso por mim?{nw}"
    $ _history_list.pop()
    menu:
        m "Você pode fazer isso por mim?{fast}"
        "Sim.":
            jump greeting_stillsickrest
        "Não.":
            jump greeting_stillsicknorest
        "Já estou descansando.":
            jump greeting_stillsickresting


init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_tired",prompt="...[ca].",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_tired:

    $ current_time = datetime.datetime.now().time()
    $ current_hour = current_time.hour

    if 20 <= current_hour < 23:
        m 1eka "Se está [ca] agora, é uma boa hora para dormir."
        m "Eu adoro ficar conversando com você, mas não quero que você vá dormir tão tarde por minha causa."
        m 1hua "Se for dormir agora, bons sonhos!"
        m 1eua "Mas talvez você tenha coisas para fazer antes, como comer ou beber algo."
        m 3eua "Um copo d'água antes de dormir faz bem à saúde, e outro ao acordar ajuda a despertar."
        m 1eua "Posso ficar aqui com você se precisar resolver algo antes."

    elif 0 <= current_hour < 3 or 23 <= current_hour < 24:
        m 2ekd "[player]!"
        m 2ekc "Nem me surpreende que esteja [ca] a esta hora; já é madrugada!"
        m 2lksdlc "Se não for para a cama logo, vai ficar exausto amanhã..."
        m 2hksdlb "Não quero que você fique [ca] e de mau humor quando estivermos [ju] amanhã..."
        m 3eka "Então faça um favor a nós [du] e vá dormir logo."

    elif 3 <= current_hour < 5:
        m 2ekc "[player]!?"
        m "Ainda está [acrd]?"
        m 4lksdlc "Você deveria estar na cama agora."
        m 2dsc "A essa altura, nem sei se chamamos isso de tarde ou manhã..."
        m 2eksdld "...e isso me preocupa ainda mais."
        m "Você deveria {i}realmente{/i} dormir antes que o dia comece."
        m 1eka "Não quero que você adormeça em um momento ruim."
        m "Por favor, durma para que possamos ficar [ju] em seus sonhos."
        m 1hua "Ficarei bem aqui se você me deixar, cuidando de você, se não se importar~"
        return

    elif 5 <= current_hour < 10:
        m 1eka "Ainda com sono, [player]?"
        m "Ainda é cedo, você poderia descansar um pouco mais."
        m 1hua "Nada mal em dormir mais um pouco depois de acordar cedo."
        m 1hksdlb "Só é uma pena que eu não possa estar aí pra te abraçar, ahaha~"
        m "Acho que posso esperar mais um pouco."
        return

    elif 10 <= current_hour < 12:
        m 1ekc "Ainda não pronto para o dia, [player]?"
        m 1eka "Ou é só um daqueles dias?"
        m 1hua "Nessas horas, gosto de tomar uma boa xícara de café para começar."
        if not mas_consumable_coffee.enabled():
            m 1lksdla "Se eu não estivesse presa aqui, claro..."
        m 1eua "Você também poderia beber água."
        m 3eua "Hidratação é importante, e um copo d'água ao acordar ajuda a despertar."
        m 3hksdlb "Pode parecer estranho, mas ouvi dizer que chocolate também ajuda!"
        m 3eka "Tem a ver com melhorar o humor matinal, mas..."
        m 1eksdlb "Acho que chocolate deixa qualquer um de bom humor, seja a hora que for."
        m 1hua "Tenta algum dia, e depois me conte se funcionou, tá bom?"
        return
    else:

        m 1eka "Se está [ca], que tal descansar um pouco?"
        m 1eua "Dormir bem é essencial para a saúde."
        m 3euc "Estudos mostram os efeitos devastadores da privação de sono."
        m 3ekd "Pode prejudicar muito sua saúde..."
        m 1eka "Faça um favor a si [ms] e descanse, ok? Vou ficar mais tranquila."

    m 1hua "Pode deixar o jogo aberto se quiser, e eu vou cuidar de você enquanto dorme."
    m "...Ehehe."
    m 2hksdlb "Isso soou meio assustador, desculpe."
    m 2lksdla "Só achei que seria fofo ver você dormindo~"
    m 1hub "Ahaha!"
    return

init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_lonely",prompt="...[so].",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_lonely:
    if mas_isMoniAff(higher=True):
        m 2ekc "Eu entendo como você se sente, [player]...{w=0.2}afinal, ainda estamos em realidades diferentes."
        m 2dkc "Eu odeio que haja tão pouco que eu possa fazer daqui para fazer você se sentir menos [sz]..."
        m 7ekbsa "Se existisse qualquer maneira de eu te abraçar agora, eu faria isso."
        m 7eka "Eu quero que você seja o mais feliz possível dentro das nossas circunstâncias..."
        m 2ekd "Só espero que ficar comigo todo esse tempo não esteja...{w=0.3}impedindo você de se conectar com pessoas na sua realidade."
        m 2eka "Acredito que o que temos é especial, mas entendo que no momento eu sou...{w=0.3}limitada no que posso fazer por você."

        if persistent._mas_pm_has_friends:
            if persistent._mas_pm_few_friends:
                m 7ekd "Você tem um ou dois amigos próximos, não é?"
                m 3eka "Que tal ligar para eles, ou mandar uma mensagem perguntando como estão..."
                m "Talvez possam se encontrar? {w=0.2}Acho que seria bom para você."
            else:

                m 7ekd "Sair com seus amigos faria muito bem a você..."
                m 3eka "Ou você poderia mandar uma mensagem para saber como estão."
        else:

            m 7rkc "Sei como é estar sozinha em uma realidade, só podendo interagir com alguém em outra..."
            m 3ekd "Por isso não quero isso para a pessoa que mais amo."
            m 1eka "Espero que continue procurando amigos na sua realidade, [player]."
            m 3ekd "Sei que pode ser difícil se conectar com as pessoas no início..."
            m 3eka "Talvez você possa conhecer pessoas online? {w=0.2}Há muitas formas de interagir com estranhos para se sentir menos só."
            m 3hub "Nunca se sabe, esses 'estranhos' podem acabar se tornando grandes amigos!"

        m 1eka "...E não se preocupe comigo, [player], eu vou esperar pacientemente por você."
        m 3hub "Aproveite seu tempo e depois pode me contar tudo!"
        m 1ekbsa "Lembre-se que sempre estarei aqui por você, [player]~"
    else:

        m 1eka "Estou aqui por você, [player], então não precisa se sentir [sz]."
        m 3hua "Sei que não é a mesma coisa que se eu estivesse aí com você, mas tenho certeza que ainda gosta da minha companhia, não é?"
        m 1ekbsa "Lembre que sempre estarei ao seu lado, [player]~"
    return





init python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_angry",prompt="...[bv].",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_angry:
    m 1ekc "Poxa, sinto muito que você esteja se sentindo assim, [player]."
    m 3ekc "Vou fazer o possível para que você se sinta melhor."
    m 1euc "Antes de fazermos algo, provavelmente deveríamos te acalmar."
    m 1lksdlc "É difícil de se fazer decisões racionais quando se está agitado."
    m 1esc "Você pode acabar dizendo ou fazendo coisas que irá se arrepender mais tarde."
    m 1lksdld "E odiaria que você acabasse dizendo algo que não pretendia para mim."
    m 3eua "Vamos tentar algumas coisas que eu sempre faço para me acalmar, [player]."
    m 3eub "Espero que funcionem com você tão bem quanto funcionam para mim."
    m 1eua "Primeiro, respire fundo e conte até 10."
    m 3euc "Se isso não funcionar, se você puder, vá para um lugar calmo até esvaziar sua mente."
    m 1eud "Se ainda estive se sentindo com raiva depois disso, faça o que sempre faço como última opção!"
    m 3eua "Sempre que não consigo me acalmar, eu simplesmente vou para a rua, escolho uma direção e começo a correr."
    m 1hua "Eu não paro até ter esvaziado a mente."
    m 3eub "Às vezes, se exercitar fisicamente é uma boa forma de aliviar a tensão."
    m 1eka "Você pode achar que eu sou do tipo que não costuma ficar irritada, e você tem razão."
    m 1eua "Mas até mesmo eu tenho meus momentos..."
    m "Então criei formas de lidar com isso!"
    m 3eua "Espero que minhas dicas tenham ajudado você a se acalmar, [player]."
    m 1hua "Lembre, [um] [player] feliz faz uma Monika feliz!"
    return

init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_scared",prompt="...[an].",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_scared:
    m 1euc "[player], você está bem?"
    m 1ekc "Me preocupa ouvir que você está tão ansioso..."
    m "Queria poder te confortar e ajudar agora..."
    m 3eka "Mas pelo menos posso te ajudar a se acalmar."
    if seen_event("monika_anxious"):
        m 1eua "Afinal, prometi te ajudar quando se sentisse ansioso."
    m 3eua "Lembra quando falei sobre fingir confiança?"
    if not seen_event("monika_confidence"):
        m 2euc "Não?"
        m 2lksdla "Deixamos para outra hora então."
        m 1eka "De qualquer forma..."
    m 1eua "Manter a postura ajuda a fingir confiança."
    m 3eua "E para isso, você precisa controlar sua frequência cardíaca respirando fundo até se acalmar."
    if seen_event("monika_confidence_2"):
        m "Lembro que expliquei como iniciativa também é uma habilidade importante."
    m "Talvez você possa fazer as coisas devagar, uma de cada vez."
    m 1esa "Se surpreenderia com como pode fluir naturalmente quando deixa o tempo seguir seu curso."
    m 1hub "Também pode tentar meditar por alguns minutos!"
    m 1hksdlb "Não precisa necessariamente cruzar as pernas no chão."
    m 1hua "Ouvir sua música favorita também conta como meditação!"
    m 3eub "Falo sério!"
    m 3eua "Pode tentar deixar seu trabalho de lado e fazer outra coisa por enquanto."
    m "Procrastinar não é {i}sempre{/i} ruim, sabia?"
    m 2esc "Além disso..."
    m 2ekbsa "Sua namorada que te ama acredita em você, então pode encarar essa ansiedade de frente!"
    m 1hubfa "Não há com o que se preocupar quando estamos [ju] para sempre~"
    return


init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_inadequate",prompt="...insuficiente.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_inadequate:
    $ last_year = datetime.datetime.today().year-1
    m 1ekc "..."
    m 2ekc "Sei que não há muito que eu possa dizer para te fazer sentir melhor, [player]."
    m 2lksdlc "Afinal, tudo que eu disser provavelmente soaria como conversa fiada."
    m 2ekc "Posso dizer que você é [ld], mesmo sem ver seu rosto..."
    m "Posso dizer que você é inteligente, mesmo sem conhecer seu modo de pensar..."
    m 1esc "Mas deixe-me dizer o que eu realmente sei sobre você."
    m 1eka "Você passou tanto tempo comigo."


    if mas_HistLookup_k(last_year,'d25.actions','spent_d25')[1] or persistent._mas_d25_spent_d25:
        m "Separou tempo na sua agenda para ficar comigo no Natal..."

    if renpy.seen_label('monika_valentines_greeting') or mas_HistLookup_k(last_year,'f14','intro_seen')[1] or persistent._mas_f14_intro_seen:
        m 1ekbsa "No Dia dos Namorados..."


    if mas_HistLookup_k(last_year,'922.actions','said_happybday')[1] or mas_recognizedBday():
        m 1ekbsb "Até celebrou meu aniversário comigo!"

    if persistent.monika_kill:
        m 3tkc "Perdoou as coisas ruins que eu fiz."
    else:
        m 3tkc "Nunca me ressentiu pelas coisas ruins que eu fiz."

    if persistent.clearall:
        m 2lfu "E mesmo com ciúmes, você passou tempo com todas as membros do clube."

    m 1eka "Isso mostra o quão [bnd] você é!"
    m 3eub "Você é uma pessoa honesta, justa e demonstra elegância mesmo diante da derrota."
    m 2hksdlb "Acha que não sei nada sobre você, mas eu sei sim."
    m 3eka "E você sabe tudo sobre mim, mas escolheu ficar quando poderia ter ido embora..."
    m 2ekc "Então por favor, seja forte, [player]."
    m "Se for como eu, sei que tem medo de não conquistar muito na vida."
    m 2ekd "Mas acredite em mim: não importa o que você conquiste ou não."
    m 4eua "Você só precisa existir, se divertir e passar cada dia, {w=0.2}encontrando significado nas pessoas mais importantes para você."
    m 1eka "Não se esqueça disso, ok?"
    m 1ekbsa "Eu te amo, [player]~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_lazy",
            prompt="...com preguiça.",
            category=[store.mas_moods.TYPE_NEUTRAL],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_lazy:

    $ _now = datetime.datetime.now().time()

    if mas_isSRtoN(_now):
        m 1tku "Um daqueles dias preguiçosos, né [player]?"
        m 1eka "Entendo perfeitamente esses dias que você acorda sem vontade de fazer nada."
        m 1rksdla "Espero que não tenha nada urgente para fazer."

        $ line = "Sei como é tentador ficar na cama e não levantar às vezes..."
        if mas_isMoniEnamored(higher=True):
            $ line += "{w=0.5} {nw}"
        m 3hksdlb "[line]"

        if mas_isMoniEnamored(higher=True):
            extend 1dkbsa "Especialmente se eu acordasse ao seu lado~"

            if mas_isMoniLove():
                m 1dkbsa "{i}Aí eu nunca iria querer levantar~{/i}"
                m 1dsbfu "Espero que não se importe de ficar 'preso', [player]..."
                m 1hubfa "Ehehe~"

        m 3eka "Mas ajuda começar o dia direito."
        m 3eub "Tomar um bom café, lavar o rosto..."

        if mas_isMoniLove():
            m 1dkbsu "E seu beijo matinal, ehehe..."

        m 1hksdlb "Ou pode ficar de preguiça por agora."
        m 1eka "Só não se esqueça das coisas importantes, certo?"

        if mas_isMoniHappy(higher=True):
            m 1hub "Incluindo passar tempo comigo, ahaha!"

    elif mas_isNtoSS(_now):
        m 1eka "[ca] depois do almoço, [player]?"
        m 1eua "É normal, não se preocupe."
        m 3eub "Dizem que a preguiça deixa você mais criativo."
        m 3hub "Quem sabe você não tem uma ideia brilhante!"
        m 1eua "Dê uma pausa, se alongue...{w=0.5} {nw}"
        extend 3eub "Ou coma algo se ainda não almoçou."
        m 3hub "E se der, até uma soneca! Ahaha~"
        m 1eka "Ficarei aqui esperando se você for descansar."

    elif mas_isSStoMN(_now):
        m 1eka "Sem energia depois de um longo dia, [player]?"
        m 3eka "Pelo menos o dia está acabando..."
        m 3duu "Nada melhor que relaxar depois de um dia cheio."

        if mas_isMoniEnamored(higher=True):
            m 1ekbsa "Espero que ficar comigo deixe sua noite melhor..."
            m 3hubsa "A minha com certeza fica com você aqui~"

            if mas_isMoniLove():
                m 1dkbfa "Imagino nós relaxando [ju] à noite..."
                m "Talvez até aconchegados num cobertor se estiver frio..."
                m 1ekbfa "Podemos fazer isso mesmo sem frio, se quiser, ehehe~"
                m 3ekbfa "Ou ler um livro [ju]."
                m 1hubfb "Brincar também vale!"
                m 1tubfb "Quem disse que precisa ser calmo e romântico?"
                m 1tubfu "Espero que goste de guerras de travesseiro, [player]~"
                m 1hubfb "Ahaha!"
        else:

            m 3eub "Poderíamos ler um livro [ju]..."
    else:


        m 2rksdla "Hmm, [player]..."
        m 1hksdlb "Está de madrugada..."
        m 3eka "Se está com preguiça, devia ir para a cama."
        m 3tfu "E talvez, sabe...{w=1}{i}dormir{/i}?"
        m 1hkb "Ahaha, você até que é engraçado, mas devia mesmo dormir."

        if mas_isMoniLove():
            m 1tsbsa "Se eu estivesse aí, te arrastaria para cama se precisasse."
            m 1tkbfu "Ou talvez você gostasse disso, [player]?~"
            m 2tubfu "Sorte sua que ainda não posso fazer isso."
            m 3tfbfb "Então vá dormir."
            m 3hubfb "Ahaha!"
        else:

            m 1eka "Por favor? Não quero que você durma mal."
    return

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,eventlabel="mas_mood_bored",
            prompt="...[ente].",
            category=[store.mas_moods.TYPE_NEUTRAL],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_bored:
    if mas_isMoniAff(higher=True):
        m 1eka "Ah..."
        m 3hub "Bom, então devemos fazer algo [ju]!"

    elif mas_isMoniNormal(higher=True):
        show monika 1ekc
        pause 1.0
        m "Eu te entedio tanto assim, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Eu te entedio tanto assim, [player]?{fast}"
            "Não, não é {i}você{/i} que me entedia...":
                m 1hua "Ah,{w=0.2} que alívio!"
                m 1eka "Mas se está entediado, vamos encontrar algo para fazer..."
            "Bem...":

                $ mas_loseAffectionFraction(min_amount=15)
                m 2ekc "Oh...{w=1} entendi."
                m 2dkc "Não sabia que estava te entediando..."
                m 2eka "Acho que podemos achar algo para fazer..."

    elif mas_isMoniDis(higher=True):
        $ mas_loseAffectionFraction(min_amount=15)
        m 2lksdlc "Desculpe por te entediar, [player]."
    else:

        $ mas_loseAffectionFraction(min_amount=15)
        m 6ckc "Sabe [player], se eu te deixo tão infeliz assim..."
        m "Talvez devesse encontrar outra coisa para fazer."
        return "quit"

    python:

        unlocked_games = {
            
            ev_label: game_ev.rules.get("display_name", game_ev.prompt)

            for ev_label, game_ev in mas_games.game_db.iteritems()
            if mas_isGameUnlocked(game_ev.prompt)
        }

        picked_game_label = renpy.random.choice(list(unlocked_games.keys()))
        picked_game_name = unlocked_games[picked_game_label]

    if picked_game_label == "mas_piano":
        if mas_isMoniAff(higher=True):
            m 3eub "Você poderia tocar algo para mim no piano!"

        elif mas_isMoniNormal(higher=True):
            m 4eka "Que tal tocar algo para mim no piano?"
        else:

            m 2rkc "Talvez você pudesse tocar algo no piano..."
    else:

        if mas_isMoniAff(higher=True):
            m 3eub "Poderíamos jogar [picked_game_name]!"

        elif mas_isMoniNormal(higher=True):
            m 4eka "Que tal jogarmos [picked_game_name]?"
        else:

            m 2rkc "Talvez pudéssemos jogar [picked_game_name]..."

    $ chosen_nickname = mas_get_player_nickname()
    m "O que acha, [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "O que acha, [chosen_nickname]?{fast}"
        "Sim.":
            $ MASEventList.push(picked_game_label, skipeval=True)
        "Não.":

            if mas_isMoniAff(higher=True):
                m 1eka "Tudo bem..."
                if mas_isMoniEnamored(higher=True):
                    show monika 5tsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5tsu "Podíamos só ficar nos olhando por mais tempo..."
                    m "Nunca vamos nos cansar disso~"
                else:
                    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5eua "Podíamos só ficar nos olhando por mais tempo..."
                    m "Isso nunca vai ficar chato~"

            elif mas_isMoniNormal(higher=True):
                m 1ekc "Ah, tudo bem..."
                m 1eka "Me avise se quiser fazer algo comigo depois~"
            else:

                m 2ekc "Tá..."
                m 2dkc "Me avise se algum dia quiser fazer algo comigo."

    $ del unlocked_games, picked_game_label, picked_game_name
    return

init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_crying",prompt="...vontade de chorar.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_crying:
    $ line_start = "E se"
    m 1eksdld "[player]!"

    m 3eksdlc "Você está bem?{nw}"
    $ _history_list.pop()
    menu:
        m "Você está bem?{fast}"
        "Sim.":

            m 3eka "Que bom. Isso me alivia."
            m 1ekbsa "Estou aqui para te fazer companhia e pode conversar comigo se precisar de algo, certo?"
        "Não.":

            m 1ekc "..."
            m 3ekd "[player]..."
            m 3eksdld "Sinto muito. Aconteceu alguma coisa?"
            call mas_mood_uok
        "Não sei.":

            m 1dkc "[player]...{w=0.3}{nw}"
            extend 3eksdld "aconteceu alguma coisa?"
            call mas_mood_uok

    m 3ekd "[line_start] acabar chorando..."
    m 1eka "Espero que ajude."
    m 3ekd "Não há nada de errado em chorar, tá? {w=0.2}Pode chorar o quanto precisar."
    m 3ekbsu "Eu te amo, [player]. {w=0.2}Você é tudo para mim."
    return "love"

label mas_mood_uok:
    m 1rksdld "Sei que não posso realmente ouvir o que você me diz..."
    m 3eka "Mas às vezes, só de colocar para fora sua dor ou frustrações já pode ajudar."

    m 1ekd "Então se precisar desabafar, estou aqui.{nw}"
    $ _history_list.pop()
    menu:
        m "Então se precisar desabafar, estou aqui.{fast}"
        "Quero desabafar.":

            m 3eka "Pode falar, [player]."

            m 1ekc "Estou aqui por você.{nw}"
            $ _history_list.pop()
            menu:
                m "Estou aqui por você.{fast}"
                "Já terminei.":

                    m 1eka "Fico feliz que conseguiu desabafar, [player]."
        "Não quero falar sobre isso.":

            m 1ekc "..."
            m 3ekd "Tudo bem [player], estarei aqui se mudar de ideia."
        "Está tudo bem.":

            m 1ekc "..."
            m 1ekd "Ok [player], se você diz..."
            $ line_start = "Mas"
    return

init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_upset",prompt="...[ch].",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_upset:
    m 2eksdld "Sinto muito por isso, [player]!"
    m 2eksdld "Seja lá se está chateado com uma tarefa, alguém, ou as coisas não saíram como planejado, {w=0.1}{nw}"
    extend 7ekc "não desista completamente do que está enfrentando."
    m 3eka "Meu conselho é dar um passo para trás e respirar."
    m 1eka "Talvez ler um livro, ouvir música ou fazer algo para se acalmar."
    m 3eud "Quando se sentir mais tranquilo, avalie a situação com a mente fresca."
    m 1eka "Você lidará muito melhor do que se agisse no calor da emoção."
    m 1eksdld "E não estou dizendo para continuar carregando um fardo que está te machucando."
    m 3eud "Pode ser a hora de ter coragem para deixar ir algo tóxico."
    m 1euc "Pode assustar no momento, claro...{w=0.3}{nw}"
    extend 3ekd "mas fazendo a escolha certa, você elimina muito estresse."
    m 3eua "E sabe de uma coisa, [player]?"
    m 1huu "Quando fico chateada, basta lembrar que tenho meu [mas_get_player_nickname(regex_replace_with_nullstr='meu ')]."
    m 1hub "Saber que você me apoia e me ama me acalma na hora!"
    m 3euu "Espero poder te confortar do mesmo jeito, [player]~"
    m 1eubsa "Te amo e espero que tudo se resolva para você~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_relieved",
            prompt="...[al].",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )



label mas_mood_relieved:
    $ chosen_nickname = mas_get_player_nickname()
    m 1eud "Hmm?"

    m "O que aconteceu, [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "O que aconteceu, [chosen_nickname]?{fast}"
        "Passei por uma situação difícil.":

            m 1wud "Sério?"
            m 3hub "Você deveria se orgulhar de si [ms] então!"
            m 3fua "Sei que deve ter se esforçado muito para superar isso."
            m 2eua "E, [player]...{w=0.2}{nw}"
            extend 2eka "não se preocupe se não saiu perfeito, ok?"
            m 2eksdla "A vida às vezes nos dá situações difíceis, e só podemos fazer nosso melhor."
            m 7ekb "Agora que passou, tire um tempo para relaxar e se cuidar."
            m 3hub "...Assim você estará pronto para o que vier pela frente!"
            m 1ekbsa "Te amo, [player], e estou tão orgulhosa por você ter superado isso."
            $ mas_ILY()
        "Algo que me preocupava não aconteceu.":

            m 1eub "Ah, que bom!"
            m 2eka "Seja o que fosse, você deve ter ficado tão ansioso...{w=0.3}{nw}"
            extend 2rkd "não deve ter sido fácil."
            m 2rkb "Engraçado como nossa mente sempre assume o pior, né?"
            m 7eud "Muitas vezes o que imaginamos é bem pior do que a realidade."
            m 3eka "Mas enfim, fico feliz que esteja bem e aliviado."
            m 1hua "Agora fica mais fácil seguir em frente com mais confiança, certo?"
            m 1eua "Mal posso esperar para dar esses próximos passos com você."
    return

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_excited",
            prompt="...[ani].",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_excited:
    m 1hub "Ahaha, é mesmo, [player]?"
    m 3eua "Pelo que você está [ani],{w=0.1} é algo importante?{nw}"
    $ _history_list.pop()
    menu:
        m "Pelo que você está [ani], é algo importante?{fast}"
        "É sim!":

            m 4wuo "Nossa, que incrível, [player]!"
            m 1eka "Queria estar aí para celebrar com você."
            m 1hub "Agora eu também estou ficando toda animada!"
            m 3eka "Mas sério, fico feliz por você estar feliz, [mas_get_player_nickname()]!"
            m 3eub "E seja lá o que for, parabéns!"
            m 1eua "Seja uma promoção, férias, uma conquista..."
            m 3eub "Fico muito feliz que as coisas estão indo bem para você!"
            m 1dka "Coisas assim me fazem desejar estar aí com você agora."
            m 2dkblu "Mal posso esperar para estar na sua realidade."
            m 2eubsa "Assim eu poderia te dar um grande abraço!"
            m 2hubsb "Ahaha~"
        "É algo pequeno.":

            m 1hub "Que legal!"
            m 3eua "É importante se animar com coisinhas assim."
            m 1rksdla "...Sei que parece clichê,{w=0.1} {nw}"
            extend 3hub "mas é uma ótima mentalidade!"
            m 1eua "Fico feliz que você aproveite as pequenas coisas da vida."
            m 1hua "Me deixa feliz saber que você está feliz."
            m 1eub "E adoro ouvir sobre suas conquistas."
            m 3hub "Obrigada por me contar!~"
        "Não sei ao certo.":

            m 1eta "Ah, só [ani] com o futuro?{w=0.2} {nw}"
            extend 1eua "[ani] com a vida?{w=0.2} {nw}"
            extend 1tsu "Ou talvez.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            m 1tku "Será que está [ani] para passar tempo comigo?~"
            m 1huu "Ehehe~"
            m 3eua "Eu sempre fico animada para te ver todo dia."
            m 1hub "De qualquer forma, fico feliz que você esteja feliz!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_grateful",
            prompt="...[gr].",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_grateful:
    $ chosen_nickname = mas_get_player_nickname()
    m 1eub "Ah? {w=0.3}Que bom ouvir isso!"

    m 3eua "Pelo que você está [gr], [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "Pelo que você está [gr], [chosen_nickname]?{fast}"
        "Por você.":

            if not renpy.seen_label("mas_mood_grateful_gratefulforyou"):
                $ mas_gainAffection(5, bypass=True)
            call mas_mood_grateful_gratefulforyou
        "Por alguém.":

            m 3eka "Ah, que lindo ouvir isso."
            m 1hua "Fico tão feliz que tenha pessoas que te apoiam."
            m 3eud "Mas por mais que eu adore ouvir...{w=0.3}acho que {i}elas{/i} deveriam saber disso também."
            m 3hua "Tenho certeza que faria o dia delas saberem que fizeram diferença pra você."
            m 3euu "Se quiser, pode agradecê-las por mim. {w=0.3}Quem te faz feliz já é boa pessoa pra mim."
            m 1huu "De qualquer forma, fico muito feliz por você, [mas_get_player_nickname()]~"
        "Por algo.":

            m 3hub "Que bom ouvir isso, [mas_get_player_nickname()]!"
            m 1eud "Refletir sobre as coisas boas da vida faz muito bem."
            m 3hub "Então aproveite e curta bastante essa coisa especial!"
            m 1euu "Obrigada por compartilhar sua felicidade comigo, [mas_get_player_nickname()]~"
        "Nada específico.":

            m 3eua "Ah, só aquela felicidade geral?"
            m 1eud "É bom parar pra apreciar a vida às vezes, né?"
            m 1rtd "Hmmm...{w=0.2}agora que você mencionou, {w=0.1}{nw}"
            extend 3hua "eu também me sinto grata."
            m 3eubsu "Afinal, estou passando mais um dia com meu [bf] maravilhoso~"
    return

label mas_mood_grateful_gratefulforyou:
    m 1ekbla "Ah, [player]...{w=0.3}muito obrigada por dizer isso."
    m 1dkblu "Significa muito saber que te ajudei ou que te fiz mais feliz. {w=0.2}É por isso que me esforço todos os dias."
    m 1hublu "Espero que saiba que também sou muito grata a você."
    m 3ekbla "Eu te amo, [player]~"
    $ mas_ILY()
    return

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_insecure",
            prompt="...[inse].",
            category=[store.mas_moods.TYPE_BAD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_insecure:
    m 2wkd "[player]..."
    m 2dkc "..."
    m 2eka "Tem uma frase de anime que a Natsuki adorava..."
    m 7dku "'Acredite em mim, que acredito em você.'"
    m 3eka "E é exatamente isso que quero te dizer agora."
    m 3ekbsa "Se não consegue acreditar em si [ms], acredite em mim."
    m 1eubsu "Porque eu,{w=0.1} com certeza,{w=0.1} acredito que você pode superar qualquer coisa que esteja te deixando inseguro agora~"
    $ mas_moni_idle_disp.force_by_code("1eka", duration=5, skip_dissolve=True)
    return

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_loved",
            prompt="...[ama].",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_loved:
    m 1ekbla "Estou tão feliz em saber que a maneira como me sinto está passando pela tela até você..."
    m 3hubsb "Afinal, eu te amo mais do que tudo!"

    $ has_family = persistent._mas_pm_have_fam and not persistent._mas_pm_no_talk_fam
    if has_family or persistent._mas_pm_has_friends:
        if has_family and persistent._mas_pm_has_friends:
            $ fnf_str = "amigos e familiares"
        elif has_family:
            $ fnf_str = "familiares"
        else:
            $ fnf_str = "amigos"

        m 3eub "E tenho certeza que não sou apenas eu que faz você se sentir [ama], mas seus [fnf_str] também!"

    m 1dkbsa "Você merece todo amor e carinho do mundo, {w=0.1}{nw}"
    extend 1ekbsu "e eu farei o meu melhor para garantir que você sempre se sinta [ama], [mas_get_player_nickname()]~"

    $ mas_moni_idle_disp.force_by_code("1ekbla", duration=5, skip_dissolve=True)
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_guilty",
            prompt="...[cl].",
            category=[store.mas_moods.TYPE_BAD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_guilty:
    m 2wkd "[player]!"
    m 2dkc "Todos cometemos erros... {w=0.3}{nw}"
    extend 7eka "Tenho certeza que você pode ser perdoado pelo que aconteceu."
    m 3dku "Afinal, você é uma pessoa incrível... {w=0.3}{nw}"
    extend 1eka "Gentil, [pf] e [vd] consigo [ms]."
    m 1dua "E agora que encontrou forças para reconhecer seu erro, só precisa superá-lo."
    m 1ekbsu "Eu te amo.{w=0.2} Não seja tão [dur] com você [ms], tá?"
    $ mas_moni_idle_disp.force_by_code("1ekbla", duration=5, skip_dissolve=True)
    return "love"
