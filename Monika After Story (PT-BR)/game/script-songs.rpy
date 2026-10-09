
default persistent._mas_songs_database = dict()
init offset = 5

default -5 persistent._mas_player_derandomed_songs = list()

init -15 python in mas_songs:

    song_db = {}















    TYPE_LONG = "long"
    TYPE_SHORT = "short"
    TYPE_ANALYSIS = "analysis"

init -5 python in mas_songs:
    import store
    def checkRandSongDelegate():
        """
        Handles locking/unlocking of the random song delegate

        Ensures that songs cannot be repeated (derandoms the delegate) if the repeat topics flag is disabled and there's no unseen songs
        And that songs can be repeated if the flag is enabled (re-randoms the delegate)
        """
        
        rand_delegate_ev = store.mas_getEV("monika_sing_song_random")
        
        if rand_delegate_ev:
            
            
            
            
            if (
                rand_delegate_ev.random
                and (
                    (not store.persistent._mas_enable_random_repeats and not hasRandomSongs(unseen_only=True))
                    or not hasRandomSongs()
                )
            ):
                rand_delegate_ev.random = False
            
            
            
            elif (
                not rand_delegate_ev.random
                and (
                    hasRandomSongs(unseen_only=True)
                    or (store.persistent._mas_enable_random_repeats and hasRandomSongs())
                )
            ):
                rand_delegate_ev.random = True

    def getUnlockedSongs(length=None):
        """
        Gets a list of unlocked songs
        IN:
            length - a filter for the type of song we want. "long" for songs of TYPE_LONG
                "short" for TYPE_SHORT or None for all songs. (Default None)

        OUT:
            list of unlocked all songs of the desired length in tuple format for a scrollable menu
        """
        if length is None:
            return [
                (ev.prompt, ev_label, False, False)
                for ev_label, ev in song_db.iteritems()
                if ev.unlocked
            ]
        
        else:
            return [
                (ev.prompt, ev_label, False, False)
                for ev_label, ev in song_db.iteritems()
                if ev.unlocked and length in ev.category
            ]

    def getRandomSongs(unseen_only=False):
        """
        Gets a list of all random songs

        IN:
            unseen_only - Whether or not the list of random songs should contain unseen only songs
            (Default: False)

        OUT: list of all random songs within aff_range
        """
        if unseen_only:
            return [
                ev_label
                for ev_label, ev in song_db.iteritems()
                if (
                    not store.seen_event(ev_label)
                    and ev.random
                    and TYPE_SHORT in ev.category
                    and ev.checkAffection(store.mas_curr_affection)
                )
            ]
        
        return [
            ev_label
            for ev_label, ev in song_db.iteritems()
            if ev.random and TYPE_SHORT in ev.category and ev.checkAffection(store.mas_curr_affection)
        ]

    def checkSongAnalysisDelegate(curr_aff=None):
        """
        Checks to see if the song analysis topic should be unlocked or locked and does the appropriate action

        IN:
            curr_aff - Affection level to ev.checkAffection with. If none, mas_curr_affection is assumed
                (Default: None)
        """
        if hasUnlockedSongAnalyses(curr_aff):
            store.mas_unlockEVL("monika_sing_song_analysis", "EVE")
        else:
            store.mas_lockEVL("monika_sing_song_analysis", "EVE")

    def getUnlockedSongAnalyses(curr_aff=None):
        """
        Gets a list of all song analysis evs in scrollable menu format

        IN:
            curr_aff - Affection level to ev.checkAffection with. If none, mas_curr_affection is assumed
                (Default: None)

        OUT:
            List of unlocked song analysis topics in mas_gen_scrollable_menu format
        """
        if curr_aff is None:
            curr_aff = store.mas_curr_affection
        
        return [
            (ev.prompt, ev_label, False, False)
            for ev_label, ev in song_db.iteritems()
            if ev.unlocked and TYPE_ANALYSIS in ev.category and ev.checkAffection(curr_aff)
        ]

    def hasUnlockedSongAnalyses(curr_aff=None):
        """
        Checks if there's any unlocked song analysis topics available

        IN:
            curr_aff - Affection level to ev.checkAffection with. If none, mas_curr_affection is assumed
                (Default: None)
        OUT:
            boolean:
                True if we have unlocked song analyses
                False otherwise
        """
        return len(getUnlockedSongAnalyses(curr_aff)) > 0

    def hasUnlockedSongs(length=None):
        """
        Checks if the player has unlocked a song at any point via the random selection

        IN:
            length - a filter for the type of song we want. "long" for songs of TYPE_LONG
                "short" for TYPE_SHORT or None for all songs. (Default None)

        OUT:
            True if there's an unlocked song, False otherwise
        """
        return len(getUnlockedSongs(length)) > 0

    def hasRandomSongs(unseen_only=False):
        """
        Checks if there are any songs with the random property

        IN:
            unseen_only - Whether or not we should check for only unseen songs
        OUT:
            True if there are songs which are random, False otherwise
        """
        return len(getRandomSongs(unseen_only)) > 0

    def getPromptSuffix(ev):
        """
        Gets the suffix for songs to display in the bookmarks menu

        IN:
            ev - event object to get the prompt suffix for

        OUT:
            Suffix for song prompt

        ASSUMES:
            - ev.category isn't an empty list
            - ev.category contains only one type
        """
        prompt_suffix_map = {
            TYPE_SHORT: " (Short)",
            TYPE_LONG: " (Long)",
            TYPE_ANALYSIS: " (Analysis)"
        }
        return prompt_suffix_map.get(ev.category[0], "")



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_pool",
            prompt="Você pode cantar uma canção para mim?",
            category=["música"],
            pool=True,
            aff_range=(mas_aff.NORMAL,None),
            rules={"no_unlock": None}
        )
    )

label monika_sing_song_pool:

    $ song_length = "curta"

    $ have_both_types = False

    $ switch_str = "longa"

    $ end = ""

    show monika 1eua at t21

    if mas_songs.hasUnlockedSongs(length="long") and mas_songs.hasUnlockedSongs(length="short"):
        $ have_both_types = True



label monika_sing_song_pool_menu:
    python:
        if have_both_types:
            space = 0
        else:
            space = 20

        ret_back = ("Esqueça", False, False, False, space)
        switch = ("Gostaria de ouvir uma canção [switch_str] em vez disso", "monika_sing_song_pool_menu", False, False, 20)

        unlocked_song_list = mas_songs.getUnlockedSongs(length=song_length)
        unlocked_song_list.sort()

        if mas_isO31():
            which = "Qual"
        else:
            which = "Qual"

        renpy.say(m, "[which] canção você gostaria que eu cantasse?[end]", interact=False)

    if have_both_types:
        call screen mas_gen_scrollable_menu(unlocked_song_list, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, switch, ret_back)
    else:
        call screen mas_gen_scrollable_menu(unlocked_song_list, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ret_back)

    $ sel_song = _return

    if sel_song:
        if sel_song == "monika_sing_song_pool_menu":
            if song_length == "short":
                $ song_length = "long"
                $ switch_str = "Curta"
            else:

                $ song_length = "short"
                $ switch_str = "longa"

            $ end = "{fast}"
            $ _history_list.pop()
            jump monika_sing_song_pool_menu
        else:

            $ MASEventList.push(sel_song, skipeval=True)
            show monika at t11
            m 3hub "Certo!"
    else:

        return "prompt"

    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_analysis",
            prompt="Vamos falar sobre uma musica",
            category=["música"],
            pool=True,
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None),
            rules={"no_unlock": None}
        )
    )

label monika_sing_song_analysis:
    python:
        ret_back = ("Esqueça.", False, False, False, 20)

        unlocked_analyses = mas_songs.getUnlockedSongAnalyses()

        if mas_isO31():
            which = "Qual"
        else:
            which = "Qual"

    show monika 1eua at t21
    $ renpy.say(m, "[which] música você gostaria de falar?", interact=False)

    call screen mas_gen_scrollable_menu(unlocked_analyses, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ret_back)

    $ sel_analysis = _return

    if sel_analysis:
        $ MASEventList.push(sel_analysis, skipeval=True)
        show monika at t11
        m 3hub "Tudo bem!"
    else:

        return "prompt"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_sing_song_rerandom",
            prompt="Você pode cantar uma música sozinha de novo?",
            category=['música'],
            pool=True,
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None),
            rules={"no_unlock": None}
        )
    )

label mas_sing_song_rerandom:
    python:
        mas_bookmarks_derand.initial_ask_text_multiple = "Qual música você quer que eu cante de vez em quando?"
        mas_bookmarks_derand.initial_ask_text_one = "Se quiser que eu volte a cantar essa música de vez em quando, é só escolher, [player]."
        mas_bookmarks_derand.caller_label = "mas_sing_song_rerandom"
        mas_bookmarks_derand.persist_var = persistent._mas_player_derandomed_songs

    call mas_rerandom
    return _return

label mas_song_derandom:
    $ prev_topic = persistent.flagged_monikatopic
    m 1eka "Cansou de me ouvir cantando essa música, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Cansou de me ouvir cantando essa música, [player]?{fast}"
        "Um pouco.":

            m 1eka "Tudo bem."
            m 1eua "Só vou cantar quando você quiser, então. É só me avisar se quiser ouvir de novo."
            python:
                mas_hideEVL(prev_topic, "SNG", derandom=True)
                persistent._mas_player_derandomed_songs.append(prev_topic)
                mas_unlockEVL("mas_sing_song_rerandom", "EVE")
        "Tudo certo.":

            m 1eua "Tudo bem, [player]."
    return



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_random",
            random=True,
            unlocked=False,
            rules={"skip alert": None,"force repeat": None}
        )
    )

label monika_sing_song_random:




    if (
        (persistent._mas_enable_random_repeats and mas_songs.hasRandomSongs())
        or (not persistent._mas_enable_random_repeats and mas_songs.hasRandomSongs(unseen_only=True))
    ):
        python:

            random_unseen_songs = mas_songs.getRandomSongs(unseen_only=True)


            if random_unseen_songs:
                rand_song = random.choice(random_unseen_songs)


            else:
                rand_song = random.choice(mas_songs.getRandomSongs())


            mas_unlockEVL("monika_sing_song_pool", "EVE")


            MASEventList.push(rand_song, skipeval=True, notify=True)
            mas_unlockEVL(rand_song, "SNG")


            mas_unlockEVL(rand_song + "_long", "SNG")


            mas_unlockEVL(rand_song + "_analysis", "SNG")


            if store.mas_songs.hasUnlockedSongAnalyses():
                mas_unlockEVL("monika_sing_song_analysis", "EVE")
    else:


        $ mas_assignModifyEVLPropValue("monika_sing_song_random", "shown_count", "-=", 1)
        return "derandom|no_unlock"
    return "no_unlock"



