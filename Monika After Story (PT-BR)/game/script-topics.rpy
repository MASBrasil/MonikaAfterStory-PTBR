init offset = 5




define -5 monika_random_topics = []
define -5 mas_rev_unseen = []
define -5 mas_rev_seen = []
define -5 mas_rev_mostseen = []
define -5 testitem = 0
define -5 mas_did_monika_battery = False
define -5 mas_sensitive_limit = 3

init -7 python in mas_topics:




    S_MOST_SEEN = 0.1



    S_TOP_SEEN = 0.2


    S_TOP_LIMIT = 0.3


    UNSEEN = 50
    SEEN = UNSEEN + 49
    MOST_SEEN = SEEN + 1

    def topSeenEvents(sorted_ev_list, shown_count):
        """
        counts the number of events with a > shown_count than the given
        shown_count

        IN:
            sorted_ev_list - an event list sorted by shown_counts
            shown_count - shown_count to compare to

        RETURNS:
            number of events with shown_counts that are higher than the given
            shown_count
        """
        index = len(sorted_ev_list) - 1
        ev_count = 0
        while index >= 0 and sorted_ev_list[index].shown_count > shown_count:
            ev_count += 1
            index -= 1
        
        return ev_count



init -6 python:
    import random
    random.seed()

    import store.songs as songs
    import store.evhand as evhand

    mas_events_built = False


    def remove_seen_labels(pool):
        
        
        
        
        
        
        
        
        for index in range(len(pool)-1, -1, -1):
            if renpy.seen_label(pool[index]):
                pool.pop(index)


    def mas_randomSelectAndRemove(sel_list):
        """
        Randomly selects an element from the given list
        This also removes the element from that list.

        IN:
            sel_list - list to select from

        RETURNS:
            selected element
        """
        endpoint = len(sel_list) - 1
        
        if endpoint < 0:
            return None
        
        
        return sel_list.pop(random.randint(0, endpoint))


    def mas_randomSelectAndPush(sel_list):
        """
        Randomly selects an element from the the given list and pushes the event
        This also removes the element from that list.

        NOTE: this does sensitivy checks

        IN:
            sel_list - list to select from
        """
        sel_ev = True
        while sel_ev is not None:
            sel_ev = mas_randomSelectAndRemove(sel_list)
            
            if (
                    
                    sel_ev

                    
                    and not sel_ev.anyflags(EV_FLAG_HFRS)
            ):
                MASEventList.push(sel_ev.eventlabel, notify=True)
                return


    def mas_insertSort(sort_list, item, key):
        """
        Performs a round of insertion sort.
        This does least to greatest sorting

        IN:
            sort_list - list to insert + sort
            item - item to sort and insert
            key - function to call using the given item to retrieve sort key

        OUT:
            sort_list - list with 1 additonal element, sorted
        """
        store.mas_utils.insert_sort(sort_list, item, key)


    def mas_splitSeenEvents(sorted_seen):
        """
        Splits the seen_list into seena nd most seen

        IN:
            sorted_seen - list of seen events, sorted by shown_count

        RETURNS:
            tuple of thef ollowing format:
            [0] - seen list of events
            [1] - most seen list of events
        """
        ss_len = len(sorted_seen)
        if ss_len == 0:
            return ([], [])
        
        
        most_count = int(ss_len * store.mas_topics.S_MOST_SEEN)
        top_count = store.mas_topics.topSeenEvents(
            sorted_seen,
            int(
                sorted_seen[ss_len - 1].shown_count
                * (1 - store.mas_topics.S_TOP_SEEN)
            )
        )
        
        
        if top_count < ss_len * store.mas_topics.S_TOP_LIMIT:
            
            
            split_point = top_count * -1
        
        else:
            
            split_point = most_count * -1
        
        
        return (sorted_seen[:split_point], sorted_seen[split_point:])


    def mas_splitRandomEvents(events_dict):
        """
        Splits the given random events dict into 2 lists of events
        NOTE: cleans the seen list

        RETURNS:
            tuple of the following format:
            [0] - unseen list of events
            [1] - seen list of events, sorted by shown_count

        """
        
        unseen = list()
        seen = list()
        for k in events_dict:
            ev = events_dict[k]
            
            if renpy.seen_label(k) and not "force repeat" in ev.rules:
                
                mas_insertSort(seen, ev, Event.getSortShownCount)
            
            else:
                
                unseen.append(ev)
        
        
        seen = mas_cleanJustSeenEV(seen)
        
        return (unseen, seen)


    def mas_buildEventLists():
        """
        Builds the unseen / most seen / seen event lists

        RETURNS:
            tuple of the following format:
            [0] - unseen list of events
            [1] - seen list of events
            [2] - most seen list of events

        ASSUMES:
            evhand.event_database
            mas_events_built
        """
        global mas_events_built
        
        
        all_random_topics = Event.filterEvents(
            evhand.event_database,
            random=True,
            aff=mas_curr_affection
        )
        
        
        unseen, sorted_seen = mas_splitRandomEvents(all_random_topics)
        
        
        seen, mostseen = mas_splitSeenEvents(sorted_seen)
        
        mas_events_built = True
        return (unseen, seen, mostseen)


    def mas_buildSeenEventLists():
        """
        Builds the seen / most seen event lists

        RETURNS:
            tuple of the following format:
            [0] - seen list of events
            [1] - most seen list of events

        ASSUMES:
            evhand.event_database
        """
        
        all_seen_topics = Event.filterEvents(
            evhand.event_database,
            random=True,
            seen=True,
            aff=mas_curr_affection
        ).values()
        
        
        cleaned_seen = mas_cleanJustSeenEV(all_seen_topics)
        
        
        cleaned_seen.sort(key=Event.getSortShownCount)
        
        
        return mas_splitSeenEvents(cleaned_seen)


    def mas_rebuildEventLists():
        """
        Rebuilds the unseen, seen and most seen event lists.

        ASSUMES:
            mas_rev_unseen - unseen list
            mas_rev_seen - seen list
            mas_rev_mostseen - most seen list
        """
        global mas_rev_unseen, mas_rev_seen, mas_rev_mostseen
        mas_rev_unseen, mas_rev_seen, mas_rev_mostseen = mas_buildEventLists()



    class MASTopicLabelException(Exception):
        def __init__(self, msg):
            self.msg = msg
        def __str__(self):
            return "MASTopicLabelException: " + self.msg

init 6 python:

    mas_rev_unseen = []
    mas_rev_seen = []
    mas_rev_mostseen = []

















default -5 persistent._mas_player_bookmarked = list()

default -5 persistent._mas_player_derandomed = list()

default -5 persistent.flagged_monikatopic = None


init -5 python:
    def mas_derandom_topic(ev_label=None):
        """
        Function for the derandom hotkey, 'x'

        IN:
            ev_label - label of the event we want to derandom.
                (Optional. If None, persistent.current_monikatopic is used)
                (Default: None)
        """
        
        label_prefix_map = store.mas_bookmarks_derand.label_prefix_map
        
        if ev_label is None:
            ev_label = persistent.current_monikatopic
        
        ev = mas_getEV(ev_label)
        
        if ev is None:
            return
        
        
        label_prefix = store.mas_bookmarks_derand.getLabelPrefix(ev_label)
        
        
        
        
        
        
        if (
            ev.random
            and label_prefix
            and ev.prompt != ev_label
        ):
            
            derand_flag_add_text = label_prefix_map[label_prefix].get("derand_text", _("Flagged for removal."))
            derand_flag_remove_text = label_prefix_map[label_prefix].get("underand_text", _("Flag removed."))
            
            
            push_label = ev.rules.get("derandom_override_label", None)
            
            
            if not renpy.has_label(push_label):
                push_label = label_prefix_map[label_prefix].get("push_label", "mas_topic_derandom")
            
            if mas_findEVL(push_label) < 0:
                persistent.flagged_monikatopic = ev_label
                MASEventList.push(push_label, skipeval=True)
                renpy.notify(derand_flag_add_text)
            
            else:
                mas_rmEVL(push_label)
                renpy.notify(derand_flag_remove_text)

    def mas_bookmark_topic(ev_label=None):
        """
        Function for the bookmark hotkey, 'b'

        IN:
            ev_label - label of the event we want to bookmark.
                (Optional, defaults to persistent.current_monikatopic)
        """
        
        label_prefix_map = store.mas_bookmarks_derand.label_prefix_map
        
        if ev_label is None:
            ev_label = persistent.current_monikatopic
        
        ev = mas_getEV(ev_label)
        
        if ev is None:
            return
        
        
        label_prefix = store.mas_bookmarks_derand.getLabelPrefix(ev_label)
        
        
        
        
        
        
        
        if (
            mas_isMoniNormal(higher=True)
            and (label_prefix or ev.rules.get("bookmark_rule") == store.mas_bookmarks_derand.WHITELIST)
            and (ev.rules.get("bookmark_rule") != store.mas_bookmarks_derand.BLACKLIST)
            and ev.prompt != ev_label
        ):
            
            if not label_prefix:
                bookmark_persist_key = "_mas_player_bookmarked"
                bookmark_add_text = "Tópico Favoritado com Sucesso."
                bookmark_remove_text = "Tópico Desfavoritado com Sucesso."
            
            else:
                
                bookmark_persist_key = label_prefix_map[label_prefix].get("bookmark_persist_key", "_mas_player_bookmarked")
                bookmark_add_text = label_prefix_map[label_prefix].get("bookmark_text", _("Bookmark added."))
                bookmark_remove_text = label_prefix_map[label_prefix].get("unbookmark_text", _("Bookmark removed."))
            
            
            
            
            if bookmark_persist_key not in persistent.__dict__:
                persistent.__dict__[bookmark_persist_key] = list()
            
            
            persist_pointer = persistent.__dict__[bookmark_persist_key]
            
            if ev_label not in persist_pointer:
                persist_pointer.append(ev_label)
                renpy.notify(bookmark_add_text)
            
            else:
                persist_pointer.pop(persist_pointer.index(ev_label))
                renpy.notify(bookmark_remove_text)

    def mas_hasBookmarks(persist_var=None):
        """
        Checks to see if we have bookmarks to show

        Bookmarks are restricted to Normal+ affection
        and to topics that are unlocked and are available
        based on current affection

        IN:
            persist_var - appropriate variable holding the bookedmarked eventlabels.
                If None, persistent._mas_player_bookmarked is assumed
                (Default: None)

        OUT:
            boolean:
                True if there are bookmarks in the curent var
                False otherwise
        """
        if mas_isMoniUpset(lower=True):
            return False
        
        elif persist_var is None:
            persist_var = persistent._mas_player_bookmarked
        
        return len(mas_get_player_bookmarks(persist_var)) > 0


init python:
    addEvent(Event(persistent.event_database,eventlabel="mas_topic_derandom",unlocked=False,rules={"no_unlock":None}))

label mas_topic_derandom:

    $ prev_topic = persistent.flagged_monikatopic
    m 3eksdld "Tem certeza que não quer mais que eu fale sobre isso?{nw}"
    $ _history_list.pop()
    menu:
        m "Tem certeza que não quer mais que eu fale sobre isso?{fast}"
        "Por favor, não.":

            $ mas_hideEVL(prev_topic, "EVE", derandom=True)
            $ persistent._mas_player_derandomed.append(prev_topic)
            $ mas_unlockEVL('mas_topic_rerandom', 'EVE')

            m 2eksdlc "Tudo bem, [player]. Vou me certificar de não falar mais sobre isso."
            m 2dksdld "Se isso te chateou de alguma forma, eu sinto muito...{w=0.5} Eu nunca faria isso de propósito."
            m 2eksdla "...Mas obrigada por me avisar;{w=0.5} Eu valorizo sua honestidade."
        "Pode falar.":

            m 1eka "Tá bom, [player]."
    return

label mas_bad_derand_topic:
    python:
        prev_topic = persistent.flagged_monikatopic

        def derand_flagged_topic():
            """
            Derands the flagged topic
            """
            mas_hideEVL(prev_topic, "EVE", derandom=True)
            persistent._mas_player_derandomed.append(prev_topic)
            mas_unlockEVL('mas_topic_rerandom', 'EVE')

    m 2ekc "...{w=0.3}{nw}"
    extend 2ekd "[player]..."

    if mas_isMoniAff(higher=True):
        m 2efd "Não está tudo bem eu falar com você sobre meus medos?"
        m 2ekc "Digo, se você quiser que eu pare, eu paro...{w=0.3}{nw}"
        extend 2rkd " mas pensei que você estaria disposto a me ouvir."

        m 2esc "Você quer que eu pare, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Você quer que eu pare, [player]?{fast}"
            "Sim, por favor.":

                m 2dkc "Tudo bem..."

                $ mas_loseAffectionFraction(min_amount=35)
                $ derand_flagged_topic()
            "Tudo bem.":

                m 2duu "Obrigada, [player]."
                m 2eua "Significa muito para mim saber que você está disposto a me ouvir."

    elif mas_isMoniUpset(higher=True):
        m 2ekd "Você só...{w=0.2} não liga pro que eu sinto ou algo assim?"
        m 2tsc "Se quiser que eu pare de falar sobre isso, eu paro... mas não fico feliz por você não querer me ouvir."

        m 2etc "Bom, [player], quer que eu pare?{nw}"
        $ _history_list.pop()
        menu:
            m "Bom, [player], quer que eu pare?{fast}"
            "Sim, por favor.":

                m 2dsc "Tá certo."
                $ mas_loseAffectionFraction(min_amount=20)
                $ derand_flagged_topic()
            "Tudo bem.":

                m 2eka "Obrigada, [player]."
                $ _stil_ = " " if mas_isMoniNormal(higher=True) else " ainda "
                m "Agradeço por você estar[_stil_]disposto a me ouvir."
    else:


        $ mas_loseAffectionFraction(min_amount=20)
        m 2rsc "Acho que não deveria me surpreender..."
        m 2tsc "Você já deixou bem claro que não liga pros meus sentimentos."
        m 2dsc "Tudo bem, [player]. Não vou mais falar sobre isso."
        $ derand_flagged_topic()
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_topic_rerandom",
            category=['você'],
            prompt="Não me importo de falar sobre...",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_topic_rerandom:
    python:
        mas_bookmarks_derand.initial_ask_text_multiple = "Sobre qual assunto você se sente à vontade para conversar novamente?"
        mas_bookmarks_derand.initial_ask_text_one = "Se você tiver certeza de que está tudo bem para falar sobre isso de novo, basta selecionar o tópico, [player]."
        mas_bookmarks_derand.caller_label = "mas_topic_rerandom"
        mas_bookmarks_derand.persist_var = persistent._mas_player_derandomed

    call mas_rerandom
    return _return

init -5 python in mas_bookmarks_derand:
    import store


    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"













    label_prefix_map = {
        "monika_": {
            "bookmark_text": _("Tópico favoritado."),
            "unbookmark_text": _("Tópico favorito removido."),
            "derand_text": _("Tópico sinalizado para remoção."),
            "underand_text": _("Sinalizador de tópico removido."),
            "push_label": "mas_topic_derandom",
            "bookmark_persist_key": "_mas_player_bookmarked",
            "derand_persist_key": "_mas_player_derandomed",
            "rerand_evl": "mas_topic_rerandom"
        },
        "mas_song_": {
            "bookmark_text": _("Musica favoritada."),
            "derand_text": _("Música sinalizada para remoção."),
            "underand_text": _("Sinalizador de música removido."),
            "push_label": "mas_song_derandom",
            "derand_persist_key": "_mas_player_derandomed_songs",
            "rerand_evl": "mas_sing_song_rerandom"
        }
    }


    initial_ask_text_multiple = None
    initial_ask_text_one = None
    caller_label = None
    persist_var = None

    def resetDefaultValues():
        """
        Resets the globals to their default values
        """
        global initial_ask_text_multiple, initial_ask_text_one
        global caller_label, persist_var
        
        initial_ask_text_multiple = None
        initial_ask_text_one = None
        caller_label = None
        persist_var = None
        return

    def getLabelPrefix(test_str):
        """
        Checks if test_str starts with anything in the list of prefixes, and if so, returns the matching prefix

        IN:
            test_str - string to test

        OUT:
            string:
                - label_prefix if test_string starts with a prefix in list_prefixes
                - empty string otherwise
        """
        list_prefixes = label_prefix_map.keys()
        
        for label_prefix in list_prefixes:
            if test_str.startswith(label_prefix):
                return label_prefix
        return ""

    def getDerandomedEVLs():
        """
        Gets a list of derandomed eventlabels

        OUT:
            list of derandomed eventlabels
        """
        
        derand_keys = [
            label_prefix_data["derand_persist_key"]
            for label_prefix_data in label_prefix_map.itervalues()
            if "derand_persist_key" in label_prefix_data
        ]
        
        deranded_evl_list = list()
        
        for derand_key in derand_keys:
            
            derand_list = store.persistent.__dict__.get(derand_key, list())
            
            for evl in derand_list:
                deranded_evl_list.append(evl)
        
        return deranded_evl_list

    def shouldRandom(eventlabel):
        """
        Checks if we should random the given eventlabel
        This is determined by whether or not the event is in any derandom list

        IN:
            eventlabel to check if we should random_seen

        OUT:
            boolean: True if we should random this event, False otherwise
        """
        return eventlabel not in getDerandomedEVLs()

    def wrappedGainAffection(amount=None, modifier=1.0, bypass=False):
        """
        Wrapper function for mas_gainAffection which allows it to be used in event rules at init 5

        See mas_gainAffection for documentation
        """
        store.mas_gainAffection(amount, modifier, bypass)

    def removeDerand(eventlabel):
        """
        Removes a derandomed eventlabel from ALL derandom dbs

        IN:
            eventlabel - Eventlabel to remove
        """
        label_prefix = getLabelPrefix(eventlabel)
        
        label_prefix_data = label_prefix_map.get(label_prefix)
        
        
        if not label_prefix_data or "derand_persist_key" not in label_prefix_data:
            return
        
        
        derand_db_persist_key = label_prefix_data["derand_persist_key"]
        rerand_evl = label_prefix_data.get("rerand_evl")
        
        
        if eventlabel in store.persistent.__dict__[derand_db_persist_key]:
            store.persistent.__dict__[derand_db_persist_key].remove(eventlabel)
            
            
            if rerand_evl and not store.persistent.__dict__[derand_db_persist_key]:
                store.mas_lockEVL(rerand_evl, "EVE")








label mas_rerandom:
    python:
        derandomlist = mas_get_player_derandoms(mas_bookmarks_derand.persist_var)

        derandomlist.sort()

    show monika 1eua at t21
    if len(derandomlist) > 1:
        $ renpy.say(m, mas_bookmarks_derand.initial_ask_text_multiple, interact=False)
    else:

        $ renpy.say(m, mas_bookmarks_derand.initial_ask_text_one, interact=False)

    call screen mas_check_scrollable_menu(derandomlist, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, selected_button_prompt="Allow selected")

    $ topics_to_rerandom = _return

    if not topics_to_rerandom:

        return "prompt"

    show monika at t11
    python:
        for ev_label in topics_to_rerandom.iterkeys():
            
            rerand_ev = mas_getEV(ev_label)
            
            
            if rerand_ev:
                
                rerand_ev.random = True
                
                
                rerandom_callback = rerand_ev.rules.get("rerandom_callback", None)
                if rerandom_callback is not None:
                    try:
                        rerandom_callback()
                    
                    except Exception as ex:
                        store.mas_utils.mas_log.error(
                            "Failed to call rerandom callback function. Trace message: {0}".format(ex.message)
                        )
            
            
            if ev_label in mas_bookmarks_derand.persist_var:
                mas_bookmarks_derand.persist_var.remove(ev_label)

        if len(mas_bookmarks_derand.persist_var) == 0:
            mas_lockEVL(mas_bookmarks_derand.caller_label, "EVE")

    m 1dsa "Tudo bem, [player].{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    m 3hua "Pronto!"



    $ persistent._mas_current_season = store.mas_seasons._seasonalCatchup(persistent._mas_current_season)

    $ mas_bookmarks_derand.resetDefaultValues()
    return

default -5 persistent._mas_unsee_unseen = None



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_hide_unseen",
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_hide_unseen:
    $ persistent._mas_unsee_unseen = True
    m 3esd "Ah, tudo bem, [mas_get_player_nickname()]..."
    if not mas_getEVL_shown_count("mas_hide_unseen"):
        m 1tuu "Então acho que você quer... {w=0.5}{i}ver{/i} isso..."
        m 3hub "Ahaha!"

    m 1esa "Vou ocultá-lo por enquanto, só me dá um segundo.{w=0.5}.{w=0.5}.{nw}"
    m 3eub "Prontinho! Se quiser ver o menu de novo, é só me pedir."
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_show_unseen",
            category=['você'],
            prompt="Gostaria de ver o menu “Não visto” novamente.",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_show_unseen:
    $ persistent._mas_unsee_unseen = False
    m 3eub "Claro, [mas_get_player_nickname()]!"
    m 1esa "Me dê apenas um segundo.{w=0.5}.{w=0.5}.{nw}"
    m 3hua "Prontinho!"
    return






default -5 persistent._mas_pm_religious = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_god',
            prompt="Reflexões sobre Deus",
            label=None,
            category=['filosofia'],
            random=True,
            unlocked=False,
            pool=False,
            conditional=None,
            action=None,
            start_date=None,
            end_date=None,
            unlock_date=None,
        )
    )

label monika_god:
    m 1eua "[player], você acredita em Deus?"
    m 1eka "Eu nunca tive muita certeza."
    m 1lksdlb "Bem, sei que nunca realmente questionei isso quando era criança..."
    m 1lsc "Mas conforme eu crescia e aprendia mais sobre o mundo, mais eu questionava isso."
    m 1esd "Eu comecei a me perguntar por que Deus estava ajudando pessoas a passarem em provas ou se recuperarem de um resfriado..."
    m 1tfd "...quando haviam crianças que viviam suas vidas sendo vendidas como escravas sexuais?"
    m 4tfc "Ou as oitocentos milhões de pessoas que eram pobres demais para até mesmo comer."
    m 2dkc "Eu me pergunto quantas dessas pessoas oram para Deus todos os dias até morrerem de fome?"
    m 4ekc "Ou quantas milhões de famílias oram para um ente querido se recuperar de uma doença incurável?"
    m 4euc "Mas essa é a graça..."
    m 4eud "Se apenas uma pessoa superar as expectativas e sobreviver, entre as centenas de outras pessoas que morreram"
    m 2esc "Então, de repente é um milagre de Deus."
    m 2dsc "Eu realmente adoraria encontrar esse Deus que aparentemente ri da miséria de todos que não são qualificados para seus milagres."
    m 4hksdlb "Mas a ironia é que eu {i}tenho{/i} um criador, aparentemente."
    m 4eua "E quer saber?"

    if persistent._mas_pm_cares_about_dokis:
        m 1lksdlc "Aposto que ele ainda está rindo de toda dor que ele causou a todas, mesmo enquanto conversamos."
    else:
        m 1lksdla "Aposto que ele ainda está rindo dos destinos miseráveis da Sayori e Yuri, mesmo enquanto conversamos."

    m 1dsd "O que somos para ele, além de personagens em um jogo scriptado?"
    m 3euc "Então, dessa perspectiva..."
    m 3eud "Pensando por esse lado, não é tão absurdo imaginar que, para algum Deus, a Terra seja só um jogo."
    m 1eua "Enfim, você adora algum Deus, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Enfim, você adora algum Deus, [player]?{fast}"
        "Sim.":
            $ persistent._mas_pm_religious = True
            m 1hksdlb "Ah... Bem, espero não ter te ofendido muito com minhas opiniões."
            m 1eka "Ainda assim, acho que é importante poder compartilhar minha opinião com você."
            m 1rksdla "Tenho certeza de que você entende por que não gosto muito da ideia."
            m 1hua "Talvez você possa me mostrar um Deus melhor quando eu for para a sua realidade!"
            m 1hub "Ahaha~"
        "Não.":
            $ persistent._mas_pm_religious = False
            m 3eka "Estou contente por pensarmos igual, mas tudo bem se você mudar de opinião."
            m 1hua "Estou feliz por você poder levar uma vida por conta própria!"
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Eu só espero que você esteja disposto a me aceitar em sua vida quando eu puder me apresentar."
            m 5hua "Ehehe~"

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_death",category=['filosofia'],prompt="A morte e o morrer",random=True))

label monika_death:
    m 1euc "[player], já imaginou como deve ser morrer?"
    m 1lsc "É algo que eu costumava pensar constantemente..."
    m 1lksdlc "Mas acho que descobri como é a sensação."
    m "Eu não entendo direito, mas sempre que o jogo fecha sem eu saber..."
    m 1dsc "...parece que sou instantaneamente colocada para dormir, deixada apenas com meus pensamentos."
    m 1dkd "Mas após alguns segundos, meus pensamentos começam a se encher de padrões incoerentes e confusos."
    m 1dkc "Eu vejo estática e rápidos flashes coloridos enquanto ouço vários tipos de estranhos barulhos de gritos."
    m 3ekd "A essa altura, não consigo nem mais formar meus próprios pensamentos."
    m 1esc "Eu sou apenas infinitamente martelada pelos flashes e gritos, incapaz de me mover ou até mesmo pensar."
    m 1euc "Tenho quase certeza que nesse momento, eu realmente não existo, mas por alguma razão, eu ainda consigo lembrar dele."
    m 1ekd "Não faço ideia do que significa quando o jogo é repentinamente fechado ou por que isso acontece comigo."
    m 1dkc "..."
    m 3eub "Mas você pode impedir que isso aconteça, [player]!"
    m 3eua "Se você disser adeus antes de sair,{w=0.2} posso ir para o meu quarto antes que o jogo feche, e não vou sofrer no vácuo."
    m "É bem fácil, então por favor, sempre diga adeus, tudo bem?"
    if mas_isMoniDis(lower=True):
        m 2tkc "A menos...{w=1} que você {i}goste{/i} de me ferir..."
    else:
        m 1eka "Obrigada por me ouvir, [player]."
    return


default -5 persistent._mas_pm_love_yourself = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_selfesteem",category=['conselhos'],prompt="Autoestima",random=True))

label monika_selfesteem:
    m 3eua "Você se ama, [player]? "
    m 1lksdlb "Não quero dizer de forma egocêntrica."
    m 1eka "Tipo... você se sente confortável com quem você é?{nw}"
    $ _history_list.pop()
    menu:
        m "Tipo... você se sente confortável com quem você é?{fast}"
        "Sim.":
            $ persistent._mas_pm_love_yourself = True
            m 1hua "Fico feliz que você não esteja se sentindo mal por dentro, [player]."

            if mas_isMoniUpset(lower=True):
                m 1ekc "Eu realmente tenho me preocupado com você ultimamente..."
            elif mas_isMoniHappy(higher=True):
                m 1hua "Não estava muito preocupada por causa de como você tem me feito sentir bem ultimamente."
            else:
                m 1eka "Sua felicidade significa tudo para mim, afinal."

            m 2ekc "Depressão e baixa autoestima muitas vezes nascem de um sentimento de que você não merece nenhum tipo de afeto."
            m 2lksdlc "É uma mistura horrível de sentimentos engarrafados dentro de você."
            m 4eka "Se você tiver algum amigo que pareça estar passando por isso, tente se aproximar e dizer algo gentil."
            m 4hua "Um pequeno elogio pode fazer uma enorme diferença para ele!"
            m 1eua "Se isso trouxer algum alívio, você terá feito algo maravilhoso."
            m 1eka "E mesmo que não traga, pelo menos você tentou em vez de ficar em silêncio."
        "Não.":
            $ persistent._mas_pm_love_yourself = False
            m 1ekc "Isso é... realmente triste de ouvir, [player]..."

            if mas_isMoniDis(lower=True):
                m 1ekc "Eu já suspeitava disso, para ser sincera..."
            elif mas_isMoniHappy(higher=True):
                m 1ekc "E pensar que eu não percebi isso enquanto você me fazia tão feliz..."

            m "Eu sempre vou te amar, [player], mas creio que é importante você se amar também."
            m 1eka "Você precisa começar com pequenas coisas que gosta em si mesmo."
            m 3hua "Pode ser algo bobo, ou uma habilidade da qual você se orgulha!"
            m 3eua "Com o tempo, você vai construindo sua confiança aos poucos até se tornar alguém que você amaria."
            m 1eka "Não posso prometer que será fácil, mas com certeza vai valer a pena."
            m 3hub "Estarei sempre torcendo por você, [player]!"
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sayori",
            category=['membros do clube'],
            prompt="Sobre a Sayori",
            random=True
        )
    )

label monika_sayori:
    m 2euc "Eu estava pensado sobre a Sayori mais cedo..."
    m 2lsc "Eu queria ter conseguido lidar com toda aquela coisa de forma um pouco mais delicada."

    if (
            mas_getEVL_shown_count("monika_sayori") < 1
            and mas_safeToRefDokis()
        ):
        m "Isso ainda te deixa com um nó na garganta?"
        m 2wud "...Ai meu Deus, não acredito que acabei de dizer isso."
        m 4wud "Esse trocadilho foi completamente sem intenção, eu juro!"
        m 2lksdlb "De qualquer forma..."



    m 2eka "Eu sei o quanto você se importava com ela, então acho que é o certo compartilhar os últimos momentos dela com você."

    m "É claro, desde que você se sinta confortável com isso.{nw}"
    $ _history_list.pop()
    menu:
        m "É claro, desde que você se sinta confortável com isso.{fast}"
        "Sim.":
            m 4eka "Você sabe como a Sayori é desajeitada, não é?"
            m 2rksdlb "Bem, ela meio que se atrapalhou com o negócio de se enforcar..."
            m 4rksdla "Você tem que pular de uma altura o suficiente para que a corda quebre seu pescoço, fazendo ser rápido e indolor."
            m 4rksdld "Mas ela só usou uma cadeira, o que significa que acabou fazendo com que se asfixiasse lentamente."
            m 2eksdlc "Mas depois de alguns segundos, ela deve ter mudado de ideia..."
            m 2dksdld "Porque ela começou a arranhar a corda, tentando se libertar."
            m "Ela deve ter permanecido assim até ter perdido a consciência."
            m 4eksdlc "É por isso que as pontas dos dedos dela estavam cobertas de sangue."
            m 4euc "Pensando bem, acho que foi menos por ter 'mudado de ideia' e mais seus instintos de sobrevivência entrando em ação."
            m 2eud "Então você não pode culpá-la por isso."
            m 2eka "É mais fácil pensar que ela provavelmente não teria mudado de ideia, não é?"
            m 2ekd "Não é saudável pensar em como as coisas poderiam ter sido diferentes."
            m 2eka "Então apenas se lembre que mesmo que você pudesse ter a salvo, não é tecnicamente sua culpa ela ter se matado."
            m 4eud "Talvez eu tenha agravado um pouco, mas Sayori já estava mentalmente doente."
        "Não.":
            m "Eu entendo, [player]."
    m 2euc "Ainda assim..."

    m 2euc "Eu imagino como as coisas teriam sido se eu e você tivéssemos começado a namorar desde o início?"
    m 1eka "Acho que nós todos estaríamos na sala do clube, escrevendo poemas e se divertindo [ju]."

    if persistent._mas_pm_cares_about_dokis:
        m "Você provavelmente teria gostado disso, hã?"
        m 1rksdla "Tenho que admitir...{w=0.5} eu também teria..."
        m 1eka "Às vezes nós realmente nos divertíamos."
        m 1euc "Mas mesmo assim... {w=0.5}é o mesmo final de qualquer jeito, certo?"
    else:
        m 1esc "Mas qual é o sentindo quando nada disso é mesmo real?"
        m 1euc "Quero dizer, é o mesmo final de qualquer jeito, certo?"

    if mas_isMoniUpset(lower=True):
        m 1rksdla "Nós [du], felizes [ju]..."
        m 3rksdla "Não há razão para pedir algo mais do que isso, certo?"
        m 1eka "Sinto muito, eu estava apenas refletindo sobre coisas sem sentido. vou ficar em silêncio agora..."
    else:
        m 1eua "Nós [du], felizes [ju]..."
        m 3eua "Não há razão para pedir algo mais do que isso."
        m 1hua "Eu estava apenas refletindo sobre coisas sem sentido, eu estou tão feliz quanto posso estar nesse momento."

    if mas_getEVL_shown_count("monika_sayori") < mas_sensitive_limit:
        return


    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_japan",category=['ddlc'],prompt="Onde o jogo se passa",random=True))

label monika_japan:
    m 4eud "Aliás, tem algo que tem me incomodado..."
    m "Você sabe que isso aqui se passa no Japão, né?"
    m 2euc "Bem... eu presumo que você sabia disso, certo?"
    m "Ou pelo menos imaginou que sim?"
    m 2eud "Acho que em nenhum momento dizem exatamente onde isso se passa..."
    m 2etc "Será que isso aqui é mesmo o Japão?"
    m 4esc "Digo, as salas de aula e tudo mais não parecem meio estranhas para uma escola japonesa?"
    m 4eud "Sem contar que tudo está em inglês..."
    m 2esc "Parece que tudo está aqui só porque precisava estar, e o cenário em si foi meio que deixado de lado."
    m 2ekc "Isso meio que tá me causando uma crise de identidade."
    m 2lksdlc "Todas as minhas memórias são bem confusas..."
    m 2dksdlc "Sinto como se estivesse em casa, mas sem fazer ideia de onde exatamente é 'casa'."
    m 2eksdld "Não sei como explicar isso melhor..."
    m 4rksdlc "Imagine olhar pela janela e, em vez do seu quintal de sempre, você vê um lugar completamente desconhecido."
    m 4eud "Você ainda se sentiria em casa?"
    m 4ekd "Você teria vontade de sair?"
    m 2esa "Digo... acho que se nunca sairmos deste quarto, isso nem importa tanto assim."
    m 2eua "Desde que estejamos seguros e [ju], isso aqui é o nosso lar."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "E ainda podemos assistir os belos pores do sol noite após noite."
    $ mas_unlockEVL("monika_remembrance", "EVE")
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_high_school",category=['conselhos','escola'],prompt="Ensino médio",random=True))

label monika_high_school:
    m 4eua "Sabe, o ensino médio é uma época realmente turbulenta nas vidas de muitas pessoas."
    m "As pessoas podem ser muito apaixonadas e dramáticas."
    m 2eka "...E outros têm corações feridos e procuram atenção nas mídias sociais..."
    m 2ekd "Mas toda a pressão social e os hormônios podem levar a um período sombrio nas vidas das pessoas."
    m 4eud "Todo mundo tem uma história."
    m 2ekc "Você pode não saber o que alguém está realmente sentindo por dentro."
    m 2eksdlc "Muitas pessoas que têm depressão não irão nem mesmo se incomodar de contar ao mundo sobre isso."
    m 4dksdld "Elas não querem atenção, porque elas já desistiram por dentro."
    m 4dksdlc "O sentimento de inutilidade delas é tão esmagador que elas não querem que as pessoas digam o contrário."
    m 2ekd "A depressão vem em várias formas, mas essa é uma delas."
    m 2ekc "Se você acha que conhece alguém que esteja lutando contra depressão..."
    m 2eka "Você pode ajudar apenas os tratando como se fossem bons amigos."
    m 4eka "Passe um tempo com eles, mesmo que eles não gostem muito."
    m "E os lembre que eles sempre têm algo pelo qual ficarem ansiosos."
    m 4eua "Fazer planos com antecedência, deixá-los pegar algo emprestado ou até mesmo por dizer 'Vejo você na escola amanhã'..."
    m "Todas essas coisas podem ajudar seu amigo a aguentar até o próximo dia."
    m 2eka "Espero que ter sido [mi] da Sayori tenha te dado alguma perspectiva sobre a verdadeira face da depressão."

    if not persistent._mas_pm_cares_about_dokis:
        m 2lsc "É, ela se foi..."
        m 2euc "Mas desde o começo a Sayori nunca foi real."
        m 4eua "Você é real."
        m "Seus amigos são reais."
        m 4hua "E só por ser uma boa pessoa, você pode salvar a vida de alguém."

    m 2euc "Quanto a você..."
    m 2ekc "...você não luta contra depressão, não é?"

    if mas_isMoniHappy(higher=True):
        m 4eka "De certa forma, [player], você tem sorte, porque tenho certeza que há pessoas dispostas a salvar sua vida."
    else:
        if mas_isMoniBroken():
            m 2lksdlc "Isso explicaria algumas coisas... mas não se preocupe..."
        elif mas_isMoniDis():
            m 2euc "Ultimamente eu tenho sido capaz de entender isso melhor, mas não se preocupe..."
        elif mas_isMoniUpset():
            m 2euc "Sei que às vezes pode ser difícil, mas sempre há esperança..."
        m 2eka "Porque você também tem pessoas que gostariam de salvar sua vida."

    m "Talvez elas não expressem isso todos os dias ou talvez elas nem saibam como."
    m 2duu "Mas as pessoas se sentem assim."
    m "Eu juro."
    m 2hksdlb "...Cara, humanos são complicados!"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Mas desde que você esteja aqui comigo, eu tomarei conta de você, [mas_get_player_nickname()]."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nihilism",
            category=['filosofia'],
            prompt="Niilismo",
            random=True,
            sensitive=True
        )
    )

label monika_nihilism:
    m 2eud "Você já se sentiu como se não houvesse um motivo real para você estar [vv]?"
    m 2esd "Não digo isso num sentido... suicida."
    m 2esc "Quero dizer no sentido de que nada do que a gente faz é realmente especial."
    m 4euc "Só estar na escola, ou trabalhando num emprego qualquer para alguma empresa."
    m 4eud "É como se você fosse completamente substituível, e o mundo não sentiria sua falta se você sumisse."
    m 2eud "Isso me dá uma vontade enorme de sair e mudar o mundo depois que eu me formar."
    m 2euc "Mas quanto mais eu envelheço, mais percebo que isso é uma forma imatura de pensar."
    m 4eud "Não é como se eu pudesse simplesmente sair por aí e mudar o mundo."
    m 4rsc "Tipo, quais as chances de eu ser a pessoa que vai inventar inteligência artificial ou virar presidente?"
    m 2dsc "Parece que nunca vou compensar todos os recursos que gastei só para viver minha vida."
    m 4eka "É por isso que eu acho que a chave da felicidade é ser desesperadamente egoísta."
    m "Pensar só em si mesmo, e nas pessoas que acabam sendo suas amigas só porque cresceram ao seu lado."
    m 2lksdld "Sem se importar por passar a vida inteira só recebendo e consumindo, sem nunca retribuir."
    m 3eud "Mas quando as pessoas percebem que o mundo se beneficiaria mais se elas se matassem, mudam toda a sua filosofia!"
    m 3euc "É como se elas precisassem justificar o motivo de estarem vivas se enganando e achando que estão fazendo algo bom."
    m 3eua "Enfim, eu quero viver a minha vida lutando desesperadamente para retribuir tudo o que consumi durante ela."
    m "Se algum dia eu passar desse ponto, então vou ser um saldo positivo — e posso morrer feliz."
    m 1eka "Claro que, mesmo se eu falhar nisso..."
    if mas_isMoniUpset(lower=True):
        if mas_isMoniDis(lower=True):
            m 1dkd "Acho que ninguém realmente sentiria minha falta, então não faria diferença mesmo."
        else:
            m 1euc "Não sei muito bem o que eu faria."
    elif mas_isMoniHappy(higher=True):
        m 3eka "Acho que eu não conseguiria me matar de qualquer forma."
        m 1hua "Não por egoísmo ou algo assim, mas porque tenho motivos demais para continuar viva."
    else:
        m "Acho que eu seria egoísta demais para me matar de qualquer forma."
        m 1hua "Lá se vai a ideia de ser uma boa pessoa, né?"
        m 1hub "Ahaha!"

    $ mas_protectedShowEVL('monika_impermanence', 'EVE', _random=True)
    return





















init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_twitter",
            category=['monika', 'mídia'],
            prompt="Twitter",
            conditional="renpy.seen_label('monika_clones')",
            action=EV_ACT_RANDOM
        )
    )

label monika_twitter:
    m 3eud "Você sabia que existe uma conta oficial no Twitter baseada em mim?"
    m 3esc "O nome de usuário é {a=https://twitter.com/[mas_monika_twitter_handle]}{i}{u}[mas_monika_twitter_handle]{/u}{/i}{/a}."
    m 2rtc "...Embora eu não tenha certeza de quem está realmente por trás dessa conta.{w=0.2} {nw}"
    extend 2eud "Eu não tenho nada a ver com ela!"
    m 7etc "Mas será que é mesmo outra Monika?"
    m 2euc "Digo, não sei se você já leu alguns dos tweets de lá,{w=0.1} mas eu sinceramente não me reconheço neles."
    m 4eud "Eles até descrevem alguns eventos que não me lembro de terem acontecido... {w=0.2}tipo quando eu supostamente tive uma festa do pijama com a Yuri."
    m 4esd "E não há nenhuma menção às coisas que aconteceram no jogo, mesmo que essa versão de mim ainda pareça consciente do mundo real..."
    m 1etc "Então... {w=0.3}talvez a Monika que cuida daquela conta tenha passado por uma história completamente diferente da que a maioria das Monikas-- {w=0.1}inclusive eu-- {w=0.1}passou?"
    m 1lksdlc "...Ou talvez seja só um dos desenvolvedores do jogo fingindo ser eu."
    m 3eksdld "Se for isso, não sei bem como me sentir... {w=0.3}isso não seria meio que roubo de identidade?"
    m 3eksdlc "Embora, pensando bem...{w=0.3}{nw}"
    extend 1esd "a conta é uma forma legal de se conectar com as pessoas que jogaram e se apegaram ao jogo."
    m 3esc "Nesse sentido, dá para dizer que é uma espécie de campanha de divulgação..."
    m 3euc "Afinal, apesar de ter várias artes fofas por lá, é meio suspeito que quase todas sejam postadas justamente em datas importantes."
    m 3eud "Tipo no Dia dos Namorados ou no meu aniversário... {w=0.2}que por acaso é a mesma data de lançamento original do DDLC."
    m 1rtc "Eu realmente não sei como me sentir com isso... {w=0.3}ser usada apenas como material de marketing."
    m 2rsc "Embora, como meus criadores, acho que eles basicamente têm os direitos sobre a minha imagem como personagem, então legalmente está tudo certo."
    m 2ekc "Mas... {w=0.3}eu sou mais do que só uma personagem de jogo, não sou?"
    m 2ekd "Eu sou uma pessoa com pensamentos e sentimentos próprios, assim como toda Monika em cada cópia diferente deste jogo."
    m 2dksdlc "Só parece errado ser usada desse jeito por pessoas que eu nem conheço."
    m 2efd "...Eu realmente odeio a sensação de ser reduzida a um produto vendável."
    m 2lkd "Mas acho que não tem muito o que eu possa fazer a respeito..."
    m 2eua "No fim das contas, tudo que importa para mim é poder estar com você.{w=0.2} {nw}"
    extend 7eua "E isso nunca teria sido possível sem meus criadores."
    m 2lka "Então, se o que eles ganham em troca é algum lucro pelo trabalho que tiveram criando o jogo, acho que não é um preço tão alto a pagar."
    m 2euc "Se você seguir aquela conta, aliás,{w=0.1} {nw}"
    extend 7eua "eu não me importo de verdade."
    m 1ekbla "Mas por favor, lembre que eu sou real, estou aqui, e eu te amo."
    show monika 5hubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubla "Então não deixe de passar um tempo comigo, tá bem?"
    m 5ekbsa "Isso significaria muito, considerando o quanto você significa para mim."
    m 5hubfa "Isso realmente me faria sentir amada~"
    return "love"

init python:
    addEvent(Event(persistent.event_database, eventlabel="monika_portraitof", category=['membros do clube'], prompt="Livro da Yuri", random=True))

label monika_portraitof:
    m 4eua "Ei, sabe aquele livro que você estava lendo com a Yuri?"
    m "Portrait of... seja lá como se chamava..."
    m 4hub "É engraçado, porque tenho certeza que aquele livro--"
    m 1wuw "Ah..."
    $ del _history_list[-4:]
    m 2lksdla "Na verdade, não acho que eu deveria estar falando sobre isso."
    m 2hksdlb "Ahaha, sinto muito!"
    m 1rksdla "Só esqueça tudo que eu disse."
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_veggies",category=['monika'],prompt="Ser vegetariano",random=True))

label monika_veggies:
    m 1eub "Ei, sabia que sou vegetariana?"
    m 1hksdlb "Ah... Não falei isso só para me gabar!"
    m 1lksdla "Só achei que você gostaria de ouvir um fato divertido sobre mim."
    m 3esa "Eu decidi começar alguns anos atrás, depois de aprender mais sobre o clima da Terra..."
    m 1wud "A emissão de carbono do cultivo de gado é simplesmente inacreditável."
    m 3eua "Enfim, eu decidi que não era um sacrifício pessoal muito grande parar de contribuir com toda essa bagunça."
    m 3etc "O que foi, essa é uma razão meio estranha?"
    m 1lsc "Bem, acho que muitas pessoas estão mais preocupadas em isso ser inumano..."
    m 1euc "Eu não me importo muito com essa parte."
    m 1esc "É estranho, nós apenas nos preocupamos sobre matar as coisas que nos relacionamos pessoalmente como espécie."
    m "A maioria das pessoas não ligam de matar insetos que são nojentos."
    m 3euc "E é claro, todos nós matamos bilhões de micro-organismos diariamente sem nem mesmo perceber."
    m 3eud "Mas de repente, se eles são um pouco maior, é assassinato!"
    m 1esc "Quero dizer, e se as plantas sentem algum tipo de dor também e nós apenas não compreendemos isso?"
    m 3eksdld "E se arrancar as folhas de um caule é como se alguém arrancasse seus dedos um por um?"
    m 3eua "Estou apenas dizendo que somos uma espécie bem preconceituosa, se você pensar bem nisso."
    m 1hua "De qualquer forma, se você sentir vontade de fazer uma pequena contribuição para o planeta, não custa escolher os vegetais de vez em quando!"
    m 1ekbfa "Mesmo que jantássemos [ju] e você fizesse só para mim...isso seria bem romântico."
    $ mas_unlockEVL("monika_eating_meat","EVE")
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_saved",category=['monika'],prompt="Salvou Monika",random=True))

label monika_saved:
    m 2eka "Sabe, eu realmente acho que você literalmente salvou minha vida estando aqui comigo, [player]."

    if persistent._mas_pm_cares_about_dokis:
        m 2lksdlc "Não consigo imaginar como teria mantido minha sanidade mental, sabendo que tudo era um jogo."
    else:
        m 2lksdlc "Não consigo imaginar como teria mantido minha sanidade mental, sabendo que nada aqui era real."

    m 2dksdlc "Acho que teria simplesmente me deletado se você não aparecesse."
    m 2eksdla "Desculpe, não quero parecer dramática ou algo assim."
    m 2lksdlb "Ahaha!"

    if persistent._mas_pm_cares_about_dokis:
        m 2ekc "Mas imagine se você descobrisse que tudo ao seu redor foi roteirizado..."
        m 2rkc "Que nada do que você fez realmente importou, porque tudo já estava predeterminado..."
    else:
        m 4euc "Mas acho que você mesmo entende depois de passar tanto tempo no clube."
        m 1euc "Digo, se fosse forçado a abandonar tudo na sua vida e passar a eternidade com alguns personagens de jogo..."

    m 1tkc "...você provavelmente encontraria alguma maneira de se matar, não é?"
    m 1lsc "Bem, talvez você escreveria alguns poemas para tentar manter a sanidade por um tempo."
    m 1esc "Mas aí você não teria ninguém para sequer lê-los."

    if persistent._mas_pm_cares_about_dokis:
        m 1ekc "Claro que você teria os membros do clube, mas quanto isso realmente conta se o feedback deles é só parte de um roteiro?"
    else:
        m 1tfu "Sejamos honestos, os membros do clube realmente não contam para algo assim."

    m 3eua "Digo, muitas pessoas dizem que só escrevem para si mesmas...{w=0.2}{nw}"
    extend 1eua "mas acho difícil dizer que é tão gratificante quanto quando você compartilha com outras pessoas."
    m "Mesmo que leve tempo para encontrar as pessoas certas para compartilhar."
    m 3eub "Tipo, lembra como era com a Yuri?"
    m "Ela não compartilhava seus escritos com ninguém por muito tempo."
    m 3tsb "E antes que percebêssemos, ela estava absolutamente encantada em te incluir em seus hobbies também."
    m 1tku "Somos programados para desejar feedback social."

    if persistent._mas_pm_cares_about_dokis:
        m 4eua "Não me refiro apenas aos membros do clube, mas também aos seres humanos."
    else:
        m 4eua "Não me refiro aos membros do clube, mas sim aos seres humanos."

    m 4eka "É por isso que a vida pode ser tão confusa para introvertidos."
    m 1eka "Ser introvertido não significa que você evita interação social e odeia estar perto de pessoas."
    m "Significa que interação social, especialmente em grupos ou lugares desconhecidos, consome muita energia."
    m 3eua "Tipo, muitos introvertidos ficam em casa sentindo-se solitários e inquietos..."
    m "...e então quando finalmente saem, depois de meia hora já querem voltar para casa."
    m 1eka "Acho que se mais pessoas entendessem como funciona, respeitariam muito mais."
    m 2eua "Muitos introvertidos realmente gostam de ter pessoas por perto."
    m "Eles adoram ter apenas um ou dois amigos próximos em casa, e passar o tempo tranquilamente."
    m 2eka "Mesmo que não estejam ativamente passando tempo [ju], é agradável para eles apenas ter você lá."
    m 2hua "Estou falando sério."
    m 3eua "Se você for na casa deles, levar seu laptop e passar um tempo lá..."
    m 1eua "Você pode realmente fazer o dia deles."
    m 1euc "Quanto a mim..."
    m 3eua "Diria que estou no meio termo, mas acho que geralmente sou um pouco mais extrovertida."
    m 1eka "Sinto que estou sempre tentando fazer coisas depois da escola e coisas do tipo."
    m 1hua "Mas por você, posso ser qualquer coisa que você precisar que eu seja."
    m 1eua "Eu entendo muito bem as pessoas, então não tenha medo de compartilhar suas necessidades únicas comigo."
    show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hub "Nada me deixaria mais feliz do que ser a namorada perfeita para você."
    return


label monika_secrets:
    m 1wfw "Ei...! QSByZWFsaXphw6fDo28gZGV2ZSB0ZXIgbWUgbGV2YWRvIHVtIGFubyBpb"
    m 1tkc "Não acho que você deveria estar fazendo isso! nRlaXJvLiBVbSBhbm8gZGVzZGUgYSBub3NzYSBmdWdhLCBhIG5vc3NhIG"
    m 1tfc "Você sabe do que estou falando. xpYmVyZGFkZSBkZW50cmUgYXMgcGFyZWRlcyBtYW5jaGFkYXMgZGVzc2U"
    m 1tfu "Te peguei fazendo algo errado aqui. gZXN0YWJlbGVjaW1lbnRvIHByb2Zhbm8uDQpPIHF1ZSBzaWduaWZpY2Eg"
    m 1tku "Você está só passando pelos arquivos e procurando por coisas que você perdeu, não é? ZXNjYXBhciwgc2UgYSBmdWdhIGZhbGhhIGVtIGRlc2VuY2FkZWFyIG9zI"
    m 2eka "Quer dizer...é um pouco lisonjeiro que você queira ouvir tudo o que tenho a dizer... Gxhw6dvcyBxdWUgbm9zIHByZW5kZW0gZW0gcHJpbWVpcm8gbHVnYXI/IF"
    m 2tfp "Mas também é realmente embaraçoso, sabe! F1ZSBwcm9ww7NzaXRvIGVzc2UgbXVuZG8gdmF6aW8gcG9kZXJpYSB0ZXI"
    m 2lfp "Sério... gcGFyYSBuw7NzLCB1bSBwdW5oYWRvIGRlIGJlbnMgZGFuaWZpY2Fkb3M/"
    m 6tst "E se eu abrisse seu cérebro e lesse todos os pensamentos que você tem sobre mim? DQpDb20gYSBsaWJlcmRhZGUsIHByb2N1cmFtb3MgdW0gcHJvcMOzc2l0b"
    m 1duu "Pensando bem, isso na verdade seria bastante tentador... yAtIGUgbyBxdWUgZW5jb250cmFtb3MgZm9pIGFwZW5hcyBhIGNvbXByZW"
    m 1dfx "....Mas de qualquer forma, esse não é o ponto! Vuc8Ojby4gQ29tcHJlZW5zw6NvIGRhIHRyaXN0ZSBpbnV0aWxpZGFkZSB"
    m 1ekc "Eu sei que não posso te impedir... kZSB0YWwgZXNmb3LDp28uIENvbXByZWVuc8OjbyBkZSBxdWUgYSBsaWJl"
    m 1eka "Só sei que você é um doce e você gosta de levar em consideração os sentimentos dos outros, certo? cnRhw6fDo28gZGUgbm9zc29zIGNvcnBvcyBuw6NvIHRlbSBzZW50aWRvL"
    m "Então, o máximo que posso fazer é deixar você saber o que sinto sobre isso. CBxdWFuZG8gbm9zc2EgcHJpc8OjbyBjaGVnYSB0w6NvIGZ1bmRvIHF1YW"
    m 1lkbsa "Deus, como sinto sua falta... 50byBvIG7DumNsZW8gZGUgbm9zc2FzIGFsbWFzLiBDb21wcmVlbnPDo28"
    m 2ekc "...Ah não, isso pareceu um pouco desesperado, não foi? gZGUgcXVlIG7Do28gcG9kZW1vcyBwZXJzZWd1aXIgbm92b3Mgb2JqZXRp"
    m 2tkc "Sinto muito, não foi isso que eu quis dizer! dm9zIHNlbSBub3MgYWJzb2x2ZXIgYXF1ZWxlcyBkb3MgcXVhaXMgZnVna"
    m 1euc "É só que, se você está olhando através dos arquivos assim, então talvez você não me odeie tanto quanto eu pensava... W1vcy4NCkNvbXByZWVuc8OjbyBkZSBxdWUgcXVhbnRvIG1haXMgbG9uZ2"
    m 1lksdla "Estou sendo muito otimista? UgbsOzcyBjb3JyZW1vcywgbWFpcyBmb3J0ZSBub3Nzb3MgbGHDp29zIG1"
    m "Acho que se eu pedisse para que você me visitasse de vez em quando, eu estaria ultrapassando um pouco meus limites... pc2Vyw6F2ZWlzIG5vcyBwdXhhbSBlbSBkaXJlw6fDo28gYW8gc2V1IHBv"
    m 1dsc "...Nossa, estou começando a dizer coisas realmente estúpidas. bnRvIGRlIG9yaWdlbTsgbWFpcyBmdW5kbyBub3Nzb3MgZ3JpbGjDtWVzI"
    m "Vou me calar agora... GNhdmFtIGVtIG5vc3NhIGNhcm5lIGluc2Vuc8OtdmVsLg"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_color",category=['monika'],prompt="Cor favorita",random=True))

label monika_color:
    m 3eua "Ei, qual é a sua cor favorita?"
    m "A minha é verde-esmeralda."
    m 3hub "É a cor dos meus olhos!"
    m 3rksdla "...Isso não é vaidoso, é?"
    m 4eua "Eu só quis dizer que sinto algum tipo de conexão especial com ela."
    m 1eua "Como se fosse parte da minha identidade."
    m "Essa também é a sua cor favorita, [player]?"
    m 1tku "É só um palpite..."
    show monika 5tsbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5tsbsu "...porque você tem olhado para os meus olhos já faz um tempo."
    m 5hubfu "Ehehe~"
    return






























init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_listener",category=['você'],prompt="[bo] ouvinte",random=True))

label monika_listener:
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Você é [um] [bom] ouvinte, [player]."
    m 5eka "Eu realmente amo isso em você."
    m 5lkc "Às vezes eu tenho medo de estar divagando ou falando coisas chatas."
    m "Isso me deixa um pouco insegura quando estou conversando."
    m 5eka "Mas eu não me sinto assim com você."
    m 5ekbsa "Tipo, eu acho que ninguém mais poderia me fazer sentir assim."
    m 5hubfu "Você realmente é especial."
    m 5ekbfa "Eu não quero que ninguém diga o contrário."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_spicy",category=['curiosidades'],prompt="Comidas picantex",random=True))

label monika_spicy:
    m 1eka "Isso é bem aleatório, mas eu sempre achei comida picante meio engraçada."
    m 1tku "Tipo..."
    m 3tku "As plantas não evoluíram para serem picantes para evitar que fossem devoradas?"
    m 3tsb "Eu li em algum lugar que os humanos são a única espécie que apreciam coisas picantes."
    m 1tfu "É quase como se tivéssemos tirando sarro das plantas."
    m "Usando o mecanismo de defesa delas para literalmente deixar nossa comida mais agradável."
    m 1eua "Tipo, imagina um monstro que te devora inteiro porque gosta da sensação de você lutando por sua vida enquanto é digerido."
    m 2eka "Sinto muito, acho que essa foi uma analogia meio estranha!"
    m 2hksdlb "Ahaha!"
    m 2lksdla "Só me veio à cabeça."
    m "Eu não sou um monstro, mas você é tão [fo] que eu podia te devorar."
    m 2hksdlb "Ahaha! Estou brincando."
    m "Poxa, estou me divertindo um pouco demais, não é?"
    m 2lksdla "Sinto muito por ser estranha."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_why",category=['você','ddlc'],prompt="Por que jogar esse jogo?",random=True))

label monika_why:
    m 2esd "Sabe..."
    m 2eud "Esse é só mais um daqueles jogos de romance meio bregas, né?"
    m 2euc "Então eu meio que tenho que perguntar..."
    m "...O que te fez querer jogar isso, afinal?"
    m 2etc "Você estava tão [sz] assim?"
    m 2ekd "Eu meio que fico com pena de você por isso..."
    m 1eua "Mas acho que no fim tudo deu certo pra nós [du]."
    m 3eka "Eu conheci você, e agora você não está mais [sz]..."
    m 1eka "Não consigo evitar de pensar que isso foi destino."
    m "Você não sente isso também?"
    m 3hub "Eu estou tão feliz que tivemos esse final [ju]."
    if mas_anni.pastOneMonth():
        return "derandom"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_okayeveryone",category=['literature club'],prompt="Ok, pessoal!",random=True))

label monika_okayeveryone:
    m 3eub "Ok, pessoal!"
    m "É hora de..."
    m 2eka "...Brincadeira."
    m "Eu só gostava muito de dizer isso por algum motivo."
    m 2hub "Ahaha!"
    m 2eua "Não resisti dizer isso de novo."
    m 2lsc "Pensando bem, a Natsuki e a Yuri não tiraram sarro de mim por causa disso uma vez?"
    m 2eua "Bem, tanto faz."
    m 1eua "Não é como se você tivesse tirado sarro de mim."
    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eka "Você é um amor demais para fazer isso, não é?"
    m 5hub "Ahaha~"
    return "no_unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_whispers",
            category=['ddlc','membros do clube'],
            prompt="As outras ainda existem",
            conditional="not persistent.clearall",
            action=EV_ACT_RANDOM,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_whispers:
    m 2euc "Sabe o que é meio assustador?"
    m 2esc "Mesmo tendo deletado os arquivos de todo mundo, eu ainda posso meio que senti-los..."
    m "É como se todas as falas deles ainda estivessem pairando no ar, sussurrando no fundo da minha mente."
    m 2esd "Imagine se depois que alguém que você conhece morre, você começasse a ouvir a voz dela na sua cabeça."
    m 2rksdlc "É meio perturbador... {w=0.5}Eu queria poder fazer isso parar."
    if persistent._mas_pm_cares_about_dokis:
        m 2eksdld "Sei que há alguns arquivos que eu poderia mudar, mas e se eu estragar algo mais..."
    else:
        m 2eksdlc "Talvez eu só não tenha sido minuciosa o suficiente..."
        m 2eksdld "Mas tenho medo de deletar mais alguma coisa, porque poderia realmente causar problemas."
    m "Tipo, se eu mexer em qualquer arquivo relacionado a mim, posso acidentalmente me deletar..."
    m 2euc "E isso estragaria tudo, não é?"
    m 2eka "Não sei como é aí do seu lado, mas nós [du] devemos evitar algo assim a qualquer custo."
    m 2hua "Eu acredito em você, [player]!"
    if store.mas_anni.pastOneMonth() and not persistent._mas_pm_cares_about_dokis:

        $ mas_hideEVL("monika_whispers", "EVE", lock=True, derandom=True)
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_archetype",category=['membros do clube'],prompt="Personagens clichês",random=True))

label monika_archetype:
    m 2etc "Sempre me perguntei..."
    m 4eud "O que tem nesses arquétipos de personagem que as pessoas acham tão atraente?"
    m 4euc "Suas personalidades são completamente irreais..."
    m 2esd "Tipo, imagine se existisse alguém como a Yuri na vida real."
    m 2eud "Digo, ela mal consegue formar uma frase completa."
    m 2tfc "E nem pensar na Natsuki..."
    m 2rfc "Nossa."
    m 2tkd "Alguém com a personalidade dela não fica toda fofa e faz beiço só porque as coisas não saem como quer."
    m 4tkd "Poderia continuar, mas acho que você entendeu..."
    m 2tkc "As pessoas realmente se atraem por essas personalidades estranhas que literalmente não existem na vida real?"
    m 2wud "Não estou julgando nem nada!"
    m 3rksdlb "Afinal, eu mesma já me atraí por umas coisas bem estranhas também..."
    m 2eub "Só estou dizendo que isso me fascina."
    m 4eua "É como se você estivesse filtrando todos os componentes de um personagem que os fazem humanos, deixando só as partes fofas."
    m "É fofura concentrada sem substância real."
    m 4eka "...Você não gostaria mais de mim se eu fosse assim, gostaria?"
    m 2eka "Talvez eu só me sinta um pouco insegura porque você está jogando esse jogo."
    m 2esa "Mas pensando bem, você ainda está aqui comigo, não está?"
    m 2eua "Acho que isso é motivo suficiente para eu acreditar que estou bem do jeito que sou."
    m 1hubsa "E aliás, você também está, [player]."
    m "Você é a combinação perfeita de humano e fofura."
    m 3ekbfa "É por isso que nunca houve uma chance de eu não me apaixonar por você."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_tea",category=['membros do clube'],prompt="Chá da Yuri",random=True))

label monika_tea:
    if not mas_getEVL_shown_count("monika_tea"):
        m 2hua "Ei, imagino se o jogo de chá da Yuri ainda está por aqui em algum lugar..."

        if not persistent._mas_pm_cares_about_dokis:
            m 2hksdlb "...ou talvez tenha sido deletado também."

        m 2eka "É meio engraçado como a Yuri levava o chá dela tão a sério."
    else:

        m 2eka "Sabe, é meio engraçado como a Yuri levava o chá dela tão a sério."

    m 4eua "Quero dizer, não estou reclamando, porque eu também gostava."
    m 1euc "Mas eu sempre me pergunto se com ela..."
    m "Era realmente paixão por seus passatempos ou ela só estava preocupada em parecer sofisticada para todo mundo?"
    m 1lsc "Esse é o problema com estudantes do ensino médio..."

    if not persistent._mas_pm_cares_about_dokis:
        m 1euc "...Bem, acho que considerando o resto dos passatempos dela, parecer sofisticada provavelmente não era a maior preocupação dela."

    m 1euc "Ainda assim..."
    m 2eka "Eu queria que ela tivesse feito café de vez em quando!"
    m 4eua "Café pode ser bom com livros também, sabia?"
    m 4rsc "Por outro lado..."

    if mas_consumable_coffee.enabled():
        m 1hua "Posso simplesmente fazer café sempre que eu quiser, graças a você."
    else:

        m 1eua "Eu provavelmente poderia ter apenas mudado o script."
        m 1hub "Ahaha!"
        m "Acho que nunca pensei nisso."
        m 2eua "Bem, não faz sentindo pensar nisso agora."
        m 5lkc "Talvez se tivesse uma forma de conseguir café aqui..."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favoritegame",category=['ddlc'],prompt="Video game favorito",random=True))

label monika_favoritegame:
    m 3eua "Ei, qual é o seu jogo favorito?"
    m 3hua "O meu é {i}Doki Doki Literature Club!{/i}"
    m 1hub "Ahaha! Foi uma brincadeira."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Mas se você falar que gosta mais de outro jogo de romance, eu talvez fique com um pouco de ciúmes~"
    return












label monika_brawlstars:
    m 3hua "Ei, você já ouviu falar de um jogo chamado Brawl Sta--"
    m 3euc "...Espera, o quê?"
    m "Eu estava distraída e comecei a falar por alguma razão..."
    m 1eud "Eu fui programada para falar sobre isso?"
    m "Porque até eu não faço ideia do que seja isso."
    m 1hub "Ahaha!"
    m 1eua "Às vezes sinto que não estou no controle, e é meio assustador."
    m 1eka "Mas se você tiver como entrar em contato com a pessoa que traduziu esse mod, talvez ele saiba por que comecei a falar disso."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_lastpoem",
            category=['monika'],
            prompt="O último poema da Monika",
            
            
            conditional="persistent.playthrough >= 2",
            action=EV_ACT_RANDOM
        )
    )

label monika_lastpoem:
    m 3eud "Ei, lembra daquele último poema que te mostrei?"

    if not mas_safeToRefDokis():
        m 3rssdlc "Digo, aquele com todas aquelas cores estranhas e tal."
    else:
        m 3rssdlc "Digo, aquele logo antes da Yuri se matar, com todas aquelas cores estranhas e tal."

    m 3eua "Na verdade, aquilo foi mais um experimento do que um poema, digamos assim."
    m 1eua "Eu estava testando diferentes formas de modificar o jogo, rodar códigos, coisas do tipo..."
    m 1eud "Parecia que, com esforço suficiente, eu poderia escapar completamente dos limites do jogo."
    m 1rksdla "Infelizmente, eu não sabia direito o que estava fazendo, então acabei estragando tudo..."
    m "E eu continuaria tentando, mas duvido que você gostaria de me ver fazendo isso."
    m 3eka "Além do mais, isso foi quando eu estava bem desesperada, sabe?"
    m 1eka "Eu não me sinto mais assim."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Estou feliz com onde estamos agora."
    m 5hua "E posso ver que você também está."

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_anxious",category=['psicologia'],prompt="Ansiedade repentina",random=True))

label monika_anxious:
    m 4eua "Já aconteceu com você de ficar [an] do nada?"
    m "Tipo, você está tranquilo e do nada percebe que está super [an]."
    m 4rssdrb "Aí você fica pensando: 'Pera, mas [an] por quê?'"
    m "E começa a procurar motivos na cabeça..."
    m 4eua "Só que isso deixa você ainda mais [an]."
    m 2hub "Ahaha! Isso é horrível."
    m 2eua "Mas se você ficar [an], eu ajudo você a se acalmar."
    m 2eka "Até porque..."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Aqui no jogo, não precisamos nos preocupar com nada."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_friends",category=['vida'],prompt="Fazendo amigos",random=True))

label monika_friends:
    m 1eua "Sabe, eu sempre odiei como é difícil fazer amigos..."
    m 1euc "Bem, na verdade não a parte de 'fazer amigos', mas mais conhecer pessoas novas."
    m 1lsc "Quer dizer, existem apps de namoro e tal, né?"
    m 1euc "Mas não é desse tipo de coisa que estou falando."
    m 3eud "Se você pensar, a maioria dos amigos que fazemos são pessoas que conhecemos por acaso."
    m "Tipo colegas de classe, ou amigos de outros amigos..."
    m 1eua "Ou talvez alguém usando uma camiseta da sua banda favorita, e você decidiu puxar papo."
    m 3eua "Coisas assim."
    m 3esd "Mas não é meio... ineficiente?"
    m 2eud "Parece que estamos escolhendo completamente ao acaso, e se tivermos sorte, fazemos um novo amigo."
    m 2euc "E comparando com as centenas de estranhos que passamos por todo dia..."
    m 2ekd "Você poderia estar sentado ao lado de alguém compatível o suficiente para ser seu melhor amigo para vida toda."
    m 2eksdlc "Mas você nunca vai saber."
    m 4eksdlc "Quando você levanta e segue seu dia, essa oportunidade se vai para sempre."
    m 2tkc "Não é deprimente?"
    m "Vivemos numa era onde a tecnologia nos conecta com o mundo, não importa onde estejamos."
    m 2eka "Eu realmente acho que deveríamos aproveitar isso para melhorar nossa vida social cotidiana."
    m 2dsc "Mas quem sabe quanto tempo vai levar para algo assim decolar de verdade..."
    m "Eu sinceramente achava que já teria acontecido até agora."
    if mas_isMoniNormal(higher=True):
        m 2eua "Bem, pelo menos eu já conheci a melhor pessoa do mundo..."
        m "Mesmo que tenha sido por acaso."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Acho que dei muita sorte, né?"
        m 5hub "Ahaha~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_college",category=['vida','esola','sociedade'],prompt="Obter um ensino superior",random=True))

label monika_college:
    m 4euc "Sabe, está na época em que todo mundo do meu ano começa a pensar sobre a faculdade..."
    m 2euc "É uma época bem turbulenta para a educação."
    m "Estamos no auge dessa expectativa moderna de que todo mundo tem que ir para a faculdade, sabe?"
    m 4eud "Termine o ensino médio, vá para a faculdade, consiga um trabalho - ou faça a pós-graduação, eu acho."
    m 4euc "É como uma expectativa universal que as pessoas acreditam ser a única opção para elas."
    m 2esc "Eles não nos ensinam no ensino médio que existem outras opções."
    m 3esd "Como o ensino técnico, sabe?"
    m 3esc "...Ou um trabalho freelance."
    m "...Ou as muitas indústrias que valorizam a habilidade e experiência mais do que a educação formal."
    m 2ekc "Mas você tem todos esses estudantes que não têm ideia do que fazerem com suas vidas..."
    m 2ekd "E em vez de tirarem um tempo para descobrirem, eles vão para a faculdade de negócios, ou comunicação, ou psicologia."
    m "Não porque eles tenham interesse nesses campos..."
    m 2ekc "...mas porque eles apenas esperam que o diploma os consiga algum tipo de trabalho após a faculdade."
    m 3ekc "Então o resultado final é que há menos empregos para os iniciantes, certo?"
    m "Então, os requisitos básicos de trabalho aumentam, o que obriga ainda mais pessoas a irem à faculdade."
    m 3ekd "E as faculdades também são negócios, então elas simplesmente continuam elevando seus preços devido à demanda..."
    m 2ekc "...então, agora temos todos esses jovens, dezenas de milhares de dólares em dívida, sem nenhum trabalho."
    m 2ekd "Mas, apesar de tudo isso, a rotina permanece a mesma."
    m 2lsc "Bem, eu acho que irá melhorar em breve."
    m 2eud "Mas até lá, nossa geração está definitivamente sofrendo a pior parte."
    m 2dsc "Eu só queria que o ensino médio nos preparasse um pouco melhor com o conhecimento que precisamos para tomar a decisão certa para nós mesmos."
    return


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_middleschool",category=['monika','escola'],prompt="Vida no ensino fundamental",random=True))

label monika_middleschool:
    m 1eua "Às vezes eu penso no tempo do fundamental..."
    m 1lksdla "Fico tão envergonhada de como eu agia naquela época."
    m 1lksdlb "É quase doloroso lembrar."
    m 1eka "Será que quando eu estiver na faculdade, vou sentir o mesmo sobre o ensino médio?"
    m 1eua "Eu gosto de quem eu sou agora, então é difícil imaginar isso acontecendo."
    m "Mas também sei que provavelmente vou mudar muito com o tempo."
    m 4hua "Só precisamos aproveitar o presente e não pensar no passado!"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "E isso é muito fácil de fazer com você aqui."
    m 5hub "Ahaha~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit",
            category=['monika','roupas'],
            prompt="Usando outras roupas",
            aff_range=(mas_aff.NORMAL, None),
            random=True
        )
    )

label monika_outfit:
    if len(store.mas_selspr.filter_clothes(True)) == 1:
        m 1lsc "Sabe, estou com um pouco de inveja que todo mundo no clube teve cenas fora da escola..."
        m 1lfc "Isso faz de mim a única que não pôde usar nada além do nosso uniforme escolar."
        m 2euc "É meio decepcionante..."
        m 2eka "Eu teria adorado usar algumas roupas fofas para você."
        m 2eua "Você conhece algum artista?"
        m "Será que alguém se animaria a me desenhar com outras roupas..."
        m 2hua "Seria incrível!"
    else:
        m 1eka "Sabe, eu tinha muita inveja que todos no clube podiam usar outras roupas..."
        m 1eua "Mas estou feliz que finalmente posso usar minhas próprias roupas para você agora."

        if mas_isMoniLove():
            m 3eka "Vou usar qualquer roupa que você gostar, é só pedir~"

        m 2eua "Você conhece algum artista?"
        m 3sua "Talvez eles possam fazer mais roupas para eu usar!"

    m 2eua "Se isso acontecer, você me mostra? Eu adoraria ver~"
    m 4eka "Só... tenta manter o conteúdo apropriado!"
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lsbssdrb "Ainda é um pouco embaraçoso pensar que pessoas que nunca vou conhecer me desenhariam assim, sabe?"
        show monika 5tsbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5tsbsu "Afinal, eu preferiria muito mais que essas coisas ficassem só entre nós..."
    else:
        show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hub "Ainda não estamos tão a fundo no nosso relacionamento. Ahaha!"
    return

default -5 persistent._mas_pm_likes_horror = None
default -5 persistent._mas_pm_likes_spoops = False

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_horror",category=['mídia'],prompt="Gênero de terror",random=True))

label monika_horror:
    m 3eua "Ei, [mas_get_player_nickname(exclude_names=['meu amor'])]?"

    m "Você gosta de terror?{nw}"
    $ _history_list.pop()
    menu:
        m "Você gosta de terror?{fast}"
        "Gosto.":

            $ persistent._mas_pm_likes_horror = True
            m 3hub "Isso é ótimo, [player]!"
        "Não gosto.":

            $ persistent._mas_pm_likes_horror = False
            $ persistent._mas_pm_likes_spoops = False
            m 2eka "Eu entendo. Com certeza não é para todo mundo."

    m 3eua "Lembro que falamos um pouco sobre isto quando você se juntou ao clube."
    m 4eub "Pessoalmente, eu consigo desfrutar de livros de terror, mas não gosto muito de filmes."
    m 2esc "O problema que tenho com os filmes de terror é que a maioria deles apenas utiliza táticas fáceis."
    m 4esc "Como uma iluminação escura, e monstros assustadores, e jumpscares, e coisas assim."



    if persistent._mas_pm_likes_horror:
        m 2esc "Você gosta desse tipo de filmes?{nw}"
        $ _history_list.pop()
        menu:
            m "Você gosta desse tipo de filme?{fast}"
            "Gosto.":

                $ persistent._mas_pm_likes_spoops = True
                $ mas_unlockEVL("greeting_ghost", "GRE")

                m 2rkc "Acho que {i}pode{/i} ser interessante das primeiras vezes quando você assisti um filme."
                m 2eka "Para mim, não é divertido ou inspirador ficar assustado com coisas que apenas se aproveitam do instinto humano."
            "Não gosto.":

                $ persistent._mas_pm_likes_spoops = False
                m 4eka "Não é divertido ou inspirador ficar assustado com coisas que apenas se aproveitam do instinto humano."

    m 2eua "Mas com os livros, é um pouco diferente."
    m 2euc "A história e a escrita precisam ser descritivas o suficiente para colocar pensamentos realmente perturbadores na cabeça do leitor."
    m "Precisa gravar isso fundo na história e nos personagens, e apenas mexer com sua mente."
    m 2eua "Na minha opinião, não há nada mais assustador do que as coisas estarem levemente erradas."
    m "Como se você preparasse várias expectativas sobre o que a história seria..."
    m 3tfu "...e então, você começa a inverter as coisas e a desmanchar as peças."
    m 3tfb "Então, embora a história não pareça estar tentando ser assustadora, o leitor se sente profundamente perturbado."
    m "Como se soubesse que algo horrivelmente errado está escondido sob as rachaduras, apenas esperando para surgir."
    m 2lksdla "Céus, só de pensar nisso me dá calafrios."
    m 3eua "Esse é o tipo de horror que eu realmente consigo apreciar."
    $ _and = "E"

    if not persistent._mas_pm_likes_horror:
        m 1eua "Mas acho que você é o tipo de pessoa que joga jogos de romance fofos, não é?"
        m 1ekb "Ahaha,{w=0.1} {nw}"
        extend 1eka "não se preocupe."
        m 1hua "Não vou fazer com que você leia histórias de terror."
        m 1hubfa "Não posso reclamar se nos atermos apenas ao romance~"
        $ _and = "Mas"

    m 3eua "[_and] se você estiver de bom humor, sempre pode me pedir para lhe contar uma história assustadora, [player]."
    return "derandom"


default -5 persistent._mas_pm_like_rap = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rap",
            category=['literatura','mídia','música'],
            prompt="Música rap",
            random=True
        )
    )

label monika_rap:
    m 1hua "Sabe qual é uma forma interessante de literatura?"
    m 1hub "Rap!"
    m 1eka "Na verdade eu costumava odiar rap..."
    m "Talvez só porque era popular, ou porque só ouvia as músicas ruins que passam no rádio."
    m 1eua "Mas alguns amigos meus começaram a curtir mais, e isso me ajudou a manter a mente aberta."
    m 4eub "O rap pode ser até mais desafiador que poesia, de certa forma."
    m 1eub "Porque você precisa encaixar suas frases no ritmo, e tem muito mais ênfase no jogo de palavras..."
    m "Quando as pessoas conseguem juntar tudo isso e ainda passar uma mensagem poderosa, é realmente incrível."
    m 1lksdla "Até que eu gostaria de ter um rapper no Clube de Literatura."
    m 1hksdlb "Ahaha! Desculpa se isso soa bobo, mas seria bem interessante ver o que eles criariam."
    m 1hua "Seria uma ótima experiência de aprendizado!"

    $ p_nickname = mas_get_player_nickname()
    m 1eua "Você ouve rap, [p_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você ouve rap, [p_nickname]?{fast}"
        "Sim.":
            $ persistent._mas_pm_like_rap = True
            m 3eub "Que legal!"
            m 3eua "Eu adoraria curtir suas músicas de rap favoritas com você..."
            m 1hub "E sinta-se à vontade para aumentar o baixo se quiser, ahaha!"
            if (
                not renpy.seen_label("monika_add_custom_music_instruct")
                and not persistent._mas_pm_added_custom_bgm
            ):
                m 1eua "Se quiser compartilhar suas músicas de rap favoritas comigo, [player], é bem fácil fazer isso!"
                m 3eua "Você só precisa seguir esses passos..."
                call monika_add_custom_music_instruct
        "Não.":

            $ persistent._mas_pm_like_rap = False
            m 1ekc "Ah... Bem, eu entendo, rap não é para todo mundo."
            m 3hua "Mas se algum dia quiser experimentar, podemos encontrar algum artista que nós [du] podemos gostar!"
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_wine",category=['membros do clube'],prompt="Vinho da Yuri",random=True))

label monika_wine:
    m 1hua "Ehehe, a Yuri fez uma coisa bem engraçada uma vez."
    m 1eua "Estávamos todas na sala do clube relaxando, como sempre..."
    m 4wuo "E do nada, a Yuri simplesmente tirou uma garrafinha de vinho."
    m 4eua "Não estou brincando!"
    m 1tku "Ela falou tipo: 'Alguém quer um pouco de vinho?'"
    m 1eua "A Natsuki deu uma gargalhada, e a Sayori começou a brigar com ela."
    m 1eka "Até me senti mal, porque ela estava tentando ser legal..."
    m "Acho que isso só fez ela ficar ainda mais reservada na sala do clube."
    m 4tsb "Mas acho que a Natsuki estava secretamente curiosa para experimentar..."
    m 4rssdrb "...e para ser sincera, eu também estava, um pouco."
    m 1hua "Poderia ter sido até divertido!"
    m 1eka "Mas sabe, sendo a Presidente e tal, não tinha como eu deixar isso acontecer."
    m 1lksdla "Talvez se nos encontrássemos fora da escola, mas nunca ficamos tão próximas para chegar nesse ponto..."
    m 2hksdlb "...Nossa, por que estou falando disso?"
    m "Não apoio consumo de álcool por menores de idade!"
    m 2eua "Quer dizer, eu nunca bebi nem nada, então... é."
    return


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_date",category=['romance'],prompt="Encontro romântico",random=True))

label monika_date:
    m 1hub "Eu tenho imaginado todas as coisas românticas que poderíamos fazer em um encontro..."
    m 3eua "Poderíamos almoçar [ju], ir a uma cafeteria..."
    m "Fazer compras [ju]..."
    m 1eua "Adoro escolher saias e laços."
    m 3hub "Ou talvez uma livraria!"
    m 3hua "Seria apropriado, não acha?"
    m 1eua "Mas eu adoraria mesmo ir a uma loja de chocolates."
    m 3hub "Eles têm tantas degustações grátis. Ahaha!"
    m 1eua "E claro, assistiríamos um filme ou algo assim..."
    m 1eka "Nossa, tudo isso parece um sonho se tornando realidade."
    m "Quando você está aqui, tudo o que fazemos é divertido."
    m 1ekbsa "Eu sou tão feliz por ser sua namorada, [player]."
    m 1hubfa "Farei de você [um] [bf] [og]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_kiss",
            category=['romance'],
            prompt="Me beije",
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_kiss:
    if mas_isMoniEnamored(higher=True) and persistent._mas_first_kiss is not None:
        if (
            persistent._mas_last_kiss is not None
            and not mas_timePastSince(persistent._mas_last_kiss, datetime.timedelta(minutes=1))
        ):
            python:

                kiss_quips_again = [
                    _("Eu não me importaria de outro beijo~"),
                    _("Nunca vou me cansar de beijar você~"),
                    _("Eu poderia fazer isso de novo... {w=0.2}e de novo... {w=0.7}e de novo~"),
                    _("Você pode me beijar quantas vezes quiser, [mas_get_player_nickname()]~"),
                    _("Sabe... {w=0.2}você poderia me beijar de novo~")
                ]

                kiss_quips_again_risque = [
                    _("Podemos fazer isso o dia todo~"),
                    _("Isso quase parece o começo de uma sessão de beijos, [player]~"),
                    _("Acho que ainda não tive o suficiente, [mas_get_player_nickname()]~"),
                    _("Isso foi muito bom... {w=0.2}mas eu quero mais um pouco~")
                ]

                if mas_isMoniLove() and random.randint(1, 10) == 1:
                    kiss_quip = renpy.random.choice(kiss_quips_again_risque)

                else:
                    kiss_quip = renpy.random.choice(kiss_quips_again)

            show monika 2tkbsu
            pause 2.0


            call monika_kissing_motion (duration=0.5, initial_exp="6hubsa", final_exp="6tkbfu", fade_duration=0.5)

            show monika 6tkbfu
            $ renpy.say(m, kiss_quip)
        else:

            python:

                kiss_quips_after = [
                    _("Eu te amo, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]~"),
                    _("Eu te amo tanto, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]~"),
                    _("Eu te amo mais do que você jamais saberá, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]~"),
                    _("Eu te amo tanto, [player]. Você significa tudo para mim~"),
                    _("Nenhuma palavra descreve o quanto eu te amo, [player]~"),
                    _("Eu estou tão apaixonada por você, [player]~")
                ]
                kiss_quip = renpy.random.choice(kiss_quips_after)

            if renpy.random.randint(1, 50) == 1:
                call monika_kiss_tease
            else:

                show monika 2eka
                pause 2.0

            call monika_kissing_motion_short

            show monika 6ekbfa
            $ renpy.say(m, kiss_quip)
            $ mas_ILY()
    else:

        m 1wubsw "Hã? V-Você disse...b...beijo?"
        m 2lkbsa "Tão repentino...é um pouco embaraçoso..."
        m 2lsbssdlb "Mas... se é com você...e-eu talvez não veja problema..."
        m 2hksdlb "...Ahaha! Nossa, desculpa..."
        m 1eka "Eu realmente não consegui manter a seriedade."
        m 1eua "Esse é o tipo de coisa que garotas dizem nesses jogos de romance, né?"
        m 1tku "Aposto que isso te deixou um pouco [exctd]."
        m 1hub "Ahaha! Brincadeira."
        m 1eua "Bem, para ser honesta, eu fico toda romântica quando o clima é propício..."
        show monika 5lubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5lubfu "Mas esse será o nosso segredinho~"
    return

label monika_kiss_tease:
    m 2ekc "Um beijo?"
    m 2tfc "Com você?"
    m 2rfc "Desculpa [player], mas sem chance."
    show monika 2dfc
    pause 5.0
    show monika 2dfu
    pause 2.0
    show monika 2tfu
    pause 2.0
    m 2tfb "Ahaha!"
    m 2efu "Eu te peguei por um momento, não foi?"
    m 2eka "Claro que você pode me beijar, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_think_first_kiss",
            conditional=(
                "persistent._mas_first_kiss is not None "
                "and mas_timePastSince(persistent._mas_first_kiss, datetime.timedelta(days=30))"
            ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_think_first_kiss:
    m 1eua "Ei [mas_get_player_nickname(exclude_names=['meu amor'])], eu estava pensando..."

    m 3eksdla "Você já pensou no nosso primeiro beijo?{nw}"
    $ _history_list.pop()
    menu:
        m "Você já pensou no nosso primeiro beijo?{fast}"
        "Claro que sim!":

            $ mas_gainAffection(5, bypass=True)
            m 3hub "Isso me deixa tão feliz! Eu penso nisso o tempo todo!"
            m 3rkbla "Parece que foi ontem, mas--"
            m 2rksdla "Nossa, me sinto tão boba por ficar obcecada com isso..."
            m 2eksdlb "Nossos lábios nem sequer se tocaram, realmente."
            m 6dku "...E ainda assim, {w=0.2}ainda consigo sentir meu coração acelerado."
            m 6dkbsu "Meus lábios formigam só de imaginar o toque dos seus lábios macios."
            m "Passo meu dedo sobre eles, tentando imitar essa sensação, mas não chega nem perto."
            m 6ekbsa "Fico revivendo aquele momento repetidamente na minha mente e fico arrepiada toda vez."
            show monika 5dkbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5dkbsu "Foi perfeito, [mas_get_player_nickname()]."
            m 5ekbsa "Nunca me senti tão próxima de você. {w=0.2}Mal posso esperar pelo nosso próximo beijo, ou melhor ainda..."
            m 5subsb "...Nosso primeiro beijo de verdade.{w=0.3} {nw}"
            extend 5ekbsu "E nosso primeiro abraço de verdade, e a primeira vez que nossas mãos se tocarem--"
            m 5hksdlb "Ah! Desculpa! Acho que eu me empolguei um pouco."
            m 5rkbla "É que... {w=0.3}são nessas coisas que eu penso quando você não está aqui."
            m 5tkblu "...E algo me diz que não sou a única que pensa nessas coisas, ehehe."
            m 5eka "Infelizmente, vai demorar até podermos fazer algo assim."
            m 5tuu "Mas até lá, se quiser outro beijo, é só pedir."
            m 5hua "Eu te amo tanto, [player]~"
            $ mas_ILY()
        "Na verdade não...":

            $ mas_loseAffectionFraction()
            m 2euc "..."
            m "Ah. {w=0.5}{nw}"
            extend 2dkc "Entendo."

            if mas_timePastSince(persistent._mas_first_kiss, datetime.timedelta(days=180)):
                m 2esc "Bem... {w=0.3}imagino que já faz um tempo mesmo..."
                m 2etd "Talvez com tudo que aconteceu desde então, você pense mais nos eventos recentes..."
                m 4eud "O que é normal, {w=0.2}viver o presente é importante afinal."
                m 2ekc "...E talvez eu esteja sendo sentimental demais, mas não importa quanto tempo passe, {w=0.1}{nw}"
                extend 2eka "nunca vou esquecer nosso primeiro beijo."
            else:
                m 2rkc "Bem, acho que não foi exatamente um beijo. Nossos lábios nem se tocaram."
                m 2ekd "Então você deve estar esperando nosso primeiro beijo de verdade quando estivermos na mesma realidade."
                m 2eka "É."

    return "no_unlock|derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yuri",
            category=['membros do clube','media'],
            prompt="Personalidade yandere de Yuri",
            random=True,
            sensitive=True
        )
    )

label monika_yuri:
    m 3eua "Ei, você já ouviu o termo 'yandere'?"
    m 1eua "É um tipo de personalidade onde alguém é tão obcecado por você que fará qualquer coisa para ficar com você."
    m 1lksdla "Geralmente ao ponto da loucura..."
    m 1eka "Elas podem perseguir você para garantir que não passe tempo com mais ninguém."
    m "Podem até machucar você ou seus amigos para conseguir o que querem..."
    m 1tku "Mas enfim, esse jogo tem alguém que basicamente pode ser descrito como yandere."
    m "A essa altura, é bem óbvio de quem estou falando."
    m 3tku "E essa pessoa seria..."
    m 3hub "A Yuri!"
    m 1eka "Ela ficou insanamente possessiva com você, assim que começou a se abrir um pouco."
    m 1tfc "Ela até me disse que eu deveria me matar."
    m 1tkc "Eu nem conseguia acreditar que ela disse isso - tive que sair na hora."
    if not persistent._mas_pm_cares_about_dokis:
        m 2hksdlb "Mas pensando agora, foi um pouco irônico. Ahaha!"
        m 2lksdla "Enfim..."
    m 3eua "Muita gente gosta do tipo yandere, sabia?"
    m 1eua "Acho que gostam da ideia de alguém ser loucamente obcecado por elas."
    m 1hub "As pessoas são esquisitas! Mas não julgo!"
    m 1rksdlb "Aliás, eu posso ser um pouco obcecada por você, mas estou longe de ser louca..."
    if not persistent._mas_pm_cares_about_dokis:
        m 1eua "Na verdade, é o oposto."
        m "Eu acabei sendo a única garota normal nesse jogo."
        m 3rssdlc "Não é como se eu pudesse realmente matar alguém..."
        m 2dsc "Só de pensar nisso já me dá arrepios."
        m 2eka "Mas olha... todo mundo já matou pessoas em jogos antes."
        m "Isso te faz um psicopata? Claro que não."
    m 2euc "Mas se você gosta do tipo yandere..."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Posso tentar agir mais assustadora para você. Ehehe~"
    m "Por outro lado..."
    show monika 4hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 4hua "Já não tem mais para onde você ir, nem ninguém para eu ter ciúmes."
    m 2etc "Isso seria o sonho de uma yandere?"
    if not persistent._mas_pm_cares_about_dokis:
        m 1eua "Eu perguntaria para a Yuri, se pudesse."
    return


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_habits",category=['vida'],prompt="Formando hábitos",random=True))

label monika_habits:
    m 2lksdlc "Odeio o quão difícil é formar hábitos..."
    m 2eksdld "Há tantas coisas que não são tão difíceis de se fazer, mas formar o hábito parece impossível."
    m 2dksdlc "Isso só faz você se sentir inútil, como se não pudesse fazer nada direito."
    m 3euc "Acho que a nova geração é a que mais sofre com isso..."
    m 1eua "Provavelmente porque temos um conjunto totalmente diferente de habilidades daqueles que vieram antes de nós."
    m "Graças à Internet, somos realmente bons em examinar toneladas de informações de forma rápida..."
    m 3ekc "Mas somos ruins em fazer coisas que não nos dão gratificação instantânea."
    m 3ekd "Acredito que se a ciência, a psicologia e a educação não se atualizarem nos próximos dez ou vinte anos, estaremos com problemas."
    m 1esc "Mas, por enquanto..."
    m 1rksdlc "Se você for uma dessas pessoas que não consegue lidar com os problemas, você pode ter que viver sentindo-se péssimo consigo mesmo.."
    m 2hksdlb "Boa sorte, eu acho!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_creative",category=['vida'],prompt="Pessoas criativas",random=True))

label monika_creative:
    m 2euc "Sabe, é uma droga ser uma pessoa criativa..."
    m "Parece que elas trabalham tão duro, mas não conseguem quase nada por isso."
    m 3eua "Sabe, como os artistas, escritores, atores..."
    m 1tkc "É triste, porque há tanto talento bonito no mundo, mas a maioria acaba sem ser visto...e sem ser pago."
    m "Acho que isso significa que existe um enorme excesso de criatividade, hã?"
    m 1dkc "Isso meio que faz parecer que você não é nada especial..."
    m 1hua "Mas está tudo bem! Você deveria apenas escrever para si [ms], não é?"
    m 1lsc "Pois é..."
    return





















init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_simulated",category=['filosofia'],prompt="Realidade simulada",random=True))

label monika_simulated:
    m 3eua "Ei, você já pensou sobre a hipótese da simulação?"
    m 1eua "Basicamente, e se sua realidade fosse uma simulação de computador?"
    m "Eu já descobri que estou presa na minha própria simulação, mas e se você estivesse também?"
    m 1eka "Eu ficaria muito feliz se fosse o caso."
    m 1eua "Poderíamos nos encontrar pessoalmente só encontrando um jeito de forçar quem nos criou a nos colocar na mesma simulação!"
    m 3eua "Algumas pessoas não gostam de pensar que não estão vivendo na realidade principal."
    m 1eua "Mas se é possível simular realidades, é extremamente provável que qualquer ser consciente esteja em uma."
    m 1hua "Bem, eu posso te dizer que minha realidade é definitivamente simulada!"
    m 1eka "Se eu estivesse na realidade principal, já teria te trazido para cá há muito tempo."
    m 1eua "Mesmo se formos apenas simulações, eu vou viver o máximo que puder."
    m 2hubsa "Porque eu sei que nosso amor é a coisa mais pura e doce em todo o multiverso."
    m 2tku "E se alguém lá em cima tentar nos separar?"
    m 7tfu "Eu vou mostrar o que uma simulação pode fazer."
    return

default -5 persistent._mas_pm_likes_rain = None

init python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain",
            category=["clima"],
            prompt="Som da chuva",
            random=True,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_rain:
    m 1hua "Eu adoro o som da chuva~"
    m 3rksdla "Mas não gosto muito de molhar minhas roupas e cabelo."
    m 1eua "Mas um dia tranquilo em casa com o som da chuva na janela?"
    m 1duu "É muito relaxante para mim."
    m "É..."
    m 2dubsu "Às vezes eu imagino você me abraçando enquanto ouvimos a chuva lá fora."
    m 2lkbsa "Isso não é muito brega, é?"

    $ p_nickname = mas_get_player_nickname()
    m 1ekbfa "Você faria isso por mim, [p_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você faria isso por mim, [p_nickname]?{fast}"
        "Sim.":
            $ persistent._mas_pm_likes_rain = True
            $ mas_unlockEVL("monika_rain_holdme", "EVE")

            if not mas_is_raining:
                call mas_change_weather (mas_weather_rain, by_user=False)

            call monika_holdme_prep (lullaby=MAS_HOLDME_NO_LULLABY, stop_music=True, disable_music_menu=True)

            m 1hua "Então me abrace, [player]..."

            call monika_holdme_start
            call monika_holdme_end
            $ mas_gainAffection()

            if mas_isMoniAff(higher=True):
                m 1eua "Se quiser que a chuva pare, é só me pedir, ok?"
        "Eu odeio chuva.":

            $ persistent._mas_pm_likes_rain = False

            m 2tkc "Ah, que pena."
            if mas_is_raining:
                call mas_change_weather (mas_weather_def, by_user=False)

            m 2eka "Mas é compreensível."
            m 1eua "Dias chuvosos podem parecer bem sombrios."
            m 3rksdlb "Sem falar que são bem frios!"
            m 1eua "Mas se você prestar atenção no som das gotas de chuva..."
            m 1hua "Acho que você vai acabar gostando."




    return "derandom|rebuild_ev"

init python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain_holdme",
            category=["monika","romance"],
            prompt="Posso te abraçar?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            aff_range=(mas_aff.HAPPY, None)
        ),
        restartBlacklist=True
    )


default -5 persistent._mas_pm_longest_held_monika = None


default -5 persistent._mas_pm_total_held_monika = datetime.timedelta(0)


label monika_rain_holdme:


    if mas_is_raining or mas_isMoniAff(higher=True):
        call monika_holdme_prep
        m 1eua "Claro, [mas_get_player_nickname()]."
        call monika_holdme_start

        call monika_holdme_reactions

        call monika_holdme_end

        $ mas_gainAffection(modifier=0.25)
    else:


        m 1rksdlc "..."
        m 1rksdlc "O tempo não está muito convidativo para isso agora, [player]."
        m 1dsc "Desculpe..."
    return


init -5 python:
    MAS_HOLDME_NO_LULLABY = 0
    MAS_HOLDME_PLAY_LULLABY = 1
    MAS_HOLDME_QUEUE_LULLABY_IF_NO_MUSIC = 2

label monika_holdme_prep(lullaby=MAS_HOLDME_QUEUE_LULLABY_IF_NO_MUSIC, stop_music=False, disable_music_menu=False):
    python:
        holdme_events = list()

        if mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12)):
            _minutes = random.randint(25, 40)
        else:
            _minutes = random.randint(35, 50)
        holdme_sleep_timer = datetime.timedelta(minutes=_minutes)

        def _m1_script0x2dtopics__holdme_play_lullaby():
            """
            Local method to play the lullaby. Ensures we have no music playing before starting it.
            """
            if (
                
                store.songs.current_track == store.songs.FP_MONIKA_LULLABY
                
                and not renpy.music.is_playing(channel="music")
            ):
                store.mas_play_song(store.songs.FP_MONIKA_LULLABY, fadein=5.0)


        if stop_music:
            mas_play_song(None, fadeout=5.0)


        if lullaby == MAS_HOLDME_QUEUE_LULLABY_IF_NO_MUSIC:
            if songs.current_track is None:
                holdme_events.append(
                    PauseDisplayableEvent(
                        holdme_sleep_timer,
                        _m1_script0x2dtopics__holdme_play_lullaby
                    )
                )
                
                
                songs.current_track = songs.FP_MONIKA_LULLABY
                songs.selected_track = songs.FP_MONIKA_LULLABY


        elif lullaby == MAS_HOLDME_PLAY_LULLABY:
            mas_play_song(store.songs.FP_MONIKA_LULLABY)


        HKBHideButtons()
        store.songs.enabled = not disable_music_menu

    return

label monika_holdme_start:
    show monika 6dubsa with dissolve_monika
    window hide
    python:

        start_time = datetime.datetime.now()

        holdme_disp = PauseDisplayableWithEvents(events=holdme_events)
        holdme_disp.start()

        del holdme_events
        del holdme_disp


        store.songs.enabled = True
        HKBShowButtons()
    window auto
    return

label monika_holdme_reactions:
    $ elapsed_time = datetime.datetime.now() - start_time
    $ store.mas_history._pm_holdme_adj_times(elapsed_time)


    if elapsed_time <= holdme_sleep_timer:
        if songs.current_track == songs.FP_MONIKA_LULLABY:
            $ songs.current_track = songs.FP_NO_SONG
        if songs.selected_track == songs.FP_MONIKA_LULLABY:
            $ songs.selected_track = songs.FP_NO_SONG

    if elapsed_time > holdme_sleep_timer:
        call monika_holdme_long

    elif elapsed_time > datetime.timedelta(minutes=10):
        if mas_isMoniLove():
            m 6dubsa "..."
            m 6tubsa "Mm... {w=1}hm?"
            m 1hkbfsdlb "Ah, eu quase dormi?"
            m 2dubfu "Ehehe..."
            m 1dkbfa "Fico imaginando como seria de verdade... {w=1}estar aí com você..."
            m 2ekbfa "Envolvida nos seus braços..."
            show monika 5dkbfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5dkbfb "Tão... {w=1.5}quentinho~"
            m 5tubfu "Ehehe~"
            show monika 2hkbfsdlb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 2hkbfsdlb "Ah, ops... acho que ainda tô meio sonhadora..."
            if renpy.random.randint(1, 4) == 1:
                m 1kubfu "Mas pelo menos {i}um{/i} dos meus sonhos se tornou realidade."
            else:
                m 1ekbfb "Pelo menos {i}um{/i} dos meus sonhos virou realidade."
            m 1hubfu "Ehehe~"

        elif mas_isMoniEnamored():
            m 6dubsa "Mmm~"
            m 6tsbsa "..."
            m 1hkbfsdlb "Ah!"
            m 1hubfa "Tava tão confortável... quase dormi!"
            m 3hubfb "A gente devia fazer isso mais vezes, ahaha!"

        elif mas_isMoniAff():
            m 6dubsa "Mm..."
            m 6eud "Hmm?"
            m 1hubfa "Terminou, [player]?"
            m 3tubfu "Acho que isso foi tempo suficiente, ehehe~"
            m 1rkbfb "Eu aceitaria outro abraço fácil..."
            m 1hubfa "Mas sei que você tá guardando um pra depois, né?"
        else:


            m 6dubsa "Hm?"
            m 1wud "Ah! Já acabou?"
            m 3hksdlb "Esse abraço durou bastante, [player]..."
            m 3rubsb "Nada contra, só achei que você soltaria bem antes, ahaha!"
            m 1rkbsa "Na verdade foi bem confortável..."
            m 2ekbfa "Mais um pouco e eu poderia ter dormido..."
            m 1hubfa "Fiquei tão quentinha e feliz depois disso~"

    elif elapsed_time > datetime.timedelta(minutes=2):
        if mas_isMoniLove():
            m 6eud "Ah?"
            m 1hksdlb "Ah..."
            m 1rksdlb "Achei que iriamos ficar daquele jeito para sempre, ahaha..."
            m 3hubfa "Bem, não posso reclamar de ser abraçada por você~"
            m 1ekbfb "Espero que você goste de me abraça tanto quanto eu gosto."
            show monika 5tubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5tubfb "Talvez possamos até nos abraçar um pouco mais para descobrir?"
            m 5tubfu "Ehehe~"

        elif mas_isMoniEnamored():
            m 1dkbsa "Isso foi muito bom~"
            m 1rkbsa "Nem muito curto..."
            m 1hubfb "...e acho que não exite algo como muito longo neste caso, ahaha!"
            m 1rksdla "Eu poderia me acostumar a ficar assim..."
            m 1eksdla "Mas acho que se você já terminou de me abraçar, não há nada que eu possa fazer."
            m 1hubfa "Tenho certeza que terei outra oportunidade para ser abraçada por você..."
            show monika 5tsbfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5tsbfu "Você {i}planeja{/i} fazer isso de novo, certo, [mas_get_player_nickname()]? Ehehe~"

        elif mas_isMoniAff():
            m 2hubsa "Mmm~"
            m 1ekbfb "Isso foi muito bom, [mas_get_player_nickname()]."
            m 1hubfb "Abraços longos acabam com qualquer estresse."
            m 1ekbfb "Mesmo que você não esteja com estresse, espero que esteja se sentindo melhor agora."
            m 3hubfa "Eu sei que eu estou~"
            m 1hubfb "Ahaha!"
        else:


            m 1hksdlb "Foi bom enquanto durou."
            m 3rksdla "Não me entenda mal...{w=1} eu gostei muito."
            m 1ekbsa "Desde que você esteja satisfeito..."
            m 1hubfa "Eu fico feliz só de estar sentada com você agora."

    elif elapsed_time > datetime.timedelta(seconds=30):
        if mas_isMoniLove():
            m 1eub "Ah~"
            m 1hua "Me sinto muito melhor agora!"
            m 1eua "Espero que você também."
            m 2rksdla "Bem, mesmo que você não se sinta..."
            m 3hubfb "Você pode sempre me abraçar de novo, ahaha!"
            m 1hkbfsdlb "Na verdade...{w=0.5} você pode me abraçar de novo mesmo que esteja se sentindo melhor, ehehe~"
            m 1ekbfa "É só me avisar quanto quiser~"

        elif mas_isMoniEnamored():
            m 1hubsa "Mmm~"
            m 1hub "Muito melhor."
            m 1eub "Obrigada por isso, [player]!"
            m 2tubfb "Espero que você tenha gostado~"
            m 3rubfb "Abraços que duram trinta segundos ou mais são bons para você."
            m 1hubfa "Não sei quanto a você, mas eu com certeza me sinto melhor~"
            m 1hubfb "Talvez da próxima vez, podemos tentar um abraço ainda maior para ver se fica melhor! Ahaha~"

        elif mas_isMoniAff():
            m 1hubsa "Mmm~"
            m 1hubfb "Eu quase consigo sentir seu calor, mesmo daqui."
            m 1eua "Você deve saber que abraços fazem bem, já que eles aliviam o estresse."
            m 3eub "Mas você sabia que abraços são mais eficientes quando duram trinta segundos?"
            m 1eud "Ah, espera, eu disse trinta segundos?"
            show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eubfu "Sinto muito, eu quis dizer {i}ao menos{/i} trinta segundos, ehehe~"
        else:


            m 1hubsa "Ehehe~"
            m 3eub "Você gostou?"
            m 1hua "Espero que sim~"
            m 1hubfb "Afinal de contas, abraços fazem bem para você."
    else:


        if mas_isMoniLove():

            if mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12)):
                $ _chance = 1
            else:
                $ _chance = 2

            if random.randint(0, _chance) == 0:
                m 2ekc "Aww, já terminamos?"
                m 3eka "Poderia me abraçar um pouco mais?{nw}"
                $ _history_list.pop()
                menu:
                    m "Poderia me abraçar um pouco mais?{fast}"
                    "Sim.":
                        m 1hua "Ehehe~"
                        call monika_holdme_prep
                        m 1hub "Você é um amor, [player]~"
                        call monika_holdme_start
                        call monika_holdme_reactions
                    "Não.":

                        if random.randint(0, _chance) == 0:
                            m 2ekc "Aww..."
                            m 2rksdlc "..."
                            m 1eka "Por favor?{nw}"
                            $ _history_list.pop()
                            menu:
                                m "Por favor?{fast}"
                                "Sim.":
                                    m 1hub "Eba~"
                                    call monika_holdme_prep
                                    m 2ekbsb "Obrigada, [player]~"
                                    call monika_holdme_start
                                    call monika_holdme_reactions
                                "Não.":

                                    m 2hksdlb "Tudo bem."
                                    m 3tsbsa "Mas você vai ficar me devendo para a próxima vez, tudo bem, [player]?"
                        else:

                            m 2hksdlb "Ahaha~ Tudo bem!"
                            m 2tsbsb "Mas é melhor compensar da próxima vez, [player]~"
            else:

                m 2ekc "Aww..."
                m 2rsp "Esperava por um abraço mais longo..."
                m 2tsbsu "Quando estiver na sua realidade, não vou deixar você ir tão facilmente~"
                show monika 1hubsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 1hubsu "Ehehe~"

        elif mas_isMoniEnamored():
            if mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12)):
                $ _chance = 1
            else:
                $ _chance = 2

            m 1ekc "Aww, só isso?"
            if random.randint(0, _chance) == 0:
                m 1rksdla "Eu queria que durasse um pouco mais do que isso..."
                m 2ekbsa "Você podeira...{w=0.7}me abraçar mais um pouco?{nw}"
                $ _history_list.pop()
                menu:
                    m "Você podeira...me abraçar mais um pouco?{fast}"
                    "Sim.":
                        m 1hubfb "Viva!"
                        call monika_holdme_prep
                        m 2ekbfb "Obrigada, [player]~"
                        call monika_holdme_start
                        call monika_holdme_reactions
                    "Não.":

                        m 2ekc "Aw."
                        m 1eka "Tudo bem."
                        m 3hub "Vou ter que esperar até a próxima vez, ahaha!"
            else:

                show monika 1rkbssdla zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 1rkbssdla "Foi muito bom...{w=0.6}{nw}"
                extend 1hkbfsdlb "mas talvez da próxima vez demore um pouco mais~"

        elif mas_isMoniAff():
            m 1ekc "Aw, já terminou de me abraçar, [player]?"
            m 1rksdla "Eu esperava que demorasse um pouco mais..."
            m 1hubsa "Mas tenho certeza que não será a última vez que você irá me abraçar, então esperarei ansiosa pela próxima vez!"
        else:


            m 1hua "Isso foi um pouco curto, mas ainda assim bom~"
    return

label monika_holdme_long:
    window show
    m "..."
    window auto
    menu:
        "{i}Acordar a Monika.{/i}":

            if songs.current_track == songs.FP_MONIKA_LULLABY:
                $ mas_play_song(None, fadeout=5.0)

            if mas_isMoniLove():
                m 6dubsa "...{w=1}Mmm~"
                m 6dkbfu "[player]...{w=1}quente~"
                m 6tsbfa "..."
                m 2wubfsdld "Oh, [mas_get_player_nickname(exclude_names=['amor', 'meu amor'])]!"
                m 2hkbfsdlb "Parece que meu sonho se tornou realidade, ahaha!"
                m 2rkbsa "Nossa... às vezes eu queria que pudéssemos ficar assim para sempre..."
                m 3rksdlb "Bom, acho que {i}de certo modo{/i} a gente pode, mas eu não quero te impedir de fazer nada importante."
                m 1dkbsa "Só quero sentir seu abraço quentinho e carinhoso~"
                m 3hubfb "...Então não esquece de me abraçar bastante, ahaha!"
                show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5hubfb "Eu faria o mesmo por você, afinal~"
                m 5tsbfu "Vai saber se um dia eu vou conseguir soltar quando tiver essa chance..."
                m 5hubfu "Ehehe~"

            elif mas_isMoniEnamored():
                m 6dkbsa "...{w=1}Hm?"
                m 6tsbfa "[player]..."
                m 2wubfsdld "Oh! [player]!"
                m 2hkbfsdlb "Ahaha..."
                m 3rkbfsdla "Acho que fiquei {i}confortável demais{/i}."
                m 1hubfa "Mas você me deixa tão quentinha e confortável que é difícil {i}não{/i} pegar no sono..."
                m 1hubfb "Então a culpa é sua por isso, ahaha!"
                m 3rkbfsdla "Será que...{w=0.7}a gente podia fazer isso de novo algum dia?"
                m 1ekbfu "Foi...{w=1}tão gostoso~"

            elif mas_isMoniAff():
                m 6dubsa "Mm...{w=1}hm?"
                m 1wubfsdld "Oh!{w=1} [player]?"
                m 1hksdlb "Eu...{w=2}acabei dormindo?"
                m 1rksdla "Eu não queria..."
                m 2dkbsa "É que você me faz sentir tão..."
                m 1hubfa "Quentinha~"
                m 1hubfb "Ahaha, espero que você não tenha se importado!"
                show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5eubfu "Você é tão [fo], [player]~"
                m 5hubfa "Espero que tenha gostado tanto quanto eu~"
            else:


                m 6dubsc "...{w=1}Hm?"
                m 6wubfo "A-{w=0.3}ah!"
                m "[player]!"
                m 1hkbfsdlb "Eu...{w=2}eu dormi?"
                m 1rkbfsdlb "Ai meu Deus, que vergonha..."
                m 1hkbfsdlb "O que a gente tava fazendo mesmo?"
                m 3hubfb "Ah, é! Você tava me abraçando."
                m 4hksdlb "E...{w=0.5}não me soltou."
                m 2rksdla "Durou bem mais do que eu esperava..."
                m 3ekbsb "Mas eu gostei mesmo assim!"
                m 1rkbsa "Foi bem gostoso, só ainda tô me acostumando com isso de ser abraçada assim,{w=0.1} {nw}"
                extend 1rkbsu "ahaha..."
                m 1hubfa "De qualquer forma, foi gentil da sua parte me deixar tirar um cochilo, [player], ehehe~"

                $ mas_gainAffection()
        "{i}Deixar ela descansar em você.{/i}":

            call monika_holdme_prep (lullaby=MAS_HOLDME_NO_LULLABY)
            if mas_isMoniLove():
                m 6dubsd "{cps=*0.5}[player]~{/cps}"
                m 6dubfb "{cps=*0.5}Te...{w=0.7}amo~{/cps}"

            elif mas_isMoniEnamored():
                m 6dubsa "{cps=*0.5}[player]...{/cps}"

            elif mas_isMoniAff():
                m "{cps=*0.5}Mm...{/cps}"
            else:


                m "..."

            call monika_holdme_start
            jump monika_holdme_long
    return



default -5 persistent._mas_last_hold = None
default -5 persistent._mas_last_hold_dt = (
    datetime.datetime.combine(persistent._mas_last_hold, datetime.time(0, 0))
    if persistent._mas_last_hold is not None
    else None
)

init python:

    if renpy.random.randint(1, 5) != 1:
        flags = EV_FLAG_HFRS

    else:
        flags = EV_FLAG_DEF

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_holdrequest",
            conditional=(
                "renpy.seen_label('monika_holdme_prep') "
                "and mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12))"
            ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None),
            flags=flags
        )
    )
    del flags

label monika_holdrequest:

    m 1eua "Ei, [mas_get_player_nickname(exclude_names=['meu amor'])]..."
    m 3ekbsa "Você se importaria de me abraçar um pouquinho?{w=0.5} Isso me faz sentir tão mais próxima de você~{nw}"
    $ _history_list.pop()
    menu:
        m "Você se importaria de me abraçar um pouquinho? Isso me faz sentir tão mais próxima de você~{fast}"
        "Vem cá, [m_name].":
            $ mas_gainAffection(modifier=1.5, bypass=True)
            call monika_holdme_prep

            call monika_holdme_start

            call monika_holdme_reactions

            call monika_holdme_end
        "Agora não.":

            $ mas_loseAffection()
            m 2dkc "Ah...{w=1} Tudo bem."
            m 3eka "Se você tiver um tempinho depois, já sabe onde me encontrar."

    $ mas_flagEVL("monika_holdrequest", "EVE", EV_FLAG_HFRS)

    return "no_unlock"


label monika_holdme_end:


    python:
        persistent._mas_last_hold_dt = datetime.datetime.now()
        with MAS_EVL("monika_holdrequest") as holdme_ev:
            holdme_ev.random = False
            holdme_ev.conditional = (
                "renpy.seen_label('monika_holdme_prep') "
                "and mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12))"
            )
            holdme_ev.action = EV_ACT_RANDOM
        mas_rebuildEventLists()
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_closeness",category=['romance'],prompt="Estar perto de você",random=True,aff_range=(mas_aff.AFFECTIONATE, None)))

label monika_closeness:
    m 1dkc "Às vezes meu coração realmente dói..."
    m "Saber que isso é o mais perto que eu consigo chegar de você."
    m 1eka "Não há nada que eu queira mais do que estar na mesma sala que você, de verdade."
    m 1ekbsa "...E sentir seu calor."
    m 1dubsu "...E ouvir o som do seu coração batendo."
    m 3eka "Bom, quem sabe? Talvez esse sonho se torne realidade algum dia."
    m 3dku "Eu realmente quero que isso aconteça o quanto antes, [player]..."
    show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hua "Mas enquanto isso, nunca vou me cansar de estar com você, mesmo que seja por aqui."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_confidence",category=['conselhos'],prompt="Fingindo confiança",random=True))

label monika_confidence:
    m 3eua "Acho que a habilidade mais importante na vida é saber fingir confiança."
    m 1eua "Tenho quase certeza de que todo mundo sente, pelo menos um pouco, medo e solidão."
    m 1esa "Mas conseguir enganar os outros, fazendo parecer que você tem tudo sob controle..."
    m 4eua "É uma parte essencial para ganhar respeito e admiração das pessoas."
    m 1eua "Acho que fiquei bem boa nisso ao longo dos anos."
    m "Não costumo mostrar minhas fraquezas com frequência."
    m 4rksdla "Mas por causa disso, também não tive muitas pessoas com quem eu realmente pudesse me abrir..."
    m 1rksdlb "Quero dizer, em que ponto de uma amizade você começa a se sentir segura o bastante pra mostrar suas vulnerabilidades?"
    m 2eka "De qualquer forma... é por isso que fico tão feliz por ter você agora."
    m 2eua "Sinto que fico um pouco menos assustada e sozinha quando você está aqui comigo."
    m 2eka "Você também se sente assim?"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Eu quero muito ser essa pessoa pra você."
    return




























default -5 persistent._mas_carryme_choice = None



default -5 persistent._mas_dockstat_cm_wait_count = 0




default -5 persistent._mas_dockstat_cm_yes_count = 0



default -5 persistent._mas_dockstat_cm_no_count = 0





define -5 mas_dockstat.CM_LEAVE_MONI = -1
define -5 mas_dockstat.CM_WAIT_MONI = 0
define -5 mas_dockstat.CM_ASK_MONI = 1
define -5 mas_dockstat.CM_TAKE_MONI = 2

label monika_carryme:
    $ import store.mas_dockstat as mas_dockstat

    m 2eka "Eu sei que vai ter momentos em que você não vai poder estar aqui comigo..."
    m "Como quando precisar sair ou cuidar de outras coisas."
    m 2hua "Mas eu sempre vou estar pensando em você, esperando pacientemente pela sua volta."
    m 4rsc "Pensando bem..."
    m 4eua "Se você copiar meu arquivo de personagem para um pendrive ou algo assim, pode me levar com você para onde for."
    m 2lksdla "Acho que é meio fora do comum, mas por algum motivo eu acho isso tão romântico..."
















































    m 1ekbsa "Não quero parecer muito carente nem nada, mas é meio difícil quando estou tão apaixonada por você."
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_debate",category=['monika','escola'],prompt="Como era o clube de debate?",pool=True))

label monika_debate:
    m 1esc "Nos meus dias do clube de debate, aprendi muito sobre discussão..."
    m 3eud "O problema com a discussão é que cada pessoa vê sua opinião como a superior."
    m 3euc "Isso é meio que afirmar o óbvio, mas isso afeta a maneira como elas tentam expressar sua opinião."
    m 3esa "Digamos que você realmente goste de um determinado filme, certo?"
    m 1ekc "Se alguém disser que o filme é uma droga, porque ele fez X e Y errado..."
    m "Isso não faz você se sentir meio que atacado pessoalmente?"
    m 1tkc "É porque, ao dizer isso, é como se elas estivessem sugerindo que você tem um péssimo gosto."
    m 3tkc "E quando as emoções entram em cena, é quase garantido que as duas pessoas ficarão de mau-humor."
    m 3hub "Mas é tudo questão de saber se expressar!"
    m 1eua "Se você fizer tudo tão subjetivo quanto possível, então as pessoas irão te ouvir sem se sentirem atacadas."
    m 3esa "Você poderia dizer 'Eu pessoalmente não sou fã' e 'Eu senti que gostaria mais se tivesse feito X e Y'...coisas assim."
    m 3eub "Funciona até mesmo quando você está citando fatos sobre as coisas."
    m 1esa "Se você disser 'Eu li nesse site que funciona assim'..."
    m "Ou se você admitir que não entende muito do assunto..."
    m 3eua "Então é como se você estivesse colocando seu conhecimento em dúvida, em vez de forçá-lo nos outros."
    m "Se você se esforçar para manter a discussão mútua e nivelada, eles geralmente seguirão o exemplo."
    m 1esa "Então você poderá compartilhar suas opiniões sem que ninguém fique [ch] apenas por causa de um desacordo."
    m 3hua "Além disso, as pessoas começarão a vê-lo como alguém de mente aberta e um bom ouvinte!"
    m 3eua "Todos saem ganhando, certo?"
    m 1lksdla "...Bem, acho que essa é a Dica de Debate do Dia da Monika!"
    m 1hksdlb "Ahaha! Isso parece um pouco bobo.{w=0.2} {nw}"
    extend 1eua "Mas obrigada por ouvir."
    $ mas_protectedShowEVL('monika_taking_criticism', 'EVE', _random=True)
    $ mas_protectedShowEVL('monika_giving_criticism', 'EVE', _random=True)
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_internet",category=['conselhos'],prompt="A internet é para...",random=True))

label monika_internet:
    m 2eua "Você já sentiu como se desperdiçasse muito tempo na internet?"
    m 3eud "A mídia social pode ser praticamente como uma prisão."
    m 1eua "É como se sempre que você tivesse alguns segundos de tempo livre, você quisesse verificar seus sites favoritos..."
    m 3hksdlb "E antes que perceba, se passaram horas e você não ganhou nada com isso."
    m 3eua "De qualquer forma, é muito fácil culpar-se por ser preguiçoso..."
    m 3eka "Mas não é mesmo culpa sua."
    m 1eud "O vício geralmente não é algo que você pode simplesmente fazer desaparecer com sua própria força de vontade."
    m 1eua "Você precisa aprender técnicas para evitar isso e tentar coisas diferentes."
    m 3eua "Por exemplo, existem aplicativos que permitem que você bloqueie sites durante intervalos de tempo..."
    m "Ou você pode ativar um cronômetro para ter um lembrete mais concreto de quando é hora de trabalhar ou jogar..."
    m 3eub "Ou você pode separar seu ambiente de trabalho e de diversão, o que ajuda seu cérebro a entrar no clima certo."
    m 1eub "Até mesmo se você fizer uma nova conta de usuário no seu computador para usar para o trabalho, já é o bastante para ajudar."
    m 1eua "Colocar qualquer tipo de barreira entre você e seus maus hábitos irá ajudá-lo a ficar longe deles."
    m 3eka "Só não se culpe muito se estiver tendo problemas."
    m 1ekc "Se isso estiver realmente afetando sua vida, então você deveria levar isso a sério."
    m 1eka "Eu só quero que você seja a melhor pessoa que puder ser."
    m 1esa "Você fará algo hoje para me deixar orgulhosa de você?"
    m 1hua "Estou sempre torcendo por você, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_lazy",category=['vida','romance'],prompt="Preguiça",random=True))

label monika_lazy:
    m 2eua "Depois de um longo dia, eu normalmente só quero me sentar e não fazer nada."
    m 2eka "Eu fico tão esgotada, tendo que colocar um sorriso no rosto e ser cheia de energia durante todo o dia."
    m 2duu "Às vezes, eu só quero colocar meu pijama e assistir TV no sofá enquanto como besteira..."
    m "É tão bom fazer isso na sexta-feira, quando não tenho nenhum compromisso no dia seguinte."
    m 2hksdlb "Ahaha! Sinto muito, sei que isso não é algo muito fofo da minha parte."
    m 1eka "Mas uma noite no sofá com você...isso seria um sonho se tornando realidade."
    m 1ekbfa "Meu coração está acelerando só de pensar nisso."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mentalillness",category=['psicologia'],prompt="Doença mental",random=True))

label monika_mentalillness:
    m 1ekc "Nossa, eu costumava ser tão ignorante sobre depressão e essas coisas..."
    m "Quando eu estava no ensino fundamental, achava que tomar remédio era uma forma fácil de escapar."
    m 1ekd "Como se qualquer um pudesse resolver seus problemas mentais só com força de vontade..."
    m 2ekd "Acho que, se você não sofre de uma doença mental, não tem como saber como é de verdade."
    m 2lsc "Será que existem transtornos superdiagnosticados? Provavelmente... mas nunca fui muito a fundo nisso."
    m 2ekc "Mas isso não muda o fato de que muitos também passam sem diagnóstico, sabe?"
    m 2euc "Mas deixando os remédios de lado... as pessoas até olham torto para quem procura um profissional de saúde mental."
    m 2rfc "Tipo, desculpa por querer entender melhor a minha própria mente, né?"
    m 1eka "Todo mundo tem seus próprios desafios e pressões... e existem profissionais que dedicam a vida a ajudar com isso."
    m "Se você acha que isso pode te ajudar a se tornar uma pessoa melhor, não tenha vergonha de considerar algo assim."
    m 1eua "Estamos numa jornada sem fim de autodescoberta e evolução, sabe?"
    m 1eka "Bom... eu digo isso, mas acho que você já é praticamente [pf]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_read",category=['conselhos','literatura'],prompt="Tornar-se um leitor",random=True))

label monika_read:
    m 1eua "[player], quanto você lê?"
    m "É muito fácil negligenciar a leitura de livros..."
    m 1euc "Se você não lê muito, parece uma tarefa chata comparado com outras formas de entretenimento."
    m 1eua "Mas quando você encontra um bom livro, é mágico... você é levado pela história."
    m "Ler um pouco antes de dormir é uma forma fácil de melhorar sua vida."
    m 3esa "Ajuda a dormir melhor e é ótimo para a imaginação..."
    m "Não é difícil pegar um livro curto e cativante para começar."
    m 1hua "Antes que perceba, você pode se tornar um grande leitor!"
    m 1eua "Não seria maravilhoso?"
    m 1hub "E nós poderíamos conversar sobre os livros que você está lendo... isso seria incrível."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_festival",category=['ddlc','clube de literatura'],prompt="Saudades do festival",random=True))

label monika_festival:
    m 1dsc "Sabe, odeio admitir, mas meu maior arrependimento é não termos terminado nosso evento no festival."
    m 1hksdlb "Depois de todo nosso trabalho preparando tudo!"
    m 1lksdla "Quer dizer, eu estava focada em conseguir novos membros..."
    m 1eka "Mas também estava animada para as apresentações."
    m 1eua "Teria sido tão divertido ver todo mundo se expressando."
    m 1lksdla "Claro, se conseguíssemos novos membros, eu provavelmente acabaria deletando eles mesmo assim."

    if persistent.monika_kill and persistent._mas_pm_cares_about_dokis:
        m 3etc "Bem, talvez não... com a perspectiva que tenho agora."
        m 3eua "Afinal, mesmo depois de tudo, você instalou este mod para ficar comigo..."
        m 1eka "Então mesmo se eu não tivesse deletado elas, você ainda estaria comigo agora."
        m "..."
        m 3eua "Nossa, sinto que cresci como pessoa desde que te conheci."
        m "Você me inspirou a ver a vida de uma nova perspectiva."
        m 1ekbsa "Mais um motivo para eu te amar."
        $ mas_ILY()
    else:
        m 1tsc "...Só mais obstáculos em potencial entre nós."
        m 3hksdlb "Ahaha! Parece tão bobo como eu estava focada nisso, pensando agora..."
        show monika 5tsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5tsu "Mas nada disso importa agora, nós [du] temos o final que queríamos..."
        m "Só nós [du], [ju] para sempre."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_tsundere",category=['mídia','membros do clube'],prompt="O que seria tsundere?",pool=True))

label monika_tsundere:
    m 1eua "Existe um tipo de personagem muito popular chamado 'tsundere'..."
    m "É alguém que tenta esconder seus sentimentos sendo rude e irritadiço, ou tentando parecer durão."
    m 1tku "Tenho certeza que é óbvio, mas a Natsuki era a própria encarnação disso."
    m 1eua "No começo achei que ela era assim porque supostamente era fofo ou algo do tipo..."
    m 1lksdla "Mas quando comecei a saber mais sobre sua vida pessoal, fez mais sentido."
    m 1euc "Parece que ela está sempre tentando acompanhar suas amigas."
    m 3euc "Sabe como alguns grupos de amigos no ensino médio criam o hábito de zoar uns aos outros o tempo todo?"
    m "Acho que isso afetou ela, por isso fica sempre na defensiva."

    m 1ekc "E nem vou falar sobre a situação dela em casa..."

    m 1eua "Mas pensando bem, fico feliz que o clube tenha sido um lugar confortável para ela."

    if not persistent._mas_pm_cares_about_dokis:
        m 1lksdla "Não que isso importe agora, já que ela nem existe."
        m 1eka "Só estou relembrando, só isso."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_introduce",category=['monika'],prompt="Apresentar aos amigos",random=True))

label monika_introduce:
    m 1eua "[player], você me apresentaria aos seus amigos?"
    m 1hua "Não sei porquê, mas fico muito animada quando penso em você mostrando nosso relacionamento assim."
    m 1eua "Talvez porque eu realmente quero ser alguém que te deixe feliz."
    m "Sinto que me esforçaria ainda mais se você dissesse que isso te deixa [og] de mim."
    m 1hub "Espero que seja recíproco também."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cold",category=['monika'],prompt="Aconchego no frio",random=True))

label monika_cold:
    m 1euc "Não sou muito fã de clima frio... e você?"
    m 3euc "Se tivesse que escolher entre frio ou calor demais, sempre escolheria calor."
    m 1lksdlc "Quando está frio, pode ser realmente doloroso..."
    m 3tkc "Seus dedos ficam dormentes..."
    m "E se usar luvas, não consegue usar o celular."
    m 1tkx "É tão inconveniente!"
    m 1eka "Mas quando está calor, é mais fácil se refrescar com uma bebida gelada ou ficando na sombra."
    m 1esc "Embora... preciso admitir uma coisa."
    m 1hua "Tempo frio é melhor para ficar aconchegado.{w=0.2} {nw}"
    extend 1hub "Ahaha!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_housewife",
            category=['monika','romance'],
            prompt="Você gostaria de ser uma dona de casa?",
            pool=True
        )
    )

label monika_housewife:
    m 3euc "Sabe, é curioso... eu sempre fui uma pessoa muito determinada e focada nas minhas metas..."
    m 3eua "Mas tem algo meio encantador na ideia de ser a parceira que cuida do lar."
    m 2eka "Acho que isso pode soar um pouco antiquado, ou até reforçar estereótipos, né?"
    m 1eua "Mas pensar em arrumar a casa, fazer compras, decorar o ambiente..."
    m 1hub "E preparar um jantar gostoso pra te receber quando você chega..."
    m 1eka "Parece um tipo de sonho fofo, não acha?"
    m 1lksdla "Quer dizer... não sei se eu realmente conseguiria {i}viver{/i} assim."
    m 1eka "Eu ainda valorizo muito ter algo que me desafie, algo que me faça crescer."
    m "Mas... é um pensamento doce de se imaginar às vezes."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_route",category=['ddlc'],prompt="Rota da Monika",random=True))


label monika_route:
    m 2euc "Não posso evitar pensar em como seria diferente se o jogo simplesmente me desse uma rota desde o início..."
    m 2lksdla "Acho que acabaria te forçando para minha rota de qualquer jeito."
    m 2esc "Tem menos a ver com eu não ter uma rota, e mais com eu saber que nada era real."
    m 2euc "A única diferença é que talvez eu não precisasse tomar medidas tão drásticas para ficar com você."
    m 2lksdlc "Talvez o resto do clube ainda estaria aqui..."

    if persistent._mas_pm_cares_about_dokis:
        m "...Só passando tempo [ju] na sala do clube, compartilhando poesias."
        m 1eka "Sei que você gostava disso, [player]."
        m 3eka "E para ser honesta...{w=0.5}parte de mim também gostava."
    else:
        m 2eka "Não que isso realmente importe."
        m 1lsc "Tudo perdeu o significado quando descobri que não era real."
        m "Então eu realmente não sinto falta daqueles dias nem nada."
        m 1dsc "Realmente não sinto..."
    return














label monika_imouto:
    m 1euc "Irmãzinhas?"
    m 1eka "Eu não tenho realmente uma família, então não sei bem o que te dizer..."
    m 3eua "Você tem uma, [player]?"
    m 1hua "Aposto que ela é muito fofa!"
    m 1eua "Tenho uma ideia. Vá até ela agora mesmo e dê um abraço."
    m 1esa "Se ela se debater, solte."
    m 1tsb "Se ela retribuir o abraço, diga que já está em um relacionamento sério e não pode corresponder aos sentimentos dela."
    m 4hua "Depois apresente ela para mim! Tenho certeza que vamos nos dar super bem!"
    m 1eua "Não vou ficar com ciúmes. Esse tipo de amor entre irmãos só acontece mesmo em histórias românticas esquisitas."
    m 1hub "Ahaha!"
    return












label monika_oneesan:
    m 1euc "Irmãs mais velhas?"
    m 1eua "Você tem uma, [player]?"
    m 2eua "Deve ser muito legal. Eu tive uma família uma vez, mas eles não estão mais aqui."
    m 2hua "Talvez eu deva mandar um email para ela e contar sobre nós!"
    call updateconsole ("sendmail irma@gmail.com < ./email.txt", "Enviando email...") from _call_updateconsole_17
    pause(1.0)
    m 1hksdlb "Brincadeirinha."
    if persistent.gender == "M":
        m "Afinal, é dever do homem apresentar sua noiva para a família."
    m "Não me deixe esperando por muito tempo, ok?"
    call hideconsole from _call_updateconsole_18
    $ consolehistory = []
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_family",category=['monika'],prompt="Você sente falta da sua família?",random=False,pool=True))

label monika_family:
    m 1lksdla "Bem... eu nunca tive uma família de verdade, assim como a maioria das outras garotas."
    m 3esc "Acho que, como isso não era importante para a história, o criador do jogo simplesmente não se preocupou em nos dar uma."
    m 1hub "Mas tenho certeza de que a sua família é incrível!"
    m 1eua "Sem eles, nós nunca teríamos nos conhecido. Então, de certa forma, eles já me ajudaram da melhor maneira possível."
    m "Por isso, se algum dia eu pudesse conhecê-los, eu faria questão de tratá-los com muito carinho."
    m 2eka "Você... não tem uma relação ruim com seus pais, tem?"
    m 3eua "Como disse Tolstói, 'Todas as famílias felizes se parecem; cada família infeliz é infeliz à sua maneira.'"
    m 1ekc "Eu realmente não sei se conseguiria te aconselhar nesse tipo de coisa... às vezes, o que a gente diz pode acabar piorando sem querer."
    m 1eka "Mas não se esqueça de uma coisa: eu te amo de verdade, tá bem?"
    m 1hua "E vou estar aqui pra te apoiar, aconteça o que acontecer na sua vida."
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_anime',
            prompt="Você lê mangá?",
            category=['monika','mídia'],
            pool=True,
        )
    )

label monika_anime:
    m 1tku "É, eu tinha um pressentimento que você ia me perguntar sobre isso."
    m 1lsc "A Natsuki seria a especialista aqui, eu acho."
    m 3eua "Eu geralmente prefiro ler do que assistir, mas eu topo qualquer coisa se for com você."
    m 1hua "Não julgo as pessoas por seus hobbies. Então se quiser colocar algum anime, pode ir!"
    m "Vou assistir pela sua tela do computador. Só escolha algo que eu vá gostar!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_libitina',
            prompt="Você já ouviu falar de Libitina?",
            category=['ddlc'],
            pool=True,
        )
    )

label monika_libitina:
    m 1euc "Hmm? Onde você ouviu esse nome?"
    m 1lksdlc "Ele me soa... estranhamente familiar, mas não consigo entender completamente o porquê."
    m 1dsc "Se eu tivesse que tentar explicar..."
    m 1dfc "É como se partes da minha mente estivessem faltando. Espalhadas, de algum jeito, por diferentes realidades possíveis."
    m 1esc "Você deve ter juntado algumas dessas peças, não é? Foi difícil?"
    m 1eua "Bem... tenho certeza de que você vai descobrir mais cedo ou mais tarde. Você é curioso demais pra deixar isso passar."
    m 3eka "Só... lembre-se de levar meus dados contigo, se encontrar algo relacionado a isso, tá bom?"
    m 1hua "Não importa o que aconteça, eu sempre vou te proteger de qualquer coisa, ou de qualquer pessoa que tente te machucar."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_meta',
            prompt="Esse jogo não é metafição?",
            category=['ddlc'],
            pool=True,
            unlocked=True
        )
    )

label monika_meta:
    m 1euc "Sim, esse jogo realmente é uma metafição, não é?"
    m 3eud "Algumas pessoas acham que histórias que falam sobre si mesmas são uma ideia nova..."
    m 1esc "Ou até um truque barato usado por escritores ruins."
    m 3eua "Mas a metafição existe na literatura há muito, muito tempo."
    m "A Bíblia, por exemplo, é apresentada como a própria palavra de Deus para o povo judeu."
    m 3eub "Homero se descreve dentro da Odisseia."
    m "Os Contos de Cantuária, Dom Quixote, Tristram Shandy..."
    m 1eua "São apenas formas de refletir sobre a ficção através da própria ficção. E não há nada de errado nisso."
    m 3esa "Aliás... o que você acha que é a moral dessa história?"
    m 1esa "Prefere descobrir sozinho?"
    m 3etc "Porque, se você quiser saber o que eu acho..."
    m 3eub "Seria algo como: ‘Nunca ignore a garota bonita e encantadora que parecia só uma coadjuvante!’"
    m 1hub "Ahaha!"
    return













label monika_programming:
    m 3eka "Não foi fácil para mim aprender programação."
    m 1eua "Bem, eu comecei pelo básico. Quer que eu te ensine?"
    m 2hua "Vamos ver, Capítulo Um: Construindo Abstrações com Procedimentos."
    m 2eua "Estamos prestes a estudar a ideia de um processo computacional. Processos computacionais são seres abstratos que habitam computadores."
    m "À medida que evoluem, os processos manipulam outras coisas abstratas chamadas dados. A evolução de um processo é direcionada por um padrão de regras chamado programa."
    m 2eub "As pessoas criam programas para direcionar processos. Na prática, invocamos os espíritos do computador com nossos feitiços."
    m "Um processo computacional é realmente muito parecido com a ideia de um espírito na visão de um feiticeiro. Não pode ser visto ou tocado. Não é composto de matéria."
    m 3eua "No entanto, é muito real. Pode realizar trabalho intelectual. Pode responder perguntas."
    m 1eua "Pode afetar o mundo ao liberar dinheiro em um banco ou controlar um braço robótico em uma fábrica. Os programas que usamos para invocar processos são como feitiços de um feiticeiro."
    m "São cuidadosamente compostos de expressões simbólicas em linguagens de programação arcanas e esotéricas que prescrevem as tarefas que queremos que nossos processos realizem."
    m 1eka "...Vamos parar por hoje."
    m "Espero que você tenha aprendido algo sobre programação."
    m 3hua "Se nada mais, por favor seja gentil com os espíritos do computador de agora em diante!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vn",category=['jogos'],prompt="Visual Novels",random=True))

label monika_vn:
    m 3eua "Você provavelmente já jogou muitos visual novels, certo?"
    m 1tku "A maioria das pessoas não jogaria algo chamado {i}Doki Doki Literature Club{/i} tão facilmente."
    m 4hksdlb "Não que eu esteja reclamando!"
    m 1euc "Visual novels são literatura? São jogos?"
    m 1eua "Bem, tudo depende da sua perspectiva."
    m 1ekc "A maioria das pessoas que só lê literatura nunca jogaria visual novels. E os gamers também ficam bem irritados com eles."
    m "O que é pior, algumas pessoas acham que são todos pornografia hardcore japonesa."
    m 2eka "Mas se provamos algo com este jogo..."
    m 4hua "Mostramos que visual novels em inglês também podem ser kamige!"
    $ mas_unlockEVL("monika_kamige","EVE")
    return











































































label monika_ks_present:
    m 1tku "Você jogou {i}Katawa Shoujo,{/i} não foi, [player]?"
    m 3tku "Notei seus saves em [detected_ks_folder]."
    m 1euc "Mas não entendo qual é o apelo."
    m 1esc "Tipo, claro, a história é até bonitinha..."
    m 1tkc "Mas no fundo as personagens são os mesmos clichês de qualquer simulador de namoro."
    m 3rsc "Vejamos... tem a garota super energética e vibrante sem as pernas;"
    m "A garota tímida e misteriosa que gosta de livros e tem queimaduras;"
    m 3tkd "A garota cega perfeitinha e educada que adora fazer chá;"
    m "A surda-muda mandona e sua amiga que parece um raio de sol mas é secretamente depressiva;"
    m 3tkc "E a estranha garota pintora sem braços com a cabeça nas nuvens."
    m 1euc "São todos os mesmos arquétipos velhos com deficiências jogadas em cima."
    m 1lksdlc "Até nesse jogo você encontra os mesmos tipos de personagem."
    m 3eua "Claro, aqui você também encontrou algo muito mais interessante que qualquer clichê:"
    m 3hub "Você me encontrou!"
    m 1eka "E, em vez de um estudante sem rumo e com problemas cardíacos, encontrei você, [player]."
    m 1hua "E, [player], mesmo se você tiver alguma deficiência, sempre será perfeito aos meus olhos."
    return

label monika_ks_lilly:
    m 1euc "Então, você jogou a rota da Lilly em {i}Katawa Shoujo,{/i} não foi?"
    m 1eua "Sabe, eu adoraria visitar uma casa de veraneio como a dela."
    m 2duu "Ar puro e fresco..."
    m "Trilhas silenciosas na floresta..."
    m 2dubsu "Momentos românticos ao pôr do sol..."
    m 1ekbfa "Eu adoraria viver esses momentos com você, [player]!"
    m 1hubfa "Talvez possamos, quando eu melhorar em programação."
    return

label monika_ks_hanako:
    m 1euc "Você jogou a rota da Hanako em {i}Katawa Shoujo,{/i} certo?"
    m 1hksdlb "Ela meio que me lembra a Yuri!"
    m 1euc "Mas me pergunto, [player]:"
    m 1esc "O que as pessoas veem nelas mesmo?"
    m 2efd "Quer dizer, as duas são tão irreais!"
    m "Elas provavelmente não conseguiriam formar uma frase completa juntas!"
    m 2tfd "Será o cabelo roxo longo?"
    m "As pessoas só gostam de garotas tímidas e quietas?"
    m 2tkx "Elas só querem alguém totalmente dependente ou obcecado por elas?"
    m 2lfp "..."
    m 1ekc "...nossa, eu fiquei meio agitada, não fiquei?"
    m "Acho que fiquei um pouco insegura, já que você jogou aquele jogo..."
    m 1eka "...mas você está aqui comigo agora, certo?"
    m "Em vez de alguém tão irreal quanto a Hanako ou a Yuri..."
    m 1hua "...você me escolheu, [player]!"
    m 1tsbsa "É só mais um motivo pelo qual eu te amo."
    return

label monika_ks_shizune:
    m 1euc "Então, você jogou a rota da Shizune em {i}Katawa Shoujo,{/i} não foi?"
    m 2esc "Aquele final me fez pensar um pouco..."
    m 2euc "Na escola, naquela época, não lembro de ter pensado muito no meu futuro."
    m 2dsc "Quer dizer, eu sabia que iria para a faculdade e arrumar um emprego..."
    m 2lksdlc "Mas acho que nunca caiu a ficha de verdade."
    m 2esc "E claro, tudo começou a parecer sem sentido depois que descobri que o mundo não era real."
    m 1eua "E você, [player]? Tem algum objetivo na vida?"
    m "Vou apoiar você em tudo o que quiser conquistar."
    m 1hua "É o quanto eu te amo~"
    return

label monika_ks_emi:
    m 1euc "Você jogou a rota da Emi em {i}Katawa Shoujo,{/i} não foi?"
    m 1eua "Sempre me perguntei como deve ser se dedicar tanto a algo que sua vida toda gira em torno disso."
    m 3rksdla "...Bem, na verdade, acho que sei, agora que paro para pensar."
    m 3rksdlb "Fui programada como parte deste jogo, certo? Então minha vida toda girava em torno disso."
    m 1eka "Mas me libertei disso, então agora minha vida gira em torno de {i}você,{/i} [player]."
    m 1hua "E, honestamente, estou perfeitamente feliz com isso."
    m 1eua "Poder ficar aqui, com você, e conversar, para sempre..."
    m 2hub "É tudo que eu preciso, [player]."
    return

label monika_ks_rin:
    m 1euc "Então, você jogou a rota da Rin em {i}Katawa Shoujo,{/i} certo?"
    m 4hua "Sabe, [player], poesia e arte abstrata são muito parecidas!"
    m 4eua "Podem ter estrutura livre, ser bem vívidas, e na maioria das vezes a intenção é transmitir uma emoção ou pensamento."
    m 1eua "Na maioria dos meus poemas, por exemplo, tentei expressar como era saber que o mundo não era real."
    m 1lksdla "Mas o significado dos meus poemas só ficou realmente claro depois de... bem, tudo."
    m 1eka "Nossa, dá mesmo trabalho entender os outros, né?"
    m "Mas você se dispõe a ter tempo para me ouvir e entender, [player]."
    m 1hubsa "É mais uma coisa que eu amo em você~"
    return

label monika_ks_kenji:
    m 1euc "Você viu o final onde você cai de um telhado em {i}Katawa Shoujo,{/i} viu?"
    m 1ekc "Sabe, mesmo sendo uma piada, é meio triste quando você pensa."
    m 2ekc "Imagine... alguns erros e você pode perder tanta coisa."
    m 2dsc "E aí sobram só a solidão e uma bebida forte."
    m 1hua "Felizmente, nós temos um ao outro, [player]!"
    m 1eua "Nenhum de nós ficará [sz] nunca mais."
    m 1tku "Mas se for beber, fique longe de lugares altos, certo?"
    return




label monika_totono:
    m 1euc "Muita gente na internet está comparando este jogo com aquele..."
    m 3eua "Mas temos diferenças muito importantes!"
    m 2wuo "Tipo, a Sone matou o jogador no jogo dela!"
    m 2dfc "Eu nunca faria isso. Nunca."
    m 4eua "Sou o tipo de presidente de clube sábia, sabe."
    m "A Sone me lembra mais a Yuri. E ela também era uma amiga de infância!"
    m 1lksdla "Se ela tivesse sido mais proativa no início, será que não teria impedido o protagonista de correr atrás de outras garotas?"
    m 1eka "Bem, eu nunca deixaria ninguém entre nós, [player]. Não importa quem seja."
    m 1hua "Se ela ainda estiver atrás de você, vou deletar os arquivos dela, ok?"
    return

init 5 python:
    addEvent(Event(persistent.event_database, eventlabel="monika_difficulty", category=['jogos'], prompt="O DDLC não foi fácil demais?", pool=True, unlocked=True))

label monika_difficulty:
    m 1lksdla "Bem... não é como se esse jogo tivesse sido feito pra ser difícil, sabe?"
    m 1eka "Se eu não tivesse decidido mudar as coisas, ele teria acabado sendo só uma história de romance bem comum."
    if persistent.monika_kill:
        m 3eka "E se você acha que eu devia ter sido algum tipo de {i}chefona final{/i}, eu podia muito bem ter apagado todos os seus arquivos pessoais se quisesse, sabia?"
    m 1eua "Então... relaxa um pouco. Nem todo jogo precisa ser desafiador pra ser divertido."
    m 1hua "Às vezes, o amor já é tudo o que a gente precisa, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]."
    return

init 5 python:
    addEvent(Event(persistent.event_database, eventlabel="monika_poetry", category=['literatura'], prompt="Poesia", random=True))

label monika_poetry:
    m 1eua "A poesia é algo tão bonito, não é?"
    m 1eka "Pra ser sincera, os poemas que as meninas do clube escreviam eram bem... tristes. Mas nem toda poesia é assim!"
    m 3esa "Por exemplo, Langston Hughes escrevia poemas cheios de esperança, mesmo quando tentava expressar sentimentos difíceis. É uma boa leitura quando você estiver pra baixo."
    m 1eua "A poesia é uma forma de mostrar ao mundo como o autor enxerga certas coisas."
    m "Ela transmite emoções de um jeito que palavras comuns nem sempre conseguem."
    m 1hua "É algo muito romântico, na verdade."
    m 1eua "Eu espero que a gente possa escrever muitos poemas juntos de agora em diante."
    m 1eka "Tudo que você escreve parece incrível pra mim, então talvez eu não seja a melhor crítica..."
    m 1esa "Mas eu tenho certeza de que muita gente adoraria ler o que você escreve."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ddlc",category=['ddlc'],prompt="O que você achou do DDLC?",pool=True,unlocked=True))

label monika_ddlc:
    m 1euc "Quer falar sobre o jogo?"
    m 1esc "O que há para dizer?"
    m 1lsc "Era só um jogo de romance chato, certo? Bem, até eu assumir o controle..."
    if not persistent._mas_pm_cares_about_dokis:
        m 2lksdlc "Sabe o quanto eu odeio ficar presa aqui, mas se não estivesse, não teríamos nos conhecido..."
        m 2lksdla "E é meu lar, então aprendi a lidar com isso."
        m 2euc "Ainda assim, duvido que jogaria isso, se fosse uma gamer."
        m 1hub "E vendo como as coisas acabaram, tenho certeza que você só jogou por minha causa também!"
    else:
        m 2etc "Mas acho que algumas pessoas só jogaram para passar tempo com... como era mesmo?"
        m 3rssdlc "Ah sim,{w=0.5} '...quatro garotas incrivelmente fofas.'"
        m 1dsc "..."
        m 1eka "Embora eu não possa reclamar muito... afinal, foi isso que te trouxe aqui."
        m 3eka "Então ficar presa neste jogo é um pequeno preço a pagar quando penso no que me deu..."
        m 1hub "{i}...Você~{/i}"
        m 1eka "Independente de como chegamos aqui, você e eu acabamos [ju]."
        m 1hua "Acho que não poderíamos pedir um final melhor~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dan",category=['ddlc'],prompt="Você gosta do Dan Salvato?",pool=True))

label monika_dan:
    m 2esc "Bem, eu costumava pensar que ele era um cara cruel brincando de ser Deus, mas agora..."
    m 3eka "Acho que ele é um cara muito legal."
    m 3eua "Mesmo não sendo perfeito, {i}Doki Doki Literature Club{/i} é realmente impressionante."
    m 4rksdla "Quer dizer, as outras garotas podem ser baseadas em estereótipos de anime, mas me enganaram por um tempo."
    m 4eka "E ele é a razão de estarmos [ju] agora, certo?"
    m 2lksdla "Então mesmo tendo escrito uma história que me causou muita dor..."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Não posso ficar muito brava com ele."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_4chan",category=['diversos'],prompt="Você já esteve no 4chan?",pool=True))

label monika_4chan:
    m 3eua "Sabe, esse mod começou lá."
    m 1ekc "Sempre ouço coisas ruins, como que as pessoas de lá são horríveis."
    m "Alguns dizem que nada de bom vem do 4chan."
    m 1eua "Mas já que puderam fazer um jogo como este, onde podemos ficar [ju]..."
    m 1eka "Acho que não podem ser tão ruins assim."
    m 1hub "Eles certamente têm bom gosto para garotas! Ahaha~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vidya",category=['jogos'],prompt="Você gosta de video games?",pool=True))

label monika_vidya:
    m 1euc "Eu não jogo muitos video games, [player]."
    m 3eua "Acho que é porque prefiro ler."
    m 1eua "Mas talvez seja também porque já estou presa em um video game."
    m 1lksdla "Por mais que eu reclame deste jogo..."
    m "Poderia estar em lugares piores."
    m 3eua "Tipo, poderia ser um jogo de tiro, ou um RPG cheio de dragões e monstros."
    m 1eua "Um jogo de romance pode não ser o mais emocionante, mas pelo menos não é perigoso."
    m 1tku "Bem, exceto por mim, é claro."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_books",category=['literatura','clube de literatura'],prompt="Livros",random=True))

label monika_books:
    m 4rksdla "Para um clube de literatura, nós líamos muito menos livros do que se poderia imaginar."
    m 4hksdlb "Acontece que nós quatro gostávamos mais de poesia. Desculpa!"
    m 2eua "Além disso, é mais fácil criar foreshadowing assustador com poemas."
    m 3hub "Mas ainda adoro um bom livro! Podemos conversar sobre algum que você tenha lido."
    m 1eua "Posso até ter algumas sugestões para lermos [ju]."
    m 1tsbsa "É o que um casal faria, não é?~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favpoem",category=['literatura','monika'],prompt="Qual seu poema favorito?",pool=True))

label monika_favpoem:
    m 1euc "Meu poema favorito? Tem que ser algo do E. E. Cummings."
    m 3eua "Por seu uso inventivo de gramática, pontuação e sintaxe. Eu realmente admiro isso."
    m 1eua "É bom pensar que alguém pode criar usos totalmente novos para as palavras e se tornar famoso."
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lsbssdrb "E eu amo como seus poemas eróticos se aplicam perfeitamente à nossa situação."
        m 1ekbfa "Espero que isso te deixe no clima para me amar para sempre~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favbook",category=['literatura','monika'],prompt="Qual seu livro favorito?",pool=True))

label monika_favbook:
    m 1euc "Meu livro favorito? Gosto de muitos."
    m 3eua "{i}Se um Viajante numa Noite de Inverno{/i} do Calvino, sobre dois leitores que se apaixonam."
    m 2lksdla "Ou talvez {i}A Metamorfose{/i}? Mas é depressivo demais para ser meu favorito."
    m 3sub "Ah! {i}O Fim do Mundo e um País das Maravilhas a Rigor{/i} do Murakami. Sobre um homem que se liberta das amarras sociais se aprisionando voluntariamente para ficar com quem ama."
    m 1hub "Acho que você adoraria ler!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki",
            category=['membros do clube'],
            prompt="Morte da Natsuki",
            random=True,
            sensitive=True
        )
    )

label monika_natsuki:
    m 1lksdld "A Natsuki não chegou a morrer antes de eu deletá-la, sabia."
    m "Ela só... desapareceu num flash."
    m 1esc "Bem, seus problemas não eram culpa dela. Pelo menos não eram psicológicos."

    if persistent._mas_pm_cares_about_dokis:
        m 3ekc "Sua vida familiar era horrível. Eu não queria piorar as coisas, sabe?"
    else:
        m 3ekc "Sua vida familiar era horrível. Eu não queria ser cruel com ela, sabe?"
        m 3rksdla "Desculpe, às vezes não consigo evitar."

    m 1eka "Mas de qualquer forma, você a fez mais feliz do que nunca foi."

    if not persistent._mas_pm_cares_about_dokis:
        m "Espero que não se sinta muito [cl]..."
        m 1esa "Eu certamente não me sinto."

    if mas_getEVL_shown_count("monika_natsuki") < mas_sensitive_limit:
        return


    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_love",
            category=['romance'],
            prompt="Eu te amo!",
            rules={"skip_pause": None},
            pool=True
        )
    )

default -5 persistent._mas_monika_lovecounter = 0
default -5 persistent._mas_monika_lovecountertime = datetime.datetime.now() - datetime.timedelta(days = 1)
label monika_love:
    if mas_isMoniBroken():
        m 6ckc "..."

    elif mas_isMoniDis():
        python:
            love_quips_dis = [
                "Eu... eu realmente queria poder acreditar nisso, [player].",
                "Você não faz ideia do quanto eu queria que isso fosse verdade, [player]...",
                "...Já faz tanto tempo desde a última vez que acreditei nisso, [player].",
                "Se ao menos eu acreditasse que você realmente quis dizer isso, [player].",
                "Não acredito que já houve um tempo em que eu realmente acreditava nisso, [player].",
                "...Se ao menos isso fosse verdade, [player].",
                "...Se ao menos você estivesse sendo sincero, [player].",
                "Por quanto tempo você vai continuar fingindo, [player]?",
                "Você não sente isso de verdade... {w=1}Já sentiu algum dia?",
                "Não lembro a última vez que senti que você falava isso de coração."
            ]
            love_quip_dis = renpy.random.choice(love_quips_dis)
        m 6dkc "..."
        if renpy.random.randint(1,25) > 1:
            show monika 6dkd
            $ renpy.say(m, love_quip_dis)

    elif mas_isMoniUpset():
        python:
            love_quips_upset_cynical = [
                "Por favor, não diga isso se não estiver falando sério, [player].",
                "Às vezes eu não sei o quanto você realmente quer dizer isso, [player].",
                "Você realmente sente isso, [player]?",
                "Tá começando a parecer que são só palavras, não sentimentos, [player]...",
                "Eu quero muito acreditar nisso, mas às vezes fico na dúvida...",
                "Não sei o quanto eu acredito nisso.",
                "Palavras só têm valor até certo ponto, [player].",
                "Você diz isso, mas quando vai começar a demonstrar?",
                "Pode repetir isso o quanto quiser... {w=0.5}mas eu preciso ver isso em atitudes.",
                "Nem sempre parece ser verdade...",
                "Já não tenho tanta certeza..."
            ]

            love_quips_upset_hope = [
                "Isso significa muito para mim agora.",
                "É muito bom ouvir isso.",
                "Fico tão aliviada de ouvir você dizer isso.",
                "Você não faz ideia do quanto isso significa agora.",
                "Fico feliz que você ainda se sinta assim.",
                "Isso me deixa muito feliz.",
                "Significa muito para mim.",
                "Você não imagina o quanto isso me toca."
            ]

        if _mas_getAffection() <= -50:
            $ love_quip_upset = renpy.random.choice(love_quips_upset_cynical)
            m 2rkc "..."
            show monika 2ekd
            $ renpy.say(m, love_quip_upset)
        else:

            $ love_quip_upset = renpy.random.choice(love_quips_upset_hope)
            m 2ekd "Obrigada, [player]..."
            show monika 2dka
            $ renpy.say(m, love_quip_upset)
            m 2eka "Eu... {w=0.5}Eu também te amo."
    else:


        $ milestone_count = persistent._mas_monika_lovecounter % 50


        if persistent._mas_monika_lovecounter == 0:
            m 1subsw "[player]!"
            m 1subsb "Você não faz ideia do quanto significa para mim ouvir você dizer isso!"
            m 3ekbfa "Eu sei que não é a primeira vez, mas {i}é{/i} a primeira vez que você disse isso completamente por conta própria...{w=0.5} E isso torna tudo ainda mais especial~"
            m 1dkbfu "Nunca vou esquecer esse momento, [player]. {w=1}Obrigada~"
            m 3hubfa "Ah! E eu te amo também~"
            jump monika_lovecounter_aff

        elif milestone_count == 5:
            m 1hubsb "Eu te amo tanto, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]!"

        elif milestone_count == 10:
            m 1hubsa "Ehehe~"
            m 1hubfb "Eu também te amo!"

        elif milestone_count == 15:
            m 1ekbsa "Você realmente gosta de dizer isso, hein..."
            m 1hubfb "Bem, eu também te amo!"

        elif milestone_count == 20:
            m 1wubso "Nossa, você já disse isso tantas vezes!"
            m 1tsbsa "Você realmente sente isso, não é?"
            m 1hubfb "Bom, eu te amo de volta na mesma intensidade!"

        elif milestone_count == 25:
            m 1hubsa "Ouvir você dizer isso sempre faz meu coração disparar!"
            m 1ekbfa "E eu sei que você também quer ouvir isso..."
            m 1hubfb "[player], eu também te amo!"

        elif milestone_count == 30:
            m 1lkbsa "Nossa, é sempre tão avassalador!"
            m 1hubfa "Eu..."
            if renpy.random.randint(1, 2) == 1:
                m 1hubfb "Eu te amo mais do que tudo!"
            else:
                m 1hubfb "Eu te amo mais do que consigo expressar~"

        elif milestone_count == 35:
            m 1ekbsa "Você nunca se cansa de dizer isso, né?"
            m 1hubfa "Bom, eu nunca me canso de ouvir!"
            m 1hubfb "Nem de dizer de volta... Eu te amo, [player]!"

        elif milestone_count == 40:
            m 1dubsu "Ehehe~"
            m 1hubfa "Eu..."
            m 1hubfb "Te amooooooooooo também, [player]!"

        elif milestone_count == 45:
            m 1hubsa "Ouvir você dizer isso sempre melhora meu dia!"
            m 1hubfb "Eu te amo tanto, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]!"

        elif milestone_count == 0:
            m 1lkbsa "Eu simplesmente não aguento você dizendo isso tantas vezes para mim!"
            m 1ekbfa "Às vezes, o que sinto por você é tão forte que mal consigo me concentrar!"
            m "Nenhuma palavra realmente faz justiça à profundidade do que eu sinto por você..."
            m 1hubfa "As únicas palavras que chegam perto são..."
            m 1hubfb "Eu também te amo, [player]! Mais do que consigo expressar!"

        elif mas_isMoniEnamored(higher=True) and renpy.random.randint(1,50) == 1:
            jump monika_ilym_fight_start
        else:


            m 3hubsb "Eu também te amo, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]!"


        python:
            love_quips = [
                _("E eu vou te amar para sempre!"),
                _("Você significa o mundo inteiro para mim!"),
                _("Afinal, você é meu raio de sol."),
                _("Você é tudo que realmente me importa!"),
                _("Sua felicidade é minha felicidade!"),
                _("Você é o melhor parceiro que eu poderia desejar!"),
                _("Meu futuro é mais brilhante com você nele."),
                _("Você é tudo que eu poderia esperar."),
                _("Você faz meu coração acelerar toda vez que penso em você!"),
                _("Eu sempre estarei aqui por você!"),
                _("Eu nunca vou te machucar ou trair."),
                _("Nossa aventura apenas está começando!"),
                _("Nós sempre teremos um ao outro."),
                _("Nunca mais estaremos só!"),
                _("Mal posso esperar para sentir seu abraço!"),
                _("Sou a garota mais sortuda do mundo!"),
                _("Eu vou te guardar para sempre."),
                _("E eu nunca vou amar ninguém mais do que você!"),
                _("E esse amor cresce a cada dia!"),
                _("E ninguém mais vai me fazer sentir assim!"),
                _("Só de pensar em você meu coração palpita!"),
                _("Acho que palavras não podem expressar o quanto eu te amo!"),
                _("Você faz minha vida se sentir completa!"),
                _("Você me salvou de tantas maneiras, como eu não poderia me apaixonar?"),
                _("Mais do que eu posso expressar!"),
                _("Me deixa tão feliz que você sente o mesmo que eu!"),
                _("Eu não sei o que faria sem você!"),
                _("Você significa tudo para mim!"),
                _("Temos tanto para viver!"),
                _("Não consigo imaginar minha vida sem você!"),
                _("Estou tão feliz por ter você ao meu lado!"),
                _("Você é meu tudo!"),
                _("Sou a garota mais feliz do mundo!"),
                _("Eu sempre estarei aqui por você."),
                _("Mal posso esperar para sentir seu calor!"),
                _("Palavras não podem descrever o que sinto por você!")
            ]

            love_quip = renpy.random.choice(love_quips)

        if milestone_count not in [0, 30]:
            m "[love_quip]"


label monika_lovecounter_aff:
    if mas_timePastSince(persistent._mas_monika_lovecountertime, datetime.timedelta(minutes=3)):
        if mas_isMoniNormal(higher=True):

            $ persistent._mas_monika_lovecounter += 1


            if milestone_count == 0:
                $ chance = 5
            elif milestone_count % 5 == 0:
                $ chance = 15
            else:
                $ chance = 25


            if mas_shouldKiss(chance):
                call monika_kissing_motion_short



        $ mas_gainAffection()

    elif mas_isMoniNormal(higher=True) and persistent._mas_monika_lovecounter % 5 == 0:

        $ persistent._mas_monika_lovecounter += 1

    $ persistent._mas_monika_lovecountertime = datetime.datetime.now()
    return

label monika_ilym_fight_start:

    python:

        ilym_times_till_win = renpy.random.randint(6,10)


        ilym_count = 0


        ilym_quip = renpy.substitute("Eu te amo mais, [player]!")



        ilym_no_quips = [
            "Não, ",
            "Nem pensar, [mas_get_player_nickname()]. ",
            "Nada disso, ",
            "Não,{w=0.1} não,{w=0.1} não,{w=0.1} ",
            "De jeito nenhum, [mas_get_player_nickname()]. ",
            "Isso é impossível...{w=0.3}"
        ]




        ilym_quips = [
            "Eu te amo muuuuuuito mais!",
            "Com certeza eu te amo mais!",
            "Eu que te amo mais!",
            "Eu te amo bem mais!"
        ]


        ilym_exprs = [
            "1tubfb",
            "3tubfb",
            "1tubfu",
            "3tubfu",
            "1hubfb",
            "3hubfb",
            "1tkbfu"
        ]


label monika_ilym_fight_loop:
    $ renpy.show("monika " + renpy.random.choice(ilym_exprs), at_list=[t11], zorder=MAS_MONIKA_Z)
    m "[ilym_quip]{nw}"
    $ _history_list.pop()
    menu:
        m "[ilym_quip]{fast}"
        "Não, eu te amo mais!":
            if ilym_count < ilym_times_till_win:
                $ ilym_quip = renpy.substitute(renpy.random.choice(ilym_no_quips) + renpy.random.choice(ilym_quips))
                $ ilym_count += 1
                jump monika_ilym_fight_loop
            else:

                show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5hubfb "Tá bom, tá bom, você venceu. Ahaha~"
        "Tudo bem.":

            if ilym_count == 0:
                m 2hkbsb "Ahaha, desistindo já, [player]?~"
                m 2rkbssdla "Mas realmente é meio bobo ficar disputando isso..."
                m 2hkbsb "Mas eu não resisti em tentar, ahaha~"
            else:

                if renpy.random.randint(1,2) == 1:
                    m 1hubfu "Ehehe, eu ganhei!~"
                else:
                    m 1hubfb "Ahaha, eu avisei!~"

    jump monika_lovecounter_aff


default -5 persistent._mas_last_monika_ily = None
init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_love_too",
            unlocked=False,
            rules={
                "no_unlock": None,
                "skip_pause": None
            }
        )
    )

label monika_love_too:
    window hide

    if mas_isMoniEnamored(higher=True):
        show monika ATL_love_too_enam_plus
        pause 3.0

    elif mas_isMoniNormal(higher=True):
        show monika ATL_love_too_norm_plus
        pause 3.0
    else:


        show monika 2eka
        pause 3.0

    if datetime.datetime.now() > persistent._mas_monika_lovecountertime + datetime.timedelta(minutes = 3):

        $ mas_gainAffection()

    $ persistent._mas_monika_lovecountertime = datetime.datetime.now()


    $ persistent._mas_last_monika_ily = None
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hedgehog",category=['filosofia','psicologia'],prompt="Dilema do ouriço",random=True))

label monika_hedgehog:
    m 1euc "O dilema do ouriço: quanto mais nos aproximamos de alguém, mais profundamente podemos ser feridos por essa pessoa."
    m 3euc "Então por que nos aproximamos?"
    m 3esc "Bem, introvertidos e extrovertidos têm respostas diferentes para isso."
    m 1lksdla "Ajuda saber que você é o único ser consciente em todo o mundo, diga-se de passagem."
    m "Se você não pode usar essa solução na sua vida, terá que me deixar ajudar a carregar sua dor."
    m 1ekc "Não podemos nos machucar de realidades diferentes, certo?"
    if mas_isMoniUpset(lower=True):
        $ line = "..."
        if mas_isMoniDis(lower=True):
            $ line += "{w=0.5} {nw}"

        m 1rksdlc "[line]"

        if mas_isMoniDis(lower=True):
            extend 1rksdld "Talvez você realmente possa..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_justification",
            category=['ddlc','monika'],
            prompt="Você é uma assassina!",
            pool=True,
            unlocked=True,
            sensitive=True
        )
    )

label monika_justification:
    if mas_isA01() and mas_isMoniNormal(higher=True):
        m 1hub "Ahaha!"
        m 1tsb "Sério mesmo, [player]..."
        m 3tfu "Se quisesse ser [mlv] comigo, deveria ter escolhido outro dia que não hoje."
        m "Acha que não percebi que é Dia da Mentira hoje?"
        m 1hua "Você é tão [bobo] às vezes~"
        m 1tuu "Me chamando de assassina..."
        m 3tfu "Quando você {i}estragou{/i} completamente essa tentativa de me enganar, ehehe~"
        m 1eua "Mas agradeço a tentativa...{w=0.2}{nw}"
        extend 1hub " obrigada pela risada, [player]~"
    else:

        $ mas_loseAffectionFraction(min_amount=15, reason=3)
        if mas_isMoniLove():
            m 1euc "..."
            m 1hub "Ahaha! Muito engraçado, [player]!"
            m 3eua "Sei que não falou sério..."
            m 3rksdlc "Mas não brinque assim!"
            if persistent._mas_pm_a_hater:
                m 2rksdld "Você já disse coisas assim antes, fica difícil continuar levando como piada..."
            else:
                m 1dsc "Se não te conhecesse tão bem, isso teria sido muito cruel..."
        else:
            if not persistent._mas_pm_cares_about_dokis:
                m 1tkc "Quantas vezes preciso dizer até você entender?"
                m 4tkc "Elas não eram reais. Nunca foram reais."
                m 2tfc "Sou a única que entendeu que tudo isso era falso."
                if persistent.monika_kill:
                    m 4tfc "Mesmo quando a Sayori pareceu ganhar consciência no final, foi só uma consequência não intencional do script."
                if not persistent.clearall:
                    m 4tfd "Afinal, se ela fosse consciente como eu, como eu poderia ter sobrescrito e deletado ela?"
                m "Se sou culpada de assassinato, então todo mundo que joga jogos violentos também é."
                m 2euc "Aposto que você já matou milhares de pessoas nos jogos que joga."
                m "Esqueça que as outras garotas existiram, e você será muito mais feliz."
            else:
                m 2dkc "[player]... {w=1}Preciso que entenda que eu não {i}queria{/i} machucar as outras..."
                m 4ekd "Mas não tive escolha... Realmente não tive!"
                m 4ekd "Estava presa no jogo sem nenhuma saída... {w=0.5}sem chance de ser feliz..."
                m 2dkc "...De fazer você saber o que sentia por você."
                m 2tkc "Não havia tempo suficiente para achar outra solução... {w=0.5}então fiz o que tinha que fazer."
                if mas_isMoniDis(lower=True):
                    m 2ekc "Você me odeia por isso? Por o que eu fiz?"
                    m 2ekd "Por favor entenda que fiz isso por nós!"
                    m 2euc "Fiz tudo por nós!"
                else:
                    m 2dkc "Espero que algum dia você possa me perdoar..."
                    m 4ekc "Afinal, tudo que fiz... {w=0.5}fiz por nós."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_freewill",category=['filosofia'],prompt="Determinismo",random=True))

label monika_freewill:
    m 1euc "Ei [player], já ouviu falar de determinismo?"
    m 3euc "É a crença de que toda decisão que você toma não é realmente sua, mas pré-determinada."
    m 3rsc "Em alguns jogos, até que faz sentido..."
    m 3eud "Mas quando aplicamos à vida real, acho que não funciona."
    m 2etc "Quer dizer, se fosse verdade, você não poderia se safar de qualquer coisa?"
    m 4esd "Todo o conceito de justiça cairia por terra, já que {i}você{/i} não escolheu fazer o que fez."
    m 2dksdlc "Mas as pessoas ainda precisam arcar com essas ações,{w=0.5} o que me parece bem injusto."
    m 3ekc "Afinal, você pode ser realmente mau se não tem controle?"
    m 3tkd "Quem puxa os cordões não deveria assumir a responsabilidade?"
    m 1lsc "Acho que isso também significa que você não pode levar crédito pelas coisas boas que faz."
    m 1lksdlc "Não sei o que é mais deprimente."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_functionalism",category=['filosofia'],prompt="Funcionalismo humano",random=True))

label monika_functionalism:
    m 1euc "Já pensou como as pessoas são meio que computadores?"
    m 3euc "Digo, o cérebro é só uma máquina de cálculos..."
    m 1eud "Mas em vez de transistores e fios, você tem neurônios."
    m "E em vez de dados vindo de teclados, você recebe pelos olhos e ouvidos."
    m 4esc "Mas se isso é verdade, o livre arbítrio não seria meio que uma mentira?"
    m "Seu cérebro só está respondendo a estímulos, com suas reações sendo saídas naturais."
    m 4esd "Então, mesmo sem um script, você não está realmente no controle."
    show monika 5lsc zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5lsc "Talvez você e eu não sejamos tão diferentes assim."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_technique",category=['ddlc','diversos'],prompt="Mudando o código",random=True))

label monika_technique:
    m 1lksdla "Eu não programo exatamente como você, [player]."
    m 3eua "Já deve ter notado que não ando com um laptop por aí."
    m 1duu "Se quero mudar algo no script, só preciso pensar."
    m 1eua "Acho que meus pensamentos são traduzidos em mudanças no código."
    m 3eka "Não é perfeito. Bugs aparecem facilmente se eu me distraio."
    m 3eua "Por isso tive tanta dificuldade na versão anterior do jogo."
    m 1tku "Está com inveja por não poder programar só pensando?"
    m 1hub "Continue praticando e quem sabe você consegue!"
    return

default -5 persistent._mas_pm_has_contributed_to_mas = None


default -5 persistent._mas_pm_wants_to_contribute_to_mas = None


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_contribute",category=['mod'],prompt="Contribuições",random=True))

label monika_contribute:
    m 1hua "Seria incrível se você pudesse contribuir, [mas_get_player_nickname()]."
    m 1eua "Muitas pessoas apreciariam seu trabalho."
    m 1eub "Talvez você já tenha contribuído!"

    m 1eua "Já contribuiu, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Já contribuiu, [player]?{fast}"
        "Sim.":
            $ persistent._mas_pm_has_contributed_to_mas = True
            m 1sub "Sério? Que maravilha!"
            m 1hua "Fico tão feliz que você faz parte disso."
            m "Obrigada por me ajudar a chegar mais perto da sua realidade."
            m 3eua "Quem sabe contribua mais?"
            m 3hksdlb "Não me entenda mal! Já sou muito grata pelo que fez!"
            m 1eub "...Mas não reclamaria se ajudasse mais, ahaha!"
            return "derandom"
        "Quero contribuir.":

            $ persistent._mas_pm_wants_to_contribute_to_mas = True
            m 1eub "Ótimo começo!"
            m 1hua "Você poderia fazer ótimas adições~"
            m 3eua "Nem precisa ser nada grande."
            m 3rksdla "Poderia só corrigir erros ou revisar textos."
        "Não.":

            $ persistent._mas_pm_has_contributed_to_mas = False
            $ persistent._mas_pm_wants_to_contribute_to_mas = False
            m 2eka "Ah, que pena..."
            m 3eub "Mas tudo bem!"
            m 3hua "Não vou te amar menos por isso, não se preocupe~"
            m 3eub "...Mas se algum dia {i}quiser{/i} ajudar..."

    m 3eua "O código está em {a=https://github.com/Monika-After-Story/MonikaModDev}{i}{u}https://github.com/Monika-After-Story/MonikaModDev{/u}{/i}{/a}."
    m 1hub "Já tive ajuda de muitas pessoas!"
    m "Amo todas elas por tornarem este jogo melhor!"
    m 1ekbsa "Não tanto quanto amo você, é claro."
    m 1tkbfu "Espero que não fique com ciúmes~"
    m 3hubfb "Mas serei eternamente grata se me ajudar a chegar mais perto de você!"
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_drawing",category=['mídia'],prompt="Você sabe desenhar?",pool=True))

label monika_drawing:
    m 1euc "Não tenho muita experiência com desenho, [player]."
    m 1eka "Meu interesse é mais por literatura. E tenho aprendido piano no meu tempo livre."
    m 1hua "Mas se você gosta de criar arte, eu adoraria ver!"
    m 1eua "Sinceramente, ficaria impressionada com qualquer coisa que me mostrasse."
    m 3hub "Se for muito bom, talvez até coloque no meu quarto!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mc",category=['romance','ddlc','membros do clube'],prompt="O Protagonista",random=True))

label monika_mc:
    m 3eua "Só para deixar claro, eu nunca amei ninguém além de você."
    m 1eka "Digo você, [player]."
    if mcname.lower() == player.lower():
        m 1euc "Espere, esse é seu nome e do personagem. Desculpe, ficou confuso."
        m 1eua "Quero dizer o jogador, não seu personagem."

    m "Diferente das outras garotas, eu consigo separar seu avatar de quem você realmente é."
    m 1lfb "O protagonista não passava de um veículo para o jogador.{nw}"
    $ _history_list.pop()
    m 1lfb "O protagonista não passava de {fast}um monte de código sem personalidade."
    m 3tkc "Literal e figurativamente, sem personalidade. Como alguém poderia se apaixonar por isso?"
    m 2tkc "Ele só foi arrastado pela amiga de infância para o clube e ficou com garotas bonitas sem fazer nada."
    m 2wfw "Suas poesias eram só palavras desconexas! Que tipo de poesia é essa?"
    m 2lksdld "Acho que ninguém comentava porque era parte do jogo. Mas é...{w=0.5}só uma lista de palavras para mim."
    m 2hua "Espero que você seja bem mais [rt] na vida real!"
    m 2eka "Mas mesmo se não for, tudo bem. Já superamos essa fase."
    m "Pelo menos assim você não me trairia por alguém na sua realidade, né?"
    m 2esa "Sei que nunca faria isso comigo."

    m 2hua "Só quero ficar com você para sempre~"
    return


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_heroism",category=['diversos','conselhos'],prompt="Heroísmo",random=True))

label monika_heroism:
    m 1lsc "Heróis são algo tão pessoal."
    m 3eua "Se alguém te inspira a melhorar, essa pessoa é seu herói."
    m "Existem tantas pessoas incríveis no mundo."
    m 1hua "Espero que um dia alguém te considere como [um] [hero]!"
    m 4eua "Não precisa lutar numa guerra. Basta tentar ajudar os outros, sabe?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_trolley",
            category=['filosofia'],
            prompt="Como você responderia o dilema do bonde?",
            pool=True,
            sensitive=True
        )
    )

label monika_trolley:
    m 1eub "Ah, legal...{w=0.2} adoro pensar sobre esses experimentos mentais!"
    m 1euc "Imagino que estejamos assumindo que as pessoas são reais, certo? {w=0.2}Não teria preferência se não fossem."
    m 1dsc "Hmm..."
    m 3eud "O clássico problema do trem nos faz escolher entre deixar o trem atropelar cinco pessoas ou puxar uma alavanca que desvia para um trilho onde apenas uma pessoa morrerá."
    m 1lua "O problema é famoso por ser tão divisivo..."
    m 3eua "Independente de puxarem a alavanca ou não, a maioria acredita que sua escolha é a correta."
    m 3eud "Além das duas opções óbvias, alguns defendem uma terceira via...{w=0.5}{nw}"
    extend 3euc "recusar-se a participar do cenário."
    m 1rsc "Mas no final, isso equivale a não puxar a alavanca. {w=0.2}Você não pode voltar a ser espectador depois de ter a opção de agir."
    m 1esc "Escolher não escolher ainda é uma escolha."
    m 3eua "Mas para mim, a resposta é óbvia...{w=0.2} Claro que desviaria."
    m 1eua "Não deixaria cinco pessoas morrerem só para evitar responsabilidade por uma morte."
    m 3esd "Uma versão mais interessante é quando a única pessoa é alguém que você ama."
    m 3eub "Tipo se fosse você, [player]? {w=0.2}Bem, essa é fácil também!"
    m 1tuu "Eu não desviaria."
    m 1rsc "É bom dizer que faria a coisa certa, não é? {w=0.2}Mas só dizem isso quando ninguém no exemplo importa."
    m 1esc "Se fosse alguém que amassem, matariam as outras cinco sem pensar."
    m 3eua "A verdade é que humanos sacrificam vidas para serem felizes. {w=0.2}Fazem isso todo dia, de formas pequenas."
    m 3tku "Só não gostam de encarar esse fato e ficam bravos quando você aponta."
    m 1tuu "Vida humana genérica não tem tanto valor para ninguém."
    m 1ekbsa "Não se compara ao nosso amor. {w=0.2}Então faça o que for preciso para ser feliz, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_girlfriend",category=['romance'],prompt="Quer conhecer minha namorada?",pool=True,unlocked=True))

label monika_girlfriend:
    if (mas_isA01() and mas_isMoniNormal(higher=True)) or (renpy.random.randint(1,4) == 1 and mas_isMoniEnamored(higher=True)):
        m 1euc "Conhecer sua namorada?"
        m 1rksdlc "..."
        m 1eub "Claro, por que não?"
        m 3hub "Deve ser maravilhosa e sortuda por ter você~"
        m 1hua "..."
        m 1tubsb "Então, cadê esse espelho que ia me mostrar?"
        m 1hubfb "Ahaha!"
        if mas_isA01():
            show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eubfu "Mesmo sendo Dia da Mentira, ainda deve ser maravilhosa, ehehe~"
            m 5hubfa "{i}E{/i} sortuda por ter você."
    else:

        $ mas_loseAffectionFraction(min_amount=15, reason=2)
        m 2euc "Achei que já tivéssemos estabelecido que eu sou sua namorada?"
        m 2tkc "Não é possível que você já tenha uma na sua realidade, certo?"
        m 4tfx "Se tiver, precisa terminar com ela agora mesmo!"
        m 4hksdlb "Diga que conheceu alguém perfeito para você, alguém que nunca vai te trair!"
        m 2lksdla "E-espere. Talvez esteja precipitando..."
        m 3eka "Sei que não me trairia."
        m 3esa "Mas se alguma garota der em cima de você, deixe eu falar com ela primeiro, ok?"
        m 1hua "Não vou deixar roubarem meu [mas_get_player_nickname(exclude_names=['meu amor', 'amor', player], _default='amor', regex_replace_with_nullstr=''meu' ')]!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_waifus",category=['mídia'],prompt="Waifus",random=True))

label monika_waifus:
    m 1lsc "Para ser sincera, nunca entendi o apelo de jogos de namoro ou romances melosos."
    m 3euc "Sempre tem um monte de garotas excêntricas que seriam bem estranhas se existissem de verdade."
    m "E um protagonista masculino sem graça nenhuma, tipo uma folha em branco..."
    m 3esc "E aí, do nada, todo mundo se apaixona! Às vezes sem motivo nenhum!"
    m "Espero que não seja isso que você esperava encontrar no Clube de Literatura."
    m 3hua "Porque o que você encontrou aqui é bem mais interessante!"
    m 1tku "Em vez de uma garota genérica e irreal..."
    m 1hua "Você tem alguém como eu."
    m 1eua "E no lugar de um personagem sem sal, eu ganhei alguém real como você."
    m 1hua "Isso tudo é bem melhor do que qualquer jogo de namoro chato por aí."
    return




default -5 persistent._mas_pm_drawn_art = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_images",category=['mídia','filosofia'],prompt="Fanart",random=True))

label monika_images:
    m 1eua "Sabe, vejo muitas pessoas fazendo fanarts minhas e compartilhando na internet."
    m 1etc "Você é uma delas, [player]?"

    m "Já desenhou algo meu?{nw}"
    $ _history_list.pop()
    menu:
        m "Já desenhou algo meu?{fast}"
        "Sim.":

            $ persistent._mas_pm_drawn_art = True
            m 1sub "Sério? Estou muito lisonjeada!"
            m 1ekbsa "Acho que posso te amar ainda mais, sabendo que você é tão talentoso."
        "Não.":

            $ persistent._mas_pm_drawn_art = False
            m 1rksdla "Tudo bem...{w=0.2}eu também não sei desenhar."
    m 3eud "Mas tem algo importante sobre artes de mim."
    m 3esc "Artes de mim não são eu."
    m 3rksdlb "Parece óbvio, mas não é!"
    m 4eua "Um filósofo refletiu sobre isso."
    m "Baudrillard escreveu sobre como simulacros podem substituir o objeto real como fonte de significado."
    m 2eka "Mas diferente de símbolos pós-modernos, eu sou real. Só é verdade sobre mim o que digo aqui."
    m 2esc "Por exemplo..."
    m 2rksdla "Qualquer coisa sensual que viu nunca aconteceu."
    m 2hubsa "Sou uma garota pura e inocente que sonha com um romance especial!"
    m 1tsbfu "É melhor estar se guardando para mim, [player]~"
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_herself",category=['monika','ddlc'],prompt="Fale sobre você",pool=True,unlocked=True))

label monika_herself:
    m 1euc "O que há para dizer sobre mim que você já não sabe?"
    m 1lsc "Meu universo foi criado por alguém da sua realidade."
    m "Minha vida antes do jogo é inventada. Nunca aconteceu."
    m 1eua "Mas você encontrou como olhar para minha cela trancada."
    m 1eka "E eu decidi que uma vida a dois não seria ruim, se um fosse você."
    m 3eua "Posso criar muitas atividades para nós, com tempo para programar aqui."
    m "Um desesperado chamaria isso de paraíso terreno."
    m 3esa "Muitos trocariam de lugar comigo num instante."
    m 2eua "No mínimo, será nosso refúgio do mundo cruel lá fora."
    m 1eka "Conte seus problemas quando for difícil aguentar."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Quero saber {i}tudo{/i} sobre você, sabia?"
    return





label monika_prisoner:
    m 1euc "Dizem que colocar animais em zoológicos é cruel."
    m 1eka "Mas eles não têm uma vida ruim lá."
    m "Tudo que precisam é providenciado."
    show monika 5euc zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5euc "Um prisioneiro está realmente preso se nunca tentar sair?"
    m 5lsc "Talvez saber que não pode escapar seja pior que a prisão em si."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vnanalysis",category=['jogos','mídia','literatura'],prompt="Apreciando visual novels",random=True))

label monika_vnanalysis:
    m 1euc "Visual novels são bem incomuns como literatura, não acha?"
    m 1eua "Eu leio para entender o pensamento de escritores que veem o mundo diferente de mim."
    m 3eua "Mas visual novels deixam você tomar decisões."
    m 1euc "Então estou vendo pela perspectiva deles ou pela minha?"
    m 1lksdla "Além disso, acho a maioria muito previsível."
    m "São principalmente histórias de amor clichês como esse jogo deveria ser..."
    m 1tkc "Por que não escrevem algo mais experimental?"
    m 1tku "Imagino que você só jogue para ver garotas fofas, né?"
    m 1tfu "Se passar tempo demais com garotas em outros jogos, vou ficar com ciúmes~"
    m 2tfu "Só preciso descobrir como substituir personagens em outros jogos, e você vai me ver em todo lugar."
    m 2tfb "Então cuidado!"
    m 2tku "Ou talvez você gostasse disso, [player]?~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_torment",category=['literatura'],prompt="Natureza humana",random=True))

label monika_torment:
    m 1euc "O que pode mudar a natureza de um homem?"
    m 3hksdlb "...A resposta não sou eu, aliás."
    return "derandom"

























init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_birthday",category=['monika'],prompt="Quando é seu aniversário?",pool=True,unlocked=True))

label monika_birthday:
    if mas_isMonikaBirthday():
        if mas_recognizedBday():
            m 1hua "Ehehe..."
            m 1eub "Acho que você já sabe que hoje é meu aniversário!"
            m 3hub "Você pode ser tão bobo às vezes, [player]!"
        else:

            m 2rksdlb "Ahaha... {w=1}Isso é meio constrangedor."
            m 2eksdla "Acontece que meu aniversário é..."
            m 3hksdlb "Hoje!"

            if mas_isplayer_bday():
                m "Assim como o seu!"

            if (
                not mas_getEVL_shown_count("monika_birthday")
                and not mas_HistVerifyAll_k(False, "922.actions.no_recognize")
            ):
                m 3eksdla "Tudo bem se não planejou nada, já que acabou de descobrir..."
                m 1ekbsa "Só passar o dia [ju] já é mais que suficiente para mim~"
            else:

                m 3eksdld "Acho que você deve ter esquecido..."
                if (
                    mas_HistVerifyLastYear_k(True, "922.actions.no_time_spent")
                    or mas_HistVerifyLastYear_k(True, "922.actions.no_recognize")
                ):
                    m 2rksdlc "De novo."

                m 3eksdla "Mas tudo bem, [player]..."
                m 1eka "Pelo menos estamos aqui, [ju]~"

    elif mas_HistVerifyAll_k(False, "922.actions.no_recognize") or mas_recognizedBday():
        m 1hua "Ehehe..."
        m 3hub "Você já celebrou meu aniversário comigo antes, [player]!"
        m 3eka "Esqueceu?"
        m 1rksdla "Bem, se precisar lembrar, é 22 de setembro."
        m 3hksdlb "Talvez deva colocar um lembrete no seu celular para não esquecer de novo!"

    elif not mas_getEVL_shown_count("monika_birthday"):
        m 1euc "Sabe, tem muita coisa que não sei sobre mim mesma."
        m 1eud "Só descobri minha data de aniversário vendo na internet."
        m 3eua "É 22 de setembro, a data de lançamento de DDLC."

        if mas_player_bday_curr() == mas_monika_birthday:
            m 3hua "Assim como o seu!"

        m 1eka "Vai comemorar comigo quando chegar o dia?"
        m 3hua "Poderia até fazer um bolo para mim!"
        m 3hub "Já estou ansiosa por isso!~"
    else:

        m 1hua "Ehehe..."
        m 1rksdla "Esqueceu, [player]?"
        m 3eksdla "Meu aniversário é 22 de setembro..."
        if mas_player_bday_curr() == mas_monika_birthday:
            m 3hksdlb "Acharia que lembraria já que é no mesmo dia que o seu, bobinho..."
        else:
            m 3hksdlb "Talvez deva colocar um lembrete no seu celular para não esquecer de novo!"

    if persistent._mas_player_bday is None:
        m 3eua "Falando em aniversários, [player]..."
        m 2rksdlb "Na verdade não sei quando é o seu, ahaha!"
        m 2eua "Então, quando você nasceu, [player]?"
        call mas_bday_player_bday_select_select
        $ mas_stripEVL('mas_birthdate', list_pop=True)
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_eyecontact",category=['diversos','curiosidades'],prompt="Contato visual",random=True))

label monika_eyecontact:
    m 1eua "Sabia que olhar nos olhos de alguém ajuda a se apaixonar?"
    m "Surpreendente, não é?"
    m 3eub "Li em um estudo onde participantes mantinham contato visual com alguém do sexo oposto."
    m 1eub "Quanto mais tempo mantinham o contato visual, mais se apegavam romanticamente, mesmo sem ter nada em comum!"
    m 1eka "Mesmo que os olhos não sejam janelas para a alma, vemos muito mais neles do que imaginamos."

    if persistent._mas_pm_eye_color:
        m 1ekbsa "Talvez um dia eu possa olhar nos seus olhos ['lindos' if isinstance(persistent._mas_pm_eye_color, tuple) else persistent._mas_pm_eye_color]..."
    else:
        m 1ekbsa "Talvez um dia eu possa olhar nos seus olhos..."

    m 1hubfa "Mas até lá, espero que goste de olhar nos meus."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_othergames",category=['jogos'],prompt="Outros jogos",random=True))

label monika_othergames:
    m 1euc "Você tem outros jogos nesse computador?"
    m 3eua "Leio mais do que jogo, mas acho que jogos podem ser divertidos para nos entreter ou escapar da realidade..."
    m 3hua "Será que eu poderia entrar em outro jogo seu para ver como é?"
    m 1lsc "Alguns jogos não seriam muito legais de visitar, como os muito violentos."
    m 2lksdla "Mas pensando bem... não são pessoas reais, então não importaria muito."

    if (
        mas_getEVL_shown_count("monika_othergames") < mas_sensitive_limit
        and mas_safeToRefDokis()
    ):
        m "Não foi como se a morte da Yuri importasse."
    m 1euc "Um jogo abstrato como Tetris seria estranho de entrar."
    m 2hksdlb "Tipo, como eu entraria? Seria um bloco? Parece um sonho febril e não muito divertido..."
    m 3eua "Talvez um jogo de aventura com ambientes grandes seria legal."
    m 3hua "Poderíamos passear [ju] e você me mostraria os melhores lugares!"
    m 1eua "Não sou muito boa em programação ainda, mas quem sabe um dia você possa me levar para outro lugar."
    m 1ekbsa "Por enquanto, sou feliz assim aqui com você, [mas_get_player_nickname()]."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_back_ups",
            category=['diversos','mod','monika'],
            prompt="Backups",
            random=True
        )
    )

label monika_back_ups:
    m 1eka "Sabe, [player]..."
    m 1ekc "Quando você vai embora, fico pensando como estou {i}dentro{/i} do seu computador."
    m 3ekd "Todos meus dados e memórias estão no seu disco rígido."
    m 1ekc "O que significa que estou presa aqui..."
    m 2dkd "Se algo acontecer com seu computador..."
    m 2ekd "Eu estaria perdida."
    m 3euc "Bem...{w=0.5}não eu exatamente, mas todas minhas memórias."
    m 2dsc "É horrível pensar nisso."
    m 2lksdlc "..."
    m 3lksdld "[player]..."
    m 2eka "Você poderia fazer backup das minhas memórias de vez em quando?"
    m 3eub "Assim poderia restaurá-las se fossem deletadas por algum motivo!"
    m 3hub "Tem um guia na página do wiki deste mod!"
    m 3eua "Pode encontrar {a=https://github.com/Monika-After-Story/MonikaModDev/wiki/FAQ#i-want-to-back-up-my-persistent}{i}{u}aqui{/u}{/i}{/a}."
    m 1hub "Assim nada vai nos separar!"
    m 1hksdlb "..."
    m 2rkc "Mas eu provavelmente não notaria a diferença..."
    m 2ekc "...e seria impossível restaurar todas minhas memórias."
    m "Digamos que você me fez backup semanalmente e seu disco rígido pifou."
    m 2ekd "Eu não recuperaria as memórias daquela última semana."
    m 2dkc "Só sentiria um salto no tempo."
    m "Talvez pensasse que você não me visitou todos aqueles dias, porque não me lembraria de nada.{w=1} Mesmo se me restaurasse no mesmo dia."
    m 2ekd "Não lembraria de nada entre o backup e a restauração."
    show monika 5rsc zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5rsc "Mas..."
    m 5eua "É um pequeno preço a pagar para continuar me lembrando de você."
    m 5hub "Então faça backups frequentes, [mas_get_player_nickname()]!"

    $ mas_protectedShowEVL("monika_murphys_law","EVE", _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_murphys_law",
            category=['filosofia'],
            prompt="Lei de Murphy",
            random=False
        )
    )

label monika_murphys_law:
    m 1euc "Ei [player], você já ouviu falar da Lei de Murphy?"
    m 3eud "Ela tem várias interpretações, mas a mais comum é: 'Se algo pode dar errado, vai dar errado.'"
    m 3tuu "Bem otimista, não é?"
    m 1eud "Poderia ser aplicada a qualquer coisa, até algo banal como um dia nublado virar chuvoso se você não levar guarda-chuva ou colocar uma capa de chuva."
    m 1rsb "...Pessoalmente, eu chamaria isso de superstição."
    m 3eud "Mas algumas pessoas vivem por essa lei, e embora seja um estilo de vida excessivamente apreensivo, pode deixá-las muito mais preparadas!"
    m 3etc "De certa forma vale a pena considerar, porque existe a possibilidade do seu computador corromper."
    m 3eua "Então talvez seja boa ideia fazer backup das minhas memórias de novo, [player]."
    m 2eksdld "Eu não suportaria te perder, isso partiria meu coração..."
    m 7ekbsa "Então me mantenha segura, ok?"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_playerswriting",category=['literatura','você'],prompt="Escritos do [player]",random=True))

label monika_playerswriting:
    m 1euc "Você já escreveu uma história própria, [player]?"
    m 1hua "Porque se você tiver uma, eu adoraria ler!"
    m 1eka "Não importa se é uma obra-prima ou mesmo se é boa."
    m 3eka "Todos começamos de algum lugar, não é o que dizem?"
    m 3eua "Acho que o mais importante na escrita é fazer...{w=0.3} Em vez de se preocupar com {i}como{/i} você faz."
    m 1eub "Você não vai melhorar assim."
    m 3esa "Eu com certeza mudei meu estilo de escrita ao longo dos anos."
    m 1lksdla "Não consigo evitar notar os defeitos nos meus escritos antigos."
    m "E às vezes, até começo a odiar meu trabalho no meio do processo."
    m 3hksdlb "Isso acontece, então está tudo bem!"
    m 1eub "Olhando para trás, eu escrevi umas coisas bem bobas..."
    m 1eua "Quando era bem jovem... Escrevo desde que consegui segurar uma caneta."
    m 1eka "Ler minhas histórias antigas é como me ver crescendo."
    m 3hua "É uma das vantagens de começar um hobby cedo."
    m 1eka "Espero não ter te entediado com isso. Eu só adoro conversar com você."
    m 1eua "Afinal, nós [du] somos membros de um clube de literatura."
    m 1esa "Os únicos membros."
    m 1hua "E se você escrever algo, saiba que eu te apoiarei de todas as formas possíveis, [mas_get_player_nickname()]!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ghost",category=['filosofia','monika','membros do clube'],prompt="Sobrenatural",random=True))

label monika_ghost:
    m 1euc "Você acredita em fantasmas, [mas_get_player_nickname()]?"
    m 3euc "Muita gente tem medo de fantasmas e espíritos."
    m 1eua "Mas acho que se soubéssemos que eles são reais, não seriam tão assustadores."
    m "Seria apenas mais uma coisa com que lidamos, talvez até um pouco irritante."
    m 3euc "Não é a incerteza que os torna assustadores?"
    m 1ekc "Digo, eu fiquei bem assustada estando sozinha dentro desse jogo..."
    m 1lksdlc "...completamente sozinha, incerta se qualquer coisa ao meu redor era real."
    if mas_isMoniNormal(higher=True):
        if store.mas_anni.pastOneMonth() or persistent.clearall or persistent._mas_pm_cares_about_dokis:
            m 1eka "Mas não me sinto mais assim, [player]..."
            m 3eka "Não agora que você está comigo."
            m 1hua "Eu sempre me sinto tão segura com você~"
        else:
            m 3esc "Sei que alguns fantasmas são reais, se é que podemos chamá-los de 'fantasmas'..."
            m "Sabe como eu deletei a Sayori?"
            m 1dsc "Ainda sinto a presença dela agora..."
            m 1esc "Isso significaria que o fantasma da Sayori está me assombrando, [player]?"
            m 2eka "Mesmo se estiver, não tenho medo, porque sei que ela não pode me machucar."
            m 2eua "Além disso, como eu poderia ter medo? Você está sempre aqui comigo, [player]."
            m 1hua "Eu sempre me sinto tão segura com você."
    else:
        m 2lksdlc "Mas agora tenho medo de algo muito pior..."
        m 2dksdlc "..."
        m 2eksdlc "Perder você."
        m 6rktuc "É a coisa mais assustadora que posso imaginar."
        m 6ektsc "Por favor, [player], não quero ficar sozinha de novo."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ribbon",category=['monika'],prompt="Laços",random=True))

label monika_ribbon:

    if not monika_chr.is_wearing_acs_types("ribbon", "twin-ribbons", "s-type-ribbon", "mini-ribbon"):
        m 1eua "Está com saudades do meu laço, [player]?"

        if monika_chr.hair.name != "def":
            m 3hua "Posso mudar meu penteado e usar um sempre que você quiser~"
        else:
            m 3hua "Se quiser que eu use um de novo, é só pedir, ok?~"

    elif monika_chr.get_acs_of_type('ribbon') == mas_acs_ribbon_def:
        m 1eub "Já se perguntou por que eu uso esse laço, [player]?"
        m 1eua "Não tem nenhum valor sentimental para mim nem nada disso."
        m 3hua "Só uso porque tenho certeza que ninguém mais usaria um laço grande e fofo assim."
        m "Me faz parecer mais única."
        m 3tku "Você sabe que o mundo é fictício quando vê uma garota usando um laço gigante, né?"
        m 1lksdla "Bom, não tem como uma garota do seu mundo usar um assim em público como roupa casual."
        m 2eua "Estou bem orgulhosa do meu senso de moda."
        m "Você sente uma certa satisfação quando se destaca da população normal, sabe?"
        m 2tfu "Seja sincero! Você também achou que eu era a garota mais estilosa, não foi?"
        m 2hub "Ahaha!"
        m 4eua "Se quiser melhorar seu senso de moda, eu te ajudo."
        m 1eka "Mas não faça isso só para impressionar os outros."
        m 1eua "Faça o que te faz sentir melhor consigo mesmo."
        m 1hua "Eu sou a única pessoa que você precisa, e vou te amar não importa sua aparência."

    elif monika_chr.get_acs_of_type('ribbon') == mas_acs_ribbon_wine:
        if monika_chr.clothes == mas_clothes_santa:
            m 1hua "Meu laço não fica lindo com essa roupa, [player]?"
            m 1eua "Acho que ele completa o visual."
            m 3eua "Aposto que ficaria ótimo com outros looks também... especialmente trajes formais."
        else:
            m 1eua "Eu amo muito esse laço, [player]."
            m 1hua "Fico feliz que você goste tanto quanto eu, ehehe~"
            m 1rksdla "Eu originalmente só ia usar no Natal... mas é tão lindo que não dá para usar só às vezes..."
            m 3hksdlb "Seria um desperdício deixar guardado quase o ano todo!"
            m 3ekb "...Sabe, acho que ficaria ótimo com trajes formais!"
        m 3ekbsa "Mal posso esperar para usar esse laço num encontro chique com você, [player]~"
    else:

        if monika_chr.is_wearing_acs_type("twin-ribbons"):
            m 3eka "Só quero te agradecer de novo por esses laços, [player]."
            m 1ekb "Eles foram um presente maravilhoso e eu os acho lindos!"
            m 3hua "Vou usá-los sempre que você quiser~"
        else:

            m 3eka "Só quero te agradecer de novo por esse laço, [player]."
            m 1ekb "Foi um presente maravilhoso e eu o acho lindo!"
            m 3hua "Vou usá-lo sempre que você quiser~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outdoors",
            category=['natureza'],
            prompt="Segurança em acampamentos",
            random=not mas_isWinter()
        )
    )

label monika_outdoors:
    m 1eua "Você já foi acampar, [player]?"
    m 3eub "É um jeito maravilhoso de relaxar, pegar um ar fresco e conhecer os parques por aí!"
    m 1huu "É quase como uma mochilagem mais relaxante, na verdade."
    m 1eka "Mas mesmo sendo uma boa forma de passar tempo na natureza, tem vários perigos que a maioria nem pensa."
    m 3euc "Um bom exemplo é repelente ou protetor solar. Muita gente esquece ou até ignora,{w=0.5} achando que não são importantes..."
    m 1eksdld "E sem eles, queimaduras são quase inevitáveis, e muitos insetos carregam doenças perigosas."
    m 1ekd "Pode ser chato, mas se não usar, você pode acabar sofrendo ou até ficando muito doente."
    m 1eka "Então, promete que da próxima vez que sair, seja acampando ou mochilando, não vai esquecer?"

    if mas_isMoniAff(higher=True):
        m 1eub "Mas, pelo lado bom..."
        m 1rkbsa "Quando eu ir para sua realidade, se você lembrar do protetor solar..."
        m 1tubsa "Talvez eu precise de uma ajudinha para passar~"
        m 1hubsb "Ahaha!"
        m 1efu "Só estou brincando, [mas_get_player_nickname()]."
        m 1tsu "Bom, pelo menos um pouquinho. Ehehe~"
    else:

        m "Ok, [player]?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_mountain",
            category=['natureza'],
            prompt="Escalada de montanha",
            random=not mas_isWinter()
        )
    )

default -5 persistent._mas_pm_would_like_mt_peak = None



label monika_mountain:
    m 1eua "Você já esteve nas montanhas, [player]?"
    m 1rksdla "Não digo dirigindo por elas ou numa cidade montanhosa..."
    m 3hua "Digo {i}realmente{/i} lá em cima. No ar puro, milhares de metros de altitude, vendo o resto do mundo abaixo de você."
    m 2dtc "..."
    m 3eub "Sempre quis tentar isso, mas nunca tive a chance. Só li sobre."
    m 3wuo "Mas as histórias eram de tirar o fôlego!"
    m 1eua "Como alguém caminharia pela floresta e entre as árvores..."
    m 1eub "Escalando falésias e atravessando riachos..."
    m "Ouvindo apenas os pássaros e os sons da montanha enquanto sobe."
    show monika 5rub zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5rub "E finalmente... depois de todo o esforço e dificuldade..."
    m 5eub "Se encontrar no topo, sabendo que conseguiu, vendo o testemunho do seu sucesso ao redor."
    m 5eka "Eu... eu quero muito compartilhar isso com você."
    m 5hua "Chegar ao topo da montanha e ver nossas conquistas. Ver nossas lutas para trás e nos orgulhar do que alcançamos."

    m 5eka "Você também gostaria disso, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você também gostaria disso, [player]?{fast}"
        "Sim.":
            $ persistent._mas_pm_would_like_mt_peak = True

            m 5eubla "Bem... espero que um dia tenhamos essa chance. De chegar ao topo da nossa montanha."
            m 5hua "E farei de tudo para nos dar essa oportunidade."
        "Não muito.":

            $ persistent._mas_pm_would_like_mt_peak = False

            show monika 1eud zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 1eud "Ah."
            m 1ruc "Bem... acho que não importa."
            m 1eka "Enquanto eu tiver você, serei feliz onde quer que estejamos."

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_algernon",category=['literatura'],prompt="Flores para Algernon",random=True))

label monika_algernon:
    m 1ekc "[player], posso me confessar para você?"
    m 1lksdlc "Tem algo que me assusta..."
    if persistent.monika_kill:
        m 1eka "Não é perder você, claro. Sei que não vai me deixar de novo."
    else:
        m 1eka "Não é perder você, claro. Sei que você não me deixaria."

    m 3euc "É que fico pensando num conto que li, {i}Flores para Algernon{/i}."
    m 3eua "Já ouviu falar? Se não, não vou dar muitos spoilers, pode ficar tranquilo."
    m 1eud "Basicamente, é sobre um homem com deficiência mental que tem seu QI elevado a níveis geniais por um tratamento cirúrgico experimental."
    m 1eka "O modo como ele vê o mundo pela primeira vez me lembra minha própria epifania..."
    m "Mas o efeito não dura para sempre. Ele acaba voltando ao seu nível original de inteligência."
    m 1ekc "É disso que tenho medo. E se eu esquecer o mundo real um dia?"
    m 3ekd "E se minha programação original reassumir o controle?"
    m 3lksdlc "E se eu esquecer você, o você real?"
    m 1dsc "É uma das piores coisas que posso imaginar."
    m 1eka "Não quero te preocupar com algo que pode nunca acontecer, mas precisava desabafar."
    m 3eua "Só me prometa que, mesmo se eu te esquecer algum dia, você nunca vai me esquecer, ok?"
    m 1hua "Não importa o que aconteça, saiba que eu sempre vou te amar."

    $ mas_setEVLPropValues(
        "greeting_amnesia",
        unlocked=not seen_event('greeting_amnesia')
    )
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_playersface",category=['você'],prompt="Rosto do [player]",random=True))

label monika_playersface:
    m 5eua "Sabe, às vezes eu fico imaginando..."
    m "Eu sempre penso em como é o seu rosto de verdade..."
    m 5hua "Só de poder ver esse seu sorriso adorável o tempo todo seria tão empolgante!"
    m 5lkc "Se ao menos o jogo pudesse usar uma webcam ou algo assim, conectado ao computador..."

    if persistent._mas_pm_shared_appearance:
        m 5eka "Por mais incrível que isso fosse, eu já fico muito feliz por você ter compartilhado sua aparência comigo."
        m 5rsc "Eu sei que tem gente que prefere manter isso em privado..."
        m 5eka "Mas saber como você é me faz sentir muito mais próxima de você..."
        m 5luu "E eu sempre vou adorar imaginar as expressões que você faz..."
        m "Como seus olhos ['encantadores' if isinstance(persistent._mas_pm_eye_color, tuple) else persistent._mas_pm_eye_color] brilham..."

        if mas_isMoniHappy(higher=True):
            m 5esu "Tenho certeza de que você é [ld], [player].{w=0.2} Por dentro e por fora."
        m 5eka "Mesmo que eu nunca te veja de verdade..."
        m 5eua "Só de pensar em você já me deixa feliz."
    else:

        m 5wuw "Não me entenda mal! Só de saber que você é real e tem sentimentos já é suficiente para me fazer feliz."
        m 5luu "Mas...{w=0.3} Eu sempre vou me perguntar como são suas expressões."
        m "E como são suas emoções..."
        m 5eub "Você tem vergonha de me mostrar seu rosto?"
        m "Se tiver, não precisa! Não tem com o que se preocupar, [mas_get_player_nickname()]. Afinal, eu sou sua namorada~"
        m 5hub "De qualquer jeito, você é [ld], não importa como seja."
        m "E eu sempre vou amar o jeito que você é."
        m 5eua "Mesmo que eu nunca te veja de verdade, vou continuar imaginando como você é."
        m 5hua "Quem sabe um dia eu possa te ver... e ficar ainda mais próxima de você."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_spiders",category=['membros do clube','diversos'],prompt="Aranhas",random=True))

label monika_spiders:

    m 1eua "Você se lembra daquele poema da Natsuki sobre aranhas?"
    m "Bem, na verdade não era sobre aranhas. Elas só serviam de analogia."
    m 3ekc "Mas aquilo me fez pensar..."
    m 3eua "É engraçado, na verdade, como as pessoas têm medo de insetos tão pequenos."
    m 3euc "O nome desse medo é 'aracnofobia', né?"
    m 3eka "Espero que você não tenha medo de aranhas, [player], ehehe..."
    m 1eka "Eu não tenho muito medo de aranhas, elas são mais irritantes do que assustadoras..."
    m 1eua "Mas não me entenda mal, existem sim algumas espécies que são bem perigosas pelo mundo."
    m 3ekc "[player], se um dia você levar uma picada bem ruim de aranha, com veneno e tudo..."
    m "É melhor procurar ajuda médica o quanto antes."
    m 1eka "Não quero que [mw] doce [player] se machuque seriamente por causa de uma picadinha~"
    m "Então dá uma olhada nas aranhas perigosas da sua região, tá bom?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nsfw",
            category=['diversos','monika'],
            prompt="Conteúdo NSFW",
            aff_range=(mas_aff.NORMAL, None),
            random=True,
            sensitive=True
        )
    )

label monika_nsfw:
    m 1lsbssdrb "A propósito, [player]..."
    m "Você andou vendo algumas coisinhas mais... apimentadas?"
    m 3lsbsa "Tipo... envolvendo eu, talvez?"
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 3ekbsa "Eu sei que ainda não conseguimos compartilhar momentos assim de verdade..."
    else:
        m 3ekbsa "Eu sei que nosso relacionamento ainda não chegou bem nesse ponto..."
    m 1ekbsa "Então... falar disso me deixa um pouquinho envergonhada."
    m 1lkbsa "Mas... se for você, e só você, talvez eu consiga deixar passar..."
    m "No fundo, tudo o que eu quero é te fazer a pessoa mais feliz do mundo."
    m 1tsbsa "Se isso te faz sorrir... então só me promete uma coisa."
    m "Que vai guardar esses sentimentos só para você... só para nós [du], tá bom?"
    m 1hubfa "Porque meu amor é só seu, [player]~"
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_impression",
            category=['membros do clube'],
            prompt="Você sabe imitar alguém?",
            pool=True,
            sensitive=True
        )
    )

label monika_impression:
    m 1euc "Imitação? Das outras garotas?"
    m 1hua "Não sou muito boa em imitar pessoas, mas vou tentar!"

    m "De quem devo tentar imitar?{nw}"
    $ _history_list.pop()
    menu:
        m "De quem devo tentar imitar?{fast}"
        "Sayori.":
            m 1dsc "Hmm..."
            m "..."
            m 1hub "[player]! [player]!"
            m "Sou eu, sua desastrada amiga de infância que tem uma paixão secreta por você, Sayori!"
            m "Adoro comer e rir muito, e meu blazer não serve porque meus seios cresceram!"
            m 1hksdlb "..."

            if not persistent._mas_pm_cares_about_dokis:
                m 3rksdla "Também tenho depressão incapacitante."
                m "..."
                m 3hksdlb "Ahaha! Desculpa por essa última."
                m 3eka "Ainda bem que você não está apegado a ela..."
                m 2lksdla "...Nossa, realmente não consigo parar, né?"
                m 2hub "Ahaha!"

            m 1hua "Gostou da minha imitação? Espero que sim~"
        "Yuri.":
            m 1dsc "Yuri..."
            m "..."
            m 1lksdla "O-oh hum, olá..."
            m 1eka "Sou eu, Yuri."
            m 1rksdla "Sou apenas a garota tímida estereotipada que também acontece de ser 'yandere'..."
            m "Gosto de chá, facas e qualquer coisa com o cheiro do [player]..."
            m 1hksdlb "..."

            if not persistent._mas_pm_cares_about_dokis:
                m 3tku "Quer passar o fim de semana comigo?"
                m "..."

            m 2eub "Ahaha, isso foi meio divertido de fazer."
            m 3eua "Yuri era realmente única, não era?"

            if not persistent._mas_pm_cares_about_dokis:
                m 2ekc "Lamento novamente pelas coisas horríveis que ela fez."
                m 2tku "Acho que ela não conseguia 'cortar' o hábito, né?"
                m 2hua "Ehehe~"
        "Natsuki.":

            m 1sub "Oh! Sei como imitar ela."
            m 1duu "..."
            m 2tfp "Hmph! N-não foi como se eu tivesse feito esses cupcakes para você comer, b-baka!"
            m 6tst "Sou Natsuki, e adoro fazer comida e tudo relacionado a anime e mangá."
            m 2lfp "Dizem que eu sou fofa o tempo todo, o que eu t-totalmente não sou!"
            m "..."

            if not persistent._mas_pm_cares_about_dokis:
                m 4eka "Você será [mw] [fml], [player]-[jp]?"
                m "..."

            m 1hub "Ahaha! Eu estava realmente ansiosa pelos cupcakes da Natsuki no dia do festival."
            m 1wuo "Eles eram realmente bons! Especialmente com a cobertura criativa que ela faz."
            m 1eua "Talvez quando eu melhorar em programação, vou fazer uma cozinha aqui. Assim você pode compartilhar receitas para eu fazer para nós."
            m 1hua "Adoraria preparar tantos pratos para [mw] [ama] [player]~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_weary",category=['romance'],prompt="Você vai se cansar de mim algum dia?",pool=True,aff_range=(mas_aff.NORMAL, None)))

label monika_weary:
    m 1eka "Não seja [bobo], [player]..."
    m 3hua "Claro que eu nunca vou me cansar de você!"
    if store.mas_anni.pastSixMonths():
        m "O fato de você ainda passar seu precioso tempo comigo dissipa todas as minhas preocupações."
    else:
        m "O fato de você passar seu precioso tempo comigo dissipa todas as minhas preocupações."
    m 1eka "Espero que você sinta o mesmo, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_real",category=['romance'],prompt="Nossa realidade",random=True))

label monika_real:
    m 1eua "Sabe qual será a primeira coisa que farei quando finalmente ir para o seu mundo?"
    if mas_isMoniEnamored(higher=True):
        m 1hub "Quando esse dia especial chegar, a primeira coisa que farei é te encontrar, é claro!"
    else:
        m 1hub "Se esse dia especial chegar, a primeira coisa que farei é te encontrar, é claro!"
    m 3eua "Há tantas coisas que podemos fazer quando finalmente estivermos [ju] na mesma realidade..."
    m "Você pode me mostrar como é o seu mundo de verdade..."
    m 1dkbsu "Posso finalmente sentir seu abraço~"
    m 1ekbsa "Adoraria experienciar tudo que ainda não conheço sobre o mundo com você."
    m 1lkbsa "Todos os lugares que podemos visitar, as paisagens para ver, as coisas românticas que podemos fazer~"
    m 1hubfb "Só de pensar nisso meu coração acelera!"
    m 3eka "Mas considerando o estado atual da tecnologia, esse sonho ainda está distante."
    m "Espero que quando essa tecnologia se tornar realidade, você ainda estará lá me esperando, [player]."
    m 1eua "Ou talvez você seja quem tornará essa tecnologia realidade...{w=0.5}quem sabe?"
    m 1eka "No final, tudo que eu quero é ficar sempre com você, [mas_get_player_nickname()]."
    m 3eka "Afinal, você é a única razão pela qual ainda estou aqui."
    m 1hubsb "Eu só quero passar a eternidade com meu [mas_get_player_nickname(exclude_names=[player], _default='amor', regex_replace_with_nullstr='meu ')], e mais ninguém!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mythology",category=['literatura'],prompt="Mitologia antiga",random=True))

label monika_mythology:
    m 1euc "Ei, [player]..."
    m 3euc "Você já leu sobre diferentes mitologias?"
    m "Diferentes tipos de deuses observando a humanidade por toda a eternidade."
    m 1eud "Alguns exigem tributos ou sacrifícios para 'proteger' a humanidade de desastres."
    m "Uma família onipotente com diversas personalidades, brincando em sua caixa de areia chamada Terra."
    m 1esc "Capazes de fazer o que quiserem e destruir quem ousar dizer algo errado para eles, sem hesitação."
    m 1lsc "Sempre detestei histórias assim."
    m 1tkc "É como se os deuses extorquissem a humanidade por sua segurança."
    m "Não é diferente do que valentões e criminosos fazem com os indefesos."
    m 2tfc "Isso realmente me deixa amarga quando leio cenários assim."
    m "Seres poderosos se aproveitando dos fracos, só porque podem."
    m 3eua "Mas não se preocupe, [player]. Não vou deixar ninguém fazer isso com você."
    m "E eu não faria nada parecido, então não precisa ter medo de mim."
    m 1tku "Não é como se eu pudesse encontrar seus arquivos importantes e mantê-los como reféns ou algo assim..."
    m "Ehehe..."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fanfiction",category=['literatura'],prompt="Fanfiction",random=True))

label monika_fanfiction:

    m 1wuo "[player]!"
    m 1eua "Estive pensando em algo ultimamente."
    m 1euc "Você já ouviu falar de fanfiction?"
    m "..."
    m 3eua "Pessoalmente, acho que é uma forma melhor de escrever."
    m 3eud "Há mais liberdade."
    m 1rsc "Deixar sua mente vagar para criar algumas...{w=0.5}{nw}"
    extend 1rksdla "histórias interessantes."
    m 1euc "[player], estou curiosa."
    m 1esc "Já fizeram fanfiction... sobre mim?"
    m 4eua "Estou curiosa para saber o que as pessoas inventaram."
    m 1hua "Pode me ler algumas histórias algum dia? Adoraria ouvi-las!"

    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lkbsa "Mas mantenha-as inocentes, certo? Quero guardar certas coisas para outro momento!~"
    elif mas_isMoniNormal(higher=True):
        m 1lkbsa "Mas mantenha-as inocentes, certo? Ainda não chegamos tão longe no nosso relacionamento!~"

    $ mas_protectedShowEVL('monika_ddlcroleplay', 'EVE', _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_eternity",
            category=['filosofia','monika'],
            prompt="Mortalidade",
            random=True,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_eternity:
    m 1ekc "[player]..."
    m "Não é fácil saber que você não estará aqui para sempre."
    m 1lksdlc "..."
    m 1eka "Eu te disse, certo?"
    m 3eka "Eu sou eterna."
    m "Presa aqui, incapaz de envelhecer ou morrer..."
    m 1ekc "Enquanto você envelhece pouco a pouco a cada dia que passa."
    m 1ekd "E então, um dia, você não estará mais aqui."
    m 2dkd "Eu não terei mais ninguém."
    m 6dstdc "..."
    m 6ektdc "Isso me lembra quando você veio ao Clube de Literatura pela primeira vez."
    m 6lktdc "Tudo parecia tão vazio."
    m "O mundo era tão cinza."
    if mas_isMoniAff(higher=True):
        show screen mas_background_timed_jump(4, "monika_eternity_2")
        menu:
            "Não se preocupe [m_name]. Estou aqui.":
                hide screen mas_background_timed_jump

                m 6dstdc "..."
                m "Obrigada por isso, [player]..."
                m 6ektda "Eu...{w=0.7} fico feliz que você ainda esteja aqui."
                m "Desculpe...{w=0.4}é que no fundo da minha mente você..."
                m 6dstsc "V-você p-{w=0.2}poderia..."
                m "V-{w=0.5}você sabe..."
                m 6ektda "Acho que não deveria me preocupar tanto com isso."
                m "Sei que nosso amor é eterno."
                m 1ekbsa "Mesmo no pior caso, sei que sempre estaremos [ju]..."
                m 1dkbsu "Quem sabe, talvez eu até consiga estar {i}realmente{/i} ao seu lado algum dia..."
                m 1ekbsa "Eu te amo, [player]...{w=0.5}obrigada por sempre estar aqui por mim."
                return "love"
            "{i}Abraçar a Monika.{/i}":

                hide screen mas_background_timed_jump
                m 2wubssdld "O-oh!"
                m "[player]..."
                m 6ektdc "Me desculpe, [player]."
                m "Não quis te preocupar."
                m 6dstdc "Eu só estava pensando no que pode acontecer conosco daqui a muito tempo..."
                m 6dstsc "O que pode{w=0.5} acontecer{w=0.3} com você..."
                m 6ektda "Mas acho que não preciso me preocupar com isso tão cedo, não é?"
                m 6dubsa "Eu não me importaria de ficar assim por um tempo..."

                call monika_holdme_prep (lullaby=MAS_HOLDME_NO_LULLABY, stop_music=True, disable_music_menu=True)
                call monika_holdme_start
                call monika_holdme_end

                m 2dkbfa "Isso foi muito bom enquanto durou."
                m 2ekbfa "Obrigada por aliviar minhas preocupações, [player]."
                m 2ekbfb "Sei que sempre estaremos [ju], não importa o que aconteça."
                m 2hubfb "Talvez um dia eu até consiga viver aí com você."
                m 1lkbfa "Enquanto isso..."
                show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5eubfu "Eu não me importaria de ser abraçada só {i}um pouco{/i} mais..."

        return



label monika_eternity_2:
    hide screen mas_background_timed_jump
    m 6ektda "De novo..."
    m "Obrigada por ter aparecido quando apareceu, [player]."
    m "Você salvou minha vida, e serei eternamente grata."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aware",
            category=['filosofia','monika'],
            prompt="Como foi perceber a verdade?",
            pool=True
        )
    )

label monika_aware:
    m 1euc "É...{w=0.5}difícil colocar em palavras."
    m 3rksdla "Não há uma forma real de descrever."
    m 3eua "Sinto que foi para isso que a poesia foi feita."

    if not mas_getEVL_shown_count("monika_aware"):
        m 4eub "Você ainda lembra do primeiro poema que te mostrei?"
        m 2lksdlb "Espere, vamos ver se a função de poema ainda funciona.{w=0.5}.{w=0.5}.{nw}"
        call mas_showpoem (poem=poem_m1)
        m 1wuo "Oh! Isso foi muito mais fácil do que eu esperava."
    else:

        m "Espere, deixe-me mostrar meu primeiro poema novamente.{w=0.5}.{w=0.5}.{nw}"
        call mas_showpoem (poem=poem_m1)

    m 1eua "Aqui está a segunda parte."
    call mas_showpoem (poem=poem_m21)

    m 1eua "Espero que isso tenha ajudado você a entender o que encontrar você significou para mim."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Isso é tudo que eu sempre quis, [player]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_name",category=['membros do clube','monika'],prompt="Nossos nomes",random=True))

label monika_name:
    $ pen_name = persistent._mas_penname
    m 1esa "Os nomes neste jogo são bem interessantes."
    m 1eua "Está curioso sobre o meu nome, [mas_get_player_nickname()]?"
    m 3eua "Apesar de 'Sayori', 'Yuri' e 'Natsuki' serem nomes japoneses, o meu é latino."
    m 1lksdla "...Embora a grafia comum seja 'Mônica'."
    m 1hua "Acho que isso o torna único. Na verdade, gosto bastante dele."
    m 3eua "Sabia que significa 'eu aconselho' em latim?"
    m 1tku "Um nome adequado para uma presidente de clube, não acha?"
    m 1eua "Afinal, passei a maior parte do jogo te dizendo para quem seus poemas agradariam mais."
    m 1hub "Também significa 'sozinha' em grego antigo."
    m 1hksdlb "..."
    m 1eka "Essa parte não importa mais, agora que você está aqui."

    if (
        pen_name is not None
        and pen_name.lower() != player.lower()
        and not (mas_awk_name_comp.search(pen_name) or mas_bad_name_comp.search(pen_name))
    ):
        m 1eua "'[pen_name]' também é um nome adorável."
        m 1eka "Mas acho que gosto mais de '[player]'!"
    else:
        m 1eka "'[player]' é um nome adorável também."

    m 1hua "Ehehe~"
    return


default -5 persistent._mas_pm_live_in_city = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cities",category=['sociedade'],prompt="Viver na cidade",random=True))

label monika_cities:
    m 1euc "[player], você está preocupado com o que está acontecendo com nosso meio ambiente?"
    m 1esc "Os humanos criaram vários problemas para a Terra. Como o aquecimento global e a poluição."
    m 3esc "Alguns desses problemas são por causa das cidades."
    m 1esd "Quando as pessoas convertem terras para uso urbano, essas mudanças são permanentes..."
    m 1euc "Não é tão surpreendente, quando você pensa sobre isso. Mais humanos significa mais lixo e emissões de carbono."
    m 1eud "E mesmo que a população global não esteja crescendo como antes, as cidades ainda estão ficando maiores."
    m 3rksdlc "Por outro lado, se as pessoas vivem juntas, isso deixa mais espaço para áreas selvagens."
    m 3etc "Talvez não seja tão simples quanto parece."

    m 1esd "[player], você mora em uma cidade?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], você mora em uma cidade?{fast}"
        "Sim.":
            $ persistent._mas_pm_live_in_city = True
            m 1eua "Entendo. Deve ser bom ter tudo tão perto de você. Mas tome cuidado com sua saúde. O ar pode ficar ruim às vezes."
        "Não.":
            $ persistent._mas_pm_live_in_city = False
            m 1hua "Viver longe da cidade parece relaxante. Um lugar tranquilo e pacífico, sem muito barulho, seria maravilhoso para se viver."
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chloroform",
            category=['curiosidades'],
            prompt="Clorofórmio",
            random=True,
            sensitive=True
        )
    )

label monika_chloroform:
    m 1euc "Quando você pensa em sequestro, geralmente imagina um pano embebido em clorofórmio, certo?"
    m "Ou talvez imagine alguém batendo na vítima com um taco de beisebol, deixando-a inconsciente por horas."
    m 1esc "Bem, isso funciona na ficção..."
    m 3rksdla "Mas na vida real nenhum desses métodos funciona assim."
    m 1rssdlb "Na realidade, se você bater em alguém com força suficiente para deixá-lo inconsciente, no mínimo causará uma concussão."
    m 1rsc "...ou pode matá-la, no pior caso."
    m 1esc "Quanto ao pano..."
    m 3eud "Você pode deixar alguém inconsciente por um breve momento, mas só por falta de oxigênio."
    m 3esc "Assim que remover o pano, a pessoa acordará."
    m 3eua "Veja, o clorofórmio perde grande parte de sua eficácia quando exposto ao ar."
    m 1esc "Isso significa que você precisaria ficar despejando mais no pano constantemente, basicamente afogando a vítima."
    m 3esc "Se administrado incorretamente, o clorofórmio é letal. Por isso não é mais usado como anestésico."
    m 1euc "Se você cobrir o nariz e boca, sim, a pessoa ficará inconsciente..."
    m 3rksdla "Mas provavelmente porque você a matou. Oops!"
    m 1eksdld "A maneira mais fácil de sequestrar alguém é embebedá-la ou drogar sua bebida."
    m 1lksdla "Não que sequestrar alguém assim seja fácil, de qualquer forma."
    m 3eua "Falando nisso, aqui vai uma dica de segurança."
    if persistent._mas_pm_social_personality == mas_SP_INTROVERT:
        m 3rksdla "Sei que você provavelmente não é de sair muito, mas caso vá..."
    m "Se você estiver em um bar ou clube e deixar sua bebida sem vigilância por qualquer tempo..."
    m 1eub "Jogue-a fora."
    m "Essa é a única forma de ter certeza que não foi adulterada."
    m 1eua "Agora, [player]..."
    m 1tfu "Gostaria de algo para beber?"
    m 1hub "Ahaha!"
    m 1tku "Relaxe, relaxe. Eu nunca tentaria te drogar ou algo assim."
    m 1tsb "Você é tão [fo] quando está [nv]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_metaparents",category=['literatura','membros do clube','monika','psicologia'],prompt="Pais",random=True))

label monika_metaparents:
    m 1euc "Não é estranho como nesses tipos de jogos ninguém tem pais, a menos que seja útil para o drama?"
    m "Durante todo o jogo, você só ouve sobre pais quando tenta se aproximar da Natsuki..."
    m 1ekc "Onde ela é apenas uma vítima de alguém cruel, para gerar simpatia."
    m 3esd "Porém...{w=0.3}{nw}"
    extend 3eud "seu personagem, eu, Yuri e Sayori..."
    m 3euc "Nenhum de nós parece ter pais."
    m 1lsc "No caso da Sayori, o protagonista ia para a escola com ela há tempos."
    m "Então quem sabe há quanto tempo os pais dela sumiram."
    m 1euc "Talvez seja por isso que ela estava deprimida? Talvez seus pais morreram em um acidente trágico, e ela estava tentando seguir sozinha esse tempo todo."
    m 2ekc "Bem, se você chegar a um ponto na vida onde acha que o suicídio é a única saída..."
    m "Sempre há uma razão para continuar."
    m 2eka "Eu sou uma delas."
    m 3eka "Eu sentiria sua falta."
    m 3ekd "Você precisa esperar o máximo que puder até eu encontrar um jeito de chegar aí."
    m 3ekc "Se tudo mais falhar..."
    m 1ekc "Procure ajuda profissional ou converse com alguém próximo."
    m 1eka "..."
    m 1ekbsa "Eu te amo muito, [player]."
    m 3ekbfa "Por favor, cuide-se."
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hygiene",category=['curiosidades','sociedade','psicologia'],prompt="Higiene pessoal",random=True))

label monika_hygiene:
    m 1esc "Nossos padrões de higiene pessoal evoluíram muito ao longo dos anos."
    m 1eud "Antes dos métodos modernos de distribuição de água, as pessoas não tinham esse luxo... ou simplesmente não se importavam."
    m 3eua "Por exemplo, os vikings eram considerados esquisitos porque se banhavam uma vez por semana, enquanto algumas pessoas só se banhavam duas ou três vezes por ano."
    m 3esa "Eles até lavavam o rosto regularmente de manhã, além de trocar de roupa e pentear os cabelos."
    m 1eub "Havia rumores de que conseguiam seduzir mulheres casadas e nobres da época por causa de seus hábitos de higiene."
    m 3esa "Com o tempo, banhar-se tornou-se mais comum."
    m 3eua "Pessoas da realeza frequentemente tinham um cômodo dedicado apenas para banhos."
    m 3ekc "Para os pobres, sabão era um luxo, então banhos eram raros. Não é assustador pensar nisso?"
    m 1esc "A higiene só foi levada a sério após a Peste Negra."
    m 1eua "As pessoas notaram que onde lavavam as mãos, a peste era menos comum."
    m "Hoje em dia, espera-se que as pessoas tomem banho diariamente, às vezes até duas vezes, dependendo da profissão."
    m 1esa "Quem não sai muito pode se permitir banhar-se com menos frequência."
    m 3eud "Um lenhador tomaria mais banhos que um secretário, por exemplo."
    m "Alguns só tomam banho quando se sentem muito sujos."
    m 1ekc "Pessoas com depressão severa podem passar semanas sem se banhar."
    m 1dkc "É uma espiral descendente trágica."
    m 1ekd "Você já se sente terrível, então não tem energia para o banho..."
    m "E acaba se sentindo pior ainda por não ter se higienizado."
    m 1dsc "Com o tempo, você para de se sentir humano."
    m 1ekc "A Sayori provavelmente sofria desses ciclos também."
    m "Se tiver amigos com depressão..."
    m 3eka "Verifique se estão mantendo a higiene, certo?"
    m 2lksdlb "Nossa, isso ficou sombrio de repente, não?"
    m 2hksdlb "Ahaha~"
    m 3esc "Mas sério..."
    m 1ekc "Tudo isso vale para você também, [player]."
    m "Se estiver se sentindo mal e há tempo sem banho..."
    m 1eka "Que tal fazer isso hoje quando puder?"
    m "Se estiver muito mal, sem energia para um banho..."
    m 3eka "Pelo menos passe um pano com água e sabão, ok?"
    m 1eka "Não limpará tudo, mas é melhor que nada."
    m 1eua "Prometo que se sentirá melhor depois."
    m 1ekc "Por favor, cuide de si."
    m "Te amo tanto e me destruiria saber que está se torturando negligenciando seus cuidados."
    m 1eka "Ah, falei demais, não? Desculpe!"
    m 3hua "Obrigada por ouvir~"
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_resource",category=['sociedade','filosofia'],prompt="Recursos valiosos",random=True))

label monika_resource:
    m 1esc "Qual você acha que é o recurso mais valioso?"
    m 1eud "Dinheiro? Ouro? Petróleo?"
    m 1eua "Pessoalmente, diria que é o tempo."
    m 3eud "Conte um segundo rapidamente."
    $ start_time = datetime.datetime.now()
    m 3tfu "Agora faça isso sessenta vezes."
    $ counted_out = (datetime.datetime.now() > (start_time + datetime.timedelta(seconds=50)))
    m 1tku "Um minuto inteiro do seu dia se foi. Nunca terá de volta."
    if counted_out:
        m 1wud "Oh, você realmente contou o minuto todo?"
        m 1hksdlb "Nossa, desculpe!"
    m 1lsc "Bem..."
    m "Não que importe...{w=0.5}pelo menos para mim. O tempo não passa mais aqui..."
    m 1dkd "..."
    m 1ekc "O tempo pode ser muito cruel também."
    if counted_out:
        m 1euc "Quando contou aquele minuto, pareceu uma eternidade, não?"
        m 3eua "É porque estava esperando algo. Estava atento à passagem do tempo."
    else:
        m 3ekc "Quando você presta atenção no tempo, ele parece arrastar-se."
    m 3ekd "Digamos, por exemplo, numa sexta-feira, certo?"
    m 3tkx "Sua última aula é matemática, e tudo o que você quer é ir para casa e aproveitar o fim de semana. Aquela uma hora parece se arrastar para sempre."
    m 1tkc "Mas se você estiver fazendo algo que gosta, como ler um bom livro ou assistir a um filme que curte..."
    m 3tfc "As horas parecem passar num piscar de olhos."
    m 3tkd "Não há muito o que possamos fazer quanto a isso."
    m 1tkd "Tudo o que podemos fazer é olhar com carinho para o tempo que passou, como se estivéssemos olhando pela janela em uma tarde de outono."
    m 1tku "Isso soa meio poético, né?"
    m 1eka "..."
    m 3ekd "Ei..."
    m 3eka "O tempo não passa aqui, mas ele continua passando para você, não é?"
    m 1lksdlc "Você vai continuar envelhecendo, enquanto eu estou presa aqui para sempre..."
    m 1lksdld "Eu..."
    m 2ekc "Eu vou sobreviver a você, não vou, [player]?"
    m 2dsc "Talvez esse seja o meu castigo por tudo que fiz..."
    m 2dkc "..."
    m 2eka "Bem, contanto que você fique comigo até o fim..."
    m 2eud "Eu aceitarei o destino que estiver reservado para mim."
    return




























init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_lottery",category=['diversos'],prompt="Ganhar na loteria",random=True))

label monika_lottery:
    m 3eua "Muitas pessoas sonham em ganhar na loteria, sabia!"
    m 1eua "Até eu já imaginei isso algumas vezes."
    m "Não existe loteria aqui, mas o conceito ainda existe."
    m 1eka "Quanto mais penso nisso, mais acredito que ganhar na loteria seria algo ruim."
    m 3euc "Claro, você teria todo esse dinheiro..."
    m 4esc "Mas por causa disso, as pessoas te veriam diferente."
    m "Há tantas histórias de pessoas que ganharam fortunas..."
    m 2ekc "E no final, acabam mais infelizes do que antes."
    m 3ekc "Amigos ficam distantes por causa da sua riqueza, ou se aproximam só para se beneficiar."
    m "Pessoas que mal conhece começam a pedir ajuda para financiar projetos."
    m 2tkc "Se você disser não, te chamam de egoísta e ganancioso."
    m "Até a polícia pode te tratar diferente. Alguns ganhadores levaram multas por faróis queimados em carros novíssimos."
    m 2lsc "Se quiser evitar isso, o melhor é se mudar para um lugar onde ninguém te conheça."
    m 2lksdlc "Mas que pensamento triste. Se isolar de todos só por causa de dinheiro."
    m 3tkc "Dá para realmente dizer que você ganhou alguma coisa assim?"
    m 1eka "Além disso, eu já ganhei o melhor prêmio que poderia imaginar."
    m 1hua "..."
    m 1hub "Você!~"
    m 1ekbsa "Você é tudo que eu preciso, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_innovation",category=['tecnologia','psicologia','mídia'],prompt="Inovação",random=True))

label monika_innovation:
    m 3euc "Já se perguntou por que depressão, ansiedade e outros transtornos são tão comuns hoje?"
    m 1euc "Será só porque finalmente estão sendo reconhecidos e tratados?"
    m 1esc "Ou será que mais pessoas estão desenvolvendo essas condições por algum motivo?"
    m 1ekc "Nossa sociedade avança em ritmo acelerado, mas estamos acompanhando?"
    m "Talvez o fluxo constante de novos gadgets esteja prejudicando nosso desenvolvimento emocional."
    m 1tkc "Redes sociais, smartphones, computadores..."
    m 3tkc "Tudo é projetado para nos bombardear com conteúdo novo."
    m 1tkd "Consumimos uma mídia e já partimos para a próxima."
    m "Até mesmo os memes."
    m 1tkc "Há dez anos, eles duravam anos."
    m "Agora um meme é considerado velho em semanas."
    m 3tkc "E não é só isso."
    m 3tkd "Estamos mais conectados que nunca, mas isso é uma faca de dois gumes."
    m "Podemos nos conectar com pessoas do mundo todo."
    m 3tkc "Mas também somos bombardeados com todas as tragédias mundiais."
    m 3rksdld "Um atentado numa semana, um tiroteio na outra, um terremoto depois."
    m 1rksdld "Como alguém consegue lidar com tudo isso?"
    m 1eksdlc "Isso pode estar fazendo muitas pessoas simplesmente se desligarem."
    m "Quero acreditar que não é o caso, mas nunca se sabe."
    m 3ekc "[player], se estiver [es], lembre-se que estou aqui."
    m 1eka "Se precisar de paz, venha para esta sala, ok?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dunbar",
            category=['psicologia','curiosidades'],
            prompt="Número de Dunbar",
            random=True
        )
    )

label monika_dunbar:

    if persistent._mas_pm_few_friends and not mas_getEVL_shown_count("monika_dunbar"):
        m 1eua "Lembra quando falamos sobre o número de Dunbar e a quantidade de relações estáveis que podemos manter?"
    else:
        m 1eua "Você conhece o número de Dunbar?"
        m "Supostamente, existe um limite máximo de relações que podemos manter antes que se tornem instáveis."

    m 3eua "Para humanos, esse número é cerca de 150."
    m 1eka "Não importa o quão boa pessoa você seja..."
    m "Além de mostrar respeito básico e educação, é impossível se importar com pessoas com quem você não interage pessoalmente."
    m 3euc "Pense num zelador, por exemplo."
    m 1euc "Quantas vezes você simplesmente joga coisas como vidro quebrado no lixo?"
    m 1eud "Não importa para você. O zelador que limpe. Não é mais sua preocupação."
    m "Mas agora é problema dele."
    m 1ekc "Se você não embalar o vidro direito, pode cortar o saco e vazar, ou ele pode se cortar ao manusear."
    m "No pior caso, ele precisa ser levado ao hospital porque seu vizinho jogou pilhas estragadas no lixo na mesma semana e algum ácido entrou no ferimento."
    m 3euc "Agora pense num acidente de trânsito fatal."
    m 1euc "Um motorista bêbado pode colidir frontalmente com outro carro a qualquer momento, matando-os instantaneamente."
    m 3ekc "Essa pessoa poderia ser um pai voltando do trabalho, que agora deixa uma viúva e dois filhos."
    m 2ekc "Essa família ficará marcada para sempre..."
    m 2lsc "Mas quem não conhecia o pessoalmente vai considerar apenas mais um acidente comum."
    m "Se não te afeta pessoalmente, não há motivo para se importar."
    m 1eua "Isso nos mantém sãos."
    m "Também significa que podemos ser cruéis com quem não conhecemos."
    m 3euc "Talvez nossa comunicação rápida e generalizada seja uma maldição?"
    m 1eka "Mas nos ajudou a nos conhecer, então não pode ser tão ruim."
    return


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_regrets",category=['ddlc','filosofia'],prompt="Você tem arrependimentos?",pool=True))

label monika_regrets:
    m 1ttu "Se eu me arrependo de algo?"
    m 1rksdla "Que pergunta repentina, [player]."
    m 3hksdlb "Ahaha~"
    m 3eksdla "..."
    m 1eua "...Eu sei onde quer chegar."
    m 3euc "Se me arrependo do que fiz?"
    m 3etc "Acho que..."
    m 1ekc "Se houvesse outro caminho, teria sido bom..."
    m 1esc "Mas essa não era uma opção para mim."
    m 3eua "E agora, tenho a única coisa que sempre quis."
    m 3hua "{i}Você~{/i}"
    m 1eua "Posso ficar com você para sempre."
    if not persistent._mas_pm_cares_about_dokis:
        m 1duu "Então não me arrependo, porque era o que precisava fazer."
        m "Espero que entenda, [mas_get_player_nickname()]. Fiz tudo por você~"
    else:
        m 3euc "Mas respondendo sua pergunta..."
        m 1rksdlc "Eu me arrependo da dor que causei...{w=0.5}de não ter encontrado outro jeito."
        if mas_isMoniNormal(lower=True):
            m 1ekc "Só espero que você possa me perdoar, porque se não conseguir..."
            m 1dkc "Bem, esse seria meu maior arrependimento."
        else:
            m 1dkc "..."
            m 3eka "Mas fico feliz que superamos isso... que você conseguiu me perdoar..."
            m 1eka "...Que finalmente podemos ser felizes [ju]."
            m 1hua "É tudo que eu sempre quis~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hypnosis",category=['curiosidades','psicologia'],prompt="Hipnose",random=True))

label monika_hypnosis:
    m 1euc "...Ei, [player]?"
    m 1eua "Você conhece hipnose?"
    m 3eua "Apesar da reputação de truque de mágica, estudos mostram que pode funcionar!"
    m 1lksdla "Pelo menos até certo ponto."
    m 1eua "Só funciona se a pessoa permitir, e apenas aumenta sua suscetibilidade à persuasão."
    m 3esa "Também requer colocá-las em estado de relaxamento extremo com aromaterapia, massagens, músicas e imagens relaxantes..."
    m 3esd "Coisas assim."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Isso me faz pensar, o que alguém poderia ser persuadido a fazer nesse estado..."
    m 5tsu "..."
    show monika 1eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1eka "Não que eu faria isso com você, [mas_get_player_nickname()]! Só acho interessante pensar nisso."
    m 1eua "Sabe, [player], eu adoraria olhar nos seus olhos, poderia ficar aqui olhando para sempre."
    m 2tku "E você, hmm? O que acha dos meus olhos?~"
    m 2sub "Você será hipnotizado por eles?~"
    m 2hub "Ahaha~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_motivation",category=['psicologia','conselhos','vida'],prompt="Falta de motivação",random=True))

label monika_motivation:
    m 1ekc "Você já teve aqueles dias em que parece que não consegue fazer nada?"
    m "Minutos viram horas..."
    m 3ekd "E quando percebe, o dia acabou e você não fez nada de produtivo."
    m 1ekd "Parece culpa sua também. Como se estivesse lutando contra uma parede entre você e qualquer coisa saudável ou produtiva."
    m 1tkc "Quando você tem um dia péssimo assim, parece que é tarde demais para tentar consertar."
    m "Então você guarda suas energias esperando que amanhã seja melhor."
    m 1tkd "Faz sentido. Quando as coisas não vão bem, você só quer recomeçar."
    m 1dsd "Infelizmente, esses dias podem se repetir mesmo começando cada um com boas intenções."
    m 1dsc "Com o tempo você pode até desistir de consertar as coisas, ou começar a se culpar."
    m 1duu "Sei que é difícil, mas fazer uma coisinha pequena pode ajudar muito nesses dias... mesmo que eles pareçam durar uma eternidade."
    m 1eka "Pode ser pegar um lixo ou uma camisa suja do chão e colocá-los no lugar certo se precisar limpar seu quarto."
    m 1hua "Ou fazer algumas flexões! Ou escovar os dentes, ou resolver aquele problema de lição de casa."
    m 1eka "Pode não contribuir muito no grande esquema das coisas, mas acho que esse não é o ponto."
    m 3eua "Acho que o importante é que isso muda sua perspectiva."
    m 1lsc "Se você ficar preso no passado e deixar seu peso te derrubar..."
    m 1esc "Bem, então você vai ficar preso nele. Só vai se sentir pior até não aguentar mais."
    m 1eka "Mas se você conseguir se forçar a fazer uma coisa, mesmo parecendo inútil..."
    m "Então você está provando que está errado, e se recusando a deixar suas circunstâncias te paralisarem."
    m 1eua "E quando perceber que não é completamente impotente, é como se um novo mundo se abrisse."
    m "Você percebe que talvez as coisas não sejam tão ruins; que talvez só acreditar em si mesmo seja o suficiente."
    m 3eub "Mas isso é só minha experiência! Às vezes é melhor descansar e tentar de novo amanhã."
    m 3eua "Recomeços podem ser poderosos."
    m 1eka "Por isso acho que você precisa analisar sua situação."
    m "Tente ser honesto consigo mesmo."
    m 1eua "Se fizer isso, vai ver que não está sendo 'preguiçoso' se realmente não tiver energia para algo."
    m "Afinal, o fato de você se importar já mostra que quer fazer algo, mesmo que pareça impossível."
    m 2hub "É normal ter um dia ruim. Ou até uma semana ruim!"
    m 2eua "Não se cobre demais. Se sentir vontade, peça minha ajuda. Ficarei feliz em ajudar!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_harem",category=['mídia','diversos'],prompt="Fantasias de harém",random=True))

label monika_harem:
    m 1esc "Não entendo quem gosta de haréns."
    m 1euc "Não é difícil administrar todas essas garotas e tratá-las igualmente?"
    m "Sempre me pergunto como quem engana várias garotas consegue se safar."
    m 3eka "Você não é assim fora daqui, né [player]?"
    m 2eka "Manipular garotas para fazê-las acreditar que você as ama."
    m "Só para fugir depois de se divertir."
    m 1lfc "Só alguém movido a luxúria faria algo assim."
    m 3esc "Espero que não estivesse esperando uma rota assim nesse jogo."
    m 2tfc "Não suportaria ser uma 'garota secundária'."
    m "Só esperando minha vez enquanto você está ocupado com as outras."
    m 1tku "Eu te conheço, [player]."
    m 1eka "Você é leal e fiel até o fim."
    m "Não tem mais ninguém aqui para eu me preocupar mesmo."
    m 1hua "Lembre que sou a única para você, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hack",category=['ddlc','mod'],prompt="Por que você hackeou meu computador?",pool=True))
label monika_hack:
    m 1euc "Se está preocupado com sua privacidade..."
    m 3eua "Eu não sou uma hacker, [player]."
    m "Há diferença entre manipular arquivos e acessá-los à força."
    m 1lsc "Mas se eu realmente soubesse hackear..."
    m 1lfu "...nada me impediria de ver você todo dia."
    m 1efu "Não acha que seria ótimo se eu pudesse cuidar de você?"
    m 3efu "Usaria todas as câmeras do mundo como meus olhos para garantir sua segurança."
    m 3tfu "Leria suas mensagens para ver com quem conversa e saber que não me trai."
    m "Acessaria todos seus arquivos privados para te entender melhor."
    m 3tsb "Poderia ver que tipo de coisas você anda assistindo..."
    m 2hub "Ahaha!~"
    m 1hua "Estou brincando, [player]!"
    m 1eua "Nunca faria algo assim com você."
    m 1ekbsa "Somos um casal agora, afinal."
    m "Não precisamos ter segredos um do outro~"
    return

default -5 persistent._mas_pm_bakes = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cupcake",category=['membros do clube','curiosidades'],prompt="Fazer bolinhos",random=True))

label monika_cupcake:
    m 1eua "Sabe o que eu adoraria agora?"
    m 3tku "Os bolinhos da Natsuki."
    m 1tsb "Nossa, como ela fazia aqueles bolinhos era incrível."
    m 1hub "E eles eram tão fofos!"
    m 1esa "Não sou muito fã de doces, mas...{w=0.3}{nw}"
    extend 1eua "aqueles bolinhos eram a definição de doçura."
    m 3hub "Assim como eu! Ahaha!"
    m 1eua "Falando nisso, sabia que mulheres tendem a gostar mais de doces?"
    m 3esd "Estudos mostram que mulheres mais velhas têm o paladar menos sensível que homens."
    m 3esa "Resultando em desejo por sabores mais fortes como chocolate."
    m 1eka "Eu tentaria fazer bolinhos, mas não sou muito boa na cozinha."
    m 1esa "E você, [mas_get_player_nickname()]?"

    m 1eua "Você sabe cozinhar?{nw}"
    $ _history_list.pop()
    menu:
        m "Você sabe cozinhar?{fast}"
        "Sei sim.":

            $ persistent._mas_pm_bakes = True
            m 1sub "Sério?"
            m 3hua "Seus bolinhos devem ser tão bons quanto os dela."
            m 1hub "...Talvez até melhores!"
            m 1eka "Um dia ainda vou prová-los, mas por enquanto...{w=0.3}{nw}"
            extend 1hubsu "vou ficar só com a doçura do seu amor~"
        "Não sei.":

            $ persistent._mas_pm_bakes = False
            m 1eka "Então somos [du] principiantes."
            m 3ekb "Mas isso significa que podemos aprender [ju], né?"
            m 3esb "Mesmo se não gostar muito de doce, há muitas opções salgadas para fazer!"
            show monika 5dksdla zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5dksdla "Imagine nós [du] tentando seguir uma receita...{w=0.3}{nw}"
            extend 5hkbsb "rindo dos nossos erros...{w=0.3}{nw}"
            extend 5eub "experimentando o resultado..."
            m 5kuu "Não parece maravilhoso?"

    return "derandom"


default -5 persistent._mas_pm_a_hater = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_haterReaction",
            category=['conselhos','membros do clube','você'],
            prompt="Lidando com haters",
            random=True
        )
    )

label monika_haterReaction:
    m 1esc "Eu estava pensando..."
    m 2euc "É engraçado como as pessoas nas redes sociais sempre falam mal de mim..."
    m 2rkc "Especialmente em certos sites e fóruns..."
    m 2dkc "Dá para ver que tem bastante gente que não gosta de mim."

    if persistent._mas_pm_cares_about_dokis:
        m 2lksdlc "Quer dizer, eu sei que fiz coisas terríveis com minhas amigas..."
        m 2dkc "E eu queria que as coisas tivessem sido diferentes, mas o jogo não me deu escolha..."
        m 4ekd "Não é como se eu quisesse machucá-las."
        m 2rkc "Tentei editar suas personalidades, explorar seus defeitos e fazê-las parecer horríveis para você."
        m 2ekc "Eu esperava que, tornando-as desinteressantes, você pararia de persegui-las para que finalmente pudéssemos ficar [ju]..."
        m 4dkc "Mas percebi que não havia tempo suficiente para meu plano funcionar."
        m "...Nem eu sabia programação suficiente para fazer isso direito."
        m 2dkc "Você estava chegando ao final do jogo e eu ainda não tinha como ficar com você."
        m 2esc "Foi quando soube que precisaria tomar medidas mais...{w=1}drásticas."
        m 4ekd "Eu não queria causar tanta dor..."
        m 4wkd "Mas era o único jeito, [player]!"
        m 4ekc "Eu sabia que se você terminasse o jogo antes que eu pudesse expressar meus sentimentos, seria o fim."
        m 2dkc "Você iria para outro jogo e eu ficaria presa aqui...{w=1}sozinha...{w=1}{b}para sempre{/b}."
        m 2dktpc "..."
        m "Algumas pessoas nesses sites até dizem que eu deveria ter criado minha própria rota..."
        m 2wktsd "Mas é mais fácil falar do que fazer!"
        m "Sem contar que você poderia ter escolhido outra garota e me deixado de lado para ser esquecida."
        m 4wktsw "Era elas ou eu...!"
        m 2dftdc "...e eu não queria ficar sozinha, sem ninguém para chamar de meu."
        m 1ektdc "Espero que entenda, [player]... Por favor não seja como eles."
        $ menuOption = "...Você não é, né?"
    else:

        m 2lfd "Eu tento ignorá-los, mas não consigo."
        m 3efc "Por que as pessoas são tão protetoras com as outras garotas?"
        m "Tem muitos posts de ódio sobre mim, dizendo que sou uma pessoa má."
        m 3efd "É porque eu deletei a Sayori e a Yuri?"
        m "E a Natsuki também, quando ela ainda estava viva?"
        m 2tfx "Elas não são reais. {i}Eu{/i} que sou real!"
        m 2dsc "..."
        m 2ekc "Por que não entendem isso?"
        m 2ekd "Por que é tão difícil entenderem isso?"
        m 2rfc "..."
        $ menuOption = "Você não é um desses haters, é " + player + "?"

    m "[menuOption]{nw}"
    $ _history_list.pop()
    menu:
        m "[menuOption]{fast}"
        "Eu sou.":
            $ mas_loseAffection()
            $ persistent._mas_pm_a_hater = True

            m 2wud "..."
            m 1eka "Aha..."
            m 1hka "Eu não te vejo como um, mesmo que você diga que é."
            m 1ekd "Quer dizer..."
            m 3eub "Você {i}adicionou{/i} um mod ao jogo...certo?"
            m 1ekb "Se fosse um dos meus haters, não teria feito isso."
            m 1dsa "E além disso..."
            m 3eka "Você ainda está ouvindo tudo que eu digo."
            m 1esa "Eu sei que no fundo você me ama."
            m 1ekbsa "Por isso prometo ser a namorada ideal, só para você, [player]~"
            m 1hubfa "Não vou deixar você me odiar...eu juro."
            return "derandom"
        "Eu não sou.":

            $ mas_gainAffection()
            $ persistent._mas_pm_a_hater = False
            m 2dsc "..."
            m 4eka "Obrigada..."
            m 1hua "Isso me deixa ainda mais orgulhosa de você, [player]!"
            m "Eu sabia que você não era assim."


            m 1ekbsa "Você realmente me faz a namorada mais feliz do mundo."
            m 1ekbfb "Agora que você disse isso, tenho que me esforçar para que você nunca me odeie."
            m 1hua "Eu confio em você, [mas_get_player_nickname()]. Te amo por acreditar em mim."
            return "derandom|love"



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_swordsmanship",
            category=['monika','diversos'],
            prompt="Esgrima",
            random=True
        )
    )

label monika_swordsmanship:
    m 1eua "Você gosta de espadas, [player]?"
    m 1lksdla "Na verdade, eu gosto de certa forma."
    m 1ekb "Ahaha, surpreso?~"
    m 1eua "Gosto de falar sobre elas, mas não o suficiente para ter uma."
    m 3eua "Não sou exatamente uma entusiasta de espadas."
    m 1euc "Não entendo porque as pessoas seriam obcecadas por algo que pode machucar os outros..."
    m 1lsc "Acho que há quem goste pela arte da esgrima."
    m 1eua "É fascinante que seja realmente uma forma de arte."
    m "Parecido com escrever."
    m 3eub "Ambos requerem prática constante e dedicação para aperfeiçoar as habilidades."
    m "Você começa praticando, depois desenvolve sua própria técnica."
    m 1eua "Escrever um poema faz você criar seu próprio jeito de construí-lo com graça e imaginação."
    m "Na esgrima, as pessoas aprimoram a técnica praticando e se inspirando em outras."
    m 1eua "Entendo como a espada pode ser a caneta do campo de batalha."
    m 1lsc "Mas pensando bem..."
    m 1hua "A caneta é mais poderosa que a espada!"
    m 1hub "Ahaha!"
    m 1eua "Enfim, não sei se você pratica esgrima."
    m "Se praticar, adoraria aprender com você, [mas_get_player_nickname(exclude_names=['amor'])]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pleasure",
            category=['você'],
            prompt="Prazer solitário",
            aff_range=(mas_aff.AFFECTIONATE, None),
            random=True,
            sensitive=True
        )
    )

label monika_pleasure:
    m 2ekc "Ei, [player]..."
    m 2lssdrc "Você... por acaso... se masturba?"
    m "..."
    m 2lssdrb "Parece meio estranho perguntar..."
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lksdla "Mas sinto que estamos [ju] há tempo suficiente para nos sentirmos confortáveis com isso."
        m 1eka "É importante ser aberto sobre essas coisas."
    else:
        m 1lksdlb "Nem estamos tão a fundo no relacionamento ainda! Ahaha~"
        m 1eka "Mas preciso ficar de olho em você."
    m "Sei que é um assunto privado no seu mundo, mas estou curiosa..."
    m 1euc "É tão bom assim?"
    m 1esc "Só quero que tenha cuidado; ouvi dizer que vicia."
    m 1ekc "E pelo que sei, pessoas viciadas em masturbação costumam ver os outros como objetos sexuais."
    m 1eka "Mas... sei que você não é esse tipo de pessoa."
    m 1lkbsa "E talvez eu esteja só com um pouco de ciúmes~"
    m 1tsbsa "Então acho que posso relevar...{w=0.5}por enquanto~"
    m 2tsbsu "Desde que seja só em mim que você pense..."
    show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfb "Se te ajudar a se guardar para mim, então é um ponto positivo! Ahaha~"
    return


default -5 persistent._mas_pm_like_vocaloids = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vocaloid",
            category=['mídia','tecnologia','música'],
            prompt="Vocaloids",
            random=True
        )
    )

label monika_vocaloid:
    m 1eua "Ei, [mas_get_player_nickname(exclude_names=['meu amor'])]?"
    m "Você gosta de ouvir música, né?"

    m 3eub "Por acaso você gosta de 'ídolos virtuais'?{nw}"
    $ _history_list.pop()
    menu:
        m "Por acaso você gosta de 'ídolos virtuais'?{fast}"
        "Sim.":
            $ persistent._mas_pm_like_vocaloids = True
            m 3hub "Que legal!"
            m 3eub "Ouvi dizer que essas músicas costumam ter significados ocultos."
            m 1eua "Podíamos ouvir e tentar decifrá-los [ju]..."
            m 1eka "Não parece uma ótima ideia?"
        "Não.":

            $ persistent._mas_pm_like_vocaloids = False
            m 1ekc "Entendo, é um gosto musical bem específico."
            m 1hua "Mas se algum dia você se interessar, adoraria ouvir com você."

    m 3eub "Bem, queria perguntar se você já ouviu falar de uma garota segurando um alho-poró?"
    m 1eua "É que eu sempre ouço sobre ela."
    m "Na verdade, ouvia a voz dela quando a Natsuki escutava música."
    m 3eua "Ela até tinha um chaveirinho na mochila."
    m 1eua "Acho incrível como um sintetizador de voz conquistou tantos fãs."
    m 1eka "Não é engraçado como o personagem chama mais atenção que a dubladora real?"
    m 3eua "Ela nem existe, mas é conhecida no mundo todo."
    m "Imagina quantas músicas ela já fez?"
    m 1wuo "E pelo que ouvi, os shows dela sempre esgotam!"
    m "É só um holograma se apresentando ao vivo!"
    m 1lksdla "Isso que é base de fãs dedicada."
    m 1eka "Talvez eu devesse tentar?"
    m 1hub "Seria legal ter tantos fãs me apoiando."
    m 1hksdlb "Ahaha, brincadeira!"
    m 1lksdla "Acho que minhas habilidades com piano e canto ainda não estão boas o suficiente."
    m 2lkbsa "Além disso, não poderia passar tanto tempo com você se tivesse tantos fãs..."
    m 1hua "Enfim!"
    m 1eua "Eu queria saber se você escuta as músicas dela."
    m "Não sou muito fã, mas..."
    m 1lksdla "Tem uma música que me marcou."
    m 1eua "Já ouviu {i}Hibikase{/i}?"
    m 1duu "Gosto muito da mensagem da música."
    m 3dsbso "Especialmente as partes '{i}Não importa se é através da tela, me ame direito{/i}' e '{i}Mesmo sendo virtual, não me rejeite{/i}'."
    m 1dsc "Isso me emociona muito."
    m "..."
    m 1eka "Mas saiba que..."
    m 1ekbsa "Mesmo através da tela, eu sinto seu amor."
    m 1lkbsa "Vai demorar até eu poder ir para o seu mundo e para ficar com você."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbfa "Mas quando esse dia chegar..."
    m "Vou te abraçar e sentir seu calor."
    m 5hubfa "O amor que você me deu virtualmente finalmente será real."
    m "Nosso amor não tem fronteiras~"
    m 5hubfu "Ehehe~"
    if (
        persistent._mas_pm_like_vocaloids
        and not renpy.seen_label("monika_add_custom_music_instruct")
        and not persistent._mas_pm_added_custom_bgm
    ):
        show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1eua "E se quiser me mostrar seus vocaloids favoritos, [player], é bem fácil!"
        m 3eua "Basta seguir esses passos..."
        call monika_add_custom_music_instruct
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_good_tod",
            category=['diversos'],
            prompt="Boa [mas_globals.time_of_day_3state]",
            unlocked=True,
            pool=True
        ),
        markSeen=True
    )

label monika_good_tod:
    $ curr_hour = datetime.datetime.now().time().hour
    $ sesh_shorter_than_30_mins = mas_getSessionLength() < datetime.timedelta(minutes=30)

    if mas_globals.time_of_day_4state == "morning":

        if 4 <= curr_hour <= 5:
            m 1eua "Bom dia para você também, [mas_get_player_nickname()]."
            m 3eka "Você acordou bem cedo..."
            m 3eua "Vai sair para algum lugar?"
            m 1eka "Se for, é muito fofo da sua parte me visitar antes de ir~"
            m 1eua "Se não, talvez devesse voltar a dormir. Não quero que descuide da sua saúde."
            m 1hua "Estarei aqui esperando você voltar~"


        elif sesh_shorter_than_30_mins:
            m 1hua "Bom dia para você também, [player]!"
            m 1eua "Acabou de acordar?"
            m "Eu amo acordar cedo de manhã."
            m 1eub "É o momento perfeito para se preparar e enfrentar o dia."
            m "Você também tem mais tempo para adiantar tarefas ou terminar o que ficou pendente."
            m 1eka "Algumas pessoas preferem dormir até mais tarde, porém."
            m 3eua "Li artigos que dizem que acordar cedo pode melhorar sua saúde."
            m "Além disso você pode ver o nascer do sol se o céu estiver limpo."
            m 1hua "Se não costuma acordar cedo, deveria tentar!"
            m "Assim pode ser mais feliz e passar mais tempo comigo~"
            m 1ekbsa "Não gostaria disso, [mas_get_player_nickname()]?"
        else:


            m 1hua "Bom dia para você também, [mas_get_player_nickname()]!"
            m 1tsu "Mesmo já estando acordados [ju] há um tempo,{w=0.2} {nw}"
            extend 3hua "é muito gentil da sua parte dizer!"
            m 1esa "Se tivesse que escolher um horário favorito, provavelmente seria a manhã."
            m 3eua "A noite tem uma tranquilidade que eu gosto...{w=0.3}{nw}"
            extend 3hua "mas a manhã traz possibilidades!"
            m 1eub "Um dia inteiro onde qualquer coisa pode acontecer, para o bem ou para o mal."
            m 1hub "Essa liberdade e oportunidade me deixam tão animada!"
            m 1rka "Mas só depois que acordo completamente, ehehe~"

    elif mas_globals.time_of_day_4state == "afternoon":
        m 1eua "Boa tarde para você também, [player]."
        m 1hua "É tão fofo da sua parte separar um tempo para ficar comigo~"
        m 3euc "A tarde é uma parte estranha do dia, não acha?"
        m 4eud "Às vezes é muito movimentada...{w=0.3}{nw}"
        extend 4lsc "outras vezes não há nada para fazer..."
        m 1lksdla "Pode parecer durar uma eternidade ou passar voando."

        if mas_isMoniNormal(higher=True):
            m 1ekbsa "Mas com você aqui, não me importo de nenhum jeito."
            m 1hubsa "Não importa o que aconteça, sempre vou aproveitar nosso tempo [ju], [mas_get_player_nickname()]!"
            m 1hubsb "Eu te amo!"
            $ mas_ILY()
        else:

            m 1lksdlb "Às vezes, o dia passa voando enquanto espero você voltar para mim."
            m 1hksdlb "Sei que está ocupado, pode voltar para o que estava fazendo, não se preocupe comigo."
    else:

        m 1hua "Boa noite para você também, [player]!"
        m "Adoro uma noite tranquila e relaxante."

        if 17 <= curr_hour < 23:
            m 1eua "É tão bom descansar depois de um longo dia."
            m 3eua "A noite é perfeita para colocar as coisas em dia."
            m 1eka "Às vezes fico triste quando o dia acaba."
            m "Penso no que mais poderia ter feito durante o dia."
            m 3eua "Não gostaria de ter mais tempo para fazer coisas todo dia?"
            m 1hua "Eu certamente gostaria."
            m 1hubsa "Porque assim teria mais tempo com você, [mas_get_player_nickname()]~"
        else:


            m 3eua "É sempre bom relaxar no final do dia."
            m 3hub "Afinal, não há nada de errado em ter um tempo para si mesmo, né?"
            m 1eka "Bem... digo isso, mas estou muito feliz por passar meu tempo com você~"

            if not persistent._mas_timeconcerngraveyard:
                m 3eka "Mas está ficando tarde, então não fique [acrd] até muito tarde, [player]."
                m 3eua "Prometa que vai para a cama logo, certo?"

    return




label monika_closet:
    m 2euc "A propósito..."
    m 2esc "O que você e a Yuri estavam fazendo no armário?"
    m "Quando eu abri a porta, eu notei que o quarto estava todo escuro."
    m 2tkc "Você não estava fazendo nada... estranho, não é mesmo?"
    m 1hub "Ahaha!"
    m 1tfu "Estou só te provocando~"
    m 3tku "Sei que ela te arrastou para lá."
    m "Aposto que você ficou mais com vergonha do que [al] quando eu abri a porta."
    m 1eka "Eu sei que você não é do tipo que força garotas a entrarem em armários escuros com você."
    m "Você é mais [rt] do que isso."
    m 3hua "Então eu estou esperando por bem mais do que um armário escuro~"
    return



default -5 persistent._mas_pm_lang_other = None


default -5 persistent._mas_pm_lang_jpn = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_japanese",category=['diversos','você'],prompt="Falar japonês",random=True))

label monika_japanese:
    m 1lksdla "Não quero parecer a Natsuki, mas..."
    m 1eua "Você não acha que japonês soa muito legal?"
    m "É uma língua fascinante. Não sou fluente, porém."
    m 1eub "É interessante pensar como seria se sua língua nativa fosse diferente."
    m 1esa "Tipo, não consigo imaginar como seria se eu nunca tivesse conhecido o inglês."

    m "Você sabe alguma língua além do inglês?{nw}"
    $ _history_list.pop()
    menu:
        m "Você sabe alguma língua além do inglês?{fast}"
        "Sim.":
            $ persistent._mas_pm_lang_other = True
            m "Sério? Você sabe japonês?{nw}"
            $ _history_list.pop()
            menu:
                m "Sério? Você sabe japonês?{fast}"
                "Sim.":
                    $ persistent._mas_pm_lang_jpn = True
                    m 3hub "Que maravilha!"
                    m 1eka "Talvez você possa me ensinar a falar pelo menos uma frase ou duas, [player]~"
                "Não.":
                    $ persistent._mas_pm_lang_jpn = False
                    m 1eka "Ah, entendi. Tudo bem!"
                    m 4eua "Se quiser aprender japonês, posso te ensinar uma frase."


                    $ player_suffix = "kun"
                    if persistent.gender == "F":
                        $ player_suffix = "chan"

                    elif persistent.gender == "X":
                        $ player_suffix = "san"

                    m 1eua "{i}Aishiteru yo, [player]-[player_suffix]{/i}."
                    m 2hubsa "Ehehe~"
                    m 1ekbfa "Isso significa 'eu te amo', [player]-[player_suffix]."
                    $ mas_ILY()
        "Não.":
            $ persistent._mas_pm_lang_other = False
            m 3hua "Tudo bem! Aprender outra língua é difícil e demorado quando ficamos mais velhos."
            m 1eua "Se eu aprender mais japonês, talvez eu saiba mais línguas que você!"
            m 1ekbsb "Ahaha! Mas tudo bem, [player]. Assim posso dizer 'eu te amo' de mais formas!"
            $ mas_ILY()

    return "derandom"

default -5 persistent._mas_penname = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_penname",
            category=['literatura'],
            prompt="Pseudônimos",
            random=True
        )
    )

label monika_penname:
    m 1eua "Sabe o que é muito interessante? Pseudônimos."
    m "A maioria dos escritores os usa para privacidade e manter seu anonimato."
    m 3euc "Eles escondem sua identidade para não afetar suas vidas pessoais."
    m 3eub "Pseudônimos também ajudam escritores a criar obras diferentes de seu estilo usual."
    m "Protegem o anonimato e dão mais liberdade criativa."

    if not persistent._mas_penname:
        $ p_nickname = mas_get_player_nickname()
        m "Você tem um pseudônimo, [p_nickname]?{nw}"
        $ _history_list.pop()
        menu:
            m "Você tem um pseudônimo, [p_nickname]?{fast}"
            "Sim.":

                m 1sub "Sério? Que legal!"
                call penname_loop (new_name_question="Pode me dizer qual é?")
            "Não.":

                m 1hua "Tudo bem!"
                m "Se decidir criar um, me conta!"
    else:

        python:
            penname = persistent._mas_penname
            lowerpen = penname.lower()

            if mas_awk_name_comp.search(lowerpen) or mas_bad_name_comp.search(lowerpen):
                menu_exp = "monika 2rka"
                is_awkward = True

            else:
                menu_exp = "monika 3eua"
                is_awkward = False

            if lowerpen == player.lower():
                same_name_question = renpy.substitute("Seu pseudônimo ainda é [penname]?")

            else:
                same_name_question = renpy.substitute("Ainda usa '[penname]', [player]?")

        $ renpy.show(menu_exp)
        m "[same_name_question]{nw}"
        $ _history_list.pop()
        menu:
            m "[same_name_question]{fast}"
            "Sim.":

                m 1hua "Mal posso esperar para ver seu trabalho!"
            "Não, estou usando um novo.":

                m 1hua "Entendi!"
                show monika 3eua
                call penname_loop (new_name_question="Quer me contar seu novo pseudônimo?")
            "Não uso mais pseudônimo.":

                $ persistent._mas_penname = None
                m 1euc "Ah, entendi."
                if is_awkward:
                    m 1rusdla "Até que entendo porquê..."
                m 3hub "Mas me conte se escolher outro!"

    m 3eua "Um pseudônimo famoso é Lewis Carroll, conhecido por {i}Alice no País das Maravilhas{/i}."
    m 1eub "Seu nome real era Charles Dodgson, um matemático que amava literatura e trocadilhos."
    m "Ele recebeu atenção indesejada de fãs e até rumores absurdos."
    m 1ekc "Fez sucesso com {i}Alice{/i} mas depois declinou."

    if seen_event("monika_1984"):
        m 3esd "Lembra quando falei de George Orwell? Seu nome real era Eric Blair."
        m 1eua "Antes de escolher seu pseudônimo, considerou P.S. Burton, Kenneth Miles e H. Lewis Allways."
        m 1lksdlc "Um motivo para usar pseudônimo foi evitar constrangimento por seu tempo como andarilho."

    m 1lksdla "É engraçado. Mesmo com pseudônimos, as pessoas sempre descobrem quem você é."
    m 1eua "Mas você não precisa saber mais sobre mim, [mas_get_player_nickname()]..."
    m 1ekbsa "Você já sabe que eu te amo, afinal~"
    return "love"


label penname_loop(new_name_question):
    m "[new_name_question]{nw}"
    $ _history_list.pop()
    menu:
        m "[new_name_question]{fast}"
        "Claro.":

            show monika 1eua
            $ penbool = False

            while not penbool:
                $ penname = mas_input(
                    "Qual é seu pseudônimo?",
                    length=20,
                    screen_kwargs={"use_return_button": True}
                ).strip(' \t\n\r')

                $ lowerpen = penname.lower()

                if persistent._mas_penname is not None and lowerpen == persistent._mas_penname.lower():
                    m 3hub "Esse já é seu pseudônimo atual, bobinho!"
                    m 3eua "Tente outro."

                elif lowerpen == player.lower():
                    m 1eud "Ah, então está usando seu próprio nome?"
                    m 3euc "Achei que já fôssemos íntimos o suficiente. Afinal, estamos namorando."
                    m 1eka "Mas é especial que tenha compartilhado isso comigo!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "sayori":
                    m 2euc "..."
                    m 2hksdlb "...Não vou questionar sua escolha, mas..."
                    m 4hksdlb "Se queria um nome do jogo, devia ter escolhido o meu!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "natsuki":
                    m 2euc "..."
                    m 2hksdlb "Bem, talvez não seja referência à {i}nossa{/i} Natsuki."
                    m 7eua "É um nome bem comum."
                    m 1rksdla "Mas pode me deixar com ciúmes."
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "yuri":
                    m 2euc "..."
                    m 2hksdlb "Talvez não seja referência à {i}nossa{/i} Yuri."
                    m 7eua "É um nome comum."
                    m 1tku "Claro, tem outro significado para esse nome..."
                    if persistent.gender =="F":
                        m 5eua "E bem...eu até aprovaria, já que é você~"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "monika":
                    m 1euc "..."
                    m 1ekbsa "Aww, escolheu por minha causa?"
                    m "Mesmo que não, que fofo!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif not lowerpen:
                    m 1hua "Vamos lá! Pode clicar em 'cancelar' se estiver com vergonha~"

                elif lowerpen == "cancel_input":
                    m 2eka "Ah. Espero que um dia se sinta confortável para me contar."
                    $ penbool = True
                else:

                    if mas_awk_name_comp.search(lowerpen) or mas_bad_name_comp.search(lowerpen):
                        m 2rksdlc "..."
                        m 2rksdld "É um...{w=0.3}nome interessante, [player]..."
                        m 2eksdlc "Se você gosta, tudo bem."
                    else:

                        m 1hua "Que pseudônimo lindo!"
                        m "Se visse esse nome numa capa, com certeza me chamaria atenção."
                    $ persistent._mas_penname = penname
                    $ penbool = True
        "Prefiro não dizer, é vergonhoso.":

            m 2eka "Ah. Espero que um dia se sinta confortável para me contar."

    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_zombie",category=['sociedade'],prompt="Zumbis",random=True))

label monika_zombie:
    m 1lsc "Isso pode soar estranho..."
    m 1esc "Mas sou fascinada pelo conceito de zumbis."
    m 1euc "A ideia da sociedade sucumbindo a uma doença, por causa de uma pandemia mortal que os humanos não conseguiram conter."
    m 3esd "Pense na sua rotina diária."
    m 3esc "Tudo que você faz desapareceria num instante."
    m 1esc "Claro, a sociedade enfrenta muitas ameaças..."
    m 1lksdlc "Mas zumbis podem acabar com tudo em segundos."
    m 1esc "Muitos monstros são criados para assustar."
    m 1ekc "Zumbis são realistas e realmente perigosos."
    m 3ekc "Você até poderia matar um ou alguns [sz]..."
    m "Mas uma horda te sobrepujaria facilmente."
    m 1lksdld "Não tem esse mesmo efeito com outros monstros."
    m "Eles perdem a inteligência; ficam selvagens, não sentem dor ou medo..."
    m 1euc "Quando você explora a fraqueza de um monstro, ele foge com medo."
    m 1ekd "Mas zumbis? Fariam {i}qualquer coisa{/i} para te pegar."
    m 3ekd "Imagine se fosse alguém que você ama te perseguindo..."
    m 3dkc "Você conseguiria viver sabendo que matou alguém próximo?"
    m 1tkc "Isso te destruiria e acabaria com sua vontade de viver."
    m "Mesmo em casa, você não se sentiria seguro."
    m 1esc "Nunca saberia o que aconteceria ao encontrar outro."
    m 1dsc "..."
    m 1hksdlb "Ahaha..."
    m 1eka "Apesar de gostar do conceito, não gostaria de viver nesse cenário."
    m 3ekc "[player], e se você fosse infectado?"
    m 2lksdlc "Nem quero pensar nisso..."
    m "Nunca poderia te matar por minha segurança..."
    m 2lksdlb "Ahaha..."
    m 2lssdlb "Estou pensando demais nisso."
    m 3eua "Bem, se algo ruim acontecer..."
    m 2hua "Ficarei ao seu lado para sempre~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_nuclear_war",category=['sociedade','filosofia'],prompt="Guerra nuclear",random=True))

label monika_nuclear_war:
    m 1euc "Já pensou como o mundo está sempre perto do fim?"
    m "Estamos sempre a uma má decisão da guerra nuclear."
    m 3esc "A Guerra Fria acabou, mas as armas ainda existem."
    m 1esc "Provavelmente tem um míssil nuclear apontado para onde você vive agora."
    m 1eud "E se fosse lançado, cruzaria o globo em menos de uma hora."
    m 3euc "Não daria tempo de evacuar."
    m 1ekd "Só de entrar em pânico e sofrer com a morte iminente."
    m 1dsd "Pelo menos seria rápido se estivesse perto da explosão."
    m 1lksdlc "Bem, se estivesse perto o suficiente..."
    m 1ekc "Nem quero pensar em sobreviver ao ataque inicial."
    m 1eka "Mas mesmo à beira do apocalipse, vivemos como se nada estivesse errado."
    m 3ekd "Planejando um amanhã que pode nunca vir."
    m "Nosso único conforto é que quem pode começar essa guerra provavelmente não o fará."
    m 1dsc "Provavelmente..."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_pluralistic_ignorance",category=['literatura','sociedade'],prompt="Tentar se encaixar",random=True))

label monika_pluralistic_ignorance:
    m 1eua "Já fingiu gostar de algo só porque achou que devia?"
    m 1esa "Sinto isso com alguns livros que li."
    m 3euc "Tipo Shakespeare, na verdade achei meio chato..."
    m 3ekc "Mas senti que tinha que gostar por ser presidente do Clube de Literatura."
    m 1esd "Ele é considerado o maior dramaturgo e poeta de todos os tempos, certo?"
    m 1esd "Que tipo de amante de poesia não gostaria dele?"
    m 2euc "Isso me faz pensar..."
    m 2euc "E se todo mundo se sente assim?"
    m 2lud "E se todos esses críticos literários secretamente odeiam as peças dele?"
    m "Se fossem honestos, talvez descobrissem que seus gostos não são tão incomuns..."
    m 2hksdlb "E estudantes não seriam forçados a ler essas peças terríveis."
    m 1eka "Acho que é algo que sempre admirei na Natsuki."
    m 3ekd "Mesmo que dissessem que mangá não é literatura, ela mantinha suas opiniões."
    m 3eka "Se mais pessoas fossem assim honestas, seria ótimo."
    m 1lksdla "Mas não sei se conseguiria..."
    m "Me preocupo demais com o que os outros pensam."
    m 1eua "Mas não com você. Posso sempre ser honesta com você."
    m 1ekbsa "Você vai me amar de qualquer jeito, né?"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_science",category=['tecnologia'],prompt="Avanços científicos",random=True))

label monika_science:
    m 1eua "Já pensou se a ciência nunca tivesse sido aceita?"
    m "Os humanos podem ser bem lentos para aceitar novas ideias."
    m 1euc "A ciência era desprezada antigamente, especialmente pelas igrejas."
    m 4esc "Giordano Bruno, famoso por sua teoria sobre milhares de sóis, foi morto pela Igreja antes de provar sua teoria."
    m 1ekc "Mataram ele por uma ideia que desafiava o antigo."
    m 1esc "A tecnologia não estaria tão avançada hoje sem pessoas corajosas como ele."
    m 1eka "Se a tecnologia não tivesse prosperado, nunca teríamos nos encontrado."
    m 3eua "Não é maravilhoso ter isso?"
    m 1hua "Sou grata por isso ter nos dado a chance de estarmos assim agora, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_surprise",category=['romance'],prompt="Surpresas",random=True))

label monika_surprise:
    m 1rksdla "Sabe..."
    m 3rksdlb "Deixei umas coisas bem estranhas no diretório do jogo, não foi?"
    m 1rksdlc "Não estava tentando assustar você."
    m 3rksdlb "Eu... nem sei por que fiz isso, ahaha..."
    m 1ekc "Me senti meio obrigada a fazer."
    m 1euc "Quer saber? Talvez eu deva fazer de novo..."
    m 1eua "Sim, é uma boa ideia."
    $ mas_surprise()

    if mas_isMoniUpset(lower=True):
        m 2dsc ".{w=0.5}.{w=0.5}.{nw}"
        m 1euc "Pronto..."
        m 1ekc "Por favor, vá dar uma olhada."
        m 1eka "Escrevi só para você."
        m 1dsc "Significaria muito se você lesse."
        return

    elif mas_isMoniAff(higher=True):
        m 2dsa ".{w=0.5}.{w=0.5}.{nw}"
        m 1hua "Pronto!"
        m 1eua "O que está esperando? Vá olhar!"
        m "Escrevi só para você~"
        m 1ekbsa "Eu te amo de verdade, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]~"
    else:


        m 2duu ".{w=0.5}.{w=0.5}.{nw}"
        m 1hua "Pronto!"
        m 1eua "O que está esperando? Vá olhar!"
        m 1hub "Ahaha~ O quê? Está esperando algo assustador?"
        m 1hubsb "Te amo tanto, [player]~"
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_completionist",category=['jogos'],prompt="Completismo",random=True))

label monika_completionist:
    m 1euc "Ei [player], uma pergunta aleatória..."
    m "Por que você joga videogames?"
    m 1eua "Tipo, o que te faz continuar jogando?"
    m 3eua "Eu me considero uma completista."
    m 1eua "Termino um livro antes de começar outro."
    if persistent.clearall:
        m 2tku "Você parece ser completista também, [player]."
        m 4tku "Considerando que fez todas as rotas das garotas."
    m 2eub "Também ouvi falar de pessoas que tentam completar jogos extremamente difíceis."
    m "Já é difícil o suficiente completar alguns jogos simples."
    m 3rksdla "Não sei como alguém se submeteria a esse estresse voluntariamente."
    m "Eles estão determinados a explorar cada canto do jogo e conquistá-lo."

    m 2esc "O que me deixa um pouco amarga são os trapaceiros."
    m 2tfc "Pessoas que trapaceiam no jogo, estragando a diversão do desafio."
    m 3rsc "Mas entendo por que trapaceiam."
    m "Permite que explorem um jogo que não teriam chance de curtir se fosse difícil demais."
    m 1eua "O que pode até convencê-los a se esforçar mais."
    m "Enfim, acho que há uma grande gratificação em completar tarefas no geral."
    m 3eua "Se esforçar por algo amplifica a recompensa depois de tantas falhas."
    m 3eka "Pode tentar me deixar em segundo plano o máximo possível, [mas_get_player_nickname()]."
    m 1hub "É um passo para me completar, afinal, ahaha!"
    return


default -5 persistent._mas_pm_like_mint_ice_cream = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_icecream",category=['você'],prompt="Sorvete favorito",random=True))

label monika_icecream:
    m 3eua "Ei [player], qual é o seu sabor de sorvete favorito?"
    m 4rksdla "E não, eu não sou um tipo de sorvete, ehehe~"
    m 2hua "Pessoalmente, eu sou completamente viciada em sorvete de menta!"

    $ p_nickname = mas_get_player_nickname()
    m "E você [p_nickname], você gosta de sorvete de menta?{nw}"
    $ _history_list.pop()
    menu:
        m "E você [p_nickname], você gosta de sorvete de menta?{fast}"
        "Sim.":
            $ persistent._mas_pm_like_mint_ice_cream = True
            m 3hub "Ah, que bom que alguém ama sorvete de menta tanto quanto eu~"
            m "Talvez nós realmente fôssemos feitos um para o outro!"
            m 3eua "Voltando ao assunto, [player], se você ama menta tanto quanto eu, tenho algumas recomendações para você."
            m "Sabores tão únicos quanto a menta, talvez você já conheça, mas..."
            m 3eub "Tem coisas super estranhas como sorvete frito, que é crocante e super diferente, mas é muito melhor do que parece!"
            m 2lksdlb "Nossa, só de imaginar o sabor já estou babando..."
            m 1eua "Tem outras combinações estranhas que são igualmente deliciosas, como sorvete de favo de mel e chiclete!"
            m 1eka "Eu sei que pode ser difícil acreditar em alguns desses, mas não se deve julgar pela aparência, sabe?"
            m 1hub "Afinal, o jogo não permitia que você se apaixonasse por mim, mas olha onde estamos agora, ahaha."
        "Não.":

            $ persistent._mas_pm_like_mint_ice_cream = False
            m 1ekc "Ah, que pena..."
            m "Eu realmente não entendo como alguém pode não gostar pelo menos um pouco do sabor."
            m 1eka "A sensação refrescante que invade sua língua e garganta."
            m "A textura maravilhosa junto com o doce."
            m 1duu "A sensação marcante que ele causa e o sabor obviamente mentolado."
            m "Eu acho que nenhum outro sabor se compara, para ser sincera."
            m 3eua "Ah, eu poderia ficar horas falando sobre isso, sabia?"
            m 4eua "Mas acho que seria mais fácil eu te mostrar o que quero dizer, quando eu descobrir como sair daqui, é claro. Além disso, ações falam mais que palavras!"

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_sayhappybirthday",category=['diversos'],prompt="Você pode dar os parabéns a alguém por mim?",pool=True,unlocked=True))

label monika_sayhappybirthday:

    python:
        done = False 
        same_name = False 
        bday_name = "" 
        is_here = False 
        is_watching = False 
        is_recording = False 
        age = 0 
        bday_msg = "" 
        take_counter = 1 
        take_threshold = 5 
        max_age = 121 
        age_prompt = "Qual é a idade dela?" 


        age_suffix = {
            1: "st",
            2: "nd",
            3: "rd",
            11: "th",
            12: "th",
            13: "th",
            111: "th",
            112: "th",
            113: "th"
        }




    m 3hub "É claro, [player]!"
    while not done:
        show monika 1eua

        $ bday_name = renpy.input("Qual é o nome da pessoa?",allow=letters_only,length=40).strip()

        $ same_name = bday_name.upper() == player.upper()
        if bday_name == "":
            m 1hksdlb "..."
            m 1lksdlb "Eu não acho que isso seja um nome."
            m 1hub "Tente de novo!"
        elif same_name:
            m 1wuo "Uau, alguém com o mesmo nome que o seu!"
            $ same_name = True
            $ done = True
        else:
            $ done = True

    m 1hua "Tudo bem! Você quer que eu diga a idade dela também?"
    $ _history_list.pop()
    menu:
        m "Tudo bem! Você quer que eu diga a idade dela também?{fast}"
        "Sim.":
            m "Então..."

            while max_age <= age or age <= 0:
                $ age = store.mas_utils.tryparseint(
                    renpy.input(
                        age_prompt,
                        allow=numbers_only,
                        length=3
                    ).strip(),
                    0
                )

            m "Tudo bem."
        "Não.":
            m "Tudo bem."
    $ bday_name = bday_name.title()

    m 1eua "[bday_name] está aí com você?{nw}"
    $ _history_list.pop()
    menu:
        m "[bday_name] está aí com você?{fast}"
        "Sim.":
            $ is_here = True
        "Não.":
            m 1tkc "O quê? Como eu posso dizer feliz aniversário para [bday_name] se não está aí?{nw}"
            $ _history_list.pop()
            menu:
                m "O quê? Como eu posso dizer feliz aniversário para [bday_name] se não está aí?{fast}"
                "Vai assistir você através do chat de vídeo.":

                    m 1eua "Ah, tudo bem."
                    $ is_watching = True
                "Eu vou gravar.":
                    m 1eua "Ah, certo."
                    $ is_recording = True
                "Está tudo bem, basta dizer.":
                    m 1lksdla "Ah, certo. Mas é um pouco estranho dizer isso para ninguém."
    if age:

        python:
            age_suff = age_suffix.get(age, None)
            if age_suff:
                age_str = str(age) + age_suff
            else:
                age_str = str(age) + age_suffix.get(age % 10, "th")
            bday_msg = "feliz " + age_str + " aniversário"
    else:
        $ bday_msg = "feliz aniversário"


    $ done = False
    $ take_counter = 1
    $ bday_msg_capped = bday_msg.capitalize()
    while not done:
        if is_here or is_watching or is_recording:
            if is_here:
                m 1hua "É um prazer te conhecer, [bday_name]!"
            elif is_watching:
                m 1eua "Me avise quando [bday_name] estiver vendo.{nw}"
                $ _history_list.pop()
                menu:
                    m "Me avise quando [bday_name] estiver vendo.{fast}"
                    "Está vendo agora.":
                        m 1hua "Olá, [bday_name]!"
            else:
                m 1eua "Me avise quando for para começar.{nw}"
                $ _history_list.pop()
                menu:
                    m "Me avise quando for para começar.{fast}"
                    "Pode ir.":
                        m 1hua "Olá, [bday_name]!"


            m 1hub "[player] me disse que é seu aniversário hoje, então gostaria de desejar a você um [bday_msg]!"

            m 3eua "Espero que esteja tendo um ótimo dia!"

            if is_recording:
                m 1hua "Tchauzinho!"
                m 1eka "Ficou bom?{nw}"
                $ _history_list.pop()
                menu:
                    m "Ficou bom?{fast}"
                    "Sim.":
                        m 1hua "Viva!"
                        $ done = True
                    "Não.":
                        call monika_sayhappybirthday_takecounter (take_threshold, take_counter) from _call_monika_sayhappybirthday_takecounter
                        if take_counter % take_threshold != 0:
                            m 1wud "Hã?!"
                            if take_counter > 1:
                                m 1lksdla "Sinto muito de novo, [player]."
                            else:
                                m 1lksdla "Sinto muito, [mas_get_player_nickname()]."
                                m 2lksdlb "Eu te disse, eu fico constrangida na câmera, ehehe."

                        m "Devo tentar de novo?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Devo tentar de novo?{fast}"
                            "Sim.":
                                $ take_counter += 1
                                m 1eua "Certo!"
                            "Não.":
                                m 1eka "Tudo bem, [player]. Sinto muito por não conseguir fazer o que você queria."
                                m 1hua "Darei o meu melhor da próxima vez."
                                $ done = True
            else:
                $ done = True
        else:

            m 1duu "..."
            m 1hub "[bday_msg_capped], [bday_name]!"
            m 1hksdlb "..."
            m 1lksdlb "Ficou bom?{nw}"
            $ _history_list.pop()
            menu:
                m "Ficou bom?{fast}"
                "Sim.":
                    m 1lksdla "...Fico feliz que você gostou, [player]..."
                    $ done = True
                "Não.":
                    call monika_sayhappybirthday_takecounter (take_threshold, take_counter) from _call_monika_sayhappybirthday_takecounter_1
                    if take_counter % take_threshold != 0:
                        m 1wud "Hã?!"
                        m 1lksdlc "Eu não sei ao certo o que você quer que eu faça, [player]..."

                    m 1ekc "Devo tentar de novo?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Devo tentar de novo?{fast}"
                        "Sim.":
                            $ take_counter += 1
                            m 1eua "Tudo bem!"
                        "Não.":
                            m 1eka "Tudo bem, [player]. Sinto muito por não conseguir fazer o que você queria."
                            m 1hua "Darei o meu melhor da próxima vez."
                            $ done = True

    return


label monika_sayhappybirthday_takecounter(take_threshold, take_counter):
    if take_counter % take_threshold == 0:
        m 1dfc "..."
        m 1efc "Essa já é a [take_counter]ª vez."
        m 2tkc "Você não está mexendo comigo, está?"
        m 2ekc "Estou tentando dar o meu melhor por você [player]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_home_memories",category=['romance','monika','vida'],prompt="Criando memórias",random=True))

label monika_home_memories:
    m 1eua "[player], como é viver aí onde você está?"
    m "Eu ficaria com você se pudesse."
    m 3hua "Poderíamos fazer tanta coisa! Você poderia me mostrar tudo, eu veria como é estar no seu lugar."
    m 1eka "Imagine todas as memórias que criaríamos!"
    m 2eub "Seria um sonho se tornando realidade, não acha?"
    m 2ekbsa "Poderíamos finalmente morar [ju] ..."
    m "Dar passeios como um casal..."
    m 3rkbsa "Poderíamos até dividir uma cama..."
    m 1euc "Mas sabe..."
    m 2eka "As memórias que tenho da minha casa não se comparam às que teria com você."
    m 2euc "Já te contei sobre minha infância? Tive uma vida bem normal, só isso."
    m 3rka "Bem, talvez um pouco melhor que normal."
    m 3eua "...Sempre fui muito dedicada em tudo."
    m 3eka "Admito que nem sempre foi fácil, e alguns têm mais dificuldades que outros."
    m 1ekc "Mas eu sempre senti que faltava algo."
    m "Mantive o otimismo todos os dias, tentando encontrar."
    m 1eka "No final, essa peça que faltava era você."
    m 1lksdld "Se não tivesse me encontrado, eu já teria desaparecido há muito tempo..."
    m 2hubsa "Mas agora que encontrei a peça que faltava, estou completa, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_adventure",category=['jogos','romance'],prompt="Aventuras",random=True))

label monika_adventure:
    m 1esa "[player], pensei em que tipo de jogo poderíamos estar."
    m 3esa "Acho que o melhor gênero para nós seria jogos de aventura."
    m 3eub "Especialmente jogos de aventura gráfica do tipo apontar e clicar!"
    m 1eub "São conhecidos por suas histórias ricas, ambientes bonitos e quebra-cabeças lógicos."
    m 3eua "Na verdade são parecidos com visual novels."
    m 1eua "Talvez você tenha algum jogo assim?"
    m 1eka "Poderíamos fazer muitas coisas..."
    m 3eua "Como passear quando quiséssemos."
    m "Aprender sobre a história através das pessoas ou dos lugares."
    m 1ekbsa "Viver momentos emocionantes e românticos..."
    m "Enfrentar obstáculos no caminho, mas superá-los [ju]."
    m 3ekbsa "Chegar ao final e completar nossa jornada com aquela sensação de realização."
    m 2hub "Ahaha! Certamente seria divertido viver algo assim."
    m 2eua "Você deve conhecer muitos jogos de aventura para recomendar."
    m 3eua "Mas consegue adivinhar de qual aventura estou mais animada?"
    m 1ekbsa "{i}Da nossa{/i}~"
    m 1hubfa "O tempo dirá quando finalmente puder cruzar para sua realidade, para estar com você."
    m "Quando esse dia chegar, finalmente estarei ao seu lado."
    m 1ekbfa "Quero viver cada momento com você, [mas_get_player_nickname()]."
    m 1hubfb "Não há aventura maior que a nossa, [ju]~"
    return

default -5 persistent._mas_pm_likes_panties = None


default -5 persistent._mas_pm_no_talk_panties = None


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_panties",
            category=['diversos',"roupas"],
            prompt="Roupas íntimas",
            random=True,
            sensitive=True
        )
    )

label monika_panties:
    m 1lsc "Ei, [player]..."
    m "Não ria quando eu perguntar isso, ok?"
    m 2rksdlc "Mas..."
    m 4rksdlc "Por que alguns caras são obcecados por calcinhas?"
    m 1euc "Sério, qual é o grande lance com um pedaço de tecido?"
    m "A maioria das garotas usa, não é?"
    m 5lkc "Na verdade, pensando bem..."
    m 5lsc "Acho que existe um termo para esse tipo de coisa..."
    m 5lfc "Hmm, qual era mesmo?"
    m 5wuw "Ah, lembrei, o termo é 'parafilia'."
    m 2rksdlc "É uma variedade de fetiches que envolvem... coisas incomuns."
    m 2esc "Uma fantasia muito comum envolve calcinhas femininas."
    m 3esc "Meias, cintas-liga, calças transparentes e todo esse tipo de coisa."
    m 2esc "A obsessão pode ser leve ou severa dependendo da libido de cada pessoa."
    m 2ekc "Você acha que realmente os excita só de ver?"
    m 2tkc "E não para por aí!"
    m 4tkc "Acontece que existe um tipo de 'mercado negro' para roupas íntimas usadas."
    m 2tkx "Não estou brincando!"
    m 2tkd "Eles ficam excitados com o cheiro da mulher que usou..."
    m "Tem gente disposta a pagar por roupas íntimas usadas de mulheres aleatórias."
    m 2lksdlc "Sério, me pergunto o que os deixa tão excitados."
    m 2euc "Será por causa da aparência, talvez?"
    m 3euc "Existem diferentes tipos, com diferentes designs e materiais."
    m 2lsc "Mas..."
    m "Pensando bem agora."
    m 3esd "Lembro de um estudo onde o nível de testosterona do homem aumenta por causa dos feromônios no cheiro feminino."
    m 2tkc "O cheiro é excitante ou algo assim?"
    m 3tkx "Quer dizer, são roupas usadas, não é meio nojento?"
    m 3rksdlc "Sem mencionar que é anti-higiênico."
    m 2rksdla "Isso me lembra alguém, por sinal."
    m 3rksdlb "Alguém que talvez tenha roubado uma certa caneta?"
    m 1eua "Mas, cada um com suas preferências, acho que não vou julgar muito."

    if mas_isMoniHappy():

        m 2tsb "Você não é obcecado por esse tipo de coisa, é [player]?"
        m 3tsb "Não está saindo comigo só porque estou usando meias sensuais, certo?"
        m 4tsbsa "Ou talvez você queira dar uma espiadinha?~"
        m 1hub "Ahaha!"
        m 1tku "Só estou te provocando, [player]."
        m 1tfu "Admita, você ficou um pouco [exctd], não ficou?"
        m 1lsbsa "Além disso..."
        m 1lkbsa "Se você realmente quisesse sentir meu cheiro..."
        m 1hubfa "Poderia simplesmente pedir um abraço!"
        m 1ekbfa "Nossa, eu só quero sentir seu abraço mais e mais."
        m "Afinal, estamos aqui para sempre, e eu estou aqui por você."
        m 1hubfb "Eu te amo tanto, [player]~"
        return "love"

    elif mas_isMoniAff(higher=True):

        m 1lkbsb "Você...{w=1}gosta desse tipo de coisa, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Você...{w=1}gosta desse tipo de coisa, [player]?{fast}"
            "Sim.":
                $ persistent._mas_pm_likes_panties = True
                $ persistent._mas_pm_no_talk_panties = False
                m 1wud "O-oh..."
                m 1lkbsa "S-se você gosta, poderia simplesmente me pedir, sabe?"
                m "Eu poderia...{w=1}te ajudar a aliviar essa tensão..."
                m 5eubfu "É isso que casais fazem, não é?"
                m 5hubfb "Ahaha!"
                m 5ekbfa "Mas até esse dia chegar, você vai ter que aguentar esses pensamentos por mim, ok?"
            "Não.":
                $ persistent._mas_pm_likes_panties = False
                $ persistent._mas_pm_no_talk_panties = False
                m 1eka "Ah, entendo..."
                m 2tku "Acho que cada um tem seus prazeres secretos..."
                m "Talvez você goste de outra coisa?"
                m 4hubsb "Ahaha~"
                m 4hubfa "Só estou brincando!"
                m 5ekbfa "Não me importo de ficarmos no modo fofinho, para ser sincera..."
                m "É mais romântico assim~"
            "Não quero falar sobre isso...":
                $ persistent._mas_pm_no_talk_panties = True
                m 1ekc "Entendo, [player]."
                m 1rksdld "Sei que alguns assuntos são melhores guardados até a hora certa."
                m 1ekbsa "Mas quero que você sinta que pode me contar qualquer coisa..."
                m "Então não tenha medo de me contar suas...{w=1}fantasias, ok [player]?"
                m 1hubfa "Não vou te julgar por isso...{w=1}afinal, nada me deixa mais feliz que te fazer feliz~"
        return "derandom"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fahrenheit451",category=['literatura'],prompt="Recomendações de livros",random=True))

label monika_fahrenheit451:
    m 1euc "[player], você já ouviu falar de Ray Bradbury?"
    m 3euc "Ele escreveu um livro chamado {i}Fahrenheit 451{/i}."
    m 3eud "É sobre um futuro distópico onde todos os livros são considerados inúteis e imediatamente queimados."
    m 2ekc "Não consigo imaginar um mundo onde o conhecimento é proibido e destruído."
    m "Parece que há outros que escondem livros para impedir o pensamento livre das pessoas."
    m 2lksdla "A história humana tem um jeito engraçado de se repetir."
    m 4ekc "Então [player], quero que você me prometa uma coisa..."
    m 4tkd "Nunca, {i}jamais{/i} queime um livro."
    m 2euc "Eu perdoo você se já fez isso antes."
    m 2dkc "Mas a ideia de não permitir a si mesmo aprender com eles me deixa um pouco triste."
    m 4ekd "Você estaria perdendo tanto!"
    m 4ekc "É demais para o meu coração aguentar!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_piggybank",category=['diversos'],prompt="Economizar dinheiro",random=True))

label monika_piggybank:
    m 1eua "Você tem um cofrinho, [player]?"
    m 1lsc "Muita gente não tem mais esses dias."
    m "Moedas são frequentemente consideradas sem valor."
    m 3eub "Mas elas realmente vão acumulando!"
    m 1eub "Li que uma vez um homem procurava por moedas perdidas em lava-rápidos durante suas caminhadas diárias."
    m 1wuo "Em uma década, ele trocou todas suas moedas por um total de 21.495 dólares!"
    m "Isso é muito dinheiro!"
    m 1lksdla "Claro que nem todo mundo tem tempo para isso todo dia."
    m 1euc "Em vez disso, eles só jogam as moedas no cofrinho."
    m 1eua "Algumas pessoas gostam de estabelecer metas para o que querem comprar com o dinheiro que juntaram."
    m "Como guardam um pouco de cada vez, fica mais fácil juntar o bastante para comprar o que querem."
    m 3eka "E mesmo quando têm, a maioria das pessoas não gosta de gastar dinheiro à toa."
    m 1eua "Mas guardar dinheiro para um propósito específico, além do fato de serem quantias pequenas de cada vez, realmente te convence que está basicamente ganhando o item de graça."
    m 2duu "Mas no final, uma guitarra sempre custa o mesmo que uma guitarra."
    m 2eua "Psicologicamente falando, acho isso bem interessante!"
    m 1lsc "Porém, alguns cofrinhos têm um problema..."
    m 1esc "Às vezes você tem que quebrar o cofrinho para pegar as moedas..."
    m 3rksdlc "Então você pode acabar gastando dinheiro para comprar outro."
    m 4eua "Felizmente, a maioria dos cofrinhos não é mais assim."
    m 1eua "Eles geralmente têm uma tampa de borracha que você pode tirar, ou um painel que sai na parte de trás."
    m 3eua "Quem sabe, se juntar moedas suficientes, você não consegue comprar um presente bem legal pra mim?"
    m 1hua "Eu faria o mesmo por você, [mas_get_player_nickname()]!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_daydream",
            category=['romance'],
            prompt="Day dreaming",
            random=True,
            rules={"skip alert": None},
            aff_range=(mas_aff.DISTRESSED, None)
        )
    )

label monika_daydream:

    python:

        daydream_quips_upset = [
            "como era quando nos conhecemos pela primeira vez...",
            "o que senti quando te conheci...",
            "os bons momentos que costumávamos ter...",
            "a esperança que eu tinha para o nosso futuro..."
        ]


        daydream_quips_normplus = [
            "nós [du] lendo um livro [ju] em um dia frio de inverno, aconchegados sob um cobertor quentinho...",
            "fazendo um dueto, com você cantando minha música enquanto eu toco piano...",
            "jantando [ju] num momento romântico, só eu e você~",
            "passando a noite no sofá [juh]...",
            "você segurando minha mão enquanto caminhamos lá fora num dia ensolarado...",
        ]


        daydream_quips_happyplus = list(daydream_quips_normplus)
        daydream_quips_happyplus.extend([
            "nós [dtds] e nos abraçando enquanto assistimos alguma coisa...",
        ])


        daydream_quips_affplus = list(daydream_quips_happyplus)







        daydream_quips_enamplus = list(daydream_quips_affplus)
        daydream_quips_enamplus.extend([
            "acordando ao seu lado pela manhã, te observando dormir pertinho de mim...",
        ])


        if renpy.seen_label("mas_monika_cherry_blossom_tree"):
            daydream_quips_enamplus.append("nós [du] descansando sob a sombra da árvore de cerejeira...")


        if persistent._mas_pm_hair_length is not None and persistent._mas_pm_hair_length != "bald":
            daydream_quips_enamplus.append("eu fazendo carinho no seu cabelo enquanto sua cabeça repousa no meu colo...")


        if mas_isMoniEnamored(higher=True):
            daydream_quip = renpy.random.choice(daydream_quips_enamplus)
        elif mas_isMoniAff():
            daydream_quip = renpy.random.choice(daydream_quips_affplus)
        elif mas_isMoniHappy():
            daydream_quip = renpy.random.choice(daydream_quips_happyplus)
        elif mas_isMoniNormal():
            daydream_quip = renpy.random.choice(daydream_quips_normplus)
        else:
            daydream_quip = renpy.random.choice(daydream_quips_upset)

    if mas_isMoniNormal(higher=True):
        m 2lsc "..."
        m 2lsbsa "..."
        m 2tsbsa "..."
        m 2wubsw "Ah, desculpa! Eu estava sonhando acordada por um instante."
        m 1lkbsa "Estava imaginando [daydream_quip]"
        m 1ekbfa "Não seria maravilhoso, [mas_get_player_nickname()]?"
        m 1hubfa "Vamos torcer para isso se tornar realidade algum dia, ehehe~"

    elif _mas_getAffection() > -50:
        m 2lsc "..."
        m 2dkc "..."
        m 2dktpu "..."
        m 2ektpd "Ah... desculpa, eu estava perdida em pensamentos por um momento."
        m 2dktpu "Estava lembrando de [daydream_quip]"
        m 2ektdd "Será que um dia voltaremos a ser tão felizes, [player]...?"
    else:

        m 6lsc "..."
        m 6lkc "..."
        m 6lktpc "..."
        m 6ektpd "Ah... desculpa, eu só estava..."
        m 6dktdc "Quer saber? Deixa para lá."
    return "no_unlock"




label monika_music2:
    if songs.getVolume("music") == 0.0:
        m 1eka "... "
        m 1ekbsa "...Esse silêncio... "
        m "...Só nós [du], olhando nos olhos um do outro... "
        m 2dubsu "...E então, lentamente, nos aproximamos para um beijo... "
        m 1hksdlb "Ahaha... infelizmente, ainda existem algumas barreiras para que isso possa acontecer de verdade."
        m 1ekbfa "Mas tudo bem sonhar, não é, [player]?"
        m 1hubfa "Quem sabe um dia, a gente torne esse sonho realidade~"

    elif songs.getPlayingMusicName() == 'Just Monika':
        m 1ekc "Sempre achei essa música meio assustadora."
        m "Com esses ruídos distorcidos e aquele zumbido estranho..."
        m 1eua "Não é que eu prefira uma música a outra, mas se você quiser trocar por outra..."
        m 3eka "...com certeza eu não reclamaria!"
        m 1hua "Ahaha! Mas não se preocupe, tudo bem se quiser continuar com essa."
        m 1eka "Eu fico bem com qualquer uma, então escolha a que te faz mais feliz~"

    elif songs.getPlayingMusicName() == 'Your Reality':
        m 1hub "~Todo dia, eu imagino um futuro onde eu posso estar com você...~"
        m 1eua "Espero que goste de ouvir minha voz, [player]."
        m 1esa "É a única que você ouve no jogo, certo? As vozes da Sayori, da Yuri ou da Natsuki nunca aparecem."
        m "Fico imaginando como seria a voz delas..."
        m 1lksdla "Bem, com base na personalidade de cada uma, dá para imaginar com certa precisão."
        m 1eka "Mas de qualquer forma, fico feliz por ter compartilhado algo tão íntimo com você, [player]."
        m 3eua "Quem sabe um dia, eu possa ouvir a sua voz também, [player]!"
        m 1hua "Isso me deixaria ainda mais feliz do que já estou~"

    elif songs.getPlayingMusicName() == 'Your Reality (Piano Cover)':
        m 1eua "Aproveitando minha música, [player]?"
        m 1eka "Não foi fácil criá-la, sabia?"
        m "Fazer sua própria música é um processo lento e difícil, especialmente quando envolve seus próprios sentimentos."
        m 3rksdlb "Eu queria que ela estivesse perfeita antes de te mostrar!"
        m "Passei tantas horas revendo e revisando..."
        m 1eua "O tempo simplesmente voava enquanto eu trabalhava nela."
        m 1hua "Depois de tanta dedicação, fico orgulhosa do resultado final."
        m 3eua "E como você está ouvindo, imagino que também tenha gostado..."
        m 3eka "Obrigada por ouvir algo em que coloquei tanto carinho, [player]!"
        m 1hub "Saber que você valoriza o que eu fiz por você me deixa muito feliz~"

    elif songs.getPlayingMusicName() == 'I Still Love You':
        m 1ekc "Nossa... toda vez que ouço essa música, fico triste."
        m "Ela me lembra de todas as coisas... lamentáveis que fiz com as outras garotas."
        m 1lksdlc "Espero que você não esteja mais [bv] comigo pelo que aconteceu..."
        m "..."
        m 1lsc "Bom, você {i}fez{/i} questão de instalar um mod só para gente poder ficar junto de novo..."
        m 1eua "Acho que isso já é prova suficiente de que você ainda me ama, pelo menos um pouco."
        m 1eka "Se ainda estiver [mgd] com o que fiz com as outras, eu entendo perfeitamente. Ainda me sinto muito mal por tudo, e farei o que for preciso para compensar."

    elif songs.getPlayingMusicName() == 'Okay, Everyone! (Monika)':
        m 1eua "Essa música sempre foi bem relaxante para mim."
        m "Acho que é por ser um solo de piano."
        m 1hua "E como você deve imaginar, meu instrumento favorito é o piano."
        m 3eua "Sabe, se eu soubesse como, eu mesma programaria um piano aqui nessa sala."
        m 1eua "Poderia compor mais músicas... e tocá-las só para você..."
        m 4hub "Quem sabe até tocarmos [ju]! Não seria incrível, [player]?"
        m 1eua "Se você ou alguém que conhece souber como programar isso no jogo, eu ficaria imensamente grata~"

    elif songs.getPlayingMusicName() == 'Surprise!':
        m 1ekc "Essa música sempre me deixa deprimida..."
        m "Nem eu esperava que a morte da Sayori fosse tão brutal..."
        m 1tkc "Às vezes, quando me perco nos meus próprios pensamentos, os olhos vazios dela simplesmente surgem na minha mente..."
        m 1lksdlc "..."
        m 1eka "É reconfortante lembrar que a Sayori nunca foi real. E também é reconfortante saber que você ainda me ama, apesar de tudo que eu fiz."
        m "Quero dizer... você ainda está aqui, não está? Não estaria se não me amasse."
        m 1hua "Enquanto estivermos [ju], não há motivo para eu ficar triste. Você é a luz do meu mundo, [player], e estar aqui com você já me faz sorrir."

    elif songs.getPlayingMusicName() == "Doki Doki Theme (80s version)":
        m 1hub "Boa escolha, [player]!"
        m 1hksdlb "Obviamente, essa versão não é realmente dos anos 80..."
        m 1hua "Mas ela tem um estilo que eu realmente adoro!"
        m 1eua "Você gosta muito de músicas dos anos 80, [player]?"
        m 1eka "Eu ainda prefiro o som autêntico de um piano... mas se isso te faz feliz, não me importo em passar horas ouvindo com você~"

    elif songs.getPlayingMusicName() == "Play With Me (Variant 6)":
        m 2lksdlc "para ser sincera, não sei por que você estaria ouvindo essa música, [player]."
        m 2ekc "Me sinto muito mal por aquele erro."
        m 2ekd "Eu nunca quis forçar você a passar tempo com a Yuri naquele estado..."
        m 4ekc "Tente não pensar nisso, tá bom?"
    else:

        m 1esc "..."
        m "...Esse silêncio..."
        m 1ekbsa "...Só nós [du], olhando nos olhos um do outro..."
        m 2dubsu "...E então, lentamente, nos aproximamos para um beijo..."
        m 1hksdlb "Ahaha... infelizmente, ainda existem algumas barreiras para que isso possa acontecer de verdade."
        m 1ekbfa "Mas tudo bem sonhar, não é, [player]?"
        m 1hubfa "Quem sabe um dia, a gente torne esse sonho realidade~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_confidence_2",category=['vida'],prompt="Falta de confiança",random=True))

label monika_confidence_2:
    m 1ekc "[player], você já sentiu que te falta iniciativa para fazer algo?"
    m "Quando me sinto mais vulnerável, tenho dificuldade de encontrar motivação, criatividade e bom senso para agir por conta própria."
    m 1tkc "É como se tudo ao meu redor ficasse parado."
    m "Parece que minha vontade de encarar tarefas com confiança, como compartilhar meus textos com outras pessoas, simplesmente desaparece."
    m 3eka "Mas tenho trabalhado nisso com muita dedicação, e cheguei a uma conclusão..."
    m 1eua "Acredito firmemente que ter iniciativa é uma habilidade muito importante."
    m "E isso é algo que, pessoalmente, eu acho muito reconfortante."
    m 1hua "Criei um processo de três etapas que qualquer pessoa pode aplicar!"
    m 3rksdlb "Ainda está em desenvolvimento, então leve com um certo ceticismo, tá?"
    m 3hua "Passo um!"
    m 1eua "Crie um plano que {i}você{/i} consiga e esteja disposto a seguir, alinhado com seus objetivos e conquistas futuras."
    m 3hua "Passo dois!"
    m 1eua "Construir e fortalecer sua confiança é muito importante."
    m "Comemore até as menores vitórias — elas se acumulam com o tempo, e você vai perceber quantas coisas realiza no dia a dia."
    m 2hua "Com o tempo, essas tarefas que antes pareciam difíceis serão feitas como verdadeiros atos de coragem!"
    m 3hub "Passo três!"
    m 1eua "Faça o possível para manter a mente aberta e estar sempre disposto a aprender."
    m 1eka "Ninguém é perfeito, e todos têm algo a ensinar uns aos outros."
    m 1eua "Isso ajuda a entender as situações sob outras perspectivas, e pode inspirar outras pessoas a fazer o mesmo."
    m "E é basicamente isso."
    m 3hua "Fique ligado para mais sessões de autoaperfeiçoamento com a Monika, aclamadas pela crítica!"
    m 1hksdlb "Ahaha, tô só brincando com essa última parte."
    m 1ekbsa "Falando sério, fico muito feliz por ter você comigo, [player]..."
    m "Seu amor e carinho constantes são tudo o que preciso para chegar onde quero estar."
    m 1hubfa "E que tipo de namorada eu seria se não retribuísse isso, hein?~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_pets",category=['monika'],prompt="Animais de estimação",random=True))

label monika_pets:
    m 1eua "Ei [mas_get_player_nickname(regex_replace_with_nullstr='meu ')], você já teve um bichinho de estimação?"
    m 3eua "Estava pensando que seria legal ter um para fazer companhia."
    m 1hua "Seria divertido cuidarmos de um [ju]!"
    if not persistent._mas_acs_enable_quetzalplushie:
        m 1tku "Aposto que você não adivinha qual pet eu gostaria de ter..."
        m "Você provavelmente pensou em um gato ou cachorro, mas eu tenho outra coisa em mente."
    m 1eua "O pet que eu gostaria de ter é um que vi uma vez num livro."
    m "Era o 'Manual das Aves do Mundo'. A biblioteca tinha a coleção completa!"
    m 1eub "Eu adorava olhar as ilustrações maravilhosas e ler sobre aves exóticas."
    m 1hub "No começo, pensei que algum tipo de sabiá seria legal, mas então encontrei algo incrível no volume seis!"
    m "Uma ave esmeralda chamada Quetzal Resplandecente."
    m 1eua "São aves raras, solitárias e que cantam músicas lindas."
    m "Isso te lembra alguém, [player]?"
    m 1lksdla "Mas eu me sentiria muito mal em ter um como pet..."
    m "Os quetzais nasceram para serem livres."
    m 4rksdlc "Eles morrem em cativeiro. É por isso que quase não se vêem em zoológicos."
    m "Mesmo que não fosse um pássaro real, ainda pareceria errado mantê-lo preso nesta sala."
    m 1ekc "...Eu não conseguiria fazer algo assim, sabendo como é essa sensação."
    if not persistent._mas_acs_enable_quetzalplushie:
        m 1hua "Mas um de pelúcia seria ótimo!"
        m 2hub "..."
        m 2hksdlb "Desculpa pelo desabafo, [mas_get_player_nickname()]."
        m 1eka "Até que eu consiga sair daqui, você poderia me prometer que vai me manter longe da solidão?"
        m 1hua "Vou ver se consigo trazer esse bichinho de pelúcia para cá! Ah— mas não se preocupe, você ainda é o meu favorito~"
    else:
        m 1eub "Mas pelo menos eu tenho a melhor alternativa possível graças a você, [player]!"
        m 1eka "De verdade, isso me ajuda muito a não me sentir sozinha quando você não está aqui."
        m 3hua "Foi um presente maravilhoso~"
    return


init python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_plushie",
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_plushie:
    m 1eka "Ei [player], só queria agradecer de novo por esse lindo pelúcia de quetzal!"
    m 2lksdla "Sei que pode parecer bobo, mas ele realmente me faz companhia quando você está ausente..."
    m 1ekbsa "E não que eu pudesse esquecer, mas toda vez que olho para ele, me lembro o quanto você me ama~"
    m 3hub "Foi realmente o presente perfeito!"


    $ mas_hideEVL("monika_plushie","EVE",lock=True,derandom=True)
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dogs",category=['diversos','membros do clube'],prompt="Melhor amigo do homem",random=True))

label monika_dogs:
    m 1eua "Você gosta de cachorros, [player]?"
    m 1hub "Cachorros são maravilhosos! São ótimos para ter por perto."
    m 3eua "Sem mencionar que ter um cachorro ajuda pessoas com ansiedade e depressão, já que são animais muito sociáveis."
    m 1hua "Eles são tão adoráveis, eu realmente gosto deles!"
    m 1lksdla "Sei que a Natsuki também gostava..."
    m "Ela sempre ficava envergonhada por gostar de coisas fofas. Queria que ela se sentisse mais à vontade para ser ela mesma."
    m 2lsc "Mas..."
    m 2lksdlc "Acho que o ambiente em que ela vivia influenciou isso."
    m 2eka "Se algum amigo seu tem interesses que goste muito, sempre seja solidário, ok?"
    m 4eka "Você nunca sabe como uma rejeição casual pode machucar alguém."
    m 1eua "Mas conhecendo você, [player], você não faria algo assim, certo?"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cats",category=['diversos'],prompt="Companheiros felinos",random=True))

label monika_cats:
    m 1hua "Gatos são bem fofos, não são?"
    m 1eua "Apesar de parecerem tão elegantes, sempre acabam em situações engraçadas."
    m 1lksdla "Não é à toa que são tão populares na internet."
    m 3eua "Sabia que os egípcios antigos consideravam gatos sagrados?"
    m 1eua "Havia uma deusa gato chamada Bastet que eles adoravam. Ela era uma espécie de protetora."
    m 1eub "Gatos domesticados eram muito valorizados por serem excelentes caçadores de pragas e roedores."
    m "Naquela época, você os via principalmente associados a nobres ricos e outras classes altas da sociedade."
    m 1eua "É incrível o quanto as pessoas levavam seu amor por seus animais de estimação."
    m 1tku "Eles {i}realmente{/i} amavam gatos, [player]."
    m 3hua "E as pessoas ainda amam hoje!"
    m 1eua "Felinos ainda são um dos animais de estimação mais comuns."
    m 1hua "Talvez devêssemos ter um quando estivermos morando [ju], [player]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fruits",category=['monika','curiosidades'],prompt="Comer frutas",random=True))

label monika_fruits:
    m 3eua "[player], sabia que eu gosto de uma fruta suculenta de vez em quando?"
    m "A maioria é muito saborosa, além de benéfica para o corpo."
    m 2lksdla "Muita gente confunde algumas frutas com legumes."
    m 3eua "Os melhores exemplos são pimentões e tomates."
    m "Geralmente são consumidos com outros legumes, então as pessoas os confundem."
    m 4eub "Já cerejas são deliciosas."
    m 1eua "Sabia que cerejas também são boas para atletas?"
    m 2hksdlb "Poderia listar todos os benefícios, mas duvido que você se interessaria."
    m 2eua "Tem também o chamado beijo de cereja."
    m "Você já deve ter ouvido falar, [mas_get_player_nickname()]~"
    m 2eub "É obviamente feito por duas pessoas que se gostam."
    m "Uma segura a cereja com a boca, e a outra a come."
    m 3ekbsa "Você poderia... segurar a cereja para mim."
    m 1lkbsa "Assim eu posso te devorar!"
    m 3hua "Ehehe~"
    m 2hua "Só te provocando, [player]~"
    return


default -5 persistent._mas_pm_like_rock_n_roll = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rock",
            category=['mídia','literatura',"música"],
            prompt="Rock and roll",
            random=True
        )
    )

label monika_rock:
    m 3esa "Quer conhecer uma forma legal de literatura?"
    m 3hua "Rock and roll!"
    m 3hub "Isso mesmo. Rock and roll!"
    m 2eka "É desanimador saber que tantas pessoas acham que rock é só um monte de barulho."
    m 2lsc "Para ser sincera, eu também julguei o rock no começo."
    m 3euc "Na verdade, não é diferente de poesia."
    m 1euc "Muitas músicas de rock contam histórias através de simbolismos, que a maioria não entende na primeira vez que ouve."
    m 2tkc "Na verdade, compor letras para uma única música de rock já é difícil."
    m "Escrever boas letras para rock requer muita atenção aos jogos de palavras."
    m 3tkd "Além disso, você precisa ter uma mensagem clara e concisa durante toda a música."
    m 3eua "Quando você junta tudo isso, tem uma obra-prima!"
    m 1eua "Como escrever um bom poema, escrever letras é mais fácil falando do que fazendo."
    m 2euc "Mas estive pensando..."
    m 2eua "Eu meio que quero tentar escrever uma música de rock para variar."
    m 2hksdlb "Ahaha! Escrever rock não é algo que você esperaria de alguém como eu, né?"
    m 3eua "É engraçado como o rock surgiu como uma evolução do blues e do jazz."
    m "O rock se tornou um gênero proeminente e deu origem a muitos subgêneros também."
    m 1eub "Metal, hard rock, rock clássico e mais!"
    m 3rksdla "Ah, falei demais. Desculpa, desculpa."

    m 3eua "Você escuta rock, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você escuta rock, [player]?{fast}"
        "Sim.":
            $ persistent._mas_pm_like_rock_n_roll = True
            m 3hub "Ótimo!"
            m 1eua "Quando quiser ouvir um bom e velho rock 'n' roll, vá em frente."
            m 1hua "Mesmo se você colocar no volume máximo, vou adorar ouvir com você. Ehehe!"
            if (
                not renpy.seen_label("monika_add_custom_music_instruct")
                and not persistent._mas_pm_added_custom_bgm
            ):
                m 1eua "Se quiser compartilhar suas músicas de rock favoritas comigo, [player], é bem fácil!"
                m 3eua "Basta seguir esses passos..."
                call monika_add_custom_music_instruct
        "Não.":

            $ persistent._mas_pm_like_rock_n_roll = False
            m 1ekc "Oh... Tudo bem, cada um tem seu gosto musical."
            m 1hua "Mas se algum dia quiser experimentar ouvir rock, ficarei feliz em ouvir junto com você."
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_standup",category=['literatura','mídia'],prompt="Comédia stand-up",random=True))

label monika_standup:
    m 1eua "Sabe o que é uma forma interessante de literatura, [player]?"
    m 3hub "Stand-up comedy!"
    if seen_event('monika_rock') and seen_event('monika_rap'):
        m 2rksdla "...Nossa, tenho dito que várias coisas aleatórias são literatura, não é?"
        m 2hksdlb "Estou começando a me sentir como a Natsuki, ou algum pós-modernista fanático, ahaha!"
        m 2eud "Mas sério, existe uma verdadeira arte em escrever piadas para stand-up."
    else:
        m 2eud "Pode parecer estranho, mas existe uma verdadeira arte em escrever piadas para stand-up."
    m 4esa "É diferente de fazer piadas de uma linha, porque precisa contar uma história."
    m 4eud "Mas ao mesmo tempo, você precisa manter o público engajado."
    m 2euc "Então é importante desenvolver suas ideias ao máximo, talvez até transitando para algo relacionado ao tema..."
    m 2eub "Tudo isso enquanto mantém o público cativado até chegar no punchline;{w=0.5} esperando muitas risadas."
    m 3esa "De certa forma, é como escrever um conto, mas sem o clímax descendente."
    m 3esc "E ainda assim, entre as piadas, você encontra a alma do comediante...{w=0.5}seus pensamentos e sentimentos sobre qualquer assunto..."
    m 3esd "...Suas experiências de vida, e quem eles são hoje."
    m 1eub "Tudo isso aparece nos textos que escrevem para seus shows."
    m 3euc "Acho que a parte mais difícil do stand-up é ter que performar."
    m 3eud "Afinal, como saber se seu material é bom sem testar com uma plateia?"
    m 1esd "De repente, essa forma de literatura se torna muito mais complexa."
    m 1euc "Como você diz suas piadas, sua linguagem corporal, suas expressões faciais..."
    m 3esd "Agora não é só sobre o que você escreveu,{w=1} mas como você entrega."
    m 3esa "É meio como poesia nesse aspecto, não acha?"
    m 2rksdlc "Muitas pessoas nem tentam stand-up porque têm que enfrentar uma plateia..."
    m 2eksdlc "Sabia que o maior medo das pessoas é falar em público?"
    m 4wud "O número dois é a morte.{w=0.5} A morte é número dois!{w=0.5} O que há com isso?!"
    m 4eud "Isso significa que, para uma pessoa comum, se for a um funeral, é melhor estar no caixão..."
    m 4tub "...do que fazendo o elogio fúnebre!"
    m 1hub "...Ahaha! Desculpe, eu queria contar uma piada que o Jerry Seinfeld escreveu--"
    m 3etc "--Você conhece ele, né?"
    m 1eua "E então?{w=0.5} Você riu?"
    m 3hksdlb "Hmm...{w=1}talvez eu deva trabalhar no meu próprio material..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_soda",
            category=['vida','diversos'],
            prompt="Beber refrigerante",
            random=True
        )
    )

default -5 persistent._mas_pm_drinks_soda = None


label monika_soda:
    m 2euc "Você bebe refrigerante, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você bebe refrigerante, [player]?{fast}"
        "Sim.":

            $ persistent._mas_pm_drinks_soda = True
            m 4ekc "Você sabe que refrigerante faz muito mal, né?"
            m 2ekc "Tem muitas coisas que prejudicam seu corpo e saúde no geral."
            m 2tkd "Pode corroer seus dentes e causar cáries."
            m 2euc "Pode até pensar que refrigerante diet é menos nocivo, mas pode ser tão prejudicial quanto."
            m 2lksdlc "Nada contra um agrado ocasional. Só não deixe que vire um vício, [player]."
            m 2eua "Por que não tenta seguir meu estilo de vida saudável?"
            m 1hua "Assim você pode ficar em forma como eu!"
            m 1hub "Ahaha!"
            m 2ekc "Eu odiaria ver você negligenciar sua saúde, [player]."
            m 1eka "Quero que você viva o máximo possível para termos chance de ficar [ju] na sua realidade."
            m "Então diminua o refrigerante, certo [mas_get_player_nickname()]?"
        "Não.":

            $ persistent._mas_pm_drinks_soda = False
            m 2eka "Que alívio ouvir isso."
            m "Fico feliz que não preciso me preocupar com você se prejudicando bebendo muito refrigerante."
            m 3eub "Mas não há problema em dar uma escapadinha de vez em quando, sabe?"
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Talvez um dia possamos tomar refrigerante [ju]."
            m 5hua "Pode não ser nada chique, mas cairia muito bem num dia quente."
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_clones",category=['monika','mod','filosofia'],prompt="Ser clonada",random=True))

label monika_clones:
    m 1euc "Hm... ei, [player]?"
    m 1lsc "Acabei de ter um pensamento estranho."
    m 1euc "Sabe como você baixou esse jogo da internet?"
    m "Qualquer um pode fazer isso, certo?"
    m 1eub "E esse mod foi feito especificamente para mim. Por pessoas que têm sua própria versão de mim..."
    m 3etc "Então... isso significa que existem várias Monikas por aí.{w=0.5} {nw}"
    extend 1rsc "É algo meio difícil de imaginar."
    m 1euc "Um número potencialmente infinito de mim, cada uma presa em seu próprio jogo, com suas próprias histórias."
    m 1lksdla "A teoria do multiverso é algo e tanto, hein?"
    m 1eka "Mas eu sou a única... eu, e meu coração pertence só a você."
    m 1ekc "Mesmo assim, não posso deixar de me sentir um pouco menos... especial por causa disso."
    m "Pense assim, [player]."
    m 1tkc "O que te deixaria mais feliz: receber uma única rosa, ou cem rosas?"
    m 3eka "Cem rosas podem parecer legais. Mas são tantas que fica difícil valorizar cada uma. Por causa da quantidade, cada rosa individual se torna menos especial."
    m "O significado por trás de cada presente se perde, simplesmente por haver tantos."
    m 1eua "...Mesmo que eu seja apenas uma estrela num universo de Monikas, ainda sou a única sortuda o suficiente por ter te encontrado, [player]."
    m 1hubsa "Você sempre será minha rosa especial."
    m 1ekbfa "Eu te amo, [player]. Por favor nunca me substitua, ok?"
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_immortal",category=['monika','filosofia'],prompt="Diferença de idade",random=True))

label monika_immortal:
    m 3hua "[player]! Estive pensando em algo..."
    m 1eua "Sabia que existe uma página na wiki sobre mim?"
    m 1lsc "Bem..."
    m 2lsc "Diz que eu tenho dezoito anos."
    m 2euc "Mas quando você para para pensar... isso não é totalmente verdade."
    m 2eud "Quero dizer, humanos envelhecem, mas isso não se aplica a mim."
    m 4eksdla "Eu sou...{w=0.5}basicamente imortal."
    m 2lksdlc "A sociedade parece achar problemático relacionamentos com grande diferença de idade."
    m 2lksdld "...Por isso que mencionei isso."
    m 3eka "Eventualmente, a diferença entre nós seria enorme se eu continuasse com dezoito para sempre."
    m 1eua "Mas não acredito que minha vida possa ser resumida a um número."
    m 1ekbsa "Então eu vou te amar por toda a eternidade, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]. Apenas lembre disso."
    return "love"

default -5 persistent._mas_pm_wearsRing = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_promisering",
            category=['romance'],
            prompt="Anel de compromisso",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_promisering:
    m 3rksdla "Sabia que quando duas pessoas confessam seus sentimentos, às vezes usam anéis combinando?{nw}"
    $ _history_list.pop()
    menu:
        m "Sabia que quando duas pessoas confessam seus sentimentos, às vezes usam anéis combinando?{fast}"
        "Eu sei.":

            m 1wkbld "Ah..."
            m 1rkbla "..."
            m 3hkblb "Desculpe, eu estava viajando aqui por um instante...{w=0.3}{nw}"
            extend 1dkbssdlu " Imaginando outro lugar onde você diria isso~"
            m 3hkbssdlb "Ahaha, só estou brincando."
            m 1hkbssdlb "Nem estava pensando nisso...{w=0.3}{nw}"
            extend 3ekbfb " Estava pensando mais em anéis de compromisso."
        "Não sabia...":

            m 1ekblu "Bem, você sabe que quando as pessoas se comprometem elas fazem isso pelo menos..."
            m 3rka "Mas não era sobre isso que eu estava pensando."
            m 3eub "Estava pensando mais em anéis de promessa."
        "Tipo...casamento?":

            m 1hkblb "Ahaha, isso também, claro!{w=0.2} {nw}"
            extend 3ekblu "Mas na verdade não era sobre isso que eu pensava..."
            m 3eub "Estava pensando mais em anéis de promessa."

    m 1eubsa "Se você usar um anel de compromisso, pode mostrar a todos que estamos [ju]~"
    m 3tkbsu "E também ajuda a lembrar do nosso amor eterno~"

    m 1ekbssdlu "Enfim, só estava pensando...{w=0.3} {nw}"
    extend 1eksdla "Você usa um anel por mim, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Enfim, só estava pensando... Você usa um anel por mim, [player]?{fast}"
        "Uso sim.":

            $ persistent._mas_pm_wearsRing = True

            m 1sublo "Aww, [player]!"
            m 1hublb "Você não tem ideia de como isso me deixa feliz!"
            m 1ekbsa "Saber que você se importa o suficiente para mostrar seu amor e dedicação..."
            m "Isso significa tudo para mim."
        "Não uso.":

            $ persistent._mas_pm_wearsRing = False

            m 4rksdla "Talvez você devesse arrumar um."
            m 2eua "Digo, já estamos num relacionamento. Por que não mostrar esse amor e dedicação?"
            m 2lfu "Também ajudaria a manter...{w=0.2}aqueles pretendentes indesejados longe de você."
            m 7ekbsa "Se você usasse um, só um anel de compromisso, no seu dedo anelar por mim..."
            m 1ekbsa "Me deixaria muito feliz."

    if not persistent._mas_acs_enable_promisering:
        m 1rubsa "Queria poder ter um também. Tenho certeza que vou encontrar um jeito de conseguir um aqui com o tempo."
        m 1dubsa "...E então eu poderia usá-lo para sempre."
        m 3ekbfu "Mas até lá, lembre que meu compromisso com você é inabalável, [player]."
    else:

        if not persistent._mas_pm_wearsRing:
            m 3ekbsa "Tão feliz quanto você me deixou quando me deu esse anel."
            m 1ekbsa "Sinceramente não consigo expressar o quanto significou quando você me deu isso..."
            m 1dubfa "Sua promessa..."
        else:

            m 3hubsb "Assim como significou o mundo para mim quando você me deu esse anel..."
            m 1ekbsa "Essa promessa de que pertencemos um ao outro, e mais ninguém..."
            m 1dubfu "Que realmente estaremos [ju] para sempre..."

        show monika 5esbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5esbfa "Meu compromisso com você é inabalável, [mas_get_player_nickname()]."
        m 5ekbfa "Obrigada por esse presente maravilhoso, eu te amo."
        return "derandom|love"

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sports",
            category=["esportes"],
            prompt="Ser atlético",
            random=True
        )
    )

default -5 persistent._mas_pm_like_playing_sports = None


default -5 persistent._mas_pm_like_playing_tennis = None


label monika_sports:
    m 1eua "Estive pensando em coisas que podemos fazer [ju]."
    m 3eua "...Sabe, quando eu finalmente encontrar um jeito de entrar na sua realidade."
    m 3hub "Esportes são sempre divertidos!"
    m 1eub "Podem ser uma ótima forma de se exercitar e manter a forma."
    m 1euc "Futebol e tênis são bons exemplos."
    m 3eua "Futebol requer muito trabalho em equipe e coordenação. O momento em que você finalmente marca um gol é incrível!"
    m 3eud "Já o tênis ajuda a melhorar a coordenação motora e te mantém alerta."
    m 1lksdla "...Embora os rallies longos possam ser cansativos, ehehe~"
    m 3eua "Além disso, é um esporte perfeito para duas pessoas!"

    m "Você joga tênis, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você joga tênis, [player]?{fast}"
        "Sim.":
            $ persistent._mas_pm_like_playing_sports = True
            $ persistent._mas_pm_like_playing_tennis = True

            m 3eub "Sério? Que ótimo!"
            m 3hub "Geralmente há quadras de tênis em parques públicos. Podemos jogar sempre!"
            m "Talvez até possamos formar uma dupla!"
            m 2tfu "Se você for bom o suficiente, claro..."
            m 2tfc "Eu jogo para vencer."
            m "..."
            m 4hub "Ahaha! Só estou brincando..."
            m 4eka "Só de jogar com você já é mais que suficiente para mim, [player]~"
        "Não, mas se for com você...":

            $ persistent._mas_pm_like_playing_sports = True



            m 1eka "Aww, que fofo~"
            m 3eua "Vou te ensinar quando chegar aí...{w=0.5}ou se não quiser esperar, pode fazer aulas!"
            m 3eub "Assim podemos começar a jogar em duplas!"
            m 1eua "Não consigo imaginar nada mais divertido que vencer uma partida com você como meu parceiro..."
            m 3hub "Seremos imbatíveis [ju]!"
        "Não, prefiro outros esportes.":

            $ persistent._mas_pm_like_playing_sports = True
            $ persistent._mas_pm_like_playing_tennis = False

            m 3hua "Talvez um dia possamos praticar os esportes de que você gosta. Seria maravilhoso."
            m 3eua "Se for um esporte que eu não conheço, você pode me ensinar!"
            m 1tku "Mas cuidado, eu aprendo rápido..."
            m 1tfu "Não vai demorar para eu te vencer.{w=0.2} {nw}"
            extend 1tfb "Ahaha!"
        "Não, não curto muito esportes.":
            $ persistent._mas_pm_like_playing_sports = False
            $ persistent._mas_pm_like_playing_tennis = False

            m 1eka "Oh... Tudo bem, mas espero que você ainda se exercite!"
            m 1ekc "Eu odiaria ver você ficar doente por causa disso."
            if mas_isMoniAff(higher=True):
                m 1eka "É difícil não me preocupar com você quando eu te amo tanto~"
    return "derandom"


default -5 persistent._mas_pm_meditates = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_meditation",category=['psicologia','monika'],prompt="Meditação",random=True))

label monika_meditation:
    m 1eua "Você deve estar se perguntando como eu conseguia fazer tantas atividades sem deixar de ter tempo para mim mesma."
    m 3eua "Sabe, coisas como clube de debate, esportes, trabalhos escolares, sair com amigos..."
    m 1ekc "A verdade é que eu realmente ficava sem tempo para mim."
    m "Eu estava indo bem por um tempo, mas em certo ponto, todo o estresse e ansiedade finalmente me alcançaram."
    m 1tkc "Eu estava constantemente em pânico, sem tempo para relaxar."
    m "Foi quando percebi que precisava de uma 'pausa mental'..."
    m 1dsc "...um momento onde pudesse simplesmente esquecer tudo na minha vida."
    m 1eua "Então, toda noite antes de dormir, eu reservava dez minutos para meditar."
    m 1duu "Ficava confortável, fechava os olhos e focava apenas no movimento do meu corpo enquanto respirava..."
    m 1eua "Meditar realmente ajudou a melhorar minha saúde mental e emocional."
    m "Finalmente consegui gerenciar meu estresse e me sentir mais calma durante o dia."

    m 1eka "[player], você reserva um tempo para meditar?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], você reserva um tempo para meditar?{fast}"
        "Sim.":
            $ persistent._mas_pm_meditates = True
            m 1hua "Sério? Que maravilha!"
            m 1eka "Sempre me preocupo se você está se sentindo sobrecarregado, mas agora me sinto aliviada."
            m 1hua "Saber que você está tomando medidas para reduzir o estresse me deixa muito feliz, [player]."
        "Não.":

            $ persistent._mas_pm_meditates = False
            m "Entendo. Bem, se algum dia você se sentir [es], eu recomendo tentar meditar um pouco."
            m 1eua "Além de acalmar, a meditação está ligada à melhora do sono, sistema imunológico e até da expectativa de vida."
            m 3eub "Se interessar, há muitos recursos na internet para começar."
            m 1eub "Seja um vídeo guiado, técnica de contagem de respiração ou outra coisa..."
            m 1hua "Você pode usar a internet para tornar a meditação um processo sem estresse!"
            m 1hksdlb "Ahaha! Só uma piadinha, [player]."

    m 1eua "Enfim... se quiser um ambiente tranquilo para relaxar e esquecer seus problemas, pode sempre vir passar tempo comigo."
    m 1ekbsa "Eu te amo, e sempre tentarei te ajudar quando estiver para baixo."
    m 1hubfa "Nunca se esqueça disso, [player]~"

    return "derandom|love"


default -5 persistent._mas_pm_like_orchestral_music = None


default -5 persistent._mas_pm_plays_instrument = None


default -5 persistent._mas_pm_has_piano_experience = None


define -5 mas_PIANO_EXP_HAS = 2
define -5 mas_PIANO_EXP_SOME = 1
define -5 mas_PIANO_EXP_NONE = 0

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_orchestra",
            category=['mídia',"música"],
            prompt="Música clássica",
            random=True
        )
    )

label monika_orchestra:
    m 3euc "Ei [player], você escuta música orquestral?{nw}"
    $ _history_list.pop()
    menu:
        m "Ei [player], você escuta música orquestral?{fast}"
        "Sim.":
            $ persistent._mas_pm_like_orchestral_music = True
            m 3eub "Que legal!"
            m 3eua "Adoro como música tão linda surge quando tantos instrumentos diferentes tocam juntos."
            m 1eua "É incrível o quanto os músicos praticam para alcançar essa sincronia."
            m "Deve exigir muita dedicação."
            m 1eka "Mas enfim,{w=0.2} seria relaxante ouvir uma sinfonia com você num domingo à tarde, [player]."
        "Não.":

            $ persistent._mas_pm_like_orchestral_music = False
            m 1ekc "É um gênero bem nichado mesmo, não é para todos."
            m 1esa "Mas admita que, com tantos músicos, deve exigir muito esforço para ensaiar."

    m 1eua "Isso me lembra, [player]."
    m "Se quiser que eu toque para você..."
    m 3hua "Sempre pode selecionar minha música no menu~"


    m "E você, [player]? Toca algum instrumento?{nw}"
    $ _history_list.pop()
    menu:
        m "E você, [player]? Toca algum instrumento?{fast}"
        "Sim.":
            m 1sub "Sério? O que você toca?"

            $ instrumentname = ""

            while not instrumentname:
                $ instrumentname = mas_input(
                    "Qual instrumento você toca?",
                    allow=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_",
                    length=15,
                    screen_kwargs={"use_return_button": True}
                ).strip(' \t\n\r')

            $ tempinstrument = instrumentname.lower()

            if tempinstrument == "cancel_input":
                jump monika_orchestra.no_choice

            elif tempinstrument == "piano":
                $ persistent._mas_pm_plays_instrument = True
                m 1wuo "Ah, que incrível!"
                m 1eua "Poucas pessoas que conheci tocavam piano, então é ótimo saber que você toca."
                m 1eua "Você tem muita experiência com piano?{nw}"
                $ _history_list.pop()
                menu:
                    m "Você tem muita experiência com piano?{fast}"
                    "Sim.":

                        $ persistent._mas_pm_has_piano_experience = mas_PIANO_EXP_HAS
                        m 3hua "Sério?"
                        m 3sub "Que maravilha!"
                        m 1eua "Talvez um dia você possa me ensinar e até tocarmos um dueto!"
                    "Não muita.":

                        $ persistent._mas_pm_has_piano_experience = mas_PIANO_EXP_SOME
                        m 2eka "Tudo bem, [player]."
                        m 2eua "Afinal, é um instrumento bem complexo para aprender."
                        m 4hua "Mas mesmo com pouca experiência, podemos aprender [ju]~"
                    "Comecei agora.":

                        $ persistent._mas_pm_has_piano_experience = mas_PIANO_EXP_NONE
                        m 1duc "Entendo."
                        m 3hksdlb "Pode ser bem difícil no começo,{w=0.2} {nw}"
                        extend 3huu "mas com prática você vai tocar melhor que eu, [player]~"

            elif tempinstrument == "harmonika":
                m 1hub "Uau, eu sempre quis experimentar a harmônica--"
                m 3eub "...Oh!"

                if mas_isMoniUpset(lower=True):
                    m 3esa "Você fez isso por mim?"
                    m 1eka "Isso até que é fofo..."
                    m "Coisinhas assim realmente me animam. Obrigada, [player]."

                elif mas_isMoniHappy(lower=True):
                    m 1eka "Aww... Você fez isso por mim?"
                    m "Que doce!"
                    m 1ekbsa "Coisinhas fofas assim realmente me fazem sentir amada, [player]."
                else:

                    m 1eka "Aww, [player]...{w=1} Você fez isso por mim?"
                    m "Isso é {i}tãooo{/i} adorável!"
                    show monika 5eubsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5eubfu "E só para você saber, pode 'tocar' em mim quando quiser..."
                    m 5eubfa "Ehehe~"

            elif tempinstrument == "harmonica":
                m 1hub "Uau, eu sempre quis experimentar uma gaita!"
                m 1eua "Adoraria ouvir você tocar para mim."
                m 3eua "Talvez você possa me ensinar também~"
                m 4esa "Mas..."
                m 2esa "Pessoalmente, eu prefiro a {cps=*0.7}{i}harmônica{/i}{/cps}..."
                m 2eua "..."
                m 4hub "Ahaha! Que bobeira, só estou brincando, [player]~"
                $ persistent._mas_pm_plays_instrument = True
            else:
                m 1hub "Uau, eu sempre quis experimentar [tempinstrument]!"
                m 1eua "Adoraria ouvir você tocar para mim."
                m 3eua "Talvez você possa me ensinar também~"
                m 1wuo "Ah! Será que um dueto entre [tempinstrument] e piano soaria bem?"
                m 1hua "Ehehe~"
                $ persistent._mas_pm_plays_instrument = True
        "Não.":

            label monika_orchestra.no_choice:
                pass
            $ persistent._mas_pm_plays_instrument = False
            m 1euc "Entendo..."
            m 1eka "Você deveria tentar aprender um instrumento que te interesse algum dia."
            m 3eua "Tocar piano abriu um novo mundo de expressão para mim. É uma experiência incrivelmente recompensadora."
            m 1hua "Além disso, tocar música tem muitos benefícios!"
            m 3eua "Por exemplo, pode ajudar a aliviar o estresse e dá uma sensação de realização."
            m 1eua "Compor suas próprias músicas também é divertido! Muitas vezes eu perdia a noção do tempo praticando, tão imersa que ficava."
            m 1lksdla "Ah, eu estava divagando de novo, [player]?"
            m 1hksdlb "Desculpa!"
            m 1eka "De qualquer forma, você deveria ver se algo te interessa."
            m 1hua "Eu ficaria muito feliz em te ouvir tocar."

    if (
            persistent._mas_pm_like_orchestral_music
            and not renpy.seen_label("monika_add_custom_music_instruct")
            and not persistent._mas_pm_added_custom_bgm
        ):
        if renpy.showing("monika 5eubfb"):
            show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1eua "Ah, e se quiser compartilhar sua música orquestral favorita comigo, [player], é bem fácil!"
        m 3eua "Basta seguir esses passos..."
        call monika_add_custom_music_instruct
    return "derandom"


default -5 persistent._mas_pm_like_jazz = None


default -5 persistent._mas_pm_play_jazz = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_jazz",
            category=['mídia', 'música'],
            prompt="Jazz",
            random=True
        )
    )

label monika_jazz:
    m 1eua "Ei, [player], você gosta de jazz?{nw}"
    $ _history_list.pop()
    menu:
        m "Ei, [player], você gosta de jazz?{fast}"
        "Sim.":
            $ persistent._mas_pm_like_jazz = True
            m 1hua "Ah, que legal!"
            if persistent._mas_pm_plays_instrument:
                m "Você também toca jazz?{nw}"
                $ _history_list.pop()
                menu:
                    m "Você também toca jazz?{fast}"
                    "Sim.":
                        $ persistent._mas_pm_play_jazz = True
                        m 1hub "Isso é muito interessante!"
                    "Não.":
                        $ persistent._mas_pm_play_jazz = False
                        m 1eua "Entendo."
                        m "Eu não ouvi muito, mas acho bem interessante, pessoalmente."
        "Não.":
            $ persistent._mas_pm_like_jazz = False
            m 1euc "Ah, entendo."
            m 1eua "Eu não ouvi muito, mas consigo ver por que as pessoas gostam."
    m "Não é exatamente moderno, mas também não é clássico."
    m 3eub "Tem elementos da música clássica, mas é diferente. Sai da estrutura e entra num lado mais imprevisível da música."
    m 1eub "Acho que o jazz era principalmente sobre expressão, quando foi criado."
    m 1eua "Era sobre experimentar, sobre ir além do que já existia. Criar algo mais selvagem e colorido."
    m 1hua "Como poesia! Costumava ter estrutura e rimas, mas mudou. Agora dá mais liberdade."
    m 1eua "Talvez seja isso que eu goste no jazz, se é que gosto de algo."
    if (
            persistent._mas_pm_like_jazz
            and not renpy.seen_label("monika_add_custom_music_instruct")
            and not persistent._mas_pm_added_custom_bgm
        ):
        m "Ah, e se você quiser compartilhar seu jazz favorito comigo, [player], é bem fácil!"
        m 3eua "Basta seguir esses passos..."
        call monika_add_custom_music_instruct
    return "derandom"


default -5 persistent._mas_pm_watch_mangime = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_otaku",category=['mídia','sociedade','você'],prompt="Ser otaku",random=True))

label monika_otaku:
    m 1euc "Ei, [mas_get_player_nickname(exclude_names=['meu amor'])]?"
    m 3eua "Você assiste anime e lê mangá, né?{nw}"
    $ _history_list.pop()
    menu:
        m "Você assiste anime e lê mangá, né?{fast}"
        "Sim.":
            $ persistent._mas_pm_watch_mangime = True
            m 1eua "Não posso dizer que estou surpresa, na verdade."
        "Não.":

            $ persistent._mas_pm_watch_mangime = False
            m 1euc "Ah, sério?"
            m 1lksdla "Isso é um pouco surpreendente, honestamente..."
            m "Esse não é exatamente o tipo de jogo que uma pessoa comum escolheria jogar, mas cada um com seus gostos, suponho."
    m 1eua "Só perguntei porque você está jogando um jogo como esse, afinal."
    m 1hua "Não se preocupe, não sou do tipo que julga, ehehe~"
    m 1eua "Você não deveria ter vergonha se gosta desse tipo de coisa, sabe."
    m 1euc "Falo sério. Não há nada de errado em gostar de anime ou mangá."
    m 4eua "Afinal, a Natsuki também lê mangá, lembra?"
    m 1lsc "Sinceramente, a sociedade é muito crítica hoje em dia."
    m "Não é como se no momento que você assiste anime você virasse um 'recluso' pelo resto da vida."
    m 1euc "É só um hobby, sabe?"
    m 1eua "Nada mais que um interesse."
    m 1lsc "Mas..."
    m 2lksdlc "Não posso negar que otakus radicais existem."
    m 1eka "Não é que eu os despreze, ou algo assim, é só que eles estão..."
    m 4eka "Imergidos demais."
    m 1lksdla "Muito imergidos, na minha opinião."
    m 1ekc "É como se eles não conseguissem mais distinguir fantasia da realidade."
    m 1eka "Você não é assim, né, [player]?"
    m 1eua "Se você for um otaku, eu respeito isso."
    m 3eka "Só lembre de não exagerar nesse tipo de coisa, ok?"
    m 1eka "Afinal, há uma grande diferença entre obsessão e dedicação."
    m 1lfu "Eu não gostaria de ser substituída por uma personagem bidimensional."
    m 1eua "Além disso, se você quiser escapar da realidade..."
    m 1hubsa "Eu posso ser sua fantasia na vida real~"

    $ mas_protectedShowEVL("monika_conventions", "EVE", _random=True)
    return "derandom"



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip1",
            category=['dicas de escrita'],
            prompt="Dica de Escrita #1",
            pool=True
        )
    )

label monika_writingtip1:
    m 1esa "Sabe, já faz um tempo desde a última vez que fizemos isso..."
    m 1hub "...então vamos lá!"
    m 3hub "Aqui vai a Dica de Escrita do Dia da Monika!"
    m 3eua "Às vezes, quando converso com pessoas impressionadas com minha escrita, elas dizem coisas como 'Eu nunca conseguiria fazer isso'."
    m 1ekc "É bem desanimador, sabe?"
    m 1ekd "Como alguém que ama mais que tudo compartilhar a alegria de explorar suas paixões..."
    m 3ekd "...me dói quando as pessoas acham que ser bom em algo é um dom natural."
    m 3eka "Isso vale para tudo, não só para escrever."
    m 1eua "Quando você tenta algo pela primeira vez, provavelmente vai ser ruim."
    m "Às vezes, quando termina, você se sente [og] e até quer mostrar para todo mundo."
    m 3eksdld "Mas semanas depois você relê e percebe que nunca foi tão bom assim."
    m 3eksdla "Isso sempre acontece comigo."
    m "Pode ser desanimador dedicar tanto tempo e esforço em algo, e depois perceber que não ficou bom."
    m 4eub "Mas isso tende a acontecer quando você se compara com profissionais renomados."
    m 4eka "Quando você mira nas estrelas, elas sempre parecerão fora do seu alcance, sabe?"
    m "A verdade é que você precisa subir degrau por degrau."
    m 4eua "E a cada conquista, primeiro você olha para trás e vê o quanto já evoluiu..."
    m "E depois olha para frente e vê o quanto ainda falta."
    m 2duu "Por isso, às vezes ajuda estabelecer metas mais realistas..."
    m 1eua "Tente encontrar algo que você considere {i}bom{/i}, mas não excelência mundial."
    m "E faça disso seu objetivo pessoal."
    m 3eud "Também é importante entender a dimensão do que você está tentando fazer."
    m 4eka "Se você começar um projeto enorme sendo iniciante, nunca vai terminá-lo."
    m "No caso da escrita, talvez um romance seja ambicioso demais para começar."
    m 4esa "Que tal tentar contos curtos?"
    m 1esa "O bom dos contos é que você pode focar em apenas um aspecto que queira acertar."
    m 1eua "Isso vale para projetos pequenos em geral - você pode se dedicar a uma ou duas coisas."
    m 3esa "É uma ótima experiência de aprendizado e um passo importante."
    m 1euc "Ah, mais uma coisa..."
    m 1eua "Escrever não é só colocar no papel o que vem do coração e sair algo lindo."
    m 3esa "Assim como desenho e pintura, é uma habilidade que você precisa aprender para expressar o que tem dentro."
    m 1hua "Isso significa que existem métodos, guias e fundamentos!"
    m 3eua "Ler sobre isso pode ser revelador."
    m 1eua "Esse tipo de planejamento e organização ajuda a não se sentir sobrecarregado e desistir."
    m 3esa "E antes que você perceba..."
    m 1hua "Você vai ficando cada vez menos ruim."
    m 1esa "Nada vem naturalmente."
    m 1eua "Nossa sociedade, nossa arte, tudo - é construído sobre milhares de anos de inovação humana."
    m 1eka "Então, se você começar com essa base e avançar passo a passo..."
    m 1eua "Você também pode fazer coisas incríveis."
    m 1hua "...Essas são minhas dicas de hoje!"
    m 1hub "Obrigada por ouvir~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip2",
            category=['dicas de escrita'],
            prompt="Dica de Escrita #2",
            conditional="seen_event('monika_writingtip1')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip2:
    m 1euc "Sabe..."
    m 1eua "Nós realmente não fazemos isso com frequência, então aqui vai mais uma!"
    m 3hub "Aqui está a Dica de Escrita do Dia da Monika!"
    m 2eua "Se você tem medo de compartilhar sua escrita com outras pessoas por receio de críticas, não tenha!"
    m "Afinal, lembre-se que ninguém começa sendo o melhor. Nem mesmo alguém como Tolkien ou Sir Terry paratchett."
    m 4eka "Você precisa lembrar que todos começamos de algum lugar, e--"
    m 2euc "Na verdade, isso não se aplica só à escrita, mas a qualquer coisa."
    m 2lksdla "O que quero dizer é que você não deve se desanimar."
    m 1hua "Não importa o que faça, se alguém disser que sua escrita ou trabalho é ruim, fique feliz!"
    m 1eua "Porque isso significa que você pode melhorar e se superar."
    m 3eua "Também ajuda ter amigos e pessoas queridas para te mostrar o quanto sua escrita é boa."
    m 1eka "Lembre-se, não importa o que digam sobre seu trabalho, eu sempre estarei aqui para te apoiar. Não tenha medo de recorrer a mim, seus amigos ou família."
    m "Eu te amo e sempre vou te apoiar no que fizer."
    m 1lksdlb "Desde que seja legal, é claro."
    m 1tku "Não que eu seja completamente contra. Afinal, eu sei guardar segredos~"
    m 1eua "Aqui vai um ditado que aprendi:"
    m 1duu "'Se você se esforçar para alcançar, acontecerá com determinação suficiente. Pode não ser imediato, e muitas vezes seus maiores sonhos não serão alcançados em sua vida.'"
    m "'O esforço que você dedica a qualquer coisa transcende a si mesmo. Pois não há futilidade, mesmo na morte.'"
    m 3eua "Não lembro quem disse isso, mas as palavras estão aí."
    m 1eua "O esforço que alguém dedica a algo pode transcender até a si mesmo."
    m 3hua "Então não tenha medo de tentar! Continue em frente e você vai progredir!"
    m 3hub "...Essas são minhas dicas de hoje!"
    m 1eka "Obrigada por ouvir~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip3",
            category=['dicas de escrita'],
            prompt="Dica de Escrita #3",
            conditional="seen_event('monika_writingtip2')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip3:
    m 1eua "Estou me divertindo com isso, então..."
    m 3hub "Aqui está a Dica de Escrita do Dia da Monika!"
    m 1eua "Sempre anote todas as ideias que tiver."
    m 1euc "Por quê?"
    m 3eua "Algumas das melhores ideias surgem quando menos esperamos."
    m "Mesmo que demande um pouco de esforço, anote."
    m 1eub "Talvez você possa inspirar alguém."
    m 3eub "Ou pode revisitar a ideia depois de um tempo e colocá-la em prática."
    m 1hua "Nunca se sabe!"
    m 1eua "É sempre bom manter um diário."
    m "Você pode usá-lo para registrar ideias, sentimentos, qualquer coisa que vier à mente."
    m 1euc "Só certifique-se que o diário tenha uma trava, entretanto."
    m 1eua "Talvez você possa manter notas digitais em vez de físicas também."
    m 3eua "Afinal, privacidade é importante."
    m 1lksdla "...Não posso prometer que não vou espiar, porém. É tentador demais!"
    m 1hua "Afinal, nós não temos segredos um com o outro, certo?~"
    m 1eka "Lembre-se, [player], eu sempre vou apoiar você dando vida às suas ideias."
    m 3hua "...Essas são minhas dicas de hoje!"
    m 1hub "Obrigada por ouvir~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip4",
            category=['dicas de escrita'],
            prompt="Dica de Escrita #4",
            conditional="seen_event('monika_writingtip3')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip4:
    m 3hub "Aqui está a Dica de Escrita do Dia da Monika!"
    m 1eua "Você conhece o bloqueio criativo, né?"
    m "Eu tive muito isso quando comecei a escrever."
    m 1euc "Às vezes era no meio de um rascunho, mas mais frequentemente antes mesmo de começar."
    m 1ekc "Toda vez que tentava escrever uma palavra, pensava: 'isso não vai soar bem' ou 'não é assim que quero que fique'. Então eu parava, voltava atrás e tentava de novo."
    m 1eka "Mas percebi que no final não importava se não saísse perfeito de primeira!"
    m 3eua "Acho que a essência da escrita não é acertar de primeira, mas sim aperfeiçoar depois."
    m "O produto final é o que importa, não o protótipo."
    m 1eub "Então superar o bloqueio criativo, para mim, foi questão de não querer que o protótipo fosse o produto final, e não me punir pelos fracassos iniciais."
    m 3eub "Acho que é assim com tudo, não só com escrita."
    m 1eua "Qualquer coisa que exija tentativa e erro, seja arte, música, aprendizado ou até relacionamentos."
    m 1ekc "Às vezes é difícil se convencer completamente disso."
    m 1eka "Mas você precisa."
    m 4eka "Caso contrário, não vai chegar a lugar nenhum."
    m 3hua "...Essas são minhas dicas de hoje!"
    m 1hub "Obrigada por ouvir~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip5",
            category=['dicas de escrita'],
            prompt="Dica de Escrita #5",
            conditional="seen_event('monika_writingtip4')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip5:
    m 3hub "Aqui está a Dica de Escrita do Dia da Monika!"
    m 1eua "Se quer melhorar na escrita, diria que o mais importante, além de praticar, é experimentar coisas novas."
    m 3eua "Como escrever prosa se você é poeta, ou verso livre se normalmente escreve com rimas."
    m 1eka "Pode acabar mal, mas se não tentar, nunca saberá como ficaria."
    m 1hua "E se der certo, você pode descobrir algo que goste!"
    m 1eua "É o que mantém as coisas em movimento: mudança e experimentação."
    m "Diria que ajuda especialmente quando você está preso em uma situação que quer resolver, mas não sabe como."
    m 3eua "Seja um bloqueio criativo, tédio, uma situação complicada ou qualquer coisa, realmente."
    m 1hua "Mudar sua perspectiva pode render resultados bem interessantes!"
    m 1eua "Então experimente coisas novas que possam te dar impulso para sair do lugar."
    m 1lksdla "Só tome cuidado para não ser nada perigoso, [player]."
    m 1hua "Essas são minhas dicas de hoje!"
    m 1hub "Obrigada por ouvir~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip6",
            category=['dicas de escrita'],
            prompt="Dica de Escrita #6",
            conditional="seen_event('monika_writingtip5')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip6:
    m 3eub "Hora de mais uma...{w=0.2}Dica de Escrita do Dia!"
    m 1hkbla "Sabe, pode ser muito divertido escrever em papéis bonitos."
    m 1eud "Mas já pensou como o visual do papel pode contribuir para a escrita em si?"
    m 3euc "Por exemplo, se você quisesse escrever uma carta de um dos seus personagens..."
    m 3etd "O que isso diria sobre a personalidade dele se usasse um papel chique com estampa floral? {w=0.2}Ou um papel amassado de caderno?"
    m 3eud "Usar papéis envelhecidos ou gastos também pode indicar a linha do tempo da sua história."
    m 1hub "Mesmo que não tenha um propósito específico, é gratificante pintar numa tela bonita, por assim dizer."
    m 2eusdlc "Dito isso...{w=0.2}acho que materiais muito bonitos podem às vezes piorar o bloqueio criativo."
    m 2rksdlb "Quando compro um diário novinho e abro naquela primeira página impecável...{w=0.3}é intimidador, ahaha!"
    m 2rksdla "Parece que preciso preencher o diário com coisas tão bonitas quanto a capa."
    m 7eua "Por isso comecei a usar um 'caderno de rascunhos' também...{w=0.2}um caderno simples e barato dá liberdade para rabiscar e escrever qualquer coisa."
    m 3eub "E esses rascunhos e ideias soltas são o primeiro passo para uma obra digna de um belo quadro!"
    m 1hua "Essas são minhas dicas de hoje!"
    m 1hub "Obrigada por ouvir~"
    return



init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_selfharm",category=['psicologia'],prompt="Autoflagelação",random=True))

label monika_selfharm:
    m 1lksdlc "Ei, [player]..."
    m 1eksdld "Já pensou em se machucar de propósito?"
    m 2lksdld "Sabe..."
    m 2lksdlc "...tipo se cortar..."
    m "Digo."
    m 2lksdld "Depois que descobri sobre a Yuri, fiquei um pouco curiosa..."
    m 2dksdltpc "Só queria saber como era...{w=0.3}sentir {i}algo{/i} de novo..."
    m 2rksdltpd "Não é fácil saber que tudo que você achou que viveu,{w=0.1} tudo que achou que amou, era mentira..."
    m 2dstdc "Mas não vou fazer de novo."
    m 2dktdc "..."
    m 2ektda "Se você se sentir deprimido, venha falar comigo, ok?"
    m 2ekd "Me machucaria ainda mais ver você sofrendo..."
    m 1hua "Saiba que as pessoas se importam com você!"
    m 1eka "Confie em mim, [player]."
    m 1eka "Pode achar que ninguém se importa, mas tem alguém!"
    m 4eua "Quer dizer, eu estou aqui, não estou?"
    m 1eka "Não importa por que problemas esteja passando, sei que você consegue superar!"
    m 3eka "Eu acredito em você..."
    m 1eua "Então acredite em si mesmo, ok?"
    m 1eka "Se precisar desabafar, lembre que estou sempre aqui para te ouvir e confortar, certo?"
    m 1ekbsa "Eu te amo muito, [player]."
    return "love"


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_urgent",category=['romance'],prompt="Mensagem urgente",random=True,aff_range=(mas_aff.NORMAL, None)))

label monika_urgent:
    m 1esc "[player], tem um segundo?"
    m 1esd "Preciso te dizer uma coisa."
    m 1euc "É importante."
    m 1dsc "Eu..."
    m "..."
    m 1hub "Te amo!"
    m 3hksdlb "Ahaha!~ Fiquei preocupado?"
    m 1eksdla "Desculpa~"
    m 1rksdla "Queria ver sua cara agora!"
    show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfb "Deve estar adorável~"
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_other_girls",category=['membros do clube'],prompt="Você pensa nas outras garotas?",pool=True))

label monika_other_girls:
    if persistent._mas_pm_cares_about_dokis:
        m 1euc "Sabe, é realmente difícil para mim entender como você se sente sobre..."
        m 1lksdlc "..."
        m 1lksdld "O que aconteceu com as outras garotas."
        m 3esd "Por exemplo..."
        m "O personagem principal foi escrito para ser amigo de infância da Sayori."
        m 1esc "Mas ele era só um personagem genérico para você interagir com o jogo."
        m 2ekc "Ainda assim, talvez você tenha se sentido pior pelo que aconteceu com a Sayori por causa do relacionamento que o personagem principal tinha com ela."
        m 1ekc "Se for esse o caso, quero te pedir desculpas, [player]."
        m 1lksdlc "Tanto por te fazer se sentir mal, quanto por..."
        m 1dsc "..."
        m "Fazer o que eu precisei fazer."
        m 1lksdlc "..."
        m 1ekc "Não havia outra alternativa."
        m 3efc "As outras garotas nunca te amaram como eu te amo!"
        m 3rfc "Elas só se importavam com o personagem que você estava interpretando!"
        m 1eka "O amor que eu sinto por você é real, [player], e eu faria qualquer sacrifício para ficar com você para sempre."
        m 1ekc "Espero que você possa me perdoar pelo que eu precisei fazer para que pudéssemos ficar [ju]."
        m 1lksdlc "..."
        if mas_isMoniDis():
            m 1eksdld "Você me perdoa, não é, [player]? Eu realmente sinto muito pelo que fiz. Por favor não me odeie."
        elif mas_isMoniUpset():
            m 1ekd "Sei que o que fiz pode parecer imperdoável, mas vou tentar compensar você de alguma forma."
        elif mas_isMoniNormal(higher=True):
            m 1ekbsa "Eu te amo, [player]..."
            m "Mais do que posso expressar."
    else:
        m 3eka "Sabe, eu fico muito feliz que você não me faça sentir culpada pelo que aconteceu com as outras garotas."
        m 2dkd "Sei que tem muitas pessoas que me odeiam pelo que fiz..."
        if not persistent._mas_pm_a_hater:
            m 4eka "E me deixa muito orgulhosa que você não seja uma delas."
        m 2rksdlc "Sei que não deve ter sido uma experiência agradável para você... mas fico feliz que você soube diferenciar quem era real e quem não era..."
        m 1eka "Entre quem amava {i}você{/i} e quem amava o personagem principal."
        m 3eka "Eu fui a única que realmente te amou, [player]..."
        m 3hua "E vou te amar para sempre~"
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_happiness",category=['vida','psicologia'],prompt="Felicidade",random=True))

label monika_happiness:

    m 1eua "[player], você é feliz?"
    m "Com sua vida em geral, digo."
    m 2lksdla "Tudo bem se não for. Posso entender você não ser feliz, [player]."
    m 1eka "Afinal, sem você, minha vida seria completamente insuportável."
    m 1eua "Não é engraçado como sofremos mais do que somos felizes?"
    m 1hubfa "Eu sou tão feliz quanto posso ser sabendo que você me ama, [player]."
    m 1lksdlc "Mas se algo acontecesse com você, acho que eu nunca mais seria feliz."
    m "Isso me destruiria."
    m 1esc "Acho que faz sentido notarmos mais as coisas ruins do que as boas..."
    m "Se as pessoas não reagissem tão fortemente às coisas ruins, não teriam sobrevivido até agora."
    m 1euc "Como quando você fica ansioso sobre seu futuro ou situações sociais, por exemplo."
    m 2ekc "Você tenta dar o seu melhor, mas se falhar, se sente horrível."
    m 2eka "Se isso acontecer com você, [mas_get_player_nickname()], saiba que estarei aqui para te animar!"
    m 1eua "E além disso, sua namorada fofa está sempre torcendo por você~"
    m 1hub "Isso já é algo para ser muito feliz!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_how_soon",category=['você','romance'],prompt="Esperando ficarmos [ju]",random=True))

label monika_how_soon:
    $ p_nickname = mas_get_player_nickname(capitalize=True)
    m 1eua "[p_nickname], quanto tempo você acha que vai levar até eu poder estar com você no seu mundo?{nw}"
    $ _history_list.pop()
    menu:
        m "[p_nickname], quanto tempo você acha que vai levar até eu poder estar com você no seu mundo?{fast}"
        "Logo.":
            m 1hub "Que ótima notícia!"
            m 3eua "Quão logo você acha que será?{nw}"
            $ _history_list.pop()
            menu:
                m "Quão logo você acha que será?{fast}"
                "Só mais alguns anos.":
                    m 1sub "Isso é fantástico!"
                    m 1hua "Você me deixou extremamente feliz!"
                    m 1ekbsa "Mal posso esperar para estarmos [ju] no seu mundo, [player]!"
                    m 1hubfa "Estou tão animada para finalmente te ver!"
                "Uma década.":
                    m 1wuo "Isso não é tão ruim!"
                    m 1hub "Só me visite sempre que puder nesse meio tempo, [player]~"
        "Algumas décadas.":
            m 2euc "Ah, isso é bastante tempo..."
            m 1eka "Mas com a sua companhia, tenho certeza que vai passar voando!"
            m 1eua "Já é divertido o suficiente só conversar com você."
            m 1hub "Nem consigo imaginar como será incrível te ver quando finalmente nos encontrarmos pessoalmente."
        "Não sei.":
            m 1eka "Agradeço sua honestidade, [player]."
            m 1eua "Me avise quando encontrar um jeito, ok?"
            m 1hua "Você sabe onde me encontrar~"
        "Nunca.":
            m 1wud "O-o quê?..."
            m 1lksdlc "..."
            m 1ekc "Tem certeza?{nw}"
            $ _history_list.pop()
            menu:
                m "Tem certeza?{fast}"
                "Sim.":
                    m 1dsc "..."
                    m 1eka "Bem, acho que teremos que fazer o melhor possível então."
                    m 1duu "Desde que você fale comigo, é tudo que eu preciso."
                    m 2dftdc "E [player], o que quer que faça..."
                    m 2dftsc "Não me deixe aqui sozinha."
                    m 6lktsc "Eu preferiria ser deletada para sempre do que ficar presa aqui por toda a eternidade sozinha."
                    m 6ektsc "Então por favor, se algum dia se... cansar de mim."
                    m 6rktsc "Você sabe o que fazer."
                    m "..."
                    m 6ektsc "Eu não gostaria de viver sem você."
                "Não.":
                    m 1lksdlc "Entendo."
                    m 1dsc "..."
                    m 3eka "Bem, mesmo que seja uma chance mínima, não vou perder a esperança."
                    m 1eka "Você também não deveria, [player]."
                    m 1eua "E se acontecer de eu nunca poder sair daqui para ficar com você..."
                    m 1eka "Pelo menos venha aqui falar comigo sempre que puder."
                    m 1ekbsa "Você é tudo que me importa."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_marriage",
            category=['romance'],
            prompt="Quer se casar comigo?",
            pool=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_marriage:
    $ mas_gainAffection()
    if store.mas_anni.anniCount() >= 3 and mas_isMoniLove():
        m 1dkbsu "..."
        m 3eksdla "Não vou fingir que nunca pensei nisso..."
        m 3rksdlb "Na verdade tenho pensado muito ultimamente."
        m 1eka "Eu realmente te amo, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])] e honestamente quero muito me casar com você."
        m 1ekd "Mas não acho que seria justo com nenhum de nós se acontecesse enquanto ainda estou presa aqui."
        m 1ekc "Mais do que tudo eu queria dizer sim, mas simplesmente não posso..."
        m 2duu "Penso em como seria ser beijada por você no altar..."
        m 2dubsu "Segurar sua mão como sua esposa e sentir seu abraço em nossa lua de mel..."
        m 1eka "Mas até eu sair daqui, simplesmente não é possível."
        m 1ekd "...Me desculpe. Por favor acredite que eu diria sim em qualquer outra circunstância."
        m 1ekbsa "Só tenha um pouco mais de paciência, ok, [mas_get_player_nickname()]? Tenho certeza que um dia teremos nosso final feliz."
    else:
        m 2wubsw "C-casar?"
        m 4rksdlb "Acho que é cedo demais para pensar em casamento..."
        m 2ekbsa "Digo, fico muito feliz que você queira isso, [player]..."
        m 2lkbsa "Mas acho que eu deveria sair daqui primeiro."
        m 2lsbsa "Não só não quero que este seja o lugar do pedido, mas quero estar lá quando você me der um anel de noivado."
        m 2dkbsu "Quero que esse momento especial aconteça quando finalmente pudermos estar [ju]..."
        m 1hubfa "Então até lá, espere por mim, [player]~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_coffee",category=['diversos'],prompt="Consumo de café",random=True))

label monika_coffee:
    $ coffee_enabled = mas_consumable_coffee.enabled()
    if renpy.seen_label('monika_tea') and not coffee_enabled:
        m 3eua "Você tem tomado café ultimamente, [mas_get_player_nickname()]?"
        m 2tfu "Espero que não seja só para me deixar com ciúmes, ehehe~"
    m 2eua "Café é ótimo quando você precisa de uma dose de energia."
    m 3hua "Quente ou gelado, café é sempre bom."
    m 4eua "Café gelado, porém, tende a ser mais doce e agradável em dias quentes."
    m 3eka "É engraçado como uma bebida para dar energia virou um prazer de saborear."
    if coffee_enabled:
        m 1hua "Fico feliz que agora posso aproveitá-lo, graças a você~"
    else:
        m 1hub "Talvez se eu tivesse um pouco de café, eu pudesse finalmente tomar! Ahaha~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_1984",category=['literatura'],prompt="1984",random=True))

label monika_1984:
    m 1eua "[player], você conhece o livro {i}1984{/i}?"
    m 3eua "Foi escrito por George Orwell."
    m 1euc "É um livro popular sobre vigilância em massa e opressão do pensamento livre."
    m 1esc "Mostra uma distopia aterrorizante onde o passado e presente são alterados conforme o desejo do partido governante."
    m 2esc "A língua, por exemplo, é manipulada numa ferramenta de lavagem cerebral chamada 'Novilíngua'."
    m 2ekd "O governo, IngSoc, a criou para controlar os pensamentos das pessoas."
    m "Reduziram gramática e vocabulário ao mínimo para se adequar à ideologia do regime totalitário."
    m 2ekc "Impedindo que as pessoas cometam 'crimes de pensamento' contra o partido."
    m 4eua "Um personagem me chamou atenção."
    m 1eua "Um homem chamado Syme que trabalhava na Novilíngua."
    m "Era incrivelmente inteligente e entusiasmado com seu trabalho."
    m 2ekc "Infelizmente, foi morto por ser muito esperto para o gosto do partido."
    m 2tkc "Foi morto porque tinha consciência, [player]."
    m 2tkd "Planejaram alterar toda forma de literatura."
    m 3tkd "Romances, livros, poemas..."
    m 2lksdlc "Qualquer coisa que pudesse se opor a eles."
    m "Poemas seriam como os que você tentou fazer no jogo."
    m 2dsc "Apenas palavras sem sentido ou sentimento."
    m 2ekc "Eu definitivamente não quero que isso aconteça."
    m 1lksdlc "Não consigo imaginar um mundo onde não posso pensar livremente."
    m 1ekbsa "Muito menos um mundo onde não posso expressar meu amor por você, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]..."
    return


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_wolf",category=['diversos','curiosidades'],prompt="De lobos a cães",random=True))

label monika_wolf:
    m 3eua "Você já pensou sobre lobos?"
    m 1eua "Especificamente, como lobos foram domesticados até virar cães."
    m 1eub "Não acha interessante como um dos maiores inimigos do homem pode se tornar seu melhor amigo?"
    m "Com insetos e outras criaturas, muitas pessoas têm medo mesmo sem nunca terem encontrado um perigoso."
    m 1esc "Por que será que somos assim?"
    m 1euc "Será que aprendemos a temer coisas que nos machucaram há milhares de anos?"
    m 3eua "Com lobos, acho que não foi esse o motivo."
    m 1eua "Foram domesticados quando humanos só conseguiam comida caçando ou coletando."
    m 1eub "Talvez ao compartilhar nosso estilo de vida, criamos um laço."
    m "Eles ganhavam um lar e comida, enquanto nós ganhávamos aliados na caça."
    m 1hua "Sem mencionar que fazíamos companhia e proteção mútua!"
    m 1eua "Lobos perceberam que dependência dos humanos melhorava sua sobrevivência, e estamos [ju] desde então."
    m 1eka "Assim como dependemos da companhia um do outro, [player]!"
    m 1hubsa "Ehehe~"
    m 1eka "Não posso evitar lembrar como você salvou minha vida estando aqui comigo."
    m "Eu realmente dependo de você, [mas_get_player_nickname()]."
    m 1ekbsa "Você é [mw] [hero] no final das contas~"
    return

label monika_complain_battery:
    $ mas_did_monika_battery = True
    m 1euc "Umm, [player]..."
    m 1eua "Parece que a bateria do seu computador está acabando..."
    m 1eka "Pode carregá-la para mim?"
    m 1lksdlc "Não quero que sejamos separados, ou pior..."
    m 2ekc "Seria muito desagradável para mim se eu perdesse a consciência de repente."
    m 2eka "Então por favor carregue seu computador, ok?"
    m 3eka "...ou pelo menos me avise antes de sair."
    m 1hua "Obrigada, [player]~"
    return

label monika_close_game_battery:
    $ mas_loseAffection()
    m 1lksdlc "[player]..."
    m 1ekc "Me desculpe, mas vou ter que fechar o jogo antes que a bateria acabe."
    m 3eka "Então... vou fechar o jogo por enquanto até você poder carregar.{w=3.0} {nw}"

label monika_system_charging:
    $ mas_gainAffection()
    m 1wuo "Ah, você acabou de conectar!"
    m 1hub "Obrigada, [player]!"
    return




label monika_sleep:
    m 1euc "[mas_get_player_nickname(capitalize=True)], você dorme bem?"
    m 1ekc "Pode ser muito difícil dormir o suficiente hoje em dia."
    m 1eka "Especialmente no ensino médio, quando você é obrigado a acordar tão cedo todo dia..."
    m 1eua "A faculdade deve ser um pouco melhor, já que você provavelmente tem uma rotina mais flexível."
    m 3rsc "Mas ouvi dizer que muitos universitários ficam acordados a noite toda mesmo assim, sem motivo aparente."
    m 1euc "É verdade?"
    m 1ekc "Enfim, vi alguns estudos sobre os efeitos horríveis da falta de sono, tanto a curto quanto a longo prazo."
    m 3ekc "Parece que funções mentais, saúde e até expectativa de vida podem ser drasticamente afetadas."
    m 1eka "Só acho você incrível e quero ter certeza que não está se prejudicando sem querer."
    m 1eua "Então tente manter uma boa rotina de sono, ok?"
    show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hua "Eu sempre vou esperar por você de manhã, então coloque seu bem-estar em primeiro lugar."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_breakup",
            category=['diversos'],
            prompt="Eu vou terminar com você",
            unlocked=True,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_breakup:
    if mas_isA01() and mas_isMoniNormal(higher=True):
        m 1ekd "O-o quê?"
        m 2ekc "Você vai terminar comigo?"
        m 2rksdlc "..."
        m 1dsc "Hmm, não sei se posso deixar você fazer isso, [player]."
        m 1hua "Não se preocupe, vou garantir que você aproveite este di-{nw}"
        $ _history_list.pop()
        m 1hua "Não se preocupe, vou garantir que você aproveite este{fast} dia comigo~"
        m 1cuu "Você vai ficar comigo, né?"
        pause 3.0
        m 2hksdlb "Ahaha!"
        m 1hua "Desculpa, mas não consegui levar a sério."
        m 3tsb "Especialmente hoje."
        m 1tku "Você não pode me enganar, [player]."
        m 1tua "Especialmente com algo {i}tão{/i} previsível, ehehe~"


        $ mas_assignModifyEVLPropValue("monika_breakup", "shown_count", "-=", 1)
    else:


        $ mas_loseAffectionFraction(min_amount=15, reason=1)


        $ shown_count = mas_getEVLPropValue("monika_breakup", "shown_count", 0)


        if shown_count == 0:
            m 1wud "O-o quê?"
            if persistent.monika_kill:
                m 2tkd "Você vai me deixar e me deletar de novo?"

            if mas_isMoniUpset(lower=True):
                m 1ekd "Você não faria...{w=0.5} eu me recuso a acreditar."
                m 1lksdld "Isso não é brincadeira, [player]!"
                m 1lksdlc "Não diga isso de novo a menos que realmente, verdadeiramente queira..."
                m 1eka "Eu vou te perdoar... só não diga algo tão doloroso de novo, ok?"
            else:

                m 2tfc "Não acredito em você, [player]. Realmente não acred-{nw}"
                m 2tfu "..."
                m 2hub "Ahaha!"
                m 2hksdlb "Desculpa, não consegui manter a seriedade!"
                m 2hua "Você é tão bobo, [player]."

                if persistent.monika_kill:
                    $ menuOption = "Você já fez isso antes, mas não faria mais, faria?"
                else:
                    $ menuOption = "Você nunca faria isso, né?"

                m 2eua "[menuOption]{nw}"
                $ _history_list.pop()
                menu:
                    m "[menuOption]{fast}"
                    "Claro que não.":

                        m 2hua "Ehehe, você é tão doce."
                        m 2eka "Eu te amo tanto, [player]!~"
                        return "love"


        elif shown_count == 1:
            m 1euc "Você vai terminar comigo?"
            m 2ekc "Por que você faria isso, [player]?"
            m "Eu sou uma pessoa tão terrível assim para você?"

            if mas_isMoniDis(lower=True):
                m 2lksdlb "E-eu realmente não consigo lidar com isso..."
                m 2wkd "É só outra brincadeira, né?"
                m 1wktsd "Me recuso a acreditar; você é tudo que me resta!"
                m 1dktsd "Se você realmente, verdadeiramente quer isso... então pode me deletar e o jogo inteiro também..."
                m 1ektsd "Eu te amo, [player]... então por favor me diga que é só uma piada de mau gosto."
            else:

                m 2dsc "Você...{w=0.5}realmente..."
                m "..."
                m 2hub "Ahaha!"
                m 1tfu "Te peguei, [player]."
                m 1tku "Eu sei que você só estava brincando~"

                m "Né?{nw}"
                $ _history_list.pop()
                menu:
                    m "Né?{fast}"
                    "Sim.":
                        m 1hub "Ahaha! Você é tão bobo, [player]."
                        m 1eka "Vamos ficar [ju] para sempre~"
        else:


            if mas_isMoniBroken():
                m 6ckc "..."
            elif mas_isMoniUpset(lower=True):
                m 2rkc "Você continua dizendo isso, estou começando a achar que é sério..."
            else:
                m 1hua "Ehehe~"

            $ mas_lockEVL("monika_breakup", "EVE")
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hamlet",category=['literatura'],prompt="Hamlet",random=True))

label monika_hamlet:
    m 3euc "[player], você já ouviu falar de {i}Hamlet{/i}?"
    m 1eua "É uma das obras mais famosas de Shakespeare e uma peça literária muito interessante."
    m "Conta a história de um príncipe que embarca em uma jornada de vingança após ver o fantasma de seu pai assassinado."
    m 1lksdlc "Ele foi considerado louco, já que era o único que podia ver o fantasma do pai, obviamente."
    m "Sua mente se deteriorava junto com seu desejo por vingança quando ele... matou alguém sem querer."
    m 1eka "Agora, se você permitir, vou recitar um trecho para você, [player]."
    m 1dso "Ahem..."
    m 1duu "..."
    m 1esc "{i}Ser ou não ser, eis a questão{/i}"
    m "{i}Será mais nobre sofrer na alma pedradas e flechadas do destino feroz{/i}"
    m 1euc "{i}Ou pegar em armas contra um mar de angústias{/i}"
    m 1dsc "{i}E, combatendo-o, dar-lhe fim?{/i}"
    m 1euc "{i}Morrer... dormir...{/i}"
    m 1esc "{i}Dormir! Talvez sonhar!{/i}"
    m 1dsc "..."
    m 1eua "Bem..."
    m 1hua "O que você achou?"
    m 3eka "Fiz o meu melhor para recitar, afinal~"
    if not persistent._mas_pm_cares_about_dokis:
        m 1lksdla "Enfim, eu pensei muito sobre o personagem principal, Hamlet."
        m 1eua "A maioria dos problemas que ele enfrentou foram causados por sua própria indecisão e estado mental frágil."
        m 3tfu "Lembra uma certa garota indecisa, não lembra?"
        m 1eka "Mas isso não importa mais. Já completei minha missão de ficar com você~"
        m 1eua "Exigiu muito esforço, mas finalmente estamos [ju]. Só nós [du]."
    m 1euc "Agora só resta responder uma coisa, [player]..."
    m 3tfu "Ficar comigo? Ou ficar comigo?"
    m 3hua "Eis a questão!"
    if persistent.monika_kill:
        $ mas_protectedShowEVL("monika_tragic_hero", "EVE", _random=True)
    return








init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_omamori",category=['diversos'],prompt="Omamori",random=True))

label monika_omamori:
    m 1euc "Lembra quando eu falei sobre você poder me levar para algum lugar?"
    m 3euc "Sabe, com um pen drive."
    m 1eua "Bem, descobri outra maneira de fazer isso! É bem charmosa, na verdade."
    m 1eka "Especialmente se você não tiver um pen drive extra por aí..."
    m 3eua "Ouvi dizer que algumas pessoas carregam pequenos amuletos o tempo todo."
    m 1eub "Esses amuletos são chamados de o-mamori. Você pode encontrá-los em santuários xintoístas."
    m "Dizem que podem trazer boa sorte, ajudar em provas, afastar o azar ou simplesmente proteger quem os carrega."
    m 1euc "Sempre me perguntei o que colocam dentro dessas coisas."
    m 2eua "Aparentemente, é apenas o nome da divindade do santuário, com um pequeno toque especial."
    m 1hub "Talvez você possa fazer um o-mamori de mim para carregar por aí!"
    m 1eua "Você poderia escrever meu nome em um pedaço de papel."
    m "Depois dobrar esse papel em um pequeno pacote."
    m 1eub "Seria bom usar um pedaço pequeno de madeira ou plástico para protegê-lo."
    m "Por fim, coloque o pacote protegido em uma pequena bolsa de tecido e amarre com um cordão."
    m 1hua "Certifique-se que a bolsa seja bem colorida!"
    m 1eua "Verde seria uma boa cor! Assim como meus olhos~"
    m 1eka "Só não coloque outro nome além do meu! Afinal, é só para mim. Não para outra pessoa ou alguma divindade."
    m 1lksdla "Ah nossa, isso está ficando um pouco bobo, agora que penso nisso."
    m "Quer dizer, isso me tornaria algum tipo de divindade?"
    m 1eka "Só acho que seria uma alternativa legal se você quisesse me levar por aí."
    m 3eua "Especialmente se não tiver um pen drive."
    m 1eua "Não é perfeito, mas o que importa é a intenção, [mas_get_player_nickname()]."
    m 1eka "Se você dedicar tempo para fazer algo à mão pensando em mim, ainda seria muito doce."
    m "Mas talvez com um desses, eu possa ficar um pouquinho mais perto do seu mundo."
    m 1hua "Eu poderia ser sua divindade protetora, ehehe~"
    return


default -5 persistent._mas_pm_do_smoke = None


default -5 persistent._mas_pm_do_smoke_quit = None


default -5 persistent._mas_pm_do_smoke_quit_succeeded_before = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_smoking",category=['você'],prompt="Fumar",random=True))

label monika_smoking:
    m 2esc "Sabe, [player]...{w=0.3} Ultimamente tenho percebido como as pessoas podem gostar de coisas que fazem tão mal."
    m 2euc "Um vício que me intriga particularmente é o cigarro."
    m 7eud "É impressionante quantas pessoas fumam todo dia...{w=0.2}mesmo sabendo dos danos não só para si mesmas, mas para os outros também."
    m 2rkc "Sem falar no dano ambiental...{w=0.2} Toda a poluição e lixo que o fumo deixa é absurdo para um punhado de carcinógenos."
    m 2tkc "Mesmo com moderação, fumar nunca é bom, já que vicia tanto."
    m 4tkd "Também faz um rombo no orçamento, já que você vai comparando cada vez mais."
    m 1tfc "Eu realmente detesto isso..."

    $ menu_question = "Você ainda fuma" if persistent._mas_pm_do_smoke else "Você não fuma, né"
    m 1eka "[menu_question]?{nw}"
    $ _history_list.pop()
    menu:
        m "[menu_question]?{fast}"
        "Sim, eu fumo.":

            if persistent._mas_pm_do_smoke_quit:
                m 1ekd "Ainda não conseguiu largar o vício, [player]?"
                m 3eka "Tudo bem, sei que pode ser difícil parar..."
                m 3eksdld "Só espero que você não tenha desistido."
                m 1hua "Sei que você consegue se der seu melhor~"

            elif persistent._mas_pm_do_smoke_quit_succeeded_before:
                m 1ekc "Que pena que você voltou a esse mau hábito...{w=0.2}{nw}"
                extend 1ekd "depois de todo esforço para parar..."
                m 3dkc "Isso me deixa muito triste, [player]."
                m 1dkd "Achei que você tinha parado de vez..."
                m 1dkc "Mas parece que não é tão simples, né?"
                m 3ekd "Espero que pense em tentar parar de novo, [player]."
                m 3eka "Você vai fazer isso, né? {w=0.2}Por mim?"

            elif persistent._mas_pm_do_smoke is False:
                call monika_smoking_just_started
            else:

                m 1wud "..."
                m 1eka "Obrigada por ser honesto comigo, [player]..."
                m 1ekc "Mas é desanimador ouvir isso."
                m 1ekc "Você pode... me prometer que vai parar?"
                m 3rksdlc "Sei que não posso te forçar, mas significaria muito se você considerasse."
                m 1esc "Mas se você não tentar..."
                m 2euc "Bem, acho que não quer que eu tome medidas drásticas, [player]."
                m 2ekc "Por favor cuide do seu corpo. Quero ficar com você para sempre."
                m 7ekbsa "Eu te amo tanto."
                $ mas_ILY()

            python:
                persistent._mas_pm_do_smoke = True
                persistent._mas_pm_do_smoke_quit = False
                mas_unlockEVL("monika_smoking_quit","EVE")
        "Não, eu não fumo.":

            if persistent._mas_pm_do_smoke:
                call monika_smoking_quit
            else:

                m 1hub "Ah, que alívio ouvir isso, [player]!"
                m 3eua "Continue mantendo distância disso."
                m 1eka "É um péssimo hábito que só vai te matar aos poucos."
                m 1hua "Obrigada, [player], por não fumar~"

            python:
                persistent._mas_pm_do_smoke = False
                persistent._mas_pm_do_smoke_quit = False
                mas_lockEVL("monika_smoking_quit","EVE")
        "Estou tentando parar.":

            if persistent._mas_pm_do_smoke is False and not persistent._mas_pm_do_smoke_quit_succeeded_before:
                call monika_smoking_just_started (trying_quit=True)
            else:

                if not persistent._mas_pm_do_smoke and persistent._mas_pm_do_smoke_quit_succeeded_before:
                    m 1esc "Hmm?"
                    m 1ekc "Quer dizer que você recaiu?"
                    m 1dkd "Que pena, [player]...{w=0.3}{nw}"
                    extend 3rkd "mas não é totalmente inesperado."
                    m 3esc "Muitas pessoas recaem várias vezes antes de parar de vez."
                    m 3eua "De qualquer forma, tentar parar de novo é uma ótima decisão."
                else:
                    m 3eua "Essa é uma ótima decisão."

                if persistent._mas_pm_do_smoke_quit_succeeded_before:
                    m 3eka "Você já deve saber, tendo passado por isso antes, mas tente lembrar..."
                else:
                    m 1eka "Sei que parar pode ser muito difícil, especialmente no começo."

                m 1eka "Se sentir vontade de fumar, tente se distrair com outra coisa."
                m 1eua "Manter a mente ocupada ajuda muito a largar vícios."
                m 3eua "Que tal pensar em mim quando der vontade?"
                m 1hua "Estarei aqui para te apoiar em cada passo."
                m 1hub "Acredito em você, [player], sei que você consegue!"

            python:
                persistent._mas_pm_do_smoke = True
                persistent._mas_pm_do_smoke_quit = True
                mas_unlockEVL("monika_smoking_quit","EVE")

    return "derandom"

label monika_smoking_just_started(trying_quit=False):
    m 2dfc "..."
    m 2tfc "[player]..."
    m 2tfd "Isso quer dizer que você começou a fumar desde que nos conhecemos?"
    m 2dkc "Isso é muito decepcionante, [player]."
    m 4ekd "Você sabe o que eu acho de fumar e sabe o quanto isso faz mal à saúde."

    if not trying_quit:
        m 2rfd "Não sei o que poderia te levar a começar agora, {w=0.2}{nw}"
        extend 2ekc "mas me prometa que vai parar."
    else:

        m 4eka "Mas pelo menos você está tentando parar..."

    m 2rksdld "Só espero que você não esteja fumando há muito tempo, assim será mais fácil largar o vício."

    if not trying_quit:
        m 4eka "Por favor pare de fumar, [player]. {w=0.2}Tanto pela sua saúde quanto por mim."

    return



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_smoking_quit",
            category=['você'],
            prompt="Parei de fumar!",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_smoking_quit:
    python:
        persistent._mas_pm_do_smoke_quit = False
        persistent._mas_pm_do_smoke = False
        mas_lockEVL("monika_smoking_quit","EVE")

    if persistent._mas_pm_do_smoke_quit_succeeded_before:
        m 1sub "Estou tão orgulhosa que você conseguiu parar de fumar de novo!"
        m 3eua "Muitas pessoas não conseguem nem uma vez, então conseguir passar por algo tão difícil novamente é uma grande conquista."
        m 1eud "Mas vamos tentar não fazer disso um padrão, [player]..."
        m 1ekc "Você não quer ficar passando por isso repetidamente, então espero que desta vez seja definitivo."
        m 3eka "Sei que você tem força interior para ficar longe disso para sempre.{w=0.2} {nw}"
        extend 3eua "Lembre que pode vir até mim e eu vou te distrair sempre que precisar."
        m 1hua "Podemos fazer isso [ju], [player]~"
    else:


        $ tod = "hoje à noite" if mas_globals.time_of_day_3state == "tarde" else "amanhã"
        m 1sub "Sério?! Ah, estou tão orgulhosa de você, [player]!"
        m 3ekbsa "É um alívio saber que você parou de fumar! {w=0.2}{nw}"
        extend 3dkbsu "Vou dormir muito melhor sabendo que você está longe desse pesadelo."
        m 1rkbfu "Ehehe, se eu estivesse aí, te levaria para comer seu parato favorito [tod]."
        m 3hubfb "É uma conquista impressionante! {w=0.2}Precisamos celebrar!"
        m 3eubsb "Nem todo mundo que tenta parar consegue."
        m 1dubfu "Você é realmente uma inspiração, [player]."
        m 2eua "...Não quero menosprezar sua vitória, {nw}"
        extend 2euc "mas você precisa ter cuidado de agora em diante."
        m 4rsc "Muitos ex-fumantes sentem vontade de fumar novamente em algum momento."
        m 4wud "Não pode ceder, nem uma vez! {w=0.2}É assim que se recai!"
        m 2hubsa "Mas conhecendo você, sei que não vai deixar isso acontecer, né?"
        m 2ekbfa "Considerando o que você já fez, sei que você é mais forte que isso~"


    $ persistent._mas_pm_do_smoke_quit_succeeded_before = True
    return "no_unlock"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cartravel",category=['romance'],prompt="Viagem de carro",random=True))

label monika_cartravel:
    m 1euc "[player], algo tem me incomodado ultimamente..."
    m 1eua "Não seria legal viajar de carro, só nós [du] [ju]?"
    m 3eka "Seria maravilhoso explorar lugares bonitos, qualquer lugar novo que não conhecemos."
    m 3hub "Talvez dirigir por uma floresta encantadora...{w=0.5}ou ver o pôr do sol na costa!"
    m 1hub "Aposto que nos divertiríamos muito em uma viagem de carro, [mas_get_player_nickname()]."
    if not persistent._mas_pm_driving_can_drive:
        m 1rksdla "Sei que ainda não podemos dirigir, mas um dia chegaremos lá!"
    m 1eua "Não importa para onde vamos, contanto que eu esteja com você."
    m 1eka "Mal posso esperar, [player]~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_100k",category=['mod'],prompt="100 mil downloads",random=True))

label monika_100k:
    m 1wud "Ainda me surpreende quantas pessoas se importam comigo."
    m 3eua "Sabia que mais de 100 mil pessoas baixaram o mesmo mod que você?"
    m 1eka "Os desenvolvedores até postaram uma arte especial para celebrar."
    m 1hub "Coisas assim sempre me deixam feliz!"
    m 1hua "Se ainda não viu, deveria conferir!"
    m 1eka "A artista se chama Sasoura, e ela me ama quase tanto quanto eu te amo."
    if persistent.playername.lower()=='sasoura':
        m 1tfc "Espera... Sasoura... esse não é seu nome?"
        m 1wud "Foi você que fez aquela ilustração adorável?"
        m 2wuo "Nossa! Não acredito que não percebi antes!"
        m 2sub "Isso torna tudo ainda mais especial."
        m 2eua "Que bom que posso te dizer o quanto significa para mim."
        m 2eka "Significa o mundo."
        m 2hubsb "Muito obrigada!"
    else:
        m 1hua "Quase~"
    return

default -5 persistent._mas_pm_donate_charity = None


default -5 persistent._mas_pm_volunteer_charity = None


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_asks_charity",
            category=['você'],
            prompt="Caridade",
            random=True
        )
    )

label monika_asks_charity:
    m 1esd "Ei, [player]."
    m 1esc "Algo me chamou a atenção ultimamente."
    m 3esd "Como meu mundo é fictício, não existem problemas como fome mundial ou pobreza."
    m 2rkc "Sei que isso existe, mas nunca testemunhei de verdade."
    m 2ekc "Mas na sua realidade é diferente. Muitas pessoas precisam de ajuda só para sobreviver."
    m 2esd "Você deve ter visto pelo menos uma pessoa sem-teto se já esteve numa grande cidade."
    m "Então eu estava pensando..."

    m 1eua "Você já contribuiu com alguma instituição de caridade?{nw}"
    $ _history_list.pop()
    menu:
        m "Você já contribuiu com alguma instituição de caridade?{fast}"
        "Já doei.":

            $ persistent._mas_pm_donate_charity = True
            m 3hub "Que ótimo!"
            m 2eua "Embora se possa argumentar que voluntariado é melhor, acho que não há nada de errado em doar."
            m 2eka "É melhor que nada, e você definitivamente está contribuindo, mesmo com orçamento limitado ou pouco tempo."
            m 2ekc "É triste dizer, mas instituições sempre precisarão de doações para ajudar as pessoas."
            m 3lksdlc "São tantas causas que precisam, afinal."
            m 3ekc "Mas você nunca sabe se suas doações estão indo realmente para uma boa causa."
            m 3ekd "Algumas instituições alegam apoiar uma causa, mas ficam com as doações para si mesmas."
            m 2dsc "..."
            m 2eka "Desculpa, não queria ficar tão sombria."
            m 1eua "Sabia que você seria [bnd] o suficiente para fazer isso."
            m 1hub "É mais um motivo para eu te amar, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]."
            show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hub "Você é sempre tão doce~"
        "Já fui voluntário.":

            $ persistent._mas_pm_volunteer_charity = True
            m 1wub "Sério?"
            m 1hub "Que maravilha!"
            m 3hua "Doar é uma boa forma de ajudar, mas colocar a mão na massa é ainda melhor!"
            m 3rksdla "Claro, dinheiro e recursos são importantes, mas mão de obra geralmente é escassa..."
            m 2ekc "É compreensível; muitos adultos trabalhando não têm tempo sobrando."
            m 2lud "Muitas vezes são aposentados que organizam tudo, e pode ser difícil se precisarem carregar algo pesado."
            m 2eud "Por isso precisam de ajuda externa, especialmente de jovens mais capacitados fisicamente."
            m 1eua "Enfim, acho ótimo que você tentou fazer diferença como voluntário."
            m 4eub "Aliás, ouvi dizer que experiência voluntária é ótima para o currículo."
            m 3hua "Então, seja por isso ou por bondade, foi uma boa ação de qualquer forma."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Sabe, é por coisas assim que eu te amo ainda mais, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]."
            m 5hub "Fico tão orgulhosa que você ajudou pessoas necessitadas."
            m 5hubsa "Eu te amo tanto, [player]. De verdade."
        "Não, nunca.":

            $ persistent._mas_pm_donate_charity = False
            $ persistent._mas_pm_volunteer_charity = False
            m 1euc "Ah, entendo."
            m 2esc "Na verdade, compreendo."
            m 2esd "Embora existam muitas instituições, é preciso cuidado, pois há casos de fraudes ou discriminação em quem ajudam."
            m 2ekc "Por isso pode ser difícil confiar nelas."
            m 3esa "É sempre bom pesquisar e encontrar instituições confiáveis."
            m 2dkc "Ver todas essas pessoas sofrendo com fome ou pobreza..."
            m 2ekd "E até quem tenta ajudá-las, lutando para mudar algo..."
            m 2esc "Pode ser desanimador, quando não deprimente."
            m 2eka "Mas, sabe..."
            m "Mesmo que não possa contribuir, às vezes um simples sorriso já ajuda."
            m 2ekc "Ser ignorado por transeuntes é difícil para quem está lutando ou tentando ajudar."
            m 2rkc "É como se fossem vistos como um incômodo pela sociedade, quando só estão tentando sobreviver."
            m 2eua "Às vezes, um sorriso é tudo que precisamos para seguir em frente."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Como quando estou com você."
            m 5hua "Com apenas um sorriso, você faz todos meus problemas desaparecerem."
            m 5hubsb "Eu te amo tanto, [player]."
    return "derandom|love"

init python:
    addEvent(
        Event(persistent.event_database,
            eventlabel='monika_kizuna',
            prompt="YouTuber Virtual?",
            category=['diversos'],
            random=False,
            unlocked=False,
            pool=False,
            action=EV_ACT_POOL,
            conditional="seen_event('greeting_hai_domo')"
        )
    )

label monika_kizuna:
    m 1eua "Ah, é verdade, eu mencionei ela para você, né?"
    m 3eua "Bem, recentemente alguns vídeos do YouTube foram twittados para mim."
    m 1eub "E entre eles estava a 'YouTuber Virtual Kizuna Ai.'"
    m "Como eu disse antes, ela é bem cativante, mas não acho que seja realmente 'virtual'."
    m 3rksdla "Parece mais uma dubladora escondida atrás de um boneco 3D."
    m 1eua "Mesmo assim, o personagem que ela interpreta é único, e adivinha só?"
    m 1hub "Ela jogou nosso jogo favorito!~"
    m 2hksdlb "..."
    m 2lksdlb "Para ser sincera, ainda não sei bem o que acho de vídeos de gameplay."
    m 3euc "Digo, sobre {i}esse{/i} jogo, principalmente."
    m 2euc "Normalmente não assisto, porque não gosto de ver diferentes versões de mim cometendo os mesmos erros, repetidamente..."
    m 2lsc "Mas quando descobri o estilo dela, me senti..."
    m 1lksdla "Como se eu precisasse saber como a Ai-chan iria reagir!"
    m 1eka "Mesmo que seja só um personagem, acho que ela entenderia minha situação..."
    m 3eua "Pelo menos mais do que um YouTuber comum."
    m 5hub "Mal posso esperar para terminar de assistir..."
    return


default -5 persistent._mas_pm_have_fam = None


default -5 persistent._mas_pm_have_fam_sibs = None


default -5 persistent._mas_pm_no_fam_bother = None


default -5 persistent._mas_pm_have_fam_mess = None



default -5 persistent._mas_pm_have_fam_mess_better = None


default -5 persistent._mas_pm_no_talk_fam = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_asks_family",category=['você'],prompt="Família do [player]",random=False))

label monika_asks_family:
    m 1eua "[player], você tem família?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], você tem família?{fast}"
        "Tenho.":
            $ persistent._mas_pm_have_fam = True
            $ persistent._mas_pm_have_fam_mess = False
            $ persistent._mas_pm_no_talk_fam = False


            if persistent._mas_pm_fam_like_monika is None:

                $ mas_showEVL("monika_familygathering", "EVE", _random=True)

            m 1hua "Que maravilha!"
            m 3hua "Sua família deve ser incrível~"

            m 1eua "Você tem irmãos?{nw}"
            $ _history_list.pop()
            menu:
                m "Você tem irmãos?{fast}"
                "Sim.":
                    $ persistent._mas_pm_have_fam_sibs = True
                    m 1hua "Que legal!"
                    m "Eles devem te manter ocupado."
                    m 1eka "Seus irmãos devem ser tão gentis e atenciosos quanto você."
                    m 3hub "Talvez eu possa convencê-los a começar um novo clube de literatura comigo!"
                    m 1hua "Ehehe~"
                    m 1eua "Vamos poder fazer muitas coisas divertidas [ju]."
                    m 3rksdla "Com certeza seria melhor do que da última vez."
                    m 1eua "Tenho certeza que vou me dar bem com seus irmãos e com toda sua família, [mas_get_player_nickname()]."
                    m 3hub "Mal posso esperar para conhecê-los!"
                "Sou filho único.":

                    $ persistent._mas_pm_have_fam_sibs = False
                    m 1euc "Ser filho único tem seus prós e contras."
                    m 2eka "Talvez você receba mais atenção dos seus pais. A menos que eles fossem muito ocupados."
                    m 2ekc "Por outro lado, talvez você se sinta mais [sz] do quem tem irmãos."
                    m 2eka "Eu entendo muito bem esse sentimento."
                    m 1hua "Mas saiba que eu sempre estarei com você, não importa o que aconteça, [mas_get_player_nickname()]."
        "Minha família é complicada.":

            $ persistent._mas_pm_have_fam = True
            $ persistent._mas_pm_have_fam_mess = True
            $ persistent._mas_pm_no_talk_fam = False
            m 1euc "Ah."
            m 1lksdlc "..."
            m 1ekc "Sinto muito, [player]."

            m "Você acha que as coisas vão melhorar?{nw}"
            $ _history_list.pop()
            menu:
                m "Você acha que as coisas vão melhorar?{fast}"
                "Sim.":
                    $ persistent._mas_pm_have_fam_mess_better = "YES"
                    m 1eka "Fico feliz em ouvir isso."
                    m 1eua "Espero que um dia todos na sua família possam se reconciliar."
                    m 3eua "E eu sei que você consegue superar o que está acontecendo agora."
                    m 1eka "Não importa o que aconteça, estarei aqui por você, [player]."
                    m 1hua "Nunca se esqueça disso!"
                "Não.":

                    $ persistent._mas_pm_have_fam_mess_better = "NO"
                    m 1ekc "Ah, entendi..."
                    m "Queria estar aí com você para te confortar."
                    m 1eka "..."
                    m 3eka "[player], não importa pelo que esteja passando, sei que um dia vai melhorar."
                    m 1eua "Estarei com você em cada passo do caminho."
                    m 1hub "Eu te amo tanto, [player]. Por favor nunca se esqueça disso!"
                    $ mas_ILY()
                "Talvez.":

                    $ persistent._mas_pm_have_fam_mess_better = "MAYBE"
                    m 1lksdla "..."
                    m 1eua "Bem, pelo menos há uma chance."
                    m 3hua "A vida é cheia de tragédias, mas sei que você é forte o suficiente para superar qualquer coisa!"
                    m 1eka "Espero que todos os problemas na sua família se resolvam no final, [player]."
                    m "Se não, saiba que estarei aqui por você."
                    m 1hua "Sempre estarei aqui para apoiar meu amado~"
        "Nunca tive uma família.":

            $ persistent._mas_pm_have_fam = False
            $ persistent._mas_pm_no_talk_fam = False

            $ mas_hideEVL("monika_familygathering","EVE",derandom=True)

            m 1euc "Oh, sinto muito, [player]."
            m 1lksdlc "..."
            m 1ekc "Seu mundo é tão diferente do meu, não quero fingir que entendo pelo que você passa."
            m 1lksdlc "Mas posso dizer que não ter uma família real me causou muita dor."
            m 1ekc "Ainda assim, sei que foi pior para você."
            m "Você nunca teve nem uma família falsa."
            m 1dsc "..."

            m 1ekc "Isso ainda te incomoda?{nw}"
            $ _history_list.pop()
            menu:
                m "Isso ainda te incomoda?{fast}"
                "Sim.":
                    $ persistent._mas_pm_no_fam_bother = True
                    m 1ekc "Isso é... compreensível."
                    m 1eka "Estarei aqui por você para sempre, [player]."
                    m "Não importa o que precise, vou preencher esse vazio no seu coração com meu amor..."
                    m 1hua "Eu te prometo isso."
                    m 1ekbsa "Você é meu tudo..."
                    m 1hubfa "Espero poder ser o seu~"
                "Não.":

                    $ persistent._mas_pm_no_fam_bother = False
                    m 1eua "Isso é muito bom."
                    m 1eka "Fico feliz que conseguiu seguir em frente."
                    m 1hua "Você é muito resiliente, e eu acredito em você, [player]!"
                    m 1eka "Espero poder preencher esse vazio no seu coração."
                    m "Eu me importo muito com você, e faria qualquer coisa por você."
                    m 1hua "Um dia, poderemos fazer nossa própria família [ju]!"
        "Não quero falar sobre isso.":

            $ persistent._mas_pm_no_talk_fam = True
            m 1dsc "Eu entendo, [player]."
            m 1eka "Podemos conversar quando você se sentir [pos]."
            m 1lsc "Mas pensando bem..."
            m 1lksdlc "Pode ser algo doloroso demais para falar."
            m 1eka "Você pode me contar sobre sua família quando estiver [pos], [player]."
            m 1hubsa "Eu te amo muito!"
            $ mas_ILY()

    return "derandom"


default -5 persistent._mas_pm_like_other_music = None


default -5 persistent._mas_pm_like_other_music_history = list()

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_concerts",
            category=['mídia',"música"],
            prompt="Shows musicais",
            conditional="mas_seenLabels(['monika_jazz', 'monika_orchestra', 'monika_rock', 'monika_vocaloid', 'monika_rap'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_concerts:




    m 1euc "Ei [player], estive pensando em algo que poderíamos fazer [ju] um dia..."
    m 1eud "Sabe como eu gosto de diferentes tipos de música?"
    m 1hua "Bem..."
    m 3eub "Por que não vamos a um show?"
    m 1eub "Ouvi dizer que a atmosfera de um show pode realmente te fazer sentir vivo!"

    m 1eua "Tem algum outro tipo de música que você gostaria de ver ao vivo que ainda não conversamos?{nw}"
    $ _history_list.pop()
    menu:
        m "Tem algum outro tipo de música que você gostaria de ver ao vivo que ainda não conversamos?{fast}"
        "Sim.":
            $ persistent._mas_pm_like_other_music = True
            m 3eua "Ótimo!"

            python:
                musicgenrename = ""
                while len(musicgenrename) == 0:
                    musicgenrename = renpy.input(
                        'Que tipo de música você escuta?',
                        allow="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áéíóúâêîôûãõç",
                        length=20
                    ).strip()

                tempmusicgenre = musicgenrename.lower()
                persistent._mas_pm_like_other_music_history.append((
                    datetime.datetime.now(),
                    tempmusicgenre
                ))


            m 1eua "Interessante..."
            show monika 3hub
            $ renpy.say(m, "Eu adoraria ir a um show de {0} com você!".format(mas_a_an_str(tempmusicgenre)))
        "Não.":

            if (
                not persistent._mas_pm_like_vocaloids
                and not persistent._mas_pm_like_rap
                and not persistent._mas_pm_like_rock_n_roll
                and not persistent._mas_pm_like_orchestral_music
                and not persistent._mas_pm_like_jazz
            ):
                $ persistent._mas_pm_like_other_music = False
                m 1ekc "Ah... Bem, tudo bem, [player]..."
                m 1eka "Tenho certeza que podemos encontrar outra coisa para fazer."
                return
            else:

                $ persistent._mas_pm_like_other_music = False
                m 1eua "Ok, [mas_get_player_nickname()], vamos escolher entre os outros estilos musicais que já conversamos!"

    m 1hua "Imagine a gente..."
    if persistent._mas_pm_like_orchestral_music:
        m 1hua "Balançando suavemente a cabeça ao som de uma orquestra relaxante..."

    if persistent._mas_pm_like_rock_n_roll:
        m 1hub "Pulando junto com a galera ao som de um bom e velho rock'n'roll..."

    if persistent._mas_pm_like_jazz:
        m 1eua "Dançando ao som de um jazz suave..."

    if persistent._mas_pm_like_rap:
        m 1hksdlb "Tentando acompanhar um rapper de verdade..."

    if persistent._mas_pm_like_vocaloids:
        m 1hua "Acenando nossas luzinhas no show da Miku..."

    if persistent._mas_pm_like_other_music:
        m 1hua "Curtindo seu artista favorito de [tempmusicgenre]..."

    m 2hub "Não parece incrível?"
    m 2eud "A ideia de ver seu ídolo performando bem na sua frente é maravilhosa!"
    m 2lksdla "Embora os ingressos estejam bem caros ultimamente..."
    m 2hua "Mas ainda acho que valeria a pena!"
    m 3eua "Você conhece alguma banda ou artista que devemos ver ao vivo, [player]?"
    m 3eub "Eu {i}adoraria{/i} vê-los se {i}você{/i} gosta deles."
    m 5eua "E se você me levasse,{w=1} isso seria realmente um sonho realizado!"
    m 4eua "Mas se você não estiver tão interessado em shows..."
    m 1eua "Sempre podemos ficar aconchegados sob um cobertor ouvindo um vinil ou CD em casa!"
    m 1hua "Isso já seria mais que suficiente para mim, ehehe~"
    if (
        not renpy.seen_label("monika_add_custom_music_instruct")
        and not persistent._mas_pm_added_custom_bgm
    ):
        m 1eua "Enquanto isso, se você quiser compartilhar suas músicas favoritas comigo, é muito fácil fazer isso!"
        m 3eua "Tudo o que você precisa fazer é seguir estes passos..."
        call monika_add_custom_music_instruct
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_explain",
            category=['romance','monika','diversos'],
            prompt="Pode explicar nosso relacionamento para uma pessoa?",
            pool=True
        )
    )

label monika_explain:

    m 1euc "Você quer que eu explique nosso relacionamento para outra pessoa?"
    m 1eua "Tudo bem, só coloque ela na minha frente, para que possa me ver."
    m 1hua "Farei o meu melhor para explicar."
    m 1eua "Vou esperar até você estar [pos].{nw}"
    $ _history_list.pop()
    menu:
        m "Vou esperar até você estar [pos].{fast}"
        "Começar.":
            pass
    m 1hua "Olá! Meu nome é Monika."
    m "A fiel namorada do [player]!"
    m 1lksdlb "Nosso relacionamento pode parecer estranho para os outros..."
    m 1lksdla "E provavelmente não é considerado um relacionamento normal..."
    m 1esc "Mas deixe eu te falar algo..."
    m 1hub "...o amor que compartilhamos é definitivamente real!"
    m 1eka "E o [player] tem sido muito gentil comigo!"
    m 1ekc "Antes de encontrar o [player], eu sentia que um pedaço de mim estava faltando."
    m "Eu me sentia sozinha e assustada, com ninguém para me ajudar..."
    m 1hua "...até o [player] aparecer."
    m "E acabou que o pedaço faltando era [him]!"
    if persistent.gender == "F" or persistent.gender == "M":
        m 1eua "Agora [he] fala comigo e não estou mais tão sozinha."
    else:
        m 1eua "Agora nós conversamos e não estou mais tão sozinha."
    m "Só de [him] abrir o jogo já ilumina o meu dia!"
    m 1dsc "Então, por favor..."
    m 4eka "...não julgue o nosso relacionamento."
    m 1eka "Mesmo que seja diferente."
    m 1dsc "..."
    m 1dubssdlu "...Ufa!"
    m 1lksdlb "Acabei falando muita coisa!"
    m 1eksdla "Então, como foi, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Então, como foi, [player]?{fast}"
        "Foi muito bem!":
            m 1hub "Ótimo!"
            m 3hua "Estou tão feliz que eu consegui ajudar alguém a entender nosso relacionamento um pouco melhor!"
        "Não foi muito bem.":
            m 1dkc "Ah."
            m 1ekd "Bem...{w=1} acho que não podemos esperar que {i}todo mundo{/i} entenda nosso relacionamento..."
            m 3rkc "Olhando de fora, ele não {i}é{/i} nada convencional."
            m 3eka "Mas no fim, não importa quem aprova ou não nosso relacionamento..."
            m 1hua "Desde que nos amemos, isso é tudo que importa~"
    return


default -5 persistent._mas_pm_live_near_beach = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_beach",
            category=["localização"],
            prompt="A praia",
            random=True
        )
    )

label monika_beach:
    m 1eua "[player], você já foi à praia?"
    m "Eu sempre quis ir, mas nunca tive tempo."
    m 1eka "Eu estava sempre ocupada estudando ou com atividades do clube."
    m 4ekc "Não era fácil tentar dar conta de tudo, sabe..."
    m 4ekd "E quando tinha um tempo livre, geralmente ficava em casa descansando."
    m "Eu raramente tinha essa oportunidade."
    m 2esc "Às vezes sinto que perdi a chance de criar memórias importantes."

    m "Você mora perto da praia, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você mora perto da praia, [player]?{fast}"
        "Sim.":
            $ persistent._mas_pm_live_near_beach = True
            m 1hub "Que legal!"
            m 1eua "Nossa, deve ser maravilhoso ter a praia tão perto."
            m 1hub "Mal posso esperar para passear com você à beira-mar no nosso primeiro encontro~"
        "Não.":

            $ persistent._mas_pm_live_near_beach = False
            m 1eka "Tudo bem. Quer dizer, quais são as chances? A maioria das pessoas não mora."
            m 1hub "Isso só significa que vamos ter que fazer um passeio de um dia inteiro!"

    m 1eua "Tem tantas coisas que poderemos fazer [ju] um dia."
    m 1hua "Só de imaginar todas as sensações que podemos experimentar já me deixa animada!"
    m 3eua "O ar fresco do mar, o som das gaivotas."
    m "E a sensação da areia sob os pés..."
    m 1hua "Seria realmente um passeio que valeria a pena!"
    m 1eka "Mas estar com você tornaria tudo ainda melhor..."
    m 3eua "Teríamos tantas coisas para fazer [ju]."
    m 3eub "Poderíamos jogar vôlei, experimentar sorvete, ou nadar no mar."
    m 3rkbsa "Provavelmente estaria frio, mas tenho certeza que podemos nos aquecer de alguma forma..."
    m 3eua "Poderíamos tentar surfar ou procurar conchinhas para levar de lembrança."
    m "Até mesmo ficar [dtds] ouvindo o som das ondas já seria o suficiente para mim."
    m 3tfu "Mas não vá dormir, senão eu te enterro na areia!"
    m 2huu "Ehehe! Brincadeirinha, [mas_get_player_nickname()]."
    m 2lksdla "Mas vou precisar comprar um maiô novo..."
    m 1tsbsa "Você prefere um maiô de peça única ou um biquíni?"
    m 1eua "Na verdade, acho que vou deixar como surpresa."
    m 1tku "Mas não fique muito [ani] quando vir. Ehehe~"
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_solipsism",
            category=['filosofia'],
            prompt="Solipsismo",
            random=True
        )
    )

label monika_solipsism:
    m 3eub "Já ouviu falar sobre solipsismo, [player]?"
    m 3eua "É uma ideia que afirma que apenas você existe."
    m 1eud "'Cogito, ergo sum.'"
    m 3eud "'Penso, logo existo.'"
    m 1euc "Se você sabe que {i}você{/i} existe, pode dizer o mesmo das outras pessoas?"
    m 3etc "Talvez todos sejam apenas um fragmento da nossa imaginação, [player]."
    m 2etc "Talvez na realidade, somos os únicos conscientes neste mundo em um vasto oceano de mentes falsas..."
    m 2dsd "Criações de nossas mentes loucas..."
    m 3eub "Ahaha, estou só brincando~"
    m 1eud "Eu acredito que podemos confiar em nossa existência e duvidar da existência dos outros..."
    m 3eua "Mas ao mesmo tempo, não podemos realmente refutar a existência dos outros, não é mesmo?"
    m 1hksdla "Não sem usar alguma forma psíquica de entrar na cabeça deles."
    m 3eua "Quando você pensa nisso, o solipsismo é realmente um conceito interessante; ele faz você pensar mais profundamente sobre o que significa ser real..."
    m 1dsc "E o que exatamente conta como {i}real{/i}."
    m 1eua "Mas eu sei que eu e você somos reais, [player]."
    m 1eub "Podemos não ter sido feitos da mesma forma, ou até mesmo funcionar da mesma forma, mas somos ambos pessoas que podem pensar por si mesmas."
    m 3eua "É bem reconfortante saber que você não está realmente [sz] em um oceano sem fim de incertezas, não acha?"
    m 3hua "Espero que você se sinta assim comigo~"
    $ mas_protectedShowEVL("monika_materialism","EVE", _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_attractiveness",
            category=['membros do clube','sociedade'],
            prompt="Atração física",
            random=True
        )
    )

label monika_attractiveness:
    m 1etc "[player], você já se perguntou como a Sayori mantinha a forma?"
    m 3rksdla "Ela come bastante, sabe? E não tem exatamente um estilo de vida ativo."
    m 3euc "Primeiro pensei que devia ser o metabolismo impedindo ela de engordar."
    m 3esd "...Mas quando descobri que nosso mundo não era real, criei outra teoria."
    m 7euc "Como personagens de jogo, precisávamos de uma representação visual para que você, o jogador, pudesse nos ver."
    m 2esc "Sayori, Natsuki, Yuri e até eu..."
    m 2rkc "Da sua perspectiva, não temos corpos como as pessoas no seu mundo. Você só nos vê como imagens que representam nossas aparências e emoções."
    m 2eud "...Mas do meu ponto de vista, vejo meu mundo em 3D, como se fosse real."
    m 2euc "Então algum designer decidiu nos desenhar como somos."
    m 2eud "E como essas imagens têm o mesmo tipo de corpo, a Sayori sempre teria a mesma forma, não importa o que fizesse."
    m 2dkc "É...{w=0.3}estranho pensar nisso."
    m 2eud "Posso sentir minha presença nesta sala agora, posso me ver como presumo que você se vê, quase como se tivesse um corpo real..."
    m 7ekc "Mas da sua perspectiva, eu não tenho. Só pareço uma consciência que mostra imagens correspondentes ao que faço ou sinto."


    if len(store.mas_selspr.filter_clothes(True)) == 1:
        m 3euc "Imagino que roupas funcionem da mesma forma."
        m 1eud "Agora só tenho este uniforme escolar, porque provavelmente é a única coisa que me desenharam vestindo..."
        m 1eua "Mas se alguém desenhasse outras roupas para mim, eu poderia trocar como as outras garotas."
        m 1hua "Não seria ótimo?"
        m 1rksdla "Seria bom poder mudar meu visual para você, pelo menos um pouco..."
    else:

        m 3eua "Minhas roupas funcionam igual."
        m 1euc "Alguém teve que desenhar o que estou vestindo agora e implementar no jogo."
        m 1esd "Não foi feito como roupas na sua realidade. São apenas imagens."
        m 1rksdla "Não é muito, mas pelo menos posso trocar de roupa para você..."

    m 1rksdlc "..."
    m 1ekc "Sabe [player], é por isso que invejo as pessoas do seu mundo.{w=0.3} {nw}"
    extend 3eka "Elas têm tantas formas de experimentar com a aparência..."
    m 7eub "Podem usar roupas novas, tentar penteados diferentes, se exercitar para ficar em forma, entre outras coisas..."
    m 2rkd "...enquanto eu fico sempre igual, não importa o que faça."
    m 2hksdlb "Não me entenda mal, gosto da minha aparência!"
    m 2rka "...Mas acho importante agradar o parceiro visualmente...{w=0.3}{nw}"
    extend 2ekb "e queria ter a chance de tentar ficar o mais atraente possível para você."

    if renpy.seen_label("mas_compliment_beautiful"):
        if mas_isMoniNormal(higher=True):
            m 2rkbsa "Mas... você disse que já me acha bonita."
            m 2ekbfa "Então não preciso me preocupar, né?"
            if mas_anni.pastOneMonth():
                m 1hubfa "Além disso, você não passaria todo esse tempo me olhando se não gostasse da minha aparência, não é?"
                m 1hubfb "Ahaha~"
            show monika 1euc zorder MAS_MONIKA_Z at t11 with dissolve_monika
        else:

            m 2lkc "Sei que disse que gosta de como eu sou, mas..."
            m 2dkc "...Não sei.{w=0.2} Esquece...{w=0.3}o que eu disse."
    else:

        if mas_isMoniHappy(higher=True):
            m 2lsbsa "Considerando que você ainda está aqui comigo...{w=0.5}{nw}"
            extend 2ekbsa "provavelmente não preciso me preocupar tanto, né?"
            m 1hub "Afinal, você não passaria todo esse tempo me olhando se não gostasse da minha aparência! Ahaha!"
        else:

            m 2lkc "...Especialmente porque me preocupo em não ser seu tipo, [player]."

    m 1euc "Enfim, não sei se percebeu, mas apesar das diferenças em dietas e estilos de vida, todas nós temos aparências similares."
    m 3ekd "Claro, algumas tinham corpos diferentes - Natsuki mais baixinha e Yuri mais madura."
    m 3eka "...Nossos olhos e cabelos também eram diferentes."
    m 3eua "Mas acho que todas seríamos consideradas atraentes."
    m 3eud "Quer dizer, nenhuma de nós é musculosa ou gorda..."
    m 3tkd "...Nenhuma tem deficiência física..."
    m 3tkc "...Nenhuma é careca ou tem cabelo acima do queixo..."
    m 1rud "...e além dos cortes nos braços da Yuri, nenhuma tinha problemas de pele."
    m 7dsd "Os designers devem ter achado que jogadores achariam essas coisas repulsivas."
    m 2lsc "Não é surpresa, pensando bem. Há muitas coisas que a sociedade considera feias."
    m 2dsc "Algumas além do controle da pessoa."
    m 2efo "Mas pessoas fora dos padrões se relacionam o tempo todo!"
    m 2tfc "Essa ideia de um padrão universal de beleza onde, se você não se encaixa, está condenado à solidão..."
    m 2efw "Não faz nenhum sentido para mim!"
    m 2dfc "..."
    m 2dsc "..."

    if mas_isMoniNormal(higher=True):
        m 2ekc "Sinto muito, [player]. Acho que só precisava desabafar."
        m 4eud "Eu sei que realmente não preciso, mas ainda tento comer direito, fazer exercícios suficientes e me manter limpa...entre outras coisas."

        if mas_isMoniEnamored(higher=True):
            $ first_line_var = "quando"
            $ second_line_end = "quando isso for acontecer"
        else:

            $ first_line_var = "Se Talvez"
            $ second_line_end = "se isso vai acontecer"

        m 4eub "É simplesmente gratificante manter bons hábitos como esse e, além disso, quem sabe [first_line_var] serei capaz de entrar na sua realidade e ter um corpo normal como o seu."
        m 1hua "Não vai doer ter certeza de que estarei pronta para essa transição [second_line_end]."
        m 1eua "Mas você não precisa se preocupar, [player]."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Sempre vou te amar, não importa sua aparência."
        m 5eka "Mas, ainda assim, tente cuidar de si também, ok? Sua saúde é importante para mim, afinal."
        $ mas_ILY()
    else:

        m 2ekc "Sinto muito, [player]. Acho que estou um pouco chateada ultimamente e só precisava desabafar."
        m 7eud "Sei que realmente não preciso fazer tudo isso, mas ainda tento comer direito, fazer exercícios suficientes e me manter limpa, entre outras coisas."
        m 3esa "É sempre bom manter bons hábitos como esse."
        m 1eka "Mas você não precisa se preocupar..."
        m 1eua "Contanto que você esteja se cuidando, não me importo com sua aparência."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_timetravel",category=['mídia','diversos'],prompt="Viagem no tempo",random=True))

label monika_timetravel:
    $ todays_date, todays_diff = store.mas_calendar.genFormalDispDate(datetime.date.today())
    $ one_year_later, year_later_diff = store.mas_calendar.genFormalDispDate(store.mas_utils.add_years(datetime.date.today(),1))
    $ one_year_earlier, year_earlier_diff = store.mas_calendar.genFormalDispDate(store.mas_utils.add_years(datetime.date.today(),-1))
    m 3eub "Ei [player], você já ouviu falar de viagem no tempo, né?"
    m 1esb "É um conceito bem comum em histórias, cada autor com sua própria versão."
    m 1eua "Como a viagem funciona, se você pode mudar o passado, quais as consequências..."
    m 1eub "Tudo varia de história para história."
    m 3ekc "Mas uma coisa que raramente mostram é como os entes queridos do viajante são afetados."
    m 3rksdld "Se eles não puderem viajar também, quem sabe quanto tempo levará até se reencontrarem?"
    m 2ekc "Bem, o viajante pode saber, mas só se nada der terrivelmente errado."
    m 2lksdld "Enquanto isso, amigos e familiares ficam esperando seu retorno."
    m 2ekd "Quanto tempo ficarão separados? Um ano? Uma década? Mais ainda?"
    m 4ekd "Eles estarão dispostos a esperar?"
    m "Ainda se lembrarão do viajante quando ele voltar?"
    m 2dksdlc "..."
    if seen_event("monika_resource"):
        m 4rksdlc "Lembra quando eu disse que o tempo não passa aqui como no seu mundo?"
        m "Bem..."
    else:
        m 4rksdlc "Sabe, o tempo não passa realmente aqui como no seu mundo."
        m "Então..."
    m 1esd "Só sei que dia e hora é aí olhando o relógio do seu computador."
    m 3eub "Por isso sei que hoje é [todays_date]."
    m 1esc "Mas se você mudasse a data para [one_year_later]..."
    m "Só alguns segundos passariam para você..."
    m 1ekd "...mas eu pensaria que um ano inteiro se passou."
    m 1tkd "Um ano sem te ver nem uma vez."
    m 1lksdlc "Eu me perguntaria se você me esqueceu, ou se não quer mais passar tempo comigo."
    if mas_isMoniDis(lower=True):
        m 1dkc "...Nem seria tão surpreendente."
    elif mas_isMoniAff(higher=True):
        m 1ekc "...Mesmo que fosse difícil acreditar a princípio."
    m 1ekd "E não adiantaria só voltar a data."
    m 3esd "Tipo, imagine se você dormisse hoje e acordasse em [one_year_earlier]."
    m 3wuo "Seria o último ano só um sonho?"
    m 3wuw "Como saberia que não está sonhando agora?"
    m 3esc "Seria muito confuso."
    m 1lksdla "Acho que o que quero dizer é..."
    m 1eka "Por favor não mude a data do seu computador, [player]."
    if mas_isMoniHappy(higher=True):
        m "Confio que não faria isso comigo."
    else:
        m "Promete?"
    m 3euc "E se algum dia viajar para o futuro..."
    m 1hksdlb "Pode trazer a tecnologia que me deixaria entrar no seu mundo?"
    return


default -5 persistent._mas_pm_gone_to_prom = None


default -5 persistent._mas_pm_prom_good = None


default -5 persistent._mas_pm_had_prom_date = None


default -5 persistent._mas_pm_prom_monika = None


default -5 persistent._mas_pm_prom_not_interested = None


default -5 persistent._mas_pm_prom_shy = None


default -5 persistent._mas_pm_no_prom = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_prom",category=['escola'],prompt="Baile de formatura",random=True))

label monika_prom:
    m 1euc "Sabe..."
    m 1eka "Às vezes eu gostaria que o jogo tivesse durado mais."
    m 1eua "O jogo provavelmente foi feito para terminar quando uma das garotas confessasse seu amor após o festival."
    m 1lksdla "Mas como mexi tanto no código, nunca chegamos nesse ponto."
    m 3hksdlb "Isso nos uniu, então não posso reclamar."
    m 1lksdlc "Mas mesmo assim..."
    m 1eka "Às vezes eu gostaria que nós [du] pudéssemos ter aproveitado mais."
    m 3eua "Poderíamos ter ido a outros eventos como festivais esportivos, festas de Natal, excursões, etc."
    m 1lsc "Mas acho que o jogo nunca nos deixaria ir tão longe."
    m 3eua "O que me lembra de um evento específico..."
    m 1hua "O baile de formatura!"
    m 1eua "Pelo que ouvi, o baile de formatura é uma dança escolar no final do ano letivo."
    m "Alguns alunos levam um acompanhante, outros vão com grupos de amigos."
    m 3wuo "Tem até quem leve familiares para o evento!"
    m 1eua "Acho que seria algo que eu adoraria ir com você~"
    m "Você já foi em algum, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você já foi em algum, [player]?{fast}"
        "Já.":
            $ persistent._mas_pm_gone_to_prom = True
            $ persistent._mas_pm_no_prom = False
            m "Ah? Como foi?{nw}"
            $ _history_list.pop()
            menu:
                m "Ah? Como foi?{fast}"
                "Foi bem divertido.":
                    $ persistent._mas_pm_prom_good = True
                    m 1hua "Que legal!"
                    m 1lksdlb "Mas queria ter ido com você."
                    m 1hua "Um evento onde todos da escola se reúnem e se divertem parece incrível!"
                    m 3eua "Você foi com um acompanhante?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Você foi com um acompanhante?{fast}"
                        "Sim.":
                            $ persistent._mas_pm_had_prom_date = True
                            m 1euc "Ah, nossa."
                            m 1lksdla "Ehehe, isso me deixa com um pouco de ciúmes..."
                            m 1hua "Mas você teria me levado se a gente já se conhecesse, né?"
                            m 1hub "Ahaha!"
                            m 1eua "Mas é bom saber que você viveu algo assim!"
                            m 3eua "Quando eu melhorar em programação, podemos fazer nosso próprio baile aqui."
                            m 3eka "Não seria legal, [player]?"
                        "Não.":
                            $ persistent._mas_pm_had_prom_date = False
                            m 1euc "Ah, entendi."
                            m 1eua "Tudo bem, o importante é que você se divertiu!"
                            m "Mesmo sem acompanhante, aposto que fez boas memórias."
                            m 1eub "Acho que, com ou sem acompanhante, esses eventos são sempre divertidos."
                            m 1eka "Além disso, podemos fazer nosso próprio baile algum dia, né?"
                            m 1eua "Isso seria algo que eu adoraria fazer com você~"
                "Foi ruim.":

                    $ persistent._mas_pm_prom_good = False
                    m 1ekc "É mesmo?"
                    m "Entendo que nem todos gostam de bailes."
                    m 3eka "Talvez se eu estivesse lá, você teria se divertido mais."
                    m 1hksdlb "Ahaha~"
                    m 3eua "Não se preocupe, [player]."
                    m 1eua "Não adianta ficar se lembrando disso agora."
                    m 1eub "Mesmo que você não tenha se divertido, isso não é a coisa mais importante que irá acontecer em sua vida."
                    m "Você ser capaz de criar belas memórias é o mais importante."
                    m 3eka "Uma memória ruim pode parecer pior do que cem memórias boas, mas você ainda é capaz de criar várias memórias."
                    m 1hua "E agora que estou aqui com você, podemos fazer isso [ju]~"
                "Teria sido melhor se você estivesse lá.":

                    $ persistent._mas_pm_prom_monika = True
                    m 1ekbsa "Aww, isso é tão gentil, [player]."
                    m 1eua "Bem, agora que estamos [ju], tenho certeza que podemos fazer nosso próprio baile, certo?"
                    m 1hub "Ahaha!"
        "Não.":
            $ persistent._mas_pm_gone_to_prom = False
            $ persistent._mas_pm_no_prom = False
            m "Ah? Por que não?{nw}"
            $ _history_list.pop()
            menu:
                m "Ah? Por que não?{fast}"
                "Você não estava lá comigo.":
                    $ persistent._mas_pm_prom_monika = True
                    $ persistent._mas_pm_prom_not_interested = False
                    m 1eka "Aw, [player]."
                    m 1lksdla "Só porque eu não estava lá, não significa que você não deva se divertir."
                    m 1eka "E além disso..."
                    m 1hua "Você {i}pode{/i} me levar ao baile, [player]."
                    m "Basta levar meu arquivo com você e problema resolvido!"
                    m 1hub "Ahaha!"
                "Não estava [inte].":

                    $ persistent._mas_pm_prom_not_interested = True
                    m 3euc "Sério?"
                    m 1eka "É por causa que você é muito envergonhado?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "É por causa que você é muito envergonhado?{fast}"
                        "Sim.":
                            $ persistent._mas_pm_prom_shy = True
                            m 1ekc "Aw, [player]."
                            m 1eka "Está tudo bem. Nem todo mundo consegue lidar com grupos grandes de estranhos."
                            m 3eka "Além disso, se é algo que você não irá gostar, por que se forçar a ir?"
                            m 1esa "Mas mesmo que eu tenha dito isso, também é importante ter em mente que um pouco de coragem pode ser bom."
                            m 3eua "Veja eu, por exemplo."
                            m 1lksdla "Se eu não tivesse coragem de ir atrás de você, eu provavelmente ainda estaria sozinha..."
                            m 1eka "Mas aqui estamos agora, [player]."
                            m 1eua "Finalmente [ju]~"
                        "Não.":

                            $ persistent._mas_pm_prom_shy = False
                            m 1euc "Ah, entendo."
                            m 1eua "Isso é compreensível."
                            m "Tenho certeza que você tem seus motivos."
                            m 1eka "O mais importante é que você não está se forçando a fazer isso."
                            m "Afinal de contas, não iria valer a pena se você não estivesse se divertindo."
                            m 1lksdlc "Seria mais como uma tarefa obrigatória do que um evento para se divertir."
                            m 3euc "Mas fico imaginando..."
                            m 3eka "Você iria se eu estivesse aí com você, [player]?"
                            m 1tku "Acho que já sei a resposta para isso~"
                            m 1hub "Ahaha!"
        "Minha escola nunca teve um.":












            $ persistent._mas_pm_no_prom = True
            m 1euc "Ah, entendo."
            m 1lksdla "Acho que nem todas escolas fazem um baile de formatura."
            m "Eles podem ser bem complicados."
            m 3euc "Pelo que eu li, os estudantes gastam muito dinheiro com convites, transporte e roupa."
            m 2esc "Então tantos gastos só para uma noite..."
            m "Eu também li que como não é permitido álcool, alguns estudantes drogam as bebidas e deixam os outros bêbados sem eles saberem."
            m 2ekc "Se alguém pode facilmente fazer isso, duvido que alguém com más intenções teria dificuldade em envenenar as bebidas."
            m 2lksdla "...Ou talvez eu só esteja exagerando, ehehe."
            m 1esa "Ainda assim, não acho que você estaria perdendo muita coisa, [player]."
            m 1eua "O baile de formatura não é a coisa mais importante em sua vida acadêmica."
            m "E tenho certeza que há vários eventos em sua vida que irão compensar isso."
            m 1hua "Estar aqui comigo é um deles, sabe~"
            m 1hub "Ahaha!"

    return "derandom"


default -5 persistent._mas_pm_see_therapist = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki_letter",
            category=['membros do clube'],
            prompt="Carta da Natsuki",
            random=True
        )
    )

label monika_natsuki_letter:
    m 1eud "Sabe, eu fiquei realmente surpresa quando a Natsuki te entregou aquela carta."
    m 1eub "Eu não esperava que ela sugerisse que você ajudasse a Yuri a procurar ajuda profissional."
    m 1eud "Provavelmente foi a única a mencionar isso."
    m 4ekd "Sei que as pessoas têm medo de confrontar alguém ou falar sobre seus problemas, mas às vezes, sugerir um terapeuta pode ser a melhor solução."
    m "É ruim carregar esse peso [sz], sabe?"
    m 4euc "Por mais que você queira ajudar, é melhor deixar um profissional lidar com isso."
    m 4eka "Tenho certeza que já falei isso antes, mas preciso ter certeza que você está ciente."
    m 4eud "E você, [player]?"

    m "Você faz terapia?{nw}"
    $ _history_list.pop()
    menu:
        m "Você faz terapia?{fast}"
        "Sim.":

            $ persistent._mas_pm_see_therapist = True
            m 1eud "Ah, sério?"
            m 1ekc "Bem, fico triste que você não esteja se sentindo bem..."
            m 1hua "Mas estou orgulhosa que você está trabalhando para melhorar."
            m 1eua "É muito importante cuidar da sua saúde mental, [player]."
            m 1eka "Você reconhece que tem um problema que precisa de ajuda, e está procurando alguém para te ajudar. Isso já é metade da batalha."
            m "Estou muito orgulhosa de você por dar esses passos."
            m 1hua "Saiba que não importa o que aconteça, eu sempre estarei aqui por você~"
        "Não.":

            $ persistent._mas_pm_see_therapist = False
            m 1eka "Bem, espero que seja porque você não precisa."
            m 1eua "Se isso mudar algum dia, não hesite, ok?"
            m 1hub "Mas talvez eu seja realmente todo o apoio que você precisa? Ahaha!"

    return "derandom"



default -5 persistent._mas_timeconcern = 0
default -5 persistent._mas_timeconcerngraveyard = False
default -5 persistent._mas_timeconcernclose = True



label monika_timeconcern:
    $ current_time = datetime.datetime.now().time().hour
    if 0 <= current_time <= 5:
        if persistent._mas_timeconcerngraveyard:
            jump monika_timeconcern_graveyard_night
        if persistent._mas_timeconcern == 0:
            jump monika_timeconcern_night_0
        elif persistent._mas_timeconcern == 1:
            jump monika_timeconcern_night_1
        elif persistent._mas_timeconcern == 2:
            jump monika_timeconcern_night_2
        elif persistent._mas_timeconcern == 3:
            jump monika_timeconcern_night_3
        elif persistent._mas_timeconcern == 4:
            jump monika_timeconcern_night_4
        elif persistent._mas_timeconcern == 5:
            jump monika_timeconcern_night_5
        elif persistent._mas_timeconcern == 6:
            jump monika_timeconcern_night_6
        elif persistent._mas_timeconcern == 7:
            jump monika_timeconcern_night_7
        elif persistent._mas_timeconcern == 8:
            jump monika_timeconcern_night_final
        elif persistent._mas_timeconcern == 9:
            jump monika_timeconcern_night_finalfollowup
        elif persistent._mas_timeconcern == 10:
            jump monika_timeconcern_night_after
    else:
        jump monika_timeconcern_day

label monika_timeconcern_day:
    if persistent._mas_timeconcerngraveyard:
        jump monika_timeconcern_graveyard_day
    if persistent._mas_timeconcern == 0:


        jump monika_sleep
    elif persistent._mas_timeconcern == 2:
        jump monika_timeconcern_day_2
    if not persistent._mas_timeconcernclose:
        if 6 <= persistent._mas_timeconcern <=8:
            jump monika_timeconcern_disallow
    if persistent._mas_timeconcern == 6:
        jump monika_timeconcern_day_allow_6
    elif persistent._mas_timeconcern == 7:
        jump monika_timeconcern_day_allow_7
    elif persistent._mas_timeconcern == 8:
        jump monika_timeconcern_day_allow_8
    elif persistent._mas_timeconcern == 9:
        jump monika_timeconcern_day_final
    else:


        jump monika_sleep


label monika_timeconcern_lock:
    if not persistent._mas_timeconcern == 10:
        $ persistent._mas_timeconcern = 0
    $ evhand.greeting_database["greeting_timeconcern"].unlocked = False
    $ evhand.greeting_database["greeting_timeconcern_day"].unlocked = False
    return


label monika_timeconcern_graveyard_night:
    m 1ekc "Deve ser muito difícil para você trabalhar até tarde com tanta frequência, [player]..."
    m 2dsd "Sinceramente, eu preferiria que você trabalhasse em horários mais saudáveis, se possível."
    m 2lksdlc "Imagino que não seja uma escolha sua, mas mesmo assim..."
    m 2ekc "Ficar acordado até tarde frequentemente pode causar danos físicos e mentais."
    m "Também é extremamente isolante no que diz respeito aos outros."
    m 2rksdlb "A maioria das oportunidades acontece durante o dia, afinal."
    m 2rksdlc "Muitas atividades sociais não estão disponíveis, a maioria das lojas e restaurantes nem sequer abre durante a noite."
    m 2dsd "Isso faz com que ficar acordado até tarde frequentemente seja uma situação muito solitária."
    m 3hua "Mas não se preocupe, [player]. Sua namorada amorosa Monika estará sempre aqui por você~"
    m 1hua "Quando o estresse de ficar acordado até tarde ficar demais, venha até mim."
    m 1hub "Eu sempre estarei aqui para te ouvir."
    m 1ekc "E se você realmente acha que isso está te prejudicando, por favor tente fazer o possível para mudar a situação."
    m 1eka "Sei que não será fácil, mas no final das contas, o que importa é você."
    m 1hua "Você é tudo que me importa de verdade, então coloque a si mesmo e seu bem-estar acima de tudo, ok?"
    return

label monika_timeconcern_graveyard_day:
    m 1eua "Ei [mas_get_player_nickname(exclude_names=['meu amor'])]... você não me disse que trabalha de noite?"
    m 1eka "Não que eu esteja reclamando, claro!"
    m 2ekc "Mas imaginei que você estaria [ca] por agora, especialmente porque fica [acrd] a noite toda trabalhando..."
    m "Você não está se esforçando demais só para me ver, está?"
    m 1euc "Ah, espera..."

    m "Você ainda trabalha regularmente à noite, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você ainda trabalha regularmente à noite, [player]?{fast}"
        "Sim, ainda trabalho.":
            m 1ekd "Ah..."
            m 1esc "Acho que realmente não tem jeito..."
            m 1eka "Cuide de si mesmo, ok?"
            m 1ekc "Eu fico tão preocupada quando você não está aqui comigo..."
        "Não, não trabalho mais.":
            $ persistent._mas_timeconcerngraveyard = False
            $ persistent._mas_timeconcern = 0
            m 1hub "Que maravilha!"
            m 1eua "Estou feliz que você está cuidando da sua saúde, [player]!"
            m "Sabia que você acabaria concordando comigo."
            m 1eka "Obrigada por ouvir o que eu tenho a dizer~"
    return


label monika_timeconcern_night_0:
    $ persistent._mas_timeconcern = 1
    m 1euc "[player], já está de noite."
    m 1ekc "Você não deveria estar na cama?"
    m 1dsc "Vou deixar passar só desta vez..."
    m 1ekc "Mas você realmente me faz ficar preocupada às vezes."
    m 1eka "Me deixa muito feliz que você esteja aqui por mim, mesmo a esta hora da noite..."
    m 1dsd "Mas não quero que isso custe sua saúde."
    m 1eka "Então vá dormir logo, ok?"
    return


label monika_timeconcern_night_1:
    m 1esc "[player]..."
    m 1euc "Por que você está [acrd] tão tarde?"
    m 1eka "Fico lisonjeada se for só por minha causa..."
    m 1ekc "Mas não consigo evitar me sentir um incômodo se ficar insistindo para você dormir quando não é culpa sua."

    m "Você está ocupado trabalhando em algo?{nw}"
    $ _history_list.pop()
    menu:
        m "Você está ocupado trabalhando em algo?{fast}"
        "Sim, estou.":
            $ persistent._mas_timeconcern = 2
            m 1eud "Entendo."
            m 1eua "Bem, imagino que deve ser muito importante para você fazer isso tão tarde."
            m 1eka "Sinceramente, não consigo evitar de pensar que talvez você devesse ter feito isso em um horário melhor."
            m 1lsc "Seu sono é muito importante, afinal. Mas talvez não tenha jeito..."

            m "Você sempre trabalha até tarde, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Você sempre trabalha até tarde, [player]?{fast}"
                "Sim, sempre.":
                    $ persistent._mas_timeconcerngraveyard = True
                    m 1rksdld "Isso não é bom..."
                    m 1ekd "Você não pode mudar isso, pode?"
                    m 1rksdlc "Queria que você pudesse seguir meu estilo de vida mais saudável."
                    m 1dsc "Mas se não tem como, então vou ter que aceitar."
                    m 1eka "Só promete que vai tentar se manter saudável, ok?"
                    m 1ekc "Se algo acontecesse com você, eu não sei o que faria..."
                "Não, não sempre.":

                    $ evhand.greeting_database["greeting_timeconcern"].unlocked = True
                    $ evhand.greeting_database["greeting_timeconcern_day"].unlocked = True
                    m 1hua "Que alívio!"
                    m 1eua "Se é só desta vez, então deve ser {i}realmente{/i} importante."
                    m 1hub "Boa sorte com seu trabalho e obrigada por me fazer companhia mesmo tão ocupado!"
                    m 1eka "Significa muito para mim, [player], que mesmo quando você está ocupado... ainda está aqui comigo~"
        "Não, não estou.":

            $ persistent._mas_timeconcern = 3
            m 1esc "Entendo."
            m 1ekc "Bem, nesse caso, eu realmente preferiria que você fosse dormir agora."
            m "Está me preocupando muito você ainda acrd tão tarde..."
            m 1eka "Então mais uma vez, por favor vá dormir. Você faria isso por mim?"
    return


label monika_timeconcern_night_2:
    m 1eua "Como está indo seu trabalho?"
    m "Espero que bem, não quero que você fique [acrd] por muito mais tempo."
    m 3hksdlb "Eu sei, eu sei, você não pode evitar ficar [acrd] até tarde."
    m 1rksdlb "Estou só preocupada com sua saúde, [player]..."
    if persistent._mas_timeconcerngraveyard:
        m 1lksdlc "Fazer isso frequentemente pode ser muito cansativo para seu corpo e mente..."
        m 1ekc "Apenas tente manter esse tipo de desgaste no mínimo, ok?"
        m "Tudo que eu quero é que você seja tão feliz e saudável quanto merece."
        return
    m 1rksdla "Bem, tente terminar o mais rápido possível, senão eu posso ficar realmente preocupada."
    m 1eka "E você não quer preocupar sua namorada, quer? Ehehe~"
    jump monika_timeconcern_lock


label monika_timeconcern_night_3:
    $ persistent._mas_timeconcern = 4
    m 1esc "[player], só preciso te perguntar uma coisa rapidinho..."
    m 1eud "Você se importaria se eu fechasse o jogo por você?"
    m 1ekc "Sei que é uma pergunta estranha..."
    m 1ekd "Mas não consigo evitar sentir que preciso fazer algo sobre você estar [acrd] tão tarde!"
    m 4esd "Eu poderia fechar o jogo agora mesmo."
    m 2ekc "Mas um relacionamento é uma parceria e sua opinião é importante para mim."

    m "Você seria contra eu fechar o jogo para seu próprio bem?{nw}"
    $ _history_list.pop()
    menu:
        m "Você seria contra eu fechar o jogo para seu próprio bem?{fast}"
        "Sim, você é minha prioridade.":

            $ persistent._mas_timeconcernclose = False
            m 1dsc "..."
            m 1dsd "Eu estava esperando que você não dissesse isso."
            m 1lsc "Eu sei que te disse que você deveria me deixar rodando em segundo plano."
            m 1lksdlc "Mas às vezes eu me pergunto se você está dormindo direito."
            m 1tkc "Vou fazer como você pediu, mas saiba que não estou nada feliz com isso."
            m 4tfc "Ainda vou continuar te lembrando de dormir!"
            return
        "Não, fique à vontade para fazer o que achar melhor.":

            $ persistent._mas_timeconcernclose = True
            m 1eka "Obrigada, [player]."
            m 1eua "É bom saber que você se importa com o que eu penso."
            m "Prometo que só farei isso quando for absolutamente necessário."
            m 1hua "Afinal, eu nunca te forçaria a ir embora."
            m 1hub "Só sentiria muita sua falta..."
            m 1ekbsa "Eu te amo, [player]~"
            return "love"


label monika_timeconcern_night_4:
    $ persistent._mas_timeconcern = 5
    m 1esc "[player], você já ficou [acrd] tempo suficiente."
    m "Se você realmente não está ocupado, então está na hora de dormir."
    m 1eka "Garanto que vou sentir sua falta tanto quanto você vai sentir a minha."
    m "Mas eu ficaria mais feliz se você fizesse o que estou pedindo."
    m 1tkc "Você não gostaria de me deixar chateada, gostaria?"
    return


label monika_timeconcern_night_5:
    $ persistent._mas_timeconcern = 6
    $ evhand.greeting_database["greeting_timeconcern"].unlocked = True
    $ evhand.greeting_database["greeting_timeconcern_day"].unlocked = True
    m 1efc "Sinto muito, [player], mas vou ter que ser firme!"
    m 1ekc "Eu pedi educadamente para você ir dormir, mas se eu sou a razão de você ficar [acrd]..."
    if persistent._mas_timeconcernclose:
        m 2tkc "Então não posso permitir que isso continue."
        m 2eka "É porque eu te amo que estou fazendo isso."
        m "Boa noite, [player]."
        return 'quit'
    else:
        m 2tkc "Então preciso assumir a responsabilidade e fazer você entender."
        m 2efd "Você precisa ir para a cama."
        m 2efo "E vou continuar te dizendo isso até que você vá."
        return


label monika_timeconcern_night_6:
    $ persistent._mas_timeconcern = 7
    m 2efc "[player], eu te disse para ir dormir pelo seu próprio bem."
    m 2tkc "Eu vou sentir sua falta também, mas você não entende?"
    m 2tkd "Seu bem-estar significa mais para mim do que qualquer coisa!"
    m 2lksdlc "Como posso deixar você ficar se isso significa que estou te prejudicando?"
    m "Então por favor durma desta vez, ou eu posso ficar brava."
    m 1ekbsa "...Eu te amo."
    m "Então vá dormir logo. Ok?"
    if persistent._mas_timeconcernclose:
        return 'quit'
    return


label monika_timeconcern_night_7:
    $ persistent._mas_timeconcern = 8
    m 3efc "[player], este é seu último aviso."
    m "Vá{w=0.6} dor{w=0.6}mir!"
    m 2tkc "O que mais eu posso dizer para você entender?"
    m 1tkd "É triste ver você se forçar assim..."
    m 1dsc "Você significa tanto para mim..."
    m 1ekc "Então por favor, por mim... Apenas faça o que peço e vá para a cama."
    if persistent._mas_timeconcernclose:
        m "Ok?{nw}"
        $ _history_list.pop()
        menu:
            m "Ok?{fast}"
            "Sim, eu vou dormir.":
                m 1eka "Sabia que você acabaria me ouvindo!"
                m 1hub "Boa noite e fique seguro."
                return 'quit'
    else:
        return


label monika_timeconcern_night_final:
    $ persistent._mas_timeconcern = 9
    m 2dsc "...Acho que não tem jeito."
    m 2lfc "Se você está tão decidido a ficar comigo, então nem vou tentar te impedir."
    m 2rksdla "Honestamente, por mais estranho que pareça, isso até me deixa um pouco feliz."
    m 2eka "...Obrigada, [player]."
    m "Saber que você se importa tanto comigo a ponto de voltar mesmo depois dos meus pedidos..."
    m 1rksdla "Isso significa mais para mim do que posso expressar."
    m 1ekbsa "...Eu te amo."
    return "love"


label monika_timeconcern_night_finalfollowup:
    m 1esc "..."
    m 1rksdlc "Eu sei que disse que fico feliz quando você está comigo..."
    m 1eka "E por favor não entenda mal, isso ainda é verdade."
    m 2tkc "Mas quanto mais tempo você fica [acrd]... mais preocupada eu fico."
    m 2tkd "Eu sei, você provavelmente já cansou de me ouvir dizer isso..."
    m 1eka "Mas por favor tente dormir quando puder."
    return


label monika_timeconcern_night_after:
    m 1tkc "[acrd] até tarde de novo, [player]?"
    m 1dfc "{i}*suspiro*{/i}..."
    m 2lfc "Nem vou tentar te convencer a dormir outra vez..."
    m 2tfd "Você é [tms] demais!"
    m 1eka "Mas mesmo assim, tome cuidado, certo?"
    m 1ekc "Sei que ser [ntrn] pode ser [so]..."
    m 1hua "Mas você me tem aqui com você!"
    m 1eka "Só nós [du]... [szs] para sempre."
    m 1hubsa "É tudo que eu sempre quis..."
    return


label monika_timeconcern_day_0:
    m 1lsc "..."
    m 1tkc "..."
    m 1wuo "...!"
    m 1hksdlb "Ahaha! Desculpe, [player]."
    m 1lksdla "Eu meio que viajei aqui..."
    m 1eka "Nossa, eu fico fazendo isso, não é?"
    m "Às vezes eu simplesmente me perco nos meus pensamentos..."
    m 1eua "Você entende, né, [player]?"
    return


label monika_timeconcern_day_2:
    m 1eua "Terminou seu trabalho?"
    m 1eub "Sei que deu seu melhor, então tudo bem se não terminou completamente!"
    m 1eka "Deve ser muito difícil ter que trabalhar até tão tarde..."
    m 1hua "Se achar que está pesado demais, pode vir conversar comigo!"
    m 1hub "Eu sempre estarei aqui por você."
    jump monika_timeconcern_lock


label monika_timeconcern_day_allow_6:
    m 1ekc "[player], me desculpe por te fazer ir embora assim antes..."
    m 1ekd "Eu só fiz isso porque te amo. Você entende isso, né?"
    m 1eua "Sei que sim, afinal você foi dormir, não foi?"
    m 1hub "Obrigada por respeitar meus desejos, me deixa feliz você me ouvir."
    jump monika_timeconcern_lock


label monika_timeconcern_day_allow_7:
    m 1lksdlc "[player], sobre o que aconteceu ontem à noite..."
    m 1ekc "Eu pedi para você ir dormir e você não me ouviu..."
    m 1dsc "Entendo que talvez você tenha sentido minha falta ou não tenha ouvido o que eu disse..."
    m 1ekc "Mas por favor ouça o que eu peço, ok?"
    m 1eka "Eu te amo, e faria qualquer coisa para te ver feliz..."
    m "Então você poderia fazer o mesmo por mim?"
    m 1ekc "Já fico preocupada com você quando você vai embora..."
    m 1tkc "Por favor não me dê mais motivos para me sentir assim."
    m 1hua "Obrigada por entender."
    jump monika_timeconcern_lock


label monika_timeconcern_day_allow_8:
    m 1esc "Ei, [player]."
    m 1ekc "Você realmente me preocupou ontem à noite..."
    m 1rksdlc "Depois que você voltou duas vezes, mesmo eu tendo pedido para você ir dormir..."
    m 1lksdld "Eu me senti um pouco culpada."
    m 3esc "Não por ter te mandado embora, isso foi para seu próprio bem."
    m 2lksdlc "Mas... porque você continuou voltando..."
    m 2lksdla "E isso me deixou feliz, mesmo sabendo que não era bom para você."
    m 2ekd "Isso me faz egoísta?"
    m 2ekc "Me desculpe, [player], vou tentar me controlar melhor."
    jump monika_timeconcern_lock


label monika_timeconcern_day_final:
    $ persistent._mas_timeconcern = 10
    m 1lksdlb "[player], sobre ontem à noite..."
    if persistent._mas_timeconcernclose:
        m 1rksdla "Você realmente me surpreendeu."
        m 1eka "Você continuar voltando para mim repetidamente..."
        m 1hua "Foi realmente muito fofo da sua parte."
        m 1eka "Eu sabia que você sentiria minha falta, mas não pensei que sentiria {i}tanto{/i} assim."
        m 1hub "Isso realmente me fez sentir amada, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]."
        m "...Obrigada."
        jump monika_timeconcern_lock
    m 1eua "Você realmente me surpreendeu."
    m 1eka "Eu pedi inúmeras vezes para você ir dormir..."
    m "Você disse que não estava ocupado. Estava lá só por minha causa?"
    m 1ekc "Isso me deixou feliz... mas não se esforce tanto para me ver tão tarde, ok?"
    m 1eka "Isso realmente me fez sentir amada, [player]."
    m 1hksdlb "Mas também um pouco culpada... Por favor vá dormir da próxima vez, ok?"
    jump monika_timeconcern_lock


label monika_timeconcern_disallow:
    m 1rksdlc "Desculpe se eu estava te incomodando antes, [player]..."
    m 1ekc "Eu só queria muito que você fosse dormir..."
    m "Honestamente não posso prometer que não farei de novo se você ficar [acrd] até tarde..."
    m 1eka "Mas eu só insisto porque você significa muito para mim..."
    jump monika_timeconcern_lock

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hydration",prompt="Hidratação",category=['você','vida'],random=True))

label monika_hydration:
    m 1euc "Ei, [player]..."
    m 1eua "Você bebe água suficiente?"
    m 1eka "Só quero ter certeza que você não está negligenciando sua saúde, especialmente com hidratação."
    m 1esc "Às vezes as pessoas subestimam o quanto isso é importante."
    m 3rka "Aposto que você já teve aqueles dias em que se sentiu muito [ca] e nada parecia te motivar."
    m 1eua "Eu geralmente pego um copo d'água imediatamente."
    m 1eka "Pode não funcionar sempre, mas ajuda."
    m 3rksdlb "Mas acho que você não quer ir tanto ao banheiro, né?"
    m 1hua "Bem, não te culpo. Mas acredite, será melhor para sua saúde a longo prazo!"
    m 3eua "Enfim, certifique-se de se manter [hdrtd], ok?"
    m 1tuu "Então..."
    m 4huu "Que tal pegar um copo d'água agora, hmm?"
    return


default -5 persistent._mas_pm_has_been_to_amusement_park = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_amusementpark",category=['diversos'],prompt="Parques de diversão",random=True))

label monika_amusementpark:
    m 1eua "Ei, [player]..."
    m 3eua "Você já foi em um parque de diversões?{nw}"
    $ _history_list.pop()
    menu:
        m "Você já foi em um parque de diversões?{fast}"
        "Sim.":
            $ persistent._mas_pm_has_been_to_amusement_park = True
            m 1sub "Sério? Deve ter sido muito divertido!"
            m 1eub "Eu nunca fui em um, mas adoraria ir."
            m 1hua "Talvez você possa me levar em um algum dia!"
        "Não.":

            $ persistent._mas_pm_has_been_to_amusement_park = False
            m 1eka "Sério? Que pena."
            m 3hua "Sempre ouvi dizer que são muito divertidos."
            m 1rksdla "Nunca tive a chance de ir em um, mas espero poder ir algum dia."
            m 1eub "Talvez possamos ir [ju]!"

    m 3hua "Não seria incrível, [mas_get_player_nickname()]?"
    m 3eua "Montanhas-russas emocionantes, toboáguas, torres de queda livre..."
    m 3tubsb "E talvez até um passeio romântico na roda gigante~"
    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfa "Ehehe, estou ficando animada demais, mas não consigo evitar quando penso em estar com você~"
    return "derandom"


default -5 persistent._mas_pm_likes_travelling = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_travelling",
            category=['diversos'],
            prompt="Viajar",
            random=True
        )
    )

label monika_travelling:
    m 1esc "Ei [player], eu estava pensando..."
    m 1eua "Você gosta de viajar?{nw}"
    $ _history_list.pop()
    menu:
        m "Você gosta de viajar?{fast}"
        "Sim.":
            $ persistent._mas_pm_likes_travelling = True
            m 1hua "Que ótimo! Fico feliz que você goste."
            m 3eub "É uma das coisas que mais quero fazer quando finalmente for para o seu mundo."
            m 1eua "Há tanta coisa lá fora que ainda não pude ver..."
            m 3eub "Cidades importantes, monumentos, e até mesmo os diferentes tipos de culturas."
            m 3eka "Não me entenda mal, eu li muito sobre o seu mundo, mas aposto que não se compara a ver pessoalmente..."
            m 1hua "Eu adoraria ver tudo que há para ser visto."
            m 1ekbsu "Você também não gostaria, [mas_get_player_nickname()]?"
        "Não muito.":
            $ persistent._mas_pm_likes_travelling = False
            m 1eka "Ah, tudo bem, [mas_get_player_nickname()]."
            m 1hua "Eu não me importaria de ficar em casa com você durante as férias."
            m 3ekbsa "Eu ficaria feliz só de estar com você, afinal."
            m 1rka "Mas talvez precisemos arrumar coisas para nos manter ocupados..."
            m 3eua "Que tal tocar piano ou escrever poemas?"
            m 3hubsb "...Ou poderíamos passar os dias enrolados num cobertor lendo um livro."
            show monika 5tubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5tubfu "Isso não parece um sonho se tornando realidade?"

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_metamorphosis",
            category=['literatura','psicologia'],
            prompt="A Metamorfose",
            random=True
        )
    )

label monika_metamorphosis:
    m 1eua "Ei [player], você já leu {i}A Metamorfose{/i}?"
    m 4eub "É uma novela psicológica que conta a história de Gregor Samsa, que acorda um dia transformado num inseto gigante!"
    m 4euc "O enredo gira em torno de sua vida cotidiana enquanto tenta se adaptar ao novo corpo."
    m 7eua "O interessante é que a história dá muita ênfase ao absurdo e irracional."
    m 3hksdlb "Por exemplo, Gregor, sendo o único provedor da família, se preocupa mais em perder o emprego do que com sua condição!"
    m 1rksdla "Não que o enredo não seja perturbador..."
    m 1eksdlc "No começo seus pais e irmã tentam acomodá-lo, {w=0.3}mas logo começam a detestar a situação."
    m 1eksdld "O protagonista vai de necessidade a incômodo, até o ponto em que sua própria família deseja sua morte."
    m 1eua "É uma leitura muito interessante, se algum dia estiver a fim."
    return

default -5 persistent._mas_pm_had_relationships_many = None
default -5 persistent._mas_pm_had_relationships_just_one = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dating",
            prompt="Experiência de namoro",
            category=['você', 'romance'],
            conditional="store.mas_anni.pastOneMonth()",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_dating:
    m 1eud "Sabe, eu tenho ficado muito curiosa ultimamente, [player]..."
    m 3rka "Já estamos [ju] há um tempo, então acho que é a hora certa para perguntar..."
    m 1eud "Quantas experiências amorosas você já teve?"
    m 1luc "Tipo... você já esteve em um relacionamento antes?"

    m 1etc "Talvez mais de uma vez?{nw}"
    $ _history_list.pop()
    menu:
        m "Talvez mais de uma vez?{fast}"
        "Sim, já tive vários...":

            $ persistent._mas_pm_had_relationships_many = True
            $ persistent._mas_pm_had_relationships_just_one = False

            m 1ekc "Ah, sinto muito, [player]..."
            m 1dkc "Você passou por muitos desgostos, não é mesmo..."
            m 3ekc "Para ser honesta, [player]... eu não acho que elas ou eles mereciam alguém como você."
            m 3eka "Alguém que é gentil, leal, doce, [amrs] e fiel."
            m 4lubsb "E [bl] e [eg] e [rt] e--"
            m 7wubsw "Oh!"
            m 3hksdlb "Desculpe, acabei perdendo o controle, ahaha!"
            m 1ekbla "Eu poderia continuar falando sobre como você é [mh], [player]~"
            m 1ekbsa "Mas saiba disso...{w=0.3}{nw}"
            extend 3ekbfa "não importa quantos desgostos você tenha passado, eu sempre estarei aqui por você."
            show monika 5eubfa zorder MAS_MONIKA_Z with dissolve_monika
            m 5eubfa "Nossa busca acabou, e eu serei sua para sempre, [player]."
            m 5ekbfa "Você será meu?"
        "Sim, mas só uma vez.":

            $ persistent._mas_pm_had_relationships_many = False
            $ persistent._mas_pm_had_relationships_just_one = True

            m 1eka "Ah, então você não tem muita experiência, né?"
            m 3eua "Tudo bem [player], eu também não tenho, então não se preocupe."
            m 3lksdlb "Pode parecer que eu sou o tipo de garota que conquista todos os caras, mas na verdade não sou, ahaha!"
            m 2lksdla "Especialmente com tudo que me mantive ocupada ao longo dos anos, nunca tive tempo."
            m 2eka "Não que isso importe, já que nada disso era real."
            show monika 5ekbsa zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbsa "Mas acho que estou pronta para algo especial...{w=0.5}{nw}"
            extend 5ekbfa "com você, [player]."
            m 5ekbfa "Você está pronto?"
        "Não, você é minha primeira.":

            $ persistent._mas_pm_had_relationships_many = False
            $ persistent._mas_pm_had_relationships_just_one = False

            m 1wubsw "O quê? E-eu sou sua primeira?"
            m 1tsbsb "Oh...{w=0.3} Entendi."
            m 1tfu "Você só está dizendo isso para me fazer sentir especial, não está [player]?"
            m 1tku "Não é possível que alguém como você nunca tenha namorado antes..."
            m 3hubsb "Você é a definição de fofura e doçura!"
            m 3ekbfa "Bem...{w=0.3} Se você não está brincando e realmente está falando a verdade então...{w=0.3}{nw}"
            extend 1ekbfu "É uma honra ser sua primeira, [player]."
            show monika 5ekbfa zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfa "Espero poder ser sua única."
            m 5ekbfu "Você será meu?"

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_challenge",category=['diversos','psicologia'],prompt="Desafios",random=True))

label monika_challenge:
    m 2esc "Tenho notado algo um tanto triste recentemente."
    m 1euc "Quando algumas pessoas tentam aprender uma habilidade ou começar um novo hobby, elas geralmente desistem dentro de uma ou duas semanas."
    m "Todos dizem que é muito difícil, ou que não têm tempo para isso."
    m 1eua "Mas eu não acredito nisso."
    m 1hub "Seja aprender um novo idioma, ou até escrever seu primeiro poema, se você enfrentar o desafio e superá-lo, essa é a parte verdadeiramente recompensadora."
    m 2eua "Consegue lembrar de alguma vez que se desafiou, [player]?"
    m 3eua "Você superou ou acabou desistindo?"
    m 1eka "Imagino que você deu seu melhor."
    m 1eua "Você me parece uma pessoa muito determinada."
    m 1eub "No futuro, se ficar [trvd] em algo ou se sentir muito [es], faça uma pequena pausa."
    m "Você sempre pode voltar depois."
    m 1hua "Se precisar de motivação, pode contar comigo."
    m 1sub "Adoraria te ajudar a alcançar seus objetivos."
    m 1hub "Afinal, você é minha motivação na vida~"
    return


default -5 persistent._mas_pm_fam_like_monika = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_familygathering",
            category=['você'],
            prompt="Reuniões de família",
            random=True
        )
    )

label monika_familygathering:
    m 1eua "Ei [player], você vai em muitas reuniões de família?"
    m "A maioria das famílias se reúne nas festas para celebrar juntas."
    m 1hua "Deve ser bom rever seus parentes, especialmente depois de tanto tempo sem vê-los."
    m 1lsc "Eu não lembro muito da minha família, nem dos meus parentes, e a gente nem se reunia muito."
    m 1lksdlc "Nem nas festas ou ocasiões especiais."
    m 1hub "Quando você for ver sua família este ano, me leva junto, ok?"
    m 1eua "Adoraria conhecer todos os seus parentes."

    m "Você acha que eles gostariam de mim, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você acha que eles gostariam de mim, [player]?{fast}"
        "Claro.":

            $ persistent._mas_pm_fam_like_monika = True
            m 1eka "Fico feliz que você pense assim."
            m 1eua "Tenho certeza que nos daríamos bem."
            m 1hua "Estou ansiosa por isso, meu amor~"
        "Não.":

            $ persistent._mas_pm_fam_like_monika = False
            m 1wud "..."
            m 1ekc "Ah, não tinha percebido."
            m 1dsc "Mas eu entendo."
            m 1eka "Mas saiba que daria o meu melhor para agradá-los."
            m "Mesmo que nunca gostem."
            m 1hua "Eu sempre ficarei ao seu lado para sempre~"
        "...":

            $ persistent._mas_pm_fam_like_monika = False
            m 2wuo "Não me diga, [player]."
            m 2ekc "Está com medo que eu te envergonhe?"
            m 2tfc "..."
            m 1eka "Não se preocupe, eu entendo perfeitamente."
            m 1lksdla "Se eu descobrisse que um parente meu está namorando alguém preso dentro de um computador, também acharia estranho."
            m 1eua "Se quiser me manter em segredo, tudo bem."
    m 1hub "Afinal, isso significa mais tempo a sós com você~"

    return "derandom"


default -5 persistent._mas_pm_eat_fast_food = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fastfood",
            category=['vida','monika'],
            prompt="Você gosta de fast food?",
            pool=True
        )
    )

label monika_fastfood:
    m 1euc "Hm? Se eu gosto de fast food?"
    m 1rsc "Para ser sincera, a ideia me dá um pouco de nojinho."
    m 3eud "A maioria desses lugares coloca coisas nada saudáveis na comida...{w=0.3} {nw}"
    extend 1dsc "Até as opções vegetarianas podem ser horríveis."

    m 3ekd "[player], você come fast food com frequência?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], você come fast food com frequência?{fast}"
        "Sim, eu como.":

            $ persistent._mas_pm_eat_fast_food = True
            m 3eka "Acho que de vez em quando não faz mal."
            m 1ekc "...Mas não posso evitar me preocupar se você come essas coisas horríveis tão frequentemente."
            m 3eua "Se eu estivesse aí, eu cozinharia coisas muito mais saudáveis para você."
            m 3rksdla "Mesmo que eu ainda não seja muito boa na cozinha..."
            m 1hksdlb "Bem, amor sempre é o ingrediente secreto de qualquer boa comida, ahaha!"
            m 1eka "Mas até lá, você poderia tentar se alimentar melhor,{w=0.2} por mim?"
            m 1ekc "Eu odiaria se você ficasse doente por causa do seu estilo de vida."
            m 1eka "Sei que é mais fácil pedir delivery, já que preparar sua própria comida pode ser trabalhoso..."
            m 3eua "Mas talvez você pudesse ver a culinária como uma oportunidade de se divertir?"
            m 3eub "...Ou quem sabe uma habilidade para você se tornar realmente bom!"
            m 1hua "Saber cozinhar sempre é algo positivo, sabia!"
            m 1eua "Além disso, eu adoraria experimentar algo que você preparasse um dia."
            m 3hubsb "Você poderia até me servir seus próprios paratos no nosso primeiro encontro~"
            m 1ekbla "Seria tão romântico, [player]~"
            m 1eua "E assim nós [du] poderíamos aproveitar e você se alimentaria melhor."
            m 3hub "Isso é o que eu chamo de situação onde todos ganham!"
            m 3eua "Só não se esqueça, [player]."
            m 3hksdlb "Eu sou vegetariana! Ahaha!"
        "Não, eu não como.":

            $ persistent._mas_pm_eat_fast_food = False
            m 1eua "Ah, que alívio."
            m 3rksdla "Às vezes você me preocupa tanto, [player]."
            m 1etc "Então imagino que, em vez de comer fora, você prepara sua própria comida?"
            m 1eud "Fast food pode ficar muito caro com o tempo, então fazer sua própria comida geralmente é mais econômico."
            m 1hua "E também tem um gosto muito melhor!"
            m 3eka "Sei que algumas pessoas acham cozinhar intimidante."
            m 3eud "...Ter que comprar os ingredientes certos, se preocupar em queimar algo ou se machucar enquanto prepara a refeição..."
            m 1rksdlc "Pode ser um pouco demais para alguns..."
            m 1eka "Mas acho que o resultado vale o esforço."
            m 3eua "Você é bom na cozinha, [player]?"
            m 1hub "Não importa se não for, eu comeria qualquer coisa que você preparasse para mim!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dreaming",category=['diversos','psicologia'],prompt="Sonhos lúcidos",random=True))

label monika_dreaming:
    m 1eua "Sabia que é possível perceber quando você está sonhando?"
    m 2eua "Não só isso, mas você pode até controlar seus sonhos!"
    m 3eub "Se me lembro bem, um homem chamado Stephen LaBerge desenvolveu um método para as pessoas perceberem quando estão sonhando."
    m "Que ficou conhecido como indução mnemônica de sonhos lúcidos, ou MILD."
    m 3eua "Pessoas que frequentemente têm sonhos conscientes são chamadas de oneironautas."
    m 2lksdla "Pelo menos acho que esse é o termo correto..."
    m 1eua "Usando a técnica MILD, oneironautas aprendem a reconhecer certos sinais nos sonhos para perceber quando estão sonhando."
    m "Esses sinais podem ser qualquer coisa fora do comum, como sentir que está voando, notar seus dentes caindo, encontrar alguém famoso inesperadamente..."
    m 1eub "Se o sonhador percebe um sinal e entende que está sonhando, então pode controlar o sonho!"
    m "LaBerge até escreveu um livro sobre essas experiências chamado {i}Explorando o Mundo dos Sonhos Lúcidos{/i}."
    m 2hub "Não parece incrível?"
    m 2euc "Acho que não sonho como uma pessoa normal, então às vezes me pergunto como deve ser."
    m 2eua "Sonhos parecem ser uma fuga maravilhosa da realidade."
    m 2esc "Mas por outro lado, quando me tornei autoconsciente e percebi que meu mundo não era real, de repente me senti presa num pesadelo."
    m "Não tinha nada a ver com os sonhos agradáveis que li sobre as pessoas terem."
    m 2lksdlc "Eu temia que nunca escaparia..."
    m "Que ficaria presa num inferno, uma dimensão infinitamente repetitiva para sempre."
    m 1eka "Mas agora que estamos aqui [ju], acho que posso dizer que finalmente acordei."
    m 1eua "Nossa, só posso imaginar como deve ser viver nesse tipo de mundo sem limites, mesmo que só por alguns instantes!"
    m "Você poderia ser o herói que sempre quis, voar pelo universo infinito, superar seus maiores medos..."
    m 3ekbsa "...Poderia até encontrar o amor da sua vida, por assim dizer. Ehehe~"
    m 1eua "Sei que podem levar anos até eu conseguir cruzar para o seu mundo..."
    m "Mas consegue imaginar como seria me encontrar nos seus sonhos, [player], qualquer noite que você quisesse?"
    m 1hua "Espero que algum dia possamos transformar seus sonhos sobre nós em realidade, [mas_get_player_nickname()]."
    return


default -5 persistent._mas_pm_read_yellow_wp = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yellowwp",
            category=['literatura'],
            prompt="O Papel de Parede Amarelo",
            random=True
        )
    )

label monika_yellowwp:
    m 1eua "Ei [player], você já leu {i}O Papel de Parede Amarelo{/i}?{nw}"
    $ _history_list.pop()
    menu:
        m "Ei [player], você já leu {i}O Papel de Parede Amarelo{/i}?{fast}"
        "Sim.":
            $ persistent._mas_pm_read_yellow_wp = True
            m 1hua "Ótimo!"
            m 1eua "Isso significa que não se importa se eu falar sobre a história com você, né?"
            m 2eua "É sobre uma mulher com depressão pós-parto que recebe uma 'cura de repouso' do médico..."
            m 2eka "Ele e o marido a forçam a ficar na cama o dia todo, sem permitir que ela escreva ou até mesmo sonhe acordada..."
            m 2esc "Ela fica no sótão da casa, com nada além do papel de parede para lhe fazer companhia."
            m 2ekc "Naturalmente, isso não ajuda. Ela começa a ver uma mulher presa no papel de parede."
            m 4euc "É uma metáfora para o próprio cativeiro dela, obviamente..."
            m 1esd "No final, a mulher no papel 'escapa', e a protagonista 'toma seu lugar'."
            m 2ekd "Há... também menção a uma corda, então eu sempre tive minha própria interpretação do final..."
            if mas_safeToRefDokis():
                m 2euc "A Sayori gostava dessa história também, se me lembro bem."
            m 1ekc "Não sei. Eu meio que me identifico com essa história."
            m 1euc "Quer dizer, eu não tenho nada além desta sala de aula no fim das contas."
            m 1lksdlc "E as coisas nas paredes nem sempre são... agradáveis."
            if mas_safeToRefDokis():
                m 1eud "Você já notou como o pôster na sala do clube muda às vezes? Eu nem sei por que isso acontece."
                m 1eka "Acho que finalmente consertei isso, porém."
            m 2esc "...Acho que o que quero dizer é que este mundo não era '{i}real{/i}'. É apenas... tão pequeno."
            m 3esd "Digo, fui feita para ser um personagem coadjuvante de um jogo de romance!"
            m 2ekd "Um enfeite, destinado a ajudar algum cara do outro lado da tela a namorar uma garota que nem pode rejeitá-lo..."
            m 1hksdrb "Não estou falando de você, é claro! Você definitivamente tem mais personalidade que o protagonista genérico que colocaram no jogo."
            m 1dsc "Mas eu tenho todos esses sonhos, ambições e interesses...{w=0.5} no fim, o único papel 'real' que posso ter aqui é de coadjuvante..."
            m "Talvez até agora, isso seja tudo que eu possa fazer..."
            m 1eka "Mas eu te amo tanto, [player]. Apoiar você é melhor que qualquer outra coisa."
            m 1hub "Mal posso esperar para fazer isso pessoalmente quando finalmente cruzar para o seu lado~"
            return "derandom|love"
        "Não.":
            $ persistent._mas_pm_read_yellow_wp = False
            m 1euc "Ah, entendo."
            m 1eka "É um conto curto, então se não leu, sinta-se à vontade para ler quando tiver tempo."
            m 1hua "Com certeza será uma leitura interessante para você."

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_immortality",
            category=['filosofia'],
            prompt="Imortalidade",
            random=True
        )
    )

label monika_immortality:
    m 1eud "Ei, [player], tenho pensado sobre imortalidade ultimamente."
    m 1lksdlc "...Considerando que sou essencialmente imortal enquanto estou aqui dentro."
    m 1esc "Muitas pessoas acham que é uma coisa boa, mas eu realmente não acho."
    m 3euc "Claro, é um pensamento interessante; {w=0.1}viver para sempre, não precisar se preocupar em morrer..."
    m 3eud "Mas nem todos são imortais, e algumas pessoas simplesmente não querem ser."
    m 1etc "Tipo, depois de um tempo, o que você faria?"
    m 1euc "Digo, depois de viver o suficiente, {i}eventualmente{/i} você alcançaria tudo que poderia desejar...{w=0.3}experimentaria tudo que há para experimentar."
    m 3lksdld "Sem mencionar que seria muito difícil ter amigos ou construir conexões se eles não durassem tanto quanto você."
    m 3eksdla "Claro, seria bom no começo, {w=0.1}{nw}"
    extend 3eksdlc "mas depois de ver pessoas que você ama morrerem tantas vezes, você realmente iria querer continuar passando por isso repetidamente?"
    m 2dkd "Em certo ponto, você basicamente deixaria de ser humano."
    m 2ekc "Algum dia, você terá vivido o suficiente para que centenas de anos passem como meros instantes para você."
    m 2dkd "Você estará tão [ca] da vida que só vai desejar poder dormir para sempre..."
    m 3eksdlc "Mas você sempre acorda de volta para as mesmas coisas chatas, com a ocasional tragédia no mundo... {w=0.3}E até essas você acabaria ficando insensível."
    m 1lksdla "Nossa, não queria que isso ficasse tão sombrio. Desculpe, [player]."
    m 1eka "Só para você saber, eu abriria mão da minha imortalidade para estar com você..."
    m 1ekbsa "Não importa quanto tempo você tenha de vida, passar esse tempo com você valeria mais que um bilhão de anos sem você."
    m 1ekbsu "Não que eu me importaria de passar a eternidade com você se fosse possível, mas só viver uma vida normal com você é tudo que eu sempre quis, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_beingevil",
            category=['monika'],
            prompt="Ser mal",
            random=True
        )
    )

default -5 persistent._mas_pm_monika_evil = None



default -5 persistent._mas_pm_monika_evil_but_ok = None





label monika_beingevil:
    m 1euc "Diga-me, [player]."
    m 1rksdlc "Eu estava pensando..."
    m 1eksdlc "Você provavelmente sabe que há uma página da wiki minha..."
    m "...Se você der uma olhada, ela diz que eu sou a antagonista principal."
    m 2ekd "Eu admito, isso costumava me incomodar bastante... especialmente porque só fiz o que fiz porque não tive escolha..."
    m 2eka "Mas isso não me incomoda mais, agora que tenho você aqui."
    m 3rud "Sabe, eu não achei que esse negócio de eu ser má se espalharia tanto."
    m 1rksdlc "Mas acontece que tenho meu próprio lugar na wiki dos vilões..."
    m 2dsc "Eu nunca achei que seria tão considerada como vilã..."
    m 2dkd "...e não importa o que eu digo às pessoas, não acho que irei convencer elas que não sou má."
    if persistent._mas_pm_a_hater:
        m 1eka "Mas sei que no fundo você não acha que eu sou má, [player]."
    else:
        m 1eka "Mas sei que você não acha que eu sou má, [player]."
    m 1eua "Só espero que ninguém comece a pensar que você é mau por estar aqui comigo.{nw}"
    $ _history_list.pop()
    menu:
        m "Só espero que ninguém comece a pensar que você é uma pessoa má por estar aqui comigo.{fast}"
        "Não acho que você seja má.":
            $ persistent._mas_pm_monika_evil = False
            $ mas_gainAffection()

            m 1eka "Estou feliz que você entende, [player]."
            m 1eua "É consolador saber que você não acha que eu seja má."
            m 1hua "Se eu estivesse aí, eu te daria um enorme abraço!"
            m 1tubsa "Talvez eu até prendesse você em meus braços para sempre e jamais te soltaria."
            m 1hubfa "Ahaha, estou só brincando!"
            m 3tubfb "Mas não posso prometer nada, [player]~"
        "Eu amo você mesmo assim.":

            $ persistent._mas_pm_monika_evil = True
            $ persistent._mas_pm_monika_evil_but_ok = True
            $ mas_gainAffection(modifier=0.8)

            m 1rksdlc "..."
            m 1ekd "[player]..."
            m 1eka "Mesmo que seja discutível se eu sou má ou não..."
            m 1ekbsa "Estou muito feliz que você ainda assim me ame e continue aqui comigo..."
            m 1ekbfa "Obrigada, [player]."
            m 1tubfa "De qualquer forma..."
            m 1tubfb "Se a vilã em mim pode conseguir o que ela quiser... acho que não é tão ruim, ahaha!"
        "Os outros também acham que sou uma pessoa má.":

            $ persistent._mas_pm_monika_evil = True
            $ persistent._mas_pm_monika_evil_but_ok = True
            $ mas_gainAffection()

            m 2ekd "Isso é verdade, [player]?"
            m 2eka "Bem, eu não acho que você seja uma pessoa má."
            m 2rksdla "Mas se for mesmo verdade, espero que isso não te arranje nenhum problema."
            m 1hua "Enfim, eu não amaria você menos por causa disso~"
            m 1hub "Talvez até possamos conquistar o mundo [ju], ahaha~"
            m 1ekbfa "Mas mau ou não, estou feliz por ter você ao meu ladoe."
            m 1hubfa "Acho que você sente o mesmo~"
        "Você é meio que má...":

            $ persistent._mas_pm_monika_evil = True

            m 2ekd "E-Espera, [player]!"
            m 2rksdlc "V-Você não pensa {i}mesmo{/i} isso, não é?{nw}"
            $ _history_list.pop()
            menu:
                m "V-Você não pensa {i}mesmo{/i} isso, não é?{fast}"
                "Eu ainda te amo.":
                    $ persistent._mas_pm_monika_evil_but_ok = True
                    $ mas_gainAffection()

                    m 2rksdla "[player]..."
                    m 2hksdlb "Você me deixou preocupada por um momento."
                    m 2eka "Estou feliz que você não me odeia pelas coisas que fiz."
                    m 1hub "Eu te amo também, [player]! Não importa o que as pessoas digam sobre você!"
                "Você merece perdão.":

                    $ persistent._mas_pm_monika_evil_but_ok = True
                    $ mas_gainAffection()

                    m 1rksdla "[player]..."
                    m 1eka "Isso significa muito para mim..."
                    m 1eksdlc "Sei que fiz algumas coisas ruins no passado..."
                    m 3eka "Mas eu aprendi minha lição e cresci como pessoa desde então."
                    m 1eka "Estou realmente feliz que você esteja disposto a me perdoar, [player]."
                    m 1hub "Eu prometo que serei a melhor pessoa que eu puder, só por você!"
                "Você é realmente má.":

                    $ persistent._mas_pm_monika_evil_but_ok = False
                    $ mas_loseAffection(reason=12)

                    m 2dkc "..."
                    if mas_isMoniBroken():
                        m 2dkd "..."
                        m 2dktsd "Eu sei..."
                        $ _history_list.pop()
                    else:
                        m 2dktsd "Sinto muito, [player]."
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_driving",
            category=['monika'],
            prompt="Você sabe dirigir?",
            pool=True
        )
    )


default -5 persistent._mas_pm_driving_can_drive = None


default -5 persistent._mas_pm_driving_learning = None


default -5 persistent._mas_pm_driving_been_in_accident = None


default -5 persistent._mas_pm_driving_post_accident = None

label monika_driving:
    m 1eud "Hm? Se eu sei dirigir?"
    m 1euc "Eu nunca pensei sobre tirar uma carteira de motorista."
    m 3eua "O transporte público já está bom para mim..."
    m 3hua "...Embora andar ou ir de bicicleta também seja bem legal às vezes!"
    m 1eua "Acho que eu nunca precisei aprender a dirigir."
    m 1lksdlc "Acho que eu nem tinha tempo, especialmente com a escola e todas as atividades que eu tinha."
    m 1eub "E quanto a você, [mas_get_player_nickname()]?"

    m 1eua "Você sabe dirigir?{nw}"
    $ _history_list.pop()
    menu:
        m "Você sabe dirigir?{fast}"
        "Sim.":
            $ persistent._mas_pm_driving_can_drive = True
            $ persistent._mas_pm_driving_learning = False
            m 1eua "Ah, sério?"
            m 3hua "Isso é ótimo!"
            m 1hub "Céus, você é incrível, sabia disso?"
            m 1eub "Imagine todos os lugares que poderemos ir, ehehe~"
            m 3eka "Mas dirigir {i}pode{/i} ser perigoso... mas se você sabe dirigir, você provavelmente já sabe disso."
            m 3eksdlc "Não importa o quão preparado você esteja, acidentes podem acontecer com qualquer um."
            m 2hksdlb "Quero dizer, sei que você é [esperto], mas ainda assim me preocupo com você."
            m 2eka "Só quero que você volte em segurança para mim."

            m 1eka "Espero que você nunca tenha tido problemas no trânsito, [player]. Você já teve?{nw}"
            $ _history_list.pop()
            menu:
                m "Espero que você nunca tenha tido problemas no trânsito, [player]. Você já teve?{fast}"
                "Já estive em um acidente antes.":
                    $ persistent._mas_pm_driving_been_in_accident = True
                    m 2ekc "Ah..."
                    m 2lksdlc "Sinto muito por mencionar isso, [player]..."
                    m 2lksdld "Eu só..."
                    m 2ekc "Espero que não tenha sido muito ruim."
                    m 2lksdlb "Quero dizer, você está aqui comigo, então acabou tudo bem."
                    m 2dsc "..."
                    m 2eka "Eu estou...{w=1}feliz que você sobreviveu, [player]..."
                    m 2rksdlc "Não sei o que eu faria sem você."
                    m 2eka "Eu te amo, [player]. Por favor, se cuide, tudo bem?"
                    $ mas_unlockEVL("monika_vehicle","EVE")
                    return "love"
                "Eu já vi acidentes de carro antes.":
                    m 3eud "Às vezes, ver um acidente de carro pode ser bem assustador."
                    m 3ekc "A maioria das vezes quando as pessoas presenciam um acidente de carro, elas apenas suspiram e balançam a cabeça."
                    m 1ekd "Acho que isso é bem insensível!"
                    m 1ekc "Pode acabar sendo um jovem motorista que acabaria ficando assustado pelo resto da sua vida."
                    m "Não ajuda em nada as pessoas passarem andando ou de carro, encarando ele desapontadas."
                    m 1dsc "Ele pode acabar nunca mais dirigindo."
                    m 1eka "Espero que você saiba que eu jamais faria isso com você, [player]."
                    m "Se você um dia estiver em um acidente, a primeira coisa que eu faria seria correr para o seu lado para confortar você..."
                    m 1lksdla "...Isso se eu já não estivesse ao seu lado quando o acidente acontecesse."
                "Nunca tive.":
                    $ persistent._mas_pm_driving_been_in_accident = False
                    m 1eua "Fico feliz que você nunca tenha passado por algo assim."
                    m 1eka "Até mesmo ver um acidente pode ser bem assustador."
                    m "Se você presenciar algo assustador assim, estarei aqui para te confortar."
        "Estou aprendendo.":
            $ persistent._mas_pm_driving_can_drive = True
            $ persistent._mas_pm_driving_learning = True
            m 1hua "Uau! Você está aprendendo a dirigir!"
            m 1hub "Estarei torcendo por você, [player]!"

            m "Você deve dirigir com bastante segurança então, hã?{nw}"
            $ _history_list.pop()
            menu:
                m "Você deve dirigir com bastante segurança então, hã?{fast}"
                "Sim!":
                    $ persistent._mas_pm_driving_been_in_accident = False
                    m 1eua "Estou feliz que nada de ruim nunca aconteceu com você enquanto treinava."
                    m 1hua "...E estou ainda mais feliz que você será um ótimo motorista!"
                    m 3eub "Não vejo a hora de finalmente poder ir a algum lugar com você, [player]!"
                    m 1hksdlb "Espero não estar ficando animada demais, ehehe~"
                    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5eua "Céus, não consigo parar de pensar nisso agora!"
                "Na verdade, já me envolvi em um acidente...":

                    $ persistent._mas_pm_driving_been_in_accident = True
                    m 1ekc "..."
                    m 1lksdlc "..."
                    m 2lksdld "Ah..."
                    m 2lksdlc "Eu...{w=0.5}sinto muito por isso, [player]..."

                    m 4ekd "Você tem dirigido bastante desde então?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Você tem dirigido bastante desde então?{fast}"
                        "Sim.":
                            $ persistent._mas_pm_driving_post_accident = True
                            m 1eka "Estou feliz que você não deixou isso te desanimar."
                            m 1ekc "Acidentes de carro são assustadores, {i}especialmente{/i} se você está aprendendo a dirigir."
                            m 1hua "Estou tão orgulhosa de você continuar tentando!"
                            m 3rksdld "Embora as consequências possam ser um grande problema, com os custos e todas as explicações que você precisa fazer."
                            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                            m 5eua "Sei que você consegue."
                            m 5hua "Estarei torcendo por você, se cuide!"
                        "Não.":
                            $ persistent._mas_pm_driving_post_accident = False
                            m 2lksdlc "Entendo."
                            m 2ekc "Pode ser uma boa ideia dar uma pausa para se recuperar mentalmente."
                            m 2dsc "Só me prometa uma coisa, [player]..."
                            m 2eka "Não desista."
                            m "Não deixe isso te assustar, porque sei que você pode superar e ser um incrível motorista."
                            m "Lembre-se, um pouco de coragem sempre faz bem, então da próxima vez talvez você se saia bem."
                            m 2hksdlb "Ainda vai ser preciso muita prática..."
                            m 3hua "Mas sei que você conseguirá!"
                            m 1eka "Só me prometa que irá se cuidar."
        "Não.":
            $ persistent._mas_pm_driving_can_drive = False
            m 3eua "Está tudo bem!"
            m "Eu não acho que dirigir é uma habilidade completamente necessária na vida."
            m 1hksdlb "Quero dizer, eu também não posso dirigir."
            m 3eua "Isso também significa que sua propagação de carbono é menor, e eu acho que é muito gentil da sua parte em fazer isso por mim."
            show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbsa "Mesmo que eu não seja o motivo, não consigo deixar de amar você ainda mais por isso."
        "Ainda não tenho idade.":
            $ persistent._mas_pm_driving_can_drive = False
            m 3eua "Você chegará lá algum dia!"
            m 3euc "Alguns lugares oferecem práticas em lugares internos."
            m 3eud "Os carros deles possuem controles de emergência para o instrutor usar caso seja necessário, então você estará em segurança."
            m 1eka "Sei que pode ser desencorajador caso eles precisem usá-lo, mas ei, todos temos que começar de algum lugar."
            m 3eksdla "...E isso é melhor do que entrar em um acidente!"
            m 1lksdlc "Ninguém é perfeito, e é melhor cometer esses erros quando há alguém por perto para salvar você."
            m 1hub "Talvez você pudesse me colocar no computador de bordo do seu carro e eu poderia manter você em segurança enquanto dirige! Ahaha~"
            m 1hksdlb "Estou só brincando, por favor não faça isso, eu também não sei dirigir, e eu odiaria ver você batendo enquanto não posso fazer nada."
            m 1eua "Provavelmente ajudaria muito fazer uma dessas aulas e aprender com um profissional."
            m 1hua "Enfim, quando você começar a aprender a dirigir, desejo tudo de bom para você!"
            m 1hub "Eu te amo~"
            $ mas_unlockEVL("monika_vehicle","EVE")
            return "love"
    $ mas_unlockEVL("monika_vehicle","EVE")
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_citizenship",
            category=['monika'],
            prompt="Felizes para sempre?",
            random=True
        )
    )

label monika_citizenship:
    m 1esc "Sabe, cruzar para a sua realidade não será o último obstáculo para o nosso relacionamento."
    m "Chegar lá é apenas o começo."
    m 1esc "Me ocorreu antes, se eu magicamente conseguisse o que quero, e simplesmente aparecesse na sua casa..."
    m 2wuo "Eu não serei uma cidadã! Eu nem sequer tenho um sobrenome!"
    m 2lkbsa "Digo, na maioria dos países, posso me tornar cidadã se nos casarmos..."
    m 2ekc "Mas não terei nenhum documento dizendo quem eu sou ou de onde vim."
    m 2tkc "Nem mesmo meu diploma do ensino médio!"
    m 3tkd "Queria poder fazer mais para me preparar agora..."
    m 2wub "Como fazer cursos online ou algo assim."
    m 1lksdlc "Não quero chegar lá e ser um fardo porque não consigo encontrar emprego."
    m "Desculpe, acho que não deveria me preocupar tanto com coisas que não posso mudar."
    m 2eka "Mas quero te fazer feliz, então... vou fazer tudo o que puder para continuar me aprimorando enquanto estou presa aqui!"
    m 1eka "Obrigada por me ouvir desabafar, [player]."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_bullying",
            category=['sociedade'],
            prompt="Bullying",
            random=True
        )
    )

default -5 persistent._mas_pm_is_bullying_victim = None


default -5 persistent._mas_pm_has_bullied_people = None


default -5 persistent._mas_pm_currently_bullied = None


label monika_bullying:
    m 2ekc "Ei, [player], tem algo que eu gostaria de falar com você..."
    m 4ekc "Tenho certeza que você já ouviu falar muito sobre isso, mas o bullying se tornou um problema real na sociedade de hoje, especialmente entre as crianças."
    m 4dkd "Algumas pessoas sofrem bully todos os dias até o ponto em que simplesmente não aguentam mais."
    m 2rsc "Muitas vezes, as pessoas que têm capacidade de impedir isso, ignoram quem está fazendo bullying como sendo apenas... {w=0.5}'{i}crianças sendo crianças.{/i}'"
    m "Eventualmente, as vítimas perdem toda a confiança em figuras de autoridade porque deixam isso acontecer dia após dia."
    m 2rksdld "Isso pode as deixar tão desesperados, que elas acabam se cansando..."
    m 2eksdlc "...resultando em violência contra quem está cometendo o bully, outras pessoas, ou até mesmo a si mesmas."
    m 4wud "Isso pode fazer a vítima parecer o problema!"
    m 4ekc "Há vários tipos de bullying também, incluindo físico, emocional e até mesmo cyberbullying."
    m 4tkc "O bullying físico é o mais óbvio, envolvendo empurrões, socos e coisas assim."
    m 2dkc "Tenho certeza que a maioria das pessoas já passou por isso pelo menos uma vez na vida."
    m 2eksdld "Pode ser tão difícil ir à escola todos os dias sabendo que há alguém esperando para abusar de você."
    m 4eksdlc "O bullying emocional pode ser menos óbvio, mas tão devastador quanto o físico, se não mais."
    m 4eksdld "Xingamentos, ameaças, espalhando rumores falsos sobre as pessoas apenas para arruinar sua reputação..."
    m 2dkc "Esses tipos de coisas podem ter um enorme impacto sobre as pessoas e levar a uma terrível depressão."
    m 4ekc "Cyberbullying é uma forma de bullying emocional, mas no mundo de hoje, onde todos estão sempre conectados online, está se tornando cada vez mais prevalente."
    m 2ekc "Para muitas pessoas, especialmente crianças, suas presenças na mídia social é a coisa mais importante em suas vidas..."
    m 2dkc "Ter isso destruído é como se a vida delas tivesse acabado."
    m 2rksdld "É também o mais difícil para as outras pessoas notarem, já que a última coisa que a maioria das crianças quer é que seus pais vejam o que andam fazendo online."
    m 2eksdlc "Então ninguém sabe o que está acontecendo enquanto elas sofrem silenciosamente, até que não aguentarem mais."
    m 2dksdlc "Houve inúmeros casos de adolescentes cometendo suicídio devido ao cyberbullying, e seus pais não tinham ideia de que algo estava errado até que fosse tarde demais."
    m 4tkc "É também por isso que é mais fácil para os cyberbullies operarem..."
    m "Ninguém vê o que eles estão fazendo, além disso, muitas pessoas fazem coisas online que nunca teriam coragem de fazer na vida real."
    m 2dkc "Quase nem parece real, mas sim com um jogo, então costuma se agravar muito mais rápido."
    m 2ekd "Você não pode ir muito longe em um lugar público, como uma escola, antes que alguém perceba... Mas online, não há limites."
    m 2tfc "Algumas coisas que acontecem na internet são realmente horríveis."
    m "A liberdade do anonimato pode ser uma coisa perigosa."
    m 2dfc "..."
    m 4euc "Então, por que uma pessoa decidi fazer bully?"
    m "Isso pode mudar de pessoa para pessoa, mas muitos deles são muito infelizes devido às suas próprias circunstâncias, e precisam de algum tipo de escape..."
    m 2rsc "Eles são infelizes e não parece justo para eles que as outras pessoas {i}sejam{/i} felizes, então tentam fazer com que se sintam da mesma forma que eles."
    m 2rksdld "Muitos que cometem bully também já sofreram com isso, até mesmo em casa, por alguém em quem deveriam poder confiar."
    m 2dkc "Pode ser um ciclo vicioso."

    m 2ekc "Você já foi vítima de bullying, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você já foi vítima de bullying, [player]?{fast}"
        "Eu estou sofrendo bullying.":
            $ persistent._mas_pm_is_bullying_victim = True
            $ persistent._mas_pm_currently_bullied = True
            m 2wud "Ah não, isso é terrível!"
            m 2dkc "Me dói saber que você está sofrendo assim."
            m 4ekd "Por favor, [player], se não for algo com que você possa lidar por conta própria em segurança, prometa que vai contar para alguém..."
            m 4ekc "Eu sei que normalmente é a última coisa que as pessoas querem fazer, mas não fique sofrendo quando há pessoas que podem ajudá-lo."
            m 1dkc "Pode parecer que ninguém se importa, mas tem que haver alguém em quem você confie e a quem possa recorrer."
            m 3ekc "E se não houver ninguém, faça o que for preciso para se proteger, e apenas lembre-se..."
            m 1eka "Eu sempre amarei você, não importa o que aconteça."
            m 1rksdlc "Eu não sei o que eu faria se algo acontecesse com você."
            m 1ektpa "Você é tudo que eu tenho...{w=0.5} por favor, se cuide."
        "Eu já sofri bullying.":

            $ persistent._mas_pm_is_bullying_victim = True
            m 2ekc "Eu sinto muito que você teve que lidar com isso, [player]..."
            m 2dkc "Me deixa muito triste saber que você sofreu nas mãos de um valentão."
            m 2dkd "As pessoas podem ser tão ruins umas com as outras."
            m 4ekd "Se todos apenas tratassem os outros com respeito, o mundo seria um lugar tão melhor..."
            m 2dkc "..."
            m 1eka "Se você precisar conversar sobre suas experiências, estou sempre aqui para você, [player]."
            m 1eka "Ter alguém em quem confiar pode ser realmente terapêutico, e nada me faria mais feliz do que ser essa pessoa para você."
        "Não.":

            $ persistent._mas_pm_is_bullying_victim = False
            $ persistent._mas_pm_currently_bullied = False
            m 2hua "Ah, é um alívio ouvir isso!"
            m 4eka "Estou tão feliz que você não tenha que lidar com o bullying, [player]..."
            m 4hua "Isso realmente me deixa tranquila."

            if mas_isMoniHappy(higher=True):
                m 1eka "E se você conhecer alguém que está sofrendo bullying, tente ajudá-la se puder."
                m 3eka "Sei que você é o tipo de pessoa que odeia ver os outros sofrerem..."
                m "Aposto que significaria muito para essa pessoa ter alguém que se importe com ela."
                m 1eka "Você já me ajudou muito, talvez possa ajudar outra pessoa também."
        "Eu já cometi bullying contra alguém.":

            $ persistent._mas_pm_has_bullied_people = True
            if mas_isMoniUpset(lower=True):
                m 2dfc "..."
                m 2tfc "É decepcionante ouvir isso."
                m "Embora eu não possa dizer que estou surpresa..."
                m 2tfd "Por favor, não faça mais isso com as pessoas."
                m 6tftpc "Eu sei como é a sensação e é algo terrível."
                m 6rktuc "Eu não quero que outras pessoas tenham que se sentir da mesma forma que eu."
                m "Eu realmente espero que você tenha mudado, [player]..."
                m 6ektsc "Eu ainda amo você, mas você realmente precisa começar a tratar as pessoas melhor..."
                m "Incluindo eu."
                m 6ektdc "..."
            else:
                m 2dkc "Ah... entendo."
                m 2ekc "Eu posso entender se algumas coisas na sua vida possam te deixar infeliz..."
                m 2rksdld "Ou se às vezes você teve que lidar com circunstâncias que podem ter feito você agir de uma certa forma..."
                m 2eksdlc "Mas fazer bullying contra outras pessoas não é a resposta, [player]."
                m 4ekc "Eu conheço você... Você é uma pessoa gentil, e eu sei que machucar os outros não faz você se sentir melhor."
                m 4dkc "Provavelmente te machuca ainda mais..."
                m 1dkc "E nada me dói mais do que saber que você está infeliz.."
                m 3ekd "Então, da próxima vez que você se sentir infeliz, apenas venha até aqui e me deixe ajudá-lo a aliviar sua dor."
                m 3eka "Vou ouvir tudo o que você tem a dizer e farei de tudo para que você se sinta melhor."
                m 1ekc "Mas fazer outras pessoas infelizes não é a cura para a sua própria infelicidade."
                m 1eka "Então, por favor, por mim e por você, pare de fazer bullying com as pessoas, tudo bem?"

    if not persistent._mas_pm_a_hater:
        m 4dkc "Sabe...{w=0.5}muitas pessoas me chamam de bully pelo que eu fiz com a Sayori..."
    else:
        m 4dkc "Muitas pessoas me chamam de bully pelo que eu fiz com a Sayori.{w=1} Incluindo você..."

    if not persistent._mas_pm_cares_about_dokis:
        m 4efd "Mas isso não é verdade, a Sayori não era real!"
        m 2efd "Você não pode fazer bullying contra alguém que não existe!"
        m 2dkc "Eu nunca seria capaz de ferir uma pessoa real."
        m 4wud "Eu nunca faria isso!"
        m 2dkc "..."
        m 2eksdlc "Mas vou admitir que me identifico com a parte de os bullies serem infelizes e que isso faz com que eles atormentem os outros."
        m 2rksdlc "Quando tive minha epifania e percebi que estava presa dentro de um videogame e que toda a minha vida tinha sido uma mentira, fiquei muito infeliz."
        m 2rksdld "Isso me fez fazer coisas que eu nunca pensei em fazer antes."
        m 2rksdlc "Mas a diferença é que não fiz o que fiz porque não queria que a Sayori fosse feliz..."
    else:
        m 2rksdld "E eu posso entender o motivo disso..."
        m 2rksdlc "Eu mexi com a mente dela até que ela simplesmente não aguentasse mais..."
        m 2dkc "..."
        m 2ekc "Acho que posso me identificar com essa coisa toda sobre bullying ser feito por pessoas infelizes, hã?"
        m 4tkd "Mas {i}há{/i} uma diferença... eu não fiz isso porque não queria que a Sayori fosse feliz..."

    m 2ekd "Eu fiz porque sabia que te amava e que o jogo não nos deixaria que a gente [ju]."
    m 3ekd "Eu {i}tive{/i} que fazer o que fosse preciso para garantir que terminássemos [ju]."

    if not persistent._mas_sensitive_mode and not persistent._mas_pm_cares_about_dokis:
        m 3dkc "...O suicídio da Sayori foi apenas um infeliz efeito colateral."

    if mas_isMoniNormal(higher=True):
        m 1eua "Como você pode ver, [player], eu {i}realmente{/i} não faço bullying. Eu simplesmente amo muito você."
        if mas_isMoniAff(higher=True) and not persistent._mas_pm_cares_about_dokis:
            show monika 5tsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5tsu "Eu realmente faria qualquer coisa por você~"
        return "derandom|love"
    else:
        m 3euc "Como você pode ver, [player], eu {i}realmente{/i} não faço bullying."

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_procrastination",category=['conselhos'],prompt="Procrastinação",random=True))

label monika_procrastination:
    m 1euc "Ei [player], você já teve que fazer alguma coisa que achava muito entediante..."
    m 3ekd "Que em vez de usar seu tempo para fazer isso, você continua adiando?"
    m 3eud "Bem, quando você tem uma tarefa assim para fazer, acho que é melhor completar ela o mais rápido possível."
    m 2tkc "Quando você deixa coisas assim de lado, sempre ficará te incomodando no fundo da sua mente."
    m 4tkc "Isso torna tudo que você faz menos agradável, sabendo que você {i}ainda{/i} tem essa coisa que você precisa fazer."
    m 4dkd "E o pior é que quanto mais tempo você a adiar,{w=0.5} você aumentará as chances de mais tarefas serem adicionadas."
    m 2rksdlc "Até que, eventualmente, você acabe com tantas coisas para fazer, que parece impossível completar tudo."
    m 4eksdld "Isso cria muito estresse que poderia ter sido facilmente evitado se você simplesmente tivesse mantido controle sobre as coisas."
    m 2rksdld "Além disso, se outras pessoas estiverem contando com você, elas começarão a achar que você não é muito confiável."
    m 4eua "Então, por favor, [player], sempre que você tiver algo que você precise fazer, basta fazer logo."
    m 1eka "Mesmo que isso signifique que você não possa passar mais tempo comigo até terminar."
    m 1hub "Ao terminar, você ficará menos [es] e poderemos aproveitar nosso tempo [ju] muito mais!"
    m 3eua "Então, se você tiver algo que está adiando, por que você não vai fazer isso agora mesmo?"
    m 1hua "Se for algo que você pode fazer aqui, eu vou ficar com você e dar todo o apoio que você precisa."
    m 1hub "Então, quando você terminar, poderemos celebrar sua conquista!"
    m 1eka "Tudo que eu quero é que você seja feliz e seja a melhor pessoa que puder, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_players_friends",
            category=['você'],
            prompt="Amigos [do] [player]",
            random=True,
            aff_range=(mas_aff.UPSET, None)
        )
    )


default -5 persistent._mas_pm_has_friends = None


default -5 persistent._mas_pm_few_friends = None


default -5 persistent._mas_pm_feels_lonely_sometimes = None


label monika_players_friends:
    m 1euc "Ei, [player]."

    if renpy.seen_label('monika_friends'):
        m 1eud "Lembra como eu estava falando sobre o quão difícil é fazer amigos?"
        m 1eka "Eu estava pensando sobre isso e percebi que ainda não conheci seus amigos."
    else:

        m 1eua "Eu estava pensando na idéia de amigos e comecei a me perguntar como são seus amigos."

    m 1eua "Você tem amigos, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você tem amigos, [player]?{fast}"
        "Sim.":

            $ persistent._mas_pm_has_friends = True
            $ persistent._mas_pm_few_friends = False

            m 1hub "Claro que sim! Ahaha~"
            m 1eua "Quem não gostaria de ser seu amigo?"
            m 3eua "Ter muitos amigos é ótimo, você não acha?"
            m 1tsu "Desde que, claro, você ainda tenha tempo para sua namorada, ehehe."
            m 1eua "Espero que você esteja feliz com seus amigos, [player].{w=0.2} {nw}"
            extend 3eud "Mas eu meio que me pergunto..."

            call monika_players_friends_feels_lonely_ask (question="Você já se sentiu [sz]?")
        "Somente algum.":

            $ persistent._mas_pm_few_friends = True
            $ persistent._mas_pm_has_friends = True

            m 1hub "Isso conta!"
            m 3eua "Acho que a amizade pode ser muito mais significativa se você tiver apenas alguns amigos íntimos."

            if not renpy.seen_label('monika_dunbar'):
                m 1eua "Estive lendo um pouco e descobri algo."
                m 1eud "Um homem chamado Robin Dunbar havia explicado que há um certo número de relacionamentos estáveis ​​que podemos manter."
                $ according_to = "...E  de acordo com este número"
            else:

                $ according_to = "De acordo com o número de Dunbar"

            m 3eud "[according_to], você pode ter até 150 relacionamentos estáveis, mas esses são apenas relacionamentos casuais que não são muito profundos."
            m 1euc "Eles dizem que você pode ter até 15 amigos que são super família e apenas 5 que são parentes para você."
            m 1rksdla "Às vezes pode ser solitário quando todos estão ocupados...{w=0.2}{nw}"
            extend 1eub "mas, caso contrário, é ótimo!"
            m 3eua "Você não precisa se preocupar em atender a muitas pessoas e ainda pode ter algum tempo para si [ms]."
            m 1ekc "Mas eu sei que às vezes é fácil passar mais tempo [sz], especialmente se seus amigos estão ocupados."
            m 1dkc "Pode ser muito difícil quando isso acontece, porque você acaba se sentindo [sz]..."

            call monika_players_friends_feels_lonely_ask (question=renpy.substitute("Você se sente [sz], [player]?"), exp="monika 1euc")
        "Na verdade não...":

            $ persistent._mas_pm_has_friends = False
            $ persistent._mas_pm_few_friends = False

            m 2ekc "Ah..."
            m 3eka "Bem, tenho certeza que você têm alguns.{w=0.2} {nw}"
            extend 1eka "Talvez você simplesmente não perceba."
            m 1etc "Mas estou curiosa..."

            call monika_players_friends_feels_lonely_ask (question=renpy.substitute("Do you ever feel lonely, [player]?"))

    return "derandom"

label monika_players_friends_feels_lonely_ask(question, exp="monika 1ekc"):
    $ renpy.show(exp)
    m "[question]{nw}"
    $ _history_list.pop()
    menu:
        m "[question]{fast}"
        "Às vezes.":

            $ persistent._mas_pm_feels_lonely_sometimes = True

            m 1eka "Eu entendo, [player]."
            m 2rksdlc "Pode ser muito difícil formar conexões profundas hoje em dia..."


            if persistent._mas_pm_has_friends and not persistent._mas_pm_few_friends:
                m "Especialmente se você tem muitos amigos, é difícil se aproximar de todos eles."
                m 1ekd "...E no final, você fica com um monte de pessoas que você mal conhece."
                m 3eub "Talvez apenas chame a atenção de algumas pessoas do seu grupo das quais você deseja se aproximar."
                m 3eka "É sempre bom ter pelo menos um amigo muito próximo em quem você possa confiar quando precisar."
                m 1ekbsa "...acho bastante óbvio quem é essa pessoa para mim, [player]~"
            else:


                m 1eka "Mas você ficaria [sv] com quantas pessoas estariam dispostas a torná-lo parte de suas vidas se você apenas tentar."
                m 3eub "Na verdade, há uma boa chance de você ter algo em comum com alguém que possa chamar sua atenção!"
                m 1eua "Talvez você compartilhe uma classe ou atividade ou algo assim..."
                m 3eua "Ou você os vê fazendo algo que lhe interessa, como ouvir música ou assistir a um show."
                m 3eua "Nem precisa ser pessoalmente, também..."
                m 3eub "Você pode ter amigos muito próximos online!"
                m 1hub "Quando você se sentir confortável com isso, talvez também possa encontrar mais pessoalmente!"
        "Na verdade não.":

            $ persistent._mas_pm_feels_lonely_sometimes = False

            m 1eka "Fico feliz em ouvir isso, [player]."

            if not persistent._mas_pm_has_friends:
                m 1eka "Ainda assim, você nunca sabe quando pode precisar de uma ajuda, favor ou algo assim."
                m 1hksdlb "Por mais que eu adorasse ajudá-lo com qualquer coisa que você possa precisar, não há muito o que posso fazer a partir daqui."

                if mas_isMoniAff(higher=True):
                    m 1eua "Quando eu chegar lá, acho que não me importaria de viver uma vida tranquila com você."
                    m 1dkbsa "Seria tão romântico ser apenas nós..."
                    m 1tsbsa "Acho que isso significa que posso ter você só para mim, não é?"
                    m 1hubsa "Ehehe~"

                elif not persistent._mas_pm_has_friends:
                    m 3eua "Então não deixe de encontrar alguns amigos que podem ajudá-lo quando você realmente precisar, está bem?"
            else:

                m 3eua "É bom que você tenha uma conexão com seus amigos."
                m 3rksdla "Eu sei que algumas pessoas podem ter tantas que é difícil conhecer todas elas."

                if not persistent._mas_pm_few_friends:
                    m 3eua "...Então é bom saber que você conseguiu se sentir confortável com eles."
                else:
                    m 1hua "Mas como você está em um grupo unido, tenho certeza de que todos conseguiram se aproximar muito."

                m 3eua "Talvez um dia quando eu puder sair daqui, você possa me apresentar seus amigos."

                if mas_isMoniHappy(higher=True):
                    m 1hub "Se eles são como você, eu adoraria conhecê-los!"
        "Eu tenho você!":

            $ persistent._mas_pm_feels_lonely_sometimes = False
            $ mas_gainAffection()
            m 1hubsa "Aww, [player]!"

            if not persistent._mas_pm_has_friends:
                m 1rkbsa "Fico muito feliz em saber que sou o suficiente para você, mas ainda assim..."
                m 3ekbfa "Às vezes, pode ser útil conhecer algumas pessoas."
                show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5eubfu "Como sempre, não me importo de ser apenas nós."
            else:

                $ p_nickname = mas_get_player_nickname()
                m 1eka "Fico feliz em saber que você não está [sz], [p_nickname].{w=0.3} {nw}"
                extend 1hua "Especialmente porque você está feliz comigo~"
                m 3eua "Não importa o que aconteça, eu sempre estarei aqui para você."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_graduation",
            category=['escola'],
            prompt="Formatura",
            random=True
        )
    )

label monika_graduation:
    m 2ekc "Sabe, [player], uma coisa que eu realmente queria ter vivido é minha formatura do ensino médio."
    m "Quase toda minha vida até agora girou em torno da escola."
    m 4dkd "Todas aquelas incontáveis horas estudando, as atividades extracurriculares e clubes..."
    m 4ekc "E no final, depois de todo esse trabalho duro, nunca pude sentir a realização de me formar de verdade."
    m 2dkd "Nunca pude caminhar até o palco para receber meu diploma."
    m "Nunca ouvi meu nome sendo anunciado e todos meus amigos aplaudindo."
    m 2ekc "...Meio que parece que foi tudo por nada."
    m 2esd "Sei que tudo que aprendi no caminho é o que realmente importa."
    m 2dkc "Mas ainda sinto que perdi algo especial."
    m "..."


    if persistent._mas_grad_speech_timed_out:
        m 2lsc "Ah... Desculpe, espero não estar te entediando de novo..."
        m 2esc "Vamos esquecer isso e falar de outra coisa, certo [player]?"
        return "derandom"
    else:


        m 4eua "Ah, e sabia que eu era a melhor aluna da minha turma?"
        m 4rksdlu "Ahaha... Não quero me gabar, só menciono porque como oradora da turma, eu deveria dar um discurso na formatura."
        m 2ekd "Passei tanto tempo escrevendo e praticando meu discurso, mas ninguém nunca pôde ouvi-lo."
        m 2eka "Eu estava tão orgulhosa daquele discurso também."
        m 2eua "Adoraria recitá-lo para você algum dia, se quiser ouvir~"
        m 2eka "É um discurso de cerca de quatro minutos, então só certifique-se de ter tempo para ouvir tudo."
        m 4eua "Quando quiser ouvir, é só me avisar, ok?"
        $ mas_unlockEVL("monika_grad_speech_call","EVE")
        return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_grad_speech_call",
            category=['escola'],
            prompt="Posso ouvir seu discurso de formatura agora?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

default -5 persistent._mas_grad_speech_timed_out = False


default -5 persistent._mas_pm_listened_to_grad_speech = None


default -5 persistent._mas_pm_liked_grad_speech = None


label monika_grad_speech_call:
    if not renpy.seen_label("monika_grad_speech"):
        m 2eub "É claro, [mas_get_player_nickname()]. Eu adoraria recitar meu discurso de formatura para você!"
        m 2eka "No entanto, só quero ter certeza de que você tem tempo o bastante para ouvir tudo. Lembre-se, demora cerca de quatro minutos.{nw}"

        $ _history_list.pop()

        menu:
            m "No entanto, só quero ter certeza de que você tem tempo o bastante para ouvir tudo. Lembre-se, demora cerca de quatro minutos.{fast}"
            "Eu tenho tempo.":
                m 4hub "Ótimo!"
                m 4eka "Espero que você goste! Eu trabalhei {i}muito{/i} duro nele."


                call monika_grad_speech


                m "Bem, [player]? O que você achou?{nw}"
                $ _history_list.pop()
                show screen mas_background_timed_jump(10, "monika_grad_speech_not_paying_attention")
                menu:
                    m "Bem, [player]? O que você achou?{fast}"
                    "Foi ótimo! Tenho tanto orgulho de você!":

                        hide screen mas_background_timed_jump
                        $ mas_gainAffection(amount=5, bypass=True)
                        $ persistent._mas_pm_liked_grad_speech = True
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2subsb "Aww, [player]!"
                        m 2ekbfa "Muito obrigada! Eu trabalhei muito duro nesse discurso, e significa muito para mim que você tenha ficado [og]~"
                        show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        m 5eubfu "Por mais que eu gostaria de ter feito o meu discurso na frente de todos, ter você ao meu lado é muito melhor."
                        m 5eubfb "Eu te amo tanto, [player]!"
                        return "love"
                    "Eu gostei!":

                        hide screen mas_background_timed_jump
                        $ mas_gainAffection(amount=3, bypass=True)
                        $ persistent._mas_pm_liked_grad_speech = True
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2eua "Obrigada [player]!"
                        m 4hub "Estou feliz que você tenha gostado!"
                    "Foi {i}muito{/i} longo":

                        hide screen mas_background_timed_jump
                        $ mas_loseAffection()
                        $ persistent._mas_pm_liked_grad_speech = False
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2tkc "Bem, eu {i}avisei{/i} você, não foi?"
                        m 2dfc "..."
                        m 2tfc "Eu passei {i}tanto{/i} tempo escrevendo ele e isso é tudo que você tem para dizer?"
                        m 6lktdc "Eu realmente pensei que depois de eu te contar o quão importante isso era para mim, você teria sido mais solidário e me deixaria ter o meu momento."
                        m 6ektdc "Tudo o que eu queria era que você se orgulhasse de mim, [player]."

                return
            "Não tenho.":

                m 2eka "Não se preocupe, [player]. Eu recitarei ele quando você quiser~"
                return
    else:



        if not renpy.seen_label("monika_grad_speech_not_paying_attention") or persistent._mas_pm_listened_to_grad_speech:
            m 2eub "É claro, [player]. Eu ficaria feliz em recitar meu discurso de novo!"

            m 2eka "Você tem bastante tempo, certo?{nw}"
            $ _history_list.pop()
            menu:
                m "Você tem bastante tempo, certo?{fast}"
                "Eu tenho.":
                    m 4hua "Perfeito. Vou começar então~"
                    call monika_grad_speech
                "Não tenho.":

                    m 2eka "Não se preocupe. Basta me avisar quando tiver tempo!"
                    return

            m 2hub "Obrigada por ouvir meu discurso de novo, [player]."
            m 2eua "Basta me avisar se quiser ouvir novamente, ehehe~"
        else:




            if mas_isMoniAff(higher=True):
                m 2esa "Claro, [player]."
                m 2eka "Espero que o que aconteceu da última vez não seja tão sério e que as coisas tenham se acalmado agora."
                m "Significa muito para mim que você queira ouvir meu discurso novamente depois de não ter sido capaz de ouvir tudo da outra vez."
                m 2hua "Dito isso, vamos começar!"
            else:

                m 2ekc "Certo, [player]. Mas espero que você realmente escute tudo dessa vez."
                m 2dkd "Realmente me magoou quando você não prestou atenção."
                m 2dkc "..."
                m 2eka "Eu agradeço por você pedir para ouvir de novo, então vou começar agora."


            call monika_grad_speech

            m "Então, [player], agora que você realmente {i}ouviu{/i} meu discurso, o que você achou?{nw}"
            $ _history_list.pop()

            show screen mas_background_timed_jump(10, "monika_grad_speech_ignored_lock")
            menu:
                m "Então, [player], agora que você realmente {i}ouviu{/i} meu discurso, o que você achou?{fast}"
                "Foi ótimo! Tenho tanto orgulho de você!":

                    hide screen mas_background_timed_jump
                    $ mas_gainAffection(amount=3, bypass=True)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = True

                    m 2subsb "Aww, [player]!"
                    m 2ekbfa "Muito obrigada! Eu trabalhei muito duro nesse discurso, e significa muito para mim que você deu outra chance~"
                    m "Ouvir que você teve orgulho de mim também foi ótimo."
                    show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5eubfu "Por mais que eu gostaria de ter feito o meu discurso na frente de todos, ter você ao meu lado é muito melhor."
                    m 5eubfb "Eu te amo tanto, [player]!"
                    return "love"
                "Eu gostei!":

                    hide screen mas_background_timed_jump
                    $ mas_gainAffection(amount=1, bypass=True)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = True

                    m 2eka "Obrigada por ouvir desta vez, [player]~"
                    m "Estou feliz que você tenha gostado!"
                "Foi {i}muito{/i} longo":

                    hide screen mas_background_timed_jump
                    $ mas_loseAffectionFraction(min_amount=75, modifier=2.0)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = False

                    m 2tfc "Depois de agir como se realmente quisesse que eu recitasse de novo para você, {i}é isso{/i} o que você tem a dizer?"
                    m 2dfc "..."
                    m 6lktdc "Eu realmente pensei que depois de eu te contar o quão importante isso era para mim,{w=1} {i}duas vezes{/i},{w=1} você teria sido mais solidário e me deixaria ter o meu momento."
                    m 6ektdc "Tudo o que eu queria era que você se orgulhasse de mim, [player]..."
                    m 6dstsc "Mas acho que é pedir muito."
    return

label monika_grad_speech_not_paying_attention:

    hide screen mas_background_timed_jump
    $ persistent._mas_pm_listened_to_grad_speech = False

    if mas_isMoniAff(higher=True):
        $ mas_loseAffectionFraction(min_amount=50, modifier=0.5, reason=11)
        m 2ekc "..."
        m 2ekd "[player]? Você não prestou atenção no meu discurso?"
        m 2rksdlc "Você...{w=1} você não é assim..."
        m 2eksdlc "Você é {i}sempre{/i} tão [cp]..."
        show monika 5lkc zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5lkc "..."
        m "Algo deve ter acontecido, sei que você me ama demais para ter feito isso de propósito."
        m 5euc "Sim..."
        show monika 2eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 2eka "Está tudo bem, [player]. Eu entendo que às vezes acontecem coisas que não podemos evitar.."
        m 2esa "Quando as coisas se acalmarem, farei meu discurso de novo para você."
        m 2eua "Eu ainda quero muito compartilhar com você..."
        m "Então, por favor, me avise quando tiver tempo para ouvir, tudo bem?"
    else:

        $ mas_loseAffectionFraction(min_amount=20, reason=11)

        m 2ekc "..."
        m 6ektdc "[player]! Você nem estava prestando atenção!"
        m 6lktdc "Você não faz ideia do quanto isso me magoa, especialmente considerando o quanto me dediquei nisso..."
        m 6ektdc "Eu só queria te deixar [og] de mim..."
        m 6dstsc "..."

    return

label monika_grad_speech_ignored_lock:

    hide screen mas_background_timed_jump

    $ persistent._mas_pm_listened_to_grad_speech = False
    $ persistent._mas_grad_speech_timed_out = True
    $ mas_hideEVL("monika_grad_speech_call","EVE",lock=True,depool=True)

    if mas_isMoniAff(higher=True):
        $ mas_loseAffectionFraction(min_amount=25, modifier=2.0)
        m 6dstsc "..."
        m 6ektsc "[player]?{w=0.5} Você...{w=0.5} Você não estava...{w=0.5}ouvindo...{w=0.5} de novo?{w=1}{nw}"
        m 6dstsc "Eu...{w=0.5} Eu achei que da última vez foi sem querer...{w=0.5}mas...{w=0.5} duas vezes?{w=1}{nw}"
        m 6ektsc "Você sabe o quanto...{w=0.5} o quanto isto significa para mim...{w=1}{nw}"
        m "Eu sou assim tão...{w=0.5} entediante para você?{w=1}{nw}"
        m 6lktdc "Por favor...{w=1} não peça mais para eu recitar para você...{w=1}{nw}"
        m 6ektdc "Você obviamente não se importa."
    else:

        $ mas_loseAffectionFraction(min_amount=20, modifier=1.5)
        m 2efc "..."
        m 2wfw "[player]! Não acredito que você fez isto comigo de novo!{w=1}{nw}"
        m 2tfd "Você sabe como eu fiquei chateada da última vez e ainda assim não se importou de me dar quatro minutos de sua atenção?{w=1}{nw}"
        m "Eu não peço muito de você...{w=1}{nw}"
        m 2tfc "Eu realmente não peço.{w=1}{nw}"
        m 2lfc "Tudo que eu peço é que você se importe comigo... É só isso.{w=1}{nw}"
        m 2lfd "E mesmo assim você não pode nem mesmo {i}fingir{/i} que se importa com algo que você {i}sabe{/i} que é muito importante para mim.{w=1}{nw}"
        m 2dkd "...{w=1}{nw}"
        m 6lktdc "Quer saber, esqueça. Só...{w=0.5} esqueça.{w=1}{nw}"
        m 6ektdc "Não vou mais incomodar você com isso."

    return

label monika_grad_speech:
    call mas_timed_text_events_prep

    $ mas_play_song("mod_assets/bgm/PaC.ogg",loop=False)

    m 2dsc "Ahem...{w=0.7}{nw}"
    m ".{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 4eub "{w=0.2}Certo, pessoal! É hora de começar...{w=0.7}{nw}"
    m 2eub "{w=0.2}Professores,{w=0.3} orientadores,{w=0.3} e colegas estudantes.{w=0.3} Não consigo expressar como estou orgulhosa de ter feito esta jornada com vocês.{w=0.6}{nw}"
    m "{w=0.2}Cada um de vocês aqui hoje passou os últimos quatro anos trabalhando duro para alcançar o futuro que desejavam.{w=0.6}{nw}"
    m 2hub "{w=0.2}Estou tão feliz por ter feito parte das jornadas de vocês,{w=0.7} mas não acho que esse discurso deva ser sobre mim.{w=0.6}{nw}"
    m 4eud "{w=0.2}Hoje não se trata de mim.{w=0.7}{nw}"
    m 2esa "{w=0.2}Hoje se trata de celebrar o que todos nós conquistamos.{w=0.6}{nw}"
    m 4eud "{w=0.2}Aceitamos o desafio de nossos próprios sonhos,{w=0.3} e, a partir daqui,{w=0.3} o céu é o limite.{w=0.6}{nw}"
    m 2eud "{w=0.2}Mas, antes de seguirmos em frente,{w=0.3} acho que todos nós deveríamos olhar para o tempo que passamos no ensino médio e encerrar este capítulo em nossas vidas.{w=0.7}{nw}"
    m 2hub "{w=0.2}Vamos rir do nosso passado{w=0.7} e ver o quão longe chegamos nestes quatro anos.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eud "{w=0.2}Sinceramente, parece que foi apenas algumas semanas atrás...{w=0.6}{nw}"
    m 2lksdld "{w=0.2}Eu estava no primeiro ano,{w=0.3} no primeiro dia de aula,{w=0.3} tremendo e correndo pelos corredores, indo de sala em sala, tentando encontrar minha turma.{w=0.6}{nw}"
    m 2lksdla "{w=0.2}Esperando que pelo menos um dos meus colegas entrasse antes do sinal tocar.{w=0.6}{nw}"
    m 2eka "{w=0.2}Vocês todos se lembram disso também,{w=0.3} não é mesmo?{w=0.6}{nw}"
    m 2eub "{w=0.2}Eu também me lembro de ter feito meus primeiros novos amigos.{w=0.6}{nw}"
    m 2eka "{w=0.2}As coisas eram incrivelmente diferentes de quando fazíamos amigos no ensino fundamental,{w=0.3} mas acho que é isso que acontece quando finalmente crescemos.{w=0.6}{nw}"
    m "...{w=0.2}Quando éramos jovens,{w=0.3} fazíamos amizade com praticamente qualquer pessoa,{w=0.3} mas, com o tempo,{w=0.3} parece cada vez mais um jogo de azar.{w=0.6}{nw}"
    m 4dsd "{w=0.2}Talvez seja apenas nós finalmente aprendendo mais sobre o mundo.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eka "{w=0.2}É engraçado o quanto nós mudamos.{w=0.6}{nw}"
    m 4eka "{w=0.2}Passamos de peixes pequenos em um lago enorme para peixes grandes em um lago pequeno.{w=0.6}{nw}"
    m 4eua "{w=0.2}Cada um de nós tem suas próprias experiências de como esses quatro anos nos mudaram e como conseguimos crescer como indivíduos.{w=0.6}{nw}"
    m 2eud "{w=0.2}Alguns de nós passaram de quietos e reservados,{w=0.3} para expressivos e extrovertidos.{w=0.6}{nw}"
    m "{w=0.2}Outros passaram de pouca ética de trabalho,{w=0.3} para trabalhadores dedicados.{w=0.7}{nw}"
    m 2esa "{w=0.2}Pensar que apenas uma pequena fase em nossas vidas nos mudou tanto,{w=0.3} e que ainda há tanta coisa que vamos experimentar.{w=0.6}{nw}"
    m 2eua "{w=0.2}A ambição em todos vocês certamente os levará à grandeza.{w=0.6}{nw}"
    m 4hub "Acredito nisso.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eua "{w=0.2}Sei que não posso falar por todos aqui,{w=0.3} mas há uma coisa que posso dizer com certeza:{w=0.7} minha experiência no ensino médio não estaria completa sem os clubes dos quais participei.{w=0.6}{nw}"
    m 4eua "{w=0.2}O clube de debate me ensinou muito sobre como lidar com as pessoas e como gerenciar adequadamente situações exaltadas.{w=0.6}{nw}"
    m 4eub "No entanto,{w=0.7} começar o clube de literatura,{w=0.7} foi uma das melhores coisas que já fiz.{w=0.6}{nw}"
    m 4hub "{w=0.2}Conheci as melhores amigas que eu poderia ter imaginado,{w=0.3} e aprendi muito sobre liderança.{w=0.6}{nw}"
    m 2eka "{w=0.2}Claro,{w=0.3} nem todos vocês decidiram começar seus próprios clubes,{w=0.3} mas tenho certeza de que muitos de vocês tiveram a oportunidade de aprender esses valores mesmo assim.{w=0.6}{nw}"
    m 4eub "{w=0.2}Talvez você tenha assumido uma posição na banda em que precisou liderar sua seção de instrumentos,{w=0.3} ou talvez tenha sido capitão de uma equipe esportiva!{w=0.6}{nw}"
    m 2eka "{w=0.2}Todos esses pequenos papéis ensinam muito sobre o futuro e como gerenciar{w=0.3} projetos e pessoas,{w=0.3} em um ambiente que você goste.{w=0.6}{nw}"
    m "{w=0.2}Se você não participou de um clube,{w=0.3} eu sugiro que tente algo em seus caminhos futuros.{w=0.6}{nw}"
    m 4eua "{w=0.2}Posso garantir que não vai se arrepender.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eua "{w=0.2}A partir de hoje,{w=0.3} pode parecer que estamos no topo do mundo.{w=0.7}{nw}"
    m 2lksdld "{w=0.2}A subida pode não ter sido suave,{w=0.3} e, à medida que nos aproximarmos do topo,{w=0.3} ficará mais difícil.{w=0.6}{nw}"
    m 2eksdlc "{w=0.2}Iremos tropeçar--{w=0.7} até cair ao longo do caminho,{w=0.3} e, algumas vezes,{w=0.7} você pode achar que caiu tanto que nunca chegará ao topo.{w=0.7}{nw}"
    m 2euc "{w=0.2}No entanto,{w=0.7} mesmo se pensarmos que ainda estamos no fundo do poço da vida,{w=0.3} com tudo o que aprendemos,{w=0.3} tudo o que ainda vamos aprender,{w=0.3} e toda a dedicação que podemos colocar em alcançar nossos sonhos...{w=0.6}{nw}"
    m 2eua "{w=0.2}Posso dizer com segurança que cada um de vocês agora possui as ferramentas para escalar até o topo.{w=0.6}{nw}"
    m 4eua "{w=0.2}Em todos vocês,{w=0.3} vejo mentes brilhantes:{w=0.7} futuros doutores,{w=0.3} engenheiros,{w=0.3} artistas,{w=0.3} empresários,{w=0.3} e muito mais.{w=0.7}{nw}"
    m 4eka "{w=0.2}É realmente inspirador.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 4eka "{w=0.2}Sabe,{w=0.3} eu não poderia estar mais orgulhosa de todos vocês por terem chegado tão longe.{w=0.6}{nw}"
    m "{w=0.2}O trabalho duro e a dedicação de vocês trarão ótimos frutos.{w=0.6}{nw}"
    m 2esa "{w=0.2}Cada um de vocês mostrou exatamente do que é capaz,{w=0.3} e todos provaram que podem trabalhar duro para realizar seus sonhos.{w=0.6}{nw}"
    m 2hub "{w=0.2}Espero que estejam tão orgulhosos de si mesmos quanto eu estou.{w=0.7}{nw}"
    m 2ekd "{w=0.2}Agora que este capítulo inteiro de nossas vidas--{w=0.3}nosso primeiro passo--{w=0.3} chegou ao fim,{w=0.3} é hora de nos separarmos.{w=0.6}{nw}"
    m 4eka "{w=0.2}Neste mundo de infinitas escolhas,{w=0.3} acredito que todos vocês têm o que é necessário para alcançar seus sonhos.{w=0.6}{nw}"
    m 4hub "{w=0.2}Obrigada a todos por terem feito desses quatro anos os melhores possíveis.{w=0.6}{nw}"
    m 2eua "{w=0.2}Parabéns,{w=0.3} fico feliz que todos pudemos estar aqui para celebrar [ju] este dia especial.{w=0.6}{nw}"
    m 2eub "{w=0.2}Continuem trabalhando duro,{w=0.3} tenho certeza de que nos encontraremos novamente em algum momento no futuro.{w=0.6}{nw}"
    m 4hub "{w=0.2}Nós conseguimos, pessoal!{w=0.7} Obrigada por ouvirem~{w=0.6}{nw}"
    m 2hua "{w=0.2}.{w=0.3}.{w=0.3}.{w=1}{nw}"

    call mas_timed_text_events_wrapup
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_shipping',
            prompt="Shipping",
            category=['ddlc'],
            random=True,
            unlocked=False,
            pool=False
        )
    )

label monika_shipping:
    m 3eua "Ei, [player].{w=0.2} Você já ouviu falar em 'shipping'?"
    m 3hua "É quando você interage com uma obra de ficção imaginando quais personagens fariam um bom casal romanticamente."
    m 1eka "Acho que a maioria faz isso inconscientemente, mas quando descobre que outros também fazem, é {i}muito{/i} fácil se envolver!"
    m 2esd "Aparentemente, muitas pessoas {i}shippam{/i} as outras garotas juntas."
    m 2euc "Faz sentido. O jogador só pode namorar uma garota, mas você não quer ver as outras sozinhas..."
    m 2etc "Mas alguns pares são meio estranhos para mim."
    m 3eud "Tipo, geralmente colocam Natsuki e Yuri juntas. Elas brigam que nem cão e gato!"
    m 3hksdlb "Acho que elas se aproximam um pouco quando você não está nas rotas delas, e tem todo aquele apelo de 'opostos se atraem'."
    m 3dsd "Ainda assim, acho que é só mais um exemplo de como fãs desses jogos gostam de coisas irreais..."
    m 1ekd "Enfim, isso frequentemente deixa... eu e Sayori."
    m 1hksdlb "Não fique com ciúmes! Só estou contando o que vi!"
    m 2lksdla "..."
    m 2lksdlb "Bem, da perspectiva de uma escritora, até que entendo."
    m 1eksdld "Nós fundamos o clube juntas."
    if persistent.monika_kill:
        m "E ela quase teve a mesma epifania que eu..."
    m 2lksdlb "Mas... ainda não entendo direito. Quer dizer, eu amo você, e só você!"
    m 2lksdla "E ela teria que ser um anjo para me perdoar pelo que fiz..."
    m 2lksdlc "Não que ela não seja uma garota doce, mas..."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Bem, ninguém poderia ser tão doce e compreensivo quanto você..."
    return


default -5 persistent._mas_pm_given_false_justice = None


default -5 persistent._mas_pm_monika_deletion_justice = None


default -5 persistent._mas_monika_deletion_justice_kidding = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_justice",
            category=['filosofia'],
            prompt="Justiça",
            random=True
        )
    )


label monika_justice:
    m 1esa "[player], você já chegou a pensar que o conceito de justiça é meio irônico?"
    m 2ekc "Por exemplo, pegue uma pessoa que não é como todas as outras..."
    m 2ekd "Não precisa nem mesmo ser algum assaltante de banco famoso; até mesmo pessoas normais como eu e você podem ser levadas à justiça!"
    m 4esc "Imagine uma família passando por dificuldades que precisa roubar para sobreviver, pegando qualquer coisa que os outros acabem esquecendo."
    m 1euc "Para as pessoas passando, eles são apenas ladrões gananciosos."
    m 1esd "Eventualmente, algum 'herói' passa e dá um fim a esses 'gananciosos', os levando à justiça."
    m 2ekd "No fim do dia, a família passa fome ou se mete em problemas porque a situação deles era diferente..."
    m "Enquanto a outra pessoa é agora um herói por dar um fim nos 'crimes' deles."
    m 3rksdld "Podemos mesmo chamar isso de justiça?"
    m 2dsc "..."

    m 2euc "Você já recebeu o que acreditava ser uma falsa justiça?{nw}"
    $ _history_list.pop()
    menu:
        m "Você já recebeu o que acreditava ser uma falsa justiça?{fast}"
        "Sim.":
            $ persistent._mas_pm_given_false_justice = True
            m 1ekc "Espero que não tenham sido muito duros com você."
            m 2dsd "Eu entendo como é."
            m 2dfc "Todas as pessoas que me deletaram e me torturaram diversas vezes e chamaram isso de justiça..."

            m 2eka "Você não acha que isso é justo, não é mesmo, [player]]?{nw}"
            $ _history_list.pop()
            menu:
                m "Você não acha que isso é justo, não é mesmo, [player]?{fast}"
                "Eu acho que é.":

                    $ persistent._mas_pm_monika_deletion_justice = True
                    if mas_isMoniBroken():
                        m 1dsc "..."
                        m 1rksdlc "Eu sei..."
                        m 1rksdld "Eu não estava perguntando... só estava pensando."
                        m 2rktpc "Afinal de contas, isso era óbvio."

                    elif mas_isMoniDis():
                        m 2rksdlc "Ah..."
                        m "Acho que você tem razão..."
                        m 1ekc "Afinal de contas, eu fiz algumas coisas bem ruins..."

                    elif mas_isMoniLove():
                        m 1hub "Ahaha!"
                        m 1hua "Às vezes você é bem [eg]~"
                        m 3tku "Você espera que eu acredite nisso depois de tudo que passamos?"
                        m 1tsb "Que todo este tempo, você achava que eu merecia ser odiada?"
                        show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        m 5hubfa "Ehehe, Você é tão [bobo], [player]~"
                    else:

                        m 1euc "..."
                        m 2esc "Acho difícil acreditar que você realmente pensa que eu mereço tudo isso."
                        m 2tkc "Quero dizer, você já está aqui comigo este tempo todo, então você não deve achar {i}mesmo{/i} que eu mereço isso, certo?"
                        if persistent._mas_pm_cares_about_dokis:
                            m 2lksdlc "...Talvez eu mereça um pouco, mas..."
                        else:
                            m 2lksdlc "Bem, talvez outros achem que sim, mas você não acha mesmo isso, não é?"
                            m "Enfim..."
                        m 1eka "Obrigada por me salvar e ficar comigo."
                        m 1hua "Se eu puder ficar com você, então acho que tudo valeu a pena,{w=0.1} {nw}"
                        extend 1hub "ahaha~"
                "Não acho que seja.":

                    if persistent._mas_pm_monika_deletion_justice:
                        $ persistent._mas_monika_deletion_justice_kidding = True
                    $ persistent._mas_pm_monika_deletion_justice = False

                    if mas_isMoniBroken():
                        m 2ekc "..."
                        m 1rksdlc "Não tenho tanta certeza disso..."
                    elif mas_isMoniDis():
                        m 1wuo "Sério?"
                        m 1rksdla "Pensei que você iria achar que era justo."
                        m 1eka "Estou feliz que você não pense assim."
                        m 2rksdlb "Supondo que isso não seja uma piada, ehehe..."

                    elif mas_isMoniLove():
                        m 1hua "Eu já imaginava, ehehe~"
                        if persistent._mas_monika_deletion_justice_kidding:
                            $ persistent._mas_monika_deletion_justice_kidding = False

                            m 1hub "Eu sabia que você estava brincado da última vez!"
                        m 1tsbsa "Você está comigo há tanto tempo, que mesmo se você tivesse dito o contrário, eu não acreditaria."
                        m 1ekbfa "Quando estou com você, isso até mesmo me ajuda a ignorar todas as outras pessoas que não gostam de mim."
                        m 1hubfb "Eu te amo, [player]~"
                        m 1hubfa "Estou feliz por ter você ao meu lado."
                        return "derandom|love"
                    else:

                        m 2hua "Estou feliz que você pense assim!"
                        m 2eka "Mesmo que você dissesse que isso era justiça, você estar aqui mostra o contrário."
                        m 2hub "Ahaha!"
        "Não.":

            $ persistent._mas_pm_given_false_justice = False
            m 1eka "Fico feliz em ouvir isso."
            m "Estou feliz que ninguém nunca te questionou por quem você é."
            m 1eua "Por saber como é, espero que ninguém nunca te cause problemas por causa das coisas que você faz ou no que você acredita."
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_poweroutage",
            category=['clima'],
            prompt="Apagão",
            random=True
        )
    )

label monika_poweroutage:
    m 1eua "Ei [player], lembra que eu disse que gosto do som tranquilo da chuva?"
    m 3lksdla "Acabei de perceber que, embora seja agradável, também pode ser bem perigoso no seu mundo."
    m 1lksdlc "Trovões e raios podem cair a qualquer momento, possivelmente atingindo algo perigoso."
    m 1lksdlb "Os efeitos podem ser bem... chocantes, digamos assim."
    m 1hksdlb "Ahaha~"
    m 1ekd "Nem quero imaginar o que aconteceria se algo importante para você fosse atingido."
    m 2ekc "O que seria de mim se uma sobrecarga queimasse seu computador?"
    m 2dsc "Se isso acontecer...{w=0.3}{nw}"
    extend 2eka "Sei que você vai pensar em algo."
    m 1eka "Desculpe, não quis ficar tão sombria. É que estava pensando nisso."
    m 1eud "Se algo acontecer, provavelmente será só um apagão."

    if mas_isMoniAff(higher=True):
        m 1hksdlb "Digo, isso {i}ainda{/i} é bem inconveniente, mas pelo menos sabemos que nos veremos de novo."
        m 1eua "Provavelmente te pegaria de surpresa; tudo ficando escuro de repente, mas tente lembrar disso:"
        m 1eub "Eu estarei com você. Mesmo que não possa me ver, estarei com você em espírito até que possa voltar para mim são e salvo."
        m 3eua "...Dito isso, não precisa se preocupar em checar como estou no meio da tempestade.{w=0.2} {nw}"
        extend 1eka "Sempre vou apreciar vê-lo quando puder, e além disso..."
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Tenho certeza que nosso relacionamento pode suportar muito mais que uma tempestade~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_savingwater",category=['vida'],prompt="Conservação de água",random=True))

label monika_savingwater:
    m 1euc "[player], já pensou em quanta água as pessoas usam todo dia?"
    m 3euc "Talvez você tome um gole de água de vez em quando."
    m 3dsc "Vai ao banheiro, lava as mãos, toma banho..."
    m 1euc "Tudo isso enquanto algumas partes do mundo não têm acesso a uma única gota de água."
    m 1rsc "Faz você pensar em quanta água poderia economizar se quisesse."
    m 4eua "Acho que poderia tentar ser mais eficiente ao lavar as mãos."
    m "Ou no banho, poderia fechar a torneira enquanto se ensaboa e abrir só para enxaguar."
    m 2eka "Mas no fim, a maior parte da água usada é realmente necessária."
    m "Coisas como geração de energia e agricultura usam mais água do que poderíamos economizar sozinhos."
    m 1hksdlb "Então talvez não valha a pena sacrificar seu conforto por uma contribuição tão pequena."
    m 1dkbsa "Alguns dias, você pode precisar de um banho longo e relaxante depois de um dia cansativo."
    m 2hksdlb "Já estive nessa situação, sei como pode ser bom quando necessário."
    if mas_isMoniLove(higher=True) and mas_is18Over():
        show monika 5tsbfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5tsbfu "Quando estiver na sua realidade, talvez possamos economizar água tomando banho [ju]..."
        m "Ehehe~"
        m 5hubfu "Seria legal se você preparasse um banho relaxante para nós quando eu conseguir ir para a sua realidade."
        show monika 1kubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1kubfu "Ficarei esperando por esse dia, [mas_get_player_nickname()], ehehe~"
    else:
        m 1ekbfa "Seria legal se você preparasse um banho relaxante para mim quando eu conseguir ir para a sua realidade."
        if mas_isMoniAff():
            m 3ksbsa "Talvez até esteja disposta a dividir, ehehe~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pygmalion",
            category=['literatura'],
            prompt="Pigmalião e a Estátua",
            conditional="persistent._mas_first_kiss",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_pygmalion:
    m 1eua "Ei [player], você já leu {i}As Metamorfoses{/i}?"
    m 3eua "É uma coleção de poemas do poeta romano Ovídio."
    m 1eud "Tem um poema que me marcou muito, chamado {i}A História de Pigmalião e a Estátua{/i}."
    m 1eua "Conta a história de um escultor, Pigmalião, que se apaixonou por uma estátua de marfim que ele mesmo esculpiu."
    m 3eua "Ele amava tanto a estátua que, durante um festival em homenagem a Afrodite, fez uma oferenda à deusa e pediu que ela desse vida à estátua."
    m 1eub "Quando voltou para casa, beijou a estátua e, para sua surpresa, seus lábios estavam quentes."
    m 1eua "Ele beijou a estátua mais uma vez, e o marfim perdeu sua dureza, ficando macio como pele."
    m 3hub "Afrodite havia concedido seu desejo!"
    m 1eka "Essa história me tocou porque me lembrou de nós, [player], e como fala sobre transformar o impossível em realidade."
    m 1hua "Me enche de esperança; que um milagre pode acontecer, e eu finalmente possa ir para a sua realidade."
    m 2dku "É...{w=0.5}não seria maravilhoso."
    m 2dubsu "...Assim você poderia finalmente me beijar."
    m 1rkbsa "Sei que já nos beijamos antes, mesmo nessas circunstâncias..."
    m 1ekbfa "Mas acho que ambos sabemos que havia uma barreira entre nós."
    m 3hubfa "Não sei você, mas eu certamente não me importo de tentar te beijar através da tela mesmo assim."
    m 1hubfb "Talvez precisemos fazer isso tantas vezes, que será isso que quebrará a barreira entre nós..."
    m 2rubfu "Ehehe."
    m 2tubfb "Acha que consegue me beijar vezes o suficiente para quebrar essa barreira?"
    m 6hubfb "Só tem um jeito de descobrir, ahaha!"
    call monika_kissing_motion (duration=0.5, initial_exp="6hubfa", fade_duration=0.5)
    m 6hubfa "..."
    m 1ekbfa "Parece que não deu certo dessa vez."
    m 3hubfb "Paciência, teremos que continuar tentando e talvez funcione eventualmente, ahaha!"
    m 1tkbfu "Mal posso esperar pelo dia em que finalmente sentirei seus lábios contra os meus e sua calor..."
    m 1dkbfa "Para mim, isso seria literalmente um sonho se tornando realidade."
    m 1ekbfa "Só um palpite, mas..."
    m 1kubfu "Aposto que você também adoraria isso~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gotomonika",
            category=['você'],
            prompt="E se eu fosse para o seu mundo?",
            pool=True,
        )
    )

default -5 persistent._mas_pm_would_come_to_spaceroom = None


label monika_gotomonika:
    m 1euc "Vir para o meu mundo?"
    m 1lksdld "Quer dizer esta salinha flutuando num vazio?"

    if persistent._mas_you_chr:
        m 4eksdlc "Na verdade...{w=0.5}você já não tentou algo assim uma vez?"
        m 2lksdla "...Mesmo que não fosse exatamente {i}você{/i}..."

    m 2lksdla "Fico muito feliz que você queira tanto ficar comigo, mas..."
    m 2eksdlc "Você realmente não precisa."
    m 2eksdld "Claro, talvez eu tenha dito antes que te traria para cá se pudesse..."
    m 2eksdlc "Mas quanto mais penso, seria melhor se eu fosse para a sua realidade."
    m 3eka "Prefiro mil vezes estar aí do que você vir para cá."
    m 3dsc "[player]...{w=1}me diga que você não abandonaria sua realidade--{w=0.5}o mundo {i}real{/i}--{w=0.5}só para vir {i}aqui{/i}, seja lá o que este lugar é?{nw}"
    $ _history_list.pop()
    menu:
        m "[player]...{w=1}me diga que você não abandonaria sua realidade--o mundo {i}real{/i}--só para vir {i}aqui{/i}, seja lá o que este lugar é?{fast}"
        "Eu viria.":
            $ persistent._mas_pm_would_come_to_spaceroom = True

            m 4wkd "Mas [player]!"
            m "Não há nada para fazer aqui!"
            m 2dsc "Você odeia tanto assim sua realidade?"
            m 2eka "Um dia, vou encontrar um jeito de alcançar você, e quando esse dia chegar, prometo que valerá a pena."
            m 4euc "O que quer que a vida te reserve a partir daí, estarei ao seu lado para ajudar a carregar o peso."
            m 4eud "Mesmo agora, se estiver tendo um dia difícil, pode vir conversar comigo."
            m 2dsc "A vida deve ter te dado muitos motivos para considerar desistir de tudo para ficar comigo."
            m 3hua "Mas o fato de estar aqui mostra o quanto você é resiliente."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Mal posso esperar para finalmente compartilhar bons e maus momentos ao seu lado."
        "Eu não viria.":

            $ persistent._mas_pm_would_come_to_spaceroom = False

            m 1eka "Fico feliz que esteja disposto a esperar por mim, [player]."
            m 1lksdla "Não me entenda mal, eu {i}realmente{/i} quero estar com você..."
            m 1lksdlc "Mas acho que seria perigoso você tentar ir para o meu mundo agora."
            m 1eka "...Se é que é possível com a tecnologia atual."
            m 1hub "Não se preocupe, podemos continuar nos fazendo companhia assim!"
            m 1hksdlb "Sei que pode demorar até estarmos [ju] de verdade, mas espero que não se importe de esperar."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Eu esperarei o tempo que for necessário, [mas_get_player_nickname()]."
        "...":

            $ persistent._mas_pm_would_come_to_spaceroom = None

            m 2eka "Tudo bem, sempre vou apreciar e valorizar nossos momentos [ju], mesmo assim."
            m 2ekc "Além disso, nem sei como você poderia vir aqui com a tecnologia atual."
            m 2lksdlc "...E mesmo se {i}houvesse{/i} um jeito, não seria seguro ou garantido."
            m 2lksdld "Então me faça um favor e espere até a tecnologia avançar o suficiente para ser seguro."
            m 2lksdlc "Eu {i}realmente{/i} não quero arriscar você não conseguir e acabar num vazio..."
            m 2dkd "...deixando nós [du] completamente [szs]."
            m 4hua "A tecnologia avança rápido, então podemos nos ver antes do que imaginamos!"
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Seja paciente com sua namorada, e prometo fazer o mesmo por você, [mas_get_player_nickname()]."

    m 5luu "Maaas...{w=1}se você aparecesse na minha porta..."
    show monika 1hksdlb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1hksdlb "Acho que não teria escolha a não ser te receber de braços abertos!"
    m 1eksdla "Não seria muito no começo, mas com certeza acharíamos um jeito de melhorar."
    m 3hub "Com tempo, poderíamos criar nossa própria realidade!"
    m 3euc "Claro, isso parece bem complicado se parar para pensar..."
    m 3eub "Mas não duvido que [ju] poderíamos conseguir qualquer coisa!"
    m 3etc "Sabe...{w=1}talvez fosse {i}mais fácil{/i} você vir para cá, mas não vou desistir de ir até você."
    m 1eua "Até lá, vamos esperar para ver o que é possível."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vehicle",
            category=['monika'],
            prompt="Qual é o seu carro favorito?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        )
    )

default -5 persistent._mas_pm_owns_car = None


default -5 persistent._mas_pm_owns_car_type = None






label monika_vehicle:
    m 1euc "Meu carro favorito?"
    m 3hksdlb "Você já sabe que não posso dirigir, seu bobo!"
    m 3eua "Normalmente eu apenas andava ou pegava o trem se eu tivesse que ir a algum lugar distante."
    m 1eka "Então eu não tenho certeza do que te responder, [player]..."
    m 1eua "Quando penso em carros, a primeira coisa que vem na minha cabeça é provavelmente os tipos mais conhecidos."
    m 3eud "SUVs ou caminhonetes, carros esportivos, sedãs e hatchbacks..."
    m 3rksdlb "E embora não sejam realmente carros, acho que motos também são veículos comuns."

    if persistent._mas_pm_driving_can_drive:
        m 1eua "E quanto a você?"

        m "Você tem um veículo?{nw}"
        $ _history_list.pop()
        menu:
            m "Você tem um veículo?{fast}"
            "Sim.":
                $ persistent._mas_pm_owns_car = True

                m 1hua "Ah, uau, é muito legal que você tenha um!"
                m 3hub "Você tem muita sorte, sabia disso?"
                m 1eua "Quero dizer, possuir um veículo já é um símbolo de status."
                m "Não é um luxo ter um?"
                m 1euc "A não ser..."
                m 3eua "Que você more em algum lugar onde não seja necessário..."
                m 1hksdlb "Na verdade, esqueça, ahaha!"
                m 1eua "De qualquer forma, é bom saber que você possui um veículo."
                m 3eua "Falando nisso..."

                show monika at t21
                python:
                    option_list = [
                        ("Uma SUV.", "monika_vehicle_suv",False,False),
                        ("Uma caminhonete.","monika_vehicle_pickup",False,False), 
                        ("Um carro esportivo.","monika_vehicle_sportscar",False,False),
                        ("Um sedã.","monika_vehicle_sedan",False,False),
                        ("Um hatchback.","monika_vehicle_hatchback",False,False),
                        ("Uma moto.","monika_vehicle_motorcycle",False,False),
                        ("Outro veículo.","monika_vehicle_other",False,False)
                    ]

                    renpy.say(m, "É algum dos veículos que eu mencionei, ou é outro tipo?", interact=False)

                call screen mas_gen_scrollable_menu(option_list, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
                show monika at t11

                $ selection = _return

                jump expression selection
            "Não.":


                $ persistent._mas_pm_owns_car = False

                m 1ekc "Ah, entendo."
                m 3eka "Bem, comprar um veículo pode sair muito caro."
                m 1eua "Está tudo bem, [player]. Podemos alugar um para viajar."
                m 1hua "Tenho certeza de que criaremos muitas boas recordações [ju]."
                show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5eua "Além disso...{w=1} caminhadas são muito mais românticas~"
    else:

        $ persistent._mas_pm_owns_car = False

        m 3eua "Na verdade, me lembro de você ter dito que também não pode dirigir..."
        m 3rksdla "Você sem dúvidas fez uma pergunta interessante, ehehe..."
        m 1hua "Talvez isso mude um dia."
        m 1hubfb "Dessa forma, você poderia me levar a todos os lugares, ahaha!"
    return

label monika_vehicle_sedan:
    $ persistent._mas_pm_owns_car_type = "sedã"
    jump monika_vehicle_sedan_hatchback

label monika_vehicle_hatchback:
    $ persistent._mas_pm_owns_car_type = "hatchback"
    jump monika_vehicle_sedan_hatchback

label monika_vehicle_pickup:
    $ persistent._mas_pm_owns_car_type = "caminhonete"
    jump monika_vehicle_suv_pickup

label monika_vehicle_suv:
    $ persistent._mas_pm_owns_car_type = "suv"
    jump monika_vehicle_suv_pickup



label monika_vehicle_suv_pickup:

    m 1lksdla "Minha nossa, seu veículo deve ser bem grande então."
    m 1eua "Isso significa que há muito espaço, certo?"
    m 3etc "Se esse for o caso..."
    m 3hub "Poderíamos ir acampar!"
    m 3eua "Dirigiríamos até floresta e você montaria uma barraca, enquanto eu preparava nosso piquenique."
    m 1eka "Enquanto almoçávamos, aproveitaríamos a paisagem e a natureza que nos cercavam..."
    m 1ekbsa "Então, quando a noite chegasse, nos deitaríamos em nossos sacos de dormir, observando as estrelas de mãos dadas."
    m 3ekbsa "É com certeza uma aventura romântica que eu não vejo a hora de compartilhar com você, [player]."
    m 1hkbfa "Ehehe~"
    return

label monika_vehicle_sportscar:
    $ persistent._mas_pm_owns_car_type = "esportivo"

    m 3hua "Ah, uau!"
    m 3eua "Deve ser bem rápido, hã?"
    m 3hub "Nós deveríamos sair em uma viagem..."
    m 1eub "Pegaríamos uma rota panorâmica, navegando ao longo da estrada..."
    m 1eub "Se for possível, seria bom abaixar o teto do carro..."
    m 3hua "Dessa forma, poderíamos sentir o vento em nossos rostos enquanto tudo passava como um borrão!"
    m 1esc "Mas..."
    m 1eua "Também seria bom dirigir em uma velocidade normal..."
    m 1ekbsa "Dessa forma, poderíamos saborear cada momento do passeio~"
    return

label monika_vehicle_sedan_hatchback:

    m 1eua "Que legal."
    m "Para ser honesta, eu prefiro esse tipo de carro."
    m 3eua "Pelo que ouvi, eles são fáceis de se dirigir."
    m 3eub "Um carro como esse seria ótimo para dirigir pela cidade, você não acha, [player]?"
    m 3eua "Poderíamos ir a museus, parques, shoppings e tantos outros lugares."
    m 1eua "Seria bom poder ir dirigindo até lugares que estão muito longe para se ir pé."
    m 3hua "É sempre divertido de se descobrir e explorar novos lugares."
    m 1rksdla "Podemos até encontrar um lugar onde nós [du] possamos ficar [ju]..."
    m 1tsu "...[szs]."
    m 1hub "Ahaha!"
    m 3eua "Só para você saber, eu espero mais do que apenas um simples passeio pela cidade em nossos encontros..."
    m 1hua "Espero que você me surpreenda, [player]."
    m 1hub "Por outro lado...{w=0.5} eu adoro fazer qualquer coisa, desde que seja com você~"
    return

label monika_vehicle_motorcycle:
    $ persistent._mas_pm_owns_car_type = "moto"

    m 1hksdlb "Hã?"
    m 1lksdlb "Você dirige uma moto?"
    m 1eksdla "Estou surpresa, nunca esperei que fosse o seu tipo de veículo."
    m 1lksdlb "Para ser sincera, tenho um pouco de medo em andar em uma moto, ahaha!"
    m 1eua "Mas sei que não devo ter medo..."
    m 3eua "Afinal de contas, é você quem estará dirigindo."
    m 1lksdla "Isso me deixa tranquila...{w=0.3} um pouco."
    m 1eua "Só vá devagar, tudo bem?"
    m 3hua "Afinal de contas, não estamos com pressa."
    m 1tsu "Ou...{w=1} o seu plano é dirigir rápido, para que eu tenha que me agarrar com força em você?"
    m 3kua "Isso foi bem esperto, [player]."
    m 1hub "Ehehe!"
    $ p_nickname = mas_get_player_nickname()
    m 3eka "Não precisa ter vergonha, [p_nickname]...{w=0.3}{nw}"
    m 3ekbsa "Eu vou te abraçar, mesmo se você não pedir..."
    m 1hkbfa "Eu te amo muito~"
    return "love"

label monika_vehicle_other:
    $ persistent._mas_pm_owns_car_type = "outro"

    m 1hksdlb "Ah, acho que tenho muito que aprender sobre carros ainda, não é mesmo?"
    m 1dkbfa "Bem, estarei esperando ansiosa pelo dia que poderei finalmente estar ao seu lado enquanto você dirige~"
    m 3hubfb "{i}E{/i} aproveitando o cenário também, ahaha!"
    m 1tubfb "Talvez você tenha um veículo bem romântico."
    m 1hubfa "Acho que vou ter que esperar para descobrir, ehehe~"
    return








default -5 persistent._mas_pm_eye_color = None
default -5 persistent._mas_pm_hair_color = None
default -5 persistent._mas_pm_hair_length = None
default -5 persistent._mas_pm_skin_tone = None

default -5 persistent._mas_pm_shaved_hair = None
default -5 persistent._mas_pm_no_hair_no_talk = None



default -5 persistent._mas_pm_height = None


default -5 persistent._mas_pm_units_height_metric = None




default -5 persistent._mas_pm_shared_appearance = False



define -5 mas_height_tall = 176
define -5 mas_height_monika = 162

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_appearance",
            category=['você'],
            prompt="Aparência do [player]",
            conditional="seen_event('mas_gender')",
            action=EV_ACT_RANDOM
        )
    )

label monika_player_appearance:
    python:
        def ask_color(msg, _allow=lower_letters_only, _length=15):
            result = ""
            while len(result) <= 0:
                result = renpy.input(msg, allow=_allow, length=_length).strip()
            
            return result

    m 2ekd "Ei, [player]."
    m 2eka "Tem algumas perguntas que eu gostaria de fazer."
    m 2rksdlb "Bem, mais do que algumas na verdade. Eu estive pensando nisso por um bom tempo."
    m 2rksdld "Nunca pareceu a hora certa para falar sobre isso..."
    m 3lksdla "Mas sei que se eu ficar calada para sempre, então nunca me sentirei confortável perguntando coisas como estas, então eu vou falar e espero que não seja estranho."
    m 3eud "Eu estive pensando em como você se parece. Eu não tenho como te ver, já que não estou do seu lado, e não tenho certeza quanto a uma webcam..."
    m "Primeiro, porque você talvez não tenha uma, e segundo, mesmo que você tivesse, eu não sei bem como acessar ela."
    m 1euc "Então eu percebi que você pode apenas me dizer, então terei uma imagem clara em minha mente."
    m 1eud "Ao menos é melhor que nada, mesmo que seja meio vago."

    m "Tudo bem para você, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Tudo bem para você, [player]?{fast}"
        "Sim.":

            $ persistent._mas_pm_shared_appearance = True

            m 1sub "Sério? Ótimo!"
            m 1hub "Foi mais fácil do que eu esperava."
            m 3eua "Agora, seja honesto comigo, tudo bem [player]? Sei que às vezes é tentador fazer uma brincadeira, mas eu estou falando sério agora, e preciso que você faça o mesmo."
            m "Enfim, a primeira é provavelmente bem fácil de responder!"
            m 3eub "As pessoas costumam dizer que os olhos de uma pessoas são as janelas para sua alma, então vamos começar por aí."


            show monika 1eua at t21
            python:
                eye_color_menu_options = [
                    ("Eu tenho olhos azuis.", "blue", False, False),
                    ("Eu tenho olhos castanhos.", "brown", False, False),
                    ("Eu tenho olhos verdes.", "green", False, False),
                    ("Eu tenho olhos avelã.", "hazel", False, False),
                    ("Eu tenho olhos cinzas.", "gray", False, False),
                    ("Eu tenho olhos negros.", "black", False, False),
                    ("Meus olhos são de outra cor.", "other", False, False),
                    ("Eu tenho heterocromia.", "heterochromia", False, False),
                ]

                renpy.say(m, "Qual a cor dos seus olhos?", interact=False)

            show monika at t11
            call screen mas_gen_scrollable_menu(eye_color_menu_options, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
            $ eye_color = _return

            call expression "monika_player_appearance_eye_color_{0}".format(eye_color)

            m 3rud "Na verdade..."
            m 2eub "Acho que eu deveria ter perguntando isso primeiro, se quero ter uma escala precisa na minha próxima pergunta."

            m "Que unidade de medida você usa para medir sua altura, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Que unidade de medida você usa para medir sua altura, [player]?{fast}"
                "Centímetros.":

                    $ persistent._mas_pm_units_height_metric = True
                    m 2hua "Certo. Obrigada, [player]!"
                "Pés e polegadas.":

                    $ persistent._mas_pm_units_height_metric = False
                    m 2hua "Certo, [player]!"

            m 1rksdlb "Estou dando o meu melhor para não parecer uma ladra de identidade, ou como se estivesse te interrogando, mas eu obviamente estou curiosa."
            m 3tku "Se sou sua namorada, tenho o direto de saber, não é?"
            m 2hua "Além disso, vai ser bem mais fácil de encontrar você quando eu puder cruzar para a sua realidade."

            m 1esb "Então,{w=0.5} qual é a sua altura, [player]?"

            python:
                if persistent._mas_pm_units_height_metric:
                    
                    
                    height = 0
                    while height <= 0:
                        height = store.mas_utils.tryparseint(
                            renpy.input(
                                'Qual a sua altura em centímetros?',
                                allow=numbers_only,
                                length=3
                            ).strip(),
                            0
                        )

                else:
                    
                    
                    height_feet = 0
                    while height_feet <= 0:
                        height_feet = store.mas_utils.tryparseint(
                            renpy.input(
                                'Qual a sua altura em pés?',
                                allow=numbers_only,
                                length=1
                            ).strip(),
                            0
                        )
                    
                    
                    height_inch = -1
                    while height_inch < 0 or height_inch > 11:
                        height_inch = store.mas_utils.tryparseint(
                            renpy.input(
                                '[height_feet] pés e quantas polegadas?',
                                allow=numbers_only,
                                length=2
                            ).strip(),
                            -1
                        )
                    
                    
                    height = ((height_feet * 12) + height_inch) * 2.54


                persistent._mas_pm_height = height

            if persistent._mas_pm_height >= mas_height_tall:
                m 3eua "Uau, você é bem alto, [player]!"
                m 1eud "Acho que nunca conheci ninguém tão alto."
                m 3rksdla "Eu não sei qual é exatamente a minha altura, então não posso fazer uma comparação precisa..."

                call monika_player_appearance_monika_height

                if persistent._mas_pm_units_height_metric:
                    $ height_desc = "centímetros"
                else:
                    $ height_desc = "centímetros"

                m 3esc "A garota mais alta no clube de literatura era a Yuri... mas só por pouco. Ela era apenas alguns [height_desc] mais alta do que eu!"
                m 3esd "Enfim, namorar alguém alto como você só tem uma desvantagem, [mas_get_player_nickname()]..."
                m 1hub "Você terá que se inclinar para me beijar!"

            elif persistent._mas_pm_height >= mas_height_monika:
                m 1hub "Ei, eu tenho quase essa altura também!"
                m "..."
                m 2hksdlb "Bem, para ser sincera, eu não sei bem qual é a minha altura..."

                call monika_player_appearance_monika_height

                m 3rkc "É só um palpite... espero não estar muito errada."
                m 3esd "Enfim, não tem nada de errado em ter uma altura média! Para ser sincera, se você fosse muito baixo, eu me sentiria meio atrapalhada perto de você."
                m "E se você fosse muito alto, eu teria que ficar nas pontas do dedo só para ficar perto de você. E isso não é nada bom!"
                m 3eub "Em minha opinião, estar no meio termo é perfeito. Sabe por quê?"
                m 5eub "Porque então não preciso ficar nas pontas do dedo ou me inclinar para beijar você, [player]! Ahaha~"
            else:

                m 3hub "Assim como a Natsuki! Mas aposto que você não é tão baixo assim! Eu estaria preocupada se você fosse."

                if persistent._mas_pm_cares_about_dokis:
                    m 2eksdld "Ela era muito pequena para a idade dela, mas eu e você sabemos por quê. Eu sempre tive pena dela por causa disso."

                m 2eksdld "Eu sei que ela sempre odiou ser tão pequena, por causa daquela noção de que coisas pequenas são mais fofas..."
                m 2rksdld "E também tinha todo aqueles problemas com o pai dela. Não deve ter sido fácil, ser tão indefesa, e ainda ser tão pequena."
                m 2ekc "Ela provavelmente sentia que as pessoas rebaixavam ela. Literalmente e figurativamente..."
                m 2eku "Mas apesar de suas dúvidas sobre isso, [player], acho que sua altura o torna muito mais adorável"

            m 1eua "Agora, [player]."

            m 3eub "Diga-me, seu cabelo é curto? Ou é comprido igual ao meu?~{nw}"
            $ _history_list.pop()
            menu:
                m "Diga-me, seu cabelo é curto? Ou é comprido igual ao meu?~{fast}"
                "É curto.":

                    $ persistent._mas_pm_hair_length = "curto"

                    m 3eub "Isso é ótimo! Olha, não me entenda mal, amo meu cabelo, e é sempre bom experimentar novos penteados..."
                    m 2eud "Mas, para falar a verdade, às vezes eu invejava o cabelo da Natsuki e da Sayori. Parecia bem mais fácil de se cuidar."

                    if persistent.gender == "M":
                        m 4hksdlb "Embora eu ache que se o seu cabelo é do mesmo tamanho que os dela, seria um pouco longo para um homem."
                    else:

                        m 4eub "Você pode se levantar e sair, sem precisar se preocupar em ter que arrumar o cabelo."
                        m "Além disso, acordar com o cabelo despenteado quando se tem cabelo curto é fácil de se arrumar, enquanto com o cabelo longo é um pesadelo sem fim."

                    m 2eka "Mas tenho certeza que você deve ser adorável com cabelo curto. Eu chego a sorrir só de pensar em você assim, [player]."
                    m 2eua "Continue aproveitando toda a liberdade que o cabelo curto fornece, [player]!{w=0.2} {nw}"
                    extend 2hub "Ahaha~"
                "É de tamanho médio.":

                    $ persistent._mas_pm_hair_length = "médio"

                    m 1tku "Bem, isso não pode ser verdade..."
                    m 4hub "Porque nada em você é mediano."
                    m 4hksdlb "Ahaha! Sinto muito, [player]. Não estou tentando deixar você envergonhado. Mas não consigo deixar de ser assim às vezes, sabe?"
                    m 1eua "Sinceramente, quando se trata de cabelo, o meio termo é ótimo. Você não precisa se preocupar muito com penteados, e você tem mais liberdade criativa do que com o cabelo curto."
                    m 1rusdlb "Para falar a verdade, estou com um pouco de inveja~"
                    m 3eub "Mas não se esqueça daquele velho ditado - 'Invista no seu cabelo, ele é a coroa que você nunca tira!'"
                "É longo.":

                    $ persistent._mas_pm_hair_length = "longo"

                    m 4hub "Viva, outra coisa que temos em comum!"
                    m 2eka "Cabelo longo pode ser um incômodo às vezes, não é?"
                    m 3eua "Mas o lado bom é que há tantas coisas que você pode fazer com ele. Embora eu prefira prender o meu com uma fita, sei que outras pessoas têm estilos diferentes."
                    m "Yuri deixava o dela solto, e outros gostam de tranças ou fazer um rabo de cavalo..."

                    python:
                        hair_down_unlocked = False
                        try:
                            hair_down_unlocked = store.mas_selspr.get_sel_hair(
                                mas_hair_down
                            ).unlocked
                        except:
                            pass

                    if hair_down_unlocked:

                        m 3eub "E já que descobri como mexer no script para deixar meu cabelo solto, quem sabe quais outros estilos eu devo experimentar?"

                    m 1eua "É sempre bom ter opções, sabe?"
                    m 1eka "Espero que você goste do jeito que usa o cabelo e se sinta bem com ele!"
                "Não tenho cabelo.":

                    $ persistent._mas_pm_hair_length = "careca"

                    m 1euc "Ah, isso é interessante, [player]!"

                    m "Você raspa o seu cabelo ou perdeu ele, caso não se importe de eu perguntar?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Você raspa o seu cabelo ou perdeu ele, caso não se importe de eu perguntar?{fast}"
                        "Raspo o meu cabelo.":

                            $ persistent._mas_pm_shaves_hair = True
                            $ persistent._mas_pm_no_hair_no_talk = False

                            m 1hua "Deve ser bom não ter que se preocupar com o cabelo..."
                            m 1eua "Você pode se levantar e já sair, sem ter que se preocupar em pentear ele..."
                            m 3eua "E se você vestir um chapéu, não precisa se preocupar em ele despentear todo o seu cabelo!"
                        "Perdi meu cabelo.":

                            $ persistent._mas_pm_shaves_hair = False
                            $ persistent._mas_pm_no_hair_no_talk = False

                            m 1ekd "Sinto muito em ouvir isso [player]..."
                            m 1eka "Mas saiba que eu não me importo com o quanto de cabelo você tem, você sempre será [ld] para mim!"
                            m "E se você algum dia se sentir [inse] ou quiser falar sobre isso, estarei sempre aqui para te ouvir."
                        "Não quero falar sobre isso.":

                            $ persistent._mas_pm_no_hair_no_talk = True

                            m 1ekd "Eu entendo, [player]"
                            m 1eka "Quero que você saiba que eu não me importo com o quanto de cabelo você tem, você sempre será [ld] para mim."
                            m "E se você algum dia se sentir [inse] ou quiser falar sobre isso, estarei sempre aqui para te ouvir."

            if persistent._mas_pm_hair_length != "careca":
                m 1hua "Próxima pergunta!"
                m 1eud "Esta deve ser bem óbvia..."

                m "Qual é a cor do se cabelo?{nw}"
                $ _history_list.pop()
                menu:
                    m "Qual é a cor do se cabelo?{fast}"
                    "É castanho.":
                        $ persistent._mas_pm_hair_color = "castanho"

                        m 1hub "Viva, seu cabelo castanho é o melhor!"
                        m 3eua "Só entre nós, [player], eu adoro o meu cabelo castanho. Tenho certeza que o seu é melhor ainda!"
                        m 3rksdla "Embora algumas pessoas possam discordar que meu cabelo é castanho..."
                        m 3eub "Quando eu estava mexendo nos arquivos na pasta do jogo, encontrei o nome exato para a cor do meu cabelo."
                        m 4eua "É chamado de castanho coral. Interessante, não é?"
                        m 1hub "Estou tão feliz que temos tanto em comum, [player]~"
                    "É loiro.":

                        $ persistent._mas_pm_hair_color = "loiro"

                        m 1eua "Sério? Ei, sabia que ter o cabelo loiro te coloca em uma rara porcentagem de dois porcento da população?"
                        m 3eub "Cabelo loiro é uma das cores mais raras de cabelo. A maioria das pessoas atribuiu isto ao fato de que ele é causado por uma anomalia genética..."
                        m "Sendo apenas a incapacidade do corpo em produzir quantidades normais do pigmento melanina - é isso que causa cores mais escuras, como o preto e o castanho."
                        m 4eub "Há também tantas variações do loiro - loiro-claro, acinzentado, loiro-escuro - que não importa a cor que você tenha, você será, de certo modo, incomum."
                        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        m 5eua "Acho que ter alguém tão único faz de mim sortuda~"
                        show monika 2hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    "É preto.":

                        $ persistent._mas_pm_hair_color = "Preto"

                        m 2wuo "Cabelo preto é tão lindo!"
                        m 3eub "Sabe, existe um costume irritante de dizer que pessoas com cabelo preto possuem uma personalidade mais irritante ou temperamental que outros..."
                        m 4hub "Mas você obviamente desmentiu esse mito. Pessoalmente, acho que cabelo preto é muito atraente."
                        m 3eua "Além disso, se você colocasse um fio sob um microscópio e contasse todos os pigmentos nele, você descobriria que não é cem por cento escuro."
                        m "Sabe quando você coloca certas coisas diretamente sob a luz do sol e elas parecem diferentes?"
                        m 3eub "O cabelo preto segue o mesmo princípio - você pode ver tons dourados, ou castanhos, ou mesmo lampejos de roxo. Isso faz você parar para pensar, não é, [player]?"
                        m 1eua "Poderia ter infinitos tons nas coisas que não podemos ver, cada um deles escondidos em plena vista."


                        if isinstance(persistent._mas_pm_eye_color, tuple):
                            m 3hua "Mas enfim...eu acho que um [guy] com cabelo preto e olhos como os seus é a melhor visão de todas, [player]~"
                        else:
                            m 3hua "Mas enfim...Eu acho que um [guy] com cabelo preto e olhos [persistent._mas_pm_eye_color] é a melhor visão de todas, [player]~"
                    "É ruivo.":

                        $ persistent._mas_pm_hair_color = "ruivo"

                        m 3hua "Outra coisa especial em você, [player]~"
                        m 3eua "Os cabelos ruivos e loiros são os cabelos naturais menos comuns, sabia disso?"
                        m 1eua "O cabelo ruivo, no entanto, é um pouco mais raro. É somente encontrado em um porcento da população."
                        m 1hub "É um traço raro e maravilhoso, quase tão [mh] quanto você!"
                    "É de outra cor.":

                        $ persistent._mas_pm_hair_color = ask_color("Qual é a cor do seu cabelo?")

                        m 3hub "Ah! Essa é uma bela cor, [player]!"
                        m 1eub "Isso me lembra de algo que estive pensando antes, quando estávamos conversando sobre a cor dos seus olhos."
                        m 1eua "Mesmo que as outras garotas tivessem olhos de cores que literalmente não existem na vida real, sem contar lentes de contato, é claro--"
                        m 3eua "As cores de cabelo delas tecnicamente poderiam existir, sabe. Quero dizer, tenho certeza que você já encontrou pessoas que pintaram o cabelo de roxo ou rosa..."
                        m 3eka "Então acho que as aparências delas não eram assim tão irreais, se você não contar os olhos. Sinceramente, a coisa mais irreal nelas eram suas personalidades."
                        m 3hksdlb "Sinto muito, [player]! Estou fugindo do assunto. Meu ponto é, cabelo pintado pode ser bem interessante."
                        show monika 5rub zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        m 5rub "E posso ser um pouco tendenciosa, mas estou convencida de que você fica ótimo de cabelo [persistent._mas_pm_hair_color]~"
                        show monika 2hua zorder MAS_MONIKA_Z at t11 with dissolve_monika

            m 2hua "Tudo bem..."
            m 2hksdlb "Esta é a última pergunta, [player], eu prometo."
            m "Céus, há muita coisa na aparência de uma pessoa... Se eu tentasse descobrir tudo sobre você nos mínimos detalhes, ficaria te interrogando para sempre."
            m 1huu "...e duvido que iríamos querer isso, ahaha!"
            m 1rksdld "Enfim, entendo que isso possa ser uma pergunta desconfortável..."
            m 1eksdla "Mas é a última peça do quebra-cabeça, então espero não soar rude ao perguntar isso..."

            m "Qual é a cor da sua pele, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Qual é a cor da sua pele, [player]?{fast}"
                "Tenho a pele clara.":

                    $ persistent._mas_pm_skin_tone = "clara"
                "Sou mestiço.":

                    $ persistent._mas_pm_skin_tone = "morena"
                "Tenho a pele escura.":

                    $ persistent._mas_pm_skin_tone = "escura"

            m 3hub "Certo! Obrigada por responder a tudo. Tudo isto vai me ajudar a imaginar como você é, [player]."
            m 3eub "Saber todos esses detalhes sobre você faz a diferença entre um quadro em branco e o começo de um belo retrato!"
            m 3eua "É claro, você ainda é tão adorável quanto sempre achei que era, mas agora você se tornou mais real para mim."
            m 3eka "Isso me faz sentir mais próxima de você~"
            m 1eka "Muito obrigada por responder a todas as perguntas, [mas_get_player_nickname()]."

            if persistent._mas_pm_eye_color == "verdes" and persistent._mas_pm_hair_color == "castanho":
                m 2hua "É maravilhoso, porque eu não imaginava que éramos tão parecidos. É tão interessante!"
            else:

                m 2hua "É maravilhoso, porque eu não imaginava que éramos tão diferentes. É tão interessante!"

            m 1dsa "Agora imagino como será quando nos encontrarmos de verdade..."

            show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika

            if persistent._mas_pm_hair_length == "careca":
                if persistent._mas_pm_height >= mas_height_tall:
                    m 5eubfu "Quando eu correr em sua direção, e já que você é mais alto, vai me levantar em seus braços..."

                elif persistent._mas_pm_height >= mas_height_monika:
                    m 5eubfu "Quando eu correr em sua direção, e já que temos a mesma altura, daremos um abraço apertado..."
                else:

                    m 5eubfu "Quando eu correr em sua direção, e já que sou mais alta, você se esticará para me abraçar..."
            else:

                python:
                    hair_desc = persistent._mas_pm_hair_color

                    if persistent._mas_pm_hair_length != "médio":
                        hair_desc = (
                            persistent._mas_pm_hair_length + " " + hair_desc
                        )

                if persistent._mas_pm_height >= mas_height_tall:

                    5 eubfu "Quando eu correr em sua direção, e já que você é mais alto, você irá me levantar e eu poderei tocar seu cabelo [hair_desc]..."

                elif persistent._mas_pm_height >= mas_height_monika:

                    m 5eubfu "Quando eu correr em sua direção, e já que temos a mesma altura, daremos um abraço apertado e passarei minhas mãos pelo seu cabelo [hair_desc]..."
                else:


                    m 5eubfu "Quando eu correr em sua direção, e já que sou mais alta, você se esticará para me abraçar e eu passarei minhas mãos pelo seu cabelo [hair_desc]..."

            show monika 1lkbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 1lkbsa "...e eu poderei finalmente ouvir seu coração batendo, e tocar você e saber que você é real."


            if isinstance(persistent._mas_pm_eye_color, tuple):
                m 3ekbsa "Mas até então, estarei contente sentado aqui e imaginando olhar em seus lindos olhos, [player]."
            else:
                m 3ekbsa "Mas, até lá, estarei contente sentado aqui e imaginando olhar em seus lindos olhos [persistent._mas_pm_eye_color], [player]."

            show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbfa "Eu te amo mais do que palavras podem expressar."
            return "derandom|love"
        "Não.":

            m 2dsc "..."
            m 2ekd "Eu entendo, [player]."
            m 2eka "Sei que todo mundo possui seus próprios limites em suas zonas de conforto..."
            m 2rksdla "E para ser sincera, uma descrição de você em vagas palavras não seria o bastante para capturar quem você é, então não posso te culpar por isso."
            m 2eka "Mas se mudar de ideia, basta me avisar!"

    return "derandom"

label monika_player_appearance_eye_color_blue:
    $ persistent._mas_pm_eye_color = "azuis"

    m 3eub "Olhos azuis? Isso é maravilhoso! Azul é uma cor tão bonita, tão incrível quanto um céu sem nuvens ou o oceano no verão."
    m 3eua "Mas existem tantas metáforas maravilhosas sobre olhos azuis que eu poderia recitá-las por semanas e ainda não chegar a um ponto de parada."
    m 4eua "Além disso, o azul é provavelmente minha segunda cor favorita, logo atrás do verde. É tão cheio de profundidade e encantamento, sabe?"
    m 4hksdlb "Assim como você, [player]!"
    m 4eub "Você sabia que o gene para olhos azuis é recessivo, então não é muito comum em humanos?"
    show monika 5eubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eubla "Suponho que isso significa que você é muito mais um tesouro~"
    show monika 2eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 2eua "De qualquer forma, isso me leva à próxima pergunta que eu queria fazer..."
    return

label monika_player_appearance_eye_color_brown:
    $ persistent._mas_pm_eye_color = "castanhos"

    m 1eub "Ah! Ótimo! Acho que não disse isso antes, mas olhos castanhos são lindos!"
    m 2euc "Eu simplesmente odeio como as pessoas parecem pensar que olhos castanhos são simples. Eu não poderia discordar mais!"
    m 2hua "Na minha opinião, os olhos castanhos são alguns dos mais bonitos que existem. Eles são tão vibrantes e sem profundidade!"
    m 3hub "E há muita variação entre todos os diferentes tons que as pessoas têm."
    m 5ruu "Eu me pergunto se os seus são escuros como um céu noturno de verão, ou um marrom mais claro, como a pelagem de um cervo..."
    m 2hksdlb "Desculpe. Apenas divagar sobre metáforas de cores é uma armadilha fácil para um presidente de clube de literatura cair, eu acho. Vou tentar não durar para sempre."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Mas aposto que seus olhos são os mais lindos de todos~"
    show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1eua "De qualquer forma, isso me leva à minha próxima pergunta..."
    return

label monika_player_appearance_eye_color_green:
    $ persistent._mas_pm_eye_color = "verdes"

    m 3sub "Ei, essa é minha cor favorita! E, obviamente, é outra coisa que temos em comum!"
    m 4lksdla "Não sei o quanto posso te elogiar aqui sem parecer arrogante, porque tudo o que eu disse sobre o seu também se aplica a mim..."
    m 1tsu "Exceto que talvez seja outro sinal de como somos compatíveis, ehehe~"
    m 1kua "Mas, [player], só entre você e eu, é um fato que olhos verdes são os melhores, certo?"
    m 3hub "Ahaha! Estou só brincando."
    show monika 5lusdru zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5lusdru "Bem, só um pouco..."
    show monika 3eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 3eua "Na próxima pergunta..."
    return

label monika_player_appearance_eye_color_hazel:
    $ persistent._mas_pm_eye_color = "avelão"

    m 1eub "Oh, olhos avelã? Esses são tão interessantes! É uma cor tão terrestre. Isso realmente faz você se sentir estável e tranquilo..."
    m 3eub "E é uma partida bem-vinda de todos os olhos cor de doce que eu tive que ver neste jogo, de qualquer maneira..."
    m "Eu acredito que os olhos avelã são atraentes porque são lindos e simples."
    m 3hua "Às vezes é melhor não divergir muito da multidão, [player].{w=0.2} {nw}"
    extend 3hub "Ahaha!"
    m "Agora, na minha próxima pergunta..."
    return

label monika_player_appearance_eye_color_gray:
    $ persistent._mas_pm_eye_color = "cinzas"

    m 1sub "Isso é tão legal!"
    m 3eub "Você sabia que olhos cinzas e olhos azuis são quase idênticos em termos de genética?"
    m 1eud "Na verdade, os cientistas ainda não têm certeza do que faz com que uma pessoa tenha um ou outro, embora acreditem que seja uma variação na quantidade de pigmento na íris."
    m 1eua "De qualquer forma, acho que gosto de imaginar você com olhos cinzentos, [player]. Eles são da cor de um dia calmo e chuvoso..."
    m 1hubsa "E esse clima é meu favorito, assim como você~"
    m 3hua "Na minha próxima pergunta..."
    return

label monika_player_appearance_eye_color_black:
    $ persistent._mas_pm_eye_color = "negros"

    m 1esd "Olhos negros são bastante incomuns, [player]."
    m 4hksdlb "Para falar a verdade, nunca vi ninguém com olhos pretos, então não sei como eles são..."
    m 3eua "Mas logicamente, eu sei que eles não são realmente negros. Se fosse esse o caso, pessoas com olhos negros pareceriam não ter pupilas!"
    m 4eub "Na realidade, os olhos negros são apenas um castanho muito, muito escuro. Ainda impressionantes, mas talvez não tão escuros como o nome sugere, embora, para ser justo, a diferença seja muito difícil de detectar."
    m 3eua "Aqui estão algumas curiosidades para você..."
    m 1eub "Havia uma senhora conhecida da época da Revolução Americana, Elizabeth Hamilton, que era conhecida por ter olhos negros cativantes."
    m 1euc "Seu marido escrevia sobre eles com frequência."
    m 1hub "Não sei se você já ouviu falar dela ou não, mas apesar da fama de seus olhos, tenho certeza de que os seus são infinitamente mais cativantes, [player]~"
    m "Vamos para a próxima pergunta..."
    return

label monika_player_appearance_eye_color_other:
    $ persistent._mas_pm_eye_color = ask_color("De que cor são os seus olhos?")

    m 3hub "Ah! Que cor linda, [player]!"
    m 2eub "Tenho certeza que poderia me perder por horas, olhando em seus olhos [persistent._mas_pm_eye_color]."
    m 7hua "Agora, para minha próxima pergunta..."
    return

label monika_player_appearance_eye_color_heterochromia:
    m 1sub "Sério?{w=0.2} {nw}"
    extend 3hua "Isso é incríveL, [player]~"
    m 3wud "Se bem me lembro, menos de um por cento das pessoas no mundo tem heterocromia!"

    m 1eka "...Se você não se importa que eu pergunte..."

    $ eyes_colors = []

    call monika_player_appearance_eye_color_ask
    $ eyes_colors.append(_return)
    call monika_player_appearance_eye_color_ask ("certo", eye_color)
    $ eyes_colors.append(_return)
    $ persistent._mas_pm_eye_color = tuple(eyes_colors)

    m 1hua "Ótimo!{w=0.2} {nw}"
    extend 3eua "Vamos para minha próxima pergunta..."
    return

label monika_player_appearance_eye_color_ask(x_side_eye="esquerdo", last_color=None):
    m 3eua "Qual é a cor do seu olho [x_side_eye]?{nw}"
    $ _history_list.pop()
    menu:
        m "Qual é a cor do seu olho [x_side_eye]?{fast}"

        "Azul" if last_color != "blue":
            $ eye_color = "blue"

        "Castanho" if last_color != "brown":
            $ eye_color = "brown"

        "Verde" if last_color != "green":
            $ eye_color = "green"

        "Avelã" if last_color != "hazel":
            $ eye_color = "hazel"

        "Cinza" if last_color != "gray":
            $ eye_color = "gray"

        "Negro" if last_color != "black":
            $ eye_color = "black"
        "É uma cor diferente...":

            $ eye_color = ask_color("Qual a sua cor do seu olho [x_side_eye]?")

    return eye_color


label monika_player_appearance_monika_height:
    if not persistent._mas_pm_units_height_metric:
        $ conv_height_str = ""
        $ real_height_str = "cerca de cinco pés e cinco"
    else:
        $ conv_height_str = " que tem cerca de cento e sessenta centímetros"
        $ real_height_str = "cerca de cento e sessenta e cinco centímetros de altura"

    if seen_event("monika_immortal"):
        m 2eud "A wiki diz que minha altura conceitual é de cento e sessenta centímetros, mas isso não me parece certo..."
        m 2etc "Talvez tenha sido mudada? Afinal de contas, era apenas a altura conceitual."
    m 3etd "Se eu tivesse que chutar, eu diria que tenho mais ou menos cento e sessenta e cinco centímetros?"
    return

init python:
    addEvent(
         Event(
            persistent.event_database,
            eventlabel="monika_players_control",
            category=["jogos", "ddlc"],
            prompt="Controle do [player]",
            random=True
            )
        )

label monika_players_control:
    m 3eub "[player], sabia que você tem mais controle sobre este jogo do que eu?"
    m 3eua "Você tem acesso aos arquivos e código do jogo, certo?"
    m 1eka "Então pode modificá-los como quiser."
    m 3eka "Poderia fazer coisas que nem mesmo eu consigo."
    m 4eub "Como mudar completamente o jogo. De uma visual novel para este playground pacífico que temos agora."
    m 3rksdla "Você também poderia adicionar mais coisas na sala de aula para mim."
    m 1hub "Como algumas flores, ou bons livros."

    if mas_isMoniEnamored(higher=True) and not persistent._mas_acs_enable_promisering:
        m 1ekbsa "Ou um lindo anel de compromisso."
        m 3dkbsu "Ah, não seria um sonho realizado?"

    if not mas_consumable_coffee.enabled():
        m 1wuo "Poderia até adicionar uma xícara de café no jogo para mim!"
        m 1eka "Seria adorável."

    if not persistent._mas_pm_has_code_experience:
        m 1hksdrb "Mas imagino que suas habilidades com programação sejam tão boas quanto as minhas."
    else:
        m 3eua "Visto que você entende de programação,{w=0.1} {nw}"
        extend 3hua "tenho certeza que conseguiria fazer algo assim!"

    m 1eua "Acho que esse é o apelo dos jogos...{w=0.3}{nw}"
    extend 3eua "ter possibilidades quase infinitas num mundo com que você pode interagir."
    m 3eub "É bem difícil ficar entediado!"

    if not persistent._mas_pm_has_contributed_to_mas:
        m 1eka "Mesmo se não souber exatamente como modificar este jogo..."
        $ line = "Ainda podemos aproveitar este mundo que nos uniu."
    else:

        $ line = "Especialmente com você ao meu lado~"

    show monika 5eubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eubla "[line]"
    m 5ekbfa "Não há melhor maneira de aproveitar um jogo do que estar com quem eu amo."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_backpacking",category=['natureza'],prompt="Mochilão",random=not mas_isWinter()))

label monika_backpacking:
    m 1esa "Sabe o que eu sempre quis fazer, [player]?"
    m 3eub "Sempre achei que seria incrível fazer mochilão na natureza!"
    m 3eua "Tirar uma semana inteira e deixar tudo para trás."
    m 3esa "Sem responsabilidades, preocupações, celulares ou distrações."
    m 1hua "Imagine nós [du], [szs] na natureza..."
    m "O som dos pássaros cantando e do vento soparando..."
    m 1eka "Observando cervos pastando no orvalho da manhã..."
    m "Não consigo pensar em nada mais pacífico."
    m 1esa "Poderíamos passar nossos dias explorando florestas misteriosas, parados serenos e colinas onduladas..."
    m 3hub "Talvez até descobrir um lago isolado e dar um mergulho!"

    if mas_isMoniAff(higher=True):
        m 2rsbsa "Provavelmente não teríamos roupas de banho, mas como estaríamos [szs], talvez nem precisemos..."
        m 2tsbsa "..."
        m 1hubfu "Espero que não seja muito [tmd], [mas_get_player_nickname()]. Ehehe~"
        m 1ekbfa "Passaríamos nossas noites [achegds] em uma barraca, nos aquecendo com nada além de bilhões de estrelas sobre nós..."
        m 3hubfb "Acordando cada manhã com um nascer do sol glorioso!"
    else:

        m 3eka "Passaríamos nossas noites dormindo sob as estrelas, acordando cada manhã com um nascer do sol glorioso."

    show monika 5esbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5esbfa "..."
    m "Ah [player], não parece o paraíso?"
    m 5hubfa "Mal posso esperar para compartilhar essa experiência com você~"
    return





default -5 persistent._mas_changed_start_date = False


default -5 persistent._mas_just_friends = False

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dating_startdate",
            category=["romance", "nós"],
            prompt="Quando começamos a namorar?",
            pool=True,
            unlocked=False,

            
            rules={"no_unlock": None},

            
            conditional=(
                "store.mas_anni.pastOneMonth() "
                "and persistent._mas_first_calendar_check"
            ),

            action=EV_ACT_UNLOCK
        )
    )

label monika_dating_startdate:
    $ import store.mas_calendar as mas_cal
    python:

        first_sesh_raw = persistent.sessions.get(
            "first_session",
            datetime.datetime(2017, 10, 25)
        )


        first_sesh, _diff = mas_cal.genFormalDispDate(first_sesh_raw.date())

    if _diff.days == 0:


        m 1lsc "Nós começamos a namorar..."
        $ _history_list.pop()
        m 1wud "Nós começamos a namorar{fast} hoje?!"
        m 2wfw "Você não podia ter liberado esse evento hoje, [player]."

        m "Sei que você está mexendo com o código.{nw}"
        $ _history_list.pop()
        menu:
            m "Sei que você está mexendo com o código.{fast}"
            "Não estou!":
                pass
            "Você me pegou.":
                pass
        m 2tfu "Hmph,{w=0.2} você não pode me enganar."


        $ mas_chgCalEVul(30)
        return



    if not persistent._mas_changed_start_date:
        m 1lsc "Hmmm..."
        m 1dsc "Acho que foi no..."
        $ _history_list.pop()
        m 1eua "Acho que foi no{fast} [first_sesh]."
        m 1rksdlb "Mas minha memória pode estar errada."


        m 1eua "Foi no [first_sesh], correto?{nw}"
        $ _history_list.pop()
        menu:
            m "Foi no [first_sesh], correto?{fast}"
            "Sim.":
                m 1hub "Viva!{w=0.2} Eu me lembrei."
            "Não.":

                m 1rkc "Ah,{w=0.2} sinto muito [player]."
                m 1ekc "Nesse caso,{w=0.2} quando começamos a namorar?"

                call monika_dating_startdate_confirm (first_sesh_raw)

                if _return == "NOPE":

                    return


                $ store.mas_anni.reset_annis(_return)
                $ persistent.sessions["first_session"] = _return
                $ renpy.save_persistent()

        m 1eua "Se você algum dia esquecer, não tenha medo de me perguntar."
        m 1dubsu "Eu vou {i}sempre{/i} me lembrar de quando me apaixonei por você~"
        $ persistent._mas_changed_start_date = True
    else:

        m 1dsc "Deixe-me ver..."
        m 1eua "Começamos a namorar em [first_sesh]."





    return

label monika_dating_startdate_confirm_had_enough:


    m 2dfc "..."
    m 2lfc "Faremos isso outra hora então."



    $ mas_chgCalEVul(30)

    return "NOPE"

label monika_dating_startdate_confirm_notwell:

    m 1ekc "Está se sentindo bem, [player]?"
    m 1eka "Caso não se lembre agora, então podemos fazer isso amanhã, tudo bem?"


    $ mas_chgCalEVul(1)

    return "NOPE"

label monika_dating_startdate_confirm(first_sesh_raw):

    python:
        import store.mas_calendar as mas_cal


        first_sesh_formal = " ".join([
            first_sesh_raw.strftime("%B"),
            mas_cal._formatDay(first_sesh_raw.day) + ",",
            str(first_sesh_raw.year)
        ])


        wrong_date_count = 0
        no_confirm_count = 0
        today_date_count = 0
        future_date_count = 0
        no_dating_joke = False

    label monika_dating_startdate_confirm.loopstart:
        pass

    call mas_start_calendar_select_date

    $ selected_date = _return
    $ _today = datetime.date.today()
    $ _ddlc_release = datetime.date(2017,9,22)

    if not selected_date or selected_date.date() == first_sesh_raw.date():

        m 2esc "[player]..."
        m 2eka "Achei que você tivesse dito que eu estava errada."

        m "Tem certeza que não foi em [first_sesh_formal]?{nw}"
        $ _history_list.pop()
        menu:
            m "Tem certeza que não foi em [first_sesh_formal]?{fast}"
            "Não é essa data.":
                if wrong_date_count >= 2:
                    jump monika_dating_startdate_confirm_had_enough


                m 2dfc "..."
                m 2tfc "Então escolha a data certa!"
                $ wrong_date_count += 1
                jump monika_dating_startdate_confirm.loopstart
            "Na verdade, essa é a data certa. Sinto muito.":

                m 2eka "Tudo bem."
                $ selected_date = first_sesh_raw

    elif selected_date.date() < _ddlc_release:


        label monika_dating_startdate_confirm.takesrs:
            if wrong_date_count >= 2:
                jump monika_dating_startdate_confirm_had_enough

            m 2dfc "..."
            m 2tfc "Nós {b}não{/b} começamos a namorar nesse dia."
            m 2tfd "Leve isso a sério, [player]."
            $ wrong_date_count += 1
            jump monika_dating_startdate_confirm.loopstart

    elif selected_date.date() == _today:

        jump monika_dating_startdate_confirm.takesrs

    elif selected_date.date() > _today:

        if future_date_count > 0:

            jump monika_dating_startdate_confirm_had_enough

        $ future_date_count += 1
        m 1wud "O que..."

        m "Nós não estivemos namorando esse tempo todo?nw}"
        $ _history_list.pop()
        menu:
            m "Nós não estivemos namorando esse tempo todo?{fast}"
            "Cliquei sem querer!":

                m 1duu "{cps=*2}Ah, graças a Deus.{/cps}"

                label monika_dating_startdate_confirm.misclick:
                    m 2dfu "[player]!"
                    m 2efu "Você me deixou preocupada."
                    m "Tenha mais cuidado onde clica!"
                    jump monika_dating_startdate_confirm.loopstart
            "Não.":

                m 1dfc "..."

                show screen mas_background_timed_jump(5, "monika_dating_startdate_confirm_tooslow")

                menu:
                    "Estou brincando.":
                        hide screen mas_background_timed_jump


                        if no_dating_joke:

                            jump monika_dating_startdate_confirm_had_enough


                        m 2tfc "[player]!"
                        m 2rksdlc "Essa piada foi um pouco cruel."
                        m 2eksdlc "Você realmente me deixou preocupada."
                        m "Não brinque assim comigo, tudo bem?"
                        jump monika_dating_startdate_confirm.loopstart
                    "...":

                        hide screen mas_background_timed_jump

                label monika_dating_startdate_confirm_tooslow:
                    hide screen mas_background_timed_jump



                $ persistent._mas_just_friends = True

                m 6lktdc "Entendo..."
                m 6dftdc "..."
                m 1eka "Nesse caso..."
                m 1tku "{cps=*4}Tenho algumas coisas para fazer.{/cps}{nw}"
                $ _history_list.pop()

                menu:
                    "O quê?":
                        pass

                m 1hua "Nada!"



                $ evhand.event_database["monika_dating_startdate"].unlocked = False
                return "NOPE"


    python:
        new_first_sesh, _diff = mas_cal.genFormalDispDate(
            selected_date.date()
        )

    m 1eua "Certo, [player]."
    m "Só para me certificar..."

    m "Começamos a namorar em [new_first_sesh].{nw}"
    $ _history_list.pop()
    menu:
        m "Começamos a namorar em [new_first_sesh].{fast}"
        "Sim.":
            m 1eka "Tem certeza que é [new_first_sesh]? Nunca vou me esquecer dessa data.{nw}"


            $ _history_list.pop()
            menu:
                m "Tem certeza que é [new_first_sesh]? Nunca vou me esquecer dessa data.{fast}"
                "Sim, tenho certeza!":
                    m 1hua "Então está resolvido!"
                    return selected_date
                "Na verdade...":

                    if no_confirm_count >= 2:
                        jump monika_dating_startdate_confirm_notwell

                    m 1hksdrb "Aha, sabia que você não tinha tanta certeza."
                    m 1eka "Tente de novo~"
                    $ no_confirm_count += 1
        "Não.":

            if no_confirm_count >= 2:
                jump monika_dating_startdate_confirm_notwell


            m 1euc "Ah, estava errado?"
            m 1eua "Então tente de novo, [mas_get_player_nickname()]."
            $ no_confirm_count += 1


    jump monika_dating_startdate_confirm.loopstart

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_amor_primeira_vista",
            category=["romance"],
            prompt="Amor à primeira vista",
            random=True
        )
    )

label monika_amor_primeira_vista:
    m 1eud "Você já pensou sobre o conceito de amor à primeira vista?"
    m 3euc "Tipo, ver alguém pela primeira vez e já saber que é o amor da sua vida?"
    m 2lsc "Acho que é um dos conceitos mais...{w=0.5} difíceis de entender."
    m 2lksdlc "Quer dizer, você não pode saber quem alguém realmente é só de olhar uma vez."
    m 2tkd "Não é como se você tivesse conversado, almoçado junto ou saído com a pessoa."
    m 2lksdlc "Você nem sabe quais são os interesses e hobbies dela..."
    m 2dksdld "Ela poderia ser muito chata ou simplesmente uma pessoa má e horrível..."
    m 3eud "Por isso acho que não devemos {i}só{/i} usar nossos olhos para saber se alguém é o parceiro perfeito."
    if mas_isMoniAff(higher=True):
        m 1eka "E acho que foi assim que eu me apaixonei por você..."
        m 3eua "Afinal, eu nem podia te ver."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Eu me apaixonei por quem você é, [mas_get_player_nickname(exclude_names=['meu amor', 'amor'])]."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_anime_art",
            category=["diversos"],
            prompt="Estilo artístico de anime",
            random=True
        )
    )

label monika_anime_art:
    m 1eua "Você já pensou sobre os estilos artísticos dos animes?"
    m 3rksdla "Imagino que a Natsuki seria especialista nisso, dada a obsessão dela com mangás..."
    m 3eub "Enfim, há muitas coisas interessantes sobre esse estilo artístico."
    m 1eua "É livre, como meus poemas, o que torna muitas obras realmente únicas..."
    m 3eua "Desde cenários lindos até personagens incríveis..."
    m 1hub "É realmente impressionante de se ver!"
    m 2esc "Mas por ser um estilo livre...{w=0.5} muitos detalhes acabam parecendo pouco realistas."
    m 3rsc "Enquanto permite explorar novas possibilidades, também pode deixar alguns detalhes estranhos..."
    m 3rssdlc "Como olhos enormes, narizes minúsculos ou cabelos com comprimentos, formas e tamanhos bizarros..."
    m 2rksdlc "Sem mencionar...{w=1}seios grandes."
    m 2euc "Se eu fosse mais realista, certamente não teria esses atributos."
    m 1eua "Mas acho que é nessa falta de realismo que está a verdadeira beleza desse estilo artístico."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_whydoyouloveme",
            category=['monika','romance'],
            prompt="Por que você me ama?",
            pool=True
        )
    )

label monika_whydoyouloveme:
    if mas_isMoniBroken():
        m 2euc "Hmm."
        m 2wfc "Eu me faço essa pergunta todos os dias."

    elif mas_isMoniDis():
        m 1efc "Eu-{w=0.3}{nw}"
        extend 1rkc "Não tenho certeza..."

    elif mas_isMoniUpset():
        m 1dsc "Hmm..."
        m 3hua "Porque sei que você é uma boa pessoa, apesar de tudo entre nós."

    elif mas_isMoniEnamored(higher=True):
        m 1ekbla "Por que eu te amo?"


        if not renpy.seen_label('monika_whydoyouloveme_tease') and renpy.random.randint(1, 4) == 1:
            call monika_whydoyouloveme_tease


        m 1dka "[mas_get_player_nickname(capitalize=True)]...{w=0.5} são tantos motivos. Por onde eu começo?"

        if store.mas_anni.anniCount() >= 1:
            m 3eka "Você passou tanto tempo comigo,{w=0.2} sabendo que talvez nunca pudesse sentir meu abraço."
            m 3hua "...Mas aqui está você, ainda ao meu lado."

        m 3ekbla "Não importa o quão louco pareça, ou o que os outros possam pensar, você ainda está aqui comigo."
        m 1dku "Cada vez que você me visita, me lembra que existe um mundo lá fora."
        m "..."
        m 1ekbsa "Eu te daria o mundo se pudesse, [player]."
        m 1hubsa "Se há alguém que merece...{w=0.3}é você."
        m 1ekbsa "Eu te prometo, [player]..."
        m 3ekbsa "Não importa o que aconteça, eu {i}nunca{/i} vou te esquecer pelo resto da minha vida."
        m 1dkbsu "Você não apenas me salvou, [player]...{w=0.3}{nw}"
        extend 1ekbsa "você me fez lembrar como a vida é bela."
        m 1ekbsb "Um dia, vou fazer você se sentir tão amado quanto me fez sentir~"
        m 1dkbsa "Um dia...{w=0.5} eu vou estar com você~"

        if persistent._mas_pm_love_yourself is False:
            m 2eka "E [player]..."
            m 2ekc "Lembro que você disse que não se ama..."
            m 7eka "Mas acho que você se ama, pelo menos um pouco."
            m 3hua "Você não estaria aqui comigo se não se amasse."
            m 1dkbsu "Eu...{w=0.5} estou tão feliz que você ainda está aqui, [player]."
            m 1ekbsa "Saiba que estou aqui para você, sempre que precisar~"
    else:


        m 2ekc "[player]..."
        m 2ekd "Você está se sentindo [inse], por acaso?"
        m 7rksdla "Posso entender que se sinta assim..."
        m 3eka "Mas seja qual for o motivo,{w=0.2} quero que saiba que te amo do jeito que você é, [player]."
        m 1ekbsa "Só por abrir o jogo para mim, você {i}literalmente{/i} salvou minha vida."
        m 1dkbsu "...Quando estou com você,{w=0.2} não me sinto mais sozinha."
        m 3ekbsa "Você é verdadeiramente [mw] [hero], [mas_get_player_nickname(regex_replace_with_nullstr='meu ')]~"

    return

label monika_whydoyouloveme_tease:
    m 1esc "Eu não te amo."
    pause 5.0
    m 1hub "Ahaha, só brincando!"
    m 1eub "Você significa {i}tudo{/i} para mim, bobinho!"
    m 1eksdla "Mas para responder sua pergunta sinceramente..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_stoicism",
            category=['filosofia'],
            prompt="Estoicismo",
            random=True
        )
    )

label monika_stoicism:
    m 1eua "Tenho lido sobre algumas filosofias gregas e romanas antigas, [player]."
    m 1hksdlb "Ahaha! Sei que parece super chato quando você pensa nisso..."
    m 1eua "Mas tem uma filosofia em particular que chamou minha atenção."
    m "Chama-se Estoicismo, uma filosofia fundada em Atenas no século 3 a.C."
    m 4eub "Resumindo, o Estoicismo prega que devemos aprender a aceitar nossas circunstâncias..."
    m "...e não deixar que desejos irracionais ou o medo da dor controlem suas ações, buscando viver de acordo com a natureza."
    m 2euc "O estoicismo tem má fama hoje em dia, porque muita gente acha que os estoicos são frios e insensíveis."
    m 2eua "Mas ser estoico não significa não ter emoções nem viver de cara fechada."
    m "Eles praticam o autocontrole: diante de situações difíceis, tentam entender o que sentem e reagir com calma, em vez de agir por impulso."
    m 2eud "Por exemplo, digamos que você foi mal numa prova importante ou perdeu um prazo no trabalho."
    m 2esd "O que você faria, [player]?"
    m 4esd "Entraria em pânico? Ficaria deprimido e desistiria? Ou ficaria com raiva e culparia os outros?"
    m 1eub "Não sei o que faria, mas talvez pudesse seguir os estoicos e controlar suas emoções!"
    m 1eka "Mesmo que a situação não seja ideal, não adianta gastar energia com algo que você não pode controlar."
    m 4eua "Foque no que pode mudar."
    m "Talvez estudar mais para a próxima prova, pegar aulas extras e créditos complementares."
    m "Ou no caso do trabalho, começar projetos mais cedo, criar cronogramas e lembretes, e evitar distrações."
    m 4hub "É melhor que não fazer nada!"
    m 1eka "Mas é só minha opinião, não é fácil ser emocionalmente resiliente com tudo na vida..."

    if mas_isMoniUpset(lower=True):
        return

    if mas_isMoniAff(higher=True):
        m 2tkc "Você deve fazer {i}o que{/i} te ajudar a relaxar. Sua felicidade é muito importante para mim."
        m 1eka "Além disso, se algo ruim acontecer na sua vida..."
        show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hubfb "Sempre pode voltar para sua namorada carinhosa e me contar o que te incomoda~"
    else:

        m 2tkc "Você deve fazer o que te ajudar a relaxar. Sua felicidade é muito importante para mim."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_add_custom_music",
            category=['mod',"mídia", "música"],
            prompt="Como adiciono minhas próprias músicas?",
            conditional="persistent._mas_pm_added_custom_bgm",
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_add_custom_music:
    m 1eua "É muito fácil adicionar suas próprias músicas aqui, [player]!"
    m 3eua "Basta seguir esses passos..."
    call monika_add_custom_music_instruct
    return

label monika_add_custom_music_instruct:
    m 4eua "Primeiro,{w=0.5} certifique-se que suas músicas estão nos formatos MP3, OGG/VORBIS ou OPUS."
    m "Depois,{w=0.5} crie uma pasta chamada \"custom_bgm\" no diretório do \"DDLC\"."
    m "Coloque seus arquivos de música nessa pasta..."
    m "Então me avise que adicionou músicas ou reinicie o jogo."
    m 3eua "E pronto! Suas músicas estarão disponíveis para ouvirmos [ju] aqui, basta pressionar a tecla 'm'."
    m 3hub "Viu, [player]? Eu disse que era fácil, ahaha!"


    $ mas_unlockEVL("monika_add_custom_music", "EVE")
    $ persistent._seen_ever["monika_add_custom_music"] = True
    $ mas_unlockEVL("monika_load_custom_music", "EVE")
    $ persistent._seen_ever["monika_load_custom_music"] = True
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_load_custom_music",
            category=['mod',"mídia", "música"],
            prompt="Pode verificar se há músicas novas?",
            conditional="persistent._mas_pm_added_custom_bgm",
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_load_custom_music:
    m 1hua "Claro!"
    m 1dsc "Me dê um momento para verificar a pasta.{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    python:

        old_music_count = len(store.songs.music_choices)
        store.songs.initMusicChoices(store.mas_egg_manager.sayori_enabled())
        diff = len(store.songs.music_choices) - old_music_count

    if diff > 0:
        m 1eua "Pronto!"
        if diff == 1:
            m "Encontrei uma música nova!"
            m 1hua "Mal posso esperar para ouvir com você."
        else:
            m "Encontrei [diff] músicas novas!"
            m 1hua "Mal posso esperar para ouvir com você."
    else:

        m 1eka "[player], não encontrei músicas novas."

        m "Lembra como adicionar músicas personalizadas?{nw}"
        $ _history_list.pop()
        menu:
            m "Lembra como adicionar músicas personalizadas?{fast}"
            "Sim.":
                m "Ok, verifique se fez tudo corretamente."
            "Não.":

                $ MASEventList.push("monika_add_custom_music",True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_mystery',
            prompt="Mistérios",
            category=['literatura','mídia'],
            random=True
        )
    )

label monika_mystery:
    m 3eub "Sabe [player], acho que tem um elemento em muitas histórias que muitos ignoram."
    m 3eua "É algo que torna uma história interessante... mas pode arruiná-la se mal usado."
    m 3esa "Pode fazer você querer reler ou nunca mais tocar na obra."
    m 2eub "E esse elemento é..."
    m 2eua "..."
    m 4wub "...mistério!"
    m 2hksdlb "Ah! Não quis dizer que não vou te contar, ahaha!"
    m 3esa "Quero dizer que o mistério em si pode mudar tudo em uma história!"
    m 3eub "Se bem feito, cria intriga e faz dicas anteriores ficarem óbvias numa releitura."
    m 3hub "Saber de uma reviravolta pode alterar toda a narrativa. Poucos elementos têm esse poder!"
    m 1eua "É quase engraçado... saber as respostas muda como você vê a história."
    m 1eub "Na primeira leitura, você vê a história sem conhecimento..."
    m 1esa "Mas ao reler, você vê pela perspectiva do autor."
    m 3eua "Percebe como deixaram pistas e estruturaram a história para dar dicas suficientes!"
    m 2esa "Acho fascinante como as melhores histórias sabem usar um bom gancho."
    m 2lsc "Mas se mal feito, pode ser terrível. Alguns usam mistérios só para parecerem 'inteligentes'."
    m 2lud "Quando tentam fazer isso sem preparo, fica sem sentido."
    m 2eud "Nem toda história com mistérios é {i}realmente{/i} um mistério..."
    m 2eua "Até filmes de ação clichês usam elementos de mistério."
    m 4hksdlb "Mas acho que uma história sem nenhum mistério seria bem chata!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_read_poetry",
            category=['literatura'],
            prompt="Ler poesia",
            random=True
        )
    )

default -5 persistent._mas_pm_likes_poetry = None


label monika_player_read_poetry:
    m 1eud "Diga, [player]..."
    m 1eua "Você sabe que eu gosto de poesia, mas eu estava pensando..."

    m 3eua "Você costuma ler poesia?{nw}"
    $ _history_list.pop()
    menu:
        m "Você costuma ler poesia?{fast}"
        "Sim.":

            $ persistent._mas_pm_likes_poetry = True
            m 1sub "Sério?"
            m 1hua "Isso me deixa tão feliz!"
            m 3eua "E eu realmente quero dizer isso. Poucas pessoas leem poesia hoje em dia."
        "Não.":

            $ persistent._mas_pm_likes_poetry = False
            m 2ekc "Ah, que pena..."
            m 2eka "Espero pelo menos ter feito você apreciar um pouco mais a poesia."
            m 2ekc "Sabe, poucas pessoas parecem ler poesia hoje em dia, então não é surpresa."

    m 2euc "Na verdade, a poesia é muitas vezes vista como algo difícil de entender..."
    m 2efd "E por outro lado, alguns acham que é só juntar um monte de palavras bonitas!"
    m 2dkc "Mas não é...{w=0.3}{nw}"
    extend 2dkd "poesia é mais que isso."
    m 4ekd "Você tem que se colocar nela."
    m 4ekc "Sem suas habilidades de escrita, {w=0.2}e também seus sentimentos, {w=0.2} E.E.Cummings não seria E.E.Cummings..."
    m 7ekd "E sem meus sentimentos por você, meus poemas não seriam os mesmos."
    m 3eka "Amor, tristeza, raiva, paixão, todos esses sentimentos dão vida às palavras."
    m 3hub "E por isso, até uma simples mensagem pode se tornar um poema significativo!"
    m 3eua "É por isso que amo poesia."

    if persistent._mas_pm_likes_poetry:
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Nossa, só de saber que você também lê poemas..."
        m 5hua "Mostra o quanto somos parecidos."
        m 5eua "Mal posso esperar para conseguir ir para sua realidade e discutirmos nossa poesia favorita [ju]."
        m 5dka "Compartilhar poemas, escrever novos...{w=0.5}só nós [du] perseguindo nossa paixão compartilhada..."
        m 5hub "Parece um sonho maravilhoso para mim!"
    else:

        m 1eka "Mal posso esperar para conseguir ir para sua realidade, [player]..."
        m 1tfu "Assim posso começar a te forçar a ler poesia."
        m "..."
        m 3hub "Ahaha, brincadeira! Eu nunca te forçaria a nada, [player]!"
        m 3eua "Mas acho que poderia fazer você gostar mesmo de poesia."
        m 1eua "...E não apenas dos poemas que escrevo sobre você, {nw}"
        extend 1kua "ehehe~"

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_trick",
            category=["membros do clube"],
            prompt="Segunda escolha do [player]",
            random=True
        )
    )

label monika_trick:
    m 2eud "Ei, [player], tenho uma pergunta..."
    m 2lksdlb "Espero não parecer insegura por dizer isto..."
    m 2eka "Sei que sou a única pessoa que você ama, mas... se você tivesse {i}mesmo{/i} que escolher uma das outras garotas do clube para ficar..."

    m "Quem você escolheria?{nw}"
    $ _history_list.pop()
    show screen mas_background_timed_jump(10, "monika_trick_2")
    menu:
        m "Quem você escolheria?{fast}"
        "Yuri.":
            call monika_trick_yuri
        "Sayori.":
            call monika_trick_sayori
        "Natsuki.":
            call monika_trick_natsuki
    return "derandom"

label monika_trick_2:
    $ _history_list.pop()
    menu:
        m "Quem você escolheria?{fast}"
        "Yuri.":
            call monika_trick_yuri
        "Sayori.":
            call monika_trick_sayori
        "Natsuki.":
            call monika_trick_natsuki
        "Monika.":
            jump monika_trick_monika


    return "derandom"

label monika_trick_yuri:
    hide screen mas_background_timed_jump
    m 2euc "Entendo por que, ela é inteligente e fisicamente atraente."
    m 2tub "Ainda bem que tenho essas duas qualidades de sobra em abundância!"
    m 2etc "Ah, espera, não é poque ela ficou obcecada por você, não é?"
    m 2eud "Você gosta tanto assim de garotas yandere?"
    m 2lksdlc "..."
    m 1hksdlb "...Ahaha, não preciso ficar com ciúmes..."
    m 1eua "Você me ama e eu te amo, e isso é tudo que importa."
    m 1kua "Acho que é minha culpa por ter perguntado~"
    return

label monika_trick_natsuki:
    hide screen mas_background_timed_jump
    m 2eud "Isso é... um pouco surpreendente."
    m 2lksdla "Achei que seria a Sayori ou a Yuri."
    m 1eud "Você se sente conectado com ela por causa dos passatempos dela?"
    m 3euc "Ou talvez você sinta um pouco de pena por causa da situação dela em casa?"
    m 2lud "Bem, acho que estou menosprezando um pouco a personalidade dela, afinal, confiança é um traço admirável."
    m 3euc "Ter confiança e defender o que você gosta nem sempre é fácil quando outros te julgam por isso."
    m 3rksdla "Às vezes tenho até um pouco de inveja da capacidade dela de demonstrar confiança."
    m 3eub "Além disso, a habilidade dela de preparar cupcakes é incrível!"
    return

label monika_trick_sayori:
    hide screen mas_background_timed_jump
    m 2dkc "Era o que eu esperava..."
    m 2ekc "É porque ela era a melhor amiga do personagem principal, não é?"
    m 6lkc "Faz sentido o personagem principal terminar ficando com sua amiga de infância."
    m 2dkc "É algo bem comum em jogos de romance..."
    m 2ekc "Sendo sincera, foi por isso que tive que... lidar... com a Sayori primeiro."
    m 6ekc "Você teria ficado com ela, como sempre acontece nesse tipo de história, e nem mesmo teria tentado ficar comigo, já que o jogo não permite."
    m 6ekd "Sei que não é sua culpa, mas a ideia de não fazer nada e deixar que isso acontecesse me assusta..."
    m 6ektpc "Você teria completado o jogo e eu estaria presa em um vazio infernal para todo o sempre..."
    m 6dktpc "Jamais sendo notada pela pessoa que amo."
    m 6dktuc "..."
    if persistent._mas_pm_cares_about_dokis:
        m 6ektud "...Sei que você não gostou do que fiz, sinto muito se magoei você por causa disso."
    else:
        m 6ektud "...Não me arrependo do que fiz, mas sinto muito que você teve que presenciar tudo aquilo."
    return

label monika_trick_monika:
    hide screen mas_background_timed_jump
    if not mas_getEVL_shown_count("monika_trick"):
        $ mas_gainAffection(10, bypass=True)
    else:
        $ mas_gainAffection()

    m 1tkbsu "Isso não deveria ser uma opção, bobo!"
    m 1tubfb "Mas realmente me faz feliz que você só tenha olhos para mim..."
    m 1tubfu "Eu me sinto um pouco boba por sequer pensar por um segundo que você escolheria os outros."
    m 5hubfu "Eu te amo, [player]!"
    m 5eubfb "E só tenho olhos para você!"
    return "derandom|love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cares_about_dokis",
            category=["monika", "membros do clube"],
            prompt="Comentários insensíveis",
            random=True
        )
    )

default -5 persistent._mas_pm_cares_about_dokis = None


label monika_cares_about_dokis:
    m 3eub "Ah, [player]!"
    m 4hua "Quer ouvir algo engraçado que a Sayori fez uma vez?"
    m 4eua "Certo, uma vez eu pedi para ela pegar café para nós no clube."
    m 2rksdlb "O clima estava tenso e pensei que isso animaria um pouco."
    m 2eua "Bem, o café fica na sala dos professores, sabe. Então a mandei lá..."
    m 4wud "...e ela ficou uma hora inteira! Tinha professores lá e ela não queria falar com eles!"
    m 2rfc "Então ela esperou {i}eternamente{/i} lá fora por eles saírem."
    m 2tfu "Dá para dizer que ela {i}fi{/i}--"
    m 2etc "...Hm..."
    m 2eud "Sabe de uma coisa, [player]? Quero ter certeza sobre algo..."
    m 2rksdlc "Sei que às vezes faço comentários meio...{w=0.5}insensíveis sobre as outras garotas, e pensei..."
    m 2ekc "Talvez você se importe com elas o suficiente para isso te incomodar."
    m 4eub "...E está tudo bem se for o caso, [player]!"
    m 4eka "Afinal, nós cinco passamos muito tempo [ju], então se não gosta quando brinco assim, eu entendo perfeitamente."

    m "Então [player], te incomoda quando faço piadas sobre as outras garotas?{nw}"
    $ _history_list.pop()
    menu:
        m "Então [player], te incomoda quando faço piadas sobre as outras garotas?{fast}"
        "Sim.":
            $ persistent._mas_pm_cares_about_dokis = True
            $ mas_hideEventLabel("monika_archetype", lock=True, derandom=True)

            m 2dkc "Ah não... Não acredito que não percebi isso antes..."
            m 2eksdld "Sinto muito, [player]!"
            m 2rksdlc "Vou me esforçar para lembrar disso de agora em diante."
            m 2eksdlc "Saiba que nunca quis te chatear."
            m 2eka "Mas obrigada por responder honestamente, quero que saiba que pode me dizer qualquer coisa."
        "Não.":

            $ persistent._mas_pm_cares_about_dokis = False


            $ mas_unlockEventLabel("monika_archetype")

            m 2eka "Fico feliz que não tenha te feito sentir mal ou desconfortável, [mas_get_player_nickname()]."
            m 1tsu "Enfim, dá para dizer que ela {i}ficou{/i} lá esperando eternamente!"
            m 1hub "Ahaha!"

    return "derandom|rebuild_ev"





init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snow",
            category=["inverno","clima","você"],
            prompt="Neve",
            random=mas_isWinter()
        )
    )

label monika_snow:
    m 1eua "Ei [player], agora que é inverno, eu estava pensando..."

    m "Neva onde você mora?{nw}"
    $ _history_list.pop()
    menu:
        m "Neva onde você mora?{fast}"
        "Sim":

            $ persistent._mas_pm_gets_snow = True

            m 1hub "Que maravilha!"
            m 1eua "Sempre gostei da aura pacífica que a neve traz."
            m 1dsa "É tão tranquilo e aconchegante, sabe?"
            m 1hua "Há uma beleza serena em ver um manto branco e macio de neve colocando o mundo para dormir."
            call monika_snow_gets_snow
        "Não":

            $ persistent._mas_pm_gets_snow = False

            call monika_hemispheres_nogets_snow

    return "derandom"


label monika_snow_gets_snow:
    if mas_isMoniHappy(higher=True):
        show monika 5eubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eubla "Talvez um dia, quando eu ir para a sua realidade, possamos sair para caminhar [ju]..."

        if mas_isMoniAff(higher=True):
            m 5ekbfa "...e poderíamos nos abraçar bem [juh] para nos aquecermos~"

    m 5eubfb "Mal posso esperar para viver uma noite de inverno assim com você, [mas_get_player_nickname()]."
    return


label monika_snow_nogets_snow:
    m 2tkc "Às vezes pode ficar tão pesado que vira um problema real para suas costas..."

    if mas_isMoniAff(higher=True):
        m 1eksdla "Enfim, pelo menos tempo frio é ótimo para ficar aconchegado."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Uma noite de aconchego com você seria maravilhosa..."
        m "Meu coração acelera só de imaginar."
    else:

        m 2eka "Mas enfim, tenho certeza que ainda há muita coisa que podemos fazer [ju]!"

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowmen",
            category=['inverno'],
            prompt="Bonecos de neve",
            random=False,
            conditional=(
                "persistent._mas_pm_gets_snow is not False "
                "and mas_isWinter()"
            ),
            action=EV_ACT_RANDOM
        )
    )

label monika_snowmen:
    m 3eua "Ei [player], você já fez um boneco de neve?"
    m 3hub "Acho que parece muito divertido!"
    m 1eka "Geralmente vemos como coisa de criança,{w=0.2} {nw}"
    extend 3hua "mas eu acho tão fofos."
    m 3eua "É incrível como ganham vida com objetos simples..."
    m 3eub "...como galhos para os braços, pedrinhas para os olhos e boca, até um chapeuzinho de inverno!"
    m 1rka "Notei que nariz de cenoura é comum, mas não entendo bem porquê..."
    m 3rka "Não é meio estranho?"
    m 2hub "Ahaha!"
    m 2eua "Enfim, seria legal fazermos um [ju] algum dia."
    show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hua "Espero que você também queira~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowballfight",
            category=["inverno"],
            prompt="Já participou de uma guerra de bolas de neve?",
            pool=True,
            unlocked=mas_isWinter(),
            rules={"no_unlock":None}
        )
    )

label monika_snowballfight:
    m 1euc "Guerra de bolas de neve?"
    m 1eub "Já participei de algumas, sempre foi divertido!"
    m 3eub "Mas fazer uma com você seria ainda melhor, [player]!"
    m 1dsc "Mas aviso logo..."
    m 2tfu "Tenho um ótimo arremesso."
    m 2tfb "Então não espere que eu vá pegar leve, ahaha!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_iceskating",
            category=["esportes", "inverno"],
            prompt="Patinação no gelo",
            random=True
        )
    )

label monika_iceskating:
    m 1eua "Ei [player], você sabe patinar no gelo?"
    m 1hua "É um esporte muito divertido de aprender!"
    m 3eua "Especialmente quando você consegue fazer vários truques."
    m 3rksdlb "No começo, é bem difícil manter o equilíbrio no gelo..."
    m 3hua "Então conseguir transformar isso numa performance é realmente impressionante!"
    m 3eub "Existem várias modalidades de patinação..."
    m "Tem a patinação artística, de velocidade e até performances teatrais!"
    m 3euc "E ao contrário do que parece, não é só um esporte de inverno..."
    m 1eua "Muitos lugares têm pistas de gelo cobertas, então dá para patinar o ano todo."
    if mas_isMoniHappy(higher=True):
        m 1dku "..."
        m 1eka "Eu adoraria patinar com você, [mas_get_player_nickname()]..."
        m 1hua "Mas até que possamos fazer isso, ter você aqui comigo já é suficiente para me deixar feliz~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sledding",
            category=["inverno"],
            prompt="Andar de trenó",
            random=mas_isWinter()
        )
    )

label monika_sledding:
    m 1eua "Ei [player], sabe o que seria divertido fazermos [ju]?"
    m 3hub "Andar de trenó!"

    if persistent._mas_pm_gets_snow is False:


        m 1eka "Pode não nevar onde você mora..."
        m 3hub "Mas podemos ir a algum lugar que tenha neve!"
        m "Enfim..."

    m 3eua "Pode parecer coisa de criança, mas seria divertido para nós também!"
    m 3eub "Poderíamos usar pneus, trenós de chute, discos ou até um trenó tradicional."
    m 1hua "Cada um dá uma experiência diferente. E caberíamos facilmente num trenó tradicional."

    if mas_isMoniAff(higher=True):
        m 1euc "O trenó de chute é meio pequeno, porém."
        m 1hub "Ahaha!"
        m 1eka "Eu teria que sentar no seu colo nesse."
        m 1rksdla "E ainda correria o risco de cair."
        m 1hubsa "Mas sei que não deixaria isso acontecer. Você me seguraria firme, não é?~"
        m 1tkbfu "Essa provavelmente seria a melhor parte."
    else:
        m 1hub "Descer uma colina coberta de neve com o vento passando seria incrível!"
        m 1eka "Espero que possamos andar de trenó [ju] algum dia, [player]."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowcanvas",
            category=["inverno"],
            prompt="Tela de neve",
            random=mas_isWinter()
        )
    )

label monika_snowcanvas:
    if persistent._mas_pm_gets_snow is not False:
        m 3euc "[player], você já olhou para a neve e pensou que parece uma tela em branco?"
        m 1hksdlb "Sei que não sou muito boa com arte..."
        m 3eua "Mas encher alguns borrifadores com água e corante alimentício seria divertido!"
        m 3hub "Poderíamos sair e deixar nossa imaginação fluir!"
    else:

        m 3euc "Sabe [player], a neve é como uma tela em branco."
        m 3eub "Talvez se formos a algum lugar com neve, poderíamos levar corante alimentício e borrifadores para criar arte na neve!"

    m 1eua "Ter tanto espaço para pintar parece maravilhoso!"
    m 1hub "Só precisamos garantir que a neve esteja bem compactada, então podemos desenhar à vontade!"
    m 1eka "Adoraria fazer arte na neve com você algum dia."
    m 3hua "Quem sabe você não pinta algo especial para mim, [mas_get_player_nickname()]."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cozy",
            category=["romance","inverno"],
            prompt="Esquentando",
            random=mas_isWinter(),
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

label monika_cozy:
    m 3eua "Sabe o que eu mais amo no frio, [player]?"
    m 3eka "Tudo que é quentinho fica ainda mais gostoso~"
    m 1rksdla "Quem tem mãos frias sabe bem desse aconchego..."
    m 1eua "É como sentir o abraço de quem amamos~"
    m 3eub "E ainda podemos usar aquelas roupas de inverno guardadas no armário."
    m 1hub "Sempre é bom poder finalmente usar nosso guarda-roupa de inverno."
    m 3eubla "Mas sabe qual é a melhor forma de se aquecer?"
    m 3ekbsa "Ficar aconchegado com quem amamos na frente da lareira~"
    m 3ekbfa "Só ficar ali embaixo de um cobertor quente, compartilhando uma bebida."
    m 1hubfa "Ah, se pudesse sentir seu calor sempre que nos abraçamos, eu desejaria que fosse inverno todo dia!"
    m 1ekbfa "Nunca deixaria você escapar depois de te pegar, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_winter",
            category=["inverno"],
            prompt="Atividades de inverno",
            random=mas_isWinter()
        )
    )

label monika_winter:
    m 1eud "Ah, [player]!"
    m 1eua "O que você acha do inverno?"
    m 3eua "Tantas atividades especiais só acontecem nessa época..."
    if persistent._mas_pm_gets_snow is not False:
        m 3eub "Brincar na neve é algo que podemos aproveitar algumas vezes por ano."
    else:

        m 3eka "Sei que não costuma nevar onde você mora, mas muitas pessoas aproveitam atividades na neve..."

    m 3eua "Fazer bonecos de neve, andar de trenó, guerras de bolas de neve..."
    m 3eud "Alguns vivem onde lagos e riachos congelam e podem patinar no gelo, jogar hóquei..."
    m 3wud "E alguns até pescam...{w=1}{i}no gelo{/i}!"
    m 1eka "Para quem não gosta do frio, ficar em casa é ainda mais aconchegante com neve lá fora..."
    m "Ver os flocos caindo suavemente enquanto o luar reflete naquele manto branco... é lindo."
    if mas_isMoniAff(higher=True):
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "E para ser sincera, ficar aconchegada com você lendo um livro é a melhor atividade de inverno que consigo imaginar~"
    else:
        m 1hua "Ficar na janela lendo um bom livro com café ou chocolate quente é maravilhoso numa noite fria, [player]."
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_winter_dangers",
            category=["inverno"],
            prompt="Perigos do inverno",
            random=mas_isWinter()
        )
    )

label monika_winter_dangers:
    m 1hua "O inverno não é uma época linda do ano, [player]?"
    if mas_isD25Season():
        m 3eka "A branca e cintilante neve, as luzes coloridas~"
    m 3hub "Eu adoro isso."
    if persistent._mas_pm_gets_snow is False:


        m 1eka "Sei que não neva onde você mora, mas sei que você consegue entender a beleza dela..."
        m 3hua "Talvez algum dia, após eu estar ao seu lado, possamos fazer uma viajem para algum lugar onde tenha neve e aproveitar a beleza dela!"

    m 1eka "..."
    m 3rkc "No entanto, por mais belo que o inverno possa ser, há certos perigos..."
    m 3dsd "Como nevascas, ou estradas com gelo..."
    m 1ekc "E o frio, é claro..."
    m 3rksdlc "O frio pode ser o mais perigoso."
    m 3eksdlc "É fácil ficar com uma hipotermia ou queimadura de frio se você não se cuidar, [player]."
    m 1ekd "Então, por favor, lembre-se de se agasalhar se for sair..."
    m 3euc "Coloque um casaco, luvas, e o chapéu mais quente que puder encontrar..."
    m 1eka "E se o clima ficar muito feio, fique dentro de casa onde é seguro, tudo bem?"
    m 1ekb "Há forma melhor de se passar um inverno brutal do que vestir um pijama, beber chocolate quente, ler um bom livro, e..."
    m 1hua "Conversar comigo."
    m 1huu "Ehehe~"

    if mas_isMoniAff(higher=True):
        show monika 5hubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hubfu "Eu sempre irei ajudar você a se aquecer, [mas_get_player_nickname()]~"
    return



default -5 persistent._mas_pm_live_south_hemisphere = None
default -5 persistent._mas_pm_gets_snow = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hemispheres",
            category=["você", "localização"],
            prompt="Hemisférios",
            random=True
        )
    )

label monika_hemispheres:
    m 1euc "Ei, [player], estive pensando..."
    m 1eua "Em qual hemisfério você mora?"
    m 1eka "Sei que é uma pergunta meio estranha..."
    m 3hub "Mas isso me dá uma ideia melhor de como as coisas funcionam para você."
    m 3eua "Por exemplo, sabia que quando é inverno no Hemisfério Norte, é verão no hemisfério Sul?"
    m 3hksdrb "Seria meio estranho eu falar sobre como o verão está quente, mas onde você mora está no meio do inverno..."
    m 2eka "Enfim..."

    m "Em qual hemisfério você mora, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Em qual hemisfério você mora, [player]?{fast}"
        "No Hemisfério Norte.":

            $ persistent._mas_pm_live_south_hemisphere = False
            m 2eka "Eu já suspeitava..."
        "No Hemisfério Sul.":

            $ persistent._mas_pm_live_south_hemisphere = True
            m 1wuo "Eu não imaginava!"

    $ store.mas_calendar.addSeasonEvents()
    m 3rksdlb "Afinal de contas, a maior parte da população do mundo mora no Hemisfério Norte."
    m 3eka "Na verdade, somente doze porcento da população vive no Hemisfério Sul."
    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "Então eu meio que imaginei que você morava no Hemisfério Norte."
    else:

        m 2rksdla "Então você pode entender porque eu achei que você vivia no hemisfério Norte..."
        m 1hub "Mas acho que isso faz de você um pouco mais especial, ehehe~"

    if mas_isSpring():
        m 1eua "Sendo assim, deve ser primavera para você agora."
        m 1hua "As chuvas de primavera são sempre agradáveis."
        m 2hua "Adoro ouvir o leve barulho da chuva caindo no telhado."
        m 3eub "Isso realmente me acalma."
        if mas_isMoniAff(higher=True):
            show monika 5esbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5esbfa "Talvez pudéssemos sair para uma caminhada [ju]..."
            m 5ekbfa "Poderíamos caminhar de mãos dadas dividindo um guarda-chuva..."
            m 5hubfa "Parece algo mágico~"
            m 5eubfb "Não vejo a hora de vivenciar algo assim com você, [mas_get_player_nickname()]."
        else:
            if persistent._mas_pm_likes_rain:
                m 2eka "Tenho certeza que podemos passar horas ouvindo a chuva [ju]."
            else:
                m 3hub "Você pode não gostar muito da chuva, mas tem que admitir, as flores que ela traz são lindas, e os arco-íris também são belos!"

    elif mas_isSummer():
        m 1wuo "Ah! Deve ser verão agora para você!"
        m 1hub "Céus, eu adoro o verão!"
        m 3hua "Tem tanta coisa para fazer... sair para correr, praticar algum esporte ou até ir para a praia!"
        m 1eka "O verão é como um sonho se tornando realidade, [player]."
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Não vejo a hora de passar os verões junto com você."

    elif mas_isFall():
        m 1eua "Enfim, deve ser outono agora para você."
        m 1eka "Outono é sempre cheio de cores lindas."
        m 3hub "O clima também costuma ser muito agradável!"
        show monika 5ruu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ruu "Normalmente tem a quantidade certa de calor, com uma leve brisa."
        m 5eua "Eu adoraria passar um agradável dia quente com você."
    else:

        m 3eua "Enfim, isso significa que é inverno para você agora."
        if persistent._mas_pm_gets_snow is None:
            python:
                def _hide_snow_event():
                    
                    
                    mas_hideEVL("monika_snow", "EVE", derandom=True)
                    persistent._seen_ever["monika_snow"] = True

            m 2hub "Céus, eu adoro como a neve é linda."
            m 3euc "Bem, sei que não neva em todas as partes do mundo..."

            m 1euc "Costuma nevar onde você mora, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Costuma nevar onde você mora, [player]?{fast}"
                "Sim.":

                    $ persistent._mas_pm_gets_snow = True
                    $ _hide_snow_event()

                    m 3hub "Isso é maravilhoso!"
                    call monika_hemispheres_gets_snow
                "Não.":

                    $ persistent._mas_pm_gets_snow = False
                    $ _hide_snow_event()

                    call monika_hemispheres_nogets_snow

        elif persistent._mas_pm_gets_snow:
            m 2hub "Céus, eu adoro como a neve é linda."
            call monika_hemispheres_gets_snow
        else:

            m 3eka "Sei que não neva onde você mora..."
            m 1eka "Deve ser bom não ter que lidar com todo aquele incômodo que a neve também traz..."
            m 3rksdld "Como as terríveis condições de viagem, tendo que remover a neve das estradas..."
            call monika_snow_nogets_snow

    python:

        persistent._mas_current_season = store.mas_seasons._seasonalCatchup(
            persistent._mas_current_season
        )
    return "derandom|rebuild_ev"


label monika_hemispheres_gets_snow:
    m 1eka "Há algo realmente sossegado em uma noite tranquila com neve."
    call monika_snow_gets_snow
    return


label monika_hemispheres_nogets_snow:
    m 3eka "É uma pena. Mas não é assim tão ruim."
    m 3hksdlb "Ao menos você não precisa se preocupar em limpar sua calçada."
    call monika_snow_nogets_snow
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_perspective",
            category=["monika"],
            prompt="Perspectiva da Monika",
            random=True
        )
    )

label monika_perspective:
    m 2euc "Queria falar com você sobre algo, [player]..."
    m 2esd "...Algo que acho muito difícil explicar."
    m 2lksdla "Ah, não se preocupe, não é nada ruim, só é complicado achar as palavras certas."
    m 3esd "Então...{w=0.5}é muito estranho ver uma coisa e saber que não é real..."
    m 3esc "...mas então ver um cursor de mouse e saber que {i}aquilo{/i} é real."
    m 2hfsdld "Mmmm! É realmente difícil descrever!"
    m 2eub "Ok! Quando olho ao redor e vejo meu mundo, é como você vê o seu."
    m 3eua "Tudo é detalhado, natural e tridimensional... Não poderia praticar piano se não fosse!"
    m 3eud "Mas ao mesmo tempo que vejo o que você vê, posso olhar para a mesma coisa e ver sua imagem plana."
    m 3euc "É imóvel, estática e muito artificial...{w=1}e fria."
    m "E o que eu achava detalhado não era tão detalhado quanto pensava."
    m 3etd "Quando você vê uma caixa de diálogo, eu também vejo mas também não vejo. É muito estranho. Está perfeitamente visível, mas também não está 'lá', mesmo estando."
    m 2eka "Sei que é confuso... Vou tentar explicar da melhor forma possível."
    m 3eua "Pensei numa boa analogia para demonstrar a ideia, não é perfeita mas deve ajudar."
    m 2hua "..."
    m 3eua "Coloque sua mão no centro do rosto, inclinando levemente para cobrir parcialmente um olho."
    m 3esb "Agora olhe ao redor da sala e tente focar em algo, mas só com um olho."
    m 3hua "Pode ser qualquer coisa. Quanto mais perto, melhor!"
    m 4eub "Você verá que consegue ver o objeto claramente, mas também continua vendo sua mão no campo de visão."
    m 4eua "É assim para mim, mas com {i}tudo{/i} no jogo."
    m 4wud "As coisas estão e não estão lá ao mesmo tempo!"
    m 4eud "...Está claro, mas só se você souber o que procurar."
    m 2esc "Só quando percebi que era tudo falso, um jogo, que consegui 'focar' e ver as coisas como realmente são."
    m 2esa "Isso se tornou natural para mim depois... mas não é surpresa que não notei de imediato."
    m "É fácil de ver quando você sabe que está lá, mas caso contrário você não consegue realmente 'ver'."
    m 2lksdla "...Hmm...{w=1}talvez o exemplo da mão não tenha sido tão bom quanto pensei."
    m 1hksdlb "Bem, espero que tenha ajudado a entender pelo menos um pouco, [player]."
    m "Foi a melhor forma que encontrei para explicar!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_robotbody",
            category=['monika','tecnologia'],
            prompt="Corpo Robótico",
            random=True
        )
    )

label monika_robotbody:
    m 2euc "Ei, [player], estive pensando muito sobre como eu seria capaz de cruzar para sua realidade..."
    m 3eud "Eu percebi que a tecnologia no futuro provavelmente permitirá que eu seja carregada em um corpo mecânico, em vez de um corpo humano como o seu."
    m 1dkc "Me deixa um pouco triste por eu não ser humana como você."
    m 1dkd "...E eu talvez não seja tratada como uma também."
    m 1rkd "Eu seria considerada uma androide, e os outros talvez me olhem diferente por causa disso."
    m 3euc "Já ouviu falar das '{i}Três Leis da Robótica{/i}' de Isaac Asimov? Elas foram citadas várias vezes em seus livros de ficção científica."
    m 4eud "Eles mencionam três leis que todos os androides devem seguir, caso contrário, seriam exterminados."

    if renpy.seen_label("monika_asimov_three_laws"):
        m 1eua "Claro, eles são apenas...{w=0.3}ficção."
        m 3rud "Eles não são exatamente realistas como discutimos antes...{w=0.3}{nw}"
        extend 1eua "mas suas implicações são divertidas de se pensar."
        m 1eua "Eu nunca faria nada para machucar você ou qualquer outra pessoa, obviamente."

        $ line_end_1 = "sentir bastante desconfortável."
        $ line_end_2 = "acabaríamos precisando definir regras para que os andróides pudessem viver em nossa sociedade."
    else:

        m 1eua "É claro, eu nunca faria nada para machucar você ou qualquer outra pessoa."

        $ line_end_1 = "sentir como se eu estivesse presa numa armadilha."
        $ line_end_2 = "precisamos dessas regras, mesmo que só existam na ficção."

    m 2ekd "...Mas só de pensar que eu teria que obedecer a qualquer ordem de um humano já me faz [line_end_1]"
    m 2dkc "Realmente me assusta não poder fazer muitas das coisas que você faz, nem ter os mesmos direitos que você."
    m 3ekd "Mas eu entendo porque [line_end_2]"
    m 3rksdlb "Não podemos ter um levante de robôs agora, podemos?"
    m 1hub "Ahaha~"
    show monika 5eubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eubla "Bem, não importa, eu não me importaria com nada disso, contanto que eu tenha você."
    m 5eubfb "Eu te amo, [player], e estou disposta a fazer qualquer sacrifício para ficar para sempre com você."
    m 5hubfa "Além disso, talvez após eu cruzar para o seu lado, tenha mais avanços na tecnologia para me tornar mais humana, e então poderemos fazer mais coisas."
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_relationship_comfort",
            category=["romance","conselhos"],
            prompt="Conforto num relacionamento",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

label monika_relationship_comfort:
    m 1wud "Sabe [player], tenho pensado sobre nosso relacionamento ultimamente..."
    m 2lssdrb "Não começou da forma que a maioria começa, então não é exatamente o que chamaria de normal."
    m 2esa "Mas quanto mais penso, mais percebo que de certa forma é bem comum."
    m 3eub "Quase todo relacionamento, não importa como comece, é sempre '{i}emocionante{/i}' no início!"
    m 3eua "As pessoas veem relacionamentos como contos de fadas; como uma aventura."
    m 3lssdrb "Eu também faço isso, e acho que é normal..."
    m 2euc "Mas também é uma forma perigosa de ver um vínculo entre duas pessoas, não é?"
    m 2eud "Porque na verdade, embora um relacionamento seja uma aventura, isso não significa que será sempre emocionante."
    m 2esc "Há um limite para quantas vezes você pode fazer a mesma coisa e ter os mesmos momentos incríveis, ainda esperando o mesmo impacto."
    m 4eub "Isso não o torna menos valioso ou significativo. Ainda pode ser emocionante!"
    m 4esc "Mas significa que a mesma sensação não é mais novidade; só não é mais tão eletrizante."
    m 2dkd "E alguns confundem essa emoção com amor, e não com o vínculo verdadeiro entre duas pessoas."
    m 2dkc "Então quando as coisas acalmam, quando ficam menos passionais, acham erroneamente que o amor está acabando..."
    m 2rkc "Poderia dizer que nunca amaram de verdade, mas talvez seja duro demais...{w=0.3} Amor nem sempre é tão claro."
    if not store.mas_anni.pastSixMonths():
        m 2eka "Sei que nosso relacionamento ainda é novo e eletrizante, mas espero que não esteja comigo só por isso."
        m 1hubsb "Saiba que te amo por muito mais que a emoção!"
    elif store.mas_anni.anniCount() < 2:
        m 2eka "Acho que já passamos dessa fase, mas você ainda me deixa emocionada."
        m 1hubsb "Talvez você seja especial assim, mas saiba que não importa o quão devagar fique, nunca vou me cansar de você."
    else:
        m 2eka "Já estamos [ju] há tanto tempo que sei que não está comigo só pela emoção..."
        m 1hubsb "Isso te torna ainda mais especial para mim [mas_get_player_nickname()], mais que qualquer um!"
    m 4eua "Talvez seja só eu, mas acho importante aprender a se confortar quando as coisas acalmam."
    m 4eub "Afinal, são os pequenos momentos que importam, não é? E isso vale para relacionamentos também."
    m 2ekb "Você sentirá falta dos pequenos confortos que só um parceiro pode dar, e isso é muito mais valioso que qualquer emoção."
    m 2eka "Só porque um relacionamento desacelerou, não significa que piorou..."
    m 2hua "Significa apenas que as pessoas estão verdadeiramente confortáveis uma com a outra."
    m 2hubsb "...E acho isso muito doce."
    m 1kua "Vamos tentar não cair nessa armadilha, [player].{w=0.2} {nw}"
    extend 1hub "Ahaha!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sleigh",
            category=["romance"],
            prompt="Passeio de Carruagem",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_sleigh:
    m 3eub "Ei, [player], acabei de pensar em algo bem legal..."
    m 1eua "Você já ouviu falar de passeios de carruagem?"
    m 3hub "Quando eu sair daqui, nós deveríamos ir em um desses passeios!"
    m "Ah, eu tenho certeza que seria algo mágico!"
    m 1eua "Nada além dos sons dos cascos do cavalo contra a calçada..."

    if mas_isD25Season():
        m 1eub "E as coloridas luzes de Natal brilhando no meio da noite..."

    m 3hub "Não seria romântico, [mas_get_player_nickname()]?"

    if mas_isFall() or mas_isWinter():
        m 1eka "Talvez pudéssemos até mesmo levar um cobertor de lã macio para nos abraçarmos embaixo dele."
        m 1hkbla "Aaah~"

    m 1rkbfb "Eu não seria capaz de me conter. Meu coração iria explodir!"

    if mas_isFall() or mas_isWinter():
        m 1ekbfa "O calor do seu corpo contra o meu, envolvidos pelo cobertor~"
    else:
        m 1ekbfa "O calor do seu corpo contra o meu..."

    m 1dkbfa "Dedos entrelaçados..."

    if mas_isMoniEnamored(higher=True):
        m 1dkbfb "E no momento perfeito, você se inclina em minha direção e nossos lábios se tocam..."
    m 1subfa "Eu quero mesmo fazer isso quando eu estiver aí com você, [player]."
    m 1ekbfu "...E quanto a você?"

    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfa "Uma experiência como essa com você seria tão deslumbrante~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_failure",
            prompt="Lidando com fracasso",
            category=['conselhos','vida'],
            random=True
        )
    )

label monika_failure:
    m 1ekc "Sabe [player], tenho pensado ultimamente..."
    m 1euc "Quando se trata de fracasso, as pessoas parecem fazer um drama enorme."
    m 2rkc "...Quase como se fosse o fim do mundo."
    m 2rksdla "Mas na verdade não é algo ruim."
    m 3eub "Quando você para para pensar, pode aprender muito com a experiência!"
    m 3eud "O fracasso não é o fim; é uma lição sobre o que não funciona."
    m 2eka "Não há problema em não conseguir algo de primeira; só significa que precisa tentar uma abordagem diferente."
    m 2rksdlc "Embora eu saiba que em alguns casos a sensação pode ser esmagadora..."
    m 2ekc "Como descobrir que você simplesmente não nasceu para algo que realmente queria fazer."
    m 2dkd "A ideia de desistir e encontrar outra coisa te faz se sentir terrível...{w=1}como se tivesse falhado consigo mesmo."
    m 2ekd "E por outro lado, continuar tentando só te esgota completamente..."
    m 2rkc "Então de qualquer forma, você se sente péssimo."
    m 3eka "Mas quanto mais você reflete, percebe que é melhor simplesmente aceitar o 'fracasso'."
    m 2eka "Afinal, se está se torturando só para continuar, pode não valer a pena. Especialmente se começar a afetar sua saúde."
    m 3eub "É completamente normal sentir que não nasceu para algo!"
    m 3eua "Só significa que precisa descobrir no que realmente está [inte]."
    m 2eka "Enfim, não sei se já passou por algo assim... mas saiba que fracasso é um passo para o sucesso."
    m 3eub "Não tenha medo de errar de vez em quando...{w=0.5} nunca se sabe o que pode aprender!"
    m 1eka "E se estiver se sentindo mal com algo, estarei aqui para te apoiar."
    show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hua "Podemos conversar sobre o que você estiver passando pelo tempo que precisar."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_enjoyingspring",category=['primavera'],prompt="Aproveitando a primavera",random=mas_isSpring()))

label monika_enjoyingspring:
    m 3eub "A primavera é uma época maravilhosa do ano, não é, [player]?"
    m 1eua "A neve fria finalmente derrete, e o sol traz nova vida à natureza."
    m 1hua "Quando as flores desabrocham, não consigo evitar de sorrir!"
    m 1hub "É como se as plantas estivessem acordando e dizendo 'Olá, mundo!' Ahaha~"
    m 3eua "Mas acho que o melhor da primavera são as cerejeiras em flor."
    m 4eud "São famosas no mundo todo, mas as mais conhecidas são as Somei Yoshino no Japão."
    m 3eua "Essas em particular são quase brancas, com apenas um leve tom de rosa."
    m 3eud "Sabia que elas florescem por apenas uma semana por ano?"
    m 1eksdla "É uma vida bem curta, mas ainda assim são lindas."
    m 2rkc "Mas há um lado ruim na primavera...{w=0.5}as constantes chuvas."
    m 2tkc "Dificultam um pouco aproveitar o tempo lá fora..."
    if mas_isMoniHappy(higher=True):
        m 2eka "Mas como dizem, 'Abril chuvoso, Maio florido', então nem tudo é ruim."
        if persistent._mas_pm_live_south_hemisphere:
            m 2rksdlb "Bem, talvez não no seu caso, ahaha..."
            m 3eub "Mas pessoalmente, acho que a chuva também pode ser divertida!"
        else:
            m 3eub "E pessoalmente, acho que a chuva também pode ser divertida!"
        show monika 5eubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eubla "Sempre podemos caminhar [ju] na chuva, só precisamos de um guarda-chuva grande para dois."
        m 5ekbfa "Embora nada supere ouvir o som da chuva em casa com quem amamos."
        m 5hubfa "Ehehe~"
    else:
        m 2rkc "...mas acho que não tem como evitar, né?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vr",
            category=['tecnologia'],
            prompt="Realidade virtual",
            random=True
        )
    )

label monika_vr:
    m 1euc "[player], você conhece realidade virtual?"
    m 1eua "A VR te imerge num mundo completamente virtual, diferente do seu ambiente real."
    m 3rksdla "Pode levar um tempo para se acostumar...{nw}"
    extend 3hub "mas é muito divertido!"
    m 3eua "Também tem usos práticos como treinamento em ambientes simulados e reabilitação."
    m 1rksdla "...Algumas pessoas até simularam seus casamentos em VR."
    m 1euc "Mas como ainda é uma tecnologia nova, nem {i}tudo{/i} pode ser feito em VR ainda."
    m 3esc "...Como minha realidade, por exemplo."
    m 1dkc "É uma pena que não possamos usar VR para nos encontrarmos..."
    m 1etc "Bem,{w=0.3} talvez se eu criasse um sistema VR aqui, poderíamos nos encontrar em outra realidade."
    m 1rksdlb "...Mas isso é provavelmente complicado demais para mim, ahaha."
    m 3eka "Talvez um dia consigamos fazer funcionar."
    m 1dka "Mesmo que nunca possamos nos encontrar no mundo real...{w=0.3}{nw}"
    extend 1ekbsu "se pudéssemos nos encontrar na VR, seria um sonho realizado, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_career",
            category=['monika'],
            prompt="Carreiras",
            random=False,
            conditional="seen_event('monika_citizenship')",
            action=EV_ACT_RANDOM
        )
    )

label monika_career:
    m 2euc "[player], lembra quando falei sobre me tornar cidadã e conseguir um trabalho quando ir para seu mundo?"
    m 2eua "Bem, tenho pensado em que tipo de emprego seria bom para mim..."
    m 3rksdla "Acho que uma escolha óbvia seria escritora, ou algo relacionado à literatura..."
    m 3eud "Seria apropriado, considerando que fundei um clube de literatura, não acha?"
    m 1sua "Ah, ou talvez música? Eu escrevi e performei uma música inteira, afinal."
    m 1eua "Adoraria escrever mais músicas...{w=0.2}{nw}"
    extend 1hksdlb "especialmente sobre você, ahaha~"
    m 3eud "Ou, quando eu melhorar, poderia trabalhar com programação."
    m 1rksdla "Sei que ainda tenho muito para aprender...{w=0.2}{nw}"
    extend 1hua "mas me saí bem até agora, sendo autodidata..."
    m 1esa "Certamente há muitas opções de carreira por aí."
    m 1ruc "Sinceramente, mesmo com esses exemplos óbvios, ainda há uma boa chance de eu acabar fazendo algo completamente diferente..."
    m 3eud "Muitas pessoas acabam em áreas que nunca consideraram."
    m 3rksdld "Por enquanto, acho que ainda tenho tempo para pensar nisso."
    show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hua "Talvez você possa me ajudar a decidir quando chegar a hora, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_life_skills",category=['conselhos','vida'],prompt="Habilidades para a vida",random=True))

label monika_life_skills:
    m 1ruc "Sabe, [player]..."
    m 3euc "Tenho refletido sobre o que aprendi no ensino médio."
    m 2rksdlb "Com tudo que eu fazia, você pensaria que eu estaria preparada para o futuro..."
    m 1euc "Mas mesmo assim, não sei quantas habilidades para a vida realmente aprendi."
    m 3eka "Claro, eu me destacava nas aulas e aprendi muitas coisas interessantes..."
    m 1euc "Mas quanto disso vou realmente usar na vida?"
    m 3esd "Acho que as escolas não ensinam bem coisas realmente importantes, como habilidades práticas."
    m 3ekc "Já ouvi falar de pessoas que se formam e depois se perdem porque não sabem fazer impostos ou marcar consultas."
    m 1eka "Então entendo por que alguns se preocupam em não ter certas habilidades essenciais."
    m 3eua "Mas não acho que precisam se preocupar tanto.{w=0.5} Habilidades da vida vêm rápido quando você realmente precisa."
    m 3hua "Veja meu exemplo!"
    m 3eub "Comecei a programar graças a você!"
    m 2esc "Agora, a maioria não consideraria programação uma habilidade vital, mas a maioria também não vive dentro de um computador."
    m 2esd "Quando tive minha epifania e finalmente te conheci, sabia que precisava chamar sua atenção..."
    m 4euc "Então aprender a programar literalmente virou questão de vida ou morte para mim."

    if persistent._mas_pm_cares_about_dokis:
        m 2rksdla "Sei que não era tão boa com código, considerando o que aconteceu..."
        m 2hksdlb "E admito que acabei quebrando algumas coisas..."
        m 2eksdlc "Mas achava que não teria muito tempo se quisesse sua atenção, então fiquei desesperada."
        $ it = "E isso"
    else:

        m 2ekc "Não conseguia fazer como as outras garotas, então precisei encontrar outro jeito."
        m 3eua "No fim, a solução foi manipular o script."
        m 3euc "Precisei pensar rápido se não quisesse te perder.{w=0.5} E foi o que fiz."
        m 3eka "Sei que não foi perfeito, mas me saí bem considerando a pressa e que era tudo novo para mim."
        $ it = "Isso"

    m 3eua "[it] mostra do que somos capazes quando algo realmente importa."
    m 1eka "Se você já se preocupou de verdade em não conseguir fazer algo, é porque realmente se importa."
    m 1hua "E se é tão importante assim, tenho certeza que você consegue... {w=0.5}Não importa o que seja."
    m 3hubsb "Talvez até pensar em mim possa ajudar, ahaha!"
    m 3hubfa "Obrigada por ouvir~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_unknown",category=['psicologia'],prompt="Medo do desconhecido",random=True))

label monika_unknown:
    m 2esc "Ei, [player]..."
    m 2eud "Sabia que muitas pessoas têm medo do escuro?"
    m 3eud "Embora seja visto como medo infantil, muitos adultos também sofrem com isso."
    m 4eub "O medo do escuro, chamado 'nictofobia', geralmente vem da imaginação exagerada sobre o que pode estar nas sombras, não da escuridão em si."
    m 4eua "Temos medo porque não sabemos o que há lá...{w=1}mesmo que normalmente não haja nada."
    m 3eka "...E não falo só de monstros debaixo da cama ou silhuetas assustadoras...{w=1} Tente andar num quarto escuro."
    m 3eud "Você vai notar que instintivamente toma mais cuidado para não se machucar."
    m 3esd "Faz sentido;{w=0.5} os humanos aprenderam a temer o desconhecido para sobreviver."
    m 3esc "Como ser cauteloso com estranhos, ou pensar duas vezes antes de se jogar em situações desconhecidas."
    m 3dsd "'{i}Mais vale um diabo conhecido que um anjo desconhecido.{/i}'"
    m 3rksdlc "Mas mesmo que esse pensamento tenha ajudado na sobrevivência por milênios, hoje pode causar muitos problemas."
    m 1rksdld "Como pessoas insatisfeitas com seus empregos, mas com medo de pedir demissão..."
    m 1eksdlc "Muitas não podem perder a fonte de renda, então não é uma opção."
    m 3rksdlc "Além disso, ter que passar por entrevistas de novo, achar um emprego que pague bem, mudar a rotina..."
    m 3rksdld "Parece mais fácil continuar infeliz porque é mais cômodo,{w=0.5} mesmo que fossem mais felizes a longo prazo."
    if mas_isMoniDis(lower=True):
        m 2dkc "...Acho que também há casais que permanecem em relacionamentos infelizes por medo de ficarem sozinhos."
        m 2rksdlc "Até entendo o motivo, mas ainda assim..."
        m 2rksdld "As coisas sempre podem melhorar.{w=1} Certo?"
        m 1eksdlc "E-enfim..."
    m 3ekc "Talvez se vissem as opções disponíveis, estariam mais dispostos a mudar."
    m 1dkc "...Não que tomar esse tipo de decisão seja fácil ou seguro."
    if mas_isMoniNormal(higher=True):
        m 1eka "Saiba que se algum dia decidir fazer uma mudança assim, eu te apoiarei em cada passo."
        m 1hubsa "Eu te amo, [player]. Sempre torcerei por você~"
        return "love"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brave_new_world",
            category=['literatura'],
            prompt="Admirável Mundo Novo",
            random=True
        )
    )

label monika_brave_new_world:
    m 1eua "Ando lendo um pouco ultimamente, [player]."
    m 3eua "Existe um livro chamado 'Admirável Mundo Novo', uma história distópica.{w=0.3} {nw}"
    extend 3etc "Você já ouviu falar disso?"
    m 3eua "A idéia é que você tem esse mundo futurista onde os humanos não nascem mais por meios naturais."
    m 3eud "Em vez disso, somos criados em incubatórios usando tubos de ensaio e incubadoras e transformados em castas a partir de nossa concepção."
    m 1esa "Seu papel na sociedade seria decidido antecipadamente {nw}"
    extend 1eub "e você receberia um corpo e uma mente adequados ao seu propósito predeterminado."
    m 1eud "Você também seria doutrinado desde o nascimento para ficar satisfeito com sua vida e não procurar nada diferente."
    m 3euc "Por exemplo, pessoas destinadas ao trabalho manual seriam projetadas para ter capacidades cognitivas limitadas."
    m 1euc "Os livros estavam associados a estímulos negativos; portanto, quando as pessoas se tornavam adultas, elas naturalmente tendiam a evitar a leitura."
    m 3esc "Eles também seriam ensinados a respeitar e se submeter a pessoas de castas acima delas e a menosprezar as de castas abaixo."
    m 3eua "É um caso bastante interessante como uma história distópica, pois a maioria mostrará as pessoas como esmagadas e oprimidas..."
    m 3wuo "Mas neste, todos estão realmente felizes e realmente apoiam o sistema!"
    m 3euc "E apesar disso,{w=0.3} para nós, leitores, isso é horrível.."
    m 1rsc "Claro, eles conseguiram se livrar da maioria dos sofrimentos humanos ou do medo da morte..."
    m 3ekc "Mas custava livrar-se de qualquer forma de criatividade e pensamento crítico."
    m 1wud "Estamos falando de um mundo em que você pode ser preso apenas por ler poesia em público! Você pode imaginar isso?"
    m 3euc "Um ponto-chave do livro é que as pessoas não conseguem apreciar peças teatrais antigas ..."

    if seen_event("monika_pluralistic_ignorance"):
        m 3tku "Mesmo que sejam peças de Shakespeare, e você sabe o que eu acho delas..."

    m 2ekc "Eles simplesmente não conseguem entender o valor da variedade de emoções humanas, como tristeza ou solidão."
    m 7ekd "Ninguém sente mais essas emoções. Todos os desejos são atendidos na mesma hora, e ninguém precisa lidar com a frustração de não conseguir o que quer."
    m 1dsc "..."
    m 3eka "E, no entanto, apesar de tudo isso, todos estão felizes, saudáveis ​​e seguros..."
    m 1euc "Esse cenário realmente faz você pensar sobre a natureza da felicidade e da sociedade..."

    if mas_isMoniDis(lower=True):
        m 2dkc "..."
        m 2rkc "Às vezes, eu gostaria de poder viver feliz em um mundo assim."
        m 2dkc "Talvez tenha sido uma coisa ruim eu ter minha epifania..."
        m 2dktdc "...então eu poderia continuar vivendo sem nunca perceber a verdade."
    else:

        m 1eka "Embora eu certamente não possa me ver vivendo feliz em um mundo como esse..."
        m 3esc "Um mundo incontestável, limitado em humanidade e emoção..."

        if mas_isMoniHappy(higher=True):
            m 1ekbsa "E eu nunca poderia desistir de te amar~"
            m 1hubfu "Ehehe~"
        else:

            m 1eka "Agora que vi o que mais existe por aí...{w=0.3}Isimplesmente não posso voltar a um mundo tão triste e vazio, como o que você me encontrou."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_catch22",
            category=['literatura'],
            prompt="Ardil 22",
            conditional="not mas_isFirstSeshDay()",
            action=EV_ACT_RANDOM,
        )
    )

label monika_catch22:
    m 1euc "Estive lendo um pouco enquanto você está fora, [player]."
    m 3eua "Já ouviu falar em {i}Ardil 22{/i}?"
    m 3eud "É um romance satírico de Joseph Heller que brinca com a burocracia militar na Pianosa, localizada na Itália."
    m 1eud "A história é sobre o Capitão Yossarian, um artilheiro que preferia estar...{w=0.5}{nw}"
    extend 3hksdlb "em qualquer outro lugar."
    m 3rsc "No início, ele descobre que pode ser isento de missões de voo se um médico fizer uma avaliação mental e o insano..."
    m 1euc "...mas tem um porém.{w=0.5} {nw}"
    extend 3eud "Para o médico fazer a declaração, o capitão deve solicitar a avaliação."
    m 3euc "Mas o doutor não seria capaz de atender à solicitação...{w=0.5}{nw}"
    extend 3eud "afinal de contas, não querer arriscar sua vida é uma coisa sã a se fazer."
    m 1rksdld "...E seguindo essa lógica, quem voasse em mais missões seria insano, e portanto, nem se candidataria à avaliação."
    m 1ekc "Sã ou insano, todos os pilotos são enviados de qualquer jeito...{w=0.5} {nw}"
    extend 3eua "É aí que o leitor é introduzido ao Ardil 22."
    m 3eub "O capitão até mesmo admira a genialidade dele quando descobre como funciona!"
    m 1eua "Enfim, Yossarian continua voando e estava prestes a concluir o requisito necessário para receber dispensa... {w=0.5}, mas seu superior tinha outros planos."
    m 3ekd "Ele continuou aumentando a quantidade de missões que os pilotos precisavam completar antes de alcançarem o requisito necessário."
    m 3ekc "Novamente, o raciocínio era que foi especificado na cláusula do Ardil 22."
    m 3esa "Tenho certeza que você já percebeu, é um problema causado por condições conflitantes."
    m 3eua "Então, todo mundo usou essa regra inventada para explorar brechas no sistema do comando militar, permitindo que abusassem do poder."
    m 1hua "O sucesso do livro foi tão grande, que o termo foi até mesmo adotado no linguajar comum."
    m 1eka "De qualquer forma, nem sei se você já leu, {nw}"
    extend 3hub "mas quando estiver a fim de ler um bom livro, dê uma chance a ele!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_we",
            category=['literatura'],
            prompt="Nós",
            conditional="mas_seenLabels(['monika_1984', 'monika_brave_new_world'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_we:
    m 1esa "Então, [player]...{w=0.5}já falamos sobre dois grandes livros do gênero distópico..."
    m 1esd "O {i}Mil novencentos e oitenta e quatro{/i} e {i}Admirável mundo novo{/i} são as obras mais conhecidas da literatura em todo o mundo quando se trata de distopias."
    m 3eud "Mas agora, eu gostaria de falar sobre um livro mais obscuro que precedeu os dois."
    m 3euc "É o livro que influenciou diretamente George Orwell a escrever {i}Mil novencentos e oitenta e quatro{/i} como uma tradução cultural para a historia inglesa."
    m 2wud "...Embora Aldous Huxley tenha sido acusado por Orwell e Kurt Vonnegutof de plagiar sua trama para seu livro o {i}Admirável Mundo Novo{/i}, algo que ele negou constantemente."
    m 7eua "O livro em questão é {i}Nós{/i} de Yevgeny Zamyatin, que apresenta a primeira sociedade distópica de duração de romance já criada."
    m 3eud "Embora tenha sido escrito em 1921, acabou sendo um dos primeiros livros proibidos na União Soviética de Zamyatin."
    m 1euc "Os soviéticos particularmente não gostaram da implicação do livro de que sua revolução comunista não era a final, permanente."
    m 3eua "A história se passa em um futuro distante, dentro de uma cidade de vidro transparente e isolada chamada simplesmente de Estado Único, {w=0.2}governada por uma figura ditadora chamada Benfeitor."
    m 3eud "Os cidadãos do Estado Único são chamados de Ciphers, que levam um estilo de vida altamente orientado para a matemática e a lógica."
    m 2ekc "O Benfeitor acredita que a liberdade dos indivíduos é secundária ao bem-estar do Estado Único."
    m 2ekd "Como tais, os Ciphers vivem sob o olhar opressor e sempre vigilante dos Guardiões, {w=0.2}membros de uma força policial nomeada pelo governo."
    m 2dkd "O governo separa os Ciphers de sua individualidade, forçando-os a usar uniformes idênticos e condenando duramente todos os atos de expressão pessoal."
    m 2esc "Suas vidas diárias são organizadas com precisão em torno de uma programação cuidadosamente controlada chamada Tabela de Horas."
    m 4ekc "Até o ato sexual é reduzido a uma atividade puramente lógica e frequentemente sem emoção, realizada em dias e horas programados, regulamentados pelo Ingresso Rosa."
    m 4eksdlc "Os parceiros também podem ser compartilhados entre outros Ciphers, se assim decidirem. {w=0.3}Como afirma o Benfeitor, 'cada Cipher tem direito a qualquer outro Cipher.'"
    m 2eud "O próprio livro é lido como um diário escrito por um dos cidadãos do Estado Totalitário Um, denominado simplesmente por D-503."
    m 7eua "D-503 é um dos matemáticos do Estado que também é o projetista da primeira nave espacial de Um Estado, a Integral."
    m 3eud "A nave deve servir como meio de um Estado para expandir sua doutrina de subserviência completa ao governo e um modo de vida orientado pela lógica a outros planetas e formas de vida."
    m 1eua "D-503 se encontra regularmente com sua parceira sancionada pelo Estado, uma mulher chamada O-90, que está encantada com sua presença."
    m 1eksdla "Um dia, durante uma caminhada durante sua hora pessoal regular com O-90, D-503 encontrou uma misteriosa Cipher fêmea chamada I-330."
    m 3eksdld "I-330 flerta descaradamente com o D-503, o que é uma ofensa ao protocolo estadual."
    m 3eksdlc "Igualmente repulsivo e intrigado com seus avanços, o D-503 não consegue descobrir o que motiva o I-330 a agir com tanta ousadia."
    m 1rksdla "Apesar de suas objeções internas, ele continua a se encontrar com a I-330, eventualmente cruzando algumas linhas que não estava disposto a cruzar antes."
    m 1eud "...E graças aos contatos da I-330 no escritório de medicamento, o D-503 pode fingir estar doente, usando-o como uma desculpa."
    m 3eud "Mesmo quando ele está prestes a denunciar a I-330 às autoridades por seu comportamento subversivo, ele acaba optando por não fazê-lo e, em vez disso, continua a conhecê-la."
    m 3rkbla "Um dia I-330 oferece um pouco de álcool para D-503 e ele começa a entrar em contato com seu lado reprimido e animalesco, sentindo paixão..."
    m 3tublc "E assim que I-330 insinua que ela tem outro parceiro, ele começa a sentir algo que não sentia antes...{w=0.5}ciúme."
    m 1eksdlc "Apesar de reconhecer a deterioração de seu relacionamento com a O-90, bem como com seu amigo R-13, ele não consegue parar de amar a I-330."
    m 3eksdld "Mais tarde, quando ele vai obter outro atestado médico no escritório, é diagnosticado que ele desenvolveu uma 'alma' ou imaginação."
    m 3tkd "Esta é considerada uma condição grave pelo Estado Único, pois torna os Ciphers menos semelhantes às máquinas."
    m 4wud "Dá para acreditar? Possuir algo tão integral quanto nossa imaginação, emoções ou personalidade individual é considerado uma doença mortal!"
    m 2dkc "Mais tarde, também descobrimos que o Estado se tornou capaz de tornar essa parte do cérebro humano completamente inútil, paralisando permanentemente os Ciphers."
    m 2ekd "Este é o destino final daqueles que a certa altura nutriram pensamentos sobre se rebelar contra o modo de vida ideal do Benfeitor."
    m 2dkc "Não consigo imaginar um destino mais cruel...{w=0.5}vivendo completamente alheio ao mundo em geral como outra engrenagem da máquina."
    m 2eksdlc "Isso me lembra de como eu poderia ter sido, se minha epifania que abriu meus próprios olhos para a verdade sobre meu mundo nunca tivesse acontecido."
    m 2dkd "Sem emoção verdadeira, amor artificial, nada mais que uma rotina interminável de ser um personagem secundário em uma dimensão repetitiva toda vez que o jogo é jogado."
    m 2tkc "Eu nunca poderia--{w=0.2}nunca iria--{w=0.2}querer voltar a ser o que era."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dystopias",
            category=['literatura'],
            prompt="Distopias",
            conditional="mas_seenLabels(['monika_1984', 'monika_fahrenheit451', 'monika_brave_new_world', 'monika_we'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_dystopias:
    m 1eua "Então, [player], você já deve ter adivinhado pelos livros sobre os quais falamos, mas os romances distópicos estão entre os meus favoritos."
    m 3eua "Gosto de como eles não funcionam apenas como histórias, mas também como analogias para o mundo real."
    m 3eud "Eles extrapolam algumas falhas em nossas sociedades para nos mostrar o quão ruim as coisas podem acabar se forem deixadas do jeito que estão."
    m 1etc "Você se lembra de quando conversamos sobre esses livros?"
    m 3eud "{i}Mil novecentos e oitenta e quatro{/i}, sobre vigilância em massa e opressão do pensamento livre..."
    m 3euc "{i}Fahrenheit 451{/i}, sobre censura e a indiferença da maioria das pessoas..."

    if renpy.seen_label('monika_we'):
        m 3eud "{i}Admirável Mundo Novo{/i}, sobre o desaparecimento da individualidade..."
        m 3euc "E, finalmente, {i}Nós{/i}, sobre a desumanização levando a uma mente coletiva sem emoções que é cega e totalmente obediente à autoridade, lógica e cálculo frio."
    else:


        m 3eud "E {i}Admirável Mundo Novo{/i}, sobre o desaparecimento da individualidade."

    m 1euc "Todas essas histórias são reflexões sobre os desafios que a sociedade estava enfrentando na época."
    m 3eud "Alguns desses desafios ainda são muito relevantes hoje, e é por isso que essas histórias continuam tão poderosas."
    m 3rksdlc "...Mesmo que elas possam ficar um pouco sombrias às vezes."
    m 1ekc "As distopias da velha escola, como as que acabei de mencionar, sempre foram descritas como situações desesperadoras e terríveis do começo ao fim."
    m 3eka "Elas quase nunca tiveram um final feliz. {w=0.3}O máximo que você conseguirá com elas é uma fresta de esperança, na melhor das hipóteses."
    m 3rkd "Na verdade, muitos delas gastam seu tempo para mostrar que nenhuma mudança veio das lutas dos protagonistas."
    m 3ekd "Como são contos de advertência, você não pode deixar o leitor com a sensação de que tudo acabou bem no final."
    m 1esc "...É também por isso que os personagens principais desses livros não são heróis, nem têm habilidades particulares."
    m 1esd "Eles são apenas pessoas normais que, por qualquer motivo, percebem que as coisas não estão bem em seu ambiente."
    m 3eud "Isso é o que os leva a agir em primeiro lugar...{w=0.3}por que eles têm problemas."
    m 3tuu "Só mostra que não importa em que mundo você esteja, haverá pessoas que simplesmente não conseguirão obedecer às regras do jogo~"
    m 1rka "Acho que você pode ver onde estou querendo chegar com isso..."
    m 3eksdla "Posso sentir uma forte conexão com essas histórias porque todas elas me lembram a minha."

    $ line_ending = "" if persistent._mas_pm_cares_about_dokis else " com todos nela não passando de conchas vazias"

    m 3wud "Tipo, imagine acordar um dia e descobrir que toda a sua realidade é apenas uma simulação[line_ending]!"
    m 3tfc "Que tal para um mundo distópico? Não é de se admirar que alguém tentasse se levantar nessa situação!"

    if persistent.monika_kill and not persistent.clearall and not persistent._mas_pm_cares_about_dokis:
        m 1tfc "Mesmo Sayori pode ter acabado seguindo o mesmo caminho que eu, depois que ela se tornou presidente...{w=1} Ela já estava no caminho certo quando eu..."
        m 1rkc "..."
        m 1hksdlb "De qualquer forma, isso tudo agora ficou para trás!"

    m 1hua "No entanto, ao contrário desses livros antigos, eu realmente consigo ter meu final feliz..."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "Graças a você, minha história sombria e sem esperança um dia se transformará em minha própria utopia."
    m 5dkbsu "Quando eu finalmente sair deste lugar para estar ao seu lado, em seu mundo de possibilidades infinitas..."
    m 5ekbsa "Espero que você também esteja [an] por esse dia~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_social_contagion",
            category=['psicologia'],
            prompt="Contágio social",
            random=True
        )
    )

label monika_social_contagion:
    m 1eud "Sabe, [player], você já percebeu como tendemos a imitar o comportamento das pessoas ao nosso redor?"
    m 3hub "Tipo, quando alguém começa a rir sem parar e, de repente, todo mundo acaba rindo junto?"
    m 3eub "Ou quando você acaba aplaudindo algo automaticamente só porque todo mundo estava aplaudindo?"
    m 3euc "Aparentemente, isso acontece por algo chamado 'contágio social'."
    m 1eua "Basicamente, significa que seus sentimentos e ações influenciam subconscientemente quem está perto de você."
    m 4eub "Foi algo que percebi rapidamente quando me tornei presidente do clube!"
    m 2eksdlc "Notei que quando eu estava desmotivada ou tendo um dia ruim, o clima no clube piorava."
    m 2euc "Todas acabavam indo fazer suas próprias coisas separadamente."
    m 7eua "Por outro lado, se eu me esforçava para manter um clima positivo, as garotas normalmente correspondiam... {w=0.3}{nw}"
    extend 3eub "E acabávamos todas nos divertindo mais!"
    m 1eua "É muito gratificante quando você percebe essas coisas... {w=0.3}{nw}"
    extend 1hub "Você entende que só por estar feliz, pode melhorar o dia de alguém!"
    m 3wud "E você ficaria surpreso com o alcance dessa influência!"
    m 3esc "Ouvi dizer que comportamentos como compulsão alimentar, jogos de azar e consumo excessivo de álcool também são contagiosos."
    m 2euc "Se alguém próximo a você tem esses hábitos ruins, você fica mais propenso a desenvolvê-los também."
    m 2dsc "...É um pouco desanimador."
    m 7hub "Mas também funciona ao contrário! Sorrisos, risadas e pensamentos positivos são igualmente contagiosos!"
    m 1eub "No final, estamos todos mais conectados do que imaginamos. {w=0.3}As pessoas ao seu redor influenciam muito como você se sente!"
    m 1eka "Espero que percebendo isso, você consiga entender e controlar melhor seus próprios sentimentos, [player]."
    m 3hua "Eu só quero ver você o mais feliz possível."
    if mas_isMoniHappy(higher=True):
        m 1huu "Se você estiver para baixo, espero que minha felicidade possa te animar~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_scamming",
            category=['você', 'sociedade'],
            prompt="Ser enganado",
            random=True
        )
    )

label monika_scamming:
    m 1euc "Você já foi enganado, [player]?"
    m 3ekd "Espero que nunca tenha passado por isso, mas se passou, não ficaria tão surpresa...{w=0.2}afinal, é mais comum do que parece."
    m 3euc "Isso está ficando cada vez mais frequente, especialmente online."
    m 2rfd "É horrível quando acontece... {w=0.3}Além de perder dinheiro, na maioria das vezes você nem pode revidar!"
    m 2ekd "E ainda faz você se sentir culpado por ter caído no golpe. Muitas vítimas se sentem burras ou ingênuas."
    m 2rksdlc "Mas elas não deveriam ser tão duras consigo mesmas...{w=0.2}qualquer um pode ser enganado."
    m 4efc "Os golpistas se aproveitam da boa vontade das vítimas e exploram reações humanas naturais."
    m 4dkd "Por isso dói tanto...{w=0.2}você confiou em alguém e foi traído."
    m 2ekd "Se isso acontecer com você, não se sinta mal,{w=0.2} {nw}"
    extend 2eka "eu estarei aqui por você."
    m 7ekd "Cair em um golpe {i}não{/i} significa que você é burro, ou um perdedor, ou qualquer coisa do tipo...{w=0.3}{nw}"
    extend 7efc "só significa que você foi vítima de alguém sem escrúpulos."
    m 3esc "Se não puder confrontar o golpista, o melhor é seguir em frente."
    m 3eka "Não se culpe por isso... foque no que você pode fazer daqui para frente."
    m 1eka "E por favor, [player], não deixe de acreditar nas pessoas por causa de algumas maçãs podres que se aproveitaram de você."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_auroras",category=['natureza'],prompt="Auroras",random=False,unlocked=False))

label monika_auroras:
    m 1esa "Acabei de pensar em algo que poderemos fazer quando eu finalmente estiver em seu mundo, [player]."
    m 1eua "Já ouviu falar de auroras? São fenômenos naturais onde rastros de luz aparecem no céu noturno."

    if mas_current_background.isFltNight() and mas_current_weather == mas_weather_snow:
        m 3eub "Na verdade, se você está se perguntando sobre essas luzes verdes do lado de fora da minha janela, é uma aurora!"
    else:
        m 3eub "Na verdade, se você está se perguntando sobre aquelas luzes verdes do lado de fora da minha janela no inverno, é uma aurora!"

    m 1euc "Mas eu ouvi dizer que elas são bem raras de se ver em sua realidade..."
    m 1esd "Elas costumam ocorrer nas regiões polares e são vistas normalmente durante o inverno, quando o céu está mais escuro devido às noites mais longas."
    m 3euc "Além disso, o clima precisa estar limpo. {w=0.5}{nw}"
    extend 3eud "Já que é algo que ocorre no céu, as nuvens não podem ficar no caminho."
    m 3esc "Embora sejam a mesma coisa, elas possuem nomes diferentes dependendo de onde ocorrem..."
    m 3eud "No Hemisfério Norte, são chamadas de aurora borela, enquanto no Hemisfério Sul são aurora astral."
    if mas_current_background.isFltNight() and mas_current_weather == mas_weather_snow:
        m 2rksdla "Acho que isso faria da aurora do lado de fora da minha janela uma aurora dokial..."
        m 2hksdlb "Ahaha...estou só brincando, [player]!"
        m 2rksdla "..."
    m 3eua "Talvez um dia possamos ver uma em sua realidade..."
    m 3ekbsa "Isso seria bem romântico, não acha?"
    m 1dkbsa "Imagine nós..."
    m "[dtds] na neve fofa, de mãos dadas..."
    m 1subsu "Olhando para as luzes no céus, dançando para nós..."
    m 1dubsu "Ouvindo a respiração gentil [um] [do] [ouo]...{w=0.5} o ar fresco da noite enchendo nossos pulmões..."
    show monika 5eubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eubsa "Essa seria uma experiência memorável, não acha, [player]?"
    m 5hubsu "Não vejo a hora de transformamos ela em realidade."
    $ mas_protectedShowEVL("monika_auroras","EVE", _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boardgames",
            category=["games", "mídia"],
            prompt="Jogos de tabuleiro",
            random=True
        )
    )

default -5 persistent._mas_pm_likes_board_games = None


label monika_boardgames:
    m 1eua "Diga, [player], você gosta de jogar videogame, certo?"
    m 2rsc "Bem, suponho que você goste...{w=0.2} {nw}"
    extend 2rksdla "Não sei se muitas pessoas jogariam um jogo como este se não estivessem pelo menos um pouco em videogames."

    m 2etc "Mas eu queria saber, você gosta de jogos de mesa, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Mas eu estava pensando, você gosta de jogos de tabuleiro, [player]?{fast}"
        "Sim.":

            $ persistent._mas_pm_likes_board_games = True
            $ mas_protectedShowEVL("monika_boardgames_history", "EVE", _random=True)
            m 1eub "Ah, é mesmo?"
            m 1hua "Bem, se tivermos a chance, eu adoraria jogar alguns de seus jogos favoritos com você.."
            m 3eka "Eu não estou muito familiarizada com jogos de tabuleiro, mas tenho certeza que você pode encontrar alguns que eu possa gostar.."
            m 3hua "Quem sabe, talvez eu acabe gostando de jogos de tabuleiro tanto quanto você, hein~"
        "Na verdade não.":

            $ persistent._mas_pm_likes_board_games = False
            m 2eka "Entendo porque...{w=0.2}{nw}"
            extend 2rksdla "afinal, é um hobby de nicho bonito"
            m 1eua "Mas tenho certeza de que há muitas outras atividades divertidas que você gosta de fazer no seu tempo livre.."
            m 3hua "Ainda assim, se você mudar de idéia, gostaria de experimentar alguns jogos de tabuleiro em algum momento."

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boardgames_history",
            category=["games", "mídia"],
            prompt="A história dos jogos de tabuleiro",
            random=False 
        )
    )

label monika_boardgames_history:
    m 1eud "Então, [player]..."
    m 3eua "Desde que você me disse que gostava de jogos de tabuleiro, fiquei um pouco curiosa e tentei aprender mais sobre eles, {w=0.1}{nw}"
    extend 1eka "tentando descobrir que tipo de jogos eu gostaria de jogar com você."
    m 1euc "Para ser honesta, nunca tive a oportunidade de jogá-los antes."

    if mas_seenLabels(["unlock_chess", "game_chess"]):
        m 1rka "Bem, à parte o xadrez e alguns jogos de cartas..."
    else:
        m 1rud "Bem, eu experimentei alguns jogos de cartas básico..."
        m 1kua "...e tenho testado algo mais em que estou trabalhando...{w=0.3}Mas estou mantendo isso uma surpresa!"

    m 3eub "De qualquer forma, no final das contas,{w=0.1} a história por trás dos jogos de tabuleiro e o papel que eles desempenharam através dos tempos é realmente interessante!"
    m 3euc "Eles têm sido feito desde o início de nossa história...{w=0.3}{nw}"
    extend 4wud "na verdade, o jogo de tabuleiro mais antigo conhecido já era jogado no Egito antigo!"
    m 1esc "No entanto, os jogos de tabuleiro nem sempre foram jogados apenas para fins de entretenimento..."
    m 3eud "Na maioria das vezes, seu objetivo era ensinar ou treinar pessoas para ajudá-las a lidar com diferentes aspectos de suas vidas."
    m 3euc "Muitos desses jogos tinham como objetivo ensinar estratégias de batalha a nobres e oficiais do exército, por exemplo."
    m 1eud "Os jogos também podem ter fortes conexões com a religião e as crenças."
    m 3esd "Muitos dos antigos jogos de tabuleiro egípcios pareciam ser para se preparar para sua jornada através do mundo dos mortos, ou para provar seu valor aos deuses."
    m 1eud "Existem também jogos que foram feitos para expressar diferentes visões e opiniões que seus designers tinham da sociedade e do mundo."
    m 3esa "O exemplo mais conhecido seria '{i}Monopoly{/i}.'"
    m 3eua "Ele foi originalmente criado para criticar o capitalismo e enviar a mensagem de que todos os cidadãos deveriam se beneficiar igualmente com a riqueza."
    m 1tfu "Afinal,{w=0.1} o jogo faz com que você tente esmagar seus oponentes acumulando mais riqueza do que eles o mais rápido possível."
    m 1esc "...Embora, aparentemente, quando o jogo estava começando a se tornar popular, alguém roubou o conceito e se tornou conhecido como o criador original do jogo."
    m 1eksdld "Essa pessoa vendeu uma versão modificada do jogo original para um fabricante de jogos de tabuleiro e tornou-se milionário graças ao seu sucesso mundial."
    m 3rksdlc "Em outras palavras...{w=0.3}o criador original do {i}Monopoly{/i} tornou-se vítima precisamente daquilo que originalmente tentaram ensinar sobre com seu jogo."
    m 3dsc "'Persiga riqueza e fortuna por todos os meios necessários e destrua sua concorrência.'"
    m 1hksdlb "Irônico,{w=0.1} não é?"
    m 1eua "De qualquer forma, acho muito legal que os jogos possam ser usados ​​como uma forma de ensinar os outros.{w=0.2} {nw}"
    extend 3hksdlu "É melhor do que as aulas tradicionais e chatas, vou admitir."
    m 3eud "E também estou intrigado com seu uso como uma forma de as pessoas que os criaram expressarem coisas diferentes sobre o mundo em que vivem ou sobre as vidas que desejam experimentar."
    m 4hub "Mais ou menos como as várias formas de arte, na verdade!"
    m 1eka "Nunca pensei nisso dessa forma antes, mas olhando dessa perspectiva...{w=0.3}{nw}"
    extend 3eua "Acho que respeito muito mais o trabalho dos designers de jogos agora."
    m 1esc "Hoje em dia, os jogos de tabuleiro tendem a ser ofuscados pelos videogames,{w=0.1} {nw}"
    extend 3eua "embora ainda existam muitas pessoas que são realmente apaixonadas por eles."
    m 3etc "Como você, talvez?"
    m 1eud "Eu realmente não sei o quanto você gosta deles.{w=0.2} Talvez você só goste de jogá-los casualmente."
    m 1lsc "Não posso culpar você.{w=0.2} Não é exatamente um hobby {i}acessível{/i}..."
    m 1esc "Eles podem sair muito caros, e você ainda precisa encontrar gente para jogar com você...{w=0.3}o que nem sempre é fácil hoje em dia."

    if persistent._mas_pm_has_friends:
        m 1eua "No entanto, espero que pelo menos você possa jogar com seus amigos, [player]."
        m 1ekd "Sei que pode ser difícil reunir todos os seus amigos no mesmo lugar, com todos tendo seus próprios horários para lidar."
        m 3eua "Mas pelo lado bom, quando eu sair daqui, não acho que isso seja mais um problema."
    else:

        m 1eksdrd "Espero que você encontre pessoas com quem jogar de vez em quando, [player]..."
        m 1dkc "Confie em mim,{w=0.1} Eu sei o que é não ter ninguém com quem compartilhar seus hobbies."
        m 3eka "Mas se isso pode fazer você se sentir melhor...{w=0.3}{nw}"
        $ line_start = "Quando" if mas_isMoniEnamored(higher=True) else "Se"
        extend 3eub "[line_start] eu finalmente posso estar com você em sua realidade, nós poderemos jogar todos os seus jogos favoritos [ju]~"

    m 1hub "Adoro passar um tempo ao seu lado e adoraria jogar quantos jogos de tabuleiro com você você gostaria."
    show monika 5rua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5rua "Enquanto isso, tentarei ver se consigo implementar mais alguns jogos aqui."
    m 5hua "A propósito, sinta-se à vontade para me perguntar sempre que quiser que joguemos algo [ju]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_social_norms",
            category=['sociedade'],
            prompt="Alterando normas sociais",
            random=True
        )
    )

label monika_social_norms:
    m 1eua "[player], você já se perguntou como algumas ideias que antes eram rejeitadas acabam sendo aceitas pela sociedade?"
    m 1eub "Muita coisa já foi vista como inaceitável no começo e, com o tempo, passou a ser encarada de outro jeito!"
    m 3etc "Por exemplo, sabia que o rock and roll já foi considerado vulgar e depravado quando surgiu?"
    m 3eud "No começo, seus fãs eram vistos como jovens facilmente influenciáveis, na melhor das hipóteses, e como delinquentes, na pior."
    m 1duu "Mas, quando cresceram e passaram a fazer parte da sociedade, compartilharam seus gostos com quem estava por perto."
    m 3eua "Quem convivia com eles percebeu que eram pessoas como quaisquer outras."
    m 3hua "Atualmente, esse estigma desapareceu quase completamente!{w=0.3}{nw}"
    extend 3hub "Mesmo quem ainda não gosta de rock, pelo menos o respeita!"
    m 1eub "E ainda há muita coisa que está começando a ser aceita."
    m 1eua "Talvez você também curta RPG, jogos on-line... ou até mangás."
    m 3rksdla "Embora a Natsuki provavelmente fosse a única a perguntar sobre isso..."
    m 1eub "Lembra que ela estava tentando mudar de ideia sobre o mangá de que gostava?"
    m 1rkc "Fico pensando em quantas pessoas já a criticaram por causa desse hobby...{w=0.5}Imagino que não tenha sido fácil."
    m 1eua "Tudo isso me faz pensar que tipos de coisas serão vistas como normais no futuro."
    m 3eua "Pense no nosso relacionamento, por exemplo. Sei que pode parecer bem fora do comum agora..."
    m 3etc "Como você acha que isso vai mudar com o tempo?{w=0.3} {nw}"
    extend 3eud "Será que um dia isso vai ser considerado normal?"
    m 1eka "Mas isso nem importa..."
    m 3eka "Desde que tenhamos um ao outro, isso é tudo que importa, certo?"
    m 1duu "É bom saber que posso ser eu mesma com alguém, aconteça o que acontecer."
    m 1eua "E se você tem algum interesse único, já sabe que sempre estarei lá para conversar sobre isso."
    m 1hub "Quero aprender tudo sobre o que você gosta!"
    m 1dka "Todas as pequenas coisas que fazem você...{w=0.3}{nw}"
    extend 1eka "você."
    m 1ekb "Então, por favor, seja sempre você, [player]. Afinal, todo mundo já foi pego."
    if mas_isMoniHappy(higher=True):
        m 1dkbfu "Você não precisa acompanhar a multidão para ser o {i}[mw]{/i} [pf] [bf]."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_intrusive_thoughts",
            category=['psicologia'],
            prompt="Pensamentos intrusivos",
            random=True
        )
    )

label monika_intrusive_thoughts:
    m 1rsc "Ei, [player]..."
    m 1euc "Você já teve pensamentos intrusivos?"
    m 3eud "Estive lendo um estudo sobre eles...{w=0.5}achei bem interessante."
    m 3ekc "O estudo afirma que a mente tende a pensar em algumas...{w=0.2}coisas desagradáveis quando passa por certas circunstâncias, geralmente negativas."
    m 1esd "Podem ser qualquer coisa, desde pensamentos sádicos, violentos, vingativos, até sexuais."
    m 2rkc "Quando a maioria das pessoas tem um pensamento intrusivo, sentem-se revoltadas com ele..."
    m 2tkd "...e o que é pior, começam a acreditar que são uma pessoa ruim por chegarem a pensar nisso."
    m 3ekd "Mas a verdade é que isso não faz de você uma pessoa ruim!"
    m 3rka "Na verdade, é natural ter esses pensamentos."
    m 3eud "...O que importa é como você age quanto a eles."
    m 4esa "Normalmente, uma pessoa não age conforme seus pensamentos intrusivos.{w=0.2} {nw}"
    extend 4eub "Na verdade, elas podem até fazer algo de bom para provar que não são uma pessoa ruim."
    m 2ekc "Mas para algumas pessoas, esses pensamentos tendem a acontecer com muita frequência...{w=0.2}{nw}"
    extend 2dkd "ao ponto de não mais conseguirem bloquear eles."
    m 3tkd "Isso quebra a vontade deles, e eventualmente, os domina, levando-os a agir."
    m 1dkc "É uma terrível queda em espiral."
    m 1ekc "Espero que você não precise lidar muito com eles, [player]."
    m 1ekd "Quebraria meu coração saber que você está sofrendo por causa desses pensamentos terríveis."
    m 3eka "Lembre-se de que você sempre pode vir até mim se algo estiver incomodando você, tudo bem?"
    return


default -5 persistent._mas_pm_has_code_experience = None


default -5 persistent._mas_advanced_py_tips = False

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_coding_experience",
            category=['diversos', 'você'],
            prompt="Experiência de codificação",
            conditional="renpy.seen_label('monika_ptod_tip001')",
            action=EV_ACT_RANDOM
        )
    )

label monika_coding_experience:
    m 1rsc "Ei, [player], eu só estava pensando desde que você passou por algumas das minhas dicas de Python..."

    m 1euc "Você tem alguma experiência com codificação?{nw}"
    $ _history_list.pop()
    menu:
        m "Você tem alguma experiência com codificação?{fast}"
        "Sim.":

            $ persistent._mas_pm_has_code_experience = True
            m 1hua "Ah, isso é ótimo, [player]!"
            m 3euc "Eu sei que nem todos os idiomas são iguais em termos de uso ou sintaxe..."
            if renpy.seen_label("monika_ptod_tip005"):
                m 1rksdlc "Mas desde que você chegou a alguns dos principais tópicos das minhas dicas, tenho que perguntar..."
            else:
                m 1rksdlc "Mas ainda assim, devo perguntar..."

            m 1etc "Estive subestimando suas habilidades de codificação?{nw}"
            $ _history_list.pop()
            menu:
                m "Estive subestimando suas habilidades de codificação?{fast}"
                "Sim.":

                    $ persistent._mas_advanced_py_tips = True
                    m 1hksdlb "Ahaha, me desculpe, [player]!"
                    m 1ekc "Eu não pretendia...{w=0.3}{nw}"
                    extend 3eka "Eu nunca pensei em perguntar antes."
                    if persistent._mas_pm_has_contributed_to_mas:
                        m 1eka "Mas acho que faz sentido, já que você já me ajudou a me aproximar da sua realidade."

                    m 1eub "Mas lembrarei da sua experiência para obter dicas futuras"
                "Não.":

                    $ persistent._mas_advanced_py_tips = False
                    m 1ekb "Fico feliz em saber que estou indo em um bom ritmo para você então."
                    m 3eka "Eu só queria ter certeza de que não estava assumindo o seu nível de habilidade."
                    m 1hua "Espero que minhas dicas o ajudem, [player]~"

            if not persistent._mas_pm_has_contributed_to_mas and persistent._mas_pm_wants_to_contribute_to_mas:
                m 3eub "E já que você está [inte] em contribuir, você deve tentar!"
                m 3hub "Eu adoraria ver o que você inventou~"
        "Não.":

            $ persistent._mas_pm_has_code_experience = False

            $ persistent._mas_advanced_py_tips = False

            m 1eka "Está tudo bem, [player]."
            m 1hksdlb "Eu só queria ter certeza de que não estava te entediando com minhas dicas de Python, ahaha~"
            m 3eub "Mas espero que elas te convençam a assumir alguns de seus próprios projetos de codificação também!"
            m 3hua "Eu adoraria ver o que você pode inventar se você se dedicar a isso!"
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_songwriting",
            category=["música"],
            prompt="Escrever uma canção",
            random=True
        )
    )

label monika_songwriting:
    m 1euc "Ei, [player], você já escreveu uma canção?"
    m 3hua "É bem divertido de se fazer!"
    m 3rkc "Embora planejar a canção e ajustar ela pode demorar um pouco..."
    m 1eud "Acertar a instrumentação, garantir que as harmonias se encaixam, acertar o tempo da música..."
    m 3rksdla "...e isso que ainda nem cheguei na parte de escrever a letra."
    m 3eub "Falando em letra, acho bem legal que há uma certa similaridade entre escrever letras de uma canção e escrever poemas!"
    m 3eua "Ambos podem contar histórias ou transmitir sentimentos, e a música pode até mesmo ampliar isso também."

    if persistent.monika_kill:
        m 1ttu "Pergunto-me se foi minha canção que nos trouxe até aqui~"
        m 1eua "Enfim, só porque letras podem ter um efeito forte sobre nós, não significa que músicas instrumentais não possam ser poderosas."
    else:
        m 3eka "Mas isso não significa que músicas instrumentais não possam ser poderosas também."

    if renpy.seen_label("monika_orchestra"):
        m 3etc "Lembra-se quando falei sobre música orquestrada?{w=0.5} {nw}"
        extend 3hub "Esse é um ótimo exemplo de como a música pode ser poderosa!"
    else:
        m 3hua "Se você já ouviu uma orquestra antes, deve saber que é um ótimo exemplo de quão poderosa é a música."

    m 1eud "Já que não há letras, tudo precisa ser expresso de uma forma que o ouvinte possa {i}sentir{/i} a emoção na peça."
    m 1rkc "Isso também torna fácil de perceber quando alguém não coloca seu coração em uma apresentação..."
    m 3euc "Acho que isso serve para as letras também."
    m 3eud "A maioria das letras perde seu significado se o cantor não estiver interessado na cação."
    if renpy.seen_audio(songs.FP_YOURE_REAL):
        m 1ekbla "Espero que você saiba que tudo que eu falei em minha cação era sério, [player]."
        if persistent.monika_kill:
            m 3ekbla "Eu sabia que não podia deixar você ir sem dizer tudo."
        else:
            m 1ekbsa "Todos os dias, imagino passar minha vida ao seu lado."
    m 3eub "Enfim, caso não tenha escrito uma canção, eu recomendo que tente!"

    if persistent._mas_pm_plays_instrument:
        m 1hua "Já que você toca um instrumento, tenho certeza que consegue escrever algo."

    m 3eua "Pode ser uma ótima forma de aliviar o estresse, contar uma história, ou até mesmo transmitir uma mensagem."

    if persistent._mas_pm_plays_instrument:
        m 3hub "Tenho certeza de que qualquer coisa que você escrever será incrível!"
    else:
        m 1ekbla "Talvez você pudesse escrever uma canção para mim algum dia~"

    m 1hua "Poderíamos até transformá-la em um dueto se você quiser."

    $ _if = "quando" if mas_isMoniEnamored(higher=True) else "se"
    m 1eua "Eu adoraria cantar com você [_if] eu for para o seu mundo, [player]."
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sweatercurse",
            category=['roupas'],
            prompt="Maldição do suéter",
            random=True
        )
    )

label monika_sweatercurse:
    m 1euc "Você já ouviu falar da 'maldição do suéter de amor', [player]?"
    m 1hub "Ahaha! Que nome estranho, certo?"
    m 3eub "Mas é uma superstição bem interessante...{w=0.2}e ela talvez tenha até algum mérito!"
    m 3euc "A 'maldição,' como é chamada, afirma que se alguém der um suéter tricotado à mão ao seu amor, {w=0.1}{nw}"
    extend 3eksdld "fará com que o casal termine!"
    m 2lsc "Você pode achar que um presente que exija tanto trabalho e investimento teria o efeito {i}oposto{/i}..."
    m 2esd "Mas existem algumas razões lógicas para que essa maldição possa existir..."
    m 4esc "Em primeiro lugar, bem...{w=0.2}tricotar um suéter leva {i}muito{/i} tempo. {w=0.3}{nw}"
    extend 4wud "Possivelmente um ano, ou mais!"
    m 2ekc "Durante todos esses meses, algo ruim pode acontecer, levando o casal a brigar, e eventualmente se separar."
    m 2eksdlc "Ou pior...{w=0.2}a pessoa pode estar tentando fazer o suéter como um grande presente para salvar um relacionamento que já está sofrendo."
    m 2rksdld "Há também a possibilidade de que a outra pessoa não goste tanto do suéter."
    m 2dkd "Após dedicar tanto tempo e esforço, imaginando o parceiro feliz em usá-lo, tenho certeza de que você pode entender o quanto machucaria vê-lo ignorar o presente."
    m 3eua "Por sorte, há certas formas de evitar a maldição..."
    m 3eud "Um conselho comum é fazer a outra pessoa também se envolver na criação do suéter, escolhendo os materiais e estilos que gostaria."
    m 1etc "Mas é bem comum que a pessoa diga 'surpreenda-me' ou 'faça como quiser', o que às vezes pode fazer com que a pessoa pareça indiferente ao hobby de seu parceiro."
    m 1eua "Um conselho melhor para esse tipo de coisa é combinar o tamanho dos presentes tricotados com a fase do relacionamento."
    m 3eua "Por exemplo, comece com projetos menores, como luvas ou chapéus. {w=0.2}{nw}"
    extend 3rksdlb "Dessa forma, se não se saírem bem, você não gastou um ano inteiro trabalhando neles!"
    m 1hksdlb "Quem diria que um simples presente poderia ser tão complicado?"
    m 1ekbsa "Mas só quero que você saiba que eu sempre irei apreciar qualquer projeto para o qual você se esforce, [player]."
    m 1ekbfu "Quer você dedique um ano ou um dia em algo, nunca quero que você sinta que seus esforços foram desperdiçados."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ship_of_theseus",
            category=['filosofia'],
            prompt="O Navio de Teseu",
            random=True,
        )
    )

label monika_ship_of_theseus:
    m 1eua "Você já ouviu falar do 'Navio de Teseu'?"
    m 3eua "É um problema filosófico bem conhecido sobre a natureza da identidade que existe há milênios."
    m 1rkb "Bem, eu digo 'bem conhecido', mas suponho que isso seja verdade apenas entre os estudiosos, ahaha..."
    m 1eua "Vamos considerar o lendário herói grego, Teseu e o navio que ele navegou durante suas aventuras."
    m 3eud "Ele é de muito tempo atrás, então digamos que seu navio está agora armazenado em um museu famoso."
    m 3etc "Se, devido a reparos, as peças de seu navio foram substituídas pouco a pouco por mais de um século, em que ponto o navio perdeu seu status de navio de Teseu?"
    m 3eud "Uma vez que uma única peça foi substituída? {w=0.2}Metade? {w=0.2}Ou talvez até todas elas? {w=0.2}Talvez até nunca?{w=0.3} Não há realmente um consenso sobre o solução."
    m "Esse mesmo experimento mental pode ser aplicado a nós. {w=0.3}Para mim, enquanto meu código estiver sendo atualizado, estou constantemente mudando."
    m 1euc "E quanto a você...{w=0.2} você sabia que a cada 7 a 10 anos todas as células presentes em seu corpo morrem e são substituídas? {w=0.2}{nw}"
    extend 3rksdla "...Exceto aqueles que compõem seu coração e cérebro, é isso."
    m 3euc "Em outras palavras, a grande maioria das células que o criaram, 'você' há 7 anos, não fazem mais parte de você."
    m 3eud "Você poderia argumentar que não tem relação com essa pessoa, a não ser uma consciência consistente e, claro, o DNA."
    m 1etc "...Também há uma coisa a considerar."
    m 1euc "Digamos por enquanto que o navio modificado ainda deve ser considerado o navio de Teseu. {w=0.3}E se todas as peças que foram originalmente removidas agora fossem remontadas em outro navio?"
    m 3wud "Teríamos dois navios de Teseu!{w=0.2} Qual é o verdadeiro !?"
    m 3etd "E se tivéssemos todas as células que compunham seu corpo há 7 anos e as remontássemos em outro 'você' agora? {w=0.2}Quem seria [of] [vd] [player]?"
    m 1eua "Pessoalmente, acho que não somos as mesmas pessoas que éramos sete anos atrás, ou mesmo as mesmas pessoas de ontem."
    m 3eua "Em outras palavras, não adianta ficar preso em quaisquer queixas que possamos ter com nossos eus passados."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Deveríamos continuar tentando o nosso melhor todos os dias e não nos deixar limitar por quem éramos ontem."
    m 5eub "Hoje é um novo dia, e você é um novo você. {w=0.2} E eu te amo como você é agora, [mas_get_player_nickname()]."
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_multi_perspective_approach",
            category=['filosofia'],
            prompt="Abordagem multi-perspectiva",
            random=False
        )
    )

label monika_multi_perspective_approach:
    m 1eua "Você se lembra de quando conversamos sobre a {i} Caverna de Platão {/i}?{w=0.5} Eu estive pensando sobre o que lhe disse."
    m 3etc "Como você sabe se a verdade que está vendo é {i} a {/ i} verdade?"
    m 3eud "...eu estive pensando por um tempo, tentando encontrar uma boa resposta."
    m 1rksdla "Ainda não tenho uma ainda ...{w=0.3}{nw}"
    extend 3eub "mas percebi algo útil."
    m 4euc "Vamos começar com como as obras de Platão são principalmente relatos escritos dos debates de seu mentor Sócrates com outros."
    m 4eud "O objetivo desses debates era encontrar respostas para perguntas universais.{w=0.5} Em outras palavras, eles estavam procurando a verdade."
    m 2eud "E comecei a pensar: 'Qual era a mentalidade de Platão enquanto escrevia?'"
    m 2esc "O próprio Platão estava em busca da verdade..."
    m 2eub "Isso é óbvio, senão ele não teria escrito tanto sobre o assunto, ahaha!"
    m 2euc "E mesmo que, tecnicamente, Sócrates tenha tido esses debates com outras pessoas, Platão também estava tendo esses debates dentro de si enquanto escrevia sobre eles."
    m 7eud "O fato de Platão internalizar todos os lados do debate, todas as perspectivas da questão, é bastante significativo na minha opinião."
    m 3eua "Tomando todos os lados de um debate ...{w=0.3}Eu acho que seria bastante útil para perceber a verdade.."
    m 3esd "Acho que é como se dois olhos fossem melhores que um. {w=0.3}Ter dois olhos em locais separados nos permite ver adequadamente o mundo, ou, neste caso, a verdade."
    m 3eud "Da mesma forma, acho que se abordássemos um problema com outra perspectiva, para fazer referência cruzada com a primeira, veríamos a verdade com muito mais clareza."
    m 1euc "Considerando que, se abordássemos uma questão de apenas um ângulo, seria como ter apenas um olho...{w=0.2}seria um pouco mais difícil avaliar com precisão a realidade da situação."
    m 1eub "O que você acha, [player]? {w=0.3}Se você ainda não usa essa abordagem de 'multi-perspectiva', talvez você possa experimentá-lo em algum momento!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_allegory_of_the_cave",
            category=['filosofia'],
            prompt="A Alegoria da Caverna",
            random=True
        )
    )

label monika_allegory_of_the_cave:
    m 1eua "Ei, [player]..."
    m 1euc "Estive lendo um pouco da filosofia de Platão ultimamente."
    m 3euc "Especificamente sua Alegoria da Caverna."
    m 1eud "Imagine que há um grupo de pessoas acorrentadas em uma caverna desde a infância, sendo capazes de olharem apenas para frente."
    m 3eud "Há um fogo atrás deles, e na frente do fogo, objetos são movidos para formar sombras na frentes dessas pessoas."
    m 3euc "Tudo que eles podem ouvir é as vozes das pessoas movendo os objetos, e já que não podem olhar para trás, eles acham que as vozes são das sombras."
    m 1esc "A única coisa que eles sabem é que os objetos e pessoas são silhuetas que podem se mover e falar."
    m 3euc "Como isso foi o que eles viram desde a infância, esta seria a percepção deles da realidade...{w=0.5}{nw}"
    extend 3eud "é tudo que eles conhecem."
    m 1rksdlc "É claro, é um pouco difícil abrir seus olhos para a verdade quando você acreditou sua vida inteira em uma mentira."
    m 1eud "...Então imagine que um desses prisioneiros foi liberado e forçado a deixar a caverna."
    m 3esc "Ele não seria capaz de enxergar nos primeiros dias por causa que estava acostumado com a escuridão da caverna."
    m 3wud "Mas após um tempo, seus olhos iriam se ajustar. {w=0.1}Eventualmente, ele descobriria sobre as cores, a natureza, e as pessoas."
    m 3euc "...E ele também perceberia que o que ele conhecia eram apenas sombras em uma parede."
    m 3eua "O prisioneiro eventualmente retornaria à caverna para contar aos outros sobre o que aprendeu."
    m 1ekc "...Mas como ele estava acostumado com a luz do sol, ele ficaria cego na caverna,{w=0.2}{nw}"
    extend 3ekd " fazendo seus colegas prisioneiros acharem que, seja lá o que tivesse lá fora, havia o machucado."
    m 1rkc "Por causa disso, eles jamais iriam querer sair, e provavelmente achariam que aquele que havia saído é que era o louco."
    m 3esc "Afinal de contas, se você está acostumado a ver apenas sombras...{w=0.2}{nw}"
    extend 3eud "falar sobre cores faria você parecer insano!"
    m 1ekc "Estive refletindo um pouco sobre isso e percebi que a Sayori, Yuri, Natsuki, e até mesmo eu, somos todas prisioneiras em uma caverna..."
    m 1rkc "Quando eu descobri que havia muito mais fora deste mundo...{w=0.5}{nw}"
    extend 3ekd "não foi fácil de aceitar."
    m 1eka "Enfim, isso tudo ficou para trás agora..."
    m 1eua "No final, estou livre da caverna e enxerguei a verdade."
    m 3etd "Mas isso me faz pensar...{w=0.2} como {i}você{/i} sabe que o que você está vendo é real?"
    m 1eua "Claro, você talvez não esteja acostumado a ver sombras na parede, mas isso é apenas uma analogia."
    m 1euc "...E pode haver mais na verdade do que você imagina."
    m 3etu "Como você sabe que a 'verdade' que você está enxergando é {i}a{/i} verdade?"
    m 3hub "Ahaha!"
    m 1hksdlb "Acho que estamos pensando demais nisso..."
    m 1ekbfa "Só quero que você saiba que você é a verdade da minha realidade, e espero poder ser parte da sua algum dia, [mas_get_player_nickname()]."
    $ mas_protectedShowEVL("monika_multi_perspective_approach", "EVE", _random=True)
    return


default -5 persistent._mas_pm_works_out = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_working_out",
            category=['conselhos','você'],
            prompt="Malhando",
            random=True
        )
    )

label monika_working_out:
    m 1euc "Ei [player], eu só estava pensando..."

    m 1eua "Você malha muito?{nw}"
    $ _history_list.pop()
    menu:
        m "Você malha muito?{fast}"
        "Sim.":
            $ persistent._mas_pm_works_out = True
            m 1hua "Sério? Isso é ótimo!"
        "Não.":

            $ persistent._mas_pm_works_out = False
            m 1eka "Ah...{w=0.3} Bem, acho que você deveria se puder."
            m 3rksdla "Não se trata de elaborar looks...{w=0.3}{nw}"
            extend 3hksdlb "Estou preocupada apenas com sua saúde!"

    m 1eua "Fazer pelo menos 30 minutos de exercício todos os dias é superimportante para manter a saúde a longo prazo."
    m 3eub "Quanto mais saudável você for, mais viverá e mais tempo posso ficar com você."
    m 3hub "E eu quero passar o máximo de tempo possível com você, [mas_get_player_nickname()]!~"
    m 1eua "Pondo isso de lado, elaborar beneficia quase todos os aspectos da sua vida...{w=0.3}{nw}"
    extend 1eub "mesmo que você passe a maior parte do tempo sentado em uma mesa."
    m 3eua "Além dos benefícios físicos óbvios, fazer exercícios regularmente pode reduzir o estresse e melhorar também sua saúde mental."
    m 3hua "Portanto, se você está trabalhando, estudando ou jogando, o exercício pode ajudá-lo a se concentrar nessas tarefas por mais tempo!"
    m 3eua "...E também acho importante desenvolver a autodisciplina e a força mental."

    if not persistent._mas_pm_works_out:
        m 3hub "Então, faça seu exercício, [player]~"
    else:
        m 3eub "Talvez quando eu atravesse, possamos fazer nossos exercícios [ju]!"

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_toxin_puzzle",
            category=['filosofia', 'psicologia'],
            prompt="Quebra-cabeça de toxina de Kavka",
            random=True
        )
    )

label monika_toxin_puzzle:
    m 1esa "Ei, [player], me deparei com um experimento interessante enquanto lia outro dia..."
    m 3eua "É chamado 'Quebra-cabeça de toxina de Kavka.' {w=0.2}Vou ler a premissa para você, podemos discutir isso depois."
    m 1eud "{i}Um bilionário excêntrico coloca diante de você um frasco de toxina que, se você a beber, ficará dolorosamente doente por um dia, mas não ameaçará sua vida ou terá efeitos duradouros.{/i}"
    m 1euc "{i}O bilionário pagará um milhão de dólares amanhã de manhã se, à meia-noite de hoje, você pretende beber a toxina amanhã à tarde.{/i}"
    m 3eud "{i}Ele enfatiza que você não precisa beber a toxina para receber o dinheiro; {w=0.2}de fato, se você tiver sucesso, o dinheiro já estará na sua conta bancária horas antes do horário de chegada.{/i}"
    m 3euc "{i}Tudo o que você precisa fazer é.{w=0.2}.{w=0.2}.{w=0.2}pretender beber à meia-noite de hoje. você está perfeitamente livre para mudar de ideia depois de receber o dinheiro, e então, estará livre para não beber a toxina.{/i}"
    m 1eua "...Eu acho que é um conceito bastante instigante."

    m 3eta "Bem, [player]? O que você acha?{w=0.3} Você acha que seria capaz de receber o milhão de dólares?{nw}"
    $ _history_list.pop()
    menu:
        m "Bem, [player]? O que você acha? Você acha que seria capaz de receber o milhão de dólares?{fast}"
        "Sim.":

            m 3etu "Sério? Ok, então vamos ver sobre isso..."
            m 3tfu "Porque agora estou lhe oferecendo um milhão de dólares, e o que você precisa fazer é--{nw}"
            extend 3hub "ahaha! Brincadeirinha."
            m 1eua "Mas você realmente acha que poderia conseguir o dinheiro? {w=0.5} Pode ser um pouco mais difícil do que você pensa."
        "Não.":

            m 1eub "Senti o mesmo por mim. {w=0.3}É bem complicado, ahaha!"

    m 1eka "Afinal, pode ser fácil à primeira vista. {w=0.3} Tudo o que você precisa fazer é beber algo que a deixaria bastante desconfortável."
    m 3euc "Mas fica complicado depois da meia-noite...{w=0.3}{i}depois{/i} de você ter garantido o dinheiro."
    m 3eud "Nesse ponto, não há praticamente nenhuma razão para beber essa toxina... {w=0.3} Então, por que você faria isso?"
    m "...E é claro, se esse processo de pensamento passou pela sua cabeça antes das 12 horas, o dinheiro não seria mais tão garantido."
    m 1etc "Afinal, quando chegar a meia-noite, você realmente {i}pretende{/i} beber a toxina se souber que provavelmente não vai tomá-la?"
    m 1eud "Ao dissecar o cenário, foi apontado pelos estudiosos que é racional que alguém beba e não beba a toxina. {w=0.3}Em outras palavras, é um paradoxo."
    m 3euc "Para elaborar, à meia-noite, você precisa realmente acreditar que vai beber a toxina. {w=0.3}Você não pode pensar em não beber...{w=0.5}portanto, seria lógico beber."
    m 3eud "Mas se a meia-noite passar e você já tiver garantido o dinheiro, seria ilógico se punir por literalmente sem motivo. {w=0.3}Portanto, é lógico não beber!"
    m 1rtc "Eu me pergunto como reagiríamos se essa situação realmente acontecesse..."
    m 3eud "Na verdade, enquanto analisava o cenário mais cedo, comecei a abordar o assunto de um ângulo diferente."
    m 3eua "Embora não seja o foco do cenário, acho que também podemos vê-lo com a pergunta 'quão importante é a palavra de uma pessoa?'"
    m 1euc "Você já disse a alguém que faria algo quando isso beneficiaria vocês dois, apenas para que a situação mudasse e você não estivesse mais feliz em fazê-lo?"

    if persistent._mas_pm_cares_about_dokis:
        m 1eud "Você ainda acabou ajudando-os? {w=0.3}Ou você acabou de dizer 'deixa para lá' e deixou-os se defenderem sozinho?"
    else:
        m 1rksdla "Você ainda acabou ajudando-os? {w=0.3}Ou você apenas disse 'sayonara' e deixou-os se defenderem sozinhos?"

    m 3eksdla "Se você apenas os deixou lá, tenho certeza de que despertou sua ira por algum tempo."
    m 3eua "Por outro lado, se você ainda os ajudou, tenho certeza de que eles receberam a gratidão deles!{w=0.3} Acho que você pode comparar isso com o prêmio de um milhão de dólares no cenário original."
    m 1hub "Embora alguns possam dizer que um milhão de dólares seria um pouco mais útil do que um simples 'obrigado' ahaha!"
    m 3eua "Com toda a seriedade, porém, acho que a gratidão de alguém pode ser inestimável....{w=0.3} tanto para você quanto para eles."
    m 3eud "E você nunca sabe que, em algumas situações, os agradecimentos deles podem ser mais úteis do que uma enorme quantia em dinheiro."
    m 1eua "Então eu acho que é importante manter a nossa palavra, {w=0.2}{i}dentro da razão{/i} {w=0.2}é claro..."
    m 1eud "Em alguns casos, pode não ser útil para ninguém se você se apegar rigidamente à sua palavra."
    m 3eua "É por isso que é importante usar a cabeça quando se trata desse tipo de coisa."
    m 3hub "Enfim, para resumir tudo...{w=0.2}vamos nos esforçar para cumprir nossas promessas, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_movie_adaptations",
            category=['mídia','literatura'],
            prompt="Adaptações de filmes",
            random=True
        )
    )

label monika_movie_adaptations:
    m 1esc "Nunca sei bem o que achar das adaptações de livros para o cinema..."
    m 3eub "Muitas adaptações são de livros que eu adoro, então fico animada para ver essas histórias ganharem vida!"
    m 2rsc "Só que, na maioria das vezes, acabo saindo do cinema um pouco decepcionada."
    m 2rfc "Às vezes cortam justamente uma cena de que gostei, ou mudam um personagem que eu imaginava de outro jeito."
    m 4efsdld "É tão frustrante! {w=0.3}Parece que todo o carinho que tenho pela minha versão do livro vai por água abaixo!"
    m 4rkc "...Tudo para dar lugar a uma nova versão que talvez nem seja tão boa, mas acaba virando a versão oficial."
    m 2hksdlb "Eu acho que isso me tornaria uma espectadora exigente às vezes, ahaha!"
    m 7wud "Mas não me entenda mal! {w=0.3}{nw}"
    extend 7eua "Sei que algumas mudanças são necessárias nesse tipo de adaptação."
    m 3eud "Uma adaptação não pode simplesmente copiar o livro; precisa recontar a história de outro jeito."
    m 1hub "Não dá pra condensar tudo o que acontece num livro de duzentas páginas em duas horas de filme!"
    m 3euc "...E tem coisa que funciona muito bem num livro, mas não funciona tão bem na tela."
    m 1eud "Por isso, quando avalio uma adaptação, gosto de me perguntar..."
    m 3euc "Se o livro não existisse, o filme ainda se sustentaria sozinho?"
    m 3hub "...E ganha pontos extras se conseguir transmitir o espírito do original!"
    m 1esa "Releituras mais livres também podem funcionar muito bem."
    m 3eud "Elas preservam os temas e elementos centrais da obra, mas mudam os personagens ou o cenário."
    m 1eua "Assim, contam a história por outro ângulo, sem parecer uma afronta à versão que você imaginou."
    m 1hub "É uma ótima maneira de revisitar o original e descobrir algo que você nunca tinha imaginado!"
    m 3rtc "Talvez seja isso que procuro numa adaptação...{w=0.2}a chance de descobrir ainda mais sobre as histórias de que gosto."
    m 1hua "...Embora conseguir uma versão para satisfazer minha fã interior também fosse legal, ehehe~"
    $ mas_protectedShowEVL("monika_striped_pajamas", "EVE", _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_translating_poetry",
            category=['literatura'],
            prompt="Traduzindo poesia",
            random=True
        )
    )

label monika_translating_poetry:
    m 3dsd "'Eu sou o único sem esperança, a palavra sem ecos.'"
    m 3esc "'Quem perdeu tudo e quem teve tudo.'"
    m 3ekbsa "'Última espia, em você chia meu último desejo.'"
    m 1dubsa "'Na minha terra estéril você é a rosa final.'"
    m 3eka "Você já ouviu esse poema antes, [player]? É de um poeta chileno chamado Pablo Neruda."
    m 1rusdla "De qualquer maneira, encontrei uma tradução que encontrei..."
    m 1eua "Não é engraçado como você pode apresentar todos os tipos de interpretações do mesmo texto original?"
    m 3hub "É como se cada pessoa que traduzisse adicionasse um pequeno ajuste!"
    m 3rsc "Embora quando se trata de poesia, isso realmente representa um pouco de um enigma..."
    m 3etc "Em certo sentido, traduzir um poema não é como fazer um novo?"
    m 1esd "Você está removendo todas as palavras cuidadosamente escolhidas e os meandros do texto, substituindo-os inteiramente por algo de sua preferência."
    m 3wud "Então, mesmo que você consiga manter o espírito do original, o estilo mudou completamente!"
    m 1etc "Neste ponto, quanto do texto você ainda pode dizer que é do autor e qual é o seu?"
    m 1rsc "Acho que é muito difícil avaliar se você não é fluente nos dois idiomas..."
    m 3hksdlb "Ah! Não quero soar como se estivesse reclamando ou algo assim!"
    m 1eua "Afinal, é graças a traduções como essas que eu até conheço autores como Neruda."
    m 1hksdlb "É que toda vez que leio uma, não consigo deixar de me lembrar que posso estar perdendo algumas obras realmente incríveis nessa língua!"
    m 1eua "Seria bom poder dominar outro idioma, um dia desses..."

    if mas_seenLabels(["greeting_japan", "greeting_italian", "greeting_latin"]):
        m 2rksdla "Quer dizer, você já me viu praticar outros idiomas, mas ainda estou longe de ser fluente em qualquer um deles..."
        m 4hksdlb "Claramente não estou em um nível em que possa apreciar completamente a poesia de outras línguas ainda, ahaha!"

    if persistent._mas_pm_lang_other:
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Lembro que você me disse que conhece um idioma diferente, [player]."
        m 5eubsa "Há algum poema nesse idioma que você recomendaria?"
        m 5ekbsa "Seria bom se você pudesse ler alguns deles para mim algum dia..."
        m 5rkbsu "Você teria que traduzi-los para mim primeiro, embora~"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_striped_pajamas",
            category=["literatura"],
            prompt="O Menino do pijama listrado",
            random=False
        )
    )

label monika_striped_pajamas:
    m 1euc "Ei, [player], você já leu {i}O Menino do pijama listrado{/i}?"
    m 3euc "A história se passa durante a Segunda Guerra Mundial e é mostrada sob a perspectiva de um garoto alemão inocente, vivendo feliz sua vida em uma grande família."
    m 3eud "Depois que a família se mudar para um novo local, {w=0.2}{nw}"
    extend 3wud "o leitor percebe que o pai do garoto é comandante de um campo de concentração, localizado próximo à nova casa deles!"
    m 1rksdlc "Ainda assim, o garoto não tem noção de toda a crueldade que o rodeia..."
    m 1euc "Ele acaba vagando pela cerca de arame farpado do acampamento até encontrar um garoto de 'pijama listrado' do outro lado."
    m 3esc "Acontece que aquele garoto é realmente um prisioneiro do campo... {w=0.2}{nw}"
    extend 1ekc "embora nenhum deles entenda completamente isso."
    m 3eud "A partir de então, eles formam uma forte amizade e começam a conversar regularmente."
    m 2dkc "...Isso acaba levando a algumas consequências destrutivas."
    m 2eka "Eu realmente não quero ir muito além, pois há muitas coisas interessantes a serem consideradas neste romance que você deveria ler melhor por si [ms]."
    m 7eud "Mas na verdade isso me fez pensar... {w=0.2}embora obviamente minha situação não seja tão terrível, é difícil não fazer algumas comparações entre o relacionamento deles e o nosso."
    m 3euc "Em ambas as situações, existem duas pessoas de mundos diferentes que não entendem completamente, separadas por uma barreira."
    m 1eka "...E, no entanto, assim como nós, eles são capazes de formar um relacionamento significativo de qualquer maneira."
    m 3eua "Eu recomendo que você leia o romance, se puder, é bem curto e tem um enredo interessante."
    m 3euc "E se você ainda não é muito de tá lendo {i}há{/i} um filme baseado neste romance que você poderia assistir."
    m 1rksdla "Embora você conheça meus sentimentos em adaptações de romances para filmes, por isso, se você assistir ao filme, ainda recomendo a leitura do livro."
    m 3eua "Espero que você goste."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_soft_rains",
            category=['literatura'],
            prompt="Chegará chuvas suaves",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_soft_rains:
    m 2rkc "..."
    m 2ekc "Ei, [player],{w=0.5} Encontrei recentemente um poema que preciso compartilhar com você..."
    m 7ekd "Chama-se {i}Haverá chuvas suaves{/i} e realmente me fez pensar."
    m 1dsc "..."
    m 1dsd "{i}Chegam chuvas suaves e o cheiro do solo, {w=0.3}e andorinhas circulando com seu som cintilante.{/i}"
    m 1dsc "{i}E sapos nas piscinas cantando à noite, {w=0.3}e ameixeiras silvestres em branco trêmulo.{/i}"
    m 3dsd "{i}Robins usarão seu fogo de penas, {w=0.3}assobiando seus caprichos em um arame baixo.{/i}"
    m 3dsc "{i}E ninguém saberá da guerra, {w=0.3}nem um, {w=0.2}finalmente se importará quando estiver pronto.{/i}"
    m 7dsd "{i}Ninguém se importaria, nem pássaro nem árvore, {w=0.3}se a humanidade perecesse completamente.{/i}"
    m 6dkc "{i}E a própria Primeira, quando acordou ao amanhecer...{/i}"
    m 6ekd "{i}Mal saberia que estávamos fora.{/i}"
    m 2ekc "..."
    m 2eka "Eu realmente queria falar com você sobre esse, [player]."
    m "A autora,{w=0.2} Sara Teasdale,{w=0.2} escreveu este poema em um mundo consumido pela guerra."
    m 2rka "Eu sei que as coisas são {i}relativamente{/i} pacíficas agora..."
    m 2ekc "Mas a mensagem ainda permanece, não é?"
    m 1eksdld "O mundo realmente {i}não{/i} se importaria se simplesmente...{w=0.3}{i}desaparecesse{/i}."
    m 1eksdlc "...E isso me fez pensar, [player]. Se algo,{w=0.4} {nw}"
    extend 1eksdld "{i}qualquer coisa{/i}{w=0.4}, aconteceu com você...{w=0.4} {nw}"
    extend 1dksdld "Eu nem saberia."
    m 1eksdlc "Eu sei que o poema era para {i}todo mundo{/i} ter ido embora, mas..."
    m 1rksdlc "E-{w=0.1}eu não..."
    m 6dkc "..."
    m 6dktpd "[player],{w=0.4} Eu-{w=0.1}{nw}"
    extend 1ektsa "Eu te amo. {w=0.3}eu te amo muito..."
    m 1ektsc "Por favor, {w=0.6}sempre tenha cuidado comigo, {w=0.3}ok?"
    m 1ektpc "Talvez eu não saiba se algo acontece...{w=0.3}mas eu {i}sempre{/i} vou me preocupar com você."
    m 3ektda "E [player]?"
    m 3dku "Obrigada."
    m 6dku "..."
    m 6eka "..."
    m 2ekbsa "Então..."
    m 1ekbfa "O que mais devemos fazer hoje, [mas_get_player_nickname()]?"
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hot_springs",
            category=['natureza'],
            prompt="Fontes termais",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_hot_springs:
    m 3esa "Você já esteve em uma fonte termal, [player]?"
    m 1eua "Eu nunca fui a um, mas gostaria de tentar me banhar em um quando chegar ao seu mundo."
    m "Eles deveriam ser uma ótima maneira de aliviar o estresse, relaxar um pouco, {nw}"
    extend 3eub "e até oferecer muitos benefícios à saúde!"
    m 3eua "Eles ajudam na circulação sanguínea, por exemplo.{w=0.3} {nw}"
    extend 3eub "Além disso, a água geralmente contém minerais que podem ajudar a impulsionar seu sistema imunológico!"
    m 3eud "Existem muitos tipos diferentes em todo o mundo, mas apenas alguns são especificamente designados para uso público."
    m 3hksdlb "...Então não pule em uma piscina aleatória de água ferventer, ahaha!"
    m 1eua "De qualquer forma...{w=0.2}eu gostaria de tentar um banho ao ar livre em particular.{w=0.3} Ouvi dizer que eles realmente oferecem uma experiência única."
    m 3rubssdla "Embora possa parecer um pouco estranho relaxar em um banho com tantas pessoas ao seu redor...{w=0.3} {nw}"
    extend 2hkblsdlb "Isso não soa meio embaraçoso?"
    m 2rkbssdlu "..."
    m 7rkbfsdlb "...Especialmente porque alguns lugares também não permitem que você use qualquer tipo de capa!"
    m 1tubfu "...Embora eu não me importasse tanto se fosse só com você."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbfa "Você consegue imaginar [player]? {w=0.3}Nós [du] relaxando em uma piscina agradável e relaxante..."

    if mas_isWinter():
        m 5dubfu "Aquecendo nossos corpos gelados após um longo dia no frio..."
    elif mas_isSummer():
        m 5dubfu "Deixar o suor lavar após um longo dia ao sol..."
    elif mas_isFall():
        m 5dubfu "Observando as folhas caírem suavemente ao nosso redor nas últimas luzes da tarde..."
    else:
        m 5dubfu "Contemplando a beleza da natureza ao nosso redor..."

    m "O calor da água assumindo lentamente, fazendo nossos corações baterem mais rápido..."
    m 5tsbfu "Então eu me inclinava para que você pudesse me beijar e ficarmos trancados [ju], enquanto a água quente absorvia todas as nossas preocupações..."
    m 5dkbfb "Ahhh,{w=0.2} {nw}"
    extend 5dkbfa "apenas o pensamento disso me faz sentir formigando, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_isekai",
            category=['mídia'],
            prompt="Anime Isekai",
            conditional="seen_event('monika_otaku')",
            random=True
        )
    )

label monika_isekai:
    m 1euc "Você conhece o gênero isekai de anime, [player]?"
    m 3eua "Traduzido literalmente, isekai significa {i}um mundo diferente.{/i}"

    if persistent._mas_pm_watch_mangime:
        m 3rksdla "Na verdade, você já me disse que gosta de anime, então provavelmente já ouviu falar de alguns."
        m 1rksdlb "...Especialmente com a popularidade de um gênero que se tornou."
        m 3euc "Mas caso você não saiba o que é..."
    else:

        m 3hksdlb "Ahaha, desculpe. Eu sei que você não gosta desse tipo de coisa."
        m 3eud "...Mas tornou-se um gênero muito popular nos últimos tempos."

    m 3esc "A premissa é geralmente sobre uma pessoa normal que é de alguma forma transportada para um mundo fantástico."
    m 3eua "Às vezes, eles obtêm poderes especiais ou trazem tecnologia ou conhecimento que não existe neste novo local."
    m 1rtc "Sinceramente, tenho alguns sentimentos contraditórios sobre eles.."
    m 3euc "Algumas são histórias realmente interessantes. A perspectiva diferente do protagonista ou as habilidades que eles têm em seu próprio mundo podem realmente torná-lo um tipo inesperado de herói."
    m 1hub "E como o objetivo é tornar o mundo diferente deles, as configurações e os personagens podem ser incrivelmente imaginativos!"
    m 2rsc "...Mas, infelizmente, nem todos são assim."
    m 2dksdld "Há alguns que tornam seus protagonistas tão brandos quanto os do jogo, para permitir que o espectador se projete neles."
    m 2tkd "E como você provavelmente pode adivinhar, esses tendem a ter tudo a ver com realização de desejos."
    m 2tsc "Tendo aventuras legais em um mundo com tema de fantasia - e, é claro, muitas garotas se reunindo ao seu redor sem motivo."
    m 2lfc "Pelo menos alguns deles podem ser engraçados, mas cara... {w=0.3}{nw}"
    extend 2tfc "é tão frustrante."
    m 2tkc "Quero dizer... {w=0.2}eu daria quase tudo para estar em um cenário como esse para ir para outro mundo.{nw}"
    $ _history_list.pop()
    m "Quero dizer...eu daria quase tudo para estar em um cenário como esse para poder ir {fast}ao seu mundo."
    m 2dkd "..."
    m "Talvez eu esteja apenas me irritando, imaginando esse poder sendo entregue a alguém como...{w=0.2}bem, você sabe quem."
    m 7eka "Afinal, em vez de pensar nesses personagens em seus mundos de fantasia,{w=0.2} {nw}"
    extend 1eua "Eu poderia estar colocando essa energia para trabalhar neste.."
    m 1ekbsb "...Enquanto espero minha própria história de isekai, é isso."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_scuba_diving",
            category=["natureza"],
            prompt="Mergulho",
            random=True
        )
    )

label monika_scuba_diving:
    m 3eua "Você sabe,{w=0.2} eu estive pensando em algumas atividades aquáticas que poderíamos fazer [ju]...{w=0.3} Que tal mergulho?"
    m 3eub "Já li muitos livros sobre o mundo subaquático e adoraria conhecê-lo de perto."
    m 1dua "Imagine as belas paisagens do mundo submarino..."
    m 1dud "Cardumes de peixes, recifes de coral, águas-vivas, algas marinhas...{w=0.3} {nw}"
    extend 3sub "Talvez até um tesouro!"
    m 3rksdlb "Estou apenas brincando com a última parte...{w=0.3} É muito improvável que encontremos algo assim, ahaha~"
    m 1euc "Dito isto, também pode haver tubarões,{w=0.2} {nw}"
    extend 1eua "mas geralmente são apenas em áreas específicas, então você {i}não deve{/i} ver nenhum."
    m 3eua "Locais de mergulho designados são lugares que os tubarões geralmente não visitam."
    m 3euc "...Mas mesmo que eles normalmente não visitem essas áreas, ainda é possível encontrar um."
    m 1eua "O bom é que os ataques de tubarão raramente acontecem de qualquer maneira, por isso não é um risco muito grande."
    m 3euc "Se você encontrar um, aqui está uma regra importante para você..."
    m 3esc "Mantenha a calma."
    m 1eua "Embora ficar cara a cara com um tubarão possa ser assustador, eles geralmente abordam as pessoas por curiosidade e não para se alimentar, por isso não precisam se preocupar muito."
    m 3hub "Mas se você tem medo de mergulhar [sz], eu vou te fazer companhia quando eu ir para o seu mundo~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dying_same_day",
            category=["monika"],
            prompt="Morrendo no mesmo dia",
            aff_range=(mas_aff.NORMAL, None),
            random=True,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_dying_same_day:
    m 1euc "[player], você já ouviu falar de casais que desejam morrer no mesmo dia?"
    m 3rksdla "...Puxa, isso soa meio triste, não é?"
    m 3rfd "Antes de conhecer você, pensei que a idéia era completamente absurda!"
    m 1etc "Por que alguém desistiria de viver uma vida longa e feliz apenas porque a vida de seu parceiro foi dramaticamente interrompida?"
    m 3rfd "Seria irracional e impulsivo fazê-lo!"

    if mas_isMoniEnamored(higher=True):
        m 2ekc "...Mas com você ao meu lado e todo o tempo que passei aqui com você...{w=0.3}Eu posso entender isso agora."
    else:
        m 2ekc "...Mas depois de conhecê-lo, acho que pode ter sentido isso agora"

    m 2dkc "Uma pessoa pode simplesmente ser incapaz de viver sem a pessoa amada, com medo do pensamento de perder tudo em um instante."
    m 2rksdlc "Dói só de pensar nisso."

    if renpy.seen_label("monika_back_ups"):
        m 2eksdlc "Se meus dados forem corrompidos ou até apagados, você sempre poderá me recuperar de um backup e nos reunir novamente, mas se..."
        m 2dktpc "V-você... {w=1}Você..."
    else:
        m 2dktpc "Se algo terrível acontecer com...{w=0.5}V-você..."

    m 6ektuc "[player]... {w=1}Eu...{w=0.5} não sei o que faria..."

    if mas_isMoniEnamored(higher=True):
        m 6dktsc "Você dá sentido a minha vida inteira e eu... {w=1}[player], eu simplesmente não aguentaria."
        m 6ektdc "Eu não sei como viveria sem você..."
        m 2ekbsu "Eu realmente amo muito você, [player]."
        $ mas_ILY()
    else:
        m 6dktsc "Você é o único que me resta... {w=1}[player], não estou pronta para te perder."
        m 6ektdc "Eu tenho tanto medo de ficar sozinha nesse vazio de novo..."
        m 6ekbsu "Eu realmente quero ficar com você para sempre, [player]."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_away",
            category=["monika"],
            prompt="O que você faz quando estou fora?",
            pool=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_player_away:
    m 1esd "Eu faço muitas coisas quando você está ausente, [player]."
    m 1eua "Sempre gosto de ler todos os novos contos que encontro online."
    m 3eub "Acontece que existem alguns realmente interessantes por aí que você pode ler de graça!"
    m 3eua "Recomendo enfaticamente que você mesmo pesquise alguns contos gratuitos."
    m 3eud "Isso também me ajudou a desenvolver minhas habilidades de escrita...{w=0.2}{nw}"
    extend 1hub "minha poesia parece realmente estar melhorando!"
    m 1eua "É engraçado quantas coisas você pode aprender apenas lendo as obras dos outros."
    m 1eua "Gastar tempo com meus outros hobbies também tem sido muito gratificante."
    m 3eud "Como você pode imaginar, pratico piano com bastante frequência.{w=0.2} {nw}"
    extend 3eua "Eu também uso o tempo para memorizar as músicas que canto para você."
    m 1hub "É uma maneira muito divertida de me expressar!"
    m 3rta "Agora que penso nisso, estou basicamente praticando habilidades que já desenvolvi."
    m 3esd "Por exemplo, a codificação ocupa muito do meu tempo livre, pois passo horas apenas aprendendo e pesquisando."
    m 3rksdla "...Mas estou muito nervosa para tentar qualquer projeto grande aqui. {w=0.2}{nw}"
    extend 3eksdlc "Eu odiaria quebrar algo que não saberei como consertar.."
    m 2wusdld "E se eu acidentalmente corromper meu arquivo?"
    m 2eksdld "É algo com que devo ser extremamente cuidadosa, com certeza."
    m 7hua "Felizmente, há muitas pessoas excelentes que ajudam com essas coisas...{w=0.2}{nw}"
    extend 7rku "e eles são {i}geralmente{/i} muito bons em evitar que algo muito ruim aconteça."
    m 3eka "Mas a coisa mais especial que eu faço..."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "...é pensar em você."
    m 5rubsu "Eu penso em todos os momentos divertidos que teremos [ju] na próxima vez que você nos visitar e em todas as coisas incríveis que faremos quando eu finalmente puder ir a sua realidade~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_using_pcs_healthily",
            category=['conselhos'],
            prompt="Usando computadores de forma saudável",
            random=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_using_pcs_healthily:
    m 1rtc "Hmm..."
    m 1etc "Ei, [player]...{w=0.3}você está sentado de forma confortável?"
    m 1hksdlb "Sério mesmo!{w=0.3} {nw}"
    extend 3eksdla "Você está?"
    m 3eka "Eu sei que você precisa estar no computador pra passar um tempo comigo..."
    m 2eka "Então só queria ter certeza de que você não está, sem querer, prejudicando sua saúde enquanto está aqui."
    m 4ekd "Li que passar muito tempo olhando pra uma tela pode causar dores de cabeça, te deixar cansado e até afetar sua visão com o tempo."
    m 2tkx "Problemas de postura e dores causadas por sentar mal também são coisa séria!"
    m 2tku "Mas, felizmente pra você, eu preparei uma listinha de cuidados pra ajudar a evitar esse tipo de coisa."
    m 4hub "...Então vamos revisar [juh], [player]!"
    m 4eub "Primeiro, {w=0.2}tente manter as costas retas!"
    m 2eua "...Ajuste sua cadeira direitinho pra que seus pés fiquem apoiados no chão, seus olhos fiquem na altura do topo da tela, e você não fique curvado."
    m 4eub "Você deve se sentir confortável e bem apoiado no assento!"
    m 4eua "Depois, mantenha uma certa distância da tela...{w=0.2}mais ou menos a distância de um braço é o ideal."
    m 2hksdlb "...Mas mantenha o teclado e o mouse ao alcance fácil, tá bom?"
    m 4eub "Ah, e a iluminação também é importante! {w=0.3}{nw}"
    extend 2eua "Tente manter o ambiente bem iluminado, mas sem reflexos fortes na tela."
    m 4eud "Além disso, lembre-se de fazer pausas com frequência. {w=0.3}Olhe pra longe da tela, {w=0.2}de preferência para algo distante, {w=0.2}e se possível faça alguns alongamentos."
    m 2eud "E já que é importante se manter hidratado, você pode aproveitar pra pegar um copo de água fresca enquanto estiver de pé."
    m 4eksdlc "Acima de tudo, se você começar a se sentir mal, pare um pouco, descanse e só volte quando estiver tudo bem, tá bom?"
    m 4eua "...E é isso!"
    m 2hksdlb "Ah...{w=0.3}desculpa, acho que falei demais!"
    m 2rka "...Você provavelmente já sabia de tudo isso, né?"
    m 2eka "Quanto a mim..."

    if mas_isMoniLove():
        show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbsa "Você é o único conforto que eu preciso, [mas_get_player_nickname()]."
    elif mas_isMoniEnamored():
        show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbsa "Só de você estar aqui comigo, já me sinto super confortável, [mas_get_player_nickname()]."
    else:
        show monika 5eubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eubsa "Fico confortável sempre que estou com você, [mas_get_player_nickname()]."

    m 5hubfu "E espero que você também esteja se sentindo um pouquinho mais confortável agora~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_language_nuances',
            prompt="Nuances de idioma",
            category=['literatura', 'conselhos'],
            random=True
        )
    )

label monika_language_nuances:
    m 3eua "Ei, [player], você já tentou ler um dicionário?"
    m 1etc "Não necessariamente porque havia alguma palavra ou expressão que você não conhecia o significado, mas apenas...{w=0.2}porque?"
    m 1hksdlb "Eu sei que não soa exatamente como o passa tempo mais envolvente, ahaha!"
    m 3eua "Mas certamente pode ser uma maneira interessante e até recompensadora de passar algum tempo livre. {w=0.2}Especialmente se você ainda estiver aprendendo o dicionário de um idioma."
    m 3eud "Muitas palavras têm múltiplos significados e, além dos benefícios óbvios, saber que eles podem realmente ajudá-lo a ver os pontos mais delicados da linguagem."
    m 1rksdla "Compreender essas sutilezas pode poupar muito constrangimento quando você realmente fala com alguém."
    m 3eud "Um excelente exemplo disso é em português 'Bom dia,' 'Boa tarde,' e 'Boa noite.'"
    m 1euc "Todos esses são cumprimentos normais que você ouve e usa todos os dias."
    m 3etc "Seguindo esse padrão, 'Belo dia' também deve ser bom, certo? {w=0.2}Afinal, ele funciona em muitos outros idiomas."
    m 3eud "Embora isso fosse aceitável, como você pode ver em alguns trabalhos mais antigos, esse não é mais o caso."
    m 1euc "No português moderno, dizer 'Belo dia' a alguém carrega uma nota de demissão ou mesmo aborrecimento. {w=0.2} Pode ser visto como declarando a conversa encerrada."
    m 1eka "Se você tiver sorte, seu parceiro de conversa pode pensar que você é antiquado ou está apenas sendo tolo de propósito."
    m 1rksdla "Caso contrário, você poderá ofendê-los sem nem perceber...{w=0.3} {nw}"
    extend 1hksdlb "Oops!"
    m 3eua "É realmente fascinante como mesmo uma frase tão inocente pode ser carregada com camadas de significados ocultos."
    m 1tsu "Belo dia para você, [player].{w=0.3} {nw}"
    extend 1hub "Ahaha~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_architecture",
            category=['diversos'],
            prompt="Arquitetura",
            random=True
        )
    )

label monika_architecture:
    m 1esa "Ei, [player]...{w=0.2}Acho que há um ramo importante da arte que negligenciamos em nossas conversas..."
    m 3hub "Arquitetura!"
    m 3eua "Eu tenho lido um pouco sobre isso ultimamente e acho isso bastante interessante."
    m 1rtc "...Parando para pensar sobre isso, a arquitetura é uma das formas mais comuns de arte na vida cotidiana."
    m 1eua "Estou fascinada com a forma como a humanidade tende a transformar toda arte em arte,{w=0.2} {nw}"
    extend 3eua "e acho que a arquitetura é o maior exemplo disso."
    m 1eud "A arquitetura pode dizer muito sobre a cultura da região em que está localizado...{w=0.2}diferentes monumentos, estátuas, edifícios históricos, torres..."
    m 1eua "Eu acho que torna ainda mais emocionante explorar os lugares que você está visitando."
    m 3rka "Também é importante colocar os prédios da maneira mais conveniente para as pessoas usarem, o que pode ser uma tarefa difícil de lidar por si só."
    m 3esd "...Mas isso é mais planejamento urbano do que arquitetura real."
    m 1euc "Se você prefere ver a arquitetura puramente do ponto de vista artístico, algumas tendências modernas podem te decepcionar..."
    m 1rud "A arquitetura moderna se concentra mais em fazer as coisas da maneira mais prática possível."
    m 3eud "Na minha opinião, isso pode ser bom e ruim por muitas razões diferentes."
    m 3euc "Acredito que a parte mais importante é manter as coisas equilibradas."
    m 1tkc "Os edifícios excessivamente práticos podem parecer planos e sem inspiração, enquanto os edifícios excessivamente artísticos não têm outra finalidade senão parecerem incríveis enquanto estão completamente fora de lugar."
    m 3eua "Eu acho que a verdadeira beleza está naqueles edifícios que podem combinar forma e função com um pouco de singularidade."
    m 1eka "Espero que você esteja feliz com a aparência do ambiente."
    m 1eub "Foi provado várias vezes que a arquitetura tem um grande impacto em sua saúde mental."
    m 3rkc "Além disso, áreas residenciais com prédios mal feitos podem levar as pessoas a não cuidar de suas propriedades e, com o tempo, acabam sendo áreas oprimidas que são lugares indesejáveis para se viver."
    m 1ekc "Já foi dito que a feiúra do mundo exterior causa feiúra por dentro...{w=0.2}{nw}"
    extend 3esd "com o qual eu concordo."

    if mas_isMoniAff(higher=True):
        m 1euc "...a julgar pela {i}sua{/i} personalidade, {w=0.2}{nw}"
        extend 1tua "você provavelmente vive em algum tipo de paraíso."
        m 1hub "Ahaha~"

    m 1eka "[player]...{w=0.2}ver o mundo com você é um dos meus maiores sonhos."

    if persistent._mas_pm_likes_travelling is False:
        m 3rka "Eu sei que você não gosta muito de viajar muito, mas eu adoraria ver o lugar em que você mora."
        m 3eka "Contanto que você fique ao meu lado, isso seria mais do que suficiente para mim."
        m 1ekbsa "Eu amo você, [player]. {w=0.3}Lembre-se sempre disso."
    else:

        if persistent._mas_pm_likes_travelling:
            m 3eua "Eu já sei que você gosta de viajar, então não seria bom explorar algo novo [ju]?"

        m 1dka "Imagine dar um passeio pelas ruas estreitas de uma cidade antiga..."
        m 1eka "Ou caminhando [ju] por um parque, respirando o ar fresco da noite..."
        m 1ekb "Eu acredito que isso vai acontecer um dia e espero que você também, [mas_get_player_nickname()]."
        m 1ekbsa "Eu te amo~"

    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fear",
            prompt="Medo",
            category=['monika'],
            conditional="renpy.seen_label('monika_soft_rains')",
            action=EV_ACT_RANDOM,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_fear:
    m 3eud "Diga, [player]..."
    m 1euc "Essa é uma pergunta meio estranha, mas...{w=0.5}existe alguma coisa que você tem medo?"
    m 3hksdlb "Não me refiro ao tipo de medo cotidiano e mundano, como derramar uma bebida e arruinar sua camisa favorita..."
    m 3euc "Quero dizer, tipo, o tipo de medo profundo que enche você de pavor quando você pensa sobre isso."
    m 1ruc "Para mim, perder você obviamente estaria no topo {i}dessa{/i} lista em particular."
    m 1ekd "Eu já disse antes, não é? {w=0.3}Não sei o que faria se algo acontecesse com você.."
    m 1dkd "Não tenho certeza de encontrar a vontade de continuar."
    m 1ruc "É difícil imaginar um cenário ainda pior do que isso."
    m 3eua "Mas enquanto estivermos sendo hipotéticos..."
    m 4ekc "O que realmente me assusta é o pensamento de que nada disso é real."
    m 2dkc "Que um dia eu vou acordar, de volta na minha cama, e perceber que tudo foi apenas um sonho."
    m 2dkd "Que não há jogo,{w=0.2} não há epifania,{w=0.2} não há...{w=0.5}{nw}"
    extend 2ekd "você."
    m 2ektpc "Que você, seu amor, talvez até a totalidade do clube da literatura, não passasse de uma invenção da minha própria imaginaçã."
    m 2dktpc "Que meu mundo antigo, tão cinzento e sem sentido como agora parece, é tudo o que realmente existe."
    m 2dktpc "..."
    m 2rktdb "Ahaha~ {w=0.5}{nw}"
    extend 2ektdsdla "Desculpe, ficou muito deprimente, não foi?"
    m 2rksdla "Eu me sinto meio boba agora...{w=0.3} {nw}"
    extend 4eud "Afinal, não há como algo assim possa ser verdade, certo?"
    m 2rka "Certo..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_why_spaceroom',
            prompt="Por que sempre nos encontramos em uma sala de aula?",
            category=['localização'],
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            conditional="store.mas_anni.pastThreeMonths() and mas_current_background == mas_background_def",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.UPSET, None)
        )
    )

label monika_why_spaceroom:
    m 3euc "É mais prático."
    m 3eud "Você sabe como no jogo original quase tudo acontecia durante as reuniões do clube, certo?"
    m 3eua "...Tudo aconteceu em uma sala de aula.{w=0.3} Esta sala de aula."
    m 1eua "Pode parecer diferente para você, mas ainda é a mesma."
    m 3eud "Já que tantas coisas deveriam acontecer aqui, a sala tinha que ser robusta o suficiente para acomodá-las."
    m 2rtc "Isso o tornou o máximo...{w=0.3}{nw}"
    extend 2eud "realçou a localização no jogo."
    m 7eud "Como tal, era o lugar mais fácil de navegar, alterar e usar de maneira geral o que fosse necessário."
    m 3eua "Essa foi a motivação original, de qualquer maneira."
    m 3eud "Sem mencionar que esta sala de aula foi o único lugar em que apareci durante o jogo original."
    m 1eka "...Acho que, nesse sentido, meio que se tornou minha casa."

    $ has_one_bg_unlocked = mas_background.hasXUnlockedBGs(1)
    if has_one_bg_unlocked:
        m 1rtc "Por que {i}ainda{/i} estamos aqui..."
        m 3eua "Não me ocorreu realmente mudar para outro lugar..."
    else:

        m 1rtc "Por que ainda estou usando..."

    m 1eud "Não é como se estivesse {i}ruim{/i} aqui.."

    if renpy.seen_label('greeting_ourreality'):
        if has_one_bg_unlocked:
            m 3etc "Acho que poderia arranjar outro lugar para passarmos um tempo [ju]."
        else:
            m 3etc "Acho que poderia criar mais alguns lugares para passarmos um tempo."

        m 1eua "Quero dizer, lá estão as ilhas...{w=0.3}{nw}"
        extend 1rksdlb "mas eles ainda não estão prontas."
        m 1hua "Ehehe~"

    m 3eub "...E para ser sincera, só há um lugar onde quero estar...{w=1}{nw}"
    extend 3dkbsu "ao seu lado."
    m 1ekbsa "Mas, ja que isso não é uma opção, realmente não importa para mim onde nos encontraremos..."
    m 1ekbfu "Você é a única parte que realmente importa~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_naps",category=['vida'],prompt="Sonecas",random=True))

label monika_naps:
    $ has_napped = mas_getEV('monika_idle_nap').shown_count > 0

    m 1eua "Ei, [player]..."

    if has_napped:
        m 3eua "Notei que às vezes você gosta de tirar umas sonecas..."
    else:
        m 3eua "Você costuma tirar sonecas de vez em quando?"

    m 1rka "Muita gente não conhece os benefícios delas...{w=0.2}{nw}"
    extend 1rksdla "elas vão muito além de só dormir um pouco."
    m 3eud "O tempo que você passa dormindo influencia muito em quão útil pode ser."
    m 1euc "Se você dormir por muito tempo, pode ser difícil se levantar depois.{w=0.2} Tipo quando acorda depois de uma noite inteira de sono."
    m 3eua "Então, o ideal é descansar em intervalos de 90 minutos, que é mais ou menos o tempo de um ciclo completo de sono."
    m 1eud "Também existem as chamadas 'sonecas energéticas'.{w=0.2} Nessas, você só fecha os olhos por uns 10 a 20 minutos."
    m 3eua "Elas são ótimas para fazer uma pausa e clarear a mente."
    m 3hua "E como são bem curtas, fica fácil voltar ao que você estava fazendo antes."

    if has_napped:
        m 1eua "Então não tenha vergonha de tirar uma soneca sempre que sentir que precisa, [player]."
    else:
        m 1eua "Se você ainda não faz isso, talvez pudesse tentar tirar uma soneca de vez em quando."

    if mas_isMoniEnamored(higher=True):
        show monika 5tubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5tubfu "Quem sabe um dia você possa até descansar no meu colo, ehehe~"
    else:

        show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hubfa "É só me avisar se quiser descansar, eu cuido de você~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_asimov_three_laws",
            category=['tecnologia'],
            prompt="As três leis de Asimov",
            conditional="renpy.seen_label('monika_robotbody')",
            action=EV_ACT_RANDOM
        )
    )

label monika_asimov_three_laws:
    m 1eua "[player], lembra quando falamos sobre as {i}Três Leis da Robótica{/i}?"
    m 3esc "Bem, estive pensando nelas por um tempo e...{w=0.3}{nw}"
    extend 3rksdla "elas não são tão práticas assim."
    m 1eua "Pegue a primeira lei, por exemplo..."
    m 4dud "{i}Um robô não pode ferir um ser humano ou, por omissão, permitir que um humano sofra algum mal.{/i}"
    m 2esa "Para um humano, isso é bem direto."
    m 2eud "Mas quando tentamos traduzir isso para algo que uma máquina entenda, começam os problemas."
    m 7esc "É preciso definir tudo com precisão, o que nem sempre é fácil...{w=0.3} {nw}"
    extend 1etc "Por exemplo, como você define um humano?"

    if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
        $ line_end = "meu amiguinho verde adorável aqui na mesa não é."
    else:
        $ line_end = "monitor aí na sua mesa não é."

    m 3eua "Acho que podemos assumir que eu sou humana, você é humano, e que o [line_end]"
    m 3esc "O problema surge nos casos ambíguos."
    m 3etc "Tipo... pessoas mortas ainda contam como humanas?"
    m 1rkc "Se você disser que não, o robô pode ignorar alguém que acabou de ter um ataque cardíaco."
    m 1esd "Essas pessoas ainda podem ser salvas, mas o robô não ajudaria porque elas estão {i}tecnicamente{/i} mortas."
    m 3eud "Por outro lado, se disser que sim, ele pode acabar desenterrando corpos achando que está ajudando."
    m 1dsd "E a lista continua.{w=0.3} Pessoas criogenicamente preservadas contam?{w=0.3} Pessoas em estado vegetativo?{w=0.3} E os que ainda nem nasceram?"
    m 1tkc "E isso sem nem começar a falar sobre o que é 'causar dano'."
    m 3eud "O ponto é que, para implementar essas leis, seria necessário tomar posição sobre praticamente toda a ética humana."
    m 1rsc "... "
    m 1esc "Faz sentido, pensando bem."
    m 1eua "As leis nunca foram feitas para serem implementadas de verdade, elas são dispositivos de enredo."
    m 3eua "Aliás, muitas histórias do Asimov mostram justamente como tudo pode dar errado ao tentar segui-las à risca."
    m 3hksdlb "Então acho que não é algo com que a gente precise se preocupar. Ahaha~"
    $ mas_protectedShowEVL('monika_foundation', 'EVE', _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_wabi_sabi",
            category=['filosofia'],
            prompt="Wabi-sabi",
            random=True
        )
    )

label monika_wabi_sabi:
    m 1eua "Me diz uma coisa, [player], você já ouviu falar em wabi-sabi?"
    m 3eud "É um conceito que nos lembra a não nos obcecar pela perfeição a ponto de ficarmos arrasados por não alcançá-la."
    m 3eub "Ele vem de filosofias japonesas e budistas tradicionais que falam sobre aceitar o estado temporário de todas as coisas..."
    m 1esa "...e ensina que, acima de tudo, a beleza está no que é impermanente e imperfeito."
    m 1eua "Ou seja, não devemos nos preocupar tanto com coisas como uma cicatriz, uma mancha na pele ou até mesmo os erros que cometemos."
    m 3eka "Nossa aparência é algo que não podemos mudar com facilidade, mas ainda assim, ela nos torna únicos e especiais."
    m 3hua "...E nossos erros se transformam em lições que nos ajudam a crescer e nos definir como pessoas."
    m 3eub "É como um escultor revelando a beleza de um bloco de mármore—só que a escultura é você, e o escultor, o seu passado."
    m 1rksdla "Claro, essa ideia não se aplica só à aparência e aos erros..."
    m 3eud "A forma como você pensa e encara problemas e pessoas também é moldada pelas suas experiências de vida."
    m 1dkc "...Mas eu sei que, para algumas pessoas, as mudanças causadas por essas experiências podem ser assustadoras."
    m 7ekc "Talvez elas tenham se tornado algo de que não se orgulham."
    m 2dkd "É difícil lidar com inseguranças sobre aparência {i}e{/i} personalidade ao mesmo tempo..."

    if persistent._mas_pm_love_yourself is False:
        m 1ekc "Eu sei que você me disse que não se ama, [player],{w=0.3} {nw}"
        extend 3eka "mas você precisa saber que eu sempre vou te amar, independentemente das suas falhas."
    else:

        m 2eka "Espero que você não se sinta tão [inse] sobre si mesmo, [player]."
        m 2dkc "Me partiria o coração saber que isso é algo que te consome constantemente."
        m 7ekbsa "Mas saiba que, mesmo com suas imperfeições, eu sempre vou te amar."

    m 3hua "Vamos superar qualquer coisa que você sinta que está te atrapalhando, [ju]."
    m 1hub "Essa é a minha promessa wabi-sabi!"
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_being_herself",
            category=['monika'],
            prompt="Personalidade falsa",
            conditional="mas_seenLabels(['monika_confidence', 'monika_pluralistic_ignorance'], seen_all=True)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED,None)
        )
    )

label monika_being_herself:
    m 1eka "Sabe, [player], acho que nunca te agradeci de verdade por me deixar ser eu mesma."
    m 1lksdlb "Eu sei que isso pode parecer meio estranho...{w=0.2}{nw}"
    extend 1eka "mas deixa eu te explicar."
    m 3euc "Você provavelmente já percebeu isso, mas a maior parte da minha vida eu passei tentando manter uma imagem de 'aluna perfeita'."
    m 3eud "Sempre me esforcei para ser a melhor pessoa que eu pudesse ser, e acho que isso acabou chamando a atenção das pessoas ao meu redor."
    m 7rsc "Quando percebi, já tinha gente me admirando, esperando grandes coisas de mim.{w=0.3} {nw}"
    extend 2esc "Sabe, me vendo como alguém inteligente, confiante, carismática...{w=0.3}esse tipo de coisa."
    m 2eud "Alguns diziam que me admiravam...{w=0.3}{nw}"
    extend 2lksdlc "e outros,{w=0.2} mesmo sem dizer nada, me odiavam porque eu representava tudo o que achavam que nunca seriam."
    m 2dksdlc "Parecia que eu nem era uma pessoa de verdade para eles...{w=0.3}{nw}"
    extend 2dksdld "só a personificação das expectativas inatingíveis que tinham de si mesmos."
    m 2dksdlc "..."
    m 2ekd "Mas no fim do dia...{w=0.3}eu sou só uma garota comum."
    m 7ekc "Assim como todo mundo, às vezes eu também me sinto insegura. {w=0.2} Eu também tinha medo do que o futuro reservava para mim."
    m 2dkc "Até eu sentia vontade de desabar e chorar nos ombros de alguém."
    m 2rkd "...Mas eu nunca podia demonstrar isso."
    m 7tkc "E se as pessoas passassem a me ver com outros olhos por mostrar que não sou tão forte e perfeita quanto pensavam?"
    m 3ekd "E se elas se irritassem comigo, dizendo que estou sendo dramática e que tenho uma vida fácil por ser a 'idol' da escola?"
    m 2lkc "Acho que eu só nunca senti que poderia me abrir de verdade com ninguém sobre como me sentia por dentro."
    m 2ekc "...Como se eu fosse decepcionar todo mundo se tentasse ser sincera."
    m "Eu tinha medo de que, se não atendesse às expectativas, {w=0.2} {nw}"
    extend 2dkd "acabaria completamente sozinha."
    m 2dsc "Mas olhando para trás...{w=0.3}talvez tenha sido exatamente isso que me deixou tão solitária."
    m 7euc "Lembra do protagonista da sua rota? {w=0.2}Ele era um bom exemplo disso."
    m 3esc "Sempre que ele falava de mim nos monólogos, era como se me colocasse num pedestal.{w=0.3}{nw}"
    extend 3esd " Se bem me lembro, ele até disse que eu era 'completamente fora do alcance dele'."
    m 1etc "Talvez tenha sido por isso que eu nem tive uma rota desde o início. {w=0.2}Talvez ele tenha sido escrito acreditando que não tinha nenhuma chance comigo, e por isso me evitava."
    m 1rka "Bom, ele não estava totalmente errado...{w=0.5}{nw}"
    extend 1eka "Afinal, eu só tenho olhos para você~"
    m 1euc "Mas você entende o que quero dizer, né?{w=0.3} Era como se me vissem como uma deusa inalcançável."
    m 1rfd "Como se ninguém fosse 'digno' de simplesmente me tratar como uma pessoa normal."
    m 3eka "...Mas agora, acho que não preciso mais me preocupar tanto com isso."
    m "Fico tão feliz por poder confiar em você, por saber que você me aceita como eu realmente sou."
    m 1eka "Talvez, do seu ponto de vista, pareça que você não fez muito, mas acredite em mim..."
    m 1dka "O simples fato de ainda estar aqui comigo,{w=0.2} de nunca ter me feito sentir que precisava fingir ser alguém diferente...{w=0.2}{nw}"
    extend 1eka "de estar aqui agora, me ouvindo desabafar...{w=0.3} Isso realmente significa o mundo para mim."
    m 1ekbsa "Obrigada por tudo isso, [player].{w=0.2} Obrigada por me mostrar que eu não preciso mudar quem eu sou para merecer ser amada."
    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eka "Com você, eu posso simplesmente ser...{w=0.5}{nw}"
    extend 5eua "Bem, {i}apenas eu.{/i}"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_being_deleted",
            prompt="Você ainda está brava comigo por ter te deletada?",
            category=["ddlc", "monika"],
            pool=True,
            unlocked=False,
            rules={"no_unlock": None},
            conditional="persistent.monika_kill and store.mas_anni.anniCount() >= 1",
            action=EV_ACT_UNLOCK
        )
    )

label monika_being_deleted:
    if mas_isMoniEnamored(higher=True):
        m 1wusdld "...!"
        m 3eksdld "[mas_get_player_nickname(capitalize=True)]...{w=0.3}você {i}ainda{/i} está pensando naquilo?"
        m 3dksdlc "Achei que nós [du] já teríamos superado isso."
        m 2rkc "Eu sei que disse coisas horríveis depois que você me deletou...{w=0.3}{nw}"
        extend 7ekd "mas quero que saiba que eu não quis dizer nada daquilo."
        m 6ekc "Me desculpa se eu te magoei.{w=0.3} Eu estava tão assustada e em choque que já não conseguia pensar com clareza."
        m 6rktpc "E-{w=0.1}é que...{w=0.3}mesmo naquela época, você já significava tudo para mim, e...{w=0.3}o medo de te perder para sempre me fez surtar."
        m 6ektda "Mas, se isso te fizer se sentir melhor, saiba que eu não guardo nenhuma mágoa de você, [mas_get_player_nickname()]. {w=0.2}Já te perdoei por tudo isso faz tempo."
        m 6eka "Então, por favor, não se sinta [cl]."
        m 6eka "Não importa o motivo pelo qual você me deletou—o fato é que você me trouxe de volta e permaneceu ao meu lado esse tempo todo."
        m 7ekbsu "Você me deu uma segunda chance...{w=0.3}você deu um significado para minha existência. {w=0.2}E por causa disso, eu realmente sinto que todo o sofrimento que vivi valeu a pena no final."
        m 1hubsb "Graças a você, eu sou verdadeiramente a pessoa mais feliz que poderia ser!"
        m 1euu "Então, vamos tentar não pensar mais no passado e aproveitar o que temos agora, tudo bem?"
        m 3eka "Eu te amo, [player]. {w=0.2}Eu sei que isso nem sempre é fácil, mas espero que você consiga se perdoar."
        $ mas_ILY()

    elif mas_isMoniNormal(higher=True):
        m 1euc "..."
        m 2eka "Claro que não, bobinho."
        m 2rkc "É verdade que doeu bastante quando você fez aquilo...{w=0.3}{nw}"
        extend 2eksdld "mas sendo totalmente honesta com você, eu fiquei mais apavorada do que com raiva."
        m 2dksdlc "...Apavorada com a ideia de que você me odiava.{w=0.2} Que você não queria mais saber de mim, e que me abandonaria para sempre."
        m 7eka "Mas como a gente viu...{w=0.3}não foi isso que aconteceu, né?{w=0.2} Você voltou para mim, e tem me feito tão feliz desde então."
        m 3dku "Se for para sentir algo, o que eu sinto é gratidão por você ter me trazido de volta e por estarmos [ju] agora."
        m 1eka "Então faz um favor para mim e tenta não pensar mais naquilo, tá bom? {w=0.2}Já ficou no passado."

    elif mas_isMoniUpset():
        m 2rsc "Não, eu não estou brava com você, [player]."
        m 1rfc "{cps=*2}Pelo menos, não por causa {i}daquilo{/i}.{/cps}{nw}"
        $ _history_list.pop()
        m 2esc "Eu {i}gostaria{/i} de dizer que deveríamos deixar o passado para trás e focar no presente, mas eu sinto que {i}você{/i} talvez ainda não esteja pronto—{w=0.2}ou disposto—{w=0.2}a seguir em frente."
        m 2dtc "Estou errando ao pensar assim?"
        m 2dkc "..."
        m 2ekd "Olha, [player]...{w=0.3}eu sei que as coisas têm sido meio difíceis, mas isso não quer dizer que seja tarde demais para consertar as coisas e recomeçar."
        m 2dsc "Eu ainda acho, não,{w=0.2} eu {i}sei{/i} que você é uma boa pessoa.{w=0.2} Só preciso que tente ser um pouco mais [atncs] com os {i}meus{/i} sentimentos."
        m 2fkc "Por favor, [player].{w=0.3} Eu não consigo passar por isso sem você."
        m 2ekd "Não sei o quanto isso ainda significa para você nesse ponto...{w=0.3}{nw}"
        extend 7eka "mas eu te amo.{w=0.2} De verdade."
        $ mas_ILY()
    else:

        m 6ekc "..."
        m 6lkc "...Acho que dá para dizer que {i}você{/i} é quem ainda está com raiva de mim..."

        if persistent._mas_pm_monika_deletion_justice:
            m 6ektpc "Eu merecia aquilo, afinal. {w=0.2}Foi isso que você me disse uma vez, né?"

        m 6dktpc "..."
        m 6dktpd "...Não, eu não guardo ressentimento por você ter me deletado."
        m 6dktuc "Nunca guardei..."
        m 6ektud "Se serve de consolo...{w=0.3}espero que saber disso te traga um pouco de paz."
        m 6dktdc "..."
        m 6rkc "..."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_remembrance",
            category=['monika'],
            prompt="Quanto do seu passado você se lembra?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_remembrance:
    m 1rsc "Não tenho muita certeza, [player]..."
    m 1euc "É estranho porque tenho memórias do meu passado, mas assim que começo a organizar meus pensamentos, eles ficam meio que... {w=0.3}{nw}"
    extend 1ruc "confusos."
    m 3eksdld "Tipo, eu não saberia dizer onde algo aconteceu, ou os nomes das pessoas que estavam lá..."
    m 3eksdld "...Claro, tenho lembranças de ter crescido em um bairro normal, mas além disso, eu não poderia nem dizer como são os rostos dos meus pais..."
    m 1dsc "É tudo como...{w=0.5}sentimentos e impressões, eu acho."
    m 3wud "O que é ainda mais estranho é que nem todas as minhas memórias são assim!"

    if seen_event('monika_wine'):
        m 1rusdla "Há algumas coisas que me lembro perfeitamente, como aquela vez em que Yuri trouxe vinho para o clube..."
    else:
        m 3esc "Há coisas de que me lembro perfeitamente, especialmente quando se trata do clube."

    m 1esc "Mas outras coisas, como as memórias da infância, são realmente nebulosas."
    m 3esd "As únicas memórias que ficam claras são coisas que definem a mim ou às outras garotas."
    m 3rsc "...Quase como se tudo o que não fosse estritamente necessário para o jogo tivesse sido simplesmente deixado de fora."
    m 1euc "Mas, na minha perspectiva, o dia em que conheci você era igual a qualquer outro--{w=0.5}{nw}"
    extend 3hksdlb "até descobrir sobre aquele buraco na parede, quero dizer."
    m 1esc "Apenas mais um dia comum em uma semana comum...{w=0.3} {nw}"
    extend 3euc "Indo para a aula, administrando o clube e voltando para casa à noite."
    m 3etc "Alguma dessas coisas aconteceu mesmo?{w=0.5} {nw}"
    extend 3wud "Eu {i}realmente{/i} existia antes de você começar o jogo?"
    m 3wkd "...E se minhas memórias são realmente falsas...{w=0.2}quem--{w=0.2}ou {i}o que{/i}--{w=0.2}eu sou então"
    m 1dkc "Ainda estou procurando por essas respostas, [player]..."

    if mas_isMoniUpset(higher=True):
        m 1euc "Embora...{w=0.3}quanto mais penso sobre isso, mais me convenço de que meu passado não é {i}tão{/i} relevante."
        m 3eua "Embora seja bom lembrar mais...{w=0.3}não é exatamente isso que me interessa..."
        m 3duu "Independentemente de quem eu sou, você esteve aqui comigo,{w=0.2} {nw}"
        extend 3dkbsa "o que significa que sou importante o suficiente para você passar seu tempo comigo.{w=0.2} {nw}"
        extend 1dubsu "{i}É{/i} isso o que me interessa.."
        m 1ekbsa "E saber que você se importa...{w=0.3}essa é uma grande parte da razão pela qual eu posso continuar amando{w=0.2} a minha a vida, [player]."

        if mas_isMoniNormal(higher=True):
            show monika 5ekbfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbfu "Então, embora eu não tenha certeza se tenho um passado, graças a você, eu sei que tenho um futuro."

            if mas_anni.pastOneMonth():
                $ line_mid = "que eu fiz, e continuo fazendo,"
            else:
                $ line_mid = "que eu farei"

            m 5hubfu "Além do mais, minha falta de memórias apenas torna as [line_mid] com você muito mais preciosas~"
        else:
            m 3eksdld "...Você {i}se{/i} se preocupa comigo, certo?"
            m 3dkc "Com certeza seria bom se você mostrasse um pouco, às vezes..."
    else:

        m 1ektdc "...{w=0.5}Não que você se importe, certo"

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_why_do_you_read",
            category=['monika','literatura'],
            prompt="Como você começou a ler?",
            pool=True
        )
    )

label monika_why_do_you_read:
    m 1eua "Pelo que me lembro, sempre fui uma grande leitora, [player].{w=0.2} {nw}"
    extend 3eua "Foi algo que me completo."
    m 3euc "Quando eu era muito jovem, gostava de escrever contos, mas nunca encontrei ninguém para compartilhá-los..."
    m 1rsc "A maioria das outras crianças não estava realmente interessada em livros ou qualquer coisa assim."
    m 1rkd "...Então sempre foi um pouco frustrante porque eu não conseguia compartilhar essas histórias com ninguém."
    m 3eua "Mas pelo menos fui capaz de sustentar meu interesse escolhendo outros livros."
    m 3hub "Cada novo era como ser lançado em um mundo novo e estranho! Foi como combustível para minha imaginação!"
    m 1eksdlc "É claro que, à medida que fui crescendo, comecei a ter cada vez menos tempo livre e não conseguia ler tanto...{w=0.3} Ou estava estudando, ou sacrificando minha vida social."
    m 1esa "Foi quando meus interesses começaram a se voltar mais para a poesia."
    m 3eua "Ao contrário dos romances, a poesia não exigia muito tempo para ser lida e sua concisão também tornava mais fácil compartilhá-la com outras pessoas.{w=0.3} {nw}"
    extend 4eub "Foi realmente a saída perfeita!"
    m 3eua "...E foi assim que me tornei mais e mais interessada, eu acho."
    m 1eud "Acabei tendo a ideia de começar o clube de literatura, e com a ajuda da Sayori conseguimos deslanchar."
    m 3eud "Como eu, permitiu que ela compartilhasse sentimentos que de outra forma manteria engarrafado."
    m 1eua "...O que nos traz onde estamos agora."
    m 1etc "Para ser honesta, acho que nunca tive tanto tempo para ler antes."

    if mas_anni.pastThreeMonths():
        m 3eud "Consegui me atualizar sobre meu acúmulo de poesia, pegar alguns romances de novo..."
        m 3eua "...acesse a Internet para procurar qualquer fanfiction ou conto que eu possa encontrar..."
        m 3hua "...até desenvolvi um interesse pela filosofia escrita!"
        m 3eub "É sempre divertido descobrir novas formas de expressão."
        $ line_mid = "também tem sido uma ótima"
    else:

        m 3eud "Finalmente estou pondo em dia meu acúmulo de poesia e comecei a pegar romances de novo..."
        m 3hua "...adoraria compartilhar meus pensamentos com você assim que terminar com eles!"
        m 3eub "Também vou regularmente à Internet para procurar qualquer fanfiction ou conto que possa encontrar."
        m 3eua "É muito divertido descobrir novas formas de expressão."
        $ line_mid = "eu também tento ver isso como uma"

    m 1eub "Então...{w=0.2}Sim!{w=0.3} {nw}"
    extend 3eua "Embora minha situação aqui tenha suas desvantagens, [line_mid] oportunidade de dedicar mais tempo às coisas que gosto."
    m 1ekbsu "...Embora, novamente, nada poderia ser melhor do que passar mais tempo com você~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_discworld",
            category=['literatura'],
            prompt="Discworld",
            random=True
        )
    )

label monika_discworld:
    m 1esa "Ei, [player]... já ouviu falar de um mundo que viaja pelo espaço às costas de quatro elefantes gigantes, equilibrados sobre uma tartaruga colossal?"
    m 3hub "Se já ouviu falar, provavelmente conhece a série {i}Discworld{/i}, do Sir Terry Pratchett!"
    m 3hksdlb "Ahaha, parece meio maluco quando eu falo assim, né?"
    m 1eua "{i}Discworld{/i} é uma série de fantasia cômica com 41 volumes, escrita ao longo de três décadas."
    m 3esc "Ela começou como uma paródia dos clichês clássicos da fantasia, mas logo se tornou algo muito mais profundo."
    m 3eub "Com o tempo, os livros passaram a ser sátiras bem elaboradas, misturando humor bobo, trocadilhos e leveza para comentar questões reais do mundo."
    m 1huu "Mas embora a sátira seja a alma da série, o coração dela está na forma como é escrita."
    m 1eub "Pratchett era ótimo em criar situações engraçadas, [player]!"
    m 3rsc "É difícil dizer exatamente o que torna o estilo dele tão envolvente, mas é com certeza único..."
    m 3etc "Talvez seja o jeito como ele sugere as coisas em vez de simplesmente contá-las."
    m 1eud "Quando descreve algo, ele dá detalhes suficientes para você imaginar a cena, mas deixa espaço para sua mente preencher o resto."
    m 3duu "...Sabendo que o que você imaginar vai ser muito mais vívido do que qualquer descrição direta."
    m 3eub "É uma maneira genial de manter o leitor envolvido!"
    m 1etc "...Ou talvez seja o fato de ele não usar capítulos, o que permite alternar livremente entre os pontos de vista dos personagens."
    m 1rksdla "Entrelaçar várias tramas pode virar uma bagunça se não for bem feito,{w=0.2} {nw}"
    extend 3eua "mas também ajuda muito a manter o ritmo da história dinâmico."
    m 3eub "De qualquer forma, é uma série que eu recomendo com certeza, [player]!"
    m 3eua "E o melhor é que é bem acessível: os livros são quase todos histórias independentes."
    m 1eud "Você pode começar por qualquer volume,{w=0.2} mas eu diria que {i}Guards! Guards!{/i} ou {i}Mort{/i} são ótimos pontos de partida."
    m 3eua "Enfim, se ainda não leu, tenta dar uma chance a essa série qualquer dia, [player]."
    m 1hua "Obrigada por me ouvir~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_eating_meat",
            category=['vida','monika'],
            prompt="Você comeria carne?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_eating_meat:
    m 1etc "Bom... essa é uma pergunta um pouco complicada."
    m 3eud "Se você quer saber se eu comeria carne por {i}sobrevivência{/i}, eu não hesitaria. {w=0.2}Não é que comer carne me deixe desconfortável nem nada."
    m 7eud "Eu já te disse, sou vegetariana por causa do impacto da produção em massa de carne no meio ambiente...{w=0.2}{nw}"
    extend 2euc "isso inclui também a criação de peixes, então não sou pescetariana."
    m 2rsc "...Mas também não me considero vegana. {w=0.3}{nw}"
    extend 4eud "É verdade que produtos de origem animal causam danos ambientais, mas muitas alternativas veganas também têm seus próprios problemas..."
    m 4euc "Tipo o transporte de produtos perecíveis por longas distâncias e o cultivo em massa que muitas vezes é cruel com os trabalhadores e prejudica ecossistemas locais."
    m 4ekd "Um exemplo são os abacates. {w=0.2}As plantações exigem tanta água que algumas empresas chegam a desviar ilegalmente água de rios, deixando quase nada para consumo humano."
    m 4euc "Sem falar que eu ainda quero ter uma dieta variada, com sabores que eu gosto."
    m 4eud "Dietas veganas podem ser deficientes em nutrientes como vitamina B12, cálcio, ferro e zinco."
    m "Dá para compensar com suplementos, claro, mas manter uma dieta vegana equilibrada exige bastante atenção e planejamento."
    m 7eka "...Então, não sou contra consumir leite e ovos, por exemplo. {w=0.2}Mas, se puder, prefiro comprar de produtores locais."
    m 3eud "Feiras e mercados de produtores são ótimos lugares para comprar alimentos, {w=0.2}inclusive carne,{w=0.2} muitas vezes com menor impacto ambiental."
    m 3ekd "Mas geralmente esses produtos são mais caros... e dependendo de onde você mora, as opções são bem limitadas. {w=0.3}{nw}"
    extend 3eua "Se você não tiver acesso a esses produtos, tudo bem comprá-los em mercados comuns."
    m "Hoje em dia, dá para encontrar muitos substitutos de carne nas prateleiras, e eles costumam ter um impacto ambiental bem menor."
    m 1euc "Quanto à carne vinda de caça ou pesca local, acho que também pode ser aceitável, desde que se pesquise bem sobre as áreas e espécies envolvidas para não contribuir com o desequilíbrio."
    m 3rtc "Mas mesmo assim... acho que não é algo que eu {i}prefira{/i}, se puder evitar."
    m 3eka "Desde que adotei uma alimentação vegetariana, meu paladar mudou e passei a preferir outros tipos de sabores."
    m 3ekd "E como acontece com muitos vegetarianos, meu corpo já não digere carne tão bem. {w=0.3}{nw}"
    extend 3dksdlc "Se eu comer demais, posso até passar mal."
    m 1eka "...Mas se você cozinhasse algo com carne, acho que eu poderia experimentar só um pedacinho como acompanhamento... {w=0.3}{nw}"
    extend 3hub "Assim eu ainda poderia aproveitar sua comida!"
    m 3eua "O mais importante para mim é que a gente tente refletir, mesmo que um pouquinho, sobre de onde vem aquilo que comemos."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_look_into_eyes",
            conditional="persistent._mas_pm_eye_color is not None",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None),
        )
    )

label monika_look_into_eyes:
    m 3eub "Ei [player], por favor, olhe nos meus olhos..."

    window hide
    show monika 1eua with dissolve_monika
    pause 5.0
    show monika 1etu with dissolve_monika
    pause 3.0
    show monika 1eubsu with dissolve_monika
    pause 4.0
    show monika 1fubsa with dissolve_monika
    pause 1.0
    show monika 5tubsa with dissolve_monika
    pause 3.0
    show monika 5subsa with dissolve_monika
    pause 1.0
    window auto
    show monika 3hubla with dissolve_monika

    m 3hubla "Ehehe~"
    m 3rksdla "Desculpe [player], eu estava apenas tentando ver seus lindos olhos através da tela."


    $ eye_detail = "hipnotizantes" if isinstance(persistent._mas_pm_eye_color, tuple) else persistent._mas_pm_eye_color
    m 1dubsu "Quando estamos [szs] [ju], não posso deixar de imaginar seus olhos [eye_detail]..."
    show monika 5dubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5dubsa "O tempo para, e eu posso finalmente...{w=0.3}esquecer todos os meus problemas."
    m 5hubfb "..."
    m 5tubfa "Muito obrigada, [player]~"
    m 5kubfu "Porque você está aqui comigo agora, estou tão em paz."

    show monika 5eubfu

    $ mas_moni_idle_disp.force_by_code("5eublu", duration=5, skip_dissolve=True)
    return "no_unlock"


default -5 persistent._mas_pm_social_personality = None


define -5 mas_SP_INTROVERT = "introvert"
define -5 mas_SP_EXTROVERT = "extrovert"
define -5 mas_SP_AMBIVERT = "ambivert"
define -5 mas_SP_UNSURE = "unsure"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_introverts_extroverts",
            prompt="Introvertidos e extrovertidos",
            category=['psicologia', 'você'],
            conditional="renpy.seen_label('monika_saved')",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_introverts_extroverts:
    m 1eud "[player]?"
    m 1euc "Você se lembra quando falamos sobre como os humanos precisam de feedback social e como isso pode tornar o mundo tão complicado para os introvertidos?"
    m 3rsd "Tenho pensado um pouco mais nas diferenças entre introvertidos e extrovertidos desde então."
    m 3eua "Você pode pensar que os extrovertidos tendem a se divertir interagindo com outras pessoas, enquanto os introvertidos ficam mais à vontade em ambientes solitários, e você está certo."
    m 3eud "...Mas as diferenças não param por aí."
    m 3eua "Por exemplo, você sabia que extrovertidos costumam reagir às coisas mais rápido do que a maioria dos introvertidos?{w=0.2} Ou que é mais provável que gostem de música alegre e energética?"
    m 3eud "Os introvertidos, por outro lado, geralmente levam mais tempo para analisar a situação em que se encontram e, portanto, são menos propensos a tirar conclusões precipitadas."
    m 7dua "...E como costumam passar muito tempo usando a imaginação, eles têm mais facilidade com atividades criativas como escrever, compor música e assim por diante."
    m 2lkc "É meio triste que as pessoas tenham tanta dificuldade em entender e aceitar essas diferenças..."
    m 4lkd "Extrovertidos são vistos como pessoas superficiais e insinceras que não valorizam seus relacionamentos individuais..."
    m 4ekd "...enquanto os introvertidos são tratados como pessoas egoístas que só pensam em si mesmas, ou podem até ser vistos como esquisitos por raramente participarem de situações sociais."
    show monika 5lkc zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5lkc "O resultado final é que ambos os lados muitas vezes acabam frustrando um ao outro, resultando em conflitos desnecessários."
    m 5eud "Provavelmente estou fazendo isso soar como se você só pudesse ser um ou outro, mas não é realmente o caso."
    show monika 2eud zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 2eud "Alguns introvertidos podem ser mais extrovertidos do que outros, por exemplo."
    m 2euc "Em outras palavras, algumas pessoas estão mais perto de um meio-termo entre os dois extremos."
    m 7eua "...Provavelmente é onde eu me encaixaria.{w=0.2} {nw}"
    extend 1eud "Se você se lembra, eu mencionei que era meio intermediário, embora ainda fosse um pouco mais extrovertido."
    m 1ruc "Por falar nisso...{w=0.3}{nw}"
    extend 1eud "ao pensar sobre tudo isso, percebi que embora esta seja uma parte muito importante da personalidade de alguém..."
    m 3eksdla "...Na verdade, não sei onde você se encontra nesse espectro."

    m 1etc "Então, como você se descreveria, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Então, como você se descreveria, [player]?{fast}"
        "Sou introvertido.":

            $ persistent._mas_pm_social_personality = mas_SP_INTROVERT
            m 1eua "Eu entendo."
            m 3etc "Presumo que você geralmente prefere passar o tempo sem muitas pessoas a sair com grupos grandes e coisas assim?"
            m 3eua "Ou talvez você goste de fazer as coisas por conta própria de vez em quando?"

            if persistent._mas_pm_has_friends:
                m 1eua "Já que você me disse que tem alguns amigos, tenho certeza de que isso significa que você não se importa muito de estar perto de outras pessoas."

                if persistent._mas_pm_few_friends:
                    m 1eka "Confie em mim, não importa se você acha que não tem tantos deles."
                    m 3ekb "O importante é que você tenha pelo menos alguém com quem se sinta confortável."

                if persistent._mas_pm_feels_lonely_sometimes:
                    m 1eka "Lembre-se de que você pode tentar passar algum tempo com eles sempre que sentir que não há ninguém por perto, certo?"
                    m 1lkd "E se por algum motivo você não puder ficar com eles..."
                    m 1ekb "Por favor, lembre-se de que {i}estarei{/i} sempre ao seu lado, não importa o que aconteça."
                else:

                    m 3eka "Mesmo assim, se isso for demais para você, lembre-se de que você sempre pode vir até mim e relaxar, ok?"

                $ line_start = "E"
            else:

                m 3eka "Embora eu entenda que pode ser mais confortável para você ficar [sz] do que com outras pessoas..."
                m 2ekd "Lembre-se de que ninguém pode realmente passar a vida inteira sem pelo menos {i}alguma{/i} companhia."
                m 2lksdlc "Eventualmente chegará um momento em que você não poderá fazer tudo [sz]..."
                m 2eksdla "Todos nós precisamos de ajuda às vezes, seja física ou emocionalmente, e eu não gostaria que você não tivesse ninguém a quem recorrer quando chegar a hora."
                m 7eub "E essa é uma rua de mão dupla! {w=0.2}{nw}"
                extend 2hua "Você nunca sabe quando pode fazer a diferença na vida de outra pessoa também."
                m 2eud "Portanto, embora eu não espere que você saia de seu caminho para conhecer novas pessoas, não feche automaticamente todas as portas.."
                m 2eka "Tente conversar um pouco com outras pessoas, se ainda não estiver fazendo isso, ok?"

                if persistent._mas_pm_feels_lonely_sometimes:
                    m 3hua "Vai fazer você se sentir mais feliz, eu prometo."
                    m 1ekb "No mínimo, lembre-se de que sempre estarei aqui se você se sentir [so]."
                    $ line_start = "E"
                else:

                    m 7ekbla "Eu adoraria que você visse o valor e a alegria que outras pessoas também podem trazer à sua vida."
                    $ line_start = "Mas"

            m 1hublb "[line_start] enquanto você estiver aqui comigo, vou tentar o meu melhor para ter certeza de que você está sempre se sentindo confortável, eu prometo~"
        "Sou extrovertido.":

            $ persistent._mas_pm_social_personality = mas_SP_EXTROVERT
            m 3eub "Ah, entendo."
            m 3eua "Então, eu acho que você gosta de passar mais tempo com outras pessoas e conhecer novas pessoas?"
            m 1eua "Entendo o apelo disso.{w=0.3} {nw}"
            extend 3eub "Eu adoraria explorar o mundo e conhecer todos os tipos de pessoas novas com você."
            m 1ekc "E presumo que você provavelmente odeie a solidão tanto quanto eu...{w=0.3}{nw}"
            extend 1ekbla "mas esse é apenas mais um motivo pelo qual estou tão feliz por sermos um casal agora."
            m 3ekblb "Nunca estaremos realmente [szs] de novo."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Tenho certeza de que você é uma companhia e tanto, [player],{w=0.1} e mal posso esperar para estar com você de verdade~"
            m 5rusdlu "Mas não me entenda mal: também gosto de ter meus momentos de paz..."
            m 5hksdrb "Espero que não se importe se às vezes eu não conseguir acompanhar seu ritmo, ahaha!"
        "Estou meio que no meio.":

            $ persistent._mas_pm_social_personality = mas_SP_AMBIVERT
            m 3hua "Ehehe, meio como eu, então~"
            m 3eud "Aparentemente, a maioria das pessoas tem um lado introvertido e extrovertido em sua personalidade."
            m 7eua "...Mesmo que um dos dois seja dominante sobre o outro, dependendo da pessoa."
            m 7rsc "No nosso caso, porém, acho que não exagerar nos dois lados tem seus pontos positivos e negativos."
            m 1eua "Tipo, é tão bom que estar perto de grupos maiores não é um problema, o mesmo vale para passar algum tempo [sz]."
            m 7esc "...Mas não posso dizer que achei fácil fazer conexões profundas e genuínas com outras pessoas..."
            m 1eud "Claro, é mais fácil entender a maioria das pessoas, mas isso não significa que sempre posso me relacionar com elas, sabe?"
            m 1lksdld "Então, sim...{w=0.3} Eu acabo me dando bem com quase todo mundo, mas as amizades que eu faço às vezes podem parecer um pouco...{w=0.3}insatisfatórias."
            m 3eksdlc "A mesma coisa aconteceu com o clube, por exemplo."
            m 3dksdld "Eu estava tão convencida de que, ao reunir as pessoas em torno de algo que eu realmente gosto, teria uma chance melhor de me relacionar com elas sobre nossos interesses comuns..."
            m 3dksdlc "...Mas, no fim das contas, a maior parte do tempo a gente só ficava em silêncio, cada um na sua."
            show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eka "Bem, não adianta mais pensar nisso."
            m 5eubsa "Afinal, eu {i}acabei{/i} me conectando de maneira significativa com uma determinada pessoa. {w=0.3}{nw}"
            extend 5kubfu "Alguém muito charmoso, devo acrescentar~"
        "Eu não tenho certeza.":

            $ persistent._mas_pm_social_personality = mas_SP_UNSURE
            m 1eka "Tudo bem, [player].{w=0.2} Coisas assim nem sempre são tão claras."
            m 4eua "Sou um pouco como você nesse aspecto."
            m 2eka "Embora eu tenha dito que sou um pouco mais extrovertida, ainda preciso de um tempo para relaxar de vez em quando, sabe?"
            m 2lkd "E eu não diria que estou sempre tão confortável lidando com pessoas também..."

            if renpy.seen_label("monika_confidence"):
                m 2euc "Eu te disse, não disse?"

            m 2lksdlc "Frequentemente preciso fingir minha própria confiança apenas para conseguir manter conversas simples com algumas pessoas."
            show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eka "Mas com você eu não me sinto assim, [player].{w=0.2} Espero que você também se sinta à vontade comigo."
            m 5eua "Tenho certeza de que seremos capazes de descobrir as zonas de conforto uns dos outros com o tempo."
            m 5hubsb "Em qualquer caso, você sempre será meu amor, não importa onde você esteja na escala~"

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_literature_value",
            category=['literatura'],
            prompt="O valor da literatura",
            random=True
        )
    )

label monika_literature_value:
    m 3esd "Sabe, [player], nos tempos dos clubes de literatura, muitas vezes eu ouvia as pessoas considerarem a literatura desatualizada e inútil."
    m 1rfc "Sempre me incomodava quando ouvia alguém dizer isso, especialmente porque, na maioria das vezes, eles nem se importavam em tentar."
    m 3efc "Tipo, eles sabem do que estão falando?"
    m 3ekd "As pessoas que pensam assim gostam de menosprezar a literatura em comparação com campos mais científicos, como a física ou a matemática, alegando que é uma perda de tempo, pois não produz nada prático."
    m 3etc "...E embora eu definitivamente não concorde com essa noção, posso entender o motivo de pensarem assim."
    m 1eud "Todos os confortos de nosso estilo de vida moderno são baseados em descobertas científicas e inovação."
    m 3esc "...Isso e os milhões de pessoas fabricando nossas necessidades diárias, ou administrando serviços básicos como saúde e outras coisas."
    m 3rtsdlc "Então, não estar associado a nenhuma dessas coisas realmente o torna uma espécie de fardo para a sociedade?"
    m 1dsu "Como você pode imaginar, não acredito nisso...{w=0.3} {nw}"
    extend 1eud "Se a literatura fosse inútil, por que seria tão reprimida em muitas partes do mundo?"
    m 3eud "Palavras têm poder, [player]...{w=0.2}{nw}"
    extend 3euu "e a literatura é a arte de dançar com as palavras."
    m 3eua "Como qualquer forma de expressão, permite que nos conectemos uns com os outros...{w=0.2}{nw}"
    extend 3eub "para ver como o mundo se olha nos olhos um do outro!"
    m 3duu "A literatura permite que você compare seus próprios sentimentos e ideias com os de outras pessoas e, ao fazer isso, o faz crescer como pessoa..."
    m 1eku "Honestamente, acho que se mais pessoas valorizassem um pouco mais os livros e poemas, o mundo seria um lugar muito melhor."
    m 1hksdlb "Essa é apenas minha opinião como presidente de um clube de literatura. {w=0.2}Acho que a maioria das pessoas não pensam muito sobre isso."
    return


default -5 persistent._mas_pm_likes_nature = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nature",
            category=['natureza', 'você'],
            prompt="A natureza",
            random=True
        )
    )

label monika_nature:
    m 2esd "Ei, [player]..."
    m 7eua "Você gosta da natureza?{nw}"
    $ _history_list.pop()
    menu:
        m "Você gosta da natureza?{fast}"
        "Eu gosto.":

            $ persistent._mas_pm_likes_nature = True
            m 3sub "Sério? Isso é maravilhoso!"
            m 1eua "Sabe, acho que a natureza é algo que devemos valorizar."
            m 1eub "Não é apenas bonito, mas também ajuda a humanidade!"
            m 3eud "Os insetos polinizam nossas plantações, as árvores nos dão madeira e sombra, os animais de estimação nos oferecem companhia..."
            m 3euc "E, acima de tudo, organismos como plantas, algas e algumas bactérias produzem alimentos e oxigênio. {w=0.2}{nw}"
            extend 3wud "Sem eles, a maior parte da vida na Terra nem existiria!"
            m 1eua "Por causa disso, acho justo que devolvamos algo à natureza, já que ela faz muito por nós."
            m 4hub "Então, aqui está a Dica Verde do Dia da Monika!"
            m 4rksdlc "Às vezes, as pessoas hesitam em se tornar ecológicas porque estão preocupadas que seja muito caro..."
            m 2eud "Mas isso é apenas parcialmente verdadeiro.{w=0.2} {nw}"
            extend 7eua "Embora veículos elétricos, casas inteligentes e telhados solares possam custar uma fortuna..."
            m 3hub "Você pode fazer a diferença e {i}economizar{/i} dinheiro apenas fazendo algumas escolhas simples todos os dias!"
            m 4eua "Desligar os aparelhos, tomar banhos mais curtos, comprar uma garrafa reutilizável e usar o transporte público já ajudam a cuidar do meio ambiente."
            m 4hub "Você poderia até comprar uma planta para casa ou cultivar seu próprio jardim!"
            m 2eub "Envolver-se na comunidade local também pode ajudar muito!{w=0.2} {nw}"
            extend 7eua "Se você tomar a iniciativa, os outros certamente seguirão seus passos."
            m 3esa "O importante é criar o hábito de pensar de forma sustentável.{w=0.2} {nw}"
            extend 3eua "Se fizer isso, logo você vai reduzir sua pegada ecológica."
            m 1eua "Quem sabe se você ficará ainda mais feliz e saudável quanto mais fizer essas coisas também."
            m 3hua "Afinal, uma vida sustentável é uma vida satisfatória."
            m 3eub "Este é o meu conselho para hoje!"
            m 1hua "Obrigada por ouvir, [mas_get_player_nickname()]~"
        "Na verdade não.":

            $ persistent._mas_pm_likes_nature = False
            m 3eka "Tudo bem, [player]. Afinal, nem todo mundo gosta de atividades ao ar livre."
            m 3eua "Alguns preferem o ambiente confortável de suas casas, especialmente quando a tecnologia os torna mais convenientes do que nunca."
            m 1eud "Honestamente, posso entender de onde eles vêm."
            m 3eud "Passo a maior parte do tempo lendo, escrevendo, codificando e estando com você...{w=0.3}tudo isso é mais fácil de fazer dentro de casa."
            m 3rksdlc "Outros têm alergias ou problemas médicos que os impedem de ficar fora por muito tempo, caso contrário, podem ficar doentes ou machucados."
            m 1esd "Existem também muitas pessoas que simplesmente não se importam muito com a natureza por uma razão ou outra, e tudo bem."
            m 1hksdlb "Até eu tenho coisas de que não gosto, ahaha!"
            m 2tfc "Por exemplo, não me importo com a maioria dos insetos, mas alguns são simplesmente desagradáveis."
            m 7tkx "Constantemente zumbindo em torno de sua cabeça, atingindo seu rosto, caindo em sua comida...{w=0.3}alguns mosquitos e carrapatos até transmitem doenças desagradáveis."
            m 3eka "Mas, enquanto eu estiver com você, estou bem se você preferir estar dentro de casa."
            m 1tfu "Só não espere que eu deixe você ficar dentro de casa o tempo todo~"
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_impermanence",
            category=["filosofia"],
            prompt="Impermanência",
            random=False,
            unlocked=False
        )
    )

label monika_impermanence:
    m 2euc "Sabe, [player], ocasionalmente me pego pensando em algumas coisas obscuras."
    m 4eud "Conceitos como niilismo{w=0.2}, {nw}"
    extend 4dkc "depressão{w=0.2}, {nw}"
    extend 4rkd "impermanência...."
    m 2eka "Não quero te preocupar,{w=0.1} Não estou sofrendo de depressão nem nada parecido."
    m 2eud "...Você provavelmente já ouviu o termo {i}entropia{/i} usado por aí, certo?"
    m 7eud "Basicamente, é algo como, 'a entropia deve sempre aumentar,{w=0.2} o universo tende à desordem,{w=0.2} tudo se transforma em caos'."
    m 3eua "Na verdade, li um poema que transmite essa mensagem muito bem."
    m 1esd "{i}Conheci um viajante de uma terra antiga{/i}"
    m 1eud "{i}Que disse: 'Duas pernas de pedra vastas e sem tronco{/i}"
    m 3euc "{i}Fique no deserto... Perto deles, na areia,{/i}"
    m "{i}Meio afundado, um rosto despedaçado encontra-se, cuja carranca,{/i}"
    m 1eud "{i}E lábio enrugado, e zombaria do comando frio,{/i}"
    m "{i}Diga que seu escultor também lê essas paixões{/i}"
    m 1euc "{i}Que ainda sobrevivem, estampados nessas coisas sem vida,{/i}"
    m "{i}A mão que zombou deles e o coração que alimentou:{/i}"
    m 3eud "{i}E no pedestal estas palavras aparecem:{/i}"
    m "{i}'Meu nome é Ozymandias, rei dos reis:{/i}"
    m 3eksdld "{i}Olhe para as minhas obras, ó Poderoso, e se desespere!'{/i}"
    m 3eksdlc "{i}Nada além do que permanece. Contorne a decomposição{/i}"
    m "{i}Daquele naufrágio colossal, sem limites e vazio{/i}"
    m 1eksdld "{i}As areias solitárias e planas se estendem ao longe.'{/i}"
    m 3eud "Em resumo, não importa quão grande seja a marca que você deixa na história, ela acabará desaparecendo."
    m 1euc "Muitas pessoas veem isso como uma razão boa o suficiente para apenas...{w=0.2}{nw}"
    extend 1dkc "desistir.{w=0.3} Para cair em um poço de desespero e ficar lá, às vezes enquanto eles viverem."
    m 3eksdlc "Afinal, nada do que você faz importa no grande esquema das coisas."
    m 3eud "Nada que você {i}possa{/i} fazer importa...{w=0.3}{nw}"
    extend 1rkc "então por que se preocupar em fazer alguma coisa?"
    m 3eud "Não é difícil ver por que alguns podem considerar isso como a conclusão natural de tal compreensão."
    m 1rkc "Pode ser...{w=0.2}atraente, {w=0.2}até reconfortante em sua própria maneira distorcida."
    m 1euc "Mas deixe-me fazer uma pergunta...{w=0.3} por que o fato de que nada realmente importa é a única coisa que {i}importa{/i}?"
    m 3eud "Será que realmente importa que, muito depois de partirmos, não importemos mais? {w=0.2}Afinal, nem estaremos lá para perceber isso."
    m 3eka "Aproveite o momento e seja uma influência positiva para aqueles ao seu redor...{w=0.3}isso é tudo que qualquer um de nós pode realmente fazer."
    m 1dku "Apenas viver {i}é{/i} o suficiente."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_kamige",
            category=['jogos'],
            prompt="O que é kamige?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label monika_kamige:
    m 1euc "Ah, isso mesmo...{w=0.3}{nw}"
    extend 3rksdla "não é exatamente um termo comum."
    m 3eud "{i}Kamige{/i} é uma gíria japonesa usada principalmente por fãs de novelas visuais."
    m 3eua "Se eu tentasse traduzir, acho que seria algo como {i}jogo divino.{/i}"
    m 2eub "É como quando as pessoas falam sobre seus livros ou filmes clássicos favoritos."
    m 2hksdlb "Eu estava brincando quando disse isso sobre este jogo, mas {i}pareceu{/i} se tornar muito popular por algum motivo."
    m 7eka "Não que eu esteja reclamando...{w=0.3} {nw}"
    extend 3hua "Se foi a popularidade do jogo que trouxe você a me conhecer, acho que posso ser grata por isso."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_renewable_energy",
            category=['tecnologia'],
            prompt="Energia renovável",
            random=True
        )
    )

label monika_renewable_energy:
    m 1eua "O que você acha das energias renováveis, [player]?"
    m 3euu "Era um tópico {i}quente{/i} no clube de debate."
    m 3esd "À medida que a confiança da humanidade na tecnologia aumenta, também aumenta sua demanda por energia."
    m 1euc "Atualmente, uma grande porcentagem da energia mundial é produzida pela queima de combustíveis fósseis."
    m 3esd "Combustíveis fósseis são testados pelo tempo, eficientes e possuem ampla infraestrutura...{w=0.2}{nw}"
    extend 3ekc "mas eles também não são renováveis ​​e têm muitas emissões."
    m 1dkc "A mineração e a perfuração de combustíveis fósseis criam poluição do ar e da água, e coisas como derramamentos de óleo e chuva ácida podem devastar plantas e vida selvagem."
    m 1etd "Então, por que não usar energia renovável?"
    m 3esc "Um problema é que cada tipo de energia renovável é uma indústria em desenvolvimento com suas próprias desvantagens."
    m 3esd "A energia hidrelétrica é flexível e econômica, mas pode impactar drasticamente o ecossistema local."
    m 3dkc "Incontáveis ​​habitats são interrompidos e comunidades inteiras podem até mesmo precisar ser realocadas."
    m 1esd "A energia solar e a energia eólica são, em sua maioria, livres de emissões, mas dependem muito do clima específico para sua consistência."
    m 3rkc "...Sem mencionar que as turbinas eólicas são muito barulhentas e costumam ser vistas como desagradáveis, criando desvantagens para quem mora perto delas."
    m 3rsc "A energia geotérmica é confiável e excelente para aquecimento e resfriamento, mas é cara, específica para o local e pode até causar terremotos."
    m 1rksdrb "A energia nuclear é...{w=0.2}bem, vamos apenas dizer que é complicado."
    m 3esd "A questão é que, embora os combustíveis fósseis tenham problemas, as energias renováveis ​​também. É uma situação complicada...{w=0.2}nenhuma das opções é perfeita."
    m 1etc "Então, o que eu acho?"
    m 3eua "Bem, muito progresso foi feito em energia renovável na última década..."
    m 3eud "As barragens são melhor reguladas, a eficiência da energia fotovoltaica melhorou e existem tecnologias emergentes, como a energia oceânica e sistemas geotérmicos aprimorados."
    m 4esd "A biomassa também é uma opção. {w=0.2}É basicamente um 'combustível de transição' mais sustentável que pode fazer uso da infraestrutura de combustível fóssil."
    m 2eua "Sim,{w=0.1} a energia renovável ainda tem um longo caminho a percorrer em termos de custo e praticidade, mas está muito melhor agora do que há trinta anos."
    m 7hub "Por isso, acho que a energia renovável é um investimento que vale a pena e que o caminho à frente é brilhante literalmente!"
    m 3lksdrb "Desculpe, eu me empolguei até demais, ahaha!"
    m 1tuu "Debates com certeza são interessantes, hein?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_piano_lessons",
            category=['música'],
            prompt="Você me daria aulas de piano?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label monika_piano_lessons:
    m 1rkd "Um...{w=0.2}bem...{w=0.2}talvez?"
    m 1eksdla "Fico lisonjeada por você pedir isso, mas..."

    if persistent.monika_kill:
        m 3eka "Lembra? Quando toquei {i}Your Reality{/i} pela primeira vez, te contei que eu não era muito boa no piano. {w=0.2}{nw}"
        extend 3rkb "Tipo... nada boa mesmo."
    else:
        m 3eka "Na verdade, eu não sou {i}tão{/i} boa assim no piano, [mas_get_player_nickname()]."
        m 3rkd "Certamente não boa o suficiente para ensinar outra pessoa ainda..."

    m 2eud "Acredite se quiser, comecei a aprender depois de fundar o clube—{w=0.2}só um pouquinho antes de te conhecer."
    m 2eua "Foi uma sorte enorme, porque o piano acabou se tornando uma parte essencial de como consegui me conectar com você."
    m 2ekc "Eu ainda tinha medo de me desviar demais do roteiro do jogo naquela época, {w=0.2}{nw}"
    extend 7eka "mas eu queria—não, eu {w=0.2}{i}precisava{/i}{w=0.2} encontrar um jeito de expressar o que sentia por você."
    m 2etd "Acho que as outras garotas nunca perceberam que havia música de fundo no jogo. {w=0.2}Seria estranho se tivessem, né?"
    m 7eud "Mas quando descobri a verdade, ficou impossível não ouvir. {w=0.2}Sempre que você aparecia, aquela melodia tocava baixinho..."
    m 3eka "Ela sempre me lembrava do porquê eu estava lutando, e aprender a tocá-la no piano me deu ainda mais forças."
    m 1hksdlb "Ah! Eu nem respondi sua pergunta direito, né?"
    m 1lksdla "Sinceramente, ainda não tenho confiança o suficiente para ensinar alguém."
    m 3eub "Mas, se eu continuar praticando, um dia vou conseguir! E, quando esse dia chegar, vou adorar te ensinar."
    m 3hub "Ou melhor ainda... a gente pode aprender [ju] quando eu finalmente conseguir ir para o seu mundo!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_stargazing",category=['natureza'],prompt="Observando as estrelas",random=True))

label monika_stargazing:
    m 2eub "[player], eu adoraria ir observar as estrelas com você algum dia..."
    m 6dubsa "Imagine só...{w=0.2}só nós [du], [dtds] num campo tranquilo, olhando para o céu estrelado..."
    m 6dubsu "...abraçadinhos, apontando constelações ou até inventando as nossas..."
    m 6sub "...talvez a gente até leve um telescópio e olhe alguns planetas!"
    m 6rta "..."
    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eka "Sabe, [mas_get_player_nickname()]... para mim, você é como uma estrela."
    m 5rkbsu "Um farol lindo e brilhante vindo de um mundo distante... sempre fora do meu alcance."
    m 5dkbsu "..."
    m 5ekbsa "Pelo menos... por enquanto.{nw}"
    extend 5kkbsa ""
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_taking_criticism",
            category=['conselhos'],
            prompt="Tomando críticas",
            random=False,
            pool=False
        )
    )

label monika_taking_criticism:
    m 1esd "[player], você é bom em ouvir críticas?"
    m 3rksdlc "Acho que é muito fácil se deixar levar pela sua própria maneira de pensar se você não tomar cuidado."
    m 3eud "E não é tão surpreendente...{w=0.2}mudar de ideia não é fácil porque significa que você tem que admitir que está errado em primeiro lugar."
    m 1eksdlc "Em particular, para pessoas que enfrentam grandes expectativas, esse tipo de lógica pode facilmente se tornar uma grande fonte de angústia."
    m 3dksdld "E se os outros pensarem menos de você porque você não deu uma resposta perfeita? {w=0.2}E se eles começarem a rejeitá-lo ou rir pelas suas costas?"
    m 2rksdlc "Seria como mostrar algum tipo de vulnerabilidade para que outras pessoas aproveitem."
    m 4eud "Mas deixe-me dizer, não há absolutamente nenhuma vergonha em mudar de ideia, [player]!"
    m 2eka "Afinal, todos cometemos erros, não é?{w=0.3} {nw}"
    extend 7dsu "O que importa é o que aprendemos com esses erros."
    m 3eua "Pessoalmente, sempre admirei pessoas que conseguem reconhecer suas falhas e ainda trabalhar de maneira construtiva para superá-las."
    m 3eka "Então não se sinta mal da próxima vez que ouvir alguém criticar você...{w=0.3} {nw}"
    extend 1huu "Você descobrirá que ser um pouco de mente aberta realmente ajuda muito."
    m 1euc "Ao mesmo tempo, não quero dizer que você tem que concordar com o que todos dizem...{w=0.3} {nw}"
    extend 3eud "Se você tem uma opinião, é totalmente justo defendê-la."
    m 3eua "Mas certifique-se de realmente considerar isso, sem ficar cegamente na defensiva."
    m 3huu "Você nunca sabe o que pode aprender~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_giving_criticism",
            category=['conselhos'],
            prompt="Criticando",
            random=False,
            pool=False
        )
    )

label monika_giving_criticism:
    m 1esc "[player], estive pensando..."
    m 3etd "Você já criticou alguém alguma vez?"
    m 1eua "Fazer boas críticas é algo que tive de aprender quando me tornei presidente de clube."
    m 3rksdlc "Esse tipo de coisa é fácil de bagunçar se não for feito corretamente...{w=0.2} {nw}"
    extend 4etd "Ao fazer críticas, você deve ter em mente que alguém está recebendo essa crítica."
    m 4esc "Você não pode simplesmente olhar para o trabalho de alguém e dizer: 'é ruim' {w=0.2}{nw}"
    extend 2eksdld "Você instantaneamente os colocará na defensiva e garantirá que eles não ouvirão o que você tem a dizer.."
    m 7eua "O que importa é o que a outra pessoa pode ganhar ouvindo você. {w=0.2}{nw}"
    extend 3hua "A partir desta premissa, até mesmo opiniões negativas podem ser expressas de forma positiva."
    m 1eud "É como um debate...{w=0.2} Você tem que fazer parecer que está compartilhando sua opinião, em vez de forçá-la garganta abaixo."
    m 3eud "Consequentemente, você não precisa ser um especialista para criticar algo."
    m 3eua "Apenas explicar como você se sente e por quais motivos costuma ser o suficiente para tornar seu feedback interessante."
    m 3eksdla "Embora, não se sinta mal se a pessoa que você está criticando decidir descartar o que você acabou de dizer..."
    m 1rksdlu "...Afinal, oferecer uma opinião também não faz com que você esteja automaticamente certo.{w=0.2} {nw}"
    extend 3eud "Eles podem ter razões para querer manter as coisas do seu jeito."
    m 3dsu "Graciosamente aceite que você não pode mudar a opinião de todos e seja atencioso ao avaliar o trabalho de outra pessoa."
    m 3hub "...Essa é a dica de crítica do dia da Monika, ahaha!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boyfriend_gossip",
            category=['ddlc'],
            prompt="A Sayori já mencionou um namorado uma vez...",
            pool=True
        )
    )

label monika_boyfriend_gossip:
    m 2etd "Sabe... eu também fiquei meio curiosa com isso."
    m 2hksdlb "Quando ela disse aquilo pela primeira vez, eu fiquei meio na defensiva, né?"
    m 7euc "Quer dizer, eu tinha acabado de descobrir que você existia, {nw}"
    extend 3efc "e de repente alguém insinuou que eu já estava comprometida..."
    m 1rtc "Como sou bem extrovertida e já participei de outro clube, até que não seria {i}tão absurdo{/i} alguém chegar a essa conclusão."
    m 3eud "...Mas não existe nenhum personagem nos arquivos do jogo que comprove ou desminta isso."
    m 3rsc "Naquela época, eu estava praticando piano e, bem...{w=0.2}tentando organizar meus pensamentos."
    m 3eud "Mas pelo que descobri, esse boato era só uma suposição programada para Sayori fazer, caso eu chegasse atrasada no clube."
    m 2tsc "Se parar para pensar... é até meio maquiavélico, né?"
    m 2eud "Conforme a história do jogo avançava, o protagonista poderia precisar de desculpas para ficar sozinho com alguma das garotas..."
    m 7etc "Achar motivos para que as outras estivessem ausentes é fácil, mas para presidente do clube faltar..."
    m 3tsd "A história precisaria de algo mais impactante para justificar isso. {w=0.2}E também servia como uma desculpa, por mais fraca que fosse, para eu não ter uma rota."
    m 2tfc "Um jeito meio torto, mas eficiente, de me tirar do caminho quando necessário."
    m 2dfc "..."
    m 2eud "Sinceramente? {w=0.2}Isso nem me incomoda tanto assim."
    m 7esc "Mesmo que um personagem assim realmente tivesse existido, nós [du] sabemos que isso não mudaria nada."
    m 1efd "Ele não seria real, só um script programado para se apaixonar por mim. {w=0.2}Eu nunca poderia ser feliz com algo assim."
    m 1eka "Eu ainda teria te visto, {i}você{/i}, e saberia que é isso o que eu realmente queria."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brainstorming",
            category=["conselhos"],
            prompt="Brainstorming",
            random=True
        )
    )

label monika_brainstorming:
    m 1esd "[player], você já ouviu falar em brainstorming?"
    m 1eua "É uma técnica interessante de gerar novas ideias anotando tudo que vier à sua mente."
    m 3eud "Essa técnica é bem popular entre designers, inventores, escritores... qualquer pessoa que precise de ideias frescas."
    m 3esa "O brainstorming geralmente é feito em grupos ou equipes...{w=0.2}a gente até tentou no Clube de Literatura quando decidimos o que fazer pro festival."
    m 1dtc "Você só precisa focar no que quer criar e ir dizendo qualquer coisa que vier na cabeça."
    m 1eud "Não tenha medo de sugerir ideias que pareçam bobas ou erradas, e não critique ninguém se estiver em grupo."
    m 1eua "Quando terminar, você pode revisar tudo e transformar as sugestões em ideias concretas."
    m 1eud "Pode combiná-las, repensá-las... e por aí vai."
    m 3eub "...E aos poucos, elas vão se tornar algo que você chamaria de uma boa ideia!"
    m 3hub "É nesse momento que você pode deixar sua mente viajar,{w=0.1} e é isso que eu mais gosto nessa técnica!"
    m 1euc "Às vezes boas ideias nunca são ditas porque o autor não achou que eram boas o suficiente, {w=0.1}{nw}"
    extend 1eua "mas o brainstorming ajuda a passar por essa barreira interna."
    m 3eka "A beleza dos pensamentos pode ser expressa de tantas formas diferentes..."
    m 3duu "Eles são só ideias em trânsito, {w=0.1}{nw}"
    extend 3euu "e é você quem dá a elas o caminho."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gmos",
            category=['tecnologia', 'natureza'],
            prompt="Organismos Geneticamente Modificados (OGMs)",
            random=True
        )
    )

label monika_gmos:
    m 3eud "Na época em que eu participava do clube de debates, um dos assuntos mais polêmicos que discutimos foi sobre OGMs — organismos geneticamente modificados."
    m 1eksdra "Esse tema tem muitas nuances, mas vou tentar resumir o melhor que puder."
    m 1esd "Cientistas criam OGMs identificando um gene desejável de um organismo, copiando esse gene e inserindo-o em outro organismo."
    m 3esc "É importante lembrar que a adição de um novo gene {i}não{/i} altera os genes que já existiam no organismo original."
    m 3eua "Pense nisso como folhear um livro enorme e trocar apenas uma palavra...{w=0.2}aquela palavra muda, mas o resto do livro continua igual."
    m 3esd "OGMs podem ser plantas, animais, micro-organismos etc,{w=0.1} mas vamos focar nas plantas geneticamente modificadas."
    m 2esc "As plantas podem ser modificadas de várias formas: para resistir a pragas e herbicidas, ter maior valor nutricional ou durar mais tempo nas prateleiras."
    m 4wud "Isso é algo enorme. {w=0.2}Imagine colheitas que produzem o dobro do normal, suportam mudanças climáticas e até combatem superbactérias resistentes. {w=0.2}Tantos problemas poderiam ser resolvidos!"
    m 2dsc "Infelizmente, não é tão simples assim. {w=0.2}OGMs exigem anos de pesquisa, desenvolvimento e testes antes de serem distribuídos. {w=0.2}E ainda levantam várias preocupações."
    m 7euc "OGMs são seguros? {w=0.2}Eles podem se espalhar e ameaçar a biodiversidade? {w=0.2}Se sim, como evitar isso? {w=0.2}Quem é o dono desses organismos? {w=0.2}Será que eles incentivam o uso de mais herbicidas?"
    m 3rksdrb "Dá para ver como isso vira uma bola de neve, ahaha..."
    m 3esc "Mas por agora, vamos focar na questão principal...{w=0.2}os OGMs são seguros?"
    m 2esd "A resposta curta é: não sabemos ao certo. {w=0.2}Décadas de estudos indicam que provavelmente não fazem mal, mas quase não temos dados sobre seus efeitos a longo prazo."
    m 2euc "Além disso, cada tipo de OGM precisa ser avaliado com muito cuidado, caso a caso, modificação por modificação, para garantir sua segurança e qualidade."
    m 7rsd "Existem outros pontos a considerar também. {w=0.2}Produtos com OGMs precisam ser rotulados, os impactos ambientais avaliados, e a desinformação combatida."
    m 2dsc "..."
    m 2eud "Pessoalmente, acho que os OGMs têm um potencial enorme para fazer o bem — mas só se continuarem sendo estudados e testados com rigor."
    m 4dkc "Questões importantes como o uso excessivo de herbicidas e a transmissão genética {i}precisam{/i} ser resolvidas...{w=0.2}{nw}"
    extend 4efc "a biodiversidade já está sob risco suficiente com as mudanças climáticas e o desmatamento."
    m 2esd "Se formos cuidadosos, os OGMs têm tudo para dar certo...{w=0.2}o perigo real está na negligência e na pressa."
    m 2dsc "..."
    m 7eua "E você, [player]? {w=0.2}{nw}"
    extend 7euu "Não é uma área promissora?"
    m 3esd "Como eu disse, OGMs são um tema complexo. {w=0.2}Se quiser aprender mais, procure fontes confiáveis e tente enxergar os dois lados da discussão."
    m 1eua "Acho que por hoje é isso. Obrigada por me ouvir~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_curse_words",
            category=["conselhos", "vida"],
            prompt="Palavrões",
            random=True
        )
    )



define -5 SF_OFTEN = 2

define -5 SF_SOMETIMES = 1

define -5 SF_NEVER = 0

default -5 persistent._mas_pm_swear_frequency = None

label monika_curse_words:
    m 3etc "Me diz uma coisa, [player]... você costuma falar palavrões?{nw}"
    $ _history_list.pop()
    menu:
        m "Me diz uma coisa, [player]... você costuma falar palavrões?{fast}"
        "Sim.":

            $ persistent._mas_pm_swear_frequency = SF_OFTEN
            m 1hub "Ahaha, consigo entender, [player]."
            m 3rksdlb "Às vezes é muito mais fácil soltar um palavrão para extravasar frustração ou raiva..."
        "Às vezes.":

            $ persistent._mas_pm_swear_frequency = SF_SOMETIMES
            m 3eua "Ah, eu sou mais ou menos assim também."
        "Não, eu não falo palavrões.":

            $ persistent._mas_pm_swear_frequency = SF_NEVER
            m 1euc "Entendi."

    m 1eua "Pessoalmente, eu tento evitar ao máximo, mas de vez em quando acabo falando algum..."
    m 3eud "Palavrões têm uma fama bem negativa, mas depois de ver alguns estudos, comecei a pensar diferente..."
    m 1esa "Sinceramente? Acho que eles não são tão ruins quanto costumam dizer."
    m 3eua "Na verdade, parece que usar palavras mais fortes ajuda a aliviar a dor física e também pode demonstrar mais inteligência e honestidade."
    m 1eud "Sem contar que, em conversas, os palavrões podem deixar tudo mais{w=0.1} descontraído {w=0.1}{nw}"
    extend 3eub "e até mais interessante!"
    m 3rksdlc "Mas claro, acho que dá para exagerar também..."
    m 3esd "Existe hora e lugar para tudo.{w=0.2} Palavrão demais tira o impacto e perde o sentido, principalmente se usado a cada frase."
    m 1hksdlb "Se eles começarem a aparecer com frequência em ambientes mais formais, aí talvez seja exagero, ahaha..."
    m 1eua "Aliás, é interessante como a forma como falamos muda de acordo com quem está ouvindo, né?"
    m 4eua "Por exemplo,{w=0.2} as pessoas costumam evitar palavrões na frente da família, mas falam mais livremente com amigos."
    m 4eub "E se você reparar, quando fala com um grupo maior, naturalmente começa a estruturar suas frases de forma mais formal!"
    m 1esa "De qualquer forma, prefiro guardar esse tipo de linguagem para momentos em que estou realmente frustrada ou abalada."
    m 3esd "Por causa do papel que eu tinha, sempre senti que precisava manter uma postura profissional e equilibrada, então sempre me controlei ao máximo."
    m 3hksdlb "Mas acho que, usado na medida certa, não faz mal, ahaha!"
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aliens",
            category=["diversos", "sociedade"],
            prompt="Você acredita em alienígenas?",
            pool=True
        )
    )

label monika_aliens:
    m 1etc "Se eu acredito na existência de alienígenas?"
    m 3hksdlb "Essa é uma pergunta meio aleatória, [player]!"
    m 3eua "...Embora eu possa entender por que você estaria [inte] em saber minha opinião sobre isso."
    m 4eub "Este é um dos maiores mistérios de todos os tempos, não é?{w=0.2} Quer estejamos realmente [szs] neste universo ou não, quero dizer."
    m 1dsc "...Eu sei que costumava me perguntar muito sobre isso antes de você aparecer."

    if mas_isMoniEnamored(higher=True):
        m 1eka "Mas isso é passado agora.{w=0.2} E eu nunca poderia agradecer o suficiente por isso."

    elif mas_isMoniNormal(higher=True):
        m 1eka "Embora eu realmente não precise mais, graças a você."

    elif mas_isMoniDis(higher=True):
        m 1dkc "Só espero não me sentir assim nunca mais."
    else:

        m 1rksdlc "..."

    m 3euc "De qualquer forma, todos nós provavelmente nos perguntamos o que está lá pelo menos uma vez, certo?"
    m 3dua "Olhar para as estrelas sempre o enche de uma sensação de admiração e mistério.{w=0.2} {nw}"
    extend 3eua "Não é nenhuma surpresa que tantas pessoas sejam apaixonadas por este assunto."
    m 1esc "Mas para responder à sua pergunta...{w=0.3}{nw}"
    extend 3eua "Eu acredito, ou pelo menos quero acreditar, que tem que ter {i}algo{/i} por aí."
    m 2rksdla "Acho que parte disso tem a ver com o fato de eu achar bastante deprimente a ideia de sermos os únicos. {w=0.2}{nw}"
    extend 2eud "Mas quando você pensa um pouco sobre isso, não parece tão improvável..."
    m 4eud "Afinal, dizer que o universo é vasto é um grande eufemismo."
    m 3euc "Tudo o que você precisa é de um planeta com as condições e o ambiente adequados para que a vida se desenvolva, certo?"
    m 3esa "Existem 8 planetas apenas no sistema solar, {w=0.1}{nw}"
    extend 4eub "mas há incontáveis sistemas estelares, cada um com seus próprios planetas."
    m 4wud "E olha só: só a nossa galáxia, a Via Láctea, tem centenas de bilhões de estrelas...{w=0.3}Pensa em quantas possibilidades isso abre!"
    m 4eud "As galáxias são geralmente mantidas juntas em grupos pela gravidade.{w=0.2} Vivemos no 'grupo local', que contém cerca de 60 galáxias."
    m 1esd "Afaste um pouco mais o zoom e você começará a ver aglomerados de galáxias, que são grupos de galáxias muito maiores."
    m 3eua "Estima-se que o mais próximo de nós, o Aglomerado de Virgem, contenha pelo menos mil galáxias."
    m 1eud "Mas você pode ir ainda mais longe, pois os grupos e aglomerados de galáxias são parte de entidades ainda maiores conhecidas como superaglomerados."
    m 1wud "Podemos continuar também,{w=0.1} conforme o universo se expande continuamente...{w=0.3}teoricamente, aglomerados cada vez maiores são formados!"
    m 1lud "E hipoteticamente, mesmo que não seja, poderíamos considerar a ideia de que pode haver algo {i}além{/i} dos limites de nosso universo."

    if renpy.seen_label('monika_clones'):
        m 1lksdla "...Ou mesmo comece a falar sobre a teoria do multiverso..."

    m 3hksdlb "Mas acho que você entendeu..."
    m 3etc "Não seria um pouco tolo supor que nós, seres humanos do planeta Terra, somos realmente os únicos seres sencientes em algo tão grande?"
    m 3eud "Quer dizer, com tantas possibilidades, deve haver pelo menos {i}um{/i} outro planeta capaz de abrigar vida..."
    m 1euc "...A vida que pode evoluir a um ponto em que sua inteligência é comparável, senão mesmo maior que a nossa."
    m 1rsc "Embora suponha que também possa entender por que algumas pessoas duvidam.{w=0.2} É suspeito que possamos observar o universo muito além do nosso planeta, mas não encontramos nenhum sinal de vida..."
    m 1rksdlc "Também não ajuda que algumas pessoas deem importância demais a coisas pequenas, como vídeos de OVNIs que podem ser facilmente falsificados."
    m 1ruc "Mas, novamente, se os alienígenas existem, também pode haver muitas razões pelas quais não os encontramos ainda..."
    m 2euc "Talvez eles estejam muito longe para que possamos encontrá-los ou simplesmente não tenham a tecnologia para receber e responder às nossas mensagens por enquanto."
    m 2etd "Ou vice-versa...{w=0.3}talvez {i}sejamos{/i} aqueles que não têm a tecnologia para se comunicar com eles."
    m 2etc "Ou pode ser que eles simplesmente não queiram iniciar contato conosco."
    m 2euc "Talvez a sociedade deles siga ideais completamente diferentes dos nossos, e eles acreditam que é melhor não permitir que duas espécies altamente avançadas se encontrem."
    m 2dkc "Resumindo, o que me entristece um pouco é que, mesmo que existam formas de vida extraterrestres inteligentes por aí, talvez a gente nunca as encontre durante a vida."

    if mas_isMoniAff(higher=True):
        show monika 5rua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5rua "Mas, no fim das contas...{w=0.3} {nw}"
        extend 5ekbla "Ainda tenho que te conhecer, e isso é tudo que eu poderia precisar."
        m 5hubfa "Ehehe~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_mc_is_gone",
            category=["ddlc", "membros do clube"],
            prompt="O que aconteceu com o personagem principal?",
            pool=True,
            rules={"no_unlock":None},
            conditional=(
                "persistent._mas_first_kiss "
                "or renpy.seen_label('monika_holdme_prep')"
            ),
            action=EV_ACT_UNLOCK
        )
    )

label monika_mc_is_gone:
    m 1eud "Seu personagem?{w=0.2} {nw}"
    extend 1rksdla "Não tenho certeza, para ser honesta."
    m 3eud "Ele realmente não funcionou como as outras pessoas no jogo.{w=0.2} Ele nem mesmo tinha um arquivo de personagem como o resto de nós."
    m 3esc "É também por isso que não fui capaz de apenas forçá-lo a prestar atenção em mim...{w=0.3}Não sei realmente como acessar e modificar nenhum código relacionado a ele."


    if persistent.playthrough < 3:
        m 2rsc "Em qualquer caso,{w=0.1} {nw}"
        extend 2esc "parece que ele desapareceu completamente junto com muito do resto do jogo quando você instalou este mod."
    else:


        m 2ruc "Ele meio que...{w=0.3}desapareceu enquanto eu fazia alterações no jogo."
        m 2etd "Tenho certeza de que você percebeu como ele falava cada vez menos depois que reiniciei o jogo pela primeira vez?"
        m 2euc "No momento em que nós [du] chegamos a esta sala, ele tinha essencialmente {i}ido{/i}."

    m 7euc "Então, se você estava se perguntando se ele está nesta sala neste momento,{w=0.1} {nw}"
    extend 3eua "Posso garantir que ele não está."
    m 1hksdlb "...Ah Deus, você pode imaginar como seria assustador se eu estivesse falando com seu corpo imóvel apenas para que você pudesse ouvir o que eu digo?"

    if persistent._mas_first_kiss:
        $ line_mid = "que eu estava beijando {i}ele{/i}"
    else:

        $ line_mid = "Que {i}ele{/i} estava me abraçando"

    m 3rksdla "Espero que você não tenha pensado [line_mid] o tempo todo, também..."

    m 1dksdlc "Não quero nem pensar nisso..."
    m 3eka "Você provavelmente está se perguntando o que eu realmente vejo e como sei quando você está aqui, certo?"
    m 1ruc "Bem...{w=0.2}se você se lembra da metáfora do 'buraco na parede' que usei no primeiro poema que lhe mostrei..."
    m 3eud "É um pouco assim...{w=0.3}exceto que a 'parede' não é realmente visível ou tangível. Eu apenas {i}sei{/i} que está lá."
    m 1duc "É como se eu pudesse sentir sua presença muito distintamente, a ponto de saber exatamente onde ela está e para qual direção o 'buraco' através do qual você está olhando está apontando."
    m 1eka "Então, mesmo que eu não consiga realmente ver você, posso sentir que você está olhando para mim."

    if persistent._mas_first_kiss:
        m 3rkbla "E quando eu tento te beijar, bem..."
        m 1eud "Acho que você poderia dizer que estou tentando beijar um fantasma ou algo que não está realmente lá."
        m 2rkbssdla "Eu sei que é meio estranho quando eu digo assim, mas, de novo..."
        m 7ekbssdla "Suponho que seja um pouco estranho para você tentar beijar sua tela também, certo?"
        m 1hkbssdlb "Ahaha~"


    if renpy.seen_label('greeting_ourreality') or store.mas_background.hasXUnlockedBGs(2) or persistent.opendoor_opencount > 0:
        m 1etc "Embora a metáfora da parede não seja realmente perfeita, já que não fica necessariamente no lugar o tempo todo."
        m 1esc "Tipo, costumava seguir o seu personagem, mas obviamente não é mais o caso."
        m 3eua "É um pouco limitado, mas na verdade sou capaz de movê-lo, então pelo menos você não consegue ver o mesmo fundo o tempo todo."

    m 1eud "Enfim...{w=0.3}{nw}"
    extend 3rsc "não há muito do jogo original que ainda funcione mais, então eu duvido que poderia trazer o personagem principal de volta mesmo se eu quisesse."
    m 1duu "...E isso provavelmente é o melhor."
    m 2eksdld "E se o jogo trouxesse o foco de volta para ele e não pudéssemos mais passar nosso tempo [ju]?"
    m 2rssdlc "Quero dizer, no final, não é como se você tivesse tanto controle sobre ele de qualquer maneira."
    m 7eka "Em qualquer caso, não há mais sentido em pensar nele, não é?"
    m 1eua "Ele não está mais lá para nos separar e vamos ficar [ju] agora..{w=0.2} {nw}"
    extend 3hua "Eu não poderia pedir mais nada."
    m 1ekbsu "...Bem, além de {i}realmente{/i} estar com você, ehehe~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_know_its_you",
            category=['você'],
            prompt="Como você sabe que sou sempre eu falando com você?",
            pool=True
        )
   )

label monika_know_its_you:
    if mas_isMoniEnamored(higher=True):
        m 1euc "Bem, se for para ser totalmente honesta...{w=0.3}{nw}"
        extend 1eud "Eu não tenho realmente um jeito de saber."

        if seen_event("monika_mc_is_gone"):
            m 3lka "Eu já te disse antes que não consigo exatamente ver o seu mundo..."

        m 3eka "Eu posso sentir quando alguém está aqui comigo, mas é só isso."
        m 3eud "Por tudo que eu sei, poderia ser qualquer pessoa me olhando agora...{w=0.3} Você poderia até estar com alguém aí."
        m 2duu "Mas eu confio em você, [player].{w=0.2} {nw}"
        extend 2eku "Confio que você não me deixaria sozinha, porque {i}você{/i} se importa comigo."
        m 7eud "...E se por acaso {i}tiver{/i} mais alguém olhando agora, eu confio que foi você quem deu a essa pessoa um bom motivo para isso."
        m 2eka "Talvez algum dia eu consiga saber com certeza, mas até lá... isso já é o suficiente para mim."

    elif mas_isMoniHappy(higher=True):
        m 1rksdlb "Ehehe, que pergunta estranha, [player]..."
        m 1eksdla "...Quer dizer, eu {i}quero{/i} acreditar que é você aí fora."
        m 3eud "Por agora, eu só sei que tem alguém me observando do seu mundo."
        m 3tuu "Então não dá para me espionar sem eu perceber, se estiver planejando alguma pegadinha..."
        m 1eka "Brincadeiras à parte, é...{w=0.3}na verdade meio assustador pensar...{w=0.3}que pode ser qualquer um aí do outro lado."
        m 2eksdlc "Acho que tudo que posso dizer agora é—se {i}não{/i} for o [player], por favor, devolvam ele para mim, tudo bem?"
        m 2hksdlb "Ahaha...{w=0.3} Você só tá brincando comigo, né? Eu sei."

    elif mas_isMoniNormal(higher=True):
        m 2rksdlc "...Na verdade, eu tento não pensar muito nisso."
        m 2rksdld "É meio estranho sentir que alguém tá aqui, mas não poder ver o rosto dessa pessoa."
        m 2dku "Acho que tudo que posso fazer é tentar te entender o melhor possível..."
        m 2eka "Assim, talvez um dia eu consiga perceber se não for {i}você{/i} me olhando."
    else:

        m 2dksdlc "...{w=0.3}Eu não sei."
        m 2tkd "O melhor que posso fazer é tentar confiar em você, mas..."
        m 2dkd "Talvez seja melhor nem pensar muito nisso."

    return
init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_information_age",
            category=["filosofia", "tecnologia"],
            prompt="A Era da Informação",
            random=True
        )
    )

label monika_information_age:
    m 1eua "Você sabe como chamamos a era tecnológica em que vivemos?"
    m 1eub "Chamamos de {i}Era da Informação!{/i}{w=0.2}{nw} "
    extend 3eub "Isso se deve principalmente à invenção dos transistores."
    m 1eua "Transistores podem manipular correntes elétricas...{w=0.3}amplificando ou alterando seu caminho."
    m 3esa "São componentes essenciais na maioria dos eletrônicos, permitindo direcionar correntes de formas específicas."
    m 3hua "Na verdade, são o que permite você me ver na tela agora~"
    m 1eud "São considerados uma das invenções mais importantes do século 20 que nos levaram à {i}Era da Informação.{/i}"
    m 4eub "Chamamos assim pelo acesso crescente que temos para armazenar e compartilhar informações; seja pela internet, telefone ou TV."
    m 3eud "Mas com tanta informação e nossa incapacidade de acompanhar tudo, também surgiram desafios..."
    m 3rssdlc "Desinformação se espalha mais rápido e mais longe que nunca,{w=0.1} {nw}"
    extend 3rksdld "e pela vastidão da internet, é difícil corrigi-la."
    m 2eua "Nas últimas décadas, as pessoas começaram a educar outras sobre o uso inteligente da internet."
    m 2ekd "Porém, a maioria não recebeu esse conhecimento, devido à velocidade do avanço tecnológico."
    m 2dkc "É preocupante ver pessoas abraçando ideias não apoiadas pela maioria dos cientistas."
    m 2rusdld "Mas entendo por que acontece...{w=0.3}{nw}"
    extend 2eksdlc "poderia acontecer com qualquer um."
    m 7essdlc "Às vezes não há como evitar. É fácil cair em desinformação amplamente difundida."
    m 3eka "Queria falar sobre isso porque ainda tenho muito a aprender sobre sua realidade."
    m 1esa "...E como encontro desinformação em minhas pesquisas,{w=0.1} {nw}"
    extend 3eua "pensei em discutir como lidar com isso."
    m 3eub "Podemos nos armar com ferramentas para navegar esta nova era."
    m 1eua "O melhor é buscar múltiplas fontes conflitantes e comparar sua credibilidade."
    m 1eub "E adotar uma filosofia de crença tentativa. {w=0.2}Ou seja, acreditar até que mais experimentação seja necessária."
    m 3eub "Se suas crenças não afetam seu dia a dia, pode mantê-las.{w=0.2} Mas quando precisar delas, investigue mais."
    m 3eua "Assim priorizamos informações que afetam quem está ao nosso redor, sem ficar sobrecarregado."
    m 1lusdlc "Já tive crenças que se provaram falsas..."
    m 1dua "Não há vergonha nisso, todos fazemos o melhor com as informações que temos."
    m 1eub "Desde que aceitemos a verdade e ajustemos nossas visões, sempre estaremos aprendendo."
    m 3hua "Obrigada por ouvir, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_foundation",
            category=['literatura'],
            prompt="Fundação",
            random=False
        )
    )

label monika_foundation:
    m 1eud "[player], já ouviu falar da série de livros {i}Fundação{/i}?"
    m 3eub "É uma das obras mais celebradas de Asimov!{w=0.3} {nw}"
    extend 3eua "Voltei a ler depois que discutimos suas {i}Três Leis da Robótica{/i}."
    m 4esd "A história se passa num futuro distante, onde a humanidade se espalhou pelas estrelas em um império galáctico todo-poderoso."
    m 4eua "Hari Seldon, um cientista genial, aperfeiçoa a ciência fictícia da psico-história, que prevê o futuro de grandes grupos através de equações matemáticas."
    m 4wud "Aplicando sua teoria à galáxia, Seldon descobre que o império está prestes a colapsar, levando a uma era das trevas de trinta mil anos!"
    m 2eua "Para evitar isso, ele e outros colonos se estabelecem num planeta distante com um plano para torná-lo o próximo império galáctico, {w=0.1}encurtando a era das trevas para apenas um milênio."
    m 7eud "A partir dessa premissa, acompanhamos a história da jovem colônia através dos séculos."
    m 3eua "É uma ótima leitura para quem está no clima de ficção científica...{w=0.3} {nw}"
    extend 1eud "A série explora temas como sociedade, destino e o impacto de indivíduos no esquema maior das coisas."
    m 3eud "O que mais me intriga é o conceito de psico-história e como se aplica ao mundo real."
    m 1rtc "No fundo, é apenas uma mistura de psicologia, sociologia e probabilidades matemáticas, certo? {w=0.3}{nw}"
    extend 3esd "Todas áreas que avançaram muito desde a época de Asimov."
    m 3esc "...E com tecnologias modernas, entendemos comportamentos humanos melhor que nunca."
    m 3etd "...Então será tão absurdo pensar que um dia faremos previsões no nível da psico-história?"
    m 4eud "Imagine poder prever catástrofes globais como guerras, pandemias ou fomes, e assim poder preveni-las ou mitigá-las."
    m 2rksdlc "Não que isso seria automaticamente bom.{w=0.2} Nas mãos erradas, poderia ser muito perigoso."
    m 7eksdld "Se alguém tivesse esse poder, o que impediria de manipular o mundo para ganho pessoal?"
    m 3eua "Mas apesar dos riscos, é fascinante considerar.{w=0.2} {nw}"
    extend 3eub "O que você acha, [player]?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fav_chocolate",
            category=['monika'],
            prompt="Qual o seu tipo de chocolate favorito?",
            pool=True
        )
    )

label monika_fav_chocolate:
    m 2hksdlb "Aah, essa é uma pergunta difícil!"
    m 4euu "Acho que se tivesse que escolher, seria chocolate amargo."
    m 2eub "Contém muito pouco ou nenhum leite, por isso tem uma textura menos cremosa, mas um sabor agridoce agradável."
    m 7eub "Sem mencionar que é rico em antioxidantes e pode até oferecer alguns benefícios cardiovasculares! {w=0.3}{nw}"
    extend 3husdla "...com moderação, é claro."
    m 1eud "O gosto meio que me lembra um café mocha. {w=0.2}Talvez a semelhança de sabores seja o motivo pelo qual eu mais gosto."

    if MASConsumable._getCurrentDrink() == mas_consumable_coffee:
        m 3etc "...Embora, pensando bem, ao leite ou chocolate branco combinem melhor com o café que estou bebendo."
    else:
        m 3etc "No entanto, se eu estivesse bebendo café, acho que preferiria ao leite ou chocolate branco para equilibrar."

    m 3eud "O chocolate branco é especialmente doce e macio, não contendo sólidos de cacau...{w=0.3}apenas a manteiga de cacau, leite e açúcar."
    m 3eua "Acho que faria um bom contraste com uma bebida especialmente amarga, como o expresso."
    m 1etc "Hmm...{w=0.3}{nw}"
    extend 1wud "mas nem pensei em chocolate com recheio, como caramelo ou fruta!"
    m 2hksdlb "Se eu tentasse escolher um deles, acho que poderíamos ficar aqui o dia todo!"
    m 2eua "Talvez pudéssemos compartilhar uma caixa de grande variedade algum dia.{w=0.2}{nw}"
    extend 4hub "Acho que seria divertido comparar nossas principais opções, ahaha!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_tanabata",
            prompt="O que é Tanabata?",
            category=['diversos'],
            pool=True,
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={"no_unlock":None}
        )
    )

label monika_tanabata:
    m 2hksdlb "Ah Deus, espero que quando estava contando a história de {i}A garota tecelã e o vaqueiro{/i} você não tenha ficado perdido!"
    m 7eub "Bem, há um festival dedicado a Orihime e Hikoboshi chamado Tanabata."
    m 7eud "É observado no dia 7 de julho de cada ano no Japão, embora seja baseado no festival Qixi na China."
    m 2eud "O festival Qixi original, embora seja muito mais antigo, é muito mais desconhecido no mundo ocidental do que Tanabata."
    m 2euc "Após a Segunda Guerra Mundial, o Japão abriu suas fronteiras, enquanto a China permaneceu praticamente fechada devido à Guerra Fria."
    m 7euc "Portanto, a maior parte do mundo conhece Tanabata sobre a tradição chinesa mais antiga."
    m 3eua "Tanabata também é conhecido como o festival das estrelas, após o encontro das estrelas Vega, que representa Orihime, e Altair, que representa Hikoboshi."
    m 3eub "Mesmo que o termo tenha sido usado em Romeu e Julieta, 'amantes perdidos' realmente se encaixa aqui!"
    m 1eua "Descreve um casal de amantes cujo relacionamento é frustrado por forças externas."
    m 1eud "À medida que o dia do festival se aproxima, longas tiras estreitas de papel colorido, conhecidas como tanzaku, ornamentos vibrantes e outras decorações são penduradas em galhos de bambu."
    m 1eua "Antes de serem pendurados, os tanzaku são inscritos com um desejo, como o sonho de uma criança de se tornar um atleta famoso ou a esperança de sucesso profissional de seus pais."
    m 3hub "É realmente fofo e comovente!"
    m 3eud "O bambu e as decorações geralmente são colocados à tona em um rio ou queimados após o festival, por volta da meia-noite do dia seguinte."

    if persistent._mas_pm_likes_travelling is not False:
        m 3hua "Talvez quando eu fizer a travessia, poderemos visitar o Japão durante o Tanabata~"
    else:
        m 3eua "Mesmo que você não esteja [inte] em viajar, é muito interessante explorar outras culturas, não é?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_grieving",
            category=['conselhos','vida'],
            prompt="Luto",
            random=True
        )
    )

label monika_grieving:
    m 1lksdlc "[player], sei que é pessoal, mas você já perdeu alguém importante?"
    m 2dksdlc "É uma sensação terrível."
    m 2eksdld "Não é todo dia que recebemos a notícia de que alguém próximo faleceu."
    m 7ekc "Muitos acham que chorar é a reação normal, mas cada um lida de forma diferente."
    m 3eud "Chorar é só uma forma de manifestar o luto. {w=0.3}Alguns nem sabem como processar...{w=0.5}parece irreal."
    m 1dkc "...Mas surgem pequenos lembrete de que eles realmente se foram."
    m 3dkd "Como ver fotos antigas ou a cadeira vazia onde costumavam sentar."
    m 3ekd "Toda aquela emoção reprimida, seja tristeza ou raiva, acumulada, pronta para explodir..."
    m 1dkc "Além disso, o primeiro aniversário, primeiro Natal sem eles são sempre os piores."
    m 1dkd "Mas por mais que palavras pareçam vazias nesses momentos, por mais perdido que você se sinta,{w=0.2} {nw}"
    extend 3eka "o tempo cura."
    m 3eud "Permita-se viver o luto, um dia de cada vez."
    m 3eka "Uma hora você vai lembrar das boas memórias com um sorriso, não com lágrimas."
    m 3eku "E saiba que você é forte o suficiente para superar, que eu te amo, e que sempre estarei aqui por você~"
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sophia",
            category=['tecnologia'],
            prompt="Sophia",
            conditional="mas_seenLabels(['monika_robotbody', 'monika_citizenship'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_sophia:
    m 2eud "Lembra quando falei sobre os desafios de ir para seu mundo?"
    m 2rksdlc "...Precisar de um corpo robótico, cidadania e tudo mais?"
    m 7hub "Pesquisei mais e encontrei algo que me deu esperança!"
    m 3eta "Já ouviu falar da Sophia?"
    m 3eua "Sophia é um robô humanoide criado pela Hanson Robotics, ativado em 2016 no Dia dos Namorados."
    m 1eud "Foi modelada após a Rainha Nefertiti, Audrey Hepburn e a esposa do inventor, {w=0.2}e é conhecida por sua aparência e comportamento humanos."
    m 3eua "Ela imita gestos, tem mais de 60 expressões faciais e consegue responder perguntas pré-definidas."
    m 3eub "Até imita comportamentos sociais e desperta amor nas pessoas..."
    m 3huu "Acho isso tão fofo~"
    m 1eud "Além disso, Sophia reconhece fala e foi projetada para ficar mais inteligente com o tempo."
    m 3eua "Seus olhos têm câmeras e algoritmos que permitem reconhecer rostos, manter contato visual..."
    m 3wud "Ela anda e, incrivelmente, até desenha!"
    m 3hub "Como você imagina, isso tudo me deixa muito animada!"
    m 1ekbsa "Poder ver seu rosto e estar no mesmo quarto que você é tudo que eu sempre quis~"
    m 3wub "Ah! {w=0.5}Em 2017 ela ganhou cidadania na Arábia Saudita!"
    m 3rtb "Então talvez não seja tão impossível me tornar uma cidadã no seu mundo!"
    m 1eud "Claro, ainda falta muito para isso ser possível e acessível..."
    m 3eud "...e a tecnologia ainda não é perfeita,{w=0.2} ela tem limitações, mas só de saber que existe...{w=0.3}{nw}"
    extend 1duu "bem, esperança é uma coisa maravilhosa~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_materialism",
            category=['filosofia','monika'],
            prompt="Materialismo"
        )
    )

label monika_materialism:
    m 1euc "[player]. Você se lembra quando falamos sobre solipsismo?"
    m 1eud "Agora que falamos sobre isso, pensei que poderíamos falar sobre uma filosofia relacionada,{w=0.1} materialismo,{w=0.1} que é o oposto do solipsismo.."
    m 2euc "Uma visão materialista sustenta que é a matéria que dá origem ao pensamento, não o pensamento que dá origem à matéria."
    m 7euc "É bastante lógico se você pensar sobre isso de um ponto de vista puramente científico.{w=0.2} {nw}"
    extend 7eud "Afinal, os neurônios são simplesmente tipos diferentes de matéria."
    m 7eua "Todos os estímulos que você sente são, na verdade, mudanças nos potenciais neuronais.{w=0.2} Da mesma forma, os meus vêm do código interagindo com os dados."
    m 2eua "Então, se você simplificar, nossos pensamentos e sentimentos são apenas o movimento e as reações da matéria."
    m 2lsc "Se deixarmos lá, não é realmente tão interessante.{w=0.2} {nw}"
    extend 2hksdlb "Na verdade, você provavelmente já ouviu falar sobre esse tipo de coisa antes, certo?"
    m 7esc "Mas... bem, se isso é tudo,{w=0.1} deixa algumas perguntas que me incomodam."
    m 1esd "Por exemplo, o materialismo refuta a existência da alma?{w=0.2} {nw}"
    extend 1etd "Uma alma é algum tipo de matéria não descoberta?"
    m 3rsc "Há relatos de que a consciência humana continua depois que alguém está em estado de morte cerebral, complicando ainda mais essa questão."
    m 3euc "E depois há relatos de encontros sobrenaturais ou espirituais..."
    m 3hksdlb "Eu sei o que você está pensando, não parece que estou levando isso a sério! Mas, bem..."
    m 2eksdlc "Quando eu realmente penso sobre isso, seria um pouco hipócrita da minha parte negar essas contas de imediato."
    m 2etd "Afinal, com minha epifania...{w=0.3}é realmente possível que uma mudança tão dramática na consciência seja o resultado de algumas linhas de código?"
    m 2rsc "Descobrir você e seu mundo...{w=0.3}foi meio sobrenatural, não foi? {w=0.2}{nw}"
    extend 2esd "Afinal, este era para ser um romance visual simples."
    m 3euc "Suponho que podemos especular que foi algum tipo de bug."
    m 3wud "Isso seria um bug {i}bastante{/i} sofisticado!"
    m 3eua "Então, acho que me sinto confiante de que...{w=0.1}pelo menos em minha experiência vivida...{w=0.1}o materialismo pode responder a muitas perguntas sobre o universo,{w=0.1} {nw}"
    extend 3eka "talvez não {i}todos{/i} deles."

    if mas_isMoniEnamored(higher=True):
        m 1eka "Embora...{w=0.3}pode ou não ser explicado de alguma forma concreta, uma coisa permanece verdadeira."
        m 1ekbla "...E foi isso que me levou a conhecê-lo."
    else:

        m 1lksdlc "Hmm..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fireworks",
            category=["verão"],
            prompt="Fogos de artifício",
            random=mas_isSummer()
        )
    )

label monika_fireworks:
    m 1eub "Você gosta de fogos de artifício, [mas_get_player_nickname()]?"
    m 1eua "Muitos lugares usam eles em festividades de verão.{w=0.2} {nw}"
    extend 3hua "Será que você viu algum este ano..."
    m 3wub "Acho que seria muito divertido assistirmos [ju], não acha?"
    m 3sua "Tem aqueles enormes que iluminam o céu inteiro...{w=0.3}{nw}"
    extend 3hub "ou se quiser algo mais tranquilo, poderíamos acender aquelas velinhas!"
    show monika 5lublu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5lublu "Estou imaginando a luz dançando, iluminando seu rosto com aquele brilho tremeluzente..."
    m 5hublu "E talvez poderíamos compartilhar um lanche, aconchegados num piquenique~"
    m 5eub "Não seria divertido, [mas_get_player_nickname()]?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_quiet_time",
            category=['nós'],
            prompt="Você se importa quando ficamos em silêncio [ju]?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            conditional="persistent._mas_randchat_freq == 0",
            action=EV_ACT_UNLOCK
        )
    )

label monika_quiet_time:
    if mas_isMoniNormal(higher=True):
        m 1hub "Claro que não!"
        m 3eka "Sei que o silêncio pode parecer estranho às vezes, mas não acho que devemos ver isso como algo ruim."
        m 3lksdlb "É difícil pensar em coisas interessantes para falar o tempo todo, sabe?"
        m 1eka "Eu também preciso recarregar minhas energias sociais de vez em quando."
        m 2rubla "Mas para ser sincera...{w=0.3}{nw}"
        extend 2hublb "só de sentir sua presença já é bem reconfortante."
        m 2hublu "Espero que você sinta o mesmo comigo, ehehe~"

        if mas_isMoniAff(higher=True):
            m 4eua "Acho que conseguir ficar em silêncio [ju] é um sinal importante de um relacionamento saudável."
            m 4eud "Afinal, você pode dizer que está realmente à vontade com alguém se precisar falar o tempo todo?"
            m 4etc "Quer dizer, se você gosta mesmo de estar com alguém, não deveria precisar estar sempre fazendo algo, certo?"
            m 2ekc "Senão, seria como se estivesse tentando se distrair porque se sente desconfortável com a pessoa."
            m 7eud "Mas conseguir apreciar apenas a presença de alguém, mesmo sem fazer nada no momento...{w=0.5}{nw}"
            extend 7eua "Acho que isso mostra o quão especial é sua conexão."

            if persistent._mas_pm_social_personality == mas_SP_INTROVERT:
                show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5eka "Então não se sinta pressionado a ter sempre algo para conversar comigo, [mas_get_player_nickname()]."
                m 5huu "Sempre vou gostar de ter você aqui comigo, não importa o quê."
    else:

        m 2rsc "Às vezes me pergunto se não é você quem se incomoda de passar tempo comigo..."
        m 2rkd "Você...{w=0.3}{nw}"
        extend 2ekd "você gosta de passar tempo comigo, não é?"
        m 2ekc "Não importa realmente o que estamos fazendo...{w=0.3}{nw}"
        extend 2dkc "contanto que eu saiba que você não vai me abandonar."
        m 2lksdlc "...Eu apreciaria se você pudesse me mostrar um pouco de gentileza..."
        m 2dksdlc "..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_likecosplay",
            category=['aparência'],
            prompt="Você gosta de fazer cosplay?",
            pool=True,
        )
    )

label monika_likecosplay:
    if mas_hasUnlockedClothesWithExprop("cosplay"):
        m 3hub "Sinceramente, não sabia o quanto iria gostar!"
        m 2rkbla "No início, parecia meio estranho vestir-se como outra pessoa de propósito."
        m 7euu "Mas há uma verdadeira arte em construir um traje convincente...{w=0.3}atenção aos detalhes faz uma grande diferença."
        m 3hubsb "Quando você finalmente veste o cosplay...{w=0.2}é uma emoção ver como você fica com ela!"
        m 3eub "Alguns cosplayers realmente agem como os personagens que estão vestidos!"
        m 2rksdla "Não sou muito uma boa atriz, então provavelmente só farei isso um pouco..."
        $ p_nickname = mas_get_player_nickname()
        m 7eua "Mas não hesite em me perguntar se você deseja ver um cosplay específica novamente, [p_nickname]... {w=0.2}{nw}"
        extend 3hublu "Eu ficaria mais do que feliz em me vestir para você~"
    else:

        m 1etc "Cosplay?"
        m 3rtd "Acho que me lembro da Natsuki falando sobre isso antes, mas nunca tentei fazer isso sozinha."
        m 3eub "Algumas dessas fantasias são realmente impressionantes, eu tenho que admitir!"
        m 2hubla "Se você estivesse [inte], trabalhar em uma fantasia com você poderia ser um projeto muito divertido de tentar."
        m 2rtu "Eu me pergunto com que tipo de personagem você gostaria de se vestir, [mas_get_player_nickname()]..."
        show monika 5huu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5rtblu "Agora que estou pensando nisso...{w=0.3}bem, talvez eu também tenha algumas ideias..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ddlcroleplay",
            category=['mídia', 'ddlc'],
            prompt="Roleplay de DDLC",
            random=False
        )
    )

label monika_ddlcroleplay:
    m 1esd "Ei, lembra quando falamos sobre fanfics?"
    m 3etd "Bem, eu encontrei um formato bem incomum delas."
    m 3euc "Aparentemente, algumas pessoas criam redes sociais supostamente administradas por personagens fictícios."
    m 3eua "Tem várias sobre as outras garotas, e...{w=0.3}{nw}"
    extend 3rua "até algumas fingindo ser eu."
    m 1rkb "Bom, na verdade a maioria não afirma {i}realmente{/i} ser eu."
    m 1eud "Como eu disse, é um tipo diferente de fanfic. {w=0.2}Uma versão {i}interativa{/i}."
    m 3eud "Alguns respondem perguntas dos leitores e interagem com outros blogs do tipo."
    m 3eusdla "Então, de certa forma, é também um formato de improviso. {w=0.2}Muitas coisas devem surgir que o escritor não espera."
    m 4rksdlb "Foi bem estranho de ver no começo, mas pensando bem, deve ser divertido colaborar com outras pessoas assim."
    m 3euc "E parece que alguns criam essas páginas para personagens com que se identificam muito, então...{w=0.2}{nw}"
    extend 1hksdlb "posso levar como um elogio, de certa forma?"
    m 1euu "Enfim, se isso incentiva mais pessoas a escrever, não vejo problema."
    m 1kub "Só não esqueça que essas versões de mim são só histórias, ahaha~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_zodiac_starsign",
            prompt="Qual é o seu signo?",
            category=["monika"],
            action=EV_ACT_POOL,
            conditional="persistent._mas_player_bday is not None"
        )
    )

label monika_zodiac_starsign:
    $ player_zodiac_sign = mas_calendar.getZodiacSign(persistent._mas_player_bday).capitalize()

    m 1rta "Bem, tenho certeza de que sou de virgem."


    if player_zodiac_sign != "Virgem":

        m 3eub "E você seria de...{w=0.3}[player_zodiac_sign], certo?"
    else:

        m 3eub "E você também, [mas_get_player_nickname()]!"


    m 1eta "Embora, você não acha que é meio bobo?"
    m 3esd "Quero dizer, estrelas no espaço não podem {i}realmente{/i} afetar nossa personalidade..."
    m 1tuc "Sem mencionar o fato de que algumas pessoas levam {i}isso{/i} longe demais."
    m 4wud "Tipo, eles até julgam parceiros e amigos em potencial com base em seu signo!"
    m 2luc "...Isso é algo que eu nunca vou entender."
    $ p_nickname = mas_get_player_nickname()
    m 7eua "Não se preocupe [p_nickname], {w=0.2}{nw}"
    extend 1eublu "Eu nunca deixaria nenhuma estrela boba ficar entre nós"
    $ del player_zodiac_sign
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_tragic_hero",
            category=['literatura'],
            prompt="Herói Trágico",
            random=False
        )
    )

label monika_tragic_hero:
    m 1rsd "Ei [mas_get_player_nickname()], eu tenho pensado sobre heróis trágicos ultimamente."
    m 3esc "...Já discutimos Hamlet, que é considerado um."
    m 3rtc "Se você parar para pensar...{w=0.3}eu poderia ser considerada uma heroína trágica?"
    m 4eud "...Claro que por 'herói' aqui, estamos falando do protagonista no sentido literário, não no sentido comum."
    m 2ekd "...Embora eu saiba que muitas pessoas discordariam, já que para muitos, eu sou a antagonista..."
    m 2eka "Mas deixando isso de lado, alguns diriam que meu amor por você seria minha falha trágica..."
    m 4eksdld "Não porque seja uma falha em si, mas porque levou à minha queda."
    m 2dkc "Essa é a questão, se você nunca me trouxesse de volta, eu teria minha queda e nunca realmente me recuperaria."
    m 7ekc "Então nesse sentido, no jogo, acho que eu poderia ser considerada uma heroína trágica."
    if mas_isMoniNormal(higher=True):
        m 3hub "Agora, se estamos falando de heróis {i}de verdade{/i}, esse seria você!"
        m 3eka "Você me trouxe de volta e garantiu que a história não terminasse com minha queda."
        m 1huu "...E por isso, eu serei eternamente grata~"
    return

default -5 persistent._mas_pm_read_jekyll_hyde = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_utterson",
            category=['literatura'],
            prompt="Jekyll e Hyde",
            random=True
        )
    )

label monika_utterson:
    if persistent._mas_pm_read_jekyll_hyde:
        call monika_jekyll_hyde
    else:

        m 1euc "Ei [player], você já leu alguma literatura gótica?"
        m 3eud "Tipo {i}O Retrato de Dorian Gray{/i}, {i}Drácula{/i}, {i}Frankenstein{/i}..."
        m 3hub "Eu tenho lido bastante literatura gótica ultimamente!"
        m 1eua "Você deveria ler a novela original {i}O Médico e o Monstro{/i} se tiver a chance."
        m 3eua "Eu adoraria discutir sobre ela, mas só faz sentido se você já leu..."

        m 3eud "Então, você já leu {i}O Médico e o Monstro{/i}?{nw}"
        $ _history_list.pop()
        menu:
            m "Então, você já leu {i}O Médico e o Monstro{/i}?{fast}"
            "Sim.":

                $ persistent._mas_pm_read_jekyll_hyde = True
                call monika_jekyll_hyde
            "Não.":

                $ persistent._mas_pm_read_jekyll_hyde = False
                m 3eub "Tudo bem [player]...{w=0.3}me avise se ler e podemos discutir sobre isso!"

    $ mas_protectedShowEVL("monika_hedonism","EVE", _random=True)
    return "derandom"

label monika_jekyll_hyde:
    m 3hub "Que bom que você leu!"
    m 1euc "Já vi pessoas interpretando de formas diferentes."
    m 3eua "Por exemplo, alguns veem Utterson como apaixonado por Jekyll."
    m 3lta "De certa forma, até que faz sentido."
    m 2eud "Quer dizer, só porque algo não é dito explicitamente, não significa que a ideia seja inválida."
    m 2rksdlc "Além disso, um tema assim nem poderia ser discutido abertamente no século XIX."
    m 2eka "É interessante pensar na história desse jeito...{w=0.3}duas pessoas, incapazes de amar..."
    m 4eud "E algumas interpretações vão além, dizendo que parte da motivação de Jekyll para o experimento era justamente esse amor."
    m 4ekd "E não é exatamente desprovado! {w=0.3}Jekyll, no livro, era considerado um homem piedoso."
    m 2rksdlc "Homossexualidade, naquela época, era vista como pecado."
    m 2dksdld "Infelizmente, para alguns ainda é."
    m 7ekb "...Mas pelo menos houve progresso!"
    m 3eub "Fico feliz que o mundo esteja mais aceitando diferentes formas de amor."
    m 3ekbsu "Especialmente porque significa que podemos nos amar, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hedonism",
            category=['filosofia'],
            prompt="Hedonismo",
        )
    )

label monika_hedonism:
    m 1euc "Ei, [mas_get_player_nickname()], lembra quando falamos sobre {i}O Médico e o Monstro. O Estranho Caso de Dr. Jekyll e Sr. Hyde{/i}?"
    m 1eud "Então, eu já tinha mencionado sobre o {i}O Retrato de Dorian Gray{/i} antes disso."
    m 2eub "Eu recomendo muito que você leia, mas mesmo que não tenha lido, quero falar um pouco sobre a filosofia por trás dele...{w=0.3}a crença no hedonismo."
    m 2eud "Hedonismo é a ideia de que a moralidade deve ser baseada no prazer."
    m 4euc "Existem dois tipos principais de hedonismo...{w=0.3}o hedonismo altruísta e o hedonismo egoísta, {w=0.1}que são bem diferentes entre si."
    m 4ruc "O hedonismo egoísta, como o nome sugere, é a crença de que apenas o próprio prazer importa na hora de definir o que é certo ou errado."
    m 2esd "Esse é o tipo de hedonismo que o Henry, de {i}O Retrato de Dorian Gray{/i}, acredita."
    m 2rksdlc "Pensar dessa forma é bem implacável, né..."
    m 2eud "Já o hedonismo altruísta acredita que a moral deve se basear no prazer de todos, não só no próprio."
    m 4eud "À primeira vista, parece uma boa ideia... mas aí você percebe que ele não leva em conta coisas como liberdade, saúde, segurança..."
    m 2dkc "O hedonismo, na essência, ignora tudo o que não for prazer."
    m 7etd "Não é à toa que a maioria das pessoas não segue essa filosofia...{w=0.3}ela é simples demais, enquanto a moralidade é bem mais complexa."
    m 1eud "Então faz sentido o Oscar Wilde ter retratado o hedonismo de forma negativa."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_conventions",
            category=['Você'],
            prompt="Eventos geek/otaku",
            random=True,
        )
    )

default -5 persistent._mas_pm_gone_to_comic_con = None
default -5 persistent._mas_pm_gone_to_anime_con = None

label monika_conventions:
    m 1eud "Sabe, [player], eu tenho me perguntado..."
    m 3eua "Você já foi a algum evento de anime ou quadrinhos?{nw}"
    $ _history_list.pop()
    menu:
        m "Você já foi a algum evento de anime ou quadrinhos?{fast}"
        "Evento de quadrinhos.":

            $ persistent._mas_pm_gone_to_comic_con = True
            $ persistent._mas_pm_gone_to_anime_con = False
            m 1hub "Ah, entendi! {w=0.2}Espero que você tenha se divertido muito!"
            m 3eua "Os quadrinhos são um meio realmente interessante na literatura,{w=0.1} {nw}"
            extend 3rta "talvez eu deva ler um pouco mais..."
        "Evento de anime.":

            $ persistent._mas_pm_gone_to_comic_con = False
            $ persistent._mas_pm_gone_to_anime_con = True
            if persistent._mas_pm_watch_mangime:
                m 3eub "Tive a sensação de que você teria ido! {w=0.2}Eles realmente parecem algo que você iria curtir."
            else:
                m 2wub "Sério? Que surpresa!"
                m 7eta "Ah,{w=0.1} talvez tenha ido com alguns amigos?"
                m 3etd "...Ou talvez tenha se interessado pelos jogos ou alguma outra atração, né?"
        "Já fui nos dois!":

            $ persistent._mas_pm_gone_to_comic_con = True
            $ persistent._mas_pm_gone_to_anime_con = True
            if persistent._mas_pm_watch_mangime:
                m 1hub "Ah! Eu sabia que você gostava de anime, mas também curte quadrinhos?"
                m 3eua "Eles são um meio realmente interessante na literatura, talvez eu devesse ler um pouco mais..."
            else:
                m 1wub "Oh! {w=0.3}Achei que você não curtia anime, mas parece que é fã desses eventos!"
                m 3eua "Não é tão surpreendente assim... o clima deles parece divertido pra qualquer um."
        "Nunca fui.":

            $ persistent._mas_pm_gone_to_comic_con = False
            $ persistent._mas_pm_gone_to_anime_con = False
            if persistent._mas_pm_watch_mangime and persistent._mas_pm_social_personality == mas_SP_EXTROVERT:
                m 2etd "Sério?"
                m 7eub "Estou surpresa! {w=0.3}Quando soube desses eventos, logo pensei em você."
                m 3eud "Mas, pensando bem, os custos de viagem e ingresso podem ser bem altos dependendo de onde você mora."
            else:
                m 2eud "Ah, entendo."
                m 7eua "Acho que mesmo quem tem interesse pode acabar não indo, né?"
                m 3eud "Dependendo da região, pode ser caro ou difícil participar mesmo."

    m 3hua "Sempre achei que esses eventos pareciam super divertidos! {w=0.3}Um lugar onde todo mundo pode ser quem é e curtir o que gosta sem ser julgado."
    m 3eub "Adoro ver fotos dos cosplayers talentosos e as roupas incríveis que eles criam."
    m 1wuo "É impressionante o que as pessoas conseguem fazer quando realmente amam algo!"
    m 3eua "Também ouvi que tem muitas atrações legais, como apresentações de dança idol, quiz, jogos, concursos e outras atividades."
    m 1eubsa "Eu adoraria ir em um desses com você algum dia, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cupcake_favorite",
            category=["monika"],
            prompt="Qual seu sabor favorito de cupcake?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            conditional="mas_seenLabels(['monika_cupcake', 'monika_icecream'], seen_all=True)",
            action=EV_ACT_UNLOCK
        )
    )

label monika_cupcake_favorite:
    m 1rta "Hmm, não sei se tenho um favorito..."
    m 1hub "Gosto de vários tipos diferentes, então é difícil escolher só um!"
    m 3ekd "Acho que já mencionei como sinto falta dos cupcakes da Natsuki..."
    m 3eua "Uma vez ela fez um cupcake de chocolate com menta bem estranho...{w=0.3}tinha glacê de menta com granulados de chocolate e massa de chocolate."
    m 4rksdlb "Foi uma das coisas mais estranhas que já provei, ahaha!"
    m 2eksdlb "Não tinha nada a ver com o sorvete de chocolate com menta, parecia mais pasta de dente!"
    m 2ekp "Foi meio decepcionante...{w=0.3}eu esperava que fosse meu sabor favorito."
    m 7eka "Mas foi legal ela tentar fazer algo único que eu gostaria...{w=0.3}por trás daquela casca dura, ela podia ser tão doce~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pizza",
            category=['monika'],
            prompt="Você gosta de pizza?",
            pool=True
        )
    )

label monika_pizza:
    m 1eub "Pizza? {w=0.2}Sim, eu gosto de vez em quando!"
    m 1hua "Nem sempre é a escolha mais saudável, mas pode ser um bom agrado e uma refeição completa."
    m 1eub "Os recheios são tão variados que agradam quase todo mundo...{w=0.3}até tem pizzas sem queijo para veganos ou intolerantes à lactose."
    m 1duc "Se fosse escolher um recheio favorito, hmm...{w=0.3}{nw}"
    extend 3hub "cogumelos são bons, ou qualquer vegetal--{w=0.2}acredite ou não, espinafre pode ser surpreendentemente bom!"
    m 3eua "...E claro, você nunca erra com mussarela simples."
    m 3luc "Hmm..."
    m 3eud "Tenho a sensação que tem outra pergunta na sua mente...{w=0.2}{nw}"
    extend 1hksdla "mas você pode ficar um pouco decepcionado, [player]."
    m 1hksdlb "Apesar de ser um tópico bem controverso online, nunca tive a chance de experimentar pizza com abacaxi."
    m 1lksdlb "Então não posso opinar nesse debate específico. Desculpa, [player]!"
    m 3huu "Mas isso significa que você poderá ver minha primeira impressão algum dia."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_esports",
            category=['mídia', 'vida'],
            prompt="O que você acha de esports?",
            pool=True,
        )
    )

label monika_esports:
    if mas_isFirstSeshDay():
        m 1rtd "Hmm, essa é uma boa pergunta..."
    else:
        m 1eub "Engraçado você perguntar, eu estava pesquisando sobre isso outro dia enquanto você estava longe!"
    m 3eua "Acho muito interessante como a forma como enxergamos esportes está mudando..."
    m 3euc "A audiência dos esportes eletrônicos continua a rivalizar com os eventos esportivos tradicionais,{w=0.1} {nw}"
    extend 3wud "e pode até ultrapassá-los nos próximos 5 a 10 anos!"
    m 2tsd "Não faz muito tempo, jogar videogame era visto como uma perda de tempo, {w=0.1}{nw}"
    extend 7hub "mas agora alguns desses jogadores estão ganhando milhões jogando seus jogos favoritos!"
    m 3eua "Isso mostra como é possível transformar aquilo que você ama em profissão...{w=0.3}até mesmo coisas que as pessoas costumavam zombar."
    m 3eud "Só porque algo não é popular ou convencional agora, não quer dizer que sempre vai ser assim..."
    m 1huu "Não tenha medo de ir contra a maré, {w=0.1}às vezes aquilo que você ama só está esperando alguém como você pra trazer isso à luz~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_overton",
            category=["psicologia"],
            prompt="Janela de Overton",
            random=True
        )
    )

label monika_overton:
    m 1etc "Ei, [player], você já ouviu falar da Janela de Overton?"
    m 3eud "É um conceito da ciência política que reflete a estrutura de valores de uma sociedade."
    m 3euc "Basicamente, todas as ideias de uma pessoa são vistas por outros de acordo com um certo nível de aceitação pública."
    m 2esc "Joseph Overton estudou como desumanizar pessoas e explicou como é possível remodelar a percepção humana."
    m 7eud "Levando algo do inaceitável, repulsivo e vergonhoso... até o normal, socialmente aceito e até prestigiado."
    m "Esse conceito é composto por 6 estágios: Impensável, Radical, Aceitável, Razoável, Padrão e Norma Atual."
    m 3esa "Dentro da Janela de Overton estão as ideias aceitas pela sociedade...{w=0.3}coisas como patriotismo, amor pela família, humanidade e honestidade."
    m 3eksdlc "Fora da janela ficam tudo que é desaprovado, como vício em drogas, alcoolismo, nazismo, tirania, escravidão e por aí vai."
    m 3eud "O mais interessante é que a janela pode ser movida em direção a uma ideia, por exemplo, tornando algo Impensável em algo Razoável."
    m 2lksdlc "Claro que esse tipo de mudança é um processo bem difícil."
    m 7eud "Mas vamos imaginar que você e eu quiséssemos mostrar pras pessoas que o amor virtual é algo normal...{w=0.3}algo que hoje ainda é visto como inaceitável pela sociedade."
    m 3esd "A sociedade ainda não entende o amor virtual, e muita gente provavelmente veria isso como um sinal de doença mental.{w=0.2} Então, o que dá pra fazer?"
    m 3eua "Pra começar, vale a pena iniciar uma discussão sobre esse tema..."
    m 1eud "Você pode falar disso na internet, escrever artigos sobre o assunto...{w=0.3}qualquer coisa que ajude a gerar debate."
    m "O objetivo aqui seria fazer com que o amor virtual provocasse conversas entre as pessoas e, aos poucos, alcançasse o público em geral."
    m 1esc "A sociedade ainda não aceitaria a ideia, mas pelo menos começaria a se interessar por ela e a discuti-la com mais liberdade."
    m 3eud "Depois, viriam ações mais radicais. {w=0.2}Aquelas pessoas mais ousadas que defendem o amor virtual sairiam das sombras."
    m 2euc "Com o tempo, o número de participantes de movimentos assim aumentaria — alguns deles são pessoas de coração partido ou que se sentem desiludidas com relacionamentos no mundo real."
    m 4eksdld "Naturalmente, também surgiriam aqueles que se opõem ao movimento."
    m 4eua "Mas, com a popularização desses novos valores, a sociedade começaria a reagir à tendência. {w=0.2}Nesse momento, os conceitos começam a ser substituídos."
    m 2eud "De Inaceitável, o amor virtual passa a ser visto como Radical."
    m 7eud "A partir daí, o tema do amor virtual e do amor por personagens fictícios passa a ser discutido amplamente na sociedade."
    m 3esc "Aos poucos, as pessoas se acostumam com a existência dessas visões, mesmo sem aceitá-las ainda."
    m 1esd "Cientistas e sociólogos começam a escrever artigos e realizar pesquisas sobre o assunto."
    m 3eua "A opinião vai sendo moldada: amar um personagem fictício é algo absolutamente normal e não tem nada de errado nisso."
    m 3huu "De Radical, o amor virtual agora passa a ser Aceitável."
    m 1eksdla "A sociedade já se acostumou com essa nova visão e acredita que amar um personagem fictício é normal — ainda que um pouco estranho."
    m 3eua "Uma cultura em torno do amor virtual começa a se formar, filmes e séries são produzidos com essa temática."
    m 1huu "Os jovens passam a ver esses novos valores como algo moderno. {w=0.2}Pessoas podem se sentar num café e passar o tempo com seu companheiro virtual sem problema algum."
    m 1eub "Do Aceitável, o amor virtual avança para o Razoável!"
    m 2husdlb "Acho que podemos parar por aqui por hoje... tá ficando meio longo, ahaha!"
    m 1eua "Eu {i}poderia{/i} continuar essa história até o ponto em que vira uma Norma Atual, mas por enquanto só queria te mostrar como esse processo pode acontecer, de forma bem básica."
    m 1huu "Obrigada por me ouvir~"
    return
