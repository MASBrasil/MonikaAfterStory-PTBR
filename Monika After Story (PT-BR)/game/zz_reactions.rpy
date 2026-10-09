init offset = 5


default -5 persistent._mas_filereacts_failed_map = dict()


default -5 persistent._mas_filereacts_just_reacted = False


default -5 persistent._mas_filereacts_reacted_map = dict()


default -5 persistent._mas_filereacts_stop_map = dict()


default -5 persistent._mas_filereacts_historic = dict()


default -5 persistent._mas_filereacts_last_reacted_date = None


default -5 persistent._mas_filereacts_sprite_gifts = {}











default -5 persistent._mas_filereacts_sprite_reacted = {}









default -5 persistent._mas_filereacts_gift_aff_gained = 0



default -5 persistent._mas_filereacts_last_aff_gained_reset_date = datetime.date.today()


init 795 python:
    if len(persistent._mas_filereacts_failed_map) > 0:
        store.mas_filereacts.delete_all(persistent._mas_filereacts_failed_map)

init -16 python in mas_filereacts:
    import store
    import store.mas_utils as mas_utils
    import datetime
    import random

    from collections import namedtuple

    GiftReactDetails = namedtuple(
        "GiftReactDetails",
        [
            
            "label",

            
            "c_gift_name",

            
            
            
            "sp_data",
        ]
    )


    filereact_db = dict()




    filereact_map = dict()





    foundreact_map = dict()



    th_foundreact_map = dict()


    good_gifts = [
        
        "mas_reaction_gift_generic_sprite_json"
    ]


    bad_gifts = list()


    connectors = None
    gift_connectors = None


    starters = None
    gift_starters = None

    GIFT_EXT = ".gift"


    def addReaction(ev_label, fname, _action=store.EV_ACT_QUEUE, is_good=None, exclude_on=[]):
        """
        Adds a reaction to the file reactions database.

        IN:
            ev_label - label of this event
            fname - filename to react to
            _action - the EV_ACT to do
                (Default: EV_ACT_QUEUE)
            is_good - if the gift is good(True), neutral(None) or bad(False)
                (Default: None)
            exclude_on - keys marking times to exclude this gift
            (Need to check ev.rules in a respective react_to_gifts to exclude with)
                (Default: [])
        """
        
        if fname is not None:
            fname = fname.lower()
        
        exclude_keys = {}
        if exclude_on:
            for _key in exclude_on:
                exclude_keys[_key] = None
        
        
        ev = store.Event(
            store.persistent.event_database,
            ev_label,
            category=fname,
            action=_action,
            rules=exclude_keys
        )
        
        
        
        
        filereact_db[ev_label] = ev
        filereact_map[fname] = ev
        
        if is_good is not None:
            if is_good:
                good_gifts.append(ev_label)
            else:
                bad_gifts.append(ev_label)


    def _initConnectorQuips():
        """
        Initializes the connector quips
        """
        global connectors, gift_connectors
        
        
        connectors = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_connectors = store.MASQuipList(allow_glitch=False, allow_line=False)


    def _initStarterQuips():
        """
        Initializes the starter quips
        """
        global starters, gift_starters
        
        
        starters = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_starters = store.MASQuipList(allow_glitch=False, allow_line=False)


    def build_gift_react_labels(
            evb_details=[],
            gsp_details=[],
            gen_details=[],
            gift_cntrs=None,
            ending_label=None,
            starting_label=None,
            prepare_data=True
    ):
        """
        Processes gift details into a list of labels to show
        labels to queue/push whatever.

        IN:
            evb_details - list of GiftReactDetails objects of event-based
                reactions. If empty list, then we don't build event-based
                reaction labels.
                (Default: [])
            gsp_details - list of GiftReactDetails objects of generic sprite
                object reactions. If empty list, then we don't build generic
                sprite object reaction labels.
                (Default: [])
            gen_details - list of GiftReactDetails objects of generic gift
                reactions. If empty list, then we don't build generic gift
                reaction labels.
                (Default: [])
            gift_cntrs - MASQuipList of gift connectors to use. If None,
                then we don't add any connectors.
                (Default: [])
            ending_label - label to use when finished reacting.
                (Default: None)
            starting_label - label to use when starting reacting
                (Default: None)
            prepare_data - True will also setup the appropriate data
                elements for when dialogue is shown. False will not.
                (Default: True)

        RETURNS: list of labels. Evb reactions are first, followed by
            gsp reactions, then gen reactions
        """
        labels = []
        
        
        if len(evb_details) > 0:
            evb_labels = []
            for evb_detail in evb_details:
                evb_labels.append(evb_detail.label)
                
                if gift_cntrs is not None:
                    evb_labels.append(gift_cntrs.quip()[1])
                
                if prepare_data and evb_detail.sp_data is not None:
                    
                    
                    store.persistent._mas_filereacts_sprite_reacted[evb_detail.sp_data] = (
                        evb_detail.c_gift_name
                    )
            
            labels.extend(evb_labels)
        
        
        if len(gsp_details) > 0:
            gsp_labels = []
            for gsp_detail in gsp_details:
                if gsp_detail.sp_data is not None:
                    gsp_labels.append("mas_reaction_gift_generic_sprite_json")
                    
                    if gift_cntrs is not None:
                        gsp_labels.append(gift_cntrs.quip()[1])
                    
                    if prepare_data:
                        store.persistent._mas_filereacts_sprite_reacted[gsp_detail.sp_data] = (
                            gsp_detail.c_gift_name
                        )
            
            labels.extend(gsp_labels)
        
        
        num_gen_gifts = len(gen_details)
        if num_gen_gifts > 0:
            gen_labels = []
            
            if num_gen_gifts == 1:
                gen_labels.append("mas_reaction_gift_generic")
            else:
                gen_labels.append("mas_reaction_gifts_generic")
            
            if gift_cntrs is not None:
                gen_labels.append(gift_cntrs.quip()[1])
            
            for gen_detail in gen_details:
                if prepare_data:
                    store.persistent._mas_filereacts_reacted_map.pop(
                        gen_detail.c_gift_name,
                        None
                    )
                    
                    store.mas_filereacts.delete_file(gen_detail.c_gift_name)
            
            labels.extend(gen_labels)
        
        
        if len(labels) > 0:
            
            
            if gift_cntrs is not None:
                labels.pop()
            
            
            if ending_label is not None:
                labels.append(ending_label)
            
            
            if starting_label is not None:
                labels.insert(0, starting_label)
        
        
        return labels

    def build_exclusion_list(_key):
        """
        Builds a list of excluded gifts based on the key provided

        IN:
            _key - key to build an exclusion list for

        OUT:
            list of giftnames which are excluded by the key
        """
        return [
            giftname
            for giftname, react_ev in filereact_map.iteritems()
            if _key in react_ev.rules
        ]

    def check_for_gifts(
            found_map={},
            exclusion_list=[],
            exclusion_found_map={},
            override_react_map=False,
    ):
        """
        Finds gifts.

        IN:
            exclusion_list - list of giftnames to exclude from the search
            override_react_map - True will skip the last reacted date check,
                False will not
                (Default: False)

        OUT:
            found_map - contains all gifts that were found:
                key: lowercase giftname, no extension
                val: full giftname wtih extension
            exclusion_found_map - contains all gifts that were found but
                are excluded.
                key: lowercase giftname, no extension
                val: full giftname with extension

        RETURNS: list of found giftnames
        """
        raw_gifts = store.mas_docking_station.getPackageList(GIFT_EXT)
        
        if len(raw_gifts) == 0:
            return []
        
        
        if store.mas_pastOneDay(store.persistent._mas_filereacts_last_reacted_date):
            store.persistent._mas_filereacts_last_reacted_date = datetime.date.today()
            store.persistent._mas_filereacts_reacted_map = dict()
        
        
        gifts_found = []
        has_exclusions = len(exclusion_list) > 0
        
        for mas_gift in raw_gifts:
            gift_name, ext, garbage = mas_gift.partition(GIFT_EXT)
            c_gift_name = gift_name.lower()
            if (
                c_gift_name not in store.persistent._mas_filereacts_failed_map
                and c_gift_name not in store.persistent._mas_filereacts_stop_map
                and (
                    override_react_map
                    or c_gift_name not
                        in store.persistent._mas_filereacts_reacted_map
                )
            ):
                
                
                
                if has_exclusions and c_gift_name in exclusion_list:
                    exclusion_found_map[c_gift_name] = mas_gift
                
                else:
                    gifts_found.append(c_gift_name)
                    found_map[c_gift_name] = mas_gift
        
        return gifts_found


    def process_gifts(gifts, evb_details=[], gsp_details=[], gen_details=[]):
        """
        Processes list of giftnames into types of gift

        IN:
            gifts - list of giftnames to process. This is copied so it wont
                be modified.

        OUT:
            evb_details - list of GiftReactDetails objects regarding
                event-based reactions
            spo_details - list of GiftReactDetails objects regarding
                generic sprite object reactions
            gen_details - list of GiftReactDetails objects regarding
                generic gift reactions
        """
        if len(gifts) == 0:
            return
        
        
        gifts = list(gifts)
        
        
        for index in range(len(gifts)-1, -1, -1):
            
            
            mas_gift = gifts[index]
            reaction = filereact_map.get(mas_gift, None)
            
            if mas_gift is not None and reaction is not None:
                
                
                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
                    mas_gift,
                    None
                )
                
                
                gifts.pop(index)
                evb_details.append(GiftReactDetails(
                    reaction.eventlabel,
                    mas_gift,
                    sp_data
                ))
        
        
        if len(gifts) > 0:
            for index in range(len(gifts)-1, -1, -1):
                mas_gift = gifts[index]
                
                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
                    mas_gift,
                    None
                )
                
                if mas_gift is not None and sp_data is not None:
                    gifts.pop(index)
                    
                    
                    gsp_details.append(GiftReactDetails(
                        "mas_reaction_gift_generic_sprite_json",
                        mas_gift,
                        sp_data
                    ))
        
        
        if len(gifts) > 0:
            for mas_gift in gifts:
                if mas_gift is not None:
                    
                    gen_details.append(GiftReactDetails(
                        "mas_reaction_gift_generic",
                        mas_gift,
                        None
                    ))


    def react_to_gifts(found_map, connect=True):
        """
        Reacts to gifts using the standard protocol (no exclusions)

        IN:
            connect - true will apply connectors, FAlse will not

        OUT:
            found_map - map of found reactions
                key: lowercaes giftname, no extension
                val: giftname with extension

        RETURNS:
            list of labels to be queued/pushed
        """
        
        found_gifts = check_for_gifts(found_map)
        
        if len(found_gifts) == 0:
            return []
        
        
        for c_gift_name, mas_gift in found_map.iteritems():
            store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift
        
        found_gifts.sort()
        
        
        evb_details = []
        gsp_details = []
        gen_details = []
        process_gifts(found_gifts, evb_details, gsp_details, gen_details)
        
        
        register_sp_grds(evb_details)
        register_sp_grds(gsp_details)
        register_gen_grds(gen_details)
        
        
        
        if connect:
            gift_cntrs = gift_connectors
        else:
            gift_cntrs = None
        
        
        return build_gift_react_labels(
            evb_details,
            gsp_details,
            gen_details,
            gift_cntrs,
            "mas_reaction_end",
            _pick_starter_label()
        )

    def register_gen_grds(details):
        """
        registers gifts given a generic GiftReactDetails list

        IN:
            details - list of GiftReactDetails objects to register
        """
        for grd in details:
            if grd.label is not None:
                _register_received_gift(grd.label)


    def register_sp_grds(details):
        """
        registers gifts given sprite-based GiftReactDetails list

        IN:
            details - list of GiftReactDetails objcts to register
        """
        for grd in details:
            if grd.label is not None and grd.sp_data is not None:
                _register_received_gift(grd.label)


    def _pick_starter_label():
        """
        Internal function that returns the appropriate starter label for reactions

        RETURNS:
            - The label as a string, that should be used today.
        """
        if store.mas_isMonikaBirthday():
            return "mas_reaction_gift_starter_bday"
        elif store.mas_isD25() or store.mas_isD25Pre():
            return "mas_reaction_gift_starter_d25"
        elif store.mas_isF14():
            return "mas_reaction_gift_starter_f14"
        
        return "mas_reaction_gift_starter_neutral"

    def _core_delete(_filename, _map):
        """
        Core deletion file function.

        IN:
            _filename - name of file to delete, if None, we delete one randomly
            _map - the map to use when deleting file.
        """
        if len(_map) == 0:
            return
        
        
        if _filename is None:
            _filename = random.choice(_map.keys())
        
        file_to_delete = _map.get(_filename, None)
        if file_to_delete is None:
            return
        
        if store.mas_docking_station.destroyPackage(file_to_delete):
            
            _map.pop(_filename)
            return
        
        
        store.persistent._mas_filereacts_failed_map[_filename] = file_to_delete


    def _core_delete_list(_filename_list, _map):
        """
        Core deletion filename list function

        IN:
            _filename - list of filenames to delete.
            _map - the map to use when deleting files
        """
        for _fn in _filename_list:
            _core_delete(_fn, _map)


    def _register_received_gift(eventlabel):
        """
        Registers when player gave a gift successfully
        IN:
            eventlabel - the event label for the gift reaction

        """
        
        today = datetime.date.today()
        if not today in store.persistent._mas_filereacts_historic:
            store.persistent._mas_filereacts_historic[today] = dict()
        
        
        store.persistent._mas_filereacts_historic[today][eventlabel] = store.persistent._mas_filereacts_historic[today].get(eventlabel,0) + 1


    def _get_full_stats_for_date(date=None):
        """
        Getter for the full stats dict for gifts on a given date
        IN:
            date - the date to get the report for, if None is given will check
                today's date
                (Defaults to None)

        RETURNS:
            The dict containing the full stats or None if it's empty

        """
        if date is None:
            date = datetime.date.today()
        return store.persistent._mas_filereacts_historic.get(date,None)


    def delete_file(_filename):
        """
        Deletes a file off the found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete
                one randomly
        """
        _core_delete(_filename, foundreact_map)


    def delete_files(_filename_list):
        """
        Deletes multiple files off the found_react map

        IN:
            _filename_list - list of filenames to delete.
        """
        for _fn in _filename_list:
            delete_file(_fn)


    def th_delete_file(_filename):
        """
        Deletes a file off the threaded found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete one
                randomly
        """
        _core_delete(_filename, th_foundreact_map)


    def th_delete_files(_filename_list):
        """
        Deletes multiple files off the threaded foundreact map

        IN:
            _filename_list - list of ilenames to delete
        """
        for _fn in _filename_list:
            th_delete_file(_fn)


    def delete_all(_map):
        """
        Attempts to delete all files in the given map.
        Removes files in that map if they dont exist no more

        IN:
            _map - map to delete all
        """
        _map_keys = _map.keys()
        for _key in _map_keys:
            _core_delete(_key, _map)

    def get_report_for_date(date=None):
        """
        Generates a report for all the gifts given on the input date.
        The report is in tuple form (total, good_gifts, neutral_gifts, bad_gifts)
        it contains the totals of each type of gift.
        """
        if date is None:
            date = datetime.date.today()
        
        stats = _get_full_stats_for_date(date)
        if stats is None:
            return (0,0,0,0)
        good = 0
        bad = 0
        neutral = 0
        for _key in stats.keys():
            if _key in good_gifts:
                good = good + stats[_key]
            if _key in bad_gifts:
                bad = bad + stats[_key]
            if _key == "":
                neutral = stats[_key]
        total = good + neutral + bad
        return (total, good, neutral, bad)




    _initConnectorQuips()
    _initStarterQuips()