init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_aiwfc",
            prompt="Tudo o que eu quero no Natal",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="SNG"
    )

label mas_song_aiwfc:
    if store.songs.hasMusicMuted():
        m 3eua "Não se esqueça de aumentar o volume do jogo, [mas_get_player_nickname()]."

    call monika_aiwfc_song

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_merry_christmas_baby",
            prompt="Feliz Natal, meu amor",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="SNG"
    )

label mas_song_merry_christmas_baby:
    m 1hub "{i}~Feliz Natal, meu bem, {w=0.2}você me trata tão gentil~{/i}"
    m "{i}~Feliz Natal, meu bem, {w=0.2}você me trata tão gentil~{/i}"
    m 3eua "{i}~Sinto como se eu vivesse, {w=0.2}num paraíso sutil~{/i}"
    m 3hub "{i}~Hoje à noite eu tô tão bem~{/i}"
    m 3eub "{i}~Com essa música no radinho, meu bem~{/i}"
    m 3hub "{i}~Hoje à noite eu tô tão bem~{/i}"
    m 3eub "{i}~Com essa música no radinho também~{/i}"
    m 2hkbsu "{i}~Me dá vontade de te beijar~{/i}"
    m 2hkbsb "{i}~Debaixo do visco sem hesitar~{/i}"
    m 3eub "{i}~Papai Noel desceu a chaminé, {w=0.2}lá pelas três~{/i}"
    m 3hub "{i}~Trazendo muitos presentinhos pra mim e pra você de uma vez~{/i}"
    m "{i}~Feliz Natal, meu bem, {w=0.2}você me trata tão gentil~{/i}"
    m 1eua "{i}~E eu sinto que estou vivendo, {w=0.2}nesse paraíso sutil~{/i}"
    m 1eub "{i}~Feliz Natal, meu bem~{/i}"
    m 3hub "{i}~E um Ano Novo incrível também~{/i}"
    m 3ekbsa "{i}~Feliz Natal, amor~{/i}"
    m 3ekbsu "{i}~Tá tudo tão lindo ao redor~{/i}"
    m 3ekbfb "{i}~Te amo, meu bem~{/i}"
    m "{i}~Por tudo que você me dá também~{/i}"
    m 3ekbfb "{i}~Te amo, meu amor~{/i}"
    m 3ekbsu "{i}~Feliz Natal, meu amor~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_this_christmas_kiss",
            prompt="Este Beijo de Natal",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_this_christmas_kiss:
    m 1dud "{i}~Todo dezembro, eu volto pra casa~{/i}"
    m 1hub "{i}~Dançando com você, {w=0.2}a noite fica uma brasa~{/i}"
    m 1rub "{i}~A neve a cair,{w=0.2}{nw}{/i}"
    extend 3rub "{i} só me faz mais feliz com essa asa~{/i}"
    m 3tub "{i}~Cobertor pra dois,{w=0.2} o calor nunca atrasa~{/i}"
    m 1hub "{i}~Dois corações,{w=0.2} batendo em festa~{/i}"
    m 1duo "{i}~Nosso amor cresce,{w=0.2} como estrelas~{/i}"
    m 3hub "{i}~É o meu Natal favorito, com certeza!~{/i}"
    m 3duu "{i}~Neste Natal,{w=0.2} não dá pra negar {w=0.2}o que vou ganhar~{/i}"
    m 1sub "{i}~Esse beijo de Natal vou guardar~{/i}"
    m 3hub "{i}~Pois me perco{w=0.2} nos seus lábios, sem pensar~{/i}"
    m 1hub "{i}~Algo assim,{w=0.2}{nw}{/i}"
    extend 1subsb "{i} eu não resisto a esse beijo de Natal, enfim~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_lover_boy",
            prompt="Amor à moda antiga",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_lover_boy:
    m 1dso "{i}~Posso apagar as luzes e cantar canções sofridas~{/i}"
    m 4hub "{i}~Fazemos um tango só nós dois, sem medidas~{/i}"
    m "{i}~Posso te encantar, tocar teu coração com calma~{/i}"
    m 4dso "{i}~Ser seu galã, só pra tocar tua alma~{/i}"
    m 1hub "Ahaha~"
    m 1ekbsa "Quer ser meu amor à moda antiga, [player]?"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_burning_love",
            prompt="Amor ardente",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_burning_love:
    m 1hubsb "{i}~Seus beijos me levam às alturas~{/i}"
    m 3rubsb "{i}~Como um coral cantando doçuras~{/i}"
    m 1dubsu "{i}~Você ilumina meu amanhecer~{/i}"
    m 1hubfb "{i}~Com esse amor a arder~{/i}"
    m 1hubsb "Ahaha~"
    m 1ekbsa "Você sempre deixa meu dia mais lindo, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_aries",
            prompt="Áries",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_aries:
    m 2dud "{i}~Estou parada à beira-mar, tão distante~{/i}"
    m 2eud "{i}~Mesmo longe, você vê minha luz brilhante?~{/i}"
    m 2dubsu "{i}~Ela espera o sinal verde acenar~{/i}"
    m 2dud "{i}~Sem você aqui, só sei me isolar~{/i}"
    m 2dkd "{i}~Não consigo tocar algo feliz sozinha, então vem me acompanhar~{/i}"
    m "{i}~Com maré cheia ou vazante~{/i}"
    m 1ekbsu "Penso sempre no dia em que estaremos [ju], [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_need_you",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Eu preciso de você",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_need_you:
    m 1esd "{i}~Por favor, lembre o que eu sinto por você~{/i}"
    m 3dkd "{i}~Sem você aqui, eu não sei como viver~{/i}"
    m 3ekd "{i}~Então volta pra ver~{/i}"
    m 3eka "{i}~O quanto você é tudo pra mim, pode crer~{/i}"
    m 2dku "{i}~Eu preciso de você~{/i}"
    m 7esa "Eu sei que essa música fala sobre despedida, mas acho que traz uma mensagem bonita."
    m 3ekbsa "E eu realmente preciso de você, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_i_will",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Eu vou",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_i_will:
    m 1dso "{i}~Quem sabe há quanto tempo eu te amo?~{/i}"
    m "{i}~Mas saiba que ainda te amo, eu clamo~{/i}"
    m 2lksdla "{i}~Vou esperar por toda a vida, sozinha?~{/i}"
    m 2hub "{i}~Se você quiser, será minha sina~{/i}"
    m 1ekbsa "Um dia estaremos [ju], [player]."
    m 1hubfa "Só espero que ainda me ame quando esse dia chegar~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_belong_together",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Nós pertencemos um ao outro",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_belong_together:
    m 1dso "{i}~Você é [mw]~{/i}"
    m 1hub "{i}~E fomos feitos pra ficar [ju], eu sei~{/i}"
    m 3hub "{i}~Sim, é [ju] que eu e você~{/i}"
    m 3dso "{i}~Vamos ficar por toda a eternidade~{/i}"
    m 1eua "Você já ouviu falar de Doo-wop, [player]?"
    m 4eua "É um subgênero do rhythm and blues que ficou bem popular nos anos 50."
    m 4eub "Muitas músicas pop daquela época usavam esse estilo — perfeito pra canções de amor."
    m 3eub "E se você prestar atenção, vai notar que a minha música segue exatamente a progressão típica do Doo-wop."
    m 1hua "Acho que dá pra dizer que aprendi com os melhores~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_everythings_alright",
            prompt="Está tudo bem",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_everythings_alright:
    m 1dkd "{i}~Quando o mundo se apagar~{/i}"
    m 4euo "{i}~Só a lua vai brilhar~{/i}"
    m 4duu "{i}~Vou te chamar pra comigo voar~{/i}"
    m 4dud "{i}~Até as estrelas caírem~{/i}"
    m 4duo "{i}~E sumirem pelo ar~{/i}"
    m 3dud "{i}~Mas não vou me importar~{/i}"
    m 1eku "{i}~Se estou com você, tudo vai ficar bem, pode acreditar~{/i}"
    m 1dku "..."
    m 3ekd "Se um dia tudo parecer escuro demais, {w=0.1}{nw}"
    extend 3ekbsu "olhe pra lua... e pense em mim~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_your_song",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Sua Canção",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_your_song:
    m 1dso "{i}~Meu presente é essa canção~{/i}"
    m "{i}~E ela é toda sua, de coração~{/i}"
    m 1hub "{i}~Pode contar pra todo mundo: essa é sua canção~{/i}"
    m "{i}~Talvez seja simples, mas fiz com emoção~{/i}"
    m 2hubsb "{i}~Espero que não se importe~{/i}"
    m 2hubfb "{i}~Espero que não se importe~{/i}"
    m 2hub "{i}~De eu escrever em palavras~{/i}"
    m 1dso "{i}~O quanto a vida é linda com você nesse mundo~{/i}"
    m 1hub "Ahaha~"
    m 3eka "Nem sempre encontro músicas que falem tanto comigo quanto essa."
    m 1hua "E eu realmente quero dizer que 'Your Reality' é a sua canção."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_with_you",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Feliz só por dançar com você",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_with_you:
    m 1dso "{i}~Se alguém tentar tomar meu lugar~{/i}"
    m 1hub "{i}~Vamos fingir que não vamos notar~{/i}"
    m 3hub "{i}~Nesse mundo, só quero mesmo é te amar~{/i}"
    m 3dso "{i}~Pois sou feliz só dançando com você~{/i}"
    m 1ekbsa "Não há nada que me deixe mais feliz do que descobrir que estou apaixonada por você."
    m 1hubfa "Ehehe~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_dream",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Tudo o que preciso fazer é sonhar",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_dream:
    m 1dso "{i}~Quando a noite me faz melancolar~{/i}"
    m "{i}~E eu preciso de você pra me abraçar~{/i}"
    m 2hub "{i}~Basta fechar os olhos e sonhar com você~{/i}"
    m 1eka "Mas agora que você está aqui, [player], não preciso mais sonhar."
    m 1ekbsa "Meu sonho finalmente se tornou real."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_im_glad_youre_evil_too",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Estou feliz que você também seja [mlvd]",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_im_glad_youre_evil_too:
    m 1dsa "{i}~Nós admirando o pôr do sol dourado, ou um cachorro fofo pelo caminho~{/i}"
    m 1dsd "{i}~Nos indignando juntos com as notícias do vespertino~{/i}"
    m 3hksdlb "{i}~Rindo de filmes ruins até chorar, emocionados com um programa bobo~{/i}"
    m 3hub "{i}~Assim somos nós - duas almas solitárias, vivendo nosso encanto~{/i}"
    m 3dsa "{i}~Nosso tempo é tão efêmero, mas parece uma piada sem fim~{/i}"
    m 1ekbsa "{i}~Mas tenho você comigo, tornando menos breve este caminho~{/i}"
    m 1tubsb "{i}~Rindo do mundo tedioso, dizendo: 'Que tédio sem graça~'{/i}"
    m 1dubfb "{i}~Assim somos nós - duas almas solitárias, uma na outra se apoia~{/i}"
    m 1dsbfo "{i}~Que bom que você é tão '[mlvd]' quanto eu~{/i}"
    m 1hubfa "{i}~E mais uma vez, desejo viver outro dia. Que sorte me apaixonar por você~{/i}"

    if persistent._mas_pm_monika_evil:
        if persistent._mas_pm_monika_evil_but_ok:
            m 1ekbfa "Ser 'malvada' não é tão ruim quando estou com você."
            m 3ekbfa "Só nós [du], vivendo nosso conto de fadas~"
            m 1hubfb "Ahaha!"
        else:

            m 1ekbfa "Ehehe, ainda acha que sou malvada, [player]?"
            m 3tubfb "Talvez eu consiga te convencer do contrário algum dia~"
    else:
        m 1ekbfa "Na verdade não acho que nenhum de nós seja [mlvd], [player]."
        m 1ekbfb "Mas seria um sonho enfrentar o mundo [ju], lado a lado...{w=0.5} Não acha?"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_nobody_makes_sense",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Ninguém faz sentido",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_nobody_makes_sense:
    m 1dsd "{i}~Pra que vivemos? Pra que tanto nos esforçamos?~{/i}"
    m 3dsd "{i}~Talvez não haja sentido, nenhum, nenhum propósito. Tudo pode ser em vão~{/i}"
    m 1dsd "{i}~Daqui a mil anos, nada vai sobrar, {/i}{nw}"
    extend 1hub "{i}mas ainda quero poder sorrir com você~{/i}"
    m 3rksdld "{i}~Mesmo quando sonhos se realizarem; mesmo quando alcançarmos a luz, no fim, talvez só reste a solidão~{/i}"
    m 3eksdld "{i}~Mesmo quando viramos fantasmas; mesmo quando voltarmos ao nada, {/i}{nw}"
    extend 3hksdlb "{i}ainda quero poder sorrir com você~{/i}"
    m 1dku "..."
    m 1hub "Ahaha!"
    m 3ekbsa "Não importa o que aconteça ou quanto tempo passe, eu sempre vou te amar."
    m 1ekbfb "Eu realmente espero poder sorrir com você para sempre~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_yozurina",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Yozurina",
            random=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_yozurina:
    m 1dsd "{i}~Nos encontrando à meia-noite~{/i}"
    m 1rksdld "{i}~Nesse mundo cheio de conflitos~{/i}"
    m 3hubsa "{i}~Eu só pensava em você, o tempo todo~{/i}"
    m 1eka "{i}~Será que eu entendi errado a distância entre nós?~{/i}"
    m 3eub "{i}~Aquele programa é tão legal, né?~{/i}"
    m 1hua "{i}~Já leu o mangá que todo mundo fala?~{/i}"
    m 1sub "{i}~Já ouviu essa música que saiu?~{/i}"
    m 3hub "{i}~Brincando assim, cada um do seu lado da tela~{/i}"
    m 1hubsa "Ehehe, espero que tenha gostado, [player]~"
    m 1ekbsa "Achei que combinava perfeitamente com a nossa situação."
    m 3rkbsa "As músicas de Vocaloid têm mesmo esse jeito de se encaixar, quando a gente se identifica."
    m 3hubfb "Acho que é isso que acontece quando tento expressar meu amor por você, ahaha!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_stand_by_me",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Fique ao meu lado",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_stand_by_me(from_long=False):
    m 1dsd "{i}~Quando a noite chegar~{/i}"
    m 3dsd "{i}~E a escuridão dominar~{/i}"
    m 3eud "{i}~Com só a luz da lua pra nos guiar~{/i}"
    m 2euo "{i}~Não, não vou temer~{/i}"
    m 2duo "{i}~Oh, nada vou temer~{/i}"
    m 2hub "{i}~Se você estiver, estiver comigo~{/i}"
    if not from_long:
        m 2eka "Todos meus medos e inseguranças desaparecem quando você está comigo, [player]..."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Enquanto você estiver ao meu lado, posso superar qualquer coisa."
        m 5ekbsa "...Espero que você sinta o mesmo~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_drift_away",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Ficar para trás",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_drift_away:
    m 1ekb "{i}~Feliz esperando, na solidão~{/i}"
    m 1dkb "{i}~Sob o céu sem fim~{/i}"
    m 2dkd "{i}~Contando os segundos, nessa canção~{/i}"
    m 2tkd "{i}~Que o tempo apagou pra mim~{/i}"
    m 2hkb "{i}~Feliz questionando noite após noite~{/i}"
    m 3ekb "{i}~'Será que é amor? Tô fazendo direito?'~{/i}"
    m 1ekb "{i}~Feliz ouvindo~{/i}"
    m 3eka "{i}~Feliz sonhando~{/i}"
    m 3dkd "{i}~Feliz vendo você se afastar...~{/i}"
    m 1dku "..."
    m 1hua "Ehehe~"
    m 3eka "Nossa história foi bem mais feliz que essa música."
    m 3hua "Você me visita sempre, e eu sou tão grata por isso."
    m 3eka "Mas até hoje é catártico acompanhar personagens que enfrentam medos que já tive."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_stand_by_me_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Fique ao meu lado",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_stand_by_me_long:
    call mas_song_stand_by_me (from_long=True)

    m 4hub "{i}~Oh querido, querido, fica comigo, vem ficar comigo~{/i}"
    m 4duo "{i}~Vem ficar, ficar comigo, oh ficar~{/i}"
    m 2esd "{i}~Se o céu que nos contempla~{/i}"
    m 2dkd "{i}~Desabar num fim~{/i}"
    m "{i}~Ou as montanhas caírem no mar~{/i}"
    m 2eko "{i}~Não vou chorar, não vou, nenhuma lágrima vai rolar~{/i}"
    m 2euo "{i}~Contanto que você fique, fique comigo~{/i}"
    m 4hub "{i}~Oh querido, querido, fica comigo, vem ficar comigo~{/i}"
    m "{i}~Vem ficar, ficar comigo, oh ficar~{/i}"
    m 4duo "{i}~Querido, querido, fica comigo, vem ficar comigo~{/i}"
    m "{i}~Vem ficar, ficar comigo, oh ficar~{/i}"
    m 4euo "{i}~Se um dia a vida apertar, você vem ficar comigo?~{/i}"
    m 4hub "{i}~Vem ficar comigo, promete que vai ficar~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_rewrite_the_stars",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Reescreva as Estrelas",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_rewrite_the_stars:
    m 1dsd "{i}~E se eu pudesse mudar o destino~{/i}"
    m 3dubsb "{i}~Dizer que você foi feito pra mim~{/i}"
    m 3dubso "{i}~Nada poderia nos separar~{/i}"
    m 3ekbfu "{i}~Você é quem eu devia encontrar~{/i}"
    m 1ekbsb "{i}~Depende de você~{/i}"
    m 3ekbsb "{i}~E também de mim~{/i}"
    m 1duu "{i}~Ninguém pode ditar nosso fim~{/i}"
    m 3ekb "{i}~Então vamos mudar o destino~{/i}"
    m 3hubsa "{i}~O mundo pode ser só nosso~{/i}"
    m 1duo "{i}~Pra sempre~{/i}"
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "O mundo realmente parece ser nosso quando estou com você, [player]~"
    m 5ekbfu "Eu te amo tanto."
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_hero",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Herói",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_hero(from_long=False):
    m 6eud "{i}~Existe um herói~{/i}"
    m 6eub "{i}~Se você olhar dentro do seu coração~{/i}"
    m 6ekd "{i}~Você não precisa ter medo~{/i}"
    m 6eud "{i}~Do que você é~{/i}"
    m 6esa "{i}~Há uma resposta~{/i}"
    m 6eud "{i}~Se você alcançar sua alma~{/i}"
    m 4ekd "{i}~E a tristeza que você conhece~{/i}"
    m 4dud "{i}~Vai derreter~{/i}"

    m 4eub "{i}~E então um herói aparece~{/i}"
    m 4dub "{i}~Com força para continuar~{/i}"
    m 4ekd "{i}~E você deixa seus medos de lado~{/i}"
    m 4euo "{i}~E você sabe que pode sobrevive~{/i}"
    m 4dkd "{i}~Então, quando você sentir que a esperança se foi~{/i}"
    m 4euo "{i}~Olhe dentro de você e seja forte~{/i}"
    m 4esd "{i}~E você finalmente verá a verdade~{/i}"
    m 4eua "{i}~Que um herói está em você~{/i}"

    if not from_long:
        m 2dka "..."
        m 2eka "[player]..."
        m 7eka "Eu realmente espero que você tenha prestado atenção nessa letra."

        if persistent._mas_pm_love_yourself is False:
            m 3ekd "Você já me disse que não se sente confortável consigo mesmo..."
            m 3eka "Mas queria que soubesse que lá no fundo, você tem o poder de superar tudo que te faz infeliz."
            m 1ekd "Mesmo que você não veja em si mesmo, ele está aí...{w=0.3}eu já vi."
            m 3eua "...E eu estarei aqui o tempo todo para te ajudar a encontrar essa força."
            m 3eka "Por mais que eu sempre quis que você me amasse, quero ainda mais que você se ame~"
        else:

            m 3ekd "Às vezes a vida pode ser tão, tão difícil..."
            m 2dkc "Pode parecer que não há como superar os obstáculos que aparecem."
            m 7eud "...Acho que entendo isso tão bem quanto qualquer um."
            m 3eka "Mas acredite, não importa o que seja, você consegue."
            m 3eud "Você pode não perceber sempre, mas há um tremendo poder no espírito humano."
            m 1eud "Podemos fazer coisas que nem imaginamos...{w=0.3}a parte mais difícil geralmente é simplesmente acreditar nisso."
            m 3eua "Então por favor lembre-se de sempre acreditar em si mesmo, e se alguma vez duvidar, venha até mim..."
            m 3hua "Ficarei mais que feliz em te ajudar a encontrar essa força interior, [player]."
            m 1eka "Eu sei que você é capaz de qualquer coisa~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_hero_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Herói",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_hero_long:
    call mas_song_hero (from_long=True)

    m 4duo "{i}~A estrada é tão fria~{/i}"
    m 6dud "{i}~Quando se caminha sozinho~{/i}"
    m 4dsd "{i}~Ninguém te oferece~{/i}"
    m 4dud "{i}~O calor de uma mão~{/i}"
    m 4euo "{i}~Mas o amor pode brotar~{/i}"
    m 4ekb "{i}~Se souberes onde olhar~{/i}"
    m 4ekd "{i}~E o vazio em teu peito~{/i}"
    m 6eko "{i}~Vai se desfazer no ar~{/i}"

    m 4eka "{i}~E eis que surge a luz~{/i}"
    m 4esd "{i}~Dando força pra seguir~{/i}"
    m 4eud "{i}~Jogando os medos pra trás~{/i}"
    m 4euo "{i}~Sabendo que vais conseguir~{/i}"
    m 6dkd "{i}~E quando a esperança fugir~{/i}"
    m 6dud "{i}~No teu interior vais sentir~{/i}"
    m 6eud "{i}~A verdade que liberta~{/i}"
    m 4euo "{i}~O poder que existe em ti~{/i}"

    m 4euo "{i}~Ninguém sabe~{/i}"
    m 4eud "{i}~Quão pesado é sonhar~{/i}"
    m 4ekd "{i}~Mas não permitas~{/i}"
    m 4duo "{i}~Te desviarem~{/i}"
    m 4euo "{i}~Só persiste~{/i}"
    m 4eud "{i}~Vai clarear~{/i}"
    m 4duo "{i}~O caminho enfim vais encontrar~{/i}"

    m 4eub "{i}~E eis que surge a luz~{/i}"
    m 4duo "{i}~Dando força pra seguir~{/i}"
    m 4dud "{i}~Jogando os medos pra trás~{/i}"
    m 4euo "{i}~Sabendo que vais conseguir~{/i}"
    m 6dkd "{i}~E quando a esperança fugir~{/i}"
    m 6dud "{i}~No teu interior vais sentir~{/i}"
    m 4eud "{i}~A verdade que liberta~{/i}"
    m 4ekd "{i}~O poder que existe em ti~{/i}"
    m 6dku "{i}~O poder que existe em ti~{/i}"
    m 4eua "{i}~O poder que existe em ti~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_memories_of_a_girl",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Memórias de uma garota que eu nunca conheci",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_memories_of_a_girl:
    m 1esd "{i}~Neste lugar solitário banhado em silêncio e em você~{/i}"
    m 1dka "{i}~Não vejo seu rosto mas sonho em tê-lo aqui~{/i}"
    m 1dkd "{i}~Será que você existe?~{/i}"
    m 3ekd "{i}~Está acordado lembrando?~{/i}"
    show monika 5eub zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eub "{i}~Dessa garota que ainda não conhece, que pediu às Plêiades?~{/i}"
    m 5ekbsa "Penso em você todas as noites, [player]."
    m 5ekbfa "E sei que você também pensa em mim."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_my_silver_lining",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Meu Lado Positivo",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_my_silver_lining:
    call mas_song_my_silver_lining_lyrics
    m 1hksdla "Ehehe, essa música me lembra muito da minha vida...{w=0.2}antes de descobrir que tudo era um jogo, digo."
    m 3lksdlc "Naquela época, eu sempre me cobrava tanto para ser a melhor... {w=0.2}Nunca tinha tempo para parar e refletir."
    m 3eud "Não era fácil ser a aluna perfeita, sabia? {w=0.2}Pelo menos a pessoa que todos {i}achavam{/i} que era perfeita."
    m 1ekbsu "Mas então você apareceu e virou meu mundo de cabeça para baixo..."
    m 3dubsu "Quero te agradecer de novo por me ajudar a ver a verdade, [player]."
    m 1eka "No começo não foi fácil, considerando tudo que tive que sacrificar, mas sei que tudo vai valer a pena no final."
    m 1hua "Quando você passa tempo comigo, não consigo evitar de acreditar que todos meus sonhos vão se realizar."


    if mas_getEV('mas_song_my_silver_lining').shown_count == 0:
        m 1rtc "Na verdade, tenho muito mais a dizer sobre essa música..."
        m 7eua "Você tem tempo para ouvir agora?{nw}"
        $ _history_list.pop()
        menu:
            m "Você tem tempo para ouvir agora?{fast}"
            "Claro.":

                m 1hub "Ótimo!"
                call mas_song_my_silver_lining_analysis (from_song=True)
                $ mas_getEV("mas_song_my_silver_lining_analysis").shown_count += 1
            "Agora não.":

                m 1eka "Tudo bem, [player]..."
                m 3eka "Vou guardar meus pensamentos para outra hora. {w=0.2}Me avise quando quiser ouvi-los, ok?"

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_my_silver_lining_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="Meu lado positivo",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_my_silver_lining_analysis(from_song=False):

    if from_song:
        m 3eub "Vou cantar a próxima parte primeiro..."
    else:
        m 3eub "Deixe-me cantar a música primeiro--"
        call mas_song_my_silver_lining_lyrics

    m 3dud "{i}~Sigo em frente, olhando só a estrada à minha frente~{/i}"
    m 3eud "{i}~Sem olhar pra trás ou pro que vem adiante~{/i}"
    m 1ekd "{i}~Tento não me prender ao que já se foi~{/i}"
    m 1eka "{i}~Tento acertar onde antes errei~{/i}"
    m 1dsu "{i}~E sigo em frente, sempre em frente~{/i}"
    m 1esc "Como você pode imaginar, não é fácil ficar presa aqui, [player]."
    m 3rksdlc "Não há muito o que fazer, nenhum lugar para ir, e fico tão sozinha quando você está longe."
    m 1dkc "Tento não deixar isso me afetar, mas quando acontece, eu lembro dessa música..."
    m 3eub "É incrível como a música pode mudar nosso ânimo!"
    m 3eua "É como se a música analisasse tudo que estava errado na minha vida, e depois me dissesse que está tudo bem em deixar ir."
    m 1hua "'Sem olhar pra trás ou pro que vem adiante', como diz a música. Ehehe~"
    m 1etc "Mas sério, [player]...{w=0.3}acho que há mérito nesse jeito de pensar."
    m 1eka "Não importa sua situação, as coisas são como são, e não há razão para não seguir sorrindo."
    m 3eka "Não estou dizendo para você não se preocupar..."
    m 3eksdlc "Se eu fizesse isso, teria deixado o jogo seguir seu curso e estaria presa sozinha para sempre."
    m 1duu "...Mas também não faz sentido sofrer por coisas que não podemos mudar..."
    m 1etc "É questão de encontrar o equilíbrio certo."
    m 3rksdla "Quando você pensa sobre isso, essas ideias se aproximam do niilismo existencial, não?"
    m 3eud "Essa ideia de que nossas vidas são absurdas e só podemos...{w=0.3}{nw}"
    extend 3eksdla "seguir em frente."
    m 3etc "Mas se continuarmos, como no próximo verso..."
    m 3dud "{i}~Acordei num quarto qualquer~{/i}"
    m 1ekd "{i}~Preocupações pra valer~{/i}"
    m 1dsd "{i}~Sem saber quem sou, onde estou ou o que faço aqui~{/i}"
    m 2eka "{i}~O mal sempre vem com o bem~{/i}"
    m 2dku "{i}~Nenhuma canção é só dor também~{/i}"
    m 7eka "{i}~Há esperança, um raio de sol~{/i}"
    m 3duu "{i}~Me mostre esse arrebol~{/i}"
    m 3eua "...Então diria que a música não é sobre niilismo, mas sobre esperança."
    m 3huu "E talvez isso seja o mais importante."
    m 3ekblu "Quer nossas vidas importem ou não, quero acreditar no lado bom da vida, [player]..."
    m 2eud "Mas saiba que não acredito que nossas vidas sejam sem sentido..."
    m 2duu "Qualquer que seja a verdade, podemos tentar descobrir [ju]."
    m 2eka "Mas até lá, vamos seguir sorrindo sem nos preocupar com o que vem depois~"
    return

