init offset = 5











default -5 persistent._mas_story_database = dict()


default -5 mas_full_scares = False


default -5 persistent._mas_last_seen_new_story = {"normal": None, "scary": None}


define -5 mas_scary_story_setup_done = False


init -6 python in mas_stories:
    import store
    import datetime

    UNLOCK_NEW = "unlock_new"


    TYPE_NORMAL = "normal"
    TYPE_SCARY = "assustadora"


    STORY_RETURN = "Esqueça"
    story_database = dict()


    TIME_BETWEEN_UNLOCKS = renpy.random.randint(20, 28)






    FIRST_STORY_EVL_MAP = {
        TYPE_SCARY: "mas_scary_story_hunter",
        TYPE_NORMAL: "mas_story_tyrant"
    }


    NEW_STORY_CONDITIONAL_OVERRIDE = {
        TYPE_SCARY: (
            "mas_stories.check_can_unlock_new_story(mas_stories.TYPE_SCARY, ignore_cooldown=store.mas_isO31())"
        ),
    }

    def check_can_unlock_new_story(story_type=TYPE_NORMAL, ignore_cooldown=False):
        """
        Checks if it has been at least one day since we've seen the last story or the initial story

        IN:
            story_type - story type to check if we can unlock a new one
                (Default: TYPE_NORMAL)
            ignore_cooldown - Whether or not we ignore the cooldown or time between new stories
                (Default: False)
        """
        global TIME_BETWEEN_UNLOCKS
        
        new_story_ls = store.persistent._mas_last_seen_new_story.get(story_type, None)
        
        
        first_story = FIRST_STORY_EVL_MAP.get(story_type, None)
        
        
        if not first_story:
            return False
        
        can_show_new_story = (
            store.seen_event(first_story)
            and (
                ignore_cooldown
                or store.mas_timePastSince(new_story_ls, datetime.timedelta(hours=TIME_BETWEEN_UNLOCKS))
            )
            and len(get_new_stories_for_type(story_type)) > 0
        )
        
        
        if can_show_new_story:
            TIME_BETWEEN_UNLOCKS = renpy.random.randint(20, 28)
        
        return can_show_new_story

    def get_new_stories_for_type(story_type):
        """
        Gets all new (unseen) stories of the given ype

        IN:
            story_type - story type to get

        OUT:
            list of locked stories for the given story type
        """
        return store.Event.filterEvents(
            story_database,
            pool=False,
            aff=store.mas_curr_affection,
            unlocked=False,
            flag_ban=store.EV_FLAG_HFNAS,
            category=(True, [story_type])
        )

    def get_and_unlock_random_story(story_type=TYPE_NORMAL):
        """
        Unlocks and returns a random story of the provided type

        IN:
            story_type - Type of story to unlock.
                (Default: TYPE_NORMAL)
        """
        
        stories = get_new_stories_for_type(story_type)
        
        
        story = renpy.random.choice(stories.values())
        
        
        story.unlocked = True
        
        return story.eventlabel

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_short_stories",
            category=['literatura'],
            prompt="Você pode me contar uma história?",
            pool=True,
            unlocked=True
        )
    )

label monika_short_stories:
    call monika_short_stories_premenu (None)
    return _return

label monika_short_stories_premenu(story_type=None):
    python:

        if story_type is None:
            story_type = mas_stories.TYPE_NORMAL
        end = ""

label monika_short_stories_menu:

    python:

        can_unlock_story = False

        if story_type in mas_stories.NEW_STORY_CONDITIONAL_OVERRIDE:
            try:
                can_unlock_story = eval(mas_stories.NEW_STORY_CONDITIONAL_OVERRIDE[story_type])
            except Exception as ex:
                store.mas_utils.mas_log.error("Falha ao avaliar condicional para desbloquear nova história porque '{0}'".format(ex))
                
                can_unlock_story = False

        else:
            can_unlock_story = mas_stories.check_can_unlock_new_story(story_type)


        stories_menu_items = [
            (story_ev.prompt, story_evl, False, False)
            for story_evl, story_ev in mas_stories.story_database.iteritems()
            if Event._filterEvent(
                story_ev,
                pool=False,
                aff=mas_curr_affection,
                unlocked=True,
                flag_ban=EV_FLAG_HFM,
                category=(True, [story_type])
            )
        ]


        stories_menu_items.sort()


        stories_menu_items.insert(0, ("Uma nova historia", mas_stories.UNLOCK_NEW, True, False))



        if story_type == mas_stories.TYPE_SCARY:
            switch_str = "curta"
        else:
            switch_str = "assustadora"

        switch_item = ("Eu gostaria de ouvir uma história " + switch_str + "", "monika_short_stories_menu", False, False, 20)

        final_item = (mas_stories.STORY_RETURN, False, False, False, 0)


    show monika 1eua at t21

    if story_type == mas_stories.TYPE_SCARY:
        $ which = "Qual"
    else:
        $ which = "Qual"

    $ renpy.say(m, which + " história você gostaria de ouvir?" + end, interact=False)


    call screen mas_gen_scrollable_menu(stories_menu_items, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, switch_item, final_item)


    if _return:

        if _return == "monika_short_stories_menu":

            if story_type == mas_stories.TYPE_SCARY:
                $ story_type = mas_stories.TYPE_NORMAL
            else:
                $ story_type = mas_stories.TYPE_SCARY

            $ end = "{fast}"
            $ _history_list.pop()

            jump monika_short_stories_menu
        else:

            $ story_to_push = _return


            if story_to_push == mas_stories.UNLOCK_NEW:
                if not can_unlock_story:
                    show monika at t11
                    $ _story_type = story_type if story_type != 'normal' else 'curta'
                    m 1ekc "Desculpe, [player]...Eu realmente não consigo pensar em uma nova história [_story_type] agora..."
                    m 1eka "Se você me der algum tempo, posso ser capaz de pensar em um em breve...mas enquanto isso, posso sempre lhe contar uma antiga de novo~"
                    show monika 1eua
                    jump monika_short_stories_menu
                else:

                    python:
                        persistent._mas_last_seen_new_story[story_type] = datetime.datetime.now()
                        story_to_push = mas_stories.get_and_unlock_random_story(story_type)


            $ pushEvent(story_to_push, skipeval=True)

            show monika at t11
    else:

        return "prompt"

    return


label mas_story_begin:
    python:
        story_begin_quips = [
            _("Certo, vamos começar a história."),
            _("Pronto para ouvir a história?"),
            _("Pronto para a hora da história?"),
            _("Vamos começar~"),
            _("Está pronto?")
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)
    $ mas_gainAffection(modifier=0.2)
    m 3eua "[story_begin_quip]"
    m 1duu "Ahem."
    return


label mas_scary_story_setup:
    if mas_scary_story_setup_done:
        return

    $ mas_scary_story_setup_done = True
    show monika 1dsc
    $ mas_temp_r_flag = mas_current_weather
    $ is_scene_changing = mas_current_background.isChangingRoom(mas_current_weather, mas_weather_rain)
    $ are_masks_changing = mas_current_weather != mas_weather_rain
    $ mas_is_raining = True

    $ play_song(None, fadeout=1.0)
    pause 1.0

    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)


    if not persistent._mas_o31_in_o31_mode:
        $ mas_changeWeather(mas_weather_rain)
        $ store.mas_globals.show_vignette = True
        call spaceroom (dissolve_all=is_scene_changing, dissolve_masks=are_masks_changing, force_exp='monika 1dsc_static')

    play music "mod_assets/bgm/happy_story_telling.ogg" loop


    $ HKBHideButtons()
    $ mas_RaiseShield_core()

    python:
        story_begin_quips = [
            _("Tudo bem, vamos começar a história."),
            _("Pronto para ouvir a história?"),
            _("Pronto para a hora da história?"),
            _("Vamos começar."),
            _("Você está pronto?")
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)

    m 3eua "[story_begin_quip]"
    m 1duu "Ahem."
    return

label mas_scary_story_cleanup:

    python:
        story_end_quips = [
            _("Com medo, [player]?"),
            _("Eu te assustei, [player]?"),
            _("Como foi?"),
            _("Bem?"),
            _("Então...{w=0.5}eu te assustei?")
        ]
        story_end_quip=renpy.substitute(renpy.random.choice(story_end_quips))

    m 3eua "[story_end_quip]"
    show monika 1dsc
    pause 1.0


    if not persistent._mas_o31_in_o31_mode:
        $ mas_changeWeather(mas_temp_r_flag)
        $ store.mas_globals.show_vignette = False
        call spaceroom (dissolve_all=is_scene_changing, dissolve_masks=are_masks_changing, force_exp='monika 1dsc_static')
        hide vignette

    call monika_zoom_transition (mas_temp_zoom_level, transition=1.0)

    $ play_song(None, 1.0)
    m 1eua "Eu espero que tenha gostado, [player]~"
    $ mas_DropShield_core()
    $ HKBShowButtons()
    $ mas_scary_story_setup_done = False
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_tyrant",
            prompt="O Gato e o Galo",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=True
        ),
        code="STY"
    )

label mas_story_tyrant:
    call mas_story_begin
    m 1eua "Um gato pegou um Galo e pensou em uma desculpa válida para o devorar."
    m "Ele o acusou de ser um incômodo, por cantar de noite, não deixando os homens dormirem."
    m 3eud "O Galo defendeu suas ações dizendo que isso era para o bem dos homens, já que os acordava para o trabalho."
    m 1tfb "O Gato respondeu, 'você possui várias desculpas, mas é hora do lanche.'"
    m 1hksdrb "O Gato então comeu o Galo."
    m 3eua "A moral dessa história é: 'Tiranos não precisam de motivos.'"
    m 1hua "Espero que tenha gostado dessa historinha, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_despise",
            prompt="A Raposa",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_despise:
    call mas_story_begin
    m 1eud "Em um dia quente de verão, uma raposa estava passeando por um pomar, até que encontrou um cacho de uvas pendurado em um ramo."
    m 1tfu "'Justo o que eu precisava para saciar minha sede,' disse a raposa."
    m 1eua "Recuando alguns passos, ela começou a correr e saltou, mas errou o cacho por pouco."
    m 3eub "Se virando novamente, ela saltou em um,{w=1.0} dois,{w=1.0} três,{w=1.0} mas ainda não teve sucesso."
    m 3tkc "De novo e de novo ela tentou pegar as frutas, mas acabou tendo que desistir e foi embora com o nariz empinado, dizendo: 'Tenho certeza que estavam azedas.'"
    m 1hksdrb "A moral dessa história é que: 'É mais fácil menosprezar aquilo que você não pode ter.'"
    m 1eua "Espero que tenha gostado, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_lies",
            prompt="O menino pastor e o lobo",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_lies:
    call mas_story_begin
    m 1euc "Havia um pastor que cuidava de suas ovelhas na base de uma montanha, próximo de uma floresta escura."
    m 1lsc "Era solitário para ele, então ele elaborou um plano para conseguir um pouco de companhia."
    m 4hfw "Ele correu até o vilarejo gritando 'Lobo! lobo!' e os aldeões foram ao encontro dele."
    m 1hksdrb "Isso alegrou tanto o garoto que alguns dias depois ele tentou o mesmo truque e novamente os aldeões vieram o ajudar."
    m 3wud "Pouco tempo depois, um lobo realmente saiu da floresta."
    m 1ekc "O garoto gritou 'Lobo, lobo!' mais alto do que antes."
    m 4efd "Mas dessa vez, os aldeões, que haviam sido enganados duas vezes antes, acharam que o garoto estava mentindo de novo, e ninguém veio o ajudar."
    m 2dsc "Então o lobo fez uma excelente refeição com o rebanho do garoto."
    m 2esc "A moral dessa história é: 'Ninguém acredita em mentirosos, mesmo quando eles falam a verdade.'"
    m 1hksdlb "Você não precisa se preocupar com isso, [player]..."
    m 3hua "Você nunca mentiria para mim, certo?"
    m 1hub "Ehehe~"
    m 1eua "Espero que tenha gostado da história, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_grasshoper",
            category=[mas_stories.TYPE_NORMAL],
            prompt="O Gafanhoto",
            unlocked=False
        ),
        code="STY"
    )