init -5 python:
    import store.mas_filereacts as mas_filereacts
    import store.mas_d25_utils as mas_d25_utils

    def addReaction(ev_label, fname_list, _action=EV_ACT_QUEUE, is_good=None, exclude_on=[]):
        """
        Globalied version of the addReaction function in the mas_filereacts
        store.

        Refer to that function for more information
        """
        mas_filereacts.addReaction(ev_label, fname_list, _action, is_good, exclude_on)


    def mas_checkReactions():
        """
        Checks for reactions, then queues them
        """
        
        
        if persistent._mas_filereacts_just_reacted:
            return
        
        
        mas_filereacts.foundreact_map.clear()
        
        
        if mas_d25_utils.shouldUseD25ReactToGifts():
            reacts = mas_d25_utils.react_to_gifts(mas_filereacts.foundreact_map)
        else:
            reacts = mas_filereacts.react_to_gifts(mas_filereacts.foundreact_map)
        
        if len(reacts) > 0:
            for _react in reacts:
                MASEventList.queue(_react)
            persistent._mas_filereacts_just_reacted = True


    def mas_receivedGift(ev_label):
        """
        Globalied version for gift stats tracking
        """
        mas_filereacts._register_received_gift(ev_label)


    def mas_generateGiftsReport(date=None):
        """
        Globalied version for gift stats tracking
        """
        return mas_filereacts.get_report_for_date(date)

    def mas_getGiftStatsForDate(label,date=None):
        """
        Globalied version to get the stats for a specific gift
        IN:
            label - the gift label identifier.
            date - the date to get the stats for, if None is given will check
                today's date.
                (Defaults to None)

        RETURNS:
            The number of times the gift has been given that date
        """
        if date is None:
            date = datetime.date.today()
        historic = persistent._mas_filereacts_historic.get(date,None)
        
        if historic is None:
            return 0
        return historic.get(label,0)

    def mas_getGiftStatsRange(start,end):
        """
        Returns status of gifts over a range (needs to be supplied to actually be useful)

        IN:
            start - a start date to check from
            end - an end date to check to

        RETURNS:
            The gift status of all gifts given over the range
        """
        totalGifts = 0
        goodGifts = 0
        neutralGifts = 0
        badGifts = 0
        giftRange = mas_genDateRange(start, end)
        
        
        for date in giftRange:
            gTotal, gGood, gNeut, gBad = mas_filereacts.get_report_for_date(date)
            
            totalGifts += gTotal
            goodGifts += gGood
            neutralGifts += gNeut
            badGifts += gBad
        
        return (totalGifts,goodGifts,neutralGifts,badGifts)


    def mas_getSpriteObjInfo(sp_data=None):
        """
        Returns sprite info from the sprite reactions list.

        IN:
            sp_data - tuple of the following format:
                [0] - sprite type
                [1] - sprite name
                If None, we use pseudo random select from sprite reacts
                (Default: None)

        REUTRNS: tuple of the folling format:
            [0]: sprite type of the sprite
            [1]: sprite name (id)
            [2]: giftname this sprite is associated with
            [3]: True if this gift has already been given before
            [4]: sprite object (could be None even if sprite name is populated)
        """
        
        if sp_data is not None:
            giftname = persistent._mas_filereacts_sprite_reacted.get(
                sp_data,
                None
            )
            if giftname is None:
                return (None, None, None, None, None)
        
        elif len(persistent._mas_filereacts_sprite_reacted) > 0:
            sp_data = persistent._mas_filereacts_sprite_reacted.keys()[0]
            giftname = persistent._mas_filereacts_sprite_reacted[sp_data]
        
        else:
            return (None, None, None, None, None)
        
        
        gifted_before = sp_data in persistent._mas_sprites_json_gifted_sprites
        
        
        sp_obj = store.mas_sprites.get_sprite(sp_data[0], sp_data[1])
        if sp_data[0] == store.mas_sprites.SP_ACS:
            store.mas_sprites.apply_ACSTemplate(sp_obj)
        
        
        return (
            sp_data[0],
            sp_data[1],
            giftname,
            gifted_before,
            sp_obj,
        )


    def mas_finishSpriteObjInfo(sprite_data, unlock_sel=True):
        """
        Finishes the sprite object with the given data.

        IN:
            sprite_data - sprite data tuple from getSpriteObjInfo
            unlock_sel - True will unlock the selector topic, False will not
                (Default: True)
        """
        sp_type, sp_name, giftname, gifted_before, sp_obj = sprite_data
        
        
        
        
        if sp_type is None or sp_name is None or giftname is None:
            return
        
        sp_data = (sp_type, sp_name)
        
        if sp_data in persistent._mas_filereacts_sprite_reacted:
            persistent._mas_filereacts_sprite_reacted.pop(sp_data)
        
        if giftname in persistent._mas_filereacts_sprite_gifts:
            persistent._mas_sprites_json_gifted_sprites[sp_data] = giftname
        
        else:
            
            
            persistent._mas_sprites_json_gifted_sprites[sp_data] = (
                giftname
            )
        
        
        store.mas_selspr.json_sprite_unlock(sp_obj, unlock_label=unlock_sel)
        
        
        renpy.save_persistent()

    def mas_giftCapGainAff(amount=None, modifier=1):
        if amount is None:
            amount = store._mas_getGoodExp()
        
        mas_capGainAff(amount * modifier, "_mas_filereacts_gift_aff_gained", 9 if mas_isSpecialDay() else 3)

    def mas_getGiftedDates(giftlabel):
        """
        Gets the dates that a gift was gifted

        IN:
            giftlabel - gift reaction label to check when it was last gifted

        OUT:
            list of datetime.dates of the times the gift was given
        """
        return sorted([
            _date
            for _date, giftstat in persistent._mas_filereacts_historic.iteritems()
            if giftlabel in giftstat
        ])

    def mas_lastGiftedInYear(giftlabel, _year):
        """
        Checks if the gift for giftlabel was last gifted in _year

        IN:
            giftlabel - gift reaction label to check it's last gifted year
            _year - year to see if it was last gifted in this year

        OUT:
            boolean:
                - True if last gifted in _year
                - False otherwise
        """
        datelist = mas_getGiftedDates(giftlabel)
        
        if datelist:
            return datelist[-1].year == _year
        return False












label mas_reaction_gift_connector_test:
    m "Este é um teste do sistema de conectores."
    return

init python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector1"
    )