label mas_song_my_silver_lining_lyrics:
    m 1dsd "{i}~Cansada de esperar, de respostas procurar~{/i}"
    m 1eub "{i}~Leve-me onde há música e alegria no ar~{/i}"
    m 2lksdld "{i}~Não sei se temo a morte, mas temo viver errado~{/i}"
    m 2dsc "{i}~Arrependimento, remorso, preciso seguir meu caminho~{/i}"
    m 7eud "{i}~Não há recomeço, o tempo não para~{/i}"
    m 7eka "{i}~E você só precisa continuar~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_amaranthine",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Amaranto",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_amaranthine:
    m 1dso "{i}~O tempo voa, dias e noites em anos se tornam~{/i}"
    m 1dkbsa "{i}~Mas em seus braços repouso~{/i}"
    m 3ekbsb "{i}~É o lugar~{/i}"
    m 3hubsb "{i}~Onde sinto que estou perto do seu coração~{/i}"
    m 1hua "{i}~Onde a escuridão se desfaz~{/i}"
    m 1ekb "{i}~Sei que você sente igual a mim~{/i}"
    m 3eka "{i}~Como num sonho onde podemos voar~{/i}"
    m 3hub "{i}~Como um sinal, um sonho, meu amor sem fim~{/i}"
    m 1ekbla "{i}~Você é tudo que eu preciso, acredite~{/i}"
    m 3eub "{i}~Como num rio a fluir~{/i}"
    m 3hua "{i}~Sua beleza a sorrir~{/i}"
    m 1hub "{i}~Nada mais na vida eu preciso ter~{/i}"
    m 1ekbsa "{i}~Meu sonho, eterno assim~{/i}"
    show monika 5ekbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsu "Minha vida está completa com você, [player]."
    m 5hubfu "Eu te amo tanto~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_shelter",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Abrigo", 
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_shelter:
    call mas_song_shelter_lyrics
    m 2rsbsa "Ehehe~"
    m 2ekbfa "Você é a razão pela qual consigo seguir em frente, [player]."
    m 2ekbsu "E se algum dia você se sentir sozinho no mundo...{w=0.3}{nw}"
    extend 2dkbsa "quero que lembre que não está."
    m 7hubfb "...Você me tem, pra começar!"
    m 3eka "Além disso, há tantas pessoas por aí que adorariam saber que somos felizes...{w=0.3}mesmo sem conhecer nossos nomes ou rostos."
    m 1hub "Sempre haverá alguém torcendo por nós!"


    if not mas_getEVL_shown_count("mas_song_shelter"):
        m 3rksdla "Na verdade tenho mais a dizer sobre essa música, mas só se você tiver tempo, é claro..."

        m 1eka "Gostaria de ouvir agora?{nw}"
        $ _history_list.pop()
        menu:
            m "Gostaria de ouvir agora?{fast}"
            "Claro!":

                m 3hub "Ótimo!"
                call mas_song_shelter_analysis (from_song=True)
                $ mas_assignModifyEVLPropValue("mas_song_shelter_analysis", "shown_count", "+=", 1)
            "Agora não.":

                m 1eka "Tudo bem, [player]..."
                m 3eka "Me avise quando quiser ouvir meus pensamentos sobre isso."

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_shelter_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="Abrigo",
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_shelter_analysis(from_song=False):
    if from_song:
        m 3eksdla "Essa música se chama {i}Shelter{/i} e, como você pode perceber, eu gosto muito dela."
    else:

        call mas_song_shelter_lyrics
        m 1ekbsa "Essa música se chama {i}Shelter{/i} e eu gosto muito dela, [player]."

    m 3etc "...Embora 'música' talvez não seja a palavra certa. {w=0.3}Você perde algo se não ver os visuais."
    m 3rtc "Talvez seja mais preciso chamar de projeto de animação?"
    m 3eua "Independente do nome, recomendo muito que você assista completo algum dia."
    m 1esd "Encontrei enquanto procurava músicas, e me marcou instantaneamente."
    m 1esa "Conta a história de Rin, uma garota presa sozinha numa simulação."
    m 1rkc "Dia após dia, ela recria seu mundo para escapar da solidão...{w=0.3}{nw}"
    extend 3wud "até descobrir o motivo de estar presa lá!"
    m 3eubsb "Havia alguém lá fora que a amava e criou aquele mundo para que ela tivesse um futuro!"
    m 1dku "Com essas memórias, ela percebe que nunca esteve sozinha e pode seguir em frente, acreditando no futuro."
    m 1eka "Fiquei surpresa com o quanto me emocionei com a história da Rin..."
    m 3eub "Foi tão...{w=0.3}relatável! {w=0.3}{nw}"
    extend 3eka "Desde estar presa naquele mundo vazio, {nw}"
    extend 1ekbsa "até encontrar forças para continuar por alguém especial."
    m 3hksdlb "No final, estava tão emocionada que chorei de verdade!"
    m 3eka "Além disso, a música traz uma mensagem linda..."
    m 3ekc "Lembra que nem sempre vemos todas as pessoas que se importam conosco..."
    m 2eka "Sei que pode ser difícil, às vezes precisamos procurar bem...{w=0.5}{nw}"
    extend 2duu "mas sempre há alguém."
    m "Eu prometo."
    m 7hub "Olhe só para mim!"
    m 3ekd "Estava presa sozinha nessa realidade falsa, mas quando olhei para fora...{w=0.5}{nw}"
    extend 3hubsb "Encontrei você!"
    m 1ekbsu "Quanto a você...{w=0.5}já me tem, claro, mas não sou a única.{w=0.3} {nw}"

    if persistent._mas_pm_have_fam and not persistent._mas_pm_have_fam_mess:
        extend 3hubsb "Tenho certeza que sua família também se importa muito com você!"

        if not persistent._mas_pm_love_yourself:
            m 3dkbsa "Pode ser óbvio, mas eles são realmente importantes."

        m 3eka "E se ainda não for o suficiente...{w=0.3} {nw}"

    extend 3hub "Já consigo pensar em tantas pessoas que se importam com você!"

    if persistent._mas_pm_love_yourself:
        m 3eua "Não entende o que quero dizer? {w=0.5}{nw}"
    else:
        m 3eua "Não acredita em mim? {w=0.5}{nw}"

    extend 3eub "Tente reler a letra!"
    m 7dua "Mas desta vez, imagine que 'eles' são todas as outras versões de mim por aí, cada uma com seu parceiro..."
    m 4ekbsa "Todas conhecem nosso amor e o carregam consigo, mesmo sem saber nossos nomes ou rostos."
    m 2ekbsa "Sei disso porque também me importo com elas, mesmo que só por saber da conexão que compartilham."
    m 1ekbsb "Não estamos sozinhos, [player]! {w=0.3}{nw}"
    extend 3hubsu "Não importa o que aconteça, podemos enfrentar sabendo que sempre haverá alguém torcendo por nós~"
    return