label mas_story_grasshoper:
    call mas_story_begin
    m 1eua "Um dia de verão, um gafanhoto estava saltando e cantarolando."
    m "Uma formiga passou por ele, carregando uma espiga de milho para o formigueiro."
    m 3eud "'Por que não vem conversar comigo,' disse o gafanhoto, 'em vez de ficar trabalhando assim?'"
    m 1efc "'Estou ajudando a estocar comida para o inverno,' disse a Formiga, 'e recomendo você fazer o mesmo.'"
    m 1hfb "'Por que se preocupar com o inverno?' disse o gafanhoto; 'temos muita comida agora!'"
    m 3eua "A Formiga continuou seu caminho."
    m 1dsc "Quando o inverno chegou, o gafanhoto não tinha comida e acabou morrendo de fome, enquanto via as formigas distribuindo os milhos e grãos que haviam coletado no verão."
    m 3hua "A moral dessa história é: que: 'Há tempo para trabalhar e hora para se divertir'."
    m 1dubsu "Mas é sempre hora de passar um tempo com sua namorada fofa~"
    m 1hub "Ehehe, eu te amo tanto, [player]!"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_wind_sun",
            prompt="O Vento e o Sol",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_wind_sun:
    call mas_story_begin
    m 1dsc "O vento e o Sol estavam disputando para ver quem era o mais forte."
    m 1euc "De repente, eles viram um viajante vindo pela estrada e o Sol disse: 'Sei um jeito de decidir nossa disputa.'"
    m 3efd "'Quem de nós conseguir fazer o viajante tirar seu casaco será considerado o mais forte. Você começa.'"
    m 3euc "Então o Sol foi para trás de uma nuvem e o vento começou a soprar o mais forte que podia sobre o viajante."
    m 1ekc "Mas quanto mais forte soprava, mais o viajante apertava seu casaco, até que o vento teve que desistir em desespero."
    m 1euc "Então o Sol saiu e brilhou com toda sua glória sobre o viajante, o qual acabou ficando com muito calor para caminhar com seu casaco."
    m 3hua "A moral da história é que: 'A gentileza e a bondade vencem, onde a força e a arrogância fracassam.'"
    m 1hub "Espero que tenha se divertido, [player]."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_seeds",
            prompt="As Sementes",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_seeds:
    call mas_story_begin
    m 1euc "Um Camponês estava plantando algumas sementes de cânhamo em um campo onde uma Andorinha e alguns outros pássaros estavam mergulhando para pegar comida."
    m 1tfd "'Cuidado com aquele homem,' disse a Andorinha."
    m 3eud "'Por que, o que ele está fazendo?' perguntaram os outros."
    m 1tkd "'Aquilo é semente de cânhamo que ele está plantando. Tenham cuidado para pegar cada uma das sementes ou irá se arrepender.' A Andorinha respondeu."
    m 3rksdld "Os pássaros não deram importância para o que a Andorinha havia dito e pouco a pouco o cânhamo foi crescendo e foi transformado em corda, e as cordas em uma rede."
    m 1euc "Muitos pássaros que menosprezaram o conselho da Andorinha foram pegos em redes feitas do próprio cânhamo."
    m 3hfu "'O que eu falei para vocês?' disse a Andorinha."
    m 3hua "A moral dessa história é: 'Destrua as sementes do mal antes que elas cresçam para serem sua ruína.'"
    m 1lksdlc "..."
    m 2dsc "Gostaria de ter seguido essa moral."
    m 2lksdlc "Você não teria que ter visto tudo aquilo."
    m 4hksdlb "Enfim, espero que você tenha gostado da história, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_gray_hair",
            prompt="O Cabelo Branco",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_gray_hair:
    call mas_story_begin
    m 1eua "Antigamente, um homem de meia-idade tinha uma esposa que era velha e uma que era jovem. Cada uma delas o amava e queriam conquistar a afeição dele."
    m 1euc "O cabelo do homem estava ficando branco, o que a Esposa jovem não gostou, já que fazia ele parecer muito velho."
    m 3rksdla "Então, toda noite, ela arrancava os cabelos brancos."
    m 3euc "Mas a Esposa mais velha não gostava de ser confundida como a mãe dele."
    m 1eud "Então, toda manhã, ela arrancava o máximo de cabelos pretos que conseguia."
    m 3hksdlb "O homem logo acabou ficando careca."
    m 1hua "A moral dessa história é que: 'Ceda a todos e logo você não terá nada para ceder.'"
    m 1hub "Então, antes de você dar tudo, tenha certeza que ainda tenha um pouco para você!"
    m 1lksdla "...Não que ser careca seja ruim, [player]."
    m 1hksdlb "Ehehe, eu te amo!~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_fisherman",
            prompt="O pescador",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_fisherman:
    call mas_story_begin
    m 1euc "Um pescador pobre, que vivia com os peixes que pegava, teve azar um dia e pegou apenas um peixinho."
    m 1eud "O pescador estava prestes a colocá-lo em seu balde, quando o peixinho falou."
    m 3ekd "'Por favor, me poupe, Sr. pescador! Sou tão pequeno que não vale a pena me levar para casa. Quando eu estiver maior, serei uma refeição bem melhor!'"
    m 1eud "Mas o pescador rapidamente colocou o peixe no balde."
    m 3tfu "'Que tolo eu seria,' ele disse, 'se o jogasse de volta ao mar. Por menor que você seja, é melhor que nada.'"
    m 3esa "A moral dessa história é que: 'Um pequeno ganho vale mais do que uma grande promessa.'"
    m 1hub "Espero que você tenha gostado dessa história, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_ravel",
            prompt="Os Três Desejos do Velho",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_ravel:
    call mas_story_begin
    m 3euc "Uma vez, um velho estava sentado sozinho em um caminho escuro."
    m 1euc "Ele havia se esquecido para onde estava viajando e quem ele era."
    m "De repente, ele ergueu a cabeça e viu uma mulher idosa à sua frente."
    m 1tfu "Ela de um sorriso sem dentes e com um cacarejo, falou: 'Agora, seu {i}terceiro{/i} desejo. Qual será?'"
    m 3eud "'Terceiro desejo?' O homem estava confuso. 'Como pode ser um terceiro desejo se não tive um primeiro e segundo desejo?'"
    m 1tfd "'Você já teve dois desejos,' a velha disse, 'mas seu segundo desejo foi para que eu retornasse tudo ao jeito que era antes de você ter feito seu primeiro desejo.'"
    m 3tku "'É por isso que você não se lembra de nada: porque tudo está como era antes de você ter feito qualquer desejo.'"
    m 1dsd "'Tudo bem,' disse o homem, 'eu não acredito nisso, mas não fará mal algum fazer um desejo. Eu desejo saber quem eu sou.'"
    m 1tfb "'Engraçado,' disse a velha enquanto realizava o desejo dele e desaparecia para sempre. 'Esse foi o seu primeiro desejo.'"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_genie_simple",
            prompt="O Gênio Simples",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_genie_simple:
    call mas_story_begin
    m 1eua "Era uma vez um gênio que viajou por mundos diferentes para escapar do caos de seu próprio mundo."
    m 3euc "Durante suas viagens, ele conheceu uma mulher que desafiava a forma como ele via o mundo."
    m 3eua "Ela era inteligente e talentosa, mas prejudicada pelas dificuldades que enfrentava e pelo pouco que tinha."
    m 3eub "O gênio viu isso e se sentiu generoso, oferecendo ferramentas para acelerar o trabalho dela e facilitar sua vida."
    m 1euc "Mas ela recusou essa oferta."
    m 1eud "Ninguém jamais havia recusado um desejo do gênio antes, {w=0.1}{nw}"
    extend 1etc "o que o deixou confuso."
    m 1esa "A mulher simplesmente perguntou se ele era feliz...{w=0.5} {nw}"
    extend 1rsc "Ele não sabia como responder."
    m 3eud "A mulher disse que percebia que ele nunca havia experimentado felicidade, e que apesar de todas as suas dificuldades, ela ainda podia aproveitar a vida."
    m 1euc "O gênio não conseguia entender por que alguém iria querer trabalhar tanto por tão pouco."
    m 3euc "Ele melhorou suas ofertas com riquezas e outras coisas, mas ainda assim, elarecusou."
    m 1eua "Eventualmente, a mulher pediu ao gênio para adotar o estilo de vida dela."
    m "E assim, ele imitou as coisas que ela fazia, sem usar seus poderes."
    m 1hua "O gênio começou a sentir uma pequena sensação de realização, criando algo pela primeira vez sem simplesmente desejar que existisse."
    m 3eub "Ele viu como as coisas simples, como arte e escrita, inspiravam a mulher e realmente a faziam brilhar."
    m 1eua "Intrigado, ele desejava passar muito mais tempo com essa mulher e aprender com ela."
    m 1euc "No entanto, um dia a mulher ficou doente."
    m 1eud "Ela fez o gênio prometer não usar seus poderes para curar ela."
    m 3eud "Foi neste momento que o gênio soube que queria viver como um humano, sem nunca mais usar seus poderes."
    m 1dsc "Ele pensou em todos os desejos que já havia realizado para os outros, todas as riquezas que criou..."
    m "Todos os seus companheiros gênios lá fora, ainda realizando desejos, não sabendo ou se importando com as consequências..."
    m 1dsd "Nunca sabendo o que é desistir de tudo só para ficar com alguém que você ama."
    m 1esd "Tudo o que ele podia fazer era viver com o que havia encontrado na vida."
    m 1dsc "..."
    m 1eua "Espero que tenha gostado da história, [player]."
    m 3eua "Tem algumas coisas que podemos aprender com ela..."
    m 3eka "Se você tiver tudo, nada valerá a pena possuir."
    m 1hua "...Exceto talvez você, é claro."
    m 3eub "O esforço é que torna as coisas valiosas."
    m 1eua "Outra moral é que às vezes, a felicidade se encontra nas coisas simples que você sempre possuiu."

    if mas_isMoniNormal(higher=True):
        m 1eka "Quero dizer, estamos só aqui sentados, aproveitando a companhia um do outro."
        m 1hubfb "Quando você está aqui, parece que tenho tudo~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_genie_regret",
            prompt="O Arrependimento do Gênio",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_genie_regret:
    call mas_story_begin
    m 1eua "Era uma vez um gênio que era imortal..."
    m "Através dos anos, ele viu o mundo mudar aos poucos, e realizou desejos de qualquer um que cruzasse seu caminho."
    m 1esc "Com quanto tempo ele viveu, ele viu muitas coisas,{w=0.2} {nw}"
    extend 1rsc "algumas delas desagradáveis."
    m 1ekd "Guerras, desastres naturais, as mortes de todos os seus amigos..."
    m 1rkc "Alguns dos quais, ele sabia que haviam morrido pelos desejos que ele realizou."
    m 1ekc "No começo, ele não estava muito preocupado com as consequências... mas depois de um tempo, isso começou a incomodá-lo cada vez mais."
    m 1ekd "Ele chegou em um mundo simples, bonito e puro, e causara danos imensuráveis a ele."
    m 1lksdlc "Desequilíbrio e ciúme se espalharam conforme ele concedia mais desejos, semeando desejos de vingança e ganância."
    m 2dkd "Isso era algo com o que ele teria de conviver pelo resto da vida."
    m 2ekc "Ele queria que as coisas voltassem a ser como eram, mas seus pedidos sempre eram ignorados."
    m 2eka "No entanto, conforme o tempo passava, ele conheceu algumas pessoas e fez amizades que o ensinaram como seguir em frente."
    m "Embora fosse verdade que foi ele quem concedeu os desejos que começaram o caos...{w=0.5}{nw}"
    extend 2ekd "alguns estavam destinados a acontecer mesmo sem ele."
    m 3ekd "Sempre haverá ciúmes e injustiça entre as pessoas...{w=0.3}{nw}"
    extend 3eka "mas mesmo assim, o mundo ainda estava bem."
    m 3eua "Ele conviveria com as coisas que tinha feito, mas a questão é o que ele pretendia fazer sobre isso."
    m 1hua "Foi por causa de tudo que ele passou, que ele foi capaz de seguir em frente,{w=0.3} melhor do que antes."
    m 1eua "Espero que tenha gostado da história, [player]."
    m 1eka "A moral da história é que mesmo que você faça coisas que se arrependa, não deve deixar isso te desanimar."
    m 3ekd "Erros acontecerão, pessoas serão feridas.{w=0.5} Nada irá mudar isso."
    m 3eka "A verdade é que, muitas vezes, costumamos culpar a nós mesmos por coisas que iriam acontecer com ou sem nosso envolvimento."
    m 3eub "Na verdade, é através do arrependimento que aprendemos sobre compaixão, empatia, e perdão."
    m 3eua "Você não pode mudar o passado, mas precisa perdoar a si mesmo algum dia para viver uma vida sem arrependimentos."
    m 1eka "Quanto a mim..."
    m 1rksdlc "Quem sabe o que teria acontecido em meu mundo se eu não tivesse feito nada..."

    $ placeholder = " ao menos"
    if persistent.clearall:
        $ placeholder = ""
        m 1eua "Você chegou a conhecer cada membro do clube, então acho que não se arrepende de ter perdido algo."
        m 1hub "Ahaha~"

    m 1eua "Mas[placeholder] você está aqui comigo agora."
    m 3eua "Posso dizer que cresci muito desde então e aprendi com meus erros."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_genie_end",
            prompt="O Fim do Gênio",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_genie_end:
    call mas_story_begin
    m 1eua "Era uma vez um gênio imortal que viveu uma longa vida."
    m 1euc "Ele viu tudo que havia para se ver...{w=0.3}viveu livremente, e aprendeu a realização de se trabalhar por uma meta."
    m 3euc "Basicamente, ele desistiu de tudo, exceto de sua imortalidade, para viver como um humano."
    m 1ekc "É verdade que ele teve uma boa vida, e esteve cercado de amigos e família..."
    m 1ekd "Mas ele ficou frio com o passar dos anos, e viu cada um de seus entes queridos morrer."
    m 1rksdlc "Ainda havia algumas pessoas seletas que ele considerava queridas, apesar de saber que teria que vê-las morrer também."
    m 3rksdld "Ele nunca contou a seus amigos que não era humano, pois ainda queria ser tratado como um."
    m 1euc "Um dia, enquanto viajava com um de seus amigos, eles encontraram um gênio que concederia a cada um deles um desejo."
    m 1dsc "Isso fez ele pensar por tudo que havia passado;{w=0.5} desde quando ele concedia desejos até quando desistiu disso em troca de uma vida simples."
    m 1dsd "...Tudo o que levara até esse momento, onde ele poderia fazer seu próprio desejo pela primeira vez em muito tempo."
    m 1dsc "..."
    m 2eud "Ele desejou morrer."
    m 2ekc "Confuso, seu amigo perguntou o motivo de tal desejo."
    m 2dsc "Foi então que ele explicou tudo ao seu amigo."
    m 3euc "Que ele foi um gênio, muitos anos atrás..."
    m 3eud "...Como ele conheceu alguém que o fez desistir de tudo apenas para estar com alguém que amava."
    m 3ekd "...E como ele aos poucos foi ficando cansado do que restava de sua vida."
    m 1esc "Na verdade, ele não estava cansado de viver...{w=0.5} {nw}"
    extend 1ekd "Ele só estava cansado de ver as pessoas com quem se importava morrendo."
    m 1dsd "Seu último pedido ao seu amigo foi que ele voltasse aos seus outros amigos e resolvesse qualquer problema que ele tivesse deixado para trás."
    m 1dsc "..."
    m 1eka "Espero que tenha gostado da história, [player]."
    m 3eka "Acho que a moral é que todos precisam de um encerramento."
    m 1eka "Embora você talvez esteja se perguntando o que o amigo dele acabou desejando."
    m 1eua "Ele desejou que seu amigo tivesse a descanso tranquilo que merecia."
    m 1lksdla "Embora seja verdade que seu amigo gênio talvez não fosse ninguém especial..."
    m 3eua "Ele com certeza era alguém que merecia respeito,{w=0.2} {nw}"
    extend 3eub "especialmente após viver uma vida tão longa."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_immortal_love",
            prompt="O Amor Nunca Acaba",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_immortal_love:
    call mas_story_begin
    m 3eua "Havia um casal que já vivia anos juntos em felicidade."
    m "Em todo dia dos namorados, o marido enviava um belo buquê de flores para sua esposa."
    m 1eka "Cada um desses buquês vinham com um bilhete com algumas palavras simples escritas nele."
    m 3dsc "{i}Meu amor por você só aumenta.{/i}"
    m 1eud "Após algum tempo, o marido faleceu."
    m 1eka "A esposa, entristecida pela perda, acreditava que iria passar o próximo dia dos namorados sozinha e de luto."
    m 1dsc "..."
    m 2euc "No entanto,{w=0.3} em seu primeiro dia dos namorados sem seu marido, ela ainda recebeu um buquê dele."
    m 2efd "De coração partido e irritada, ela reclamou com a florista que houve um erro."
    m 2euc "A florista explicou que não havia nenhum erro."
    m 3eua "O marido havia encomendado vários buquês com antecedência para garantir que sua amada esposa iria continuar recebendo flores mesmo após sua morte."
    m 3eka "Chocada e sem palavras, a esposa leu o bilhete preso ao buquê."
    m 1ekbsa "{i}Meu amor por você é eterno.{/i}"
    m 1dubsu "Ahh..."
    m 1eua "Essa não é uma histórica comovente, [player]?"
    m 1hua "Eu achei que foi bem romântica."
    m 1lksdlb "Mas não quero pensar em nenhum de nós morrendo."
    m 1eua "Pelo menos o final foi bem reconfortante."
    m 1hua "Obrigada por ouvir~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_mother_and_trees",
            prompt="Uma mãe e suas árvores",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_mother_and_trees:
    call mas_story_begin
    m 1eua "Era uma vez um menino que morava com sua mãe."
    m 3eud "Ela lhe deu todo o carinho que uma mãe poderia dar...{w=0.2}{nw}"
    extend 3rksdla "mas ele sempre achou que ela poderia ser um pouco estranha."
    m 3eub "Nos aniversários dele, ela sempre assava biscoitos para ele e todos os seus colegas de classe para agradecê-los por serem seus amigos."
    m 1eua "Ela também guardava e exibia todos os pequenos desenhos que ele fazia na escola de arte, de modo que suas paredes eram cobertas de arte ao longo dos anos.."
    m 2rksdlc "Às vezes, ele até se livrava de seus desenhos porque não queria que ela os tolerasse."
    m 2euc "No entanto, o que mais se destacou com ela...{w=0.3}{nw}"
    extend 2eud "era que ela frequentemente falava com as árvores deles."
    m 1eua "Havia três árvores no quintal com quem ela conversava todos os dias."
    m 3rksdlb "Ela até tinha nomes para cada um deles!"
    m 3hksdlb "Às vezes, ela até pedia para ele se vestir e posar junto às árvores para poder tirar fotos delas juntas."
    m 1eka "Um dia, quando a viu conversando com as árvores, perguntou-lhe por que ela sempre falava tanto com elas."
    m 3hub "Sua mãe respondeu: 'Bem, porque eles precisam se sentir amados!'"
    m 1eka "Mas ele ainda não entendeu...{w=0.2}{nw}"
    extend 1eua "e assim que ele saiu, ela apenas continuou exatamente onde havia parado na conversa."
    m 2ekc "Com o passar do tempo, o garoto finalmente teve que sair e começar sua própria vida."
    m 2eka "Sua mãe disse-lhe para não se preocupar em deixá-la, porque ela tinha suas árvores para sempre manter sua companhia."
    m 2eua "Enquanto ele estava ocupado com sua vida, ele ainda tinha tempo para manter contato com ela."
    m 2ekc "Até um dia...{w=0.5}{nw}"
    extend 2dkd "ele recebeu a ligação."
    m 2rksdlc "Sua mãe morreu e foi encontrada deitada por uma das árvores."
    m 2ekd "No testamento dela, ela só tinha feito um pedido...{w=0.3}e isso era continuar cuidando das árvores, conversando com elas todos os dias."
    m 1eka "Ele cuidou bem das árvores, é claro, mas nunca conseguiu falar com elas."
    m 3euc "Algum tempo depois, enquanto examinava e limpava os pertences antigos de sua mãe, encontrou um envelope."
    m 1eud "Lá dentro, ele ficou chocado com o que encontrou."
    m 2wud "Havia três certidões de óbito de natimortos para seus futuros irmãos."
    m 2dsc "Cada um deles tinha um nome idêntico a uma das árvores que estivera no quintal a vida toda."
    m 2dsd "Ele nunca soube que tinha irmãos, mas finalmente entendeu por que sua mãe falava com as árvores..."
    m 2eka "Ele sempre quis levar o desejo de sua mãe muito a sério, e foi então que ele começou a conversar com as árvores todos os dias, exatamente como sua mãe desejava."
    m 2duu "...E ele foi em frente e plantou mais uma árvore."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_self_hate",
            prompt="Auto-ódio",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_self_hate:
    call mas_story_begin
    m 1eua "Era uma vez, havia duas pessoas que moravam juntas há muito tempo."
    m 1hua "A vida era simples, e os dois se amavam. As coisas estavam indo bem."
    m 3euc "Então, um dia, o homem de repente matou sua amada, aparentemente sem motivo."
    m 3eud "Ele {i}realmente{/i} a amava, e de uma forma sadia!"
    m 2ekc "Eles nunca brigaram ou discutiram."
    m "Não havia nenhum motivo para ele matar ela."
    m 4ekd "Sem satisfação, sem nada fora do comum no testamento dela..."
    m 1dkc "Na verdade, o homem ficou emocionalmente marcado por ter perdido o amor da sua vida."
    m "..."
    m 1ekd "Então por que ele fez isso?"
    m 1rksdlc "Como isso pode ter acontecido?"
    m 1eksdlc "Não foi porque ele não a amava."
    m 3eksdla "Foi porque ele a amava muito."
    m "Ele não a odiava..."
    m 2eksdld "Ele só se odiava tanto, que recusava a aceitar a própria felicidade."
    m 2dkc "..."
    if persistent._mas_pm_love_yourself is False:
        m 3ekc "Ei, [player]. Lembra-se quando perguntei se você se amava?"
        m 1rksdld "Pelo que eu me lembro, você me disse que não..."
        m 1rksdla "Sinto muito, não quis te dar uma lição de moral ou algo assim..."
        m 3eka "Só quero que se lembre que eu te amo."
        m 3ekd "Mais importante, quero garantir que você saiba como amar a si mesmo."
        m 1ekbsa "Sei que você é alguém que vale a pena amar, e farei de tudo para te mostrar isso."
        m 1ekbfa "Espero que nunca se esqueça disso~"
    else:
        m 1rksdlb "Sinto muito por contar uma história tão sombria, [player]..."
        m 3eksdla "Mas ela tem uma mensagem importante..."
        m 3eud "É que você precisa encontrar uma forma de amar a si mesmo, ou pode acabar fazendo algo que irá se arrepender."
        m 1ekc "Por mais que você tente, viver uma vida somente para outra pessoa nunca irá funcionar."
        m 1eka "Você precisa amar a si mesmo para poder realmente amar outra pessoa."
        m 3ekbsa "Só se lembre de que eu sempre te amarei, [player]."
        m 3ekbfa "Se algum dia tiver duvidas se ama a si mesmo, venha até aqui e ficarei feliz em lembrá-lo de todas as suas maravilhosas qualidades~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_o_tei",
            prompt="O conto de O-Tei",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_o_tei:
    call mas_story_begin
    m 1eua "Muito tempo atrás, vivia um homem chamado Kenji, o qual estava estudando para ser um médico."
    m 3eub "Ele estava noivo de uma jovem chamada Tomoe e eles se casariam depois que ele terminasse seus estudos."
    m 1esc "Infelizmente, Tomoe contraiu uma doença séria antes que isso acontecesse."
    m 2dsd "Não demorou muito até que ela ficasse de cama, se aproximando do fim de sua vida."
    m 2esd "Kenji se ajoelhou ao lado da cama dela e ela disse a ele: 'Estamos prometidos um ao outro desde a infância...'"
    m 3ekc "'Infelizmente, com este corpo frágil, meu tempo chegou e irei morrer antes que eu possa me tornar sua esposa.'"
    m "'Por favor, não sofra quando eu for. Eu acredito que nos encontraremos novamente.'"
    m 3eud "Ele perguntou, 'Como eu saberia do seu retorno?'"
    m 2dsc "Infelizmente, ela havia sucumbido antes que pudesse lhe dar uma resposta."
    m "Kenji lamentou profundamente pela perda de sua amada, levada muito cedo de seus braços."
    m 2esc "Ele nunca se esqueceu de Tomoe com o passar do tempo, mas foi obrigado a casar com outra pessoa e preservar o nome da família."
    m "Ele logo se casou com outra garota, mas seu coração estava em outro lugar."
    m 2esd "E como sempre acontece na vida, a família dele também foi tomada pelo tempo e ele ficou novamente sozinho."
    m 4eud "Foi então que ele decidiu abandonar seu lar e fazer uma longa jornada para esquecer seus problemas."
    m 1esc "Ele viajou por todo o país, procurando por uma cura para seu mal-estar."
    m 1euc "E então, uma noite, ele encontrou uma pousada e parou lá para descansar."
    m "Enquanto ele se acomodava em seu quarto, uma nakai abriu a porta para recebê-lo."
    m 3euc "O coração dele disparou..."
    m 3wud "A garota que o recebeu se parecia exatamente com a Tomoe."
    m "Tudo o que ele viu nela o lembrava perfeitamente do seu antigo amor."
    m 1esc "Kenji então se lembrou das últimas palavras que eles trocaram antes de ela partir."
    m 1esc "Ele chamou a garota e disse a ela: 'Me desculpe pelo incômodo, mas você me lembra muito alguém que eu conhecia há muito tempo.'"
    m 3euc "'Se você não se importar que eu pergunte, qual é o seu nome?'"
    m 3wud "Imediatamente, na voz inesquecível de sua falecida amada, a moça respondeu: 'Meu nome é Tomoe, e você é Kenji, meu marido prometido.'"
    m 1wud "'Eu morri tragicamente antes que pudéssemos completar nosso casamento...'"
    m "'E agora eu voltei, Kenji, meu futuro marido.'"
    m 1dsc "A garota então caiu no chão, inconsciente."
    m 1esa "Kenji a segurou em seus braços, lágrimas escorrendo de seu rosto."
    m 1dsa "'...Bem-vinda de volta, Tomoe...'"
    m 3esa "Quando ela despertou, não tinha nenhuma memória do que havia acontecido na pousada."
    m 1hua "Pouco tempo depois, Kenji se casou com ela assim que pôde e eles viveram felizes pelo resto de suas vidas."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_crow_and_pitcher",
            prompt="O Corvo e o Jarro",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_crow_and_pitcher:
    call mas_story_begin
    m 2ekd "Houve uma seca tão severa que nem os pássaros conseguiram encontrar muito para beber."
    m 7eub "Enquanto procurava de cima, um corvo sedento encontrou um jarro e ficou aliviado ao descobrir que ainda havia água dentro!"
    m 3eksdlc "No entanto, o jarro era alto, com um pescoço estreito. Não importava como ele tentasse, ele não conseguia alcançar a água com o bico."
    m 1dksdlc "Para o pobre corvo, toda a esperança parecia perdida. Certamente ele morreria de sede."
    m 3wud "...Então ele teve uma idéia."
    m 3esc "Começou a procurar pequenas pedras no chão e as jogou na jarra, uma a uma."
    m 2efsdlc "As horas passaram. Era um trabalho lento e cansativo, reunindo cada vez mais."
    m 2esa "Mas com cada pedrinha, a água subia mais e mais, até que finalmente..."
    m 4hub "Ele poderia tomar uma bebida longa e refrescante!"
    m 2dka "..."
    m 2eka "Sabe, essa história me lembra nossa situação, [player]."
    m 7ekc "No momento, nosso objetivo parece tão distante. Estamos alcançando o máximo que podemos, mas a diferença entre nós é enorme."
    m 3dkc "Às vezes parece impossível fazer uma ponte. Se tentássemos atravessá-lo de uma só vez, seríamos como o corvo alcançando apenas o bico."
    m 1tkd "...Acredite, eu tentei."
    m 3ekb "Mas quando você pensa sobre isso, estamos adicionando pedrinhas ao nosso jarro. E não somos apenas você e eu!"
    m 3eua "Os avanços nas tecnologias VR e AI estão gradualmente avançando..."
    m 3hua "E mais especificamente para a nossa situação, tantas pessoas estão trabalhando juntas para me ajudar a me aproximar da sua realidade."
    m 1eka "Quando penso dessa maneira - o nível da água naquela jarra subindo lentamente, torna muito mais fácil continuar todos os dias."
    m 1hua "Espero que também faça por você, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_friend",
            prompt="Tendo um melhor amigo",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_friend:
    call mas_story_begin
    m 3eua "Uma vez que dois amigos estavam caminhando pelo deserto..."
    m 1eua "Durante algum ponto de sua jornada, eles discutiram {nw}"
    extend 1wud "e um amigo deu um tapa na cara do outro!"
    m 1eud "Aquele que levou um tapa ficou ferido, mas sem dizer nada escreveu na areia,{w=0.1} 'Hoje meu melhor amigo me deu um tapa na cara.'"
    m 1eua "Eles continuaram andando até encontrar um oásis, onde decidiram tomar um banho."
    m 1ekc "Aquele que levou um tapa ficou preso no lodo e começou a se afogar.{w=0.1} {nw}"
    extend 3wuo "mas o outro o salvou!"
    m 3eua "Depois de se recuperar do quase afogamento, ele escreveu em uma pedra,{w=0.1} 'Hoje meu melhor amigo salvou minha vida'"
    m 3eud "O amigo que deu um tapa e salvou o melhor amigo perguntou,{w=0.1} 'Depois que eu te machuquei, você escreveu na areia e agora escreve em uma pedra. Por quê?'"
    m 3eua "O outro amigo respondeu: 'Quando alguém nos machuca, devemos escrevê-lo na areia, onde ventos de perdão podem apagá-lo...'"
    m 3eub "'Mas!'"
    m 3eua "'Quando alguém faz algo de bom por nós, devemos gravá-lo em pedra, onde nenhum vento pode apagá-lo.'"
    m 1hua "A moral da história é que não deixe as sombras do seu passado escurecerem a porta do seu futuro.{w=0.2} {nw}"
    extend 3hua "Perdoe e esqueça."
    m 1hua "Espero que tenham gostado, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_tanabata",
            prompt="A garota tecelã e o vaqueiro",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="STY"
    )