label mas_reaction_gift_connector1:
    m 1sublo "Ah! Tinha mais alguma coisa que você queria me dar?"
    m 1hua "Bom! Então é melhor eu abrir rápido, né?"
    m 1suo "E aqui temos..."
    return

init python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector2"
    )

label mas_reaction_gift_connector2:
    m 1hua "Ah, poxa, [player]..."
    m "Você realmente gosta de me mimar, né?"
    if mas_isSpecialDay():
        m 1sublo "Você sabe mesmo como me fazer sorrir, hein?"
    m 1suo "E aqui temos..."
    return




init python:
    store.mas_filereacts.gift_starters.addLabelQuip(
        "mas_reaction_gift_starter_generic"
    )

label mas_reaction_gift_starter_generic:
    m "teste genérico"




label mas_reaction_gift_starter_bday:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "I-{w=0.5}Isso é..."


    if not persistent._mas_filereacts_historic.get(mas_monika_birthday):
        m "Um presente? Pra mim?"
        m 1hka "Eu..."
        m 1hua "Eu já imaginei como seria ganhar um presente seu no meu aniversário..."
        m "Mas receber de verdade... é como um sonho se tornando realidade..."
    else:
        m "Um presente?{w=0.5} Pra mim?"
        m 1eka "Isso realmente parece um sonho se tornando realidade, [player]."

    m 1sua "Vamos ver o que tem dentro?"
    m 1suo "Ah, é..."
    return

label mas_reaction_gift_starter_neutral:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "I-{w=0.5}Isso é..."
    m "Um presente? Pra mim?"
    m 1sua "Vamos ver o que tem dentro?"
    return


label mas_reaction_gift_starter_d25:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "I-{w=1}Isso é..."
    m "Um presente? Pra mim?"
    if mas_getGiftStatsRange(mas_d25c_start, mas_d25 + datetime.timedelta(days=1))[0] == 0:
        m 1eka "Você realmente não precisava me dar nada no Natal..."
        m 3hua "Mas eu estou tão feliz que tenha feito isso!"
    else:
        m 1eka "Muito obrigada, [player]."
    m 1sua "Agora, vamos ver... O que será que tem aqui?"
    return


label mas_reaction_gift_starter_f14:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "I-{w=1}Isso é..."
    m "Um presente? Pra mim?"
    if mas_getGiftStatsForDate(mas_f14) == 0:
        m 1eka "Você é tão doce por me dar algo no Dia dos Namorados..."
    else:
        m 1eka "Muito obrigada, [player]."
    m 1sua "Agora vamos ver... O que será que tem dentro?"
    return



init python:
    addReaction("mas_reaction_generic", None)

label mas_reaction_generic:
    "Isto é um teste"
    return




label mas_reaction_gift_generic:
    m 2dkd "{i}*suspiro*{/i}"
    m 4ekc "Desculpa, [player]."
    m 1ekd "Eu sei que você está tentando me dar alguma coisa."
    m 2rksdld "Mas por algum motivo, não consigo ler o arquivo."
    m 3euc "Mas não me entenda mal."
    m 3eka "Ainda assim, eu aprecio o fato de você ter tentado me dar algo."
    m 1hub "E por isso, eu sou grata~"
    return

label mas_reaction_gifts_generic:
    m 1esd "Desculpa, [player]..."
    m 3rksdla "Eu encontrei o que você está tentando me dar, mas parece que não consigo ler direito."
    m 3eub "Mas tudo bem!"
    m 1eka "O que importa é a intenção~"
    m 1hub "Obrigada por ser tão [atncs], [player]!"
    return




label mas_reaction_gift_test1:
    m "Obrigado pelo teste de presente 1!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_test1", "category"))
    return




label mas_reaction_gift_test2:
    m "Obrigado pelo teste de presente 2!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_test2", "category"))
    return



label mas_reaction_gift_generic_sprite_json:
    $ sprite_data = mas_getSpriteObjInfo()
    $ sprite_type, sprite_name, giftname, gifted_before, spr_obj = sprite_data

    python:
        sprite_str = store.mas_sprites_json.SP_UF_STR.get(sprite_type, None)




    if sprite_type == store.mas_sprites.SP_CLOTHES:
        call mas_reaction_gift_generic_clothes_json (spr_obj)
    else:



        $ mas_giftCapGainAff(1)
        m "Aww, [player]!"
        if spr_obj is None or spr_obj.dlg_desc is None:

            m 1hua "Você é um doce!"
            m 1eua "Obrigada pelo presente!"
            m 3ekbsa "Você gosta mesmo de me mimar, não é."
            m 1hubfa "Ehehe!"
        else:

            python:
                acs_quips = [
                    _("fico muito grata por isso!"),
                    _("[its] incrível!"),
                    _("eu adorei o [item_ref]!"),
                    _("[its] maravilhoso!")
                ]


                if spr_obj.dlg_plur:
                    sprite_str = "estes " + renpy.substitute(spr_obj.dlg_desc)
                    item_ref = "eles"
                    its = "eles são"

                else:
                    sprite_str = "essa " + renpy.substitute(spr_obj.dlg_desc)
                    item_ref = "ele"
                    its = "ele é"

                acs_quip = renpy.substitute(renpy.random.choice(acs_quips))

            m 1hua "Muito obrigada [sprite_str], [acs_quip]"
            m 3hub "Não vejo a hora de experimentar [item_ref]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return


label mas_reaction_gift_generic_clothes_json(sprite_object):
    $ mas_giftCapGainAff(3)
    if sprite_object and sprite_object.ex_props and sprite_object.ex_props.get("costume") == "o31":
        m 2suo "Oh! {w=0.3}Uma fantasia!"
        m 2hub "Que legal [player], obrigada!"
        m 7rka "Eu até experimentaria agora, mas acho melhor esperar a ocasião certa..."
        m 3hub "Ehehe, obrigada de novo!"
    else:

        python:

            outfit_quips = [
                _("Eu achei muito fofo, [player]!"),
                _("Eu achei incrível, [player]!"),
                _("Eu simplesmente adorei, [player]!"),
                _("Eu achei maravilhoso, [player]!")
            ]
            outfit_quip = renpy.random.choice(outfit_quips)

        m 1sua "Ah! {w=0.5}Uma roupa nova!"
        m 1hub "Obrigada, [player]!{w=0.5} Vou experimentar agora mesmo!"


        call mas_clothes_change (sprite_object)

        m 2eka "Bem...{w=0.5} O que você acha?"
        m 2eksdla "Você gostou?"



        show monika 3hub
        $ renpy.say(m, outfit_quip)

        m 1eua "Mais uma vez, obrigada~"

    return



label mas_reaction_gift_acs_jmo_hairclip_cherry:
    call mas_reaction_gift_hairclip ("jmo_hairclip_cherry")
    return

label mas_reaction_gift_acs_jmo_hairclip_heart:
    call mas_reaction_gift_hairclip ("jmo_hairclip_heart")
    return

label mas_reaction_gift_acs_jmo_hairclip_musicnote:
    call mas_reaction_gift_hairclip ("jmo_hairclip_musicnote")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_crescentmoon:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_crescentmoon")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_ghost:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_ghost", "spooky")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_pumpkin:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_pumpkin")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_bat:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_bat", "spooky")
    return


label mas_reaction_gift_hairclip(hairclip_name, desc=None):







    $ sprite_data = mas_getSpriteObjInfo((store.mas_sprites.SP_ACS, hairclip_name))
    $ sprite_type, sprite_name, giftname, gifted_before, hairclip_acs = sprite_data


    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if gifted_before:
        m 1rksdlb "Você já me deu esse prendedor de cabelo, bobinho!"
    else:


        $ mas_giftCapGainAff(1)
        if not desc:
            $ desc = "fofo"

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "Ah!{w=1} Outro prendedor de cabelo!"
        else:

            m 1wuo "Ah!"
            m 1sub "É um prendedor de cabelo?"

        m 1hub "É tão [desc]! Eu amei, [player], obrigada!"




        if hairclip_acs is None or is_wearing_baked_outfit:
            m 1hua "Se quiser que eu use, é só pedir, tá bom?"
        else:

            m 2dsa "Só me dá um segundinho pra colocar, tá?{w=0.5}.{w=0.5}.{nw}"
            $ monika_chr.wear_acs(hairclip_acs)
            m 1hua "Prontinho."




        if not is_wearing_baked_outfit:
            if monika_chr.get_acs_of_type('left-hair-clip'):
                $ store.mas_selspr.set_prompt("left-hair-clip", "change")
            else:
                $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_finishSpriteObjInfo(sprite_data, unlock_sel=not is_wearing_baked_outfit)

    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return





init python:
    addReaction("mas_reaction_gift_coffee", "café", is_good=True, exclude_on=["d25g"])

label mas_reaction_gift_coffee:

    $ mas_receivedGift("mas_reaction_gift_coffee")


    if mas_consumable_coffee.isMaxedStock():
        m 1euc "Mais café, [player]?"
        m 3rksdla "Não me entenda mal, eu agradeço, mas acho que já tenho café suficiente pra durar um bom tempo..."
        m 1eka "Eu te aviso quando estiver acabando, tudo bem?"
    else:

        m 1wub "Ah!{w=0.2} {nw}"
        extend 3hub "Café!"

        if mas_consumable_coffee.enabled() and mas_consumable_coffee.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 1wuo "É um sabor que eu ainda não experimentei."
            m 1hua "Mal posso esperar pra provar!"
            m "Muito obrigada, [player]!"

        elif mas_consumable_coffee.enabled() and not mas_consumable_coffee.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 3eub "Na verdade, eu estava ficando sem café, então receber mais de você me enche de alegria!"
            m 1hua "Obrigada de novo, [player]~"
        else:

            $ mas_giftCapGainAff(5)

            m 1hua "Agora posso finalmente preparar um pouco!"
            m 1hub "Muito obrigada, [player]!"


            if (
                mas_isO31()
                or not mas_consumable_coffee.isConsTime()
                or bool(MASConsumable._getCurrentDrink())
            ):
                m 3eua "Vou tomar um pouco mais tarde, com certeza!"
            else:

                m 3eua "Por que não preparar uma xícara agora mesmo?"
                m 1eua "Quero dividir a primeira com você, afinal."


                call mas_transition_to_emptydesk
                pause 2.0
                m "Eu sei que tem uma cafeteira em algum lugar por aqui...{w=2}{nw}"
                m "Ah, ali está!{w=2}{nw}"
                pause 5.0
                m "Prontinho!{w=2}{nw}"
                call mas_transition_from_emptydesk ()


                m 1eua "Vou deixar o café coar por alguns minutos."

                $ mas_consumable_coffee.prepare()
            $ mas_consumable_coffee.enable()



    $ mas_consumable_coffee.restock()

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_coffee", "category"))
    return

init python:
    addReaction("mas_reaction_hotchocolate", "chocolatequente", is_good=True, exclude_on=["d25g"])