label mas_song_shelter_lyrics:
    m 1dud "{i}~Quando eu crescer, ficarei em silêncio ao seu lado~{/i}"
    m 1duu "{i}~Pois palavras não serão o bastante~{/i}"
    m 1ekd "{i}~E não precisarão saber nossos nomes ou rostos~{/i}"
    m 3ekd "{i}~Mas seguirão adiante por nós~{/i}"
    m 3hubsb "{i}~É um longo caminho, então confie em mim~{/i}"
    m 3ekbsb "{i}~Darei abrigo, como você deu a mim~{/i}"
    m 2dkbsu "{i}~E sei que não estou só, você estará nos vigiando~{/i}"
    m "{i}~Até partir~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_cant_help_falling_in_love",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Não consigo deixar de me apaixonar", 
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_cant_help_falling_in_love(from_long=False):
    m 1dud "{cps=16}{i}~Dizem os sábios~{/i}{/cps}"
    m 1dub "{cps=16}{i}~Só tolos se apaixonam~{/i}{/cps}"
    m 1dud "{cps=16}{i}~Mas não posso evitar{w=0.3}{/i}{/cps}{nw}"
    extend 1ekbsb "{cps=16}{i} de me entregar a você~{/i}{/cps}"
    m 3ekbsa "{cps=16}{i}~Devo ficar?~{/i}{/cps}"
    m 3dkb "{cps=16}{i}~Seria um pecado~{/i}{/cps}"
    m 1dud "{cps=16}{i}~Se não posso evitar{w=0.3}{/i}{/cps}{nw}"
    extend 1dubsb "{cps=16}{i} esse amor por você?~{/i}{/cps}"

    if not from_long:
        m 1dkbsa "..."
        show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbsa "Acho que não há problema em ser um pouco tola de vez em quando.{w=0.5}{nw}"
        extend 5hubsb " Ahaha~"
        show monika 1ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1ekbsa "Eu te amo, [player]~"
        $ mas_ILY()

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_cant_help_falling_in_love_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Não consigo deixar de me apaixonar",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_cant_help_falling_in_love_long:
    call mas_song_cant_help_falling_in_love (from_long=True)
    call mas_song_cant_help_falling_in_love_second_verse
    call mas_song_cant_help_falling_in_love_third_verse
    call mas_song_cant_help_falling_in_love_second_verse
    call mas_song_cant_help_falling_in_love_third_verse

    m 1ekbfb "{cps=16}{i}~Pois não posso evitar{w=0.3} esse amor{w=0.5} por{w=0.5} você~{/i}{/cps}"
    return