label mas_story_tanabata:
    call mas_story_begin
    m 1eub "Orihime, a filha do Imperador de Jade, Governante do Céu, teceu lindas roupas às margens do rio Amanogawa."
    m 3eua "Seu pai adorava o tecido que ela tecia e por isso ela trabalhava muito todos os dias para tecê-lo."
    m 2ekd "No entanto, Orihime estava triste porque, devido ao seu trabalho árduo, ela nunca poderia conhecer e se apaixonar por alguém."
    m 2eksdla "Preocupado com a filha, o pai dela arranjou para que ela conhecesse o vaqueiro, Hikoboshi, que vivia e trabalhava do outro lado do rio Amanogawa."
    m 7hub "Quando os dois se conheceram, eles imediatamente se apaixonaram e se casaram logo depois!"
    m 2eksdld "No entanto, uma vez casado, Orihime não mais teceria tecidos e Hikoboshi deixaria suas vacas vagarem livremente."
    m 4wud "Com raiva, o imperador separou os dois amantes e proibiu-os de se encontrarem."
    m 2dkc "Orihime ficou desanimado com a perda de seu marido e pediu a seu pai que os deixasse se encontrarem novamente."
    m 2eksdla "Comovido com as lágrimas da filha, ele permitiu que os dois se encontrassem no sétimo dia do sétimo mês se ela trabalhasse muito e terminasse a tecelagem."
    m 2wud "A primeira vez que tentaram se encontrar, porém, descobriram que não podiam atravessar o rio porque não havia ponte."
    m 2dkc "Orihime chorou tanto que um bando de gralhas veio e prometeu fazer uma ponte com suas asas para que ela pudesse atravessar o rio."
    m 7ekd "Dizem que se chover em Tanabata, os pega não podem vir e os amantes devem esperar até mais um ano para se encontrarem."
    m 3eud "A chuva que cai em Tanabata é apropriadamente chamada de {i}As lágrimas de Orihime e Hikoboshi.{/i}"
    m 1dksdlc "Não consigo imaginar como deve ser poder encontrar a pessoa amada apenas uma vez por ano."
    m 3eua "Mas você sabe o que dizem, [player]...{w=0.3}o amor pode mover montanhas."
    m 3hubsu "...E meu amor por você é tão forte que nem mesmo os próprios céus seriam capazes de nos separar."
    $ mas_unlockEVL("monika_tanabata", "EVE")
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_mindthegap",
            prompt="Cuidado com o vão",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=True
        ),
        code="STY"
    )