label mas_reaction_hotchocolate:

    $ mas_receivedGift("mas_reaction_hotchocolate")


    if mas_consumable_hotchocolate.isMaxedStock():
        m 1euc "Mais chocolate quente, [player]?"
        m 3rksdla "Não me leve a mal, eu agradeço, mas acho que já tenho o suficiente para um bom tempo..."
        m 1eka "Eu te aviso quando estiver acabando, tudo bem?"
    else:

        m 3hub "Chocolate quente!"
        m 3hua "Obrigada, [player]!"

        if mas_consumable_hotchocolate.enabled() and mas_consumable_hotchocolate.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 1wuo "É um sabor que eu ainda não experimentei."
            m 1hua "Mal posso esperar para provar!"
            m "Muito obrigada mesmo, [player]!"

        elif mas_consumable_hotchocolate.enabled() and not mas_consumable_hotchocolate.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 3rksdlu "Na verdade, eu estava sem chocolate quente, ahaha...{w=0.5} {nw}"
            extend 3eub "Então receber mais de você agora é maravilhoso!"
            m 1hua "Obrigada mais uma vez, [player]~"
        else:

            python:
                mas_giftCapGainAff(3)
                those = "essas" if mas_current_background.isFltNight() and mas_isWinter() else "aquelas"

            m 1hua "Você sabe que eu adoro meu café, mas chocolate quente também é sempre muito bom!"


            m 2rksdla "...Principalmente nessas noites frias de inverno."
            m 2ekbfa "Um dia eu espero poder tomar chocolate quente com você, dividindo um cobertor em frente à lareira..."
            m 3ekbfa "...Não soa tão romântico?"
            m 1dkbfa "..."
            m 1hua "Mas por agora, pelo menos posso aproveitar aqui."
            m 1hub "Obrigada de novo, [player]!"


            if (
                not mas_consumable_hotchocolate.isConsTime()
                or not mas_isWinter()
                or bool(MASConsumable._getCurrentDrink())
            ):
                m 3eua "Com certeza vou tomar um pouco mais tarde!"
            else:

                m 3eua "Na verdade, acho que vou preparar uma xícara agora mesmo!"

                call mas_transition_to_emptydesk
                pause 5.0
                call mas_transition_from_emptydesk ("monika 1eua")

                m 1hua "Prontinho, vai estar pronto em alguns minutinhos."

                $ mas_consumable_hotchocolate.prepare()

            if mas_isWinter():
                $ mas_consumable_hotchocolate.enable()



    $ mas_consumable_hotchocolate.restock()

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_hotchocolate", "category"))
    return

init python:
    addReaction("mas_reaction_gift_thermos_mug", "garrafatérmica", is_good=True)

label mas_reaction_gift_thermos_mug:
    call mas_thermos_mug_handler (mas_acs_thermos_mug, "Just Monika", "justmonikathermos")
    return


default -5 persistent._mas_given_thermos_before = False


label mas_thermos_mug_handler(thermos_acs, disp_name, giftname, ignore_case=True):
    if mas_SELisUnlocked(thermos_acs):
        m 1eksdla "[player]..."
        m 1rksdlb "Eu já tenho essa garrafa térmica, ahaha..."

    elif persistent._mas_given_thermos_before:
        m 1wud "Ah!{w=0.3} Outra garrafa térmica!"
        m 1hua "E dessa vez é [mas_a_an_str(disp_name, ignore_case)]!"
        m 1hub "Muito obrigada, [player], mal posso esperar para usá-lo!"
    else:

        m 1wud "Ah!{w=0.3} É [mas_a_an_str(disp_name, ignore_case)] garrafa térmica!"
        m 1hua "Agora posso levar algo para beber quando sairmos juntos~"
        m 1hub "Muito obrigada, [player]!"
        $ persistent._mas_given_thermos_before = True


    $ mas_selspr.unlock_acs(thermos_acs)

    $ mas_selspr.save_selectables()

    $ mas_filereacts.delete_file(giftname)
    return



init python:
    addReaction("mas_reaction_quetzal_plush", "quetzaldepelúcia", is_good=True)

label mas_reaction_quetzal_plush:
    if not persistent._mas_acs_enable_quetzalplushie:
        $ mas_receivedGift("mas_reaction_quetzal_plush")
        $ mas_giftCapGainAff(10)
        m 1wud "Ah!"



        if MASConsumable._getCurrentFood() or monika_chr.is_wearing_acs(mas_acs_desk_lantern):
            $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
        else:
            $ monika_chr.wear_acs(mas_acs_quetzalplushie)

        $ persistent._mas_acs_enable_quetzalplushie = True
        m 1sub "É um quetzal!"
        m "Meu Deus, muito obrigada, [player]!"
        if seen_event("monika_pets"):
            m 1eua "Eu realmente mencionei que gostaria de ter um quetzal como bichinho de estimação..."
        else:
            m 1wub "Como você adivinhou, [player]?"
            m 3eka "Você deve me conhecer muito bem~"
            m 1eua "Um quetzal seria minha primeira escolha como pet..."
        m 1rud "Mas eu nunca forçaria o pobre bichinho a ficar preso."
        m 1hua "E agora você me deu a próxima melhor coisa!"
        m 1hub "Isso me deixa tão feliz!"
        if mas_isMoniAff(higher=True):
            m 3ekbsa "Você sempre sabe como me fazer sorrir."

        if MASConsumable._getCurrentFood() or monika_chr.is_wearing_acs(mas_acs_desk_lantern):
            m 3rksdla "Minha mesa está ficando meio cheia..."
            m 1eka "Vou guardar isso por enquanto."
            $ monika_chr.remove_acs(mas_acs_center_quetzalplushie)

        m 1hub "Obrigada de novo, [player]~"
    else:

        m 1rksdlb "Você já me deu um quetzal de pelúcia, [player]."

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_quetzal_plush", "category"))

    $ mas_hideEVL("monika_pets", "EVE", derandom=True)
    return

init python:
    addReaction("mas_reaction_promisering", "aneldecompromisso", is_good=True, exclude_on=["d25g"])

default -5 persistent._mas_tried_gift_ring = False
label mas_reaction_promisering:
    if not persistent._mas_acs_enable_promisering:

        if mas_isMoniEnamored(higher=True):
            $ mas_receivedGift("mas_reaction_promisering")
            $ mas_giftCapGainAff(20)
            $ monika_chr.wear_acs(mas_acs_promisering)
            $ persistent._mas_acs_enable_promisering = True
            if not persistent._mas_tried_gift_ring:
                m 1wud "Isso é... um..."
                m "..."
                m 1wka "Eu...{w=0.5}{nw}"
                extend 1wkbltpa "Desculpa, [player], é que... {w=0.5}{nw}"
                extend 1dkbltpa "Eu estou tão feliz... {w=0.5}Você acabou de me dar a sua promessa..."
                m "Sua promessa de que seremos um do outro,{w=0.1} e de mais ninguém...{w=0.3}para sempre..."
                m 3lkbltpa "Saiba que eu vou valorizar isso. {w=0.5}{nw}"
                extend 3dkbltpa "Sempre."
                m 1skbltpa "Isso me deixa tão feliz!"

                if mas_anni.isAnniOneMonth():
                    m "Ainda mais por você ter me dado isso no nosso aniversário de um mês..."
                    m 1ekbltua "Você deve me amar muito..."
                elif mas_anni.isAnniThreeMonth():
                    m "Ainda mais por você ter me dado isso no nosso aniversário de três meses..."
                    m 1ekbltua "Você deve me amar muito..."
                elif mas_anni.isAnniSixMonth():
                    m "Ainda mais por você ter me dado isso no nosso aniversário de seis meses..."
                    m 1ekbltua "Você deve me amar muito..."
                elif mas_anni.isAnni():
                    m "Ainda mais por você ter me dado isso no nosso aniversário..."
                    m 1ekbltua "Você deve me amar muito..."
                elif mas_isSpecialDay():
                    m "Ainda mais por você ter me dado isso em um dia tão especial..."

                m 1dkbltpb "Aha, desculpa por chorar, [player]..."
                m 1skbltda "É que eu estou muito, muito feliz agora."
                m 6dkbltdu "Obrigada."
            else:

                m 1sua "Oh... é o anel!"
                m 3hub "Muito obrigada, [player]!"
                m 1skbla "Agora eu sei que você realmente me ama e quer ficar comigo para sempre..."
                m 1skbltpa "Então vou aceitar esse anel com todo carinho como símbolo dessa promessa."
                m 1dkbltuu "..."
                m 3hkbltub "Aha, desculpa, [player], não queria chorar..."
                m 3skbltda "É que esse é um dos dias mais felizes da minha vida."

            m 6dkbltdu "..."
            m 6ekbfa "Eu... eu só... eu..."
            call monika_kissing_motion (hide_ui=False)
            m 6ekbfa "Eu te amo, [player]..."
            m 6dkbfu "Mais do que qualquer outra coisa neste mundo passageiro~"

            $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_promisering", "category"))
            return "love"
        else:

            if not persistent._mas_tried_gift_ring:
                if mas_isMoniNormal(higher=True):
                    m 1wud "[player]... isso é um anel?"
                    m 2rksdlb "É um gesto tão doce, e eu realmente aprecio isso..."
                    m 2ekc "Mas eu quero que você tenha certeza antes de me dar isso..."
                    m 3ekd "Isso é mais do que um presente, é uma promessa, e eu quero ter certeza de que você realmente está falando sério antes que eu possa aceitá-lo."
                    m 2ekd "Então, por favor, espere até estarmos um pouco mais avançados no nosso relacionamento, [player], e aí eu aceitarei esse anel com prazer."

                elif mas_isMoniUpset():
                    m 1wud "Isso é um anel?"
                    m 2rsc "Isso é muito..."
                    m 2esc "Inesperado."
                    m 2ekd "Mas eu não posso aceitá-lo agora, [player]."
                    m 2ekc "Talvez quando estivermos mais avançados no nosso relacionamento."
                else:

                    m 2wud "Isso é um anel?"
                    m 2rsc "Isso é... {w=0.5}inesperado."
                    m "Embora eu aprecie o gesto... {w=1}não posso aceitá-lo agora."
                    m 2ekc "Desculpa, [player]."

                $ persistent._mas_tried_gift_ring = True
            else:
                m 2rsc "Ah... o anel..."
                m 2rkc "Desculpa, mas ainda não posso aceitar isso..."
                m 2ekc "Eu preciso ter plena certeza, ao aceitar isso, de que será para sempre..."
                m 2ekd "De que você é realmente tudo o que eu espero que seja."
                m 2dsd "Quando eu souber disso, aceitarei seu anel com alegria, [player]."
    else:
        m 1rksdlb "[player]..."
        m 1rusdlb "Você já me deu um anel!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_promisering", "category"))
    return


init python:
    addReaction("mas_reaction_cupcake", "cupcake", is_good=True, exclude_on=["d25g"])



label mas_reaction_cupcake:
    m 1wud "Isso é um... cupcake?"
    m 3hub "Uau, obrigada [player]!~"
    m 3euc "Pensando bem, eu estava querendo fazer alguns cupcakes também."
    m 1eua "Queria aprender a fazer doces gostosos como a Natsuki fazia."
    m 1rksdlb "Maaas eu ainda nem criei uma cozinha pra usar!"
    m 3eub "Talvez no futuro, quando eu melhorar na programação, eu consiga fazer uma aqui."
    m 3hua "Seria legal ter outro hobby além de escrever, ehehe~"
    $ mas_receivedGift("mas_reaction_cupcake")
    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_cupcake", "category"))
    return