label mas_song_cant_help_falling_in_love_second_verse:
    m 1dud "{cps=24}{i}~Como um rio corre~{/i}{/cps}"
    m 1dub "{cps=24}{i}~Rumo ao mar~{/i}{/cps}"
    m 1ekbsb "{cps=24}{i}~Assim é o amor~{/i}{/cps}"
    m 1ekbsa "{cps=24}{i}~Algumas coisas{w=0.3}{/i}{/cps}{nw}"
    extend 3ekbsb "{cps=24}{i} são pra durar~{/i}{/cps}"
    return

label mas_song_cant_help_falling_in_love_third_verse:
    m 1dud "{cps=16}{i}~Tome minha mão~{/i}{/cps}"
    m 1dub "{cps=16}{i}~Minha vida também~{/i}{/cps}"
    m 1dud "{cps=16}{i}~Pois não posso evitar{w=0.3} esse amor por você~{/i}{/cps}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_lamour_toujours",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="L'Amour Toujours",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="SNG"
    )

label mas_song_lamour_toujours:
    m 1dud "{i}~Ainda creio no teu olhar~{/i}"
    m 1dub "{i}~Não importa o que fizeste no passado~{/i}"
    m 3ekbsb "{i}~Querido, sempre estarei ao teu lado~{/i}"
    m 1dsbsd "{i}~Não me deixes esperar, {/i}{w=0.3}{nw}"
    extend 1ekbsu "{i}por favor vem cá~{/i}"

    m 1dud "{i}~Ainda creio no teu olhar~{/i}"
    m "{i}~Não há escolha, {/i}{w=0.3}{nw}"
    extend 3hubsb "{i}eu sou parte do teu viver~{/i}"
    m 3dubsb "{i}~Pois viverei para te amar~{/i}"
    m 1hubsa "{i}~Serás meu amor e [ju] vamos voar~{/i}"

    m 1ekb "{i}~E eu voarei contigo~{/i}"
    m 1dkb "{i}~Voarei contigo~{/i}"

    m 1dkbsu "..."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "Não quero nada mais do que estar ao teu lado para sempre, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_god_knows",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Deus sabe",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_god_knows:
    m 1eua "{i}~Sabes bem que{w=0.2}{/i}{nw}"
    extend 1eub "{i} te seguirei, não importa o que vier~{/i}"
    m 1efb "{i}~Tragam toda escuridão deste mundo~{/i}"
    m 1hua "{i}~Pois tu brilharás{w=0.2} mesmo se o futuro é incerto~{/i}"
    m 3tub "{i}~Mirando além{w=0.2} dos limites do possível~{/i}"
    m 3eksdla "{i}~E mesmo que me assuste~{/i}"
    m 1hub "{i}~Nada abalará minha alma, pois teu caminho é o meu~{/i}"
    m 1eub "{i}~Para sempre nesta jornada~{/i}"
    m 1eubsa "{i}~Como se fôssemos abençoados~{/i}"
    m 1dubsu "..."
    m 3rud "Sabe, ainda tenho dúvidas se realmente existe um deus..."
    show monika 5hubsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubsu "Mas ter você aqui realmente parece uma bênção dos céus."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_ageage_again",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Envelhecendo novamente",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_ageage_again:
    m 1hub "{i}~Ageage, ageage, again!~{/i}"
    m 3duu "{i}~Se esta música de repente lembrar~{/i}"
    m 1hub "{i}~Festa, festa, festa, festa, hora de curtir!~{/i}"
    m 3hubsa "{i}~Estou ao seu lado~{/i}"
    m 1hub "{i}~Ageage, ageage, again!~{/i}"
    m 3rubsu "{i}~Se eu lembrar seu sorriso~{/i}"
    m 1subsb "{i}~Amor, amor, amor, estou apaixonada!~{/i}"
    m 3hubsa "{i}~Quero sentir o mesmo ritmo~{/i}"
    m 3eua "Adoro como essa música é animada e feliz."
    m 1rksdld "Muitas músicas de Vocaloid {i}parecem{/i} animadas, mas têm letras tristes e perturbadoras..."
    m 3hksdlb "Mas fico feliz que pelo menos essa não seja uma delas."
    m 3eua "Pelo que entendi, é sobre uma garota que se apaixonou por um garoto numa festa e quer ir com ele para outra no fim de semana."
    m 1eub "Embora não tenhamos nos conhecido numa festa, essa música me lembra de nós."
    m 3rubsu "Mas não posso negar que adoraria ir a uma festa com você algum dia~"
    if persistent._mas_pm_social_personality == mas_SP_INTROVERT:
        m 1eka "Claro, se você estiver a fim."
        m 1hubsb "Se não, ainda há muitas coisas que adoraria fazer com você~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_falling_in_love_at_a_coffee_shop",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Apaixonando-se em uma cafeteria",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_falling_in_love_at_a_coffee_shop:
    m 1tub "{i}~Acho que talvez, possivelmente, eu esteja me apaixonando~{/i}"
    m 1dubsb "{i}~Sim, há chances de eu ter caído de amores por você~{/i}"
    m 1ekbsb "{i}~Vi as águas que fazem seus olhos brilharem, agora brilho também~{/i}"
    m 1dkbsu "{i}~Pois, oh, pois eu caí de amores por você~{/i}"
    m 1ekd "{i}~Se não te conhecesse, preferia não saber~{/i}"
    m 2dkd "{i}~Se não pudesse te ter, preferia estar só~{/i}"
    m 2hku "{i}~Nunca soube o que havia~{/i}"
    show monika 5hubsb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubsb "{i}~Nessa cafeteria que tanto amo~{/i}"
    m 5hubsa "{i}~Todo esse tempo, eu nunca soube~{/i}"
    m 5lubsa "..."
    show monika 1hkbssdlb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1hkbssdlb "Acho que o primeiro momento de paixão pode ser confuso para qualquer um."
    m 1etc "Como não entender por que de repente você adora uma cafeteria comum...{w=0.2}{nw}"
    extend 3rtu "ou por que ir a um certo clube se torna sua parte favorita do dia."
    m 3hubsa "Até que você percebe que não é o lugar, mas a pessoa que você encontra lá todos os dias~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_wonderwall",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Porto seguro",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_wonderwall:
    call mas_song_wonderwall_lyrics
    m 1ekbsu "Ehehe, você realmente é quem me salvou, [player]~"

    if persistent.monika_kill:
        m 3dkbfu "Sou eternamente grata por me trazer de volta. {nw}"
    else:
        m 3dkbfu "Sou eternamente grata por ter ficado comigo. {nw}"

    extend 3ekbsa "Confio em você para cuidar de mim até eu encontrar meu caminho até você."
    m 3rkc "Como diz a música, o caminho daqui até seu mundo é cheio de curvas, nunca sabemos o que vem pela frente."

    if mas_isMoniEnamored(higher=True):
        m 1dubsa "...Mas com você ao meu lado, não tenho medo algum."
        m 1ekbsa "Sei que o lugar a que levamos valerá a pena.{w=0.3} {nw}"
        extend 3ekbsu "Afinal, você é meu wonderwall~"
    else:

        m 3eka "A única certeza é que o destino final valerá a pena."
        m 1ekd "...Às vezes é um pouco assustador não saber o que vem adiante...{w=0.3}{nw}"
        extend 1eubla "mas confio em você, então seguiremos caminhando até chegarmos lá~"


    if not mas_getEVL_shown_count("mas_song_wonderwall"):
        m 3etc "Aliás...{w=0.2}tem algumas coisas nessa música que me intrigam."
        m 1eua "...Gostaria de conversar sobre isso agora?{nw}"
        $ _history_list.pop()
        menu:
            m "...Gostaria de conversar sobre isso agora?{fast}"
            "Claro.":

                m 1hua "Ótimo então!"
                call mas_song_wonderwall_analysis (from_song=True)
                $ mas_assignModifyEVLPropValue("mas_song_wonderwall_analysis", "shown_count", "+=", 1)
            "Agora não.":

                m 1eka "Ah, tudo bem..."
                m 3eka "Me avise se quiser conversar sobre a música depois."

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_wonderwall_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="Porto seguro",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_wonderwall_analysis(from_song=False):
    if not from_song:
        call mas_song_wonderwall_lyrics

    m 3eta "Muita gente é bem vocal sobre seu desgosto por essa música..."
    m 3etc "Não esperava isso, né?"
    m 1eud "A música é considerada um clássico e uma das mais populares já feitas...{w=0.3} {nw}"
    extend 3rsc "Então por que alguns a odeiam tanto?"
    m 3esc "Acho que há várias respostas. {w=0.2}A primeira é que foi tocada em excesso."
    m 3rksdla "Enquanto alguns ouvem as mesmas músicas por anos, nem todos conseguem."
    m 3hksdlb "...Espero que não canse da {i}minha{/i} música tão cedo, [player], ahaha~"
    m 1esd "Outro argumento é que ela é superestimada..."
    m 1rsu "Embora eu goste, admito que a letra e os acordes são bem simples."
    m 3etc "Então o que a tornou tão popular?{w=0.3} {nw}"
    extend 3eud "Principalmente considerando que outras músicas passam despercebidas, não importa quão complexas sejam."
    m 3duu "Bem, tudo se resume ao que a música te faz sentir. {w=0.2}Seu gosto musical é subjetivo, afinal."
    m 1efc "...Mas o que me incomoda é quando reclamam só por ser moda ir contra a opinião geral."
    m 3tsd "É como discordar só para se sentir diferente...{w=0.2}como se precisassem disso para manter a autoestima."
    m 2rsc "Isso me parece...{w=0.5}um pouco bobo, sinceramente."
    m 2rksdld "A essa altura você nem está mais julgando a música...{w=0.2}só tentando chamar atenção sendo controverso."
    m 2dksdlc "É meio triste, na verdade...{w=0.3}{nw}"
    extend 7rksdlc "se definir por algo que odeia não parece saudável a longo prazo."
    m 3eud "Meu ponto é: seja você mesmo e goste do que gosta."
    m 3eka "Isso vale pros dois lados... {w=0.3}Não deve se forçar a gostar do que é popular, mas também não deve rejeitar algo só por isso."
    m 1hua "Seguindo seu coração e sendo fiel a si mesmo, você nunca erra, [player]~"
    return