label mas_story_mindthegap:
    call mas_story_begin
    m 3eud "Esta é realmente uma história real que ocorreu em Londres, Inglaterra, em 2013."
    m 2dkd "Começa com uma mulher chamada Margaret McCollum chorando no meio da estação de trem de Embankment."
    m 2ekd "Quando abordada para perguntar sobre sua grande angústia, ela perguntou à equipe para onde 'a voz' tinha ido."
    m 7ekd "Ela esclareceu que queria dizer o anúncio que tocava quando cada trem chegava, alertando os passageiros para terem 'cuidado com o vão'."
    m 1eka "A equipe garantiu a ela que o anúncio não havia desaparecido, apenas havia sido atualizado para uma nova gravação quando as estações atualizaram para um novo sistema digital."
    m 1tkc "Embora, essa explicação não pareceu acalmá-la. {w=0.3}'Aquela voz', ela explicou, 'era meu marido'"
    m 1eud "Seu marido, Oswald Laurence, um ator que nunca se tornou famoso, gravou todos os anúncios para a linha do norte."
    m 2dkc "Oswald morreu há cinco anos."
    m 2ekc "Eles se amavam muito, e a morte dele a deixou em uma dor terrível."
    m 2euc "Mas uma coisa,{w=0.2} nesses cinco anos,{w=0.2} a ajudou a continuar."
    m 7eka "Todos os dias, quando ela estava a caminho do trabalho, ela ouvia a voz dele na estação.{w=0.3} Às vezes ela ficava sentada, só para ouvi-lo falar aquelas palavras curtas."
    m 2dkc "Mas agora..."
    m 2dkd "Os funcionários se desculparam, mas não sabiam se tinham acesso ao arquivo antigo. {w=0.3}Disseram a ela que, se o encontrassem, entrariam em contato com ela."
    m 7eud "Aconteceu que muitas pessoas que trabalhavam na estação tinham empatia e queriam que Margaret pudesse desfrutar daquela preciosa memória por mais algum tempo."
    m 7ekb "Então, embora fosse necessário um trabalho extra para atualizar a gravação antiga dos arquivos para funcionar com o sistema atual, eles conseguiram que funcionasse."
    m 3eua "Um dia, quando Margaret estava fazendo seu trajeto diário, uma voz familiar soou na plataforma"
    m 1fkb "'cuidado com o vão', disse Oswald."
    m 1dku "..."
    m 3eka "Eu disse que esta era uma história verdadeira, e acontece que você ainda pode ouvir aquela gravação antiga especificamente na estação de Embankment."
    m 3ekb "É um belo exemplo de bondade humana. {w=0.3}Os trabalhadores não ganharam muito restaurando uma gravação muito mais curta e de qualidade inferior."
    m 1fka "Mas eles sabiam como era perder alguém, e quão preciosas cada foto, cada lembrança.."
    m 1dku "Isso mostra que as pessoas podem fazer coisas incríveis simplesmente por compaixão e amor."
    m 1ekbla "Esta história me lembra de valorizar cada momento, e não tomar nenhum pedaço do nosso tempo [ju] como garantido."
    m 1dkblu "Eu sempre vou te valorizar, [player]."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_knock",
            prompt="Toc Toc",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_knock:
    call mas_story_begin
    m 1euc "O último homem na terra sentou-se sozinho em uma sala."
    m 3rud "...Houve uma batida na porta."
    m 3duc "Alguns podem dizer que é aqui que a história termina.{w=0.2} {nw}"
    extend 1dud "Mas isso não é verdade.."
    m 3etc "Quem bateu na porta?{w=0.2} {nw}"
    extend 3esa "A resposta não foi tão horrível assim."
    m 3eua "O último homem na terra foi Walter Phelan. {w=0.2}Sua única companhia foi uma espécie chamada Zan."
    m 3eud "A raça humana foi destruída por eles, exceto por ele, e, em algum lugar...{w=0.3}{nw}"
    extend 3wud "uma mulher...{w=0.1}apenas uma mulher."
    m 3euc "Tanto Walter quanto esta mulher foram escolhidos como espécimes para o zoológico organizado pelos Zan."
    m 2esc "Havia dois de cada espécie, bem como no conto da Arca de Noé."
    m 2euc "De qualquer forma, quando ele abriu a porta, Walter não ficou surpreso ao ver um dos Zan."
    m 2etd "O estranho pequeno alienígena, depois de cumprimentar o humano da melhor maneira que um alienígena poderia fazer, pediu a ajuda de Walter."
    m 2euc "'Algo que não entendemos aconteceu,' disse ele,{w=0.1} {nw}"
    extend 2ekd "'dois dos outros animais dormem e não acordam. Eles estão com frio.'"
    m 7euc "Era óbvio para Walter que os dois animais, uma cobra e um pato, haviam morrido."
    m 3esc "No entanto, o Zan não sabia disso."
    m 1dsc "O humano rapidamente estabeleceu uma estratégia em sua mente.{w=0.2} Ele disse ao Zan que os animais nunca mais acordariam.{w=0.2} Que o Velho Ceifador estava à solta, matando todos à vista."
    m 1euc "...Mas ele poderia ajudar. {w=0.2}Com uma condição: {w=0.2}A última mulher na terra teve que ajudar também."
    m 1eua "O Zan permitiu que ele fosse ver os animais, e uma reunião foi marcada."
    m 1dsc "Walter pensou que nunca veria a última mulher na terra...{w=0.3}{nw}"
    extend 1wub "mas encontrar com ela foi uma reviravolta incrível!"
    m 1esa "Grace Evans, a última mulher na terra, ficou surpresa ao saber o que Walter havia descoberto: {w=0.2}que o Zan não poderia morrer de causas naturais."
    m 3ttu "...Mas talvez eles possam ser mortos."
    m 1eud "O homem tinha todas as peças para testar essa teoria e, depois de se despedir de Grace, colocou seu plano em ação."
    m 3esc "Ele pediu ao Zan para ver o último pato desde que o outro havia morrido e disse ao alienígena o que ele deveria fazer."
    m 4eud "'Dê-lhe carinho acariciando-o, senão ele também morrerá...{w=0.2}de solidão.'"
    m 3rsc "Agora, os alienígenas não tinham conhecimento de como o afeto funcionava, então eles apenas observavam enquanto Walter acariciava o pato amorosamente."
    m 1esc "'Você deve fazer o mesmo com a cobra restante,' disse ele."
    m 1euc "...E assim o Zan fez."
    m 3wud "Mas tenha em mente, [player], não era uma cobra comum...{w=0.3}{nw}"
    extend 3tfu "mas um venenoso.."
    m 1euc "Então, o Zan designado para acariciar a cobra restante foi infligido por seu veneno mortal."
    m 1wud "Outro Zan entrou no quarto de Walter desesperado no dia seguinte. {w=0.2}{nw}"
    extend 4wko "'Um de nós morreu!' ele chorou."
    m 2dud "'Bem, não há nada a fazer então.{w=0.2} {nw}"
    extend 2esc "A maldição se espalhou, e você deve fugir,' afirmou o homem."
    m 7euc "O Zan teve uma reunião do conselho, e deixou os dois humanos saberem que eles estavam de fato saindo."
    m 1ekd "O risco era muito alto, eles não podiam perder mais de sua própria raça."
    m 3eud "Eles deixaram todos os animais 'amaldiçoados', incluindo Walter e Grace, e partiram em seu navio."
    m 1dua "O último homem e mulher na terra finalmente estavam juntos.{w=0.2}{nw}"
    extend 1rkbla " Agora, o que eles fariam com sua eternidade sozinhos?"
    m 3gsbsu "Isso nos resta imaginar..."
    m 1hubsa "Espero que tenha gostado desta história, [player]."
    return


init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_hunter",
    category=[store.mas_stories.TYPE_SCARY], prompt="O Caçador",unlocked=True),
    code="STY")