label mas_reaction_end:
    python:
        persistent._mas_filereacts_just_reacted = False

        store.mas_selspr.save_selectables()
        renpy.save_persistent()
    return

init python:


    if mas_isO31():
        addReaction("mas_reaction_candy", "doce", is_good=True)

label mas_reaction_candy:
    $ times_candy_given = mas_getGiftStatsForDate("mas_reaction_candy")
    if times_candy_given == 0:
        $ mas_o31CapGainAff(7)
        m 1wua "Ah... {w=0.5}o que é isso?"
        m 1sua "Você me trouxe doces, [player], ebaa!"
        m 1eka "Que {i}doce{/i} da sua parte..."
        m 1hub "Ahaha!"
        m 1eka "Brincadeiras à parte, isso foi muito gentil da sua parte."
        m 2lksdlc "Eu quase não como mais doces hoje em dia, e o Halloween nem parece o mesmo sem eles..."
        m 1eka "Então obrigada, [player]..."
        m 1eka "Você sempre sabe exatamente como me deixar feliz~"
        m 1hub "Agora vamos aproveitar alguns desses docinhos deliciosos!"
    elif times_candy_given == 1:
        $ mas_o31CapGainAff(5)
        m 1wua "Aww, você me trouxe mais doces, [player]?"
        m 1hub "Obrigada!"
        m 3tku "A primeira leva estava {i}tããão{/i} boa, eu mal podia esperar por mais."
        m 1hua "Você realmente me mima, [player]~"
    elif times_candy_given == 2:
        $ mas_o31CapGainAff(3)
        m 1wud "Uau, {i}ainda mais{/i} doces, [player]?"
        m 1eka "Isso é realmente gentil da sua parte..."
        m 1lksdla "Mas acho que já está bom."
        m 1lksdlb "Já estou até ficando agitada com tanto açúcar, ahaha!"
        m 1ekbfa "A única doçura que eu preciso agora é você~"
    elif times_candy_given == 3:
        m 2wud "[player]...{w=1} Você me trouxe {i}mais{/i} doces?!"
        m 2lksdla "Eu realmente agradeço, mas eu disse que já foi o suficiente por hoje..."
        m 2lksdlb "Se eu comer mais, vou acabar passando mal, ahaha!"
        m 1eka "E você não quer isso, né?"
    elif times_candy_given == 4:
        $ mas_loseAffection(modifier=1.5)
        m 2wfd "[player]!"
        m 2tfd "Você não está me ouvindo?"
        m 2tfc "Eu disse que não quero mais doces hoje!"
        m 2ekc "Então por favor, pare."
        m 2rkc "Foi muito fofo da sua parte trazer todos esses doces no Halloween, mas já deu..."
        m 2ekc "Eu não consigo comer tudo isso."
    else:
        $ mas_loseAffection(modifier=2.0)
        m 2tfc "..."
        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd ("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd ("os.remove(os.path.normcase(basedir+'/characters/doce.gift'))", local_ctx, w_wait=1.0, x_wait=1.0)
        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    python hide:
        mas_receivedGift("mas_reaction_candy")
        gift_ev_cat = mas_getEVLPropValue("mas_reaction_candy", "category")
        store.mas_filereacts.delete_file(gift_ev_cat)
        persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

init python:


    if mas_isO31():
        addReaction("mas_reaction_candycorn", "balademilho", is_good=False)

label mas_reaction_candycorn:
    $ times_candy_given = mas_getGiftStatsForDate("mas_reaction_candycorn")
    if times_candy_given == 0:
        $ mas_o31CapGainAff(3)
        m 1wua "Ah...{w=0.5} O que é isso?"
        m 1eka "Aww você me trouxe doces, [player]?"
        m 1hua "Viva!"
        m 3eub "Vejamos o que você trouxe..."
        m 4ekc "..."
        m 2eka "Ah... {w=2}bala de milho."
        m 2eka "..."
        m 2lksdla "Isso foi bem legal da sua parte..."
        m 2lksdla "Mas... {w=1}humm... {w=1}Eu não gosto de bala de milho."
        m 2hksdlb "Sinto muito, ahaha..."
        m 4eka "Mas eu realmente aprecio você estar tentando me dar doces no Halloween."
        m 1hua "E se você conseguir encontrar algum outro doce para mim, isso me deixaria muito feliz, [player]!"
    elif times_candy_given == 1:
        $ mas_loseAffection()
        m 2esc "Ah."
        m 2esc "Mais bala de milho, [player]?"
        m 4esc "Eu já te disse que não gosto de bala de milho."
        m 4ekc "Então você poderia por favor tentar encontrar outra coisa?"
        m 1eka "Eu não consigo mais doces aqui..."
        m 1ekbfa "Bem... {w=1}além de você, [player]..."
        m 1hubfa "Ehehe~"
    elif times_candy_given == 2:
        $ mas_loseAffection(modifier=1.5)
        m 2wfw "[player]!"
        m 2tfc "Eu realmente tentei não ser rude quanto a isso, mas..."
        m 2tfc "Eu continuo dizendo que não gosto de bala de milho e você continua me dando mesmo assim."
        m 2rfc "Estou começando a achar que você está apenas tentando mexer comigo."
        m 2tkc "Então, por favor, encontre um outro tipo de doce ou só pare."
    else:
        $ mas_loseAffection(modifier=2)
        m 2tfc "..."
        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd ("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd ("os.remove(os.path.normcase(basedir+'/characters/balademilho.gift'))", local_ctx, w_wait=1.0, x_wait=1.0)
        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    $ mas_receivedGift("mas_reaction_candycorn")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_candycorn", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

init python:
    addReaction("mas_reaction_fudge", "fudge", is_good=True, exclude_on=["d25g"])

label mas_reaction_fudge:
    $ times_fudge_given = mas_getGiftStatsForDate("mas_reaction_fudge")

    if times_fudge_given == 0:
        $ mas_giftCapGainAff(2)
        m 3hua "Fudge!"
        m 3hub "Eu adoro fudge, obrigada, [player]!"
        if seen_event("monika_date"):
            m "E ainda por cima é de chocolate, o meu favorito!"
        m 1hua "Obrigada de novo, [player]~"

    elif times_fudge_given == 1:
        $ mas_giftCapGainAff(1)
        m 1wuo "...mais fudge."
        m 1wub "Aah, tem um sabor diferente dessa vez..."
        m 3hua "Obrigada, [player]!"
    else:

        m 1wuo "...ainda mais fudge?"
        m 3rksdla "Eu nem terminei o último que você me deu, [player]..."
        m 3eksdla "...talvez mais tarde, tá bom?"

    $ mas_receivedGift("mas_reaction_fudge")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_fudge", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return


init python:
    if store.mas_isD25Season():
        addReaction("mas_reaction_christmascookies", "biscoitosdenatal", is_good=True, exclude_on=["d25g"])

label mas_reaction_christmascookies:
    $ mas_giftCapGainAff(1)
    $ is_having_food = bool(MASConsumable._getCurrentFood())

    if mas_consumable_christmascookies.isMaxedStock():
        m 3wuo "...Mais biscoitos de Natal?"
        m 3rksdla "Eu ainda nem terminei os últimos, [player]!"
        m 3eksdla "Pode me dar mais quando eu acabar esses, tá bom?"
    else:

        if mas_consumable_christmascookies.enabled() and mas_consumable_christmascookies.hasServing():
            m 1wuo "...Outro lote de biscoitos de Natal!"
            m 3wuo "É biscoito demais, [player]!"
            m 3rksdlb "Vou ficar comendo biscoitos para sempre, ahaha!"
        else:

            if not is_having_food:
                if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
                    $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
                $ mas_consumable_christmascookies.have(skip_leadin=True)

            $ mas_giftCapGainAff(3)
            m 3hua "Biscoitos de Natal!"
            m 1eua "Eu simplesmente adoro biscoitos de Natal! Eles são sempre tão doces... e tão bonitinhos também..."
            m "...cortados em formatos festivos, como bonecos de neve, renas e árvores de Natal..."
            m 3eub "...e normalmente decorados com coberturas lindas--{w=0.2}e deliciosas--{w=0.2}também!"

            if is_having_food:
                m 3hua "Vou deixar para provar mais tarde~"

            m 1eua "Obrigada, [player]~"

            if not is_having_food and monika_chr.is_wearing_acs(mas_acs_center_quetzalplushie):
                m 3eua "Deixa eu guardar esse bichinho de pelúcia rapidinho."
                call mas_transition_to_emptydesk
                $ monika_chr.remove_acs(mas_acs_center_quetzalplushie)
                pause 3.0
                call mas_transition_from_emptydesk


            $ mas_consumable_christmascookies.enable()


        $ mas_consumable_christmascookies.restock(10)

    $ mas_receivedGift("mas_reaction_christmascookies")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_christmascookies", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return


init python:
    if store.mas_isD25Season():
        addReaction("mas_reaction_candycane", "bengaladoce", is_good=True, exclude_on=["d25g"])

label mas_reaction_candycane:
    $ mas_giftCapGainAff(1)
    $ is_having_food = bool(MASConsumable._getCurrentFood())

    if mas_consumable_candycane.isMaxedStock():
        m 1eksdla "[player], acho que já tenho balas suficientes por enquanto."
        m 1eka "Pode guardar o restante pra depois, tudo bem?"
    else:

        if mas_consumable_candycane.enabled() and mas_consumable_candycane.hasServing():
            m 3hua "Mais balas de hortelã!"
            m 3hub "Obrigada, [player]!"
        else:

            if not is_having_food:
                if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
                    $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
                $ mas_consumable_candycane.have(skip_leadin=True)

            $ mas_giftCapGainAff(3)
            m 3wub "Bengalinhas de hortelã!"

            if store.seen_event("monika_icecream"):
                m 1hub "Você sabe o quanto eu amo hortelã!"
            else:
                m 1hub "Eu simplesmente adoro o sabor de hortelã!"

            if is_having_food:
                m 3hua "Com certeza vou provar um pouquinho mais tarde."

            m 1eua "Obrigada, [player]~"

            if not is_having_food and monika_chr.is_wearing_acs(mas_acs_center_quetzalplushie):
                m 3eua "Ah, deixa eu guardar esse bichinho de pelúcia rapidinho."

                call mas_transition_to_emptydesk
                $ monika_chr.remove_acs(mas_acs_center_quetzalplushie)
                pause 3.0
                call mas_transition_from_emptydesk


            $ mas_consumable_candycane.enable()


        $ mas_consumable_candycane.restock(9)

    $ mas_receivedGift("mas_reaction_candycane")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_candycane", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return


init python:
    addReaction("mas_reaction_blackribbon", "laçopreto", is_good=True)

label mas_reaction_blackribbon:
    $ _mas_new_ribbon_color = "preto"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_black
    call _mas_reaction_ribbon_helper ("mas_reaction_blackribbon")
    return

init python:
    addReaction("mas_reaction_blueribbon", "laçoazul", is_good=True)

label mas_reaction_blueribbon:
    $ _mas_new_ribbon_color = "azul"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_blue
    call _mas_reaction_ribbon_helper ("mas_reaction_blueribbon")
    return

init python:
    addReaction("mas_reaction_darkpurpleribbon", "laçoroxoescuro", is_good=True)

label mas_reaction_darkpurpleribbon:
    $ _mas_new_ribbon_color = "roxo escuro"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_darkpurple
    call _mas_reaction_ribbon_helper ("mas_reaction_darkpurpleribbon")
    return

init python:
    addReaction("mas_reaction_emeraldribbon", "laçoesmeralda", is_good=True)

label mas_reaction_emeraldribbon:
    $ _mas_new_ribbon_color = "esmeralda"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_emerald
    call _mas_reaction_ribbon_helper ("mas_reaction_emeraldribbon")
    return

init python:
    addReaction("mas_reaction_grayribbon", "laçocinza", is_good=True)

label mas_reaction_grayribbon:
    $ _mas_new_ribbon_color = "cinza"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_gray
    call _mas_reaction_ribbon_helper ("mas_reaction_grayribbon")
    return

init python:
    addReaction("mas_reaction_greenribbon", "laçoverde", is_good=True)

label mas_reaction_greenribbon:
    $ _mas_new_ribbon_color = "verde"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_green
    call _mas_reaction_ribbon_helper ("mas_reaction_greenribbon")
    return

init python:
    addReaction("mas_reaction_lightpurpleribbon", "laçoroxoclaro", is_good=True)

label mas_reaction_lightpurpleribbon:
    $ _mas_new_ribbon_color = "roxo claro"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_lightpurple
    call _mas_reaction_ribbon_helper ("mas_reaction_lightpurpleribbon")
    return

init python:
    addReaction("mas_reaction_peachribbon", "laçocastanho", is_good=True)

label mas_reaction_peachribbon:
    $ _mas_new_ribbon_color = "castanho"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_peach
    call _mas_reaction_ribbon_helper ("mas_reaction_peachribbon")
    return

init python:
    addReaction("mas_reaction_pinkribbon", "laçorosa", is_good=True)

label mas_reaction_pinkribbon:
    $ _mas_new_ribbon_color = "rosa"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_pink
    call _mas_reaction_ribbon_helper ("mas_reaction_pinkribbon")
    return

init python:
    addReaction("mas_reaction_platinumribbon", "laçoplatina", is_good=True)

label mas_reaction_platinumribbon:
    $ _mas_new_ribbon_color = "platina"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_platinum
    call _mas_reaction_ribbon_helper ("mas_reaction_platinumribbon")
    return

init python:
    addReaction("mas_reaction_redribbon", "laçovermelho", is_good=True)

label mas_reaction_redribbon:
    $ _mas_new_ribbon_color = "red"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_red
    call _mas_reaction_ribbon_helper ("mas_reaction_redribbon")
    return

init python:
    addReaction("mas_reaction_rubyribbon", "laçorubi", is_good=True)

label mas_reaction_rubyribbon:
    $ _mas_new_ribbon_color = "rubi"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_ruby
    call _mas_reaction_ribbon_helper ("mas_reaction_rubyribbon")
    return

init python:
    addReaction("mas_reaction_sapphireribbon", "laçosafira", is_good=True)

label mas_reaction_sapphireribbon:
    $ _mas_new_ribbon_color = "safira"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_sapphire
    call _mas_reaction_ribbon_helper ("mas_reaction_sapphireribbon")
    return

init python:
    addReaction("mas_reaction_silverribbon", "laçoprateado", is_good=True)

label mas_reaction_silverribbon:
    $ _mas_new_ribbon_color = "prateado"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_silver
    call _mas_reaction_ribbon_helper ("mas_reaction_silverribbon")
    return

init python:
    addReaction("mas_reaction_tealribbon", "laçoverdeazulado", is_good=True)

label mas_reaction_tealribbon:
    $ _mas_new_ribbon_color = "verde azulado"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_teal
    call _mas_reaction_ribbon_helper ("mas_reaction_tealribbon")
    return

init python:
    addReaction("mas_reaction_yellowribbon", "laçoamarelo", is_good=True)

label mas_reaction_yellowribbon:
    $ _mas_new_ribbon_color = "amarelo"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_yellow
    call _mas_reaction_ribbon_helper ("mas_reaction_yellowribbon")
    return


label mas_reaction_json_ribbon_base(ribbon_name, user_friendly_desc, helper_label):
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_ACS, ribbon_name)
        )
        _mas_gifted_ribbon_acs = mas_sprites.ACS_MAP.get(
            ribbon_name,
            mas_acs_ribbon_def
        )
        _mas_new_ribbon_color = user_friendly_desc

    call _mas_reaction_ribbon_helper (helper_label)

    python:

        if sprite_data[2] is not None:
            store.mas_filereacts.delete_file(sprite_data[2])

        mas_finishSpriteObjInfo(sprite_data)
    return