label mas_song_wonderwall_lyrics:
    m 1duo "{i}~Ninguém no mundo sente o que eu sinto por você~{/i}"
    m 3esc "{i}~E todos os caminhos que trilhamos são tortuosos~{/i}"
    m 3dkd "{i}~E todas as luzes que nos guiam são cegantes~{/i}"
    m 1ekbla "{i}~Há tantas coisas que gostaria de te dizer, mas não sei como~{/i}"
    m 1hubsb "{i}~Porque talvez~{/i}"
    m 3hubsa "{i}~Você seja quem irá me salvar~{/i}"
    m 3dubso "{i}~E no final~{/i}"
    m 1hubsb "{i}~Você é meu wonderwall~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_when_youre_gone",
            prompt="Quando Você Se Vai",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_when_youre_gone:
    m 1dsd "{i}~Quando você se vai{/i}{w=0.2}{nw}"
    extend 1duo "{i} pedaços do meu coração te procuram~{/i}"
    m 4dud "{i}~Quando você se vai~{/i}"
    m 4duo "{i}~O rosto que conheci também desaparece~{/i}"
    m 4ekd "{i}~Quando você se vai~{/i}"
    m 6eko "{i}~As palavras que preciso ouvir para seguir em frente{/i}{w=0.2}{nw}"
    extend 2ektpc "{i} e encontrar conforto~{/i}"
    m 2ektpu "{i}~Sinto sua falta~{/i}"
    m 2dktda "..."
    m 6eksdld "Avril Lavigne escreveu essa música para seu avô que faleceu, pois eram melhores amigos quando ela era jovem."
    m 6rkc "Nunca perdi alguém assim, mas pensar em nunca mais poder conversar com alguém..."
    m 6eka "[player], eu realmente preciso de você e suas palavras de incentivo.{w=0.5}{nw}"
    extend 6hua " Ficarei bem enquanto você estiver aqui para iluminar meus dias~"
    m 6ekbsa "Além de ser o amor da minha vida, você é meu melhor amigo.{w=0.2} Nunca subestime o quanto você é importante para mim."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_we_have_all_the_time_in_the_world",
            prompt="Temos Todo o Tempo do Mundo",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_we_have_all_the_time_in_the_world(from_long=False):
    m 1dud "{i}{cps=18}~Temos todo {w=0.7}o tempo {w=0.7}do mundo~{/cps}{/i}"
    m 1eua "{i}{cps=22}~Tempo suficiente para a vida~{/cps}{/i}"
    m 3eub "{i}{cps=22}~Revelar {w=0.7}todos os tesouros~{/cps}{/i}"
    m 3hua "{i}{cps=22}~Que o amor guarda~{/cps}{/i}"

    m 1dub "{i}{cps=18}~Temos todo {w=0.7}o amor {w=0.7}do mundo~{/cps}{/i}"
    m 1esd "{i}{cps=22}~E se isso é tudo que temos {w=0.7}você verá~{/cps}{/i}"
    m 3dka "{i}{cps=22}~Que nada mais precisamos~{/cps}{/i}"

    if not from_long:
        m 1duu "..."
        m 1ekbsb "Você me fez a garota mais feliz do mundo, [player]. Sempre serei grata por isso."
        m 1hubsa "Espero fazer o mesmo por você~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_we_have_all_the_time_in_the_world_long",
            prompt="Temos Todo o Tempo do Mundo",
            category=[store.mas_songs.TYPE_LONG],
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_we_have_all_the_time_in_the_world_long:
    call mas_song_we_have_all_the_time_in_the_world (from_long=True)

    m 1dud "{i}{cps=18}~Cada passo {w=0.7}do caminho~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Nos encontrará~{/cps}{/i}"
    m 3eud "{i}{cps=18}~Com as preocupações {w=0.7}do mundo~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Bem distantes~{/cps}{/i}"

    m 1dud "{i}{cps=18}~Temos todo {w=0.7}o tempo {w=0.7}do mundo~{/cps}{/i}"
    m 1dubsa "{i}{cps=18}~Só para amar~{/cps}{/i}"
    m 3eubsb "{i}{cps=22}~Nada mais, {w=0.75}nada menos~{/cps}{/i}"
    m 1ekbsa "{i}{cps=18}~Só amor~{/cps}{/i}"

    m 1dud "{i}{cps=18}~Cada passo {w=0.75}do caminho~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Nos encontrará~{/cps}{/i}"
    m 1dua "{i}{cps=18}~Com as preocupações {w=0.7}do mundo~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Bem distantes~{/cps}{/i}"

    m 1eub "{i}{cps=18}~Temos todo {w=0.7}o tempo {w=0.7}do mundo~{/cps}{/i}"
    m 3ekbsa "{i}{cps=18}~Só para amar~{/cps}{/i}"
    m 1dkbsd "{i}{cps=22}~Nada mais, {w=0.75}nada menos~{/cps}{/i}"
    m 3dkbsb "{i}{cps=18}~Só amor~{/cps}{/i}"

    m 1ekbla "{i}{cps=18}~Só amor~{/cps}{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_when_you_say_nothing_at_all",
            prompt="Quando Você Não Diz Nada",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_when_you_say_nothing_at_all(from_long=False):
    m 1hubsb "{i}{cps=16}~Seu sorriso me mostra que é ao meu lado o seu lugar~{/cps}{/i}"
    m 3eubso "{i}{cps=16}~Seu olhar me promete que nunca vai me deixar~{/cps}{/i}"
    m 3dud "{i}{cps=16}~Seu toque me envolve e me impede de cair~{/cps}{/i}"
    m 1eud "{i}{cps=16}~Você diz muito mais{w=0.3} sem sequer me ouvir~{/cps}{/i}"

    if not from_long:
        m 1duu "..."
        m 1dkbsu "Não posso ver seu rosto, nem ler a verdade em seus olhos, ou sentir seu toque..."
        m 1ekbsa "Mas quando você passa tempo comigo sem dizer uma palavra, isso me diz tudo que preciso saber..."
        m 3hubsa "Que sou amada por alguém, e que você estará aqui nos meus dias difíceis."
        m 1dkbsu "E espero que você também se sinta amado por mim, mesmo quando não tenho nada novo para dizer."
        m 1ekbsa "Só de abrir o jogo e me ter ao seu lado já faz toda diferença para mim, [player]~"

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_when_you_say_nothing_at_all_long",
            prompt="Quando Você Não Diz Nada",
            category=[store.mas_songs.TYPE_LONG],
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_when_you_say_nothing_at_all_long:
    m 1dubsu "{i}{cps=18}~É incrível como você fala direto ao meu coração~{/cps}{/i}"
    m 3eubsb "{i}{cps=18}~Sem dizer palavra, ilumina a escuridão~{/cps}{/i}"
    m 3dud "{i}{cps=18}~Por mais que tente, nunca poderia explicar~{/cps}{/i}"
    m 3euo "{i}{cps=18}~O que ouço quando você se cala~{/cps}{/i}"

    call mas_song_when_you_say_nothing_at_all (from_long=True)

    m 3dud "{i}{cps=18}~O dia inteiro ouço pessoas falando~{/cps}{/i}"
    m 3dubsd "{i}{cps=18}~Mas quando me abraça{w=0.2} o mundo se cala~{/cps}{/i}"
    m 1dud "{i}{cps=18}~Nem o dicionário poderia definir~{/cps}{/i}"
    m 1dubso "{i}{cps=18}~O que se fala entre seu coração e o meu~{/cps}{/i}"

    call mas_song_when_you_say_nothing_at_all (from_long=True)

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_strawberry",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Morango",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_strawberry(from_long=False):
    m 1hub "{i}{cps=24}~Dizer que você é bonito~{/cps}{/i}"
    m 3eub "{i}{cps=26}~Seria como dizer que morango é doce~{/cps}{/i}"
    m 1eud "{i}{cps=26}~Pois um morango esconde sabores~{/cps}{/i}"
    m 3dkbsu "{i}{cps=26}~Que são fortes,{w=0.3} ácidos,{w=0.3} vermelhos,{w=0.3} intensos~{/cps}{/i}"
    m 3eub "{i}{cps=26}~E eu adoraria te encontrar~{/cps}{/i}"
    m 3hub "{i}{cps=26}~Crescendo livre na floresta~{/cps}{/i}"
    m 1rub "{i}{cps=28}~Faria um ca{w=0.1}sto com minha camiseta~{/cps}{/i}"
    m 3tub "{i}{cps=26}~E levar para casa o máximo que pudesse~{/cps}{/i}"

    if not from_long:
        m 1hubsu "..."
        m 3ekbsu "Mal posso esperar pelo dia em que estaremos [ju], [player]."
        m 3ekbsa "Mal posso esperar para olhar nos seus olhos novamente..."
        show monika 5rkbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5rkbsa "Mas por enquanto...{w=0.3}posso continuar sonhando com nossas futuras aventuras."
        m 5hubsu "Sei que ainda vai demorar, mas espero que esse sonho se torne realidade~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_strawberry_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Morango",
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_strawberry_long:
    call mas_song_strawberry (from_long=True)
    m 1sub "{i}{cps=26}~Dizer que você é lindo~{/cps}{/i}"
    m 3hub "{i}{cps=26}~Seria como dizer que o mar é azul~{/cps}{/i}"
    m 3dud "{i}{cps=26}~Pois o mar contém todas as cores~{/cps}{/i}"
    m 1ekb "{i}{cps=26}~E eu vejo todas elas quando te olho~{/cps}{/i}"
    m 2tsbsu "{i}{cps=26}~E quero te explorar~{/cps}{/i}"
    m 7hubsb "{i}{cps=26}~Descalço na areia~{/cps}{/i}"
    m 3rsbsb "{i}{cps=26}~Com as calças arregaçadas, em água até os tornozelos~{/cps}{/i}"
    m 1hub "{i}{cps=26}~Dizer que você é engraçado~{/cps}{/i}"
    m 3dud "{i}{cps=26}~Seria como dizer que o céu noturno é negro~{/cps}{/i}"
    m 3sub "{i}{cps=26}~Pois o céu contém estrelas{w=0.1} e cometas~{/cps}{/i}"
    m 3sub "{i}{cps=26}~E planetas que ninguém viu ainda~{/cps}{/i}"
    m 2eub "{i}{cps=26}~E quero te admirar~{/cps}{/i}"
    m 2dud "{i}{cps=26}~Deitado no meu jardim~{/cps}{/i}"
    m 2rsbsb "{i}{cps=26}~Tentando te compreender por completo~{/cps}{/i}"
    m 2esbsb "{i}{cps=26}~Mas você simplesmente não tem fim~{/cps}{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_save_the_last_dance_for_me",
            prompt="Guarde a Última Dança para Mim",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.LOVE,None)
        ),
        code="SNG"
    )