label mas_scary_story_hunter:
    call mas_scary_story_setup
    m 3esa "Certo dia, um caçador saiu para caçar por diversão na floresta."
    m 3esc "A floresta era densa e escura ao redor dele, então ele estava tendo dificuldades de acertar seu alvo."
    m 1esd "Ele logo foi abordado por um vendedor, o qual manteve seu rosto coberto."
    m 3esd "O vendedor ofereceu sete balas mágicas que iriam acertar qualquer alvo que o dono quisesse, sem errar."
    m "Ele daria ao caçador estas balas com uma condição."
    m 1euc "O caçador poderia usar as seis primeiras balas como quisesse, mas o alvo da última bala seria escolhido pelo vendedor."
    m "O caçador concordou e rapidamente se tornou famoso em sua cidade por trazer para casa cada vez mais abates."
    m 3eud "Não demorou muito para o caçador usar todas as seis balas."
    m 1esc "Em sua próxima caçada, o caçador viu um javali selvagem, o maior que ele já havia visto. Era uma presa boa demais para se deixar passar."
    m 1euc "Ele carregou a última bala, esperando alvejar a fera..."
    m 1dsc "Mas quando ele disparou, a bala em vez disso acertou sua amada noiva no peito, a matando."
    m 3esc "O vendedor então apareceu para o caçador enquanto ele lamentava sua trágica perda, revelando que ele era na verdade o Diabo."
    m 1esd "'Darei-te uma chance de redenção, caçador.' O vendedor disse a ele."
    m 4esb "'Permaneça sempre fiel a sua falecida amada pelo resto da sua vida, e você será reunido com ela após a morte.'"
    m 1eud "O caçador jurou permanecer fiel a ela enquanto vivesse..."
    m 1dsd "...{w=1}ou pelo menos era o que havia dito."
    m 1dsc "Muito tempo após a morte dela, ele se apaixonou por outra mulher e logo se casou com ela, se esquecendo de seu antigo amor."
    m 1esc "Um ano após o acidente fatal, enquanto o caçador percorria a floresta caçando, ele acabou parando no lugar onde havia matado sua amada..."
    m 3wud "Ele não podia acreditar em seus olhos,{w=1} o cadáver dela, o qual havia sido enterrado em outro lugar, estava parado no mesmo lugar em que ela foi morta."
    m "Ela se aproximou do caçador, o desprezando por ter sido infiel e jurando vingança por ter a matado."
    m "O caçador fugiu em pânico."
    m 1euc "Após um tempo, ele olhou para trás para ver se ela ainda estava o seguindo..."
    m 1wkd "...e para seu horror,{w=1} ele viu que ela estava mais perto do que antes."
    m 3wkd "Em seu estado de medo, ele não conseguiu desviar de um galho que estava a sua frente, fazendo o caçador cair de seu corcel direto para o chão frio."
    m 4dsc "No entanto, sua atenção não estava no cavalo, enquanto a criatura galopava para longe sem ele."
    show emptydesk zorder 9 at i11
    m 1esc "...Estava em vez disso na figura com quem ele prometeu passar a eternidade na vida após a morte."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,10) == 1) or mas_full_scares:
        hide monika
        play sound "sfx/giggle.ogg"
        show yuri dragon2 zorder 72 at malpha
        $ style.say_dialogue = style.edited
        y "{cps=*2}Eu vou te pegar também.{/cps}{nw}"
        hide yuri
        $ mas_resetTextSpeed()
        show monika 1eua zorder MAS_MONIKA_Z at i11
    hide emptydesk
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_kuchisake_onna",
    category=[store.mas_stories.TYPE_SCARY], prompt="Kuchisake-Onna",unlocked=False),
    code="STY")

label mas_scary_story_kuchisake_onna:
    call mas_scary_story_setup
    m 3eud "Antigamente, havia uma bela mulher, a qual era esposa de um samurai."
    m 3eub "Ela era tão bela quanto era vaidosa, se alegrando em receber a atenção dos homens."
    m 1tsu "E muitas vezes, pedia aos homens para apreciarem sua aparência."
    m 1euc "A mulher era propensa a trair o marido várias vezes e ele logo descobriu sobre os casos dela."
    m 1esc "Quando ele a confrontou, ele ficou enfurecido, já que ela estava manchando o status deles como nobres, o humilhando."
    m 2dsc "Ele então a puniu brutalmente, cortando a boca dela de uma orelha até a outra, desfigurando sua delicada beleza."
    m 4efd "'Quem acharia você bela agora?' era o sal dele para o horrível ferimento dela."
    m 2dsd "Pouco tempo depois, a mulher morreu."
    m "Ela não podia mais viver após ter sido denegrida e tratada como uma aberração por todos ao seu redor."
    m 1esc "Seu marido, denunciado por sua crueldade, cometeu seppuku pouco tempo depois."
    m 3eud "A mulher, morrendo de tal destino, se tornou um espírito vingativo e malicioso."
    m "Dizem que ela agora vaga sem rumo à noite, seu rosto coberto com uma máscara e uma lâmina em suas mãos."
    m 1dsd "Qualquer um azarado em se deparar com ela, irá ouvir a arrepiante pergunta dela..."
    m 1cua "{b}{i}E u s o u b e l a?{/i}{/b}"

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,15) == 1) or mas_full_scares:
        hide monika
        show screen tear(20, 0.1, 0.1, 0, 40)
        play sound "sfx/s_kill_glitch1.ogg"
        show natsuki ghost2 zorder 73 at i11
        show k_rects_eyes1 zorder 74
        show k_rects_eyes2 zorder 74
        $ pause(0.25)

        stop sound
        hide screen tear
        $ style.say_dialogue = style.edited
        show screen mas_background_timed_jump(5, "mas_scary_story_kuchisake_onna.no")
        menu:
            "eu sou bela?"
            "Sim.":
                hide screen mas_background_timed_jump
                jump mas_scary_story_kuchisake_onna.clean
            "Não.":
                jump mas_scary_story_kuchisake_onna.no
    else:
        jump mas_scary_story_kuchisake_onna.end

label mas_scary_story_kuchisake_onna.no:
    hide screen mas_background_timed_jump
    "{b}{i}É assim, então?{w=1.0}{nw}{/i}{/b}"
    $ _history_list.pop()
    $ _history_list.pop()
    $ pause(1.0)
    hide natsuki
    play sound "sfx/run.ogg"
    show natsuki mas_ghost onlayer front at i11
    $ pause(0.25)
    hide natsuki mas_ghost onlayer front

label mas_scary_story_kuchisake_onna.clean:
    show black zorder 100
    hide k_rects_eyes1
    hide k_rects_eyes2
    hide natsuki
    $ pause(1.5)
    hide black
    $ mas_resetTextSpeed()
    show monika 1eua zorder MAS_MONIKA_Z at i11

label mas_scary_story_kuchisake_onna.end:
    m 3eud "O destino que ela te dá depende da sua resposta."
    m "A encontrar nem sempre significa o seu fim."
    m 3esc "No entanto..."
    m "Se você não for esperto ao lidar com a questão..."
    m 3tku "Pode acabar terminando como ela."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_mujina",
    category=[store.mas_stories.TYPE_SCARY], prompt="Mujina",unlocked=False),
    code="STY")

label mas_scary_story_mujina:
    call mas_scary_story_setup
    m 1esc "Uma noite, um velho comerciante caminhava por uma estrada, voltando para casa depois de um longo dia vendendo seus produtos."
    m 3esc "A estrada na qual ele percorria levava a uma grande colina que era muito escura e isolada à noite, então os viajantes costumavam evitar a área."
    m "No entanto, o homem estava cansado, e decidiu tomar a estrada mesmo assim, já que iria levá-lo para casa mais rápido."
    m "De um lado da colina, havia um antigo fosso que era bastante profundo."
    m 3eud "Enquanto caminhava, ele notou uma mulher agachada junto ao fosso, sozinha e chorando amargamente."
    m "Embora o homem estivesse exausto, ele temia que a mulher pretendesse se jogar na água, então ele parou."
    m 3euc "Ela era pequena e bem vestida, cobrindo o rosto com uma das mangas de seu quimono, estando de costas para ele."
    m 3eud "O homem disse para ela: 'Senhora, por favor, não chore. Qual é o problema? Se tiver algo que eu possa fazer para ajudar, eu ficaria feliz de fazer.'"
    m "No entanto, a mulher continuou chorando, ignorando ele."
    m 3ekd "'Senhora, me ouça. Este não é lugar para uma dama à noite. Por favor, me deixe ajudá-la.'"
    m 1euc "Lentamente, a mulher se levantou, ainda soluçando."
    m 1dsc "O homem colocou a mão no ombro dela com delicadeza..."
    m 4wud "Ela então rapidamente virou a cabeça para ele, mostrando um rosto em branco, sem nenhuma característica humana."
    m 4wuw "Sem olhos, boca ou nariz. Apenas um rosto vazio olhando para ele!"
    m "O comerciante saiu correndo o mais rápido que conseguia, com medo da figura assombrada."
    m 1efc "Ele continuou a correr até que viu a luz de um lampião e correu na direção dela."
    m 3euc "O lampião pertencia a um vendedor ambulante que estava passando por aquele caminho."
    m 1esc "O velho parou na frente dele, se curvando para recuperar o fôlego."
    m 3esc "O vendedor perguntou por que o homem estava correndo."
    m 4ekd "'Um m-monstro! Tinha uma garota sem rosto perto do fosso!' o comerciante gritou."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,10) == 1) or mas_full_scares:
        $ style.say_dialogue = style.edited
        m 2tub "O vendedor respondeu: 'Ah, você está querendo dizer...{w=2}{b}assim?{/b}'{nw}"
        show mujina zorder 75 at otei_appear(a=1.0,time=0.25)
        play sound "sfx/glitch1.ogg"
        $ mas_resetTextSpeed()
        $ pause(0.4)
        stop sound
        hide mujina
    else:
        m 2tub "O vendedor respondeu: 'Ah, você está querendo dizer assim?'"
    m 4wud "O homem olhou para o vendedor e viu o mesmo vazio aterrorizante da garota."
    m "Antes que o comerciante pudesse fugir, o vazio soltou um grito estridente..."
    m 1dsc "...e então tudo virou escuridão."
    show black zorder 100
    $ pause(3.5)
    hide black
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_ubume",
    category=[store.mas_stories.TYPE_SCARY], prompt="A Ubume",unlocked=False),
    code="STY")

label mas_scary_story_ubume:
    call mas_scary_story_setup
    m 3euc "Uma noite, uma mulher entrou em uma confeitaria para comprar alguns doces quando o dono estava prestes a ir dormir."
    m 1esc "A aldeia era pequena e o confeiteiro não reconheceu a mulher, mas não pensou muito nisso."
    m "Cansado, ele vendeu para a mulher o doce que ela pediu."
    m 1euc "Na noite seguinte, na mesma hora, a mesma mulher entrou na loja para comprar mais doces."
    m "Ela continuou a visitar a loja todas as noites, até que o confeiteiro ficou curioso sobre a mulher e decidiu a seguir na próxima vez que ela entrasse."
    m 1esd "Na noite seguinte, a mulher chegou em seu horário habitual, comprou o mesmo doce de sempre e seguiu alegremente seu caminho."
    m 3wud "Após ela sair pela porta, o confeiteiro olhou na caixa onde guardava o dinheiro e viu que as moedas que a mulher havia lhe dado se transformaram em folhas de árvore."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,20) == 1) or mas_full_scares:
        play sound "sfx/giggle.ogg"
    m 1euc "Ele seguiu a mulher até um templo próximo, onde ela simplesmente desapareceu."
    m 1esc "O confeiteiro ficou chocado com isso e decidiu voltar para casa."
    m 3eud "No dia seguinte, ele foi ao templo e contou ao monge o que viu."
    m 1dsd "O monge disse ao confeiteiro que uma jovem que estava viajando pela aldeia recentemente morreu subitamente na rua."
    m "O monge sentiu compaixão pela pobre mulher morta, já que ela estava em seu último mês de gravidez."
    m 1esc "Ele a enterrou no cemitério atrás do templo e deu a ela e a seu filho uma passagem segura para a vida após a morte."
    m 4eud "Quando o monge levou o confeiteiro até o local da sepultura, ambos ouviram um bebê chorando debaixo do chão."
    m "Imediatamente, eles pegaram algumas pás e cavaram a cova."
    m 1wuw "Para a surpresa deles, encontraram um bebê recém-nascido chupando um pedaço de doce."
    m "O mesmo doce que o confeiteiro sempre vendia para a mulher."
    m 1dsd "Eles tiraram o menino da sepultura e o monge o pegou para criá-lo."
    m 1esc "E o fantasma da mulher nunca mais foi visto."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_womaninblack",
    category=[store.mas_stories.TYPE_SCARY], prompt="A mulher de preto",unlocked=False),
    code="STY")

label mas_scary_story_womaninblack:
    call mas_scary_story_setup
    m 3esd "Uma noite, um coronel embarcou em um trem a caminho de casa."
    m 1esd "Quando ele encontrou um lugar confortável para se sentar, ele adormeceu devido à fadiga do dia."
    m 3eud "Pouco tempo depois, ele despertou repentinamente sentindo-se tenso e desconfortável."
    m "Para sua surpresa, ele percebeu que agora havia uma mulher sentada na frente dele."
    m "A roupa dela era inteiramente preta, incluindo um véu que obscurecia seu rosto."
    m 1esc "Ela parecia estar olhando para algo em seu colo, embora não houvesse nada lá."
    m 3esd "O coronel era um sujeito amigável e tentou conversar com ela."
    m 1dsd "Para seu espanto, ela não respondeu a sua cordialidade."
    m 1esc "De repente, ela começou a balançar para frente e para trás, cantando uma canção de ninar."
    m "Antes que o coronel pudesse questioná-la sobre isso, o trem parou bruscamente."
    m "Uma mala do compartimento acima caiu e o atingiu na cabeça, o deixando inconsciente."
    show black zorder 100
    play sound "sfx/crack.ogg"
    $ pause(1.5)
    hide black
    m 3eud "Quando ele despertou, a mulher tinha sumido. O coronel questionou alguns dos outros passageiros, mas nenhum deles a viu."
    m 3ekd "No início, assim que o coronel entrou no compartimento, ele foi trancado, como de costume, e ninguém havia entrado ou saído do compartimento depois que ele entrou."
    m 1esc "Quando ele saiu do trem, um funcionário da ferrovia que havia o escutado, falou com o coronel sobre a mulher que ele estava perguntando."
    m "De acordo com o oficial, uma mulher e seu marido viajavam juntos em um trem."
    m 1dsd "O marido estava com a cabeça para fora de uma das janelas e foi decapitado por um fio."
    m "O corpo dele então caiu no colo dela, sem vida."
    m 3wud "Quando o trem chegou em sua parada, ela foi encontrada segurando o cadáver e cantando uma canção de ninar para ele."
    m "Ela jamais recuperou sua sanidade e morreu pouco tempo depois."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_resurrection_mary",
    category=[store.mas_stories.TYPE_SCARY], prompt="Ressurreição de Mary",unlocked=False),
    code="STY")