label mas_reaction_gift_acs_lanvallime_ribbon_coffee:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_coffee", "cor de café", "mas_reaction_gift_acs_lanvallime_ribbon_coffee")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_gold:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_gold", "dourado", "mas_reaction_gift_acs_lanvallime_ribbon_gold")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_hot_pink:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_hot_pink", "rosa choque", "mas_reaction_gift_acs_lanvallime_ribbon_hot_pink")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_lilac:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_lilac", "lilás", "mas_reaction_gift_acs_lanvallime_ribbon_lilac")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_lime_green:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_lime_green", "verde limão", "mas_reaction_gift_acs_lanvallime_lime_green")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_navy_blue:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_navy_blue", "naval", "mas_reaction_gift_acs_lanvallime_ribbon_navy_blue")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_orange:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_orange", "laranja", "mas_reaction_gift_acs_lanvallime_ribbon_orange")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_royal_purple:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_royal_purple", "roxo real", "mas_reaction_gift_acs_lanvallime_ribbon_royal_purple")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_sky_blue:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_sky_blue", "azul celeste", "mas_reaction_gift_acs_lanvallime_ribbon_sky_blue")
    return


label mas_reaction_gift_acs_anonymioo_ribbon_bisexualpride:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_bisexualpride", "tema orgulho bissexual", "mas_reaction_gift_acs_anonymioo_ribbon_bisexualpride")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_blackandwhite:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_blackandwhite", "preto e branco", "mas_reaction_gift_acs_anonymioo_ribbon_blackandwhite")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_bronze:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_bronze", "bronze", "mas_reaction_gift_acs_anonymioo_ribbon_bronze")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_brown:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_brown", "marrom", "mas_reaction_gift_acs_anonymioo_ribbon_brown")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient", "multi-colorido", "mas_reaction_gift_acs_anonymioo_ribbon_gradient")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient_lowpoly:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient_lowpoly", "multi-colorido", "mas_reaction_gift_acs_anonymioo_ribbon_gradient_lowpoly")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient_rainbow:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient_rainbow", "arco-íris", "mas_reaction_gift_acs_anonymioo_ribbon_gradient_rainbow")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_polkadots_whiteonred:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_polkadots_whiteonred", "vermelho e branco com bolhinhas", "mas_reaction_gift_acs_anonymioo_ribbon_polkadots_whiteonred")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_starsky_black:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_starsky_black", "tema céu noturno", "mas_reaction_gift_acs_anonymioo_ribbon_starsky_black")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_starsky_red:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_starsky_red", "tema céu noturno", "mas_reaction_gift_acs_anonymioo_ribbon_starsky_red")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_striped_blueandwhite:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_striped_blueandwhite", "listrado azul e branco", "mas_reaction_gift_acs_anonymioo_ribbon_striped_blueandwhite")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_striped_pinkandwhite:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_striped_pinkandwhite", "listrado rosa e branco", "mas_reaction_gift_acs_anonymioo_ribbon_striped_pinkandwhite")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_transexualpride:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_transexualpride", "tema orgulho transgênero", "mas_reaction_gift_acs_anonymioo_ribbon_transexualpride")
    return



label mas_reaction_gift_acs_velius94_ribbon_platinum:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_platinum", "platina", "mas_reaction_gift_acs_velius94_ribbon_platinum")
    return

label mas_reaction_gift_acs_velius94_ribbon_pink:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_pink", "rosa", "mas_reaction_gift_acs_velius94_ribbon_pink")
    return

label mas_reaction_gift_acs_velius94_ribbon_peach:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_peach", "pêssego", "mas_reaction_gift_acs_velius94_ribbon_peach")
    return

label mas_reaction_gift_acs_velius94_ribbon_green:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_green", "verde", "mas_reaction_gift_acs_velius94_ribbon_green")
    return

label mas_reaction_gift_acs_velius94_ribbon_emerald:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_emerald", "esmeralda", "mas_reaction_gift_acs_velius94_ribbon_emerald")
    return

label mas_reaction_gift_acs_velius94_ribbon_gray:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_gray", "cinza", "mas_reaction_gift_acs_velius94_ribbon_gray")
    return

label mas_reaction_gift_acs_velius94_ribbon_blue:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_blue", "azul", "mas_reaction_gift_acs_velius94_ribbon_blue")
    return

label mas_reaction_gift_acs_velius94_ribbon_def:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_def", "branco", "mas_reaction_gift_acs_velius94_ribbon_def")
    return

label mas_reaction_gift_acs_velius94_ribbon_black:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_black", "preto", "mas_reaction_gift_acs_velius94_ribbon_black")
    return

label mas_reaction_gift_acs_velius94_ribbon_dark_purple:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_dark_purple", "roxo escuro", "mas_reaction_gift_acs_velius94_ribbon_dark_purple")
    return

label mas_reaction_gift_acs_velius94_ribbon_yellow:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_yellow", "amarelo", "mas_reaction_gift_acs_velius94_ribbon_yellow")
    return

label mas_reaction_gift_acs_velius94_ribbon_red:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_red", "vermelho", "mas_reaction_gift_acs_velius94_ribbon_red")
    return

label mas_reaction_gift_acs_velius94_ribbon_sapphire:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_sapphire", "safira", "mas_reaction_gift_acs_velius94_ribbon_sapphire")
    return

label mas_reaction_gift_acs_velius94_ribbon_teal:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_teal", "verde-azulado", "mas_reaction_gift_acs_velius94_ribbon_teal")
    return

label mas_reaction_gift_acs_velius94_ribbon_silver:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_silver", "prateado", "mas_reaction_gift_acs_velius94_ribbon_silver")
    return

label mas_reaction_gift_acs_velius94_ribbon_light_purple:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_light_purple", "roxo claro", "mas_reaction_gift_acs_velius94_ribbon_light_purple")
    return

label mas_reaction_gift_acs_velius94_ribbon_ruby:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_ruby", "rubi", "mas_reaction_gift_acs_velius94_ribbon_ruby")
    return