label mas_song_save_the_last_dance_for_me:
    call mas_song_save_the_last_dance_for_me_lyrics
    m 6dublu "..."
    m 7eua "Essa música é tão profunda para mim, [player]."
    m 3rubsu "Toda vez que a ouço, meu coração anseia por finalmente dançarmos juntos..."

    if not mas_getEVL_shown_count("mas_song_save_the_last_dance_for_me"):
        m 1eua "Na verdade tem uma história por trás dessa música, tem tempo para ouvir agora?{nw}"
        $ _history_list.pop()
        menu:
            m "Na verdade tem uma história por trás dessa música, tem tempo para ouvir agora?{fast}"
            "Sim.":

                call mas_song_save_the_last_dance_for_me_analysis (from_song=True)
            "Não.":

                m 3eua "Ah, tudo bem, me avise se quiser conversar sobre essa música depois, ok?"
    else:
        m 6rublb "Obrigada por continuar ouvindo meu coração ansioso..."
        m 6eubsa "Eu te amo, [player]~"
        return "love"

    return

label mas_song_save_the_last_dance_for_me_lyrics:
    m 1dud "{i}~Você pode dançar{w=0.3} com quem quiser~{/i}"
    m 3eud "{i}~Com quem te conquistar,{w=0.2} deixe-se abraçar~{/i}"
    m 3huu "{i}~Pode sorrir{w=0.3} para quem te fizer~{/i}"
    m 3eud "{i}~Segurar sua mão sob o luar~{/i}"
    m 4eublo "{i}~Mas não esqueça quem te levará pra casa~{/i}"
    m 4tublb "{i}~E em qual colo vai descansar~{/i}"
    m 6hublb "{i}~Então querida,{w=0.2} guarde a última dança pra mim~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_save_the_last_dance_for_me_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="Guarde a Última Dança para Mim",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.LOVE,None)
        ),
        code="SNG"
    )

label mas_song_save_the_last_dance_for_me_analysis(from_song=False):
    if not from_song:
        call mas_song_save_the_last_dance_for_me_lyrics
    else:

        m 3hub "Ótimo!"

    m 1eud "A história por trás dessa música pode parecer só mais uma declaração romântica de fidelidade."
    m 1duc "Mas na verdade é bem dramática e triste..."
    m 3ekc "Uma condição médica impediu um dos compositores,{w=0.1} Jerome Felder, de andar ou dançar em sua própria noite de núpcias."
    m 1rkd "Anos depois, esses sentimentos voltaram quando ele encontrou um convite de casamento que não haviam enviado."
    m 3rksdlc "Jerome sentiu ciúmes ao lembrar do irmão dançando com sua esposa no casamento, enquanto ele só podia assistir."
    m 3ekd "O vencedor do Grammy ficou paralítico por poliomielite na infância, e só se locomovia com auxílio de muletas ou cadeira de rodas."
    m 3eka "Ao compor a letra, ele queria um tom poético."
    m 3rkbla "Mesmo com um toque de ciúme, ele queria que fosse romântica."
    m 2dkc "Sabe...{w=0.3}essa barreira entre nós...{w=0.3}é como se fosse minha cadeira de rodas."
    m 2rkp "...E se for ser sincera,{w=0.1} fico com ciúmes de você poder dançar com alguém enquanto fico aqui observando."
    m 6ekblu "Então no final das contas, só espero que guarde a última dança pra mim~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_fly_me_to_the_moon",
            prompt="Leve-me à Lua",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_fly_me_to_the_moon:
    m 1dud "{i}~Leve-me à lua~{/i}"
    m 3sub "{i}~Entre as estrelas me deixe vagar~{/i}"
    m 3eub "{i}~Mostre-me como é a primavera~{/i}"
    m 3hub "{i}~Em Júpiter e em Marte~{/i}"
    m 3eub "{i}~Em outras palavras, segure minha mão~{/i}"
    m 1dud "{i}~Em outras palavras,{/i}{w=0.2}{nw}"
    extend 1dkbsu "{i} querido, me beije~{/i}"
    m 3eubsb "{i}~Encha meu peito de canções, deixe-me cantar sem parar~{/i}"
    m 3hkbsb "{i}~Você é tudo que eu almejo; {w=0.2}tudo que venero e amo~{/i}"
    m 1eud "{i}~Em outras palavras, seja sincero~{/i}"
    m "{i}~Em outras palavras, {/i}{nw}"
    extend 3fkbsb "{i}eu {w=0.2}te {w=0.2}amo~{/i}"
    m 3hubsb "E sempre vou amar!"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_heaven",
            prompt="Paraíso",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_heaven:
    m 1dsbsd "{i}~Querido, você é tudo que eu quero~{/i}"
    m 3dkbsd "{i}~Quando está aqui em meus braços~{/i}"
    m 3dubsd "{i}~É difícil até acreditar~{/i}"
    m 1eubsb "{i}~Que estamos no paraíso~{/i}"
    m 1eubso "{i}~E amor é tudo que preciso~{/i}"
    m 3ekbso "{i}~E eu encontrei no seu coração~{/i}"
    m 3ekbsd "{i}~Não é difícil ver~{/i}"
    m 3eubsb "{i}~Que estamos no paraíso~{/i}"
    m 1ekbfa "Não passa um dia sem que eu sonhe com nós [du] [ju], [player]."
    m 1rubsu "E algo me diz que não sou a única~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_can_you_feel_the_sunshine",
            prompt="Você Pode Sentir o Sol?",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_can_you_feel_the_sunshine:
    m 1dkd "{i}~Sem você, nada mais me anima~{/i}"
    m 1eka "{i}~Você também sente o sol que brilha?~{/i}"
    m 3hkb "{i}~Ele me aquece; {w=0.2}me faz renascer~{/i}"
    m 3hubsb "{i}~Com você aqui, quero você sempre perto de mim~{/i}"
    m 3eubsb "{i}~Pois tudo fica mais claro assim~{/i}"
    m 1hkbsu "{i}~E hoje será um dia mais iluminado~{/i}"
    m 1ekbla "Sempre que você vem, ilumina meu dia...{w=0.3}Espero fazer o mesmo por você, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_on_the_front_porch",
            prompt="Na Varanda",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_on_the_front_porch:
    m 5dkbsd "{i}~Quando o dia findar, só quero ficar~{/i}"
    m 5fkbsu "{i}~Aqui na varanda contigo a sonhar~{/i}"
    m 5hubsb "{i}~No balanço vão, ouvindo o sabiá~{/i}"
    m 5dubsu "{i}~Vendo vaga-lumes e nosso amor brilhar~{/i}"
    m 5dkbsb "{i}~Como o tempo voa, a lua à toa~{/i}"
    m 5ekbsu "{i}~O ar tão doce enquanto o céu contemplamos~{/i}"
    m 5ekbstpu "{i}~Queria ficar assim pra sempre aqui~{/i}"
    m 5dkbstpu "{i}~De mãos dadas e um beijo {/i}{w=0.2}{nw}"
    extend 5gkbstub "{i}ou dois {/i}{w=0.2}{nw}"
    extend 5ekbstuu "{i}na varanda com você~{/i}"
    m 5dkbstda "..."
    m 5hkblb "Desculpe se fiquei muito emotiva, ahaha!"
    m 5rka "Mas você não pode me culpar, né?"
    m 5eka "Afinal, fazer algo assim [ju] seria...{w=0.3}{nw}"
    extend 5dkbsu "simplesmente maravilhoso~"
    return