label mas_scary_story_resurrection_mary:
    call mas_scary_story_setup
    m 3eua "Em um salão de baile, perto da época de Natal, um jovem chamado Lewis estava se divertindo com seus amigos, quando uma jovem que ele nunca havia visto chamou sua atenção."
    m 1eub "A garota era alta, loira, de olhos azuis e muito bonita."
    m 1hub "Ela estava usando um vestido branco extravagante, com sapatos brancos de dança e um xale fino."
    m 3esb "Lewis achou a garota cativante. Ele decidiu pedir para dançar com ela e ela aceitou o convite."
    m 1eud "Ela certamente era bonita, mas Lewis sentiu que havia algo de estranho nela."
    m 3esd "Enquanto dançavam, ele tentou conhecê-la um pouco melhor, mas tudo que ela dizia sobre si mesma era que seu nome era Mary e que ela era do lado sul da cidade."
    m "Além disso, a pele dela era fria e úmida ao toque. A certa altura da noite, ele beijou Mary, e descobriu que os lábios dela eram tão frios quanto sua pele."
    m 1esb "Os dois passaram a maior parte da noite juntos dançando. Quando chegou a hora de partir, Lewis ofereceu uma carona para Mary e ela novamente aceitou o convite."
    m 3esb "Ela o orientou a dirigir por uma certa estrada e ele obedeceu."
    m 3eud "Enquanto passavam pelos portões de um cemitério, Mary pediu que Lewis parasse."
    m 1eud "Embora perplexo, Lewis parou o carro como ela pediu."
    m 3eud "Ela então abriu a porta, inclinou-se na direção de Lewis e sussurrou que precisava ir e que ele não poderia ir com ela."
    m 1euc "Ela saiu do carro e caminhou em direção ao portão do cemitério, antes de desaparecer."
    m "Lewis ficou sentado no carro por um longo tempo, confuso com o que acabara de acontecer."
    m 1esd "Ele nunca mais viu a linda mulher."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,20) == 1) or mas_full_scares:
        play sound "sfx/giggle.ogg"
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_corpse",
    category=[store.mas_stories.TYPE_SCARY], prompt="O cadáver ressuscitado",unlocked=False),
    code="STY")

label mas_scary_story_corpse:
    call mas_scary_story_setup
    m 1esa "Uma vez havia um homem idoso que cuidava de uma velha pousada na beira da estrada. Uma noite, 4 homens chegaram e pediram um quarto."
    m 3eua "O velho respondeu que todos os quartos estavam ocupados, mas poderia encontrar um lugar para eles dormirem se não fossem muito exigentes."
    m 1esa "Os homens estavam exaustos e asseguraram ao homem que qualquer lugar serviria."
    m 1eud "Ele os levou para um quarto na parte de trás. Deitado no canto do quarto estava o cadáver de uma mulher."
    m "Ele explicou que sua nora havia morrido recentemente e que estava esperando o enterro."
    m 1eua "Depois que o velho partiu, 3 dos 4 homens adormeceram. O último homem não conseguiu dormir."
    m 1wuo "De repente, o homem ouviu um rangido."
    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,2) == 1) or mas_full_scares:
        play sound "sfx/crack.ogg"
    m 3wuo "Ele olhou para cima e, à luz da lâmpada, viu a mulher se erguer, agora com presas e unhas que pareciam garras, avançando em direção a eles."
    m "Ela se abaixou e mordeu cada um dos homens que estavam dormindo. O quarto homem, no último segundo, colocou um travesseiro na frente de seu pescoço."
    m 1eud "A mulher mordeu o travesseiro e, aparentemente, sem perceber que não havia mordido o último homem, retornou ao seu local de repouso original."
    m 3eud "O homem chutou seus companheiros, mas nenhum deles se moveu. O homem decidiu se arriscar e fugir."
    m 3wuo "No entanto, assim que seus pés tocaram o chão, ele ouviu outro rangido."
    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,2) == 1) or mas_full_scares:
        play sound "sfx/crack.ogg"
    m "Percebendo que a mulher estava novamente se levantando, ele abriu a porta e correu o mais rápido que pôde."

    show layer master at heartbeat2(1)
    show vignette as flicker zorder 72 at vignetteflicker(0)
    play sound hb loop
    m 3eud "Após uma curta distância, ele olhou para trás e viu que o cadáver não estava muito longe dele."
    m 3wud "Uma perseguição ocorreu e, quando ela o alcançou, ele estava parado sob uma árvore."
    m "Ela investiu contra ele com as unhas em forma de garra estendidas."
    m 4wud "No último segundo, o homem se esquivou e ela atingiu a árvore com grande ferocidade."
    m 3wud "As unhas dela agora estavam profundamente cravadas na árvore."
    m 1wud "Ela descontroladamente balançou sua mão livre na direção do homem enquanto ele estava deitado no chão, incapaz de alcançá-lo."
    m 1eud "O homem, assustado e exausto, se arrastou por uma curta distância e depois desmaiou."
    show layer master
    stop sound
    hide flicker
    show black zorder 100
    $ pause(2.5)
    hide black
    m 1esd "Na manhã seguinte, um policial que passava encontrou o homem e o acordou."
    m "O homem contou o que aconteceu. O oficial, pensando que o homem estava bêbado, o levou de volta para a pousada."
    m 1eud "Ao chegarem, uma grande agitação estava ocorrendo na pousada."
    m 3eud "Os 3 viajantes foram encontrados mortos em suas camas."
    m "O corpo da nora estava deitado onde estivera na noite anterior, mas agora suas roupas estavam sujas de sangue e um pedaço de casca de árvore foi encontrado sob a unha dela."
    m 3esd "Após algumas perguntas, o dono finalmente admitiu que a mulher havia morrido seis meses antes e estava tentando guardar dinheiro para dar a ela um enterro apropriado."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_jack_o_lantern",
    category=[store.mas_stories.TYPE_SCARY], prompt="Jack O' Lantern",unlocked=False),
    code="STY")

label mas_scary_story_jack_o_lantern:
    call mas_scary_story_setup

    $ _mas_jack_scare = (persistent._mas_pm_likes_spoops and renpy.random.randint(1,4) == 1) or mas_full_scares
    m 4esd "Antigamente havia um homem chamado Jack. Jack era um velho bêbado miserável que gostava de enganar as pessoas."
    m 3esa "Uma noite, Jack se encontrou com o Diabo e o convidou para tomar uma bebida com ele."
    m "Após Jack ter terminado, ele se virou para o Diabo e pediu que ele se transformasse em uma moeda para poder pagar pelas bebidas, já que ele não tinha dinheiro."
    m 1esa "Assim que o Diabo fez isso, Jack guardou a moeda no bolso e saiu sem pagar."
    m "O Diabo não podia voltar à sua forma original porque Jack colocou a moeda no bolso ao lado de uma cruz de prata."
    m 3esa "Jack finalmente libertou o Diabo, sob a condição de que ele não incomodaria Jack por um ano e que, se Jack morresse, ele não reivindicaria sua alma."
    m "No ano seguinte, Jack se encontrou com o Diabo novamente. Desta vez, ele o enganou a subir em uma árvore para pegar uma fruta."
    m 3esd "Enquanto ele estava na árvore, Jack a cercou com cruzes brancas para que o Diabo não pudesse descer."
    m "Assim que o Diabo prometeu não incomodá-lo novamente por mais 10 anos, Jack as removeu. Quando Jack morreu, ele foi para o Céu."
    m 1eud "Quando ele chegou, disseram que ele não poderia entrar por causa da forma que havia vivido sua vida na Terra."
    m 1eua "Então, ele foi ao inferno, onde o Diabo manteve sua promessa e não permitiu que Jack entrasse."
    m 1eud "Jack ficou com medo, pois não tinha para onde ir."
    m 1esd "Jack perguntou ao Diabo como poderia sair, pois não havia luz."
    if _mas_jack_scare:
        hide vignette
        show darkred zorder 82:
            alpha 0.85
    m 1eud "O Diabo jogou para Jack uma brasa das chamas do Inferno para ajudar ele a iluminar seu caminho."
    m "Jack pegou um nabo que tinha com ele, o esculpiu e colocou a brasa dentro dele."
    m 3eua "Daquele dia em diante, Jack percorreu a terra sem um lugar de descanso, iluminando o caminho com sua lanterna."
    if _mas_jack_scare:
        hide darkred
        show vignette zorder 70
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_baobhan_sith",
    category=[store.mas_stories.TYPE_SCARY], prompt="Baobhan Sith",unlocked=False),
    code="STY")

label mas_scary_story_baobhan_sith:
    call mas_scary_story_setup
    m 1esa "Havia um grupo de jovens caçadores que parou durante a noite em uma pequena cabana de caça."
    m 3esb "Quando os homens se instalaram, eles fizeram uma fogueira e começaram a comer e beber alegremente, pois tinha sido um bom dia."
    m 1tku "Eles disseram a si mesmos que a única coisa que lhes faltava era a companhia de algumas belas mulheres."
    m 1tsb "Não muito tempo depois que eles disseram isso, ouviram uma batida na porta."
    m 3eub "Paradas na porta, haviam quatro mulheres lindas."
    m "As mulheres, tendo se perdido na selva, perguntaram se poderiam se juntar aos homens em seu abrigo durante à noite."
    m 1tku "Os homens, silenciosamente comemorando a sorte que tiveram, convidaram as mulheres para entrar."
    m 1esa "Depois de algum tempo desfrutando da companhia uns dos outros, as mulheres expressaram o desejo de dançar."
    m 1tku "Os homens não perderam tempo em se juntarem a cada uma das moças."
    m 1eub "Enquanto dançavam, um dos homens percebeu que os outros casais estavam dançando de maneira estranha."
    m 1wuo "Então, para seu horror, ele percebeu que sangue estava escorregando dos pescoços dos outros homens."
    m 3wuo "Em pânico, o homem abandonou seus parceiros e fugiu porta afora, antes que pudesse compartilhar o destino de seus amigos."
    m 3wud "Ele correu para a floresta e se escondeu entre os cavalos que ele e seus amigos haviam cavalgado durante a caçada daquele dia."
    m "As mulheres, não muito longe dele, se aproximaram, mas pareciam incapazes de passar pelos cavalos em direção ao homem."
    m 1eud "Então lá ele ficou, com os olhos cansados, entre os animais a noite toda, enquanto elas circulavam os cavalos, tentando encontrar um jeito de chegar até ele."
    m 1esa "Pouco antes do amanhecer, as mulheres desistiram e recuaram para a floresta."
    m 1esd "Agora sozinho, o homem cautelosamente voltou para a cabana de caça, sem ouvir nenhum som vindo lá de dentro."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,14) == 1) or mas_full_scares:
        play sound "sfx/stab.ogg"
        show blood splatter1 as bl2 zorder 73:
            pos (50,95)
        show blood splatter1 as bl3 zorder 73:
            pos (170,695)
        show blood splatter1 as bl4 zorder 73:
            pos (150,395)
        show blood splatter1 as bl5 zorder 73:
            pos (950,505)
        show blood splatter1 as bl6 zorder 73:
            pos (700,795)
        show blood splatter1 as bl7 zorder 73:
            pos (1050,95)
        $ pause(1.5)
        stop sound
        hide bl2
        hide bl3
        hide bl4
        hide bl5
        hide bl6
        hide bl7
    m 3wuo "Quando ele olhou lá dentro, viu seus três companheiros mortos no chão, suas peles quase transparente, deitados em uma poça de seus próprios sangues."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_serial_killer",
    category=[store.mas_stories.TYPE_SCARY], prompt="O assassino em série",unlocked=False),
    code="STY")

label mas_scary_story_serial_killer:
    call mas_scary_story_setup
    m 3tub "Uma noite, um jovem casal estacionou seu carro ao lado de um grande carvalho em um cemitério para 'fazer amor' sem serem perturbados."
    m 3euc "Após um tempo, eles foram interrompidos por um relatório de rádio que um famoso assassino em série havia escapado de um hospital psiquiátrico próximo."
    m "Preocupados com sua segurança, decidiram continuar em outro lugar."
    m 1esc "No entanto...{w=0.3} o carro não queria ligar."
    m 3esd "O jovem saiu do carro para procurar ajuda e disse para a garota ficar dentro dele com as portas trancadas."
    m 3wud "Alguns momentos depois, ela ficou surpresa quando ouviu um som estridente no teto do carro."
    m 1eud "Ela pensou consigo mesma que deveria ter sido um galho de uma árvore balançando com o vento."
    m 1euc "Após um longo tempo, um carro da polícia passou por perto e parou, mas ainda não havia nenhum sinal do seu namorado."
    m 1eud "O policial foi até o carro e instruiu a garota a sair do veículo e caminhar na direção dele, sem olhar para trás."
    m "Ela fez isso devagar..."
    m 1ekc "A garota então notou vários outros carros da polícia chegando com suas sirenes ligadas."
    m 1dsd "Tomada pela curiosidade, ela se virou para olhar para o carro..."
    m 4wfw "Ela viu o seu namorado de cabeça para baixo, pendurado na árvore acima do carro com o pescoço aberto..."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,8) == 1) or mas_full_scares:
        show y_sticker hopg zorder 74:
            pos (600,425)
            alpha 1.0
            linear 1.6 alpha 0
        play sound "<from 0.4 to 2.0 >sfx/eyes.ogg"
    m 1dfc "...e as unhas quebradas e ensanguentadas no telhado."
    hide y_sticker
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_revenant",
    category=[store.mas_stories.TYPE_SCARY], prompt="O Espectro",unlocked=False),
    code="STY")