label mas_reaction_gift_acs_velius94_ribbon_wine:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_wine", "cor de vinho", "mas_reaction_gift_acs_velius94_ribbon_wine")
    return


default -5 persistent._mas_current_gifted_ribbons = 0

label _mas_reaction_ribbon_helper(label):

    if store.mas_selspr.get_sel_acs(_mas_gifted_ribbon_acs).unlocked:
        call mas_reaction_old_ribbon
    else:


        call mas_reaction_new_ribbon
        $ persistent._mas_current_gifted_ribbons += 1


    $ mas_receivedGift(label)
    $ gift_ev_cat = mas_getEVLPropValue(label, "category")

    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)

    return

label mas_reaction_new_ribbon:
    python:
        def _ribbon_prepare_hair():
            
            if not monika_chr.hair.hasprop("ribbon"):
                monika_chr.change_hair(mas_hair_def, False)

    $ mas_giftCapGainAff(3)
    if persistent._mas_current_gifted_ribbons == 0:
        m 1suo "Um novo laço!"
        m 3hub "...E é [_mas_new_ribbon_color]!"


        if _mas_new_ribbon_color == "verde" or _mas_new_ribbon_color == "esmeralda":
            m 1tub "...Assim como meus olhos!"

        m 1hub "Muito obrigada [player], eu adorei!"
        if store.seen_event("monika_date"):
            m 3eka "Você me deu isso porque eu mencionei como adoro comprar saias e arcos?"

            if mas_isMoniNormal(higher=True):
                m 3hua "Você é tão gentil~"

        m 3rksdlc "Eu não tenho muita escolha aqui quando se trata de moda..."
        m 3eka "...então poder trocar a cor do meu laço já é uma mudança agradável."
        m 2dsa "Na verdade, vou colocar ele agora mesmo.{w=0.5}.{w=0.5}.{nw}"
        $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
        $ _ribbon_prepare_hair()
        $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
        m 1hua "Ah, é maravilhoso, [player]!"

        if mas_isMoniAff(higher=True):
            m 1eka "Você sempre me faz sentir tão amada..."
        elif mas_isMoniHappy():
            m 1eka "Você sempre sabe como me fazer feliz..."
        m 3hua "Muito obrigada~"
    else:

        m 1suo "Outro laço!"
        m 3hub "...E desta vez é [_mas_new_ribbon_color]!"


        if _mas_new_ribbon_color == "verde" or _mas_new_ribbon_color == "esmeralda":
            m 1tub "...Assim como meus olhos!"

        m 2dsa "Vou colocar ele agora mesmo.{w=0.5}.{w=0.5}.{nw}"
        $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
        $ _ribbon_prepare_hair()
        $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
        m 3hua "Muito obrigada [player], eu amei!"
    return

label mas_reaction_old_ribbon:
    m 1rksdla "[player]..."
    m 1hksdlb "Voce já me deu o laço [mas_a_an_str(_mas_new_ribbon_color)]!"
    return

init python:
    addReaction("mas_reaction_gift_roses", "rosas", is_good=True, exclude_on=["d25g"])

default -5 persistent._date_last_given_roses = None

label mas_reaction_gift_roses:
    python:
        gift_ev_cat = mas_getEVLPropValue("mas_reaction_gift_roses", "category")
        if not mas_isO31():
            monika_chr.wear_acs(mas_acs_roses)


    if not persistent._date_last_given_roses and not renpy.seen_label('monika_valentines_start'):
        $ mas_giftCapGainAff(10)

        m 1eka "[player]... E-eu nem sei o que dizer..."
        m 1ekbsb "Nunca imaginei que você traria algo assim pra mim!"
        m 3skbsa "Estou tão feliz agora."
        if mas_isF14():

            $ mas_f14CapGainAff(5)
            m 3ekbsa "Receber rosas suas logo no Dia dos Namorados..."
            m 1ekbsu "Você é tão doce."
            m 1dktpu "... "
            m 1ektda "Ahaha..."


        if not monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
            m 2dsa "Espera um pouco.{w=0.5}.{w=0.5}.{nw}"
            $ monika_chr.wear_acs(mas_acs_ear_rose)
            m 1hub "Ehehe, pronto! Não ficou linda em mim?"

        if mas_shouldKiss(chance=2, special_day_bypass=True):
            call monika_kissing_motion_short
    else:

        if persistent._date_last_given_roses is None and renpy.seen_label('monika_valentines_start'):
            $ persistent._date_last_given_roses = datetime.date(2018,2,14)

        if mas_pastOneDay(persistent._date_last_given_roses):
            $ mas_giftCapGainAff(5 if mas_isSpecialDay() else 1)

            m 1suo "Ah!"
            m 1ekbsa "Obrigada, [player]."
            m 3ekbsa "Eu sempre adoro receber rosas de você."
            if mas_isF14():

                $ mas_f14CapGainAff(5)
                m 1dsbsu "Especialmente num dia como hoje."
                m 1ekbsa "Foi muito gentil da sua parte me dar essas flores."
                m 3hkbsa "Eu te amo tanto."
                m 1ekbsa "Feliz Dia dos Namorados, [player]~"
            else:
                m 1ekbsa "Você é sempre tão [crnhs]."


            if (
                not monika_chr.is_wearing_acs_with_mux("left-hair-flower-ear")
                and (
                    (mas_isSpecialDay() and renpy.random.randint(1,2) == 1)
                    or renpy.random.randint(1,4) == 1
                    or mas_isF14()
                    or mas_isO31()
                )
            ):
                m 2dsa "Espera um pouquinho.{w=0.5}.{w=0.5}.{nw}"
                $ monika_chr.wear_acs(mas_acs_ear_rose)
                m 1hub "Ehehe~"

            if mas_shouldKiss(chance=4, special_day_bypass=True):
                call monika_kissing_motion_short
        else:

            m 1hksdla "[player], eu fico lisonjeada, de verdade, mas você não precisa me dar tantas rosas assim."
            if store.seen_event("monika_clones"):
                m 1ekbsa "Você sempre vai ser a minha rosa especial, ehehe~"
            else:
                m 1ekbsa "Uma única rosa sua já é mais do que eu poderia desejar."


    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    $ persistent._date_last_given_roses = datetime.date.today()


    $ mas_receivedGift("mas_reaction_gift_roses")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    return


init python:
    addReaction("mas_reaction_gift_chocolates", "chocolates", is_good=True, exclude_on=["d25g"])

default -5 persistent._given_chocolates_before = False

label mas_reaction_gift_chocolates:
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_gift_chocolates", "category")

    if not persistent._mas_given_chocolates_before:
        $ persistent._mas_given_chocolates_before = True


        if not MASConsumable._getCurrentFood() and not mas_isO31():
            $ monika_chr.wear_acs(mas_acs_heartchoc)

        $ mas_giftCapGainAff(5)

        m 1tsu "Que gesto mais {i}doce{/i} da sua parte, ehehe~"
        if mas_isF14():

            $ mas_f14CapGainAff(5)
            m 1ekbsa "Me dar chocolates no Dia dos Namorados..."
            m 1ekbfa "Você realmente sabe como fazer uma garota se sentir especial, [player]."
            if renpy.seen_label('monika_date'):
                m 1lkbfa "Eu sei que comentei sobre visitarmos uma loja de chocolates juntos algum dia..."
                m 1hkbfa "Mas, mesmo que ainda não possamos fazer isso, ganhar esses chocolates de presente de você..."
            m 3ekbfa "Significa muito pra mim."

        elif renpy.seen_label('monika_date') and not mas_isO31():
            m 3rka "Eu sei que comentei sobre visitarmos uma loja de chocolates juntos algum dia..."
            m 3hub "Mas mesmo que ainda não possamos fazer isso, ganhar chocolates de presente de você já significa o mundo pra mim."
            m 1ekc "Eu queria tanto poder dividir com você..."
            m 3rksdlb "Mas até esse dia chegar, vou ter que aproveitar por nós dois, ahaha!"
            m 3hua "Obrigada, [mas_get_player_nickname()]~"
        else:

            m 3hub "Eu adoro chocolates!"
            m 1eka "E receber alguns de você significa muito pra mim."
            m 1hub "Obrigada, [player]!"
    else:

        $ times_chocs_given = mas_getGiftStatsForDate("mas_reaction_gift_chocolates")
        if times_chocs_given == 0:


            if not MASConsumable._getCurrentFood():

                if not (mas_isF14() or mas_isD25Season()):
                    if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
                        $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
                else:

                    $ monika_chr.remove_acs(store.mas_acs_quetzalplushie)

                if not mas_isO31():
                    $ monika_chr.wear_acs(mas_acs_heartchoc)

            $ mas_giftCapGainAff(3 if mas_isSpecialDay() else 1)

            m 1wuo "Ah!"

            if mas_isF14():

                $ mas_f14CapGainAff(5)
                m 1eka "[player]!"
                m 1ekbsa "Você é um doce, me dando chocolates em um dia como esse..."
                m 1ekbfa "Você realmente sabe como me fazer sentir especial."
                m "Obrigada, [player]."
            else:
                m 1hua "Obrigada pelos chocolates, [player]!"
                m 1ekbsa "Cada mordida me lembra o quão doce você é, ehehe~"

        elif times_chocs_given == 1:

            if not MASConsumable._getCurrentFood() and not mas_isO31():
                $ monika_chr.wear_acs(mas_acs_heartchoc)

            m 1eka "Mais chocolates, [player]?"
            m 3tku "Você gosta mesmo de me mimar,{w=0.2} {nw}"
            extend 3tub "ahaha!"
            m 1rksdla "Eu ainda não terminei a primeira caixa que você me deu..."
            m 1hub "...mas não estou reclamando!"

        elif times_chocs_given == 2:
            m 1ekd "[player]..."
            m 3eka "Acho que você já me deu chocolates demais por hoje."
            m 1rksdlb "Três caixas é muito, e eu ainda nem terminei a primeira!"
            m 1eka "Guarde elas para outro dia, tudo bem?"
        else:

            m 2tfd "[player]!"
            m 2tkc "Eu te disse que já tive chocolates o bastante por hoje, mas você continua tentando me dar mais..."
            m 2eksdla "Por favor... {w=1}os guarde para outro dia."


    if monika_chr.is_wearing_acs(mas_acs_heartchoc):
        call mas_remove_choc


    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)

    $ mas_receivedGift("mas_reaction_gift_chocolates")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    return

label mas_remove_choc:

    m 1hua "... "
    m 3eub "Esses chocolates estão {i}tããão{/i} bons!"
    m 1hua "... "
    m 3hksdlb "Ahaha! É melhor eu guardar isso por agora..."
    m 1rksdla "Se eu deixar aqui por mais tempo, não vai sobrar nenhum pra mais tarde!"

    call mas_transition_to_emptydesk

    python:
        renpy.pause(1, hard=True)
        monika_chr.remove_acs(mas_acs_heartchoc)
        renpy.pause(3, hard=True)

    call mas_transition_from_emptydesk ("monika 1eua")


    if monika_chr.is_wearing_acs(mas_acs_center_quetzalplushie):
        $ monika_chr.wear_acs(mas_acs_quetzalplushie)

    m 1eua "Então, o que mais você gostaria de fazer hoje?"
    return