init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_plays_yr",
            category=['monika','música'],
            prompt="Você pode tocar 'Your Reality' para mim?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST}
        )
    )

label mas_monika_plays_yr(skip_leadin=False):
    if not skip_leadin:
        if not renpy.seen_audio(songs.FP_YOURE_REAL) and not persistent.monika_kill:
            m 2eksdlb "Ah, ahaha! Você quer que eu toque a versão original, [player]?"
            m 2eka "Apesar de nunca ter tocado pra você, imagino que tenha ouvido na trilha sonora ou no YouTube, né?"
            m 2hub "O final não é meu favorito, mas ficarei feliz em tocar para você!"
            m 2eua "Deixe-me pegar o piano.{w=0.5}.{w=0.5}.{nw}"
        else:

            m 3eua "Claro, deixe-me pegar o piano.{w=0.5}.{w=0.5}.{nw}"

    window hide
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)
    show monika at rs32
    hide monika
    pause 3.0
    show mas_piano zorder MAS_MONIKA_Z+1 at lps32, rps32
    pause 5.0
    show monika zorder MAS_MONIKA_Z at ls32
    show monika 6dsa

    if store.songs.hasMusicMuted():
        $ enable_esc()
        m 6hua "Não se esqueça de aumentar o volume do jogo, [player]!"
        $ disable_esc()

    window hide
    call mas_timed_text_events_prep

    pause 2.0
    $ mas_play_song(store.songs.FP_YOURE_REAL,loop=False)


    show monika 6hua
    $ renpy.pause(10.012)
    show monika 6eua_static
    $ renpy.pause(5.148)
    show monika 6hua
    $ renpy.pause(3.977)
    show monika 6eua_static
    $ renpy.pause(5.166)
    show monika 6hua
    $ renpy.pause(3.743)
    show monika 6esa
    $ renpy.pause(9.196)
    show monika 6eka
    $ renpy.pause(13.605)
    show monika 6dua
    $ renpy.pause(9.437)
    show monika 6eua_static
    $ renpy.pause(5.171)
    show monika 6dua
    $ renpy.pause(3.923)
    show monika 6eua_static
    $ renpy.pause(5.194)
    show monika 6dua
    $ renpy.pause(3.707)
    show monika 6eka
    $ renpy.pause(16.884)
    show monika 6dua
    $ renpy.pause(20.545)
    show monika 6eka_static
    $ renpy.pause(4.859)
    show monika 6dka
    $ renpy.pause(4.296)
    show monika 6eka_static
    $ renpy.pause(5.157)
    show monika 6dua
    $ renpy.pause(8.064)
    show monika 6eka
    $ renpy.pause(22.196)
    show monika 6dka
    $ renpy.pause(3.630)
    show monika 6eka_static
    $ renpy.pause(1.418)
    show monika 6dka
    $ renpy.pause(9.425)
    show monika 5dka with dissolve_monika
    $ renpy.pause(5)

    show monika 6eua at rs32 with dissolve_monika
    pause 1.0
    hide monika
    pause 3.0
    hide mas_piano
    pause 6.0
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    pause 1.0
    call monika_zoom_transition (mas_temp_zoom_level, 1.0)
    call mas_timed_text_events_wrapup
    window auto

    $ mas_unlockEVL("monika_piano_lessons", "EVE")
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_plays_or",
            category=['monika','música'],
            prompt="Você pode tocar 'Our Reality' para mim?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST}
        )
    )

label mas_monika_plays_or(skip_leadin=False):
    if not skip_leadin:
        m 3eua "Claro, só me deixe pegar o piano.{w=0.5}.{w=0.5}.{nw}"

    if persistent.gender == "F":
        $ gen = "seu"
    elif persistent.gender == "M":
        $ gen = "seu"
    else:
        $ gen = "seu"

    window hide
    call mas_timed_text_events_prep
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)
    show monika at rs32
    hide monika
    pause 3.0
    show mas_piano zorder MAS_MONIKA_Z+1 at lps32, rps32
    pause 5.0
    show monika zorder MAS_MONIKA_Z at ls32
    show monika 6dsa

    if store.songs.hasMusicMuted():
        $ enable_esc()
        m 6hua "Não se esqueça de aumentar o volume do jogo, [player]!"
        $ disable_esc()

    pause 2.0
    $ mas_play_song(songs.FP_PIANO_COVER, loop=False)

    show monika 1dsa
    pause 9.15
    m 1eua "{i}{cps=10}Todo dia,{w=0.5} {/cps}{cps=15}eu imagino um futuro onde{w=0.22} {/cps}{cps=13}eu possa estar com você{w=4.10}{/cps}{/i}{nw}"
    m 1eka "{i}{cps=12}Em minha mão{w=0.5} {/cps}{cps=17}há uma caneta que escreverá um poema{w=0.5} {/cps}{cps=16}sobre mim e você{w=4.10}{/cps}{/i}{nw}"
    m 1eua "{i}{cps=16}A tinta escorre{w=0.25} {/cps}{cps=10}em uma poça escura{w=1}{/cps}{/i}{nw}"
    m 1eka "{i}{cps=18}Apenas mova sua mão,{w=0.45} {/cps}{cps=20}escreva o caminho até o [gen] coração{w=1.40}{/cps}{/i}{nw}"
    m 1dua "{i}{cps=15}Mas neste mundo{w=0.25} {/cps}{cps=11}de escolhas infinitas{w=0.90}{/cps}{/i}{nw}"
    m 1eua "{i}{cps=16}O que será preciso{w=0.25}{/cps}{cps=18} para encontrar aquele dia especial{/cps}{/i}{w=0.90}{nw}"
    m 1dsa "{i}{cps=15}O que será preciso{w=0.50} para encontrar{w=1} aquele dia especial{/cps}{/i}{w=1.82}{nw}"
    pause 7.50

    m 1eua "{i}{cps=15}Será que hoje{w=0.5} {/cps}{cps=15}dei a todos uma tarefa divertida{w=0.30} {/cps}{cps=12}para fazer?{w=4.20}{/cps}{/i}{nw}"
    m 1hua "{i}{cps=18}Quando você está aqui,{w=0.25} {/cps}{cps=13.25}tudo que fazemos já é divertido pra eles, de qualquer forma{w=4}{/cps}{/i}{nw}"
    m 1esa "{i}{cps=11}Quando nem consigo entender meus próprios sentimentos{/cps}{w=1}{/i}{nw}"
    m 1eka "{i}{cps=17}De que servem as palavras,{w=0.3} se um sorriso diz tudo?{/cps}{/i}{w=1}{nw}"
    m 1lua "{i}{cps=11}E se este mundo não escrever um final pra mim{/cps}{/i}{w=0.9}{nw}"
    m 1dka "{i}{cps=18}O que será preciso{w=0.5} para que eu tenha tudo?{/cps}{/i}{w=2}{nw}"
    show monika 1dsa
    pause 17.50

    m 1eka "{i}{cps=15}Neste mundo,{w=0.5} {/cps}{cps=15}distante de quem sempre {/cps}{cps=17}será querido pra mim{/cps}{w=4.5}{/i}{nw}"
    m 1ekbsa "{i}{cps=15}Você, meu amor,{w=0.5} {/cps}{cps=16.5}guarda a chave do dia em que eu serei finalmente livre{/cps}{w=8.5}{/i}{nw}"
    m 1eua "{i}{cps=16}A tinta escorre{w=0.25} {/cps}{cps=10}em uma poça escura{/cps}{w=1.2}{/i}{nw}"
    m 1esa "{i}{cps=18}Como posso atravessar{w=0.45} {/cps}{cps=13}para a sua realidade?{/cps}{w=1.40}{/i}{nw}"
    m 1eka "{i}{cps=12}Onde eu possa ouvir o som do seu coração{/cps}{w=0.8}{/i}{nw}"
    m 1ekbsa "{i}{cps=16}E transformá-lo em amor,{w=0.6} mesmo na nossa realidade{/cps}{/i}{w=0.6}{nw}"
    m 1hubsa "{i}{cps=16}E na nossa realidade,{w=1} sabendo que eu te amarei para sempre{/cps}{w=4.2}{/i}{nw}"
    m 1ekbsa "{i}{cps=19}Com você, eu estarei{/cps}{/i}{w=2}{nw}"

    show monika 1dkbsa
    pause 9.0
    show monika 6eua at rs32
    pause 1.0
    hide monika
    pause 3.0
    hide mas_piano
    pause 6.0
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    pause 1.0
    call monika_zoom_transition (mas_temp_zoom_level, 1.0)
    call mas_timed_text_events_wrapup
    window auto

    $ mas_unlockEVL("monika_piano_lessons", "EVE")
    return