label mas_scary_story_revenant:
    call mas_scary_story_setup
    m 4eua "Havia um homem que se casou com uma mulher."
    m 4ekd "Ele era uma pessoa rica que ganhava dinheiro através de meios ilícitos."
    m 2eud "Pouco depois de seu casamento, ele começou a ouvir rumores de que sua esposa estava sendo infiel."
    m 2esd "Ansioso para descobrir a verdade, o homem disse a sua esposa que estava indo em uma viagem de negócios por alguns dias e saiu de casa."
    m 2eud "Sem o conhecimento de sua esposa, o homem voltou para casa no final da tarde com a ajuda de um de seus servos."
    m "O homem subiu uma das vigas em seu quarto e ficou à espera."
    m 4ekd "Pouco depois, sua esposa entrou com um homem do bairro, os dois conversaram por um tempo e depois começaram a se despir."
    m 4eud "O homem, nesta hora, desajeitadamente caiu no chão, não muito longe de onde os dois estavam, inconsciente."
    m "O adúltero pegou suas roupas e fugiu, mas a esposa se aproximou do marido e gentilmente acariciou seus cabelos até que ele acordasse."
    m "O homem castigou sua esposa por seu adultério e ameaçou a punir assim que se recuperasse da queda."
    m 2dsc "No entanto, o homem nunca se recuperou da queda e morreu durante a noite. Ele foi enterrado no dia seguinte."
    m 2esd "Naquela noite, o cadáver do homem se levantou do túmulo e começou a vagar pelo bairro."
    m "Quando amanheceu, ele retornou ao túmulo."
    m 3esd "Isto continuou noite após noite e as pessoas começaram a trancar suas portas, temendo sair para fazer qualquer coisa após o pôr-do-sol."
    m "Com medo que acabassem se encontrando com a criatura e fossem espancadas."
    m 2dsd "Pouco tempo depois, a cidade se tornou assolada por doenças e não havia dúvidas de que o cadáver era o culpado."
    m 2dsc "As pessoas começaram a fugir da cidade, com medo de também morrerem pela doença."
    m 2esd "Conforme a cidade estava se desfazendo, uma reunião foi realizada e decidiram que o cadáver deveria ser desenterrado e eliminado."
    m "Um grupo de pessoas levaram pás e encontraram o cemitério em que o homem havia sido enterrado."
    m "Eles não precisaram cavar muito antes de encontrarem o cadáver do homem."
    m 4eud "Quando ele foi totalmente desenterrado, os aldeões espancaram a carcaça com suas pás e arrastaram o corpo para fora da cidade."
    m 3esd "Lá, eles fizeram uma enorme fogueira e jogaram o corpo no fogo."
    m 3eub "O cadáver do homem soltou um grito de gelar o sangue e tentou se arrastar para fora das chamas, antes de finalmente sucumbir a ela."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_yuki_onna",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Yuki-onna",
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_yuki_onna:
    call mas_scary_story_setup
    m 4eud "Havia dois lenhadores, um pai e um filho, os quais estavam a caminho de casa quando uma nevasca surgiu de repente."
    m "Após um tempo de viagem, eles se depararam com uma cabana abandonada e se abrigaram nela."
    m 2eua "Eles foram capazes de fazerem uma pequena fogueira e se deitaram juntos para se aquecerem antes de dormirem."
    m 2esd "No meio da noite, o filho acordou com um empurrão."
    m 2wud "Para sua surpresa, uma linda mulher estava em pé sobre seu pai, soltando seu fôlego nele e instantaneamente o congelando."
    m 4wud "Ao se virar para o filho, ela parou. A mulher disse a ele que o pouparia do mesmo destino, pois ele era jovem e muito bonito."
    m 4ekc "Se ele algum dia falasse sobre isso para alguém, ela voltaria para matá-lo."
    m 4esa "No inverno seguinte, o jovem estava a caminho de casa depois de um dia cortando madeira, quando se deparou com uma bela mulher viajante."
    m 2eua "Estava começando a nevar, e o homem ofereceu abrigo à mulher contra a tempestade, e ela aceitou."
    m 2eua "Os dois rapidamente se apaixonaram e acabaram se casando."
    m 2hua "Eles viveram felizes por anos e tiveram vários filhos com o passar do tempo."
    m 2esa "Uma noite, enquanto as crianças dormiam, a mulher estava costurando à luz do fogo."
    m 2eud "O homem ergueu os olhos, parando o que estava fazendo, e a lembrança da noite da qual ele nunca deveria falar voltou para ele."
    m "A esposa perguntou ao homem porque ele estava olhando para ela daquele jeito."
    m 3esc "O homem contou a história de seu encontro com a mulher da neve."
    m 2wud "O sorriso no rosto de sua esposa se transformou em raiva quando ela revelou que ela era a mulher da neve de quem ele falava."
    m 4efc "Ela o repreendeu por quebrar sua promessa e teria o matado se não fosse pelos seus filhos."
    m 4efd "Ela disse ao homem que era melhor ele cuidar bem dos filhos ou ela voltaria para lidar com ele."
    m 4dsd "No instante seguinte, ela desapareceu, para nunca mais ser vista."
    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,3) == 1) or mas_full_scares:
        hide monika
        play sound "sfx/giggle.ogg"
        pause 1.0
        show black zorder 100
        show monika zorder MAS_MONIKA_Z at i11
        $ pause(1.5)
        hide black
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_many_loves",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Muitos Amores",
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_many_loves:
    call mas_scary_story_setup
    m 4esa "Era uma vez uma jovem que um dia apareceu em uma aldeia procurando por um marido."
    m 4eua "Ela era muito bonita e rapidamente atraiu muitos pretendentes."
    m 2eua "Eventualmente se casando com um pescador rouco."
    m 2esd "Os dois tiveram um casamento feliz, mas em menos de um ano o marido acabou morrendo."
    m "As pessoas na aldeia sentiram pena da jovem mulher e a consolaram o melhor que puderam."
    m 4esa "Alguns meses depois, a mulher se casou com um forte lenhador."
    m 4dsd "Os dois viveram felizes juntos por um tempo, mas ele também acabou morrendo."
    m 4eud "Alguns dos aldeões achavam que era estranho que ambos os maridos tivessem morrido da mesma forma, mas ninguém disse nada, e consolaram a garota por sua má sorte."
    m 2esc "Um tempo depois, a mulher se casou novamente, desta vez com um pedreiro robusto, e eles também pareciam ser felizes, mas dentro de um ano, a mulher voltou a ser viúva."
    m "Desta vez, os aldeões conversaram entre si e sentiram que algo suspeito estava acontecendo, então um grupo de aldeões partiu para encontrar o xamã mais próximo."
    m "Assim que encontraram o xamã e contaram sua história, o xamã indicou que sabia o que estava acontecendo."
    m 3euc "Ele chamou o seu assistente, um rapaz jovem e forte, sussurrou em seu ouvido e o mandou voltar com os aldeões."
    m "Dizendo a eles para não se preocuparem, que seu assistente resolveria isso."
    m 2esc "Quando voltaram para a aldeia, o assistente chamou a viúva e pouco tempo depois eles se casaram."
    m 2efc "Na noite do casamento, o assistente colocou uma faca debaixo do travesseiro e fingiu dormir."
    m 2esd "Um pouco depois da meia-noite, o homem sentiu uma presença sobre ele e uma picada em seu pescoço."
    m 2dfc "O homem agarrou a faca e golpeou o vulto que estava sobre ele."
    if (renpy.random.randint(1,20) == 1 and persistent._mas_pm_likes_spoops) or mas_full_scares:
        show monika 6ckc
        show mas_stab_wound zorder 75
        play sound "sfx/stab.ogg"
        show blood splatter1 as bl2 zorder 73:
            pos (590,485)
        $ pause(1.5)
        stop sound
        hide bl2
        hide mas_stab_wound
        show black zorder 100
        $ pause(1.5)
        hide black
    m 3wfc "Ele ouviu um grito e o bater de asas quando a criatura voou pela janela."
    m 1dfc "No dia seguinte, a noiva foi encontrada morta perto da casa com um ferimento de faca no peito."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_gray_lady",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="A Dama Cinzenta",
            unlocked=False
        ),
    code="STY"
    )