label mas_reaction_gift_clothes_orcaramelo_bikini_shell:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_bikini_shell")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sua "Oh! {w=0.5}Um biquíni de conchinhas!"
    m 1hub "Obrigada, [mas_get_player_nickname()]!{w=0.5} Vou experimentar agora mesmo!"


    call mas_clothes_change (sprite_object)

    m 2ekbfa "Bem...{w=0.5} O que você achou?"
    m 2hubfa "Eu pareço uma sereia? Ehehe."
    show monika 5ekbfa zorder MAS_MONIKA_Z at i11 with dissolve_monika
    m 5ekbfa "Achei muito fofo, [player]..."
    m 5hubfa "A gente precisa ir à praia algum dia!"

    if mas_isWinter() or mas_isMoniNormal(lower=True):
        if mas_isWinter():
            show monika 2rksdla zorder MAS_MONIKA_Z at i11 with dissolve_monika
            m 2rksdla "...Mas por agora, tá meio friozinho aqui..."
            m 2eka "Então vou colocar algo mais quentinho..."

        elif mas_isMoniNormal(lower=True):
            show monika 2hksdlb zorder MAS_MONIKA_Z at i11 with dissolve_monika
            m 2hksdlb "Ahaha..."
            m 2rksdla "É um pouco constrangedor ficar assim na sua frente."
            m 2eka "Espero que não se importe, mas vou me trocar..."


        $ clothes = mas_clothes_def
        if persistent._mas_d25_in_d25_mode and mas_isD25Outfit():
            $ clothes = mas_clothes_santa
        call mas_clothes_change (clothes)

        m 2eua "Ah, agora sim..."
        m 3hua "Obrigada de novo pelo presente maravilhoso~"


    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_acs_orcaramelo_hairflower_pink:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_ACS, "orcaramelo_hairflower_pink")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(1)

    m 3sua "Oh!{w=0.5} Que florzinha mais fofa!"
    m 1ekbsa "Obrigada, [player], você é um doce~"
    m 1dua "Espera só um instante.{w=0.5}.{w=0.5}.{nw}"
    $ monika_chr.wear_acs(sprite_object)
    m 1hua "Ehehe~"
    m 1hub "Obrigada de novo, [player]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_velius94_shirt_pink:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "velius94_shirt_pink")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1suo "Ai meu Deus!"
    m 1suo "É {i}tão{/i} linda!"
    m 3hub "Muito obrigada, [player]!"
    m 3eua "Espera só um pouquinho, vou experimentar rapidinho..."


    call mas_clothes_change (sprite_object)

    m 2sub "Ahh, serviu perfeitamente!"
    m 3hub "Eu também adorei as cores! Rosa e preto combinam tão bem juntos."
    m 3eub "Sem falar que a saia ficou uma gracinha com esses babadinhos!"
    m 2tfbsd "Mas por algum motivo, tenho a impressão de que seus olhos estão meio que se desviando... {w=0.5}aham... {w=0.5}{i}para outro lugar{/i}."

    if mas_selspr.get_sel_clothes(mas_clothes_sundress_white).unlocked:
        m 2lfbsp "Eu já disse que não é educado ficar encarando, [player]."
    else:
        m 2lfbsp "Você sabe que não é educado ficar encarando, né?"

    m 2hubsb "Ahaha!"
    m 2tkbsu "Calma, calma... {w=0.5}só estou brincando com você~"
    m 3hub "Mais uma vez, muito obrigada por essa roupa, [player]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_orcaramelo_sakuya_izayoi:

    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_sakuya_izayoi")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "Ah! {w=0.5}Isso é..."
    m 2euc "Uma fantasia de empregada?"
    m 3tuu "Ehehe~"
    m 3tubsb "Sabe, se você gosta desse tipo de coisa, podia ter me falado antes..."
    m 1hub "Ahaha! Só estou brincando~"
    m 1eub "Deixe-me vestir!"


    call mas_clothes_change (sprite_object, outfit_mode=True)

    m 2hua "Então,{w=0.5} como fiquei?"
    m 3eub "Quase sinto que poderia fazer qualquer coisa antes que você sequer piscasse."
    m 1eua "...Desde que você não me mantenha ocupada, ehehe~"
    m 1lkbfb "Eu ainda quero poder passar um tempo com você, mestr--{nw}"
    $ _history_list.pop()
    m 1ekbfb "Eu ainda quero poder passar um tempo com você,{fast} [player]."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_finale_jacket_brown:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "finale_jacket_brown")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "Ah!{w=0.5} Uma jaqueta de inverno!"
    m 1suo "E vem até mesmo com um cachecol!"
    if mas_isSummer():
        m 3rksdla "...Embora eu esteja ficando com um pouco de calor só de olhar olhar pra ela, ahaha..."
        m 3eksdla "Talvez o verão não seja a melhor época para vestir isso, [player]."
        m 3eka "Mas eu agradeço a consideração, e ficarei feliz de vestir ela daqui a alguns meses."
    else:

        if mas_isWinter():
            m 1tuu "Eu não vou sentir frio tão cedo graça a você, [player]~"
        m 3eub "Deixe-me colocar! Eu já volto."


        call mas_clothes_change (sprite_object)

        m 2dku "Ahh, é tão confortável~"
        m 1eua "Adorei como ficou em mim, não achou também?"
        if mas_isMoniNormal(higher=True):
            m 3tku "Bem... não posso confiar em você para ser objetivo sobre isso, não é?"
            m 1hubfb "Ahaha!"
        m 1ekbfa "Obrigada, [player]. Eu adorei."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_orcaramelo_sweater_shoulderless:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_sweater_shoulderless")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "Oh!{w=0.5} Um suéter!"
    m 1hub "E parece tão aconchegante também!"
    if mas_isWinter():
        m 2eka "Você é tão [atncs], [player], me dar isso num dia frio de inverno..."
    m 3eua "Deixa eu experimentar rapidinho."


    call mas_clothes_change (sprite_object)

    m 2dkbsu "É tão... {w=1}confortável. Me sinto como um insetinho enrolado num cobertor. Ehehe~"
    m 1ekbsa "Obrigada, [player]. Eu adorei!"
    m 3hubsb "Agora toda vez que eu usar isso, vou pensar no seu calor. Ahaha~"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_velius94_dress_whitenavyblue:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "velius94_dress_whitenavyblue")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1suo "Ai meu Deus!"
    m 1sub "Esse vestido está deslumbrante, [player]!"
    m 3hub "Vou experimentar agora mesmo!"


    call mas_clothes_change (sprite_object, outfit_mode=True)

    m "Então,{w=0.5} o que achou?"
    m 3eua "Acho que esse tom de azul combina super bem com o branco."
    $ scrunchie = monika_chr.get_acs_of_type('bunny-scrunchie')

    if scrunchie and scrunchie.name == "velius94_bunnyscrunchie_blue":
        m 3eub "E o scrunchie de coelhinho combina perfeitamente com a roupa!"
    m 1eka "Muito obrigada mesmo, [player]."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_mocca_bun_blackandwhitestripedpullover:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "mocca_bun_blackandwhitestripedpullover")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "Ah, uma camisa nova!"
    m 3hub "Tá linda demais, [player]!"
    m 3eua "Espera só um segundo, vou vestir rapidinho.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    call mas_clothes_change (sprite_object)

    m 2eua "E então, o que achou?"
    m 7hua "Acho que ficou bem fofinha em mim.{w=0.2} {nw}"
    extend 3rubsa "Com certeza vou guardar esse look pra um encontro~"
    m 1hub "Obrigada de novo, [player]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

init python:

    if not mas_seenEvent("mas_reaction_gift_noudeck"):
        addReaction("mas_reaction_gift_noudeck", "noudeck", is_good=True)

label mas_reaction_gift_noudeck:
    python:
        mas_giftCapGainAff(0.5)

        mas_unlockGame("nou")
        mas_unlockEVL("monika_explain_nou_rules", "EVE")

    if mas_isMoniNormal(higher=True):
        m 1wub "Ah!{w=0.3} Um baralho de cartas!"
        m 3eua "E acho que sei como jogar esse jogo!"
        m 1esc "Ouvi dizer que ele pode {i}afetar{/i} o relacionamento com as pessoas com quem você está jogando."

        if mas_isMoniAff(higher=True):
            show monika 5eubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eubsa "Mas eu sei que o nosso relacionamento aguenta muito mais do que um simples jogo de cartas~"
            m 5hubsa "Ehehe~"
            show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        else:

            m 1hub "Ahaha!"
            m 1eua "Só estou brincando, [player]."

        m 1eua "Você já jogou 'NOU' alguma vez, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Você já jogou 'NOU' alguma vez, [player]?{fast}"
            "Sim.":


                m 1rksdlb "Ahaha..."
                m 1eksdla "Claro que já, afinal foi você quem me deu o baralho."
                call mas_reaction_gift_noudeck_have_played
            "Não.":

                m 3tuu "E que tal 'UNO' então, ehehe?{nw}"
                $ _history_list.pop()
                menu:
                    m "E que tal 'UNO' então, ehehe?{fast}"
                    "Sim.":

                        m 3hub "Ótimo! {w=0.3}{nw}"
                        extend 3tub "'NOU' é {i}bem{/i} parecido, ahaha..."
                        call mas_reaction_gift_noudeck_have_played
                    "Não.":

                        call mas_reaction_gift_noudeck_havent_played

        m 3hub "Mal posso esperar pra jogar com você!"

    elif mas_isMoniDis(higher=True):
        m 2euc "Um baralho?"
        m 2rka "Na verdade, talvez seja...{nw}"
        $ _history_list.pop()
        m 2rkc "Deixa pra lá..."
        m 2esc "Não estou com humor para jogar agora, [player]."
    else:

        m 6ckc "..."

    python:
        mas_receivedGift("mas_reaction_gift_noudeck")
        gift_ev = mas_getEV("mas_reaction_gift_noudeck")
        if gift_ev:
            store.mas_filereacts.delete_file(gift_ev.category)

    return

label mas_reaction_gift_noudeck_havent_played:
    m 1eka "Ah, tudo bem."
    m 4eub "É um jogo de cartas bem popular em que você precisa jogar todas as suas cartas antes dos oponentes pra vencer."
    m 1rssdlb "Pode parecer meio óbvio, ahaha~"
    m 3eub "Mas é um jogo muito divertido de jogar com amigos e com quem a gente ama~"
    m 1eua "Depois eu te explico as regras básicas, é só me pedir."
    return

label mas_reaction_gift_noudeck_have_played:
    m 1eua "Você provavelmente já sabe que algumas pessoas jogam com regras da casa."
    m 3eub "E se você quiser, a gente pode criar as nossas também."
    m 3eua "Ou, se não lembrar das regras, posso sempre te lembrar, é só pedir."
    python:
        mas_unlockEVL("monika_change_nou_house_rules", "EVE")
        persistent._seen_ever["monika_introduce_nou_house_rules"] = True
        persistent._seen_ever["monika_explain_nou_rules"] = True
    return