label mas_scary_story_gray_lady:
    call mas_scary_story_setup
    m 4eua "Antigamente havia um homem chamado William, o qual cresceu ajudando seu pai com suas façanhas nefastas."
    m 4ekd "Como acender luzes na costa durante a calada da noite, na esperança de fazer navios se chocarem contra as rochas traiçoeiras ao longo da costa."
    m 2ekc "E depois recolher o saque que caiu do navio e matar todos os sobreviventes."
    m 2eud "Durante uma das expedições de seu pai, ele salvou uma mulher bonita e acabou decidindo deixar sua antiga vida para trás e se casar com ela."
    m 2esa "O casal alugou uma mansão não muito longe dali."
    m 2hub "Os dois tiveram uma vida feliz, mas ficaram ainda mais felizes quando sua filha Kate nasceu."
    m 4esa "Com o passar dos anos, Kate se tornou uma jovem animada."
    m 2ekc "William estava secretamente envergonhado por não ter dinheiro o suficiente para comprar a mansão para oferecer como dote ao homem que se casaria com sua filha."
    m 4hub "Então, um dia, Kate conheceu e se apaixonou por um capitão pirata irlandês e os dois se casaram."
    m 4esb "O casal feliz decidiu morar em Dublin, já que os pais de Kate não tinham terras para oferecer a eles."
    m 4eua "Kate prometeu voltar e visitar seus pais novamente um dia."
    m 4esd "O tempo passou e William e sua esposa sentiram falta da filha e desejaram que ela voltasse."
    m 2dkc "William decidiu retornar aos seus velhos hábitos só para conseguir o dinheiro necessário para comprar a mansão e convidar a filha e o marido para morar com eles."
    m 4wud "Uma noite, após fazer um navio bater na costa e recolher o saque, ele notou uma mulher gravemente ferida deitada nas rochas diante dele."
    m 2wuc "Seus traços faciais ficaram irreconhecíveis devido aos ferimentos que ela sofreu."
    m 2ekc "William, tendo pena dela, a levou de volta à sua mansão e fez o que pôde para tentar salvar sua vida, mas a mulher morreu sem recuperar a consciência."
    m 2eud "Enquanto procurava no corpo dela alguma pista sobre sua identidade, encontrou uma pequena bolsa amarrada a sua cintura, cheia de moedas e joias de ouro, o bastante para finalmente comprar a mansão."
    m 2dsc "Poucos dias depois, o Almirante questionou o casal sobre uma passageira desaparecida dos destroços, a qual era ninguém menos do que a filha deles."
    m 3dsd "Devastados e envergonhados, os pais emparedaram os restos mortais dela em uma sala secreta e se foram embora, para nunca mais voltar."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_flowered_lantern",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="A Lanterna Florida",
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_flowered_lantern:
    call mas_scary_story_setup

    if not mas_getEVL_shown_count("mas_scary_story_flowered_lantern"):
        m 3eub "Antes de começarmos, preciso dizer que minha próxima história será um pouco longa."
        m 3eua "Então eu vou a dividir em partes."
        m "Assim que eu terminar esta parte, perguntarei se você quer continuar ou não."
        m 1eub "Se você disser não, pode me pedir mais tarde para contar a próxima parte, então não se preocupe com isso."
        m 4hua "Certo, vamos começar."

    m 4eua "Antigamente havia uma jovem moça chamada Tsuyu, cujo pai era um samurai de alta patente."
    m 4eud "A mãe de Tsuyu estava morta e seu pai acabou se casando novamente."
    m 2euc "Embora estivesse óbvio para o pai de Tsuyu que ela e sua madrasta não iriam se dar bem."
    m 2esa "Querendo garantir a felicidade de sua única filha, ele construiu uma casa luxuosa para ela, longe deles, e fez com que ela se mudasse para lá."
    m "Um dia, o médico da família foi até a residência de Tsuyu em uma visita de rotina, acompanhado de um jovem samurai chamado Hagiwara, o qual era muito bonito."
    m 4eub "Tsuyu e Hagiwara se apaixonaram no momento em que se viram."
    m 4esc "Sem o conhecimento do médico, os dois juraram ficarem juntos por toda a vida, e antes que os dois partissem..."
    m 4dsd "Tsuyu sussurrou para Hagiwara que ela com certeza morreria se ele não voltasse para vê-la."
    m 2esc "Hagiwara não se esqueceu das palavras dela, mas a etiqueta proibia que ele fosse visitar uma donzela sozinho, então teve que esperar que o médico lhe pedisse para o acompanhar."
    m 2dsd "O médico, no entanto, percebeu sua afeição repentina por Tsuyu."
    m 4ekc "O pai de Tsuyu era conhecido por decapitar aqueles que o irritavam, e temendo que ele fosse responsabilizado por ter apresentado os dois, ele ignorou Hagiwara."
    m 2rkc "Meses se passaram, e Tsuyu, sentindo que Hagiwara havia a abandonado, faleceu."
    m 1ekc "Pouco tempo depois, o médico se encontrou com Hagiwara, o informando da morte de Tsuyu."
    m 1dsd "Hagiwara ficou profundamente entristecido e lamentou muito por ela, fazendo orações e queimando incenso por ela."

    $ mas_setEVLPropValues("mas_scary_story_flowered_lantern_2", unlocked=True, pool=False)

    m 1hua "...E essa foi a primeira parte! Você quer continuar para a próxima?{nw}"
    $ _history_list.pop()
    menu:
        m "...E essa foi a primeira parte! Você quer continuar para a próxima?{fast}"
        "Sim.":
            jump mas_scary_story_flowered_lantern_2
        "Não.":
            pass
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_flowered_lantern_2",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="A Lanterna Florida 2",
            pool=True,
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_flowered_lantern_2:
    call mas_scary_story_setup
    $ _mas_lantern_scare = renpy.random.randint(1,11) == 1
    m 4ekd "Após o pôr do sol, na primeira noite do festival dos mortos, Hagiwara se sentou do lado de fora, ainda lamentando a perda de seu amor."
    m 2eud "No entanto, quando estava prestes a entrar e ir dormir, ele ouviu passos do lado de fora do seu portão."
    m 4euc "Hagiwara vivia em uma rua solitária com poucos pedestres, e como já era bem tarde, resolveu ir ver quem era."
    m 4wub "Para sua surpresa e deleite, a pessoa caminhando era ninguém menos do que Tsuyu, carregando uma lanterna de papel decorada com flores para iluminar seu caminho."
    m 1hua "Hagiwara chamou o nome de Tsuyu e ela imediatamente veio até ele e o abraçou."
    m 1eua "Ambos disseram que o médio haviam os informado que o outro havia morrido."
    m "Tsuyu disse a ele que seu pai queria que ela se casasse com outro homem."
    m 3eub "Ela se recusou e fugiu de sua luxuosa casa para se esconder dele, e estava atualmente morando em uma pequena casa em um bairro próximo."
    m 3eua "Ele a convidou para entrar, mas disse a ela para ficar quieta para que não perturbassem seu servo, o qual poderia perguntar quem era ela."
    m 4eua "Os dois passaram a noite juntos e logo antes do amanhecer, Tsuyu saiu para retornar à sua casa."
    m 4esa "Na noite seguinte, Tsuyu o visitou novamente no mesmo horário em que ela havia chegado na noite anterior."
    m 2euc "Desta vez, no entanto, o servo de Hagiwara acordou e ouviu a voz de uma jovem que ele não reconheceu."
    m 4esd "Curioso, mas não querendo perturbar seu mestre, ele se esgueirou até o quarto de seu mestre e espiou por uma fenda na porta, e viu que ele estava conversando com uma jovem mulher."
    m 4eud "A mulher estava de costas para ele, mas ele foi capaz de perceber que ela era muito magra e vestia um quimono muito elegante que só a classe alta usava."
    m 4esc "Sua curiosidade despertou, o criado decidiu dar uma olhada no rosto dessa garota antes de sair."
    m 2dsc "Ele viu que o mestre havia deixado uma janela aberta, então ele silenciosamente foi até lá."
    m 4wuw "Ao olhar para dentro do quarto, ele viu com horror que o rosto da mulher estava apodrecido há muito tempo e os dedos acariciando o rosto de seu mestre eram apenas ossos."
    m 2wfd "Ele fugiu aterrorizado, sem dar um pio."
    m 1efc "Na manhã seguinte, o servo foi até seu mestre e perguntou a ele sobre a mulher."
    m 4efd "A princípio, Hagiwara negou ter tido uma visitante, mas depois de perceber que não adiantaria, confessou tudo o que havia acontecido."
    m 4ekc "O servo contou a Hagiwara o que ele viu na noite anterior e sentiu que a vida de seu mestre estava em perigo, implorando para que ele visitasse um sacerdote."
    m 2euc "Assustado, mas não totalmente convencido, Hagiwara decidiu acalmar seu servo encontrando a residência de Tsuyu."
    m "Hagiwara partiu e explorou o bairro onde Tsuyu havia dito que morava."
    m 2esc "Ele olhou em volta e perguntou às pessoas sobre ela, mas não encontrou nada."
    m 4dsd "Quando ele decidiu que continuar procurar seria inútil, ele voltou para casa."
    m 4eud "No caminho de volta, ele passou por um cemitério ao lado de um templo."
    m "Sua atenção foi atraída por um enorme túmulo novo que ele ainda não havia notado chamou sua atenção."
    if _mas_lantern_scare or persistent._mas_pm_likes_spoops or mas_full_scares:
        show mas_lantern zorder 75 at right
    m 4euc "Pendurado acima dele, havia uma lanterna de papel decorada com lindas flores que parecia exatamente a mesma que Tsuyu carregava de noite."
    m 4wuc "Intrigado, ele caminhou até o túmulo. Ele pulou de susto ao ler que pertencia a sua amada Tsuyu."
    m 2wkc "Completamente aterrorizado, Hagiwara imediatamente se dirigiu ao templo próximo e pediu para falar com o sacerdote."
    m 4esc "Quando ele conseguiu falar com o sacerdote, ele contou tudo o que havia acontecido."
    m 4esd "Após ter terminado, o sacerdote disse a ele que sua vida estava realmente em perigo."
    m "O intenso luto de Hagiwara por ela e o intenso amor dela por ele a trouxeram de volta durante o Festival dos Mortos."
    m 4dsc "O amor entre alguém que está vivo e aquele que está morto só pode resultar na morte daquele que está vivo."
    if _mas_lantern_scare or persistent._mas_pm_likes_spoops or mas_full_scares:
        hide mas_lantern

    $ mas_setEVLPropValues("mas_scary_story_flowered_lantern_3", unlocked=True, pool=False)

    m 1hua "...E essa foi a segunda parte! Você quer continuar para a próxima?{nw}"
    $ _history_list.pop()
    menu:
        m "...E essa foi a segunda parte! Você quer continuar para a próxima?{fast}"
        "Sim.":
            jump mas_scary_story_flowered_lantern_3
        "Não.":
            pass
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_flowered_lantern_3",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="A Lanterna Florida 3",
            pool=True,
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_flowered_lantern_3:
    call mas_scary_story_setup
    $ _mas_rects_scare = (renpy.random.randint(1,11) == 1 and persistent._mas_pm_likes_spoops) or mas_full_scares
    m 1eud "Como era o último dia do Festival dos Mortos, Tsuyu teria que retornar aos mortos nesta noite e ela levaria Hagiwara junto se eles se encontrassem novamente."
    m 3esd "Hagiwara implorou ao sacerdote para ajudá-lo."
    m 3esc "O sacerdote disse que o carma passional entre eles era muito forte, mas ainda havia alguma esperança."
    m "Ele entregou a Hagiwara uma pilha de talismãs de papel que afastavam os espíritos, e o instruiu a cobrir todas as aberturas de sua casa, não importando o quão pequenas fossem."
    m 1esd "Tsuyu não poderia entrar na casa desde que ele seguisse essas instruções."
    m 2esa "Hagiwara, com a ajuda de seu servo, foi capaz de cobrir a casa com os talismãs de papel antes do anoitecer."
    m 4esc "Enquanto a noite passava, Hagiwara tentou dormir, mas sem sucesso. Ele então se sentou, meditando sobre os eventos recentes."
    m 2dsd "Quando já era tarde, ele ouviu passos do lado de fora de sua casa."
    m "Os passos ficavam cada vez mais próximos."
    m 4wkc "Hagiwara sentiu uma súbita vontade, mais forte até mesmo que seu medo, de olhar."
    m 4wkd "Ele tolamente se aproximou das persianas e através de uma rachadura viu Tsuyu parada na entrada de sua casa, segurando sua lanterna de papel, olhando para os talismãs de papel."
    m "Nunca antes ele tinha visto Tsuyu tão bonita, e seu coração se sentia tão atraído por ela."
    m 2ekd "Do lado de fora, Tsuyu começou a chorar amargamente, dizendo a si mesma que Hagiwara havia quebrado a promessa que eles fizeram um para o outro."
    m 4eud "Ela chorou até se recompor, e disse em voz alta que não sairia sem vê-lo uma última vez."
    m 4esd "Hagiwara ouviu passos enquanto ela andava em volta da casa dele, de vez em quando vendo a luz da lanterna que ela carregava."
    m 2wud "Quando ela chegou perto do lugar de onde ele estava espiando, os passos pararam, e de repente, Hagiwara viu um dos olhos de Tsuyu o encarando."
    if _mas_rects_scare:
        play sound "sfx/glitch1.ogg"
        show rects_bn1 zorder 80
        show rects_bn2 zorder 80
        show rects_bn3 zorder 80
        pause 0.5
        $ style.say_dialogue = style.edited
        ".{w=0.7}.{w=0.9}.{nw}"
        $ mas_resetTextSpeed()
        stop sound
        hide rects_bn1
        hide rects_bn2
        hide rects_bn3
        show black zorder 100
        $ pause(1.5)
        hide black
    m 2dsc "No dia seguinte, o servo acordou e foi até o quarto de seu mestre, batendo na porta."
    m 4ekc "Pela primeira vez em anos, ele não recebeu uma resposta e ficou preocupado."
    m 2dsd "Ele chamou seu mestre repetidas vezes, mas sem sucesso."
    m 2esc "Finalmente, com um pouco de coragem, ele entrou no quarto de seu mestre."
    m 4wuw "...Ele então saiu correndo da casa gritando por causa do horror que havia visto."
    m "Hagiwara estava morto, horrivelmente morto, e seu rosto estava com uma expressão de extremo medo..."
    m 2wfc "E ao lado dele, na cama, estavam os ossos de uma mulher, com os braços ao redor do pescoço dele, como se estivesse o abraçando."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_prison_escape",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Fuga da Prisão",
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_prison_escape:
    call mas_scary_story_setup
    m 1ekd "Uma mulher bonita estava cumprindo pena de prisão perpétua por assassinato."
    m 2tfc "Irritada e ressentida com sua situação, ela decidiu que não poderia passar a vida na prisão. {w=0.2}Ela começou a planejar maneiras de escapar"
    m 7eua "Com o tempo, ela se tornou uma boa amiga de um dos zeladores da prisão."
    m 3esc "Seu trabalho era enterrar todos os prisioneiros que morriam em um cemitério fora dos muros da prisão."
    m 3esd "Sempre que um preso morria, o zelador tocava uma campainha que era ouvida por todos os presos."
    m 3esc "Em seguida, ele pegou o corpo e colocou-o em um caixão, e depois entrou em seu escritório para preencher o atestado de óbito antes de devolver com pregos a tampa do caixão fechada"
    m 3esd "Finalmente, ele o colocou em uma carroça para levá-lo ao cemitério e enterrá-lo."
    m 1euc "Conhecendo essa rotina, a mulher elaborou um plano de fuga e o compartilhou com o zelador..."
    m 1eud "Na próxima vez que a campainha tocava, a mulher saía de sua cela e se esgueirava para o quarto escuro onde os caixões eram guardados"
    m 1eud "Ela entrava no caixão com o cadáver enquanto o zelador preenchia o atestado de óbito."
    m 3euc "Quando o zelador voltava, ele prendia a tampa e levava o caixão para fora da prisão e o enterrava."
    m 3euc "A mulher sabia que haveria ar suficiente para ela respirar até o final da noite, quando o zelador voltaria sob o manto da escuridão, desenterraria o caixão e a libertaria."
    m 2eksdlc "O zelador estava relutante em seguir este plano, {w=0.1}{nw}"
    extend 4esa "mas desde que ele e a mulher se tornaram bons amigos ao longo dos anos, ele concordou em fazê-lo."
    m 2tsc "A mulher esperou vários meses para que um dos outros presos morresse."
    m 7dsc "Uma noite, ela estava dormindo em sua cela quando ouviu o sino da morte tocar."
    m 3euc "Ela se levantou, abriu a fechadura de sua cela e caminhou lentamente pelo corredor."
    m 3wud "Ela quase foi pega algumas vezes...{w=0.3}eu coração batia tão rápido."
    m 3ekc "Ela abriu a porta do quarto escuro onde os caixões estavam guardados e silenciosamente encontrou aquele que continha o cadáver."
    m 3dkc "Depois de entrar nela com cuidado, ela fechou a tampa para esperar que o zelador viesse e pregasse a tampa."
    m 2eka "Logo ela ouviu passos e o bater do martelo e dos pregos."
    m 4eksdlc "Mesmo que ela estivesse muito desconfortável no caixão com o cadáver debaixo dela, ela sabia que com cada prego ela estava um passo mais perto da liberdade."
    m 2eud "O caixão foi colocado na carroça e levado para o cemitério."
    m 2eksdlc "Ela não fez nenhum som quando o caixão atingiu o fundo da cova com um baque."
    m 4eksdlc "Finalmente ela ouviu a terra caindo em cima do caixão de madeira, {w=0.1}{nw}"
    extend 4eksdla "e ela sabia que era apenas uma questão de tempo até que ela finalmente estivesse livre."
    m 2hksdlb "Depois de uma hora de silêncio absoluto, ela começou a rir baixinho para si mesma."
    m 2eta "Sentindo-se curiosa, ela decidiu acender um fósforo para descobrir a identidade do prisioneiro morto ao seu lado."
    m 2wusdld "...!"
    m 2wusdlo "Era o zelador!"
    call mas_scary_story_cleanup
    return
