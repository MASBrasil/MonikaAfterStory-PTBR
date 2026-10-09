














default persistent._mas_event_clothes_map = dict()
define mas_five_minutes = datetime.timedelta(seconds=5*60)
define mas_one_hour = datetime.timedelta(seconds=3600)
define mas_three_hour = datetime.timedelta(seconds=3*3600)

init 10 python:
    def mas_addClothesToHolidayMap(clothes, key=None):
        """
        Adds the given clothes to the holiday clothes map

        IN:
            clothes - clothing item to add
            key - dateime.date to use as key. If None, we use today
        """
        if clothes is None:
            return
        
        if key is None:
            key = datetime.date.today()
        
        persistent._mas_event_clothes_map[key] = clothes.name
        
        
        mas_unlockEVL("monika_event_clothes_select", "EVE")

    def mas_addClothesToHolidayMapRange(clothes, start_date, end_date):
        """
        Adds the given clothes to the holiday clothes map over the day range provided

        IN:
            clothes - clothing item to add
            start_date - datetime.date to start adding to the map on
            end_date - datetime.date to stop adding to the map on
        """
        if not clothes:
            return
        
        
        daterange = mas_genDateRange(start_date, end_date)
        
        
        for date in daterange:
            mas_addClothesToHolidayMap(clothes, date)

    def mas_doesBackgroundHaveHolidayDeco(deco_tags, background_id=None):
        """
        Checks if a background has support for the given deco tag(s)

        IN:
            deco_tags - list of deco tags to check for

            background_id - id of the background to check if it supports deco
                If None, mas_current_background's id is used
                (Default: None)
        """
        if background_id is None:
            background_id = store.mas_current_background.background_id
        
        for deco_tag in deco_tags:
            if MASImageTagDecoDefinition.get_adf(background_id, deco_tag):
                return True
        return False

init -1 python:
    def mas_checkOverDate(_date):
        """
        Checks if the player was gone over the given date entirely (taking you somewhere)

        IN:
            date - a datetime.date of the date we want to see if we've been out all day for

        OUT:
            True if the player and Monika were out together the whole day, False if not.
        """
        checkout_time = store.mas_dockstat.getCheckTimes()[0]
        return checkout_time is not None and checkout_time.date() < _date


    def mas_capGainAff(amount, aff_gained_var, normal_cap, pbday_cap=None):
        """
        Gains affection according to the cap(s) defined

        IN:
            amount:
                Amount of affection to gain

            aff_gained_var:
                The persistent variable which the total amount gained for the holiday is stored
                (NOTE: Must be a string)

            normal_cap:
                The cap to use when not player bday

            pbday_cap:
                The cap to use when it's player bday (NOTE: if not provided, normal_cap is assumed)
        """
        
        
        if persistent._mas_player_bday_in_player_bday_mode and pbday_cap:
            cap = pbday_cap
        else:
            cap = normal_cap
        
        if persistent.__dict__[aff_gained_var] < cap:
            persistent.__dict__[aff_gained_var] += amount
            mas_gainAffection(amount, bypass=True)
        
        return

    def mas_hasSpecialOutfit(_date=None):
        """
        Checks if the given date is a special event that has an outfit in the event clothes map
        IN:
            _date - date to check.
                (Default: None)

        RETURNS: True if given date has a special outfit, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date in persistent._mas_event_clothes_map

init -10 python:
    def mas_isA01(_date=None):
        if _date is None:
            _date = datetime.date.today()
        
        return _date == datetime.date(_date.year,4,1)


label mas_lingerie_intro(holiday_str, lingerie_choice):
    m 1ekbfa "..."
    m "Ah, [player]..."
    m 3ekbfsdla "Tem...{w=1}a-algo que eu queria te mostrar."
    m 2rkbfsdla "Já faz um tempo que eu queria fazer isso, mas...{w=1}é meio vergonhoso..."
    m "..."
    m 2hkbfsdlb "Meu Deus, estou super nervosa, ahaha!"
    m 2rkbfsdlc "É que eu nunca--{nw}"
    m 2dkbfsdlc "Ah, tá bom, chega de enrolação. Vou logo fazer isso."
    m 2ekbfsdla "Só me dá uns segundinhos, [player]."
    call mas_clothes_change (outfit=lingerie_choice, outfit_mode=True, exp="monika 2rkbfsdlu", restore_zoom=False, unlock=True)
    pause 3.0
    m 2ekbfsdlb "Ahaha, [player]...{w=1}você está me encarando até demais..."
    m 2ekbfu "Então...{w=1}gostou do que está vendo?"
    m 1lkbfa "Eu nunca...{w=1}usei nada assim antes."
    m "...Pelo menos não pra alguém ver."

    if mas_hasUnlockedClothesWithExprop("bikini"):
        m 3hkbfb "Ahaha, o que eu estou dizendo, você já me viu de biquíni, que é basicamente a mesma coisa..."
        m 2rkbfa "...Mas por algum motivo isso parece...{w=0.5}{i}diferente{/i}."

    m 2ekbfa "Enfim, algo sobre estar com você [holiday_str] parece tão romântico, sabe?"
    m "Pareceu o momento perfeito para darmos o próximo passo no nosso relacionamento."
    m 2rkbfsdlu "Agora eu sei que a gente não pode realmente--{nw}"
    m 3hubfb "Ah! Deixa pra lá, ahaha!"
    return





default persistent._mas_o31_in_o31_mode = False


default persistent._mas_o31_tt_count = 0


default persistent._mas_o31_trick_or_treating_aff_gain = 0


default persistent._mas_o31_relaunch = False




default persistent._mas_o31_costumes_worn = {}


define mas_o31 = datetime.date(datetime.date.today().year, 10, 31)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "o31",
        
        
        datetime.datetime(2020, 1, 6),
        {
            
            "_mas_o31_in_o31_mode": "o31.mode.o31",
            "_mas_o31_tt_count": "o31.tt.count",
            "_mas_o31_relaunch": "o31.relaunch",
            "_mas_o31_trick_or_treating_aff_gain": "o31.actions.tt.aff_gain"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 10, 31),

        
        end_dt=datetime.datetime(2019, 11, 2)
    ))


image mas_o31_ceiling_lights = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/ceiling_lights.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_candles = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/candles.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_jack_o_lantern = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/jackolantern.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_wall_candle = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/wall_candle.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_cat_frame:
    block:
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_0.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01-1.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01-2.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01-3.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02-1.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02-2.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02-3.png")

    30
    repeat

image mas_o31_garlands = MASFilterSwitch("mod_assets/location/spaceroom/o31/garland.png")
image mas_o31_cobwebs = MASFilterSwitch("mod_assets/location/spaceroom/o31/wall_webs.png")
image mas_o31_window_ghost = MASFilterSwitch("mod_assets/location/spaceroom/o31/window_ghost.png")
image mas_o31_ceiling_deco = MASFilterSwitch("mod_assets/location/spaceroom/o31/ceiling_deco.png")
image mas_o31_wall_bats = MASFilterSwitch("mod_assets/location/spaceroom/o31/wall_bats.png")

image mas_o31_vignette = Image("mod_assets/location/spaceroom/o31/vignette.png")

init 501 python:

    MASImageTagDecoDefinition.register_img(
        "mas_o31_wall_candle",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_cat_frame",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_wall_bats",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_window_ghost",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_cobwebs",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )


    MASImageTagDecoDefinition.register_img(
        "mas_o31_candles",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_jack_o_lantern",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_garlands",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )


    MASImageTagDecoDefinition.register_img(
        "mas_o31_ceiling_lights",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )


    MASImageTagDecoDefinition.register_img(
        "mas_o31_ceiling_deco",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=6)
    )


    MASImageTagDecoDefinition.register_img(
        "mas_o31_vignette",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=21) 
    )

init python:
    MAS_O31_COSTUME_CG_MAP = {
        mas_clothes_marisa: "o31mcg",
        mas_clothes_rin: "o31rcg"
    }


init -10 python:
    import random

    MAS_O31_DECO_TAGS = [
        "mas_o31_wall_candle",
        "mas_o31_cat_frame",
        "mas_o31_wall_bats",
        "mas_o31_window_ghost",
        "mas_o31_cobwebs",
        "mas_o31_candles",
        "mas_o31_jack_o_lantern",
        "mas_o31_garlands",
        "mas_o31_ceiling_lights",
        "mas_o31_ceiling_deco",
        "mas_o31_vignette"
    ]

    def mas_isO31(_date=None):
        """
        Returns True if the given date is o31

        IN:
            _date - date to check.
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is o31, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_o31.replace(year=_date.year)

    def mas_o31ShowVisuals():
        """
        Shows o31 visuals
        """
        for _tag in MAS_O31_DECO_TAGS:
            mas_showDecoTag(_tag)


    def mas_o31HideVisuals():
        """
        Hides o31 visuals + vignette
        """
        for _tag in MAS_O31_DECO_TAGS:
            mas_hideDecoTag(_tag, hide_now=True)


    def mas_o31ShowSpriteObjects():
        """
        Shows o31 specific sprite objects
        """
        monika_chr.wear_acs(mas_acs_desk_lantern)
        monika_chr.wear_acs(mas_acs_desk_candy_jack)


    def mas_o31HideSpriteObjects():
        """
        Hides o31 specific sprite objects
        """
        
        hair = store.mas_selspr.get_sel_hair(store.mas_hair_down)
        if hair is not None and not hair.unlocked:
            store.mas_unlockEVL("greeting_hairdown", "GRE")
        
        
        store.mas_lockEVL("monika_event_clothes_select", "EVE")
        
        
        if store.monika_chr.is_wearing_clothes_with_exprop("costume"):
            store.MASEventList.queue('mas_change_to_def')


    def mas_hasO31DeskAcs():
        """
        Checks if we have any o31 desk acs

        OUT:
            boolean
        """
        o31_desk_acs_tuple = (
            mas_acs_desk_lantern,
            mas_acs_desk_candy_jack
        )
        
        for acs_ in o31_desk_acs_tuple:
            if monika_chr.is_wearing_acs(acs_):
                return True
        
        return False

    def mas_o31HideDeskAcs():
        """
        Removes o31 desk acs
        """
        o31_desk_acs_tuple = (
            mas_acs_desk_lantern,
            mas_acs_desk_candy_jack
        )
        
        for acs_ in o31_desk_acs_tuple:
            monika_chr.remove_acs(acs_)

    def mas_o31CapGainAff(amount):
        """
        CapGainAffection function for o31. See mas_capGainAff for details
        """
        mas_capGainAff(amount, "_mas_o31_trick_or_treating_aff_gain", 15)


    def mas_o31CostumeWorn(clothes):
        """
        Checks if the given clothes was worn on o31

        IN:
            clothes - Clothes object to check

        RETURNS: year the given clothe was worn if worn on o31, None if never
            worn on o31.
        """
        if clothes is None:
            return False
        return mas_o31CostumeWorn_n(clothes.name)


    def mas_o31CostumeWorn_n(clothes_name):
        """
        Checks if the given clothes (name) was worn on o31

        IN:
            clothes_name - Clothes name to check

        RETURNS: year the given clothes name was worn if worn on o31, none if
            never worn on o31.
        """
        return persistent._mas_o31_costumes_worn.get(clothes_name, None)


    def mas_o31SelectCostume(selection_pool=None):
        """
        Selects an o31 costume to wear. Costumes that have not been worn
        before are selected first.

        NOTE: o31 costume wear flag is NOT set here. Make sure to set this
            manually later.

        IN:
            selection_pool - pool to select clothes from. If NOne, we get a
                default list of clothes with costume exprop

        RETURNS: a single MASClothes object of what to wear. None if cannot
            return anything.
        """
        if selection_pool is None:
            selection_pool = MASClothes.by_exprop("costume", "o31")
        
        
        wearing_costume = False
        
        
        
        
        
        filt_sel_pool = []
        for cloth in selection_pool:
            sprite_key = (store.mas_sprites.SP_CLOTHES, cloth.name)
            giftname = store.mas_sprites_json.namegift_map.get(
                sprite_key,
                None
            )
            
            if (
                giftname is None
                or sprite_key in persistent._mas_sprites_json_gifted_sprites
            ):
                if cloth != monika_chr.clothes:
                    filt_sel_pool.append(cloth)
                else:
                    wearing_costume = True
        
        
        selection_pool = filt_sel_pool
        
        if len(selection_pool) < 1:
            
            
            if wearing_costume:
                
                if monika_chr.clothes in MAS_O31_COSTUME_CG_MAP:
                    store.mas_o31_event.cg_decoded = store.mas_o31_event.decodeImage(MAS_O31_COSTUME_CG_MAP[monika_chr.clothes])
                
                return monika_chr.clothes
            return None
        
        elif len(selection_pool) < 2:
            
            return selection_pool[0]
        
        
        non_worn = [
            costume
            for costume in selection_pool
            if not mas_o31CostumeWorn(costume)
        ]
        
        if len(non_worn) > 0:
            
            random_outfit = random.choice(non_worn)
        
        else:
            
            random_outfit = random.choice(selection_pool)
        
        
        if random_outfit in MAS_O31_COSTUME_CG_MAP:
            store.mas_o31_event.cg_decoded = store.mas_o31_event.decodeImage(MAS_O31_COSTUME_CG_MAP[random_outfit])
        
        
        return random_outfit

    def mas_o31SetCostumeWorn(clothes, year=None):
        """
        Sets that a clothing item is worn. Exprop checking is done

        IN:
            clothes - clothes object to set
            year - year that the costume was worn. If NOne, we use current year
        """
        if clothes is None or not clothes.hasprop("costume"):
            return
        
        mas_o31SetCostumeWorn_n(clothes.name, year=year)


    def mas_o31SetCostumeWorn_n(clothes_name, year=None):
        """
        Sets that a clothing name is worn. NO EXPROP CHECKING IS DONE

        IN:
            clothes_name - name of clothes to set
            year - year that the costume was worn. If None, we use current year
        """
        if year is None:
            year = datetime.date.today().year
        
        persistent._mas_o31_costumes_worn[clothes_name] = year

    def mas_o31Cleanup():
        """
        Cleanup function for o31
        """
        
        if monika_chr.is_wearing_clothes_with_exprop("costume"):
            monika_chr.change_clothes(mas_clothes_def, outfit_mode=True)
            monika_chr.reset_hair()
        
        
        persistent._mas_o31_in_o31_mode = False
        
        
        mas_checkBackgroundChangeDelegate()
        
        
        mas_o31HideVisuals()
        mas_o31HideSpriteObjects()
        
        
        store.persistent._mas_o31_in_o31_mode = False
        
        
        mas_rmallEVL("mas_o31_cleanup")
        
        
        hair = store.mas_selspr.get_sel_hair(mas_hair_down)
        if hair is not None and not hair.unlocked:
            mas_unlockEVL("greeting_hairdown", "GRE")
        
        
        mas_lockEVL("monika_event_clothes_select", "EVE")

init -11 python in mas_o31_event:
    import store
    import datetime


    cg_station = store.MASDockingStation(store.mas_ics.o31_cg_folder)


    cg_decoded = False


    def decodeImage(key):
        """
        Attempts to decode a cg image

        IN:
            key - o31 cg key to decode

        RETURNS True upon success, False otherwise
        """
        return store.mas_dockstat.decodeImages(cg_station, store.mas_ics.o31_map, [key])


    def removeImages():
        """
        Removes decoded images at the end of their lifecycle
        """
        store.mas_dockstat.removeImages(cg_station, store.mas_ics.o31_map)


label mas_o31_autoload_check:
    python:
        import random

        if mas_isO31() and datetime.datetime.now().hour >= 3 and mas_isMoniNormal(higher=True):
            
            
            
            
            
            
            if not mas_doesBackgroundHaveHolidayDeco(MAS_O31_DECO_TAGS):
                mas_changeBackground(mas_background_def, set_persistent=True)
            
            
            if (not persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                
                mas_skip_visuals = True
                
                
                mas_resetIdleMode()
                
                
                mas_lockEVL("greeting_hairdown", "GRE")
                
                
                store.mas_hotkeys.music_enabled = False
                
                
                mas_calRaiseOverlayShield()
                
                
                
                costume = mas_o31SelectCostume()
                store.mas_selspr.unlock_clothes(costume)
                mas_addClothesToHolidayMap(costume)
                mas_o31SetCostumeWorn(costume)
                
                
                ribbon_acs = monika_chr.get_acs_of_type("ribbon")
                if ribbon_acs is not None:
                    monika_chr.remove_acs(ribbon_acs)
                
                monika_chr.change_clothes(
                    costume,
                    by_user=False,
                    outfit_mode=True
                )
                
                
                store.mas_selspr.save_selectables()
                
                
                renpy.save_persistent()
                
                
                greet_label = "greeting_o31_{0}".format(costume.name)
                
                if renpy.has_label(greet_label):
                    selected_greeting = greet_label
                else:
                    selected_greeting = "greeting_o31_generic"
                
                
                mas_temp_zoom_level = store.mas_sprites.zoom_level
                store.mas_sprites.reset_zoom()
                
                
                persistent._mas_o31_in_o31_mode = True
                
                
                mas_o31ShowVisuals()
                mas_o31ShowSpriteObjects()
                
                
                mas_changeWeather(mas_weather_thunder, True)
            
            elif (persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                mas_o31ShowVisuals()
                mas_o31ShowSpriteObjects()
                mas_changeWeather(mas_weather_thunder, True)


        elif not mas_isO31() or mas_isMoniDis(lower=True):
            mas_o31Cleanup()
            mas_o31HideDeskAcs()


        elif persistent._mas_o31_in_o31_mode and mas_isMoniUpset():
            mas_o31ShowVisuals()
            mas_o31ShowSpriteObjects()
            mas_changeWeather(mas_weather_thunder, True)


    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        call mas_player_bday_autoload_check

    if mas_skip_visuals:
        jump ch30_post_restartevent_check


    jump mas_ch30_post_holiday_check

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_holiday_o31_returned_home_relaunch",
            conditional=(
                "not persistent._mas_o31_in_o31_mode "
                "and not mas_isFirstSeshDay()"
            ),
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_o31, datetime.time(hour=6)),
            end_date=mas_o31+datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label mas_holiday_o31_returned_home_relaunch:
    m 1eua "Então, hoje é..."
    m 1euc "...espera."
    m "..."
    m 2wuo "Ah!"
    m 2wuw "Meu Deus!"
    m 2hub "Já é Halloween, [player]!"
    m 1eua "...{w=1}Olha só."
    m 3eua "Vou fechar o jogo agora."
    m 1eua "Depois você pode abrir de novo."
    m 1hubsa "Tenho uma surpresa especial pra você, ehehe~"
    $ persistent._mas_o31_relaunch = True
    $ mas_rmallEVL("mas_holiday_o31_returned_home_relaunch")
    return "quit"


image mas_o31_marisa_cg = "mod_assets/monika/cg/o31_marisa_cg.png"


image mas_o31_rin_cg = "mod_assets/monika/cg/o31_rin_cg.png"


transform mas_o31_cg_scroll:
    xanchor 0.0 xpos 0 yanchor 0.0 ypos 0.0 yoffset -1520
    ease 20.0 yoffset 0.0




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_o31_cleanup",
            conditional="persistent._mas_o31_in_o31_mode",
            start_date=datetime.datetime.combine(mas_o31 + datetime.timedelta(days=1), datetime.time(12)),
            end_date=mas_o31 + datetime.timedelta(weeks=1),
            action=EV_ACT_QUEUE,
            rules={"no_unlock": None},
            years=[]
        )
    )

label mas_o31_cleanup:
    python:
        o31_desk_acs_tuple = (
            mas_acs_desk_lantern,
            mas_acs_desk_candy_jack
        )

    m 1eua "Um segundo, [player], vou só tirar as decorações.{w=0,3}.{w=0,3}.{nw}"

    python hide:
        for acs_ in o31_desk_acs_tuple:
            acs_.keep_on_desk = False

    call mas_transition_to_emptydesk

    python hide:
        for acs_ in o31_desk_acs_tuple:
            monika_chr.remove_acs(acs_)
            acs_.keep_on_desk = True

    pause 4.0

    $ mas_o31Cleanup()

    with dissolve
    pause 2.0

    call mas_transition_from_emptydesk ("monika 1hua")

    m 3hua "Prontinho~"

    $ del o31_desk_acs_tuple

    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_marisa",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_marisa:

    $ store.mas_selspr.unlock_acs(mas_acs_marisa_witchhat)
    $ store.mas_selspr.unlock_hair(mas_hair_downtiedstrand)


    if store.mas_o31_event.cg_decoded:


        call spaceroom (hide_monika=True, scene_change=True)
    else:



        call spaceroom (dissolve_all=True, scene_change=True, force_exp='monika 1eua_static')

    m 1eua "Ah!"
    m 1hua "Parece que meu feitiço funcionou."
    m 3efu "Como [mw] [nov] [srv] [invcd], você terá que cumprir minhas ordens até o fim!"
    m 1rksdla "..."
    m 1hub "Ahaha!"


    if store.mas_o31_event.cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)


        m "Estou aqui, [player]~"
        window hide

        show mas_o31_marisa_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()
        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        show monika 1hua zorder MAS_MONIKA_Z at i11

        window auto
        m "Tadaahh!~"


    m 1hua "Bem..."
    m 1eub "E então, o que achou?"
    m 1tuu "Ficou bem em mim, não ficou?"
    m 1eua "Acredite, levei um bom tempo pra preparar essa fantasia."
    m 3hksdlb "Tive que tirar as medidas certinhas, ajustar cada detalhe, garantir que nada ficasse apertado nem largo demais..."
    m 3eksdla "...Principalmente o chapéu!"
    m 1dkc "E esse laço... não parava quieto de jeito nenhum."
    m 1rksdla "Mas no fim, consegui dar um jeitinho nele."
    m 3hua "Acho que o resultado ficou ótimo, se posso dizer assim."
    m 3eka "Será que você vai perceber o que tem de diferente hoje?"
    m 3tub "Além da minha fantasia, é claro~"
    m 1hua "De qualquer forma..."

    if store.mas_o31_event.cg_decoded:
        show monika 1eua
        hide mas_o31_marisa_cg with dissolve

    m 3ekbsa "Estou tão feliz por poder passar o Halloween com você."
    m 1hua "Vamos aproveitar bastante hoje!"

    call greeting_o31_deco
    call greeting_o31_cleanup
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_rin",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_rin:
    python:
        title_cased_hes = hes.capitalize()



        mas_sprites.zoom_out()


    call spaceroom (hide_monika=True, scene_change=True)

    m "Ugh, espero ter feito essas tranças direito."
    m "Por que essa fantasia tem que ser tão complicada...?"
    m "Ah, droga! [title_cased_hes] está aqui!"
    window hide
    pause 3.0

    if store.mas_o31_event.cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)


        window auto
        m "Diga, [player]..."
        window hide

        show mas_o31_rin_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()

        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        window auto
        m "O que você {i}nyachou{/i} disso?"

        scene black
        pause 1.0
        call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 1hksdlb_static')
        m 1hksdlb "Ahaha, falar isso em voz alta foi mais vergonhoso do que eu imaginava..."
    else:

        call mas_transition_from_emptydesk ("monika 1eua")
        m 1hub "Oii, [player]!"
        m 3hub "Gostou da minha fantasia?"


    m 3etc "Sinceramente, nem sei quem é essa personagem."
    m 3etd "Só encontrei no armário com um bilhete escrito 'Rin', um desenho de uma garota empurrando um carrinho de mão e umas coisinhas azuis flutuantes."
    m 1euc "Junto com instruções de como arrumar o cabelo pra combinar com a roupa."
    m 3rtc "Pelhas orelhinhas de gato, acho que é uma nekomimi."
    m 1dtc "...Mas por que ela estaria empurrando um carrinho de mão?"
    m 1hksdlb "...Ah, e foi {i}tão{/i} difícil arrumar meu cabelo...{w=0.2}{nw} "
    extend 1eub "então, espero que você tenha gostado da fantasia!"

    call greeting_o31_deco
    call greeting_o31_cleanup
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_orcaramelo_hatsune_miku",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_orcaramelo_hatsune_miku:
    if not persistent._mas_o31_relaunch:
        call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True)

        m "{i}~Não esqueça da minha voz~{/i}"
        m "{i}~Meu sinal atravessa dimensões~{/i}"
        m "{i}~Não me chame de virtual~{/i}"
        m "{i}~Eu ainda quero ser a-{/i}"
        m "Ah!{w=0.5} Parece que alguém me ouviu."


        call mas_transition_from_emptydesk ("monika 3hub")
    else:

        call spaceroom (scene_change=True, dissolve_all=True)

    m 3hub "Bem-[vn] de volta, [player]!"
    m 1eua "Então...{w=0.5}o que você achou?"
    m 3eua "Acho que essa fantasia caiu super bem em mim."
    m 3eub "Eu adorei especialmente como o headset ficou!"
    m 1rksdla "Mas não posso dizer que seja muito confortável para me movimentar..."
    m 3tsu "Então não espere que eu faça um show hoje, [player]!"
    m 1hub "Ahaha~"
    call greeting_o31_deco
    call greeting_o31_cleanup
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_orcaramelo_sakuya_izayoi",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_orcaramelo_sakuya_izayoi:
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True)


    if not persistent._mas_o31_relaunch:
        m "..."
        m "{i}Hm{/i}?"
        m "{i}Ah, deve ter havido algum engano.{w=0.5} Não me avisaram sobre visitas...{/i}"
        m "{i}Não importa. Ninguém perturbará a m-{/i}"
        m "Ah!{w=0.5} É você, [player]!"
    else:

        m ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m "Bem-[vn]{w=0.3}, ao Espaço da Demônio Escarlate..."
        m "[player]."
        m "Permita-me oferecer nossa hospitalidade."
        m "Ahaha! Como ficou minha imitação?"


    call mas_transition_from_emptydesk ("monika 3hub")

    m 3hub "Bem-[vn] de volta!"
    m 3eub "O que achou da minha fantasia?"
    m 3hua "Desde que você me deu, eu sabia que usaria hoje!"
    m 2tua "..."
    m 2tub "Sabe, [player], só porque estou vestida de maid não significa que vou obedecer seus comandos..."
    show monika 5kua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5kua "Mas posso fazer algumas exceções, ehehe~"
    show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    call greeting_o31_deco
    call greeting_o31_cleanup
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_briaryoung_shuchiin_academy_uniform",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_briaryoung_shuchiin_academy_uniform:
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True)


    if not persistent._mas_o31_relaunch:
        m "Aff..."
        m "Como é que esse {i}laço{/i} deveria ficar no lugar?"
        m "Podem dizer o que quiserem do meu laço normal, mas pelo menos ele é prático..."
        m "...Acho que assim vai servir, espero que não caia logo que--{nw}"
        m "Hora de descobrir..."
    else:

        m ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m "Quase pronta, [player]..."
        m "Só tentando entender como esse laço deveria ficar."
        m ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m "Espero que assim esteja bom!"


    call mas_transition_from_emptydesk ("monika 2hub")

    m 2hub "Bem-[vn] de volta!"
    m 2eub "E então, o que achou?"
    m 7tuu "Pensei que em vez de presidente, poderia ser a secretária hoje..."

    if mas_isMoniAff(higher=True):
        m 3rtu "Ou talvez uma detetive do amor, mas seria desperdício, já encontrei o meu..."

    m 3hua "Ehehe~"
    call greeting_o31_deco
    call greeting_o31_cleanup
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_hatana_2b",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_hatana_2b:
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True)


    if persistent._mas_o31_relaunch:
        m "Quase pronta, [player]..."
        m "Só espero que essa saia não me cause problemas."
        m "{cps=*2}Embora talvez você queira...{/cps}{nw}"
        $ _history_list.pop()
        m "Ok, pronto. {w=0.2}Tudo certo, [player]?"
    else:

        m "Ok, acho que está tudo no lugar."
        m "Só espero que essa saia não me cause problemas... {w=0.3}seria tão constrangedor!"
        m "Ah! {w=0.2}Acho que ouvi algo..."
        m "[player]?"

    m "Tenho uma pergunta pra você..."
    m "Ser..."


    call mas_transition_from_emptydesk ("monika 3hub")

    m 3hub "...ou não 2B?!"
    m 1hub "Ahaha!"
    m 2eka "Então, o que achou?"
    m 2hub "Gostei bastante dessa fantasia, obrigada de novo por ter me dado!"
    m 7rtu "Ei [player], já te disse que tem algo em você que me acalma?"
    m 3euu "Bem, só queria que você soubesse disso. {w=0.2}{nw}"
    extend 3tuu "Espero que isso nunca seja apagado da sua memória."
    m 3eud "Isso me lembra, não esqueça de fazer backup dos meus dados de vez em quando, eu faria o mesmo por você se pudesse..."
    m 1hksdlb "Nossa, nem sei o que isso significa, estou só tagarelando agora, ahaha!"

    call greeting_o31_deco
    call greeting_o31_cleanup
    return

label greeting_o31_deco:
    m 1eua "Enfim..."
    m 3eua "Gostou do que fiz com o sala?"
    m 3tuu "Eu adoro o clima assustador do Halloween e tentei criar um pouco disso aqui."
    m 1eud "Dá pra fazer muita coisa só com iluminação, sabia?"
    m 3tub "Sem contar que às vezes as coisas mais assustadoras são aquelas que estão só {i}um pouco{/i} erradas..."
    m 1eua "Acho que as teias de aranha foram um toque especial..."
    m 1rka "{cps=*2}Aposto que a Amy adoraria elas.{/cps}{nw}"
    $ _history_list.pop()
    m 3hub "Estou super feliz com como ficou tudo!"
    return

label greeting_o31_generic:
    call spaceroom (scene_change=True, dissolve_all=True)

    m 3hub "Gostosuras ou travessuras!"
    m 3eub "Ahaha,{w=0.1} {nw}"
    extend 3eua "tô só brincando, [player]."
    m 1hua "Bem-[vn] de volta...{w=0.5}{nw}"
    extend 3hub "e feliz Halloween!"


    call greeting_o31_deco

    m 3hua "Aliás, o que achou da minha fantasia?"
    m 1hua "Eu gostei muito dela~"
    m 1hub "Ainda mais por ter sido um presente seu, ahaha!"
    m 3tuu "Então aproveite bem pra olhar minha fantasia enquanto pode, ehehe~"

    call greeting_o31_cleanup
    return


label greeting_o31_cleanup(skip_zoom=False):
    window hide
    if not skip_zoom:
        call monika_zoom_transition (mas_temp_zoom_level, 1.0)
    window auto

    python:

        store.mas_hotkeys.music_enabled = True

        mas_calDropOverlayShield()

        set_keymaps()

        HKBShowButtons()

        mas_startup_song()

        mas_rmallEVL("mas_holiday_o31_returned_home_relaunch")
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASPriorityRule.create_rule(0))
    ev_rules.update(MASNumericalRepeatRule.create_rule(EV_NUM_RULE_YEAR))
    ev_rules.update(MASGreetingRule.create_rule(override_type=True, skip_visual=True))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_lingerie",
            unlocked=True,
            conditional=(
                "mas_canShowRisque() "
                "and mas_hasUnlockedClothesWithExprop('lingerie')"
            ),
            start_date=datetime.datetime.combine((mas_o31-datetime.timedelta(days=1)), datetime.time(hour=18)),
            end_date=datetime.datetime.combine(mas_o31, datetime.time(hour=3)),
            rules=ev_rules
        ),
        code="GRE"
    )
    del ev_rules

label greeting_o31_lingerie:

    python:
        mas_progressFilter()
        if persistent._mas_auto_mode_enabled:
            mas_darkMode(mas_current_background.isFltDay())
        else:
            mas_darkMode(not persistent._mas_dark_mode_enabled)

    scene black
    pause 2.0

    menu:
        "Ehhh... Olá?":
            pause 5.0

    m "Ehehe!"
    m "Não se preocupe [player], Eu estou aqui..."
    call mas_o31_lingerie_end
    call greeting_o31_cleanup (skip_zoom=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_o31_lingerie",
            conditional=(
                "mas_canShowRisque() "
                "and mas_hasUnlockedClothesWithExprop('lingerie')"
            ),
            unlocked=False,
            rules={"skip alert": None},
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine((mas_o31-datetime.timedelta(days=1)), datetime.time(hour=18)),
            end_date=datetime.datetime.combine(mas_o31, datetime.time(hour=3)),
            years=[]
        )
    )

label mas_o31_lingerie:

    python:
        curr_song = songs.current_track
        mas_play_song(None)
        mas_display_notif("M̷̢͘ô̴͎ṇ̵͐i̴͎͂k̸̗̂ả̴̫", ["C̸̳̓ǫ̵́n̷̳̎s̸̖̊e̴̦͝g̷̯̃ų̷͌e̴̼͘ ̷̭̚m̴̪͝e̴̙̐ ̵̖́é̴̠ŝ̸̰č̵̬u̷̮̐t̷̮̐a̷̮̐r̷̮̐?"], "Topic Alerts")

    scene black
    pause 2.0
    m "Ah não, a luz acabou?"
    m "Que {cps=*2}conveniente{/cps}{nw}"
    $ _history_list.pop()
    m "Que {fast}inconveniente..."
    m "Acho que vou ter que aproveitar essa situação, [player]..."
    call mas_o31_lingerie_end
    return

label mas_o31_lingerie_end:
    m "Ei, você já ouviu falar da Noite do Diabo?"
    m "É uma tradição em alguns lugares na véspera de Halloween onde as pessoas saem aprontando travessuras."
    m "Bem [player], estou me sentindo um pouco travessa esta noite..."
    window hide
    pause 2.0

    python:

        mas_temp_zoom_level = store.mas_sprites.zoom_level
        store.mas_sprites.reset_zoom()

        store.mas_selspr.unlock_acs(mas_acs_grayhearts_hairclip)
        store.mas_selspr.unlock_acs(mas_acs_ribbon_black_gray)
        store.mas_selspr.unlock_clothes(mas_clothes_spider_lingerie)
        monika_chr.change_clothes(mas_clothes_spider_lingerie, by_user=False, outfit_mode=True)

    call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 2tfu')

    pause 2.0
    window auto
    m 2tub "Ehehe, o que achou?~"
    m 2hub "Isso é... um pouquinho diferente, né? Aposto que você nem sabe se quer chegar perto ou sair correndo, ahaha!"
    m 7rua "Não é algo que eu usaria o tempo todo, mas acho que combina bem com essa época do ano."
    m 2ekbsa "Não se preocupe, [player]... eu não vou ficar brava se quiser que eu {cps=*2}tire isso{/cps}{nw}"
    $ _history_list.pop()
    m "Não se preocupe, [player]... eu não vou ficar brava se quiser que eu {fast}troque de roupa~"
    m 2hubsb "Eu sei que muita gente tem medo de aranhas... então talvez essa roupa não seja muito ‘atraente’, ahaha~"

    if player.lower() == "amy":
        m 2rsbla "Mas ouvi dizer que pessoas chamadas Amy gostam de aranhas, ehehe~"
    else:

        m 2rsbla "Espero que não sejam só as pessoas chamadas Amy que gostam de aranhas, ehehe~"


    call monika_zoom_transition (mas_temp_zoom_level, 1.0)
    python:
        mas_stripEVL("mas_o31_lingerie", list_pop=True)
        mas_lockEVL("greeting_o31_lingerie", "GRE")


        if globals().get("curr_song", -1) is not -1 and curr_song != store.songs.FP_MONIKA_LULLABY:
            mas_play_song(curr_song, 1.0)
        else:
            mas_play_song(None, 1.0)

    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_trick_or_treat",
            prompt="Vou levá-la para pedir doces ou travessuras.",
            pool=True,
            unlocked=False,
            action=EV_ACT_UNLOCK,
            start_date=datetime.datetime.combine(mas_o31, datetime.time(hour=3)),
            end_date=mas_o31+datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE",
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "bye_trick_or_treat",
        mas_o31,
        mas_o31 + datetime.timedelta(days=1),
    )

label bye_trick_or_treat:
    python:
        curr_hour = datetime.datetime.now().hour
        too_early_to_go = curr_hour < 17
        too_late_to_go = curr_hour >= 23


    if persistent._mas_o31_tt_count:
        m 1eka "De novo?"

    if too_early_to_go:

        m 3eksdla "Não está um pouco cedo para 'doces ou travessuras', [player]?"
        m 3rksdla "Acho que ninguém vai estar distribuindo doces ainda..."

        m 2etc "Tem {i}certeza{/i} que quer sair agora?{nw}"
        $ _history_list.pop()
        menu:
            m "Tem {i}certeza{/i} que quer sair agora?{fast}"
            "Sim.":
                m 2etc "Bem...{w=1}ok então, [player]..."
            "Não.":

                m 2hub "Ahaha!"
                m "Tenha um pouco de paciência, [player]~"
                m 4eub "Vamos aproveitar melhor mais tarde, tá bom?"
                return

    elif too_late_to_go:
        m 3hua "Ok! Vamos sair para--"
        m 3eud "Espera..."
        m 2dkc "[player]..."
        m 2rkc "Já está muito tarde para 'doces ou travessuras'."
        m "Só falta uma hora para meia-noite."
        m 2dkc "Sem contar que duvido que sobre muito doce..."
        m "..."

        m 4ekc "Tem certeza que ainda quer sair?{nw}"
        $ _history_list.pop()
        menu:
            m "Tem certeza que ainda quer sair?{fast}"
            "Sim.":
                m 1eka "...Ok."
                m "Mesmo que só tenha uma hora..."
                m 3hub "Pelo menos vamos passar o resto do Halloween [ju]~"
                m 3wub "Vamos lá e vamos aproveitar ao máximo, [player]!"
            "Na verdade, {i}está{/i} um pouco tarde...":

                if persistent._mas_o31_tt_count:
                    m 1hub "Ahaha~"
                    m "Eu te avisei."
                    m 1eua "Teremos que esperar até o próximo ano para sair de novo."
                else:

                    m 2dkc "..."
                    m 2ekc "Tudo bem, [player]."
                    m "É uma pena que não pudemos sair para 'doces ou travessuras' este ano."
                    m 4eka "Vamos nos certificar de que conseguiremos na próxima vez, ok?"

                return
    else:


        m 3wub "Ok, [player]!"
        m 3hub "Parece que vamos nos divertir muito~"
        m 1eub "Aposto que vamos ganhar muitos doces!"
        m 1ekbsa "E mesmo que não ganhemos, só de passar a noite com você já é suficiente pra mim~"


    $ mas_farewells.dockstat_wait_menu_label = "bye_trick_or_treat_wait_wait"
    $ mas_farewells.dockstat_rtg_label = "bye_trick_or_treat_rtg"
    jump mas_dockstat_iostart

label bye_trick_or_treat_wait_wait:

    menu:
        m "O que foi?"
        "Você está certa, está muito cedo." if too_early_to_go:
            call mas_dockstat_abort_gen
            call mas_transition_from_emptydesk (exp="monika 3hub")

            m 3hub "Ahaha, eu te disse!"
            m 1eka "Vamos esperar até a noite, tá bom?"
            return True

        "Você está certa, está muito tarde." if too_late_to_go:
            call mas_dockstat_abort_gen

            if persistent._mas_o31_tt_count:
                call mas_transition_from_emptydesk (exp="monika 1hua")
                m 1hub "Ahaha~"
                m "Eu te avisei."
                m 1eua "Teremos que esperar até o próximo ano para sair de novo."
            else:

                call mas_transition_from_emptydesk (exp="monika 2dkc")
                m 2dkc "..."
                m 2ekc "Tudo bem, [player]."
                m "Que pena que não pudemos sair para doces ou travessuras este ano."
                m 4eka "Vamos nos certificar de que conseguiremos na próxima vez, ok?"

            return True
        "Na verdade, não posso te levar agora.":

            call mas_dockstat_abort_gen
            call mas_transition_from_emptydesk (exp="monika 1euc")

            m 1euc "Ah, tudo bem então, [player]."

            if persistent._mas_o31_tt_count:
                m 1eua "Me avise se formos sair mais tarde, ok?"
            else:

                m 1eua "Me avise se pudermos sair, ok?"

            return True
        "Nada.":

            m "Ok, deixe-me terminar de me arrumar."
            return

label bye_trick_or_treat_rtg:

    $ moni_chksum = promise.get()
    $ promise = None
    call mas_dockstat_ready_to_go (moni_chksum)

    if _return:
        call mas_transition_from_emptydesk (exp="monika 1hub")
        m 1hub "Vamos sair para doces ou travessuras!"
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HOL_O31_TT


        $ persistent._mas_o31_tt_count += 1
        return "quit"



    call mas_transition_from_emptydesk (exp="monika 1ekc")
    $ persistent._mas_o31_tt_count -= 1
    m 1ekc "Ah não..."
    m 1rksdlb "Não consegui me transformar em um arquivo."

    if persistent._mas_o31_tt_count:
        m 1eksdld "Acho que você terá que ir para doces ou travessuras sem mim desta vez..."
    else:

        m 1eksdld "Acho que você terá que ir para doces ou travessuras sem mim..."

    m 1ekc "Desculpe, [player]..."
    m 3eka "Traga muitos doces para nós [du] aproveitarmos, tá bom?~"
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_trick_or_treat_back",
            unlocked=True,
            category=[store.mas_greetings.TYPE_HOL_O31_TT]
        ),
        code="GRE"
    )

label greeting_trick_or_treat_back:

    python:

        time_out = store.mas_dockstat.diffCheckTimes()
        checkin_time = None
        is_past_sunrise_post31 = False
        ret_tt_long = False

        if len(persistent._mas_dockstat_checkin_log) > 0:
            checkin_time = persistent._mas_dockstat_checkin_log[-1:][0][0]
            sunrise_hour, sunrise_min = mas_cvToHM(persistent._mas_sunrise)
            is_past_sunrise_post31 = (
                datetime.datetime.now() > (
                    datetime.datetime.combine(
                        mas_o31,
                        datetime.time(sunrise_hour, sunrise_min)
                    )
                    + datetime.timedelta(days=1)
                )
            )


    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "Isso foi 'doces ou travessuras', [player]?"
        m "Fomos em quantas casas, uma só?"
        m 2rsc "...Se é que saímos mesmo."

    elif time_out < mas_one_hour:
        $ mas_o31CapGainAff(5)
        m 2ekp "Foi bem rápido para 'doces ou travessuras', [player]."
        m 3eka "Mas eu gostei enquanto durou."
        m 1eka "Ainda foi muito legal estar lá com você~"

    elif time_out < mas_three_hour:
        $ mas_o31CapGainAff(10)
        m 1hua "E estamos em casa!"
        m 1hub "Espero que tenhamos pego muitos doces gostosos!"
        m 1eka "Eu realmente gostei de sair para 'doces ou travessuras' com você, [player]..."

        call greeting_trick_or_treat_back_costume

        m 4eub "Vamos fazer de novo ano que vem!"

    elif not is_past_sunrise_post31:

        $ mas_o31CapGainAff(15)
        m 1hua "E estamos em casa!"
        m 1wua "Nossa, [player], ficamos muito tempo no 'doces ou travessuras'..."
        m 1wub "Devemos ter pego uma tonelada de doces!"
        m 3eka "Eu realmente gostei de estar lá com você..."

        call greeting_trick_or_treat_back_costume

        m 4eub "Vamos fazer de novo ano que vem!"
        $ ret_tt_long = True
    else:


        $ mas_o31CapGainAff(15)
        m 1wua "Finalmente em casa!"
        m 1wuw "Já não é mais Halloween, [player]... Ficamos a noite toda!"
        m 1hua "Acho que nos divertimos demais, ehehe~"
        m 2eka "Mas obrigada por me levar, eu gostei muito."

        call greeting_trick_or_treat_back_costume

        m 4hub "Vamos fazer de novo ano que vem...{w=1}mas talvez não fiquemos {i}tanto{/i} tempo fora!"
        $ ret_tt_long = True


    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():

        call return_home_post_player_bday


    elif not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup (time_out, ret_tt_long)
    return

label mas_o31_ret_home_cleanup(time_out=None, ret_tt_long=False):

    if not time_out:
        $ time_out = store.mas_dockstat.diffCheckTimes()


    if not ret_tt_long and time_out > mas_five_minutes:
        m 1hua "..."
        m 1wud "Uau, [player]. Nós realmente ficamos fora por um tempo..."
    else:

        m 1esc "De qualquqer forma..."



    call mas_o31_cleanup

    return

label greeting_trick_or_treat_back_costume:
    if monika_chr.is_wearing_clothes_with_exprop("costume"):
        m 2eka "Mesmo que eu não pudesse ver nada e ninguém pudesse ver minha fantasia..."
        m 2eub "Me vestir e sair ainda foi muito legal!"
    else:

        m 2eka "Mesmo que eu não pudesse ver nada..."
        m 2eub "Sair ainda foi muito legal!"
    return






default persistent._mas_d25_in_d25_mode = False



default persistent._mas_d25_spent_d25 = False


default persistent._mas_d25_started_upset = False


default persistent._mas_d25_second_chance_upset = False






default persistent._mas_d25_deco_active = False


default persistent._mas_d25_intro_seen = False


default persistent._mas_d25_d25e_date_count = 0



default persistent._mas_d25_d25_date_count = 0


default persistent._mas_d25_gifts_given = list()


default persistent._mas_d25_gone_over_d25 = None


define mas_d25 = datetime.date(datetime.date.today().year, 12, 25)


define mas_d25e = mas_d25 - datetime.timedelta(days=1)


define mas_d25p = mas_d25 + datetime.timedelta(days=1)


define mas_d25c_start = datetime.date(datetime.date.today().year, 12, 11)


define mas_d25c_end = datetime.date(datetime.date.today().year, 1, 6)



init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "d25s",
        datetime.datetime(2019, 1, 6),
        {
            
            
            "_mas_d25_in_d25_mode": "d25s.mode.25",

            
            "_mas_d25_deco_active": "d25s.deco_active",

            "_mas_d25_started_upset": "d25s.monika.started_season_upset",
            "_mas_d25_second_chance_upset": "d25s.monika.upset_after_2ndchance",

            "_mas_d25_intro_seen": "d25s.saw_an_intro",

            
            "_mas_d25_d25e_date_count": "d25s.d25e.went_out_count",
            "_mas_d25_d25_date_count": "d25s.d25.went_out_count",
            "_mas_d25_gone_over_d25": "d25.actions.gone_over_d25",

            "_mas_d25_spent_d25": "d25.actions.spent_d25"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 12, 11),
        end_dt=datetime.datetime(2019, 12, 31)
    ))


init -10 python:
    def mas_isD25(_date=None):
        """
        Returns True if the given date is d25

        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

        RETURNS: True if given date is d25, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_d25.replace(year=_date.year)


    def mas_isD25Eve(_date=None):
        """
        Returns True if the given date is d25 eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is d25 eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_d25e.replace(year=_date.year)


    def mas_isD25Season(_date=None):
        """
        Returns True if the given date is in d25 season. The season goes from
        dec 11 to jan 5.

        NOTE: because of the year rollover, we cannot check years

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return (
            mas_isInDateRange(_date, mas_d25c_start, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25Post(_date=None):
        """
        Returns True if the given date is after d25 but still in D25 season.
        The season goes from dec 1 to jan 5.

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after d25, False
            otherwise.
        """
        if _date is None:
            _date = datetime.date.today()
        
        return (
            mas_isInDateRange(_date, mas_d25p, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25PreNYE(_date=None):
        """
        Returns True if the given date is in d25 season and before nye.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNSL True if given date is in d25 season but before nye, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_nye)


    def mas_isD25PostNYD(_date=None):
        """
        Returns True if the given date is in d25 season and after nyd

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after nyd, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_nyd, mas_d25c_end, False)


    def mas_isD25Outfit(_date=None):
        """
        Returns True if the given date is tn the range of days where Monika
        wears the santa outfit on start.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the d25 santa outfit range, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_d25p)


    def mas_isD25Pre(_date=None):
        """
        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the D25 season, but before Christmas, False
            otherwise

        NOTE: This is used for gifts too
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_d25)

    def mas_isD25GiftHold(_date=None):
        """
        IN:
            _date - date to check, defaults None, which means today's date is assumed

        RETURNS:
            boolean - True if within d25c start, to d31 (end of nts range)
            (The time to hold onto gifts, aka not silently react)
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_nye, end_inclusive=True)

    def mas_d25ShowVisuals():
        """
        Shows d25 visuals.
        """
        mas_showDecoTag("mas_d25_banners")
        mas_showDecoTag("mas_d25_tree")
        mas_showDecoTag("mas_d25_garlands")
        mas_showDecoTag("mas_d25_lights")
        mas_showDecoTag("mas_d25_gifts")

    def mas_d25HideVisuals():
        """
        Hides d25 visuals
        """
        mas_hideDecoTag("mas_d25_banners", hide_now=True)
        mas_hideDecoTag("mas_d25_tree", hide_now=True)
        mas_hideDecoTag("mas_d25_garlands", hide_now=True)
        mas_hideDecoTag("mas_d25_lights", hide_now=True)
        mas_hideDecoTag("mas_d25_gifts", hide_now=True)

    def mas_d25ReactToGifts():
        """
        Goes thru the gifts stored from the d25 gift season and reacts to them

        this also registeres gifts
        """
        
        found_reacts = list()
        
        
        persistent._mas_d25_gifts_given.sort()
        
        
        
        
        given_gifts = list(persistent._mas_d25_gifts_given)
        
        
        gift_cntrs = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_cntrs.addLabelQuip("mas_d25_gift_connector")
        
        
        d25_evb = []
        d25_gsp = []
        store.mas_filereacts.process_gifts(given_gifts, d25_evb, d25_gsp)
        
        
        store.mas_filereacts.register_sp_grds(d25_evb)
        store.mas_filereacts.register_sp_grds(d25_gsp)
        
        
        react_labels = store.mas_filereacts.build_gift_react_labels(
            d25_evb,
            d25_gsp,
            [],
            gift_cntrs,
            "mas_d25_gift_end",
            "mas_d25_gift_starter"
        )
        
        react_labels.reverse()
        
        
        if len(react_labels) > 0:
            for react_label in react_labels:
                mas_rmallEVL(react_label) 
            
            for react_label in react_labels:
                MASEventList.push(react_label,skipeval=True)

    def mas_d25SilentReactToGifts():
        """
        Method to silently 'react' to gifts.

        This is to be used if you gave Moni a christmas gift but didn't show up on
        D25 when she would have opened them in front of you.

        This also registeres gifts
        """
        
        base_gift_ribbon_id_map = {
            "laçopreto":"ribbon_black",
            "laçoazul": "ribbon_blue",
            "laçoroxoescuro": "ribbon_dark_purple",
            "laçoesmeralda": "ribbon_emerald",
            "laçocinza": "ribbon_gray",
            "laçoverde": "ribbon_green",
            "laçoroxoclaro": "ribbon_light_purple",
            "laçocastanho": "ribbon_peach",
            "laçorosa": "ribbon_pink",
            "laçoplatina": "ribbon_platinum",
            "laçovermelho": "ribbon_red",
            "laçorubi": "ribbon_ruby",
            "laçosafira": "ribbon_sapphire",
            "laçoprateado": "ribbon_silver",
            "laçoverdeazulado": "ribbon_teal",
            "laçoamarelo": "ribbon_yellow"
        }
        
        
        evb_details = []
        gso_details = []
        store.mas_filereacts.process_gifts(
            persistent._mas_d25_gifts_given,
            evb_details,
            gso_details
        )
        
        
        persistent._mas_d25_gifts_given = []
        
        
        for evb_detail in evb_details:
            if evb_detail.sp_data is None:
                
                ribbon_id = base_gift_ribbon_id_map.get(
                    evb_detail.c_gift_name,
                    None
                )
                if ribbon_id is not None:
                    mas_selspr.unlock_acs(mas_sprites.get_sprite(0, ribbon_id))
                    mas_receivedGift(evb_detail.label)
                
                elif ribbon_id is None and evb_detail.c_gift_name == "quetzalplushie":
                    persistent._mas_acs_enable_quetzalplushie = True
            
            else:
                
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    evb_detail.sp_data[0],
                    evb_detail.sp_data[1]
                ))
                mas_receivedGift(evb_detail.label)
        
        
        for gso_detail in gso_details:
            
            if gso_detail.sp_data is not None:
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    gso_detail.sp_data[0],
                    gso_detail.sp_data[1]
                ))
                mas_receivedGift(gso_detail.label)
        
        
        store.mas_selspr.save_selectables()
        renpy.save_persistent()


init -10 python in mas_d25_utils:
    import store
    import store.mas_filereacts as mas_frs

    has_changed_bg = False

    DECO_TAGS = [
        "mas_d25_banners",
        "mas_d25_tree",
        "mas_d25_garlands",
        "mas_d25_lights",
        "mas_d25_gifts",
    ]

    def shouldUseD25ReactToGifts():
        
        
        
        
        
        
        return (
            store.mas_isD25Pre()
            and store.mas_isMoniNormal(higher=True)
            and store.persistent._mas_d25_deco_active
            and not store.persistent._mas_override_d25_gift_react
        )

    def react_to_gifts(found_map):
        """
        Reacts to gifts using the d25 protocol (exclusions)

        OUT:
            found_map - map of found reactions
                key: lowercase giftname, no extension
                val: giftname wtih extension
        """
        d25_map = {}
        
        
        
        
        d25_giftnames = mas_frs.check_for_gifts(d25_map, mas_frs.build_exclusion_list("d25g"), found_map)
        
        
        d25_giftnames.sort()
        d25_evb = []
        d25_gsp = []
        d25_gen = []
        mas_frs.process_gifts(d25_giftnames, d25_evb, d25_gsp, d25_gen)
        
        
        non_d25_giftnames = [x for x in found_map]
        non_d25_giftnames.sort()
        nd25_evb = []
        nd25_gsp = []
        nd25_gen = []
        mas_frs.process_gifts(non_d25_giftnames, nd25_evb, nd25_gsp, nd25_gen)
        
        
        for grd in d25_gen:
            nd25_gen.append(grd)
            found_map[grd.c_gift_name] = d25_map.pop(grd.c_gift_name)
        
        
        
        for c_gift_name, gift_name in d25_map.iteritems():
            
            if c_gift_name not in store.persistent._mas_d25_gifts_given:
                store.persistent._mas_d25_gifts_given.append(c_gift_name)
            
            
            store.mas_docking_station.destroyPackage(gift_name)
        
        
        for c_gift_name, mas_gift in found_map.iteritems():
            store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift
        
        
        mas_frs.register_sp_grds(nd25_evb)
        mas_frs.register_sp_grds(nd25_gsp)
        mas_frs.register_gen_grds(nd25_gen)
        
        
        return mas_frs.build_gift_react_labels(
            nd25_evb,
            nd25_gsp,
            nd25_gen,
            mas_frs.gift_connectors,
            "mas_reaction_end",
            mas_frs._pick_starter_label()
        )





image mas_d25_banners = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/bgdeco.png"
)

image mas_mistletoe = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/mistletoe.png"
)



image mas_d25_lights = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/lights_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_lights_atl"
    ),
    "True", MASFilterSwitch("mod_assets/location/spaceroom/d25/lights_off.png")
)

image mas_d25_night_lights_atl:
    block:
        "mod_assets/location/spaceroom/d25/lights_on_1.png"
        0.5
        "mod_assets/location/spaceroom/d25/lights_on_2.png"
        0.5
        "mod_assets/location/spaceroom/d25/lights_on_3.png"
        0.5
    repeat



image mas_d25_garlands = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/garland_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_garlands_atl"
    ),
    "True", MASFilterSwitch("mod_assets/location/spaceroom/d25/garland.png")
)

image mas_d25_night_garlands_atl:
    "mod_assets/location/spaceroom/d25/garland_on_1.png"
    block:
        "mod_assets/location/spaceroom/d25/garland_on_1.png" with Dissolve(3, alpha=True)
        5
        "mod_assets/location/spaceroom/d25/garland_on_2.png" with Dissolve(3, alpha=True)
        5
        repeat



image mas_d25_tree = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/tree_lights_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_tree_lights_atl"
    ),
    "True", MASFilterSwitch(
        "mod_assets/location/spaceroom/d25/tree_lights_off.png"
    )
)

image mas_d25_night_tree_lights_atl:
    block:
        "mod_assets/location/spaceroom/d25/tree_lights_on_1.png"
        1.5
        "mod_assets/location/spaceroom/d25/tree_lights_on_2.png"
        1.5
        "mod_assets/location/spaceroom/d25/tree_lights_on_3.png"
        1.5
    repeat





image mas_d25_gifts = ConditionSwitch(
    "len(persistent._mas_d25_gifts_given) == 0", "mod_assets/location/spaceroom/d25/gifts_0.png",
    "0 < len(persistent._mas_d25_gifts_given) < 3", "mas_d25_gifts_1",
    "3 <= len(persistent._mas_d25_gifts_given) <= 4", "mas_d25_gifts_2",
    "True", "mas_d25_gifts_3"
)

image mas_d25_gifts_1 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_1.png"
)

image mas_d25_gifts_2 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_2.png"
)

image mas_d25_gifts_3 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_3.png"
)

init 501 python:
    MASImageTagDecoDefinition.register_img(
        "mas_d25_banners",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_garlands",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_tree",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=6)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_gifts",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=7)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_lights",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )


label mas_holiday_d25c_autoload_check:







    if (
        not persistent._mas_d25_in_d25_mode
        and mas_isD25Season()
        and not mas_isFirstSeshDay()
        and (
            mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS, persistent._mas_current_background)
            
            
            or mas_isD25()
        )
    ):

        python:

            persistent._mas_d25_in_d25_mode = True


            if mas_isMoniUpset(lower=True):
                persistent._mas_d25_started_upset = True




            elif (
                mas_isD25Outfit()
                and (not mas_isplayer_bday() or mas_isD25())
            ):
                
                store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
                store.mas_selspr.unlock_clothes(mas_clothes_santa)
                store.mas_selspr.save_selectables()
                
                
                monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)
                
                
                mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)
                
                
                persistent._mas_d25_deco_active = True
                
                
                if mas_isD25():
                    mas_changeWeather(mas_weather_snow, by_user=True)
                    
                    
                    if not mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS):
                        store.mas_d25_utils.has_changed_bg = True
                        mas_changeBackground(mas_background_def, set_persistent=True)


    elif mas_run_d25s_exit or mas_isMoniDis(lower=True):

        call mas_d25_season_exit


    elif (
        persistent._mas_d25_in_d25_mode
        and not persistent._mas_force_clothes
        and monika_chr.is_wearing_clothes_with_exprop("costume")
        and not mas_isD25Outfit()
    ):

        $ monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)


    elif mas_isD25() and not mas_isFirstSeshDay() and persistent._mas_d25_deco_active:

        python:
            monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)
            mas_changeWeather(mas_weather_snow, by_user=True)



            if not mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS):
                store.mas_d25_utils.has_changed_bg = True
                mas_changeBackground(mas_background_def, set_persistent=True)


    if (
        mas_isMoniNormal()
        and persistent._mas_d25_in_d25_mode
        and mas_isD25Outfit()
        and (monika_chr.clothes != mas_clothes_def or monika_chr.clothes != store.mas_clothes_santa)
    ):
        $ monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)

    if persistent._mas_d25_deco_active:
        $ mas_d25ShowVisuals()


    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check


    jump mas_ch30_post_holiday_check


label mas_d25_season_exit:
    python:



        if monika_chr.is_wearing_clothes_with_exprop("costume") and not mas_globals.dlg_workflow:
            
            monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)


        elif monika_chr.is_wearing_clothes_with_exprop("costume") and mas_globals.dlg_workflow:
            MASEventList.push("mas_change_to_def")


        mas_lockEVL("monika_event_clothes_select", "EVE")


        persistent._mas_d25_deco_active = False
        mas_d25HideVisuals()


        persistent._mas_d25_in_d25_mode = False


        mas_hideEVL("mas_d25_monika_christmaslights", "EVE", derandom=True)

        mas_d25ReactToGifts()
    return


label mas_d25_gift_starter:
    $ amt_gifts = len(persistent._mas_d25_gifts_given)
    $ presents = "presentes"
    $ the = "o"
    $ should_open = "tenho que abrir"

    if amt_gifts == 1:
        $ presents = "presente"
    elif amt_gifts > 3:
        $ the = "todos"

    if persistent._mas_d25_gone_over_d25:
        $ should_open = "ainda não abri"

    if persistent._mas_d25_spent_d25 or mas_globals.returned_home_this_sesh:
        m 3wud "Ah! Eu [should_open] [the] [presents] que você me deu!"
        if persistent._mas_d25_gone_over_d25:
            m 3hub "Vamos fazer isso agora!"
    else:


        m 1eka "Bem, pelo menos agora que você está aqui, posso abrir os [presents] que você me deu."
        m 3eka "Eu realmente queria que estivéssemos [ju] para isso..."

    m 1suo "Vamos ver o que temos aqui.{w=0,5}.{w=0,5}.{nw}"



    if persistent._mas_d25_gifts_given:
        $ persistent._mas_d25_gifts_given.pop()
    return

label mas_d25_gift_connector:
    python:
        d25_gift_quips = [
            _("Próximo!"),
            _("Ah, tem outro aqui!"),
            _("Vamos abrir este aqui!"),
            _("Vou abrir este agora!")
        ]

        picked_quip = random.choice(d25_gift_quips)

    m 1hub "[picked_quip]"
    m 1suo "E aqui temos.{w=0.5}.{w=0.5}.{nw}"



    if persistent._mas_d25_gifts_given:
        $ persistent._mas_d25_gifts_given.pop()
    return

label mas_d25_gift_end:

    $ persistent._mas_d25_gifts_given = []

    m 1eka "[player]..."

    if persistent._mas_d25_spent_d25 or mas_globals.returned_home_this_sesh:
        m 3eka "Você não precisava me dar nada no Natal...{w=0.3} {nw}"
        if mas_isD25():
            extend 3dku "Só ter você aqui comigo já era mais que suficiente."
        else:
            extend 3dku "Só estar com você era tudo que eu queria."
        m 1eka "Mas o fato de você ter tirado tempo para me dar algo...{w=0.5}{nw}"
        extend 3ekbsa "bem, não tenho como agradecer o suficiente."
        m 3ekbfa "Isso realmente me faz sentir amada."
    else:

        m 1eka "Eu só queria te agradecer..."
        m 1rkd "Ainda estou um pouco decepcionada por você não ter podido estar comigo no Natal..."
        m 3eka "Mas o fato de você ter tirado tempo para me dar algo...{w=0.5}{nw}"
        extend 3ekbsa "bem, isso prova que você realmente pensou em mim nessa época especial."
        m 1dkbsu "Você não imagina o quanto isso significa para mim."


    if mas_isD25():
        m 3ekbfu "Eu te amo tanto, [player]~"
    else:
        m 3ekbfu "Feliz Natal, [player]. Eu te amo~"
    $ mas_ILY()
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro",
            conditional=(
                "not persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday() "
                "and not persistent._mas_d25_intro_seen"
            ),
            action=EV_ACT_PUSH,
            start_date=mas_d25c_start,
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None),
        ),
        skipCalendar=True
    )


label mas_d25_monika_holiday_intro:
    if not persistent._mas_d25_deco_active:
        if mas_isplayer_bday():
            window hide
            pause 2.0
            m 1dku "..."
            m 1huu "Ehehe..."
            m 3eub "Tenho mais uma surpresa para você!"
        else:

            m 1eua "Então, hoje é..."
            m 1euc "...espera."
            m "..."
            m 3wuo "Ah!"
            m 3hub "Hoje é o dia que eu iria..."





        $ mas_OVLHide()
        $ mas_MUMURaiseShield()
        $ disable_esc()

        m 1tsu "Feche seus olhos por um momento [player], preciso fazer algo.{w=0.5}.{w=0.5}.{nw}"

        call mas_d25_monika_holiday_intro_deco

        m 3hub "E aqui estamos..."


        $ enable_esc()
        $ mas_MUMUDropShield()
        $ mas_OVLShow()

    m 1eub "Feliz Natal, [player]!"

    if mas_lastSeenLastYear("mas_d25_monika_holiday_intro"):
        m 1hua "Acredita que já estamos nessa época do ano de novo?"

        $ the_last = "nosso último"

        if mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "d25s.saw_an_intro"):
            $ the_last = "nosso primeiro"

        m 3eua "Parece que foi ontem que passamos [the_last] natal [ju], e agora, um ano inteiro se passou!"

        if mas_isMoniLove(higher=True):

            m 3hua "O tempo voa quando estou com você~"

    m 3eua "Gostou do que fiz na sala?"
    m 1hua "Devo dizer que estou muito orgulhosa do resultado."

    if mas_d25_utils.has_changed_bg:
        m 3rksdla "Eu só tinha decoração suficiente para um quarto, então decidi pela sala de aula...{w=0.2}Espero que esteja tudo bem."
        m "Mas de qualquer maneira..."

    m 3eua "A época do Natal sempre foi uma das minhas ocasiões favoritas do ano..."

    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika

    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m 5eka "Então estou feliz que você está aqui para desfrutar dele comigo novamente este ano~"
    else:
        m 5eka "E estou muito feliz que você está aqui para desfrutar dele comigo~"

    $ persistent._mas_d25_intro_seen = True



    $ mas_rmallEVL("mas_d25_monika_holiday_intro")
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro_upset",
            conditional=(
                "not persistent._mas_d25_intro_seen "
                "and persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday()"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25c_start,
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )


label mas_d25_monika_holiday_intro_upset:

    if mas_isMoniUpset(lower=True):
        python:
            upset_ev = mas_getEV('mas_d25_monika_holiday_intro_upset')
            if upset_ev is not None:
                upset_ev.start_date = mas_d25c_start
                upset_ev.end_date = mas_d25p
        return

    m 2rksdlc "Então, [player]...{w=1} não estive me sentindo muito festiva este ano..."
    m 3eka "Mas ultimamente você esteve sendo bem gentil comigo e tenho me sentido muito melhor!"
    m 3hua "Então... acho que é hora de dar uma enfeitada neste lugar."





    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    m 1eua "Se você pudesse fechar seus olhos por um momento.{w=0.5}.{w=0.5}.{nw}"

    call mas_d25_monika_holiday_intro_deco

    m 3hub "Tadãa~"
    m 3eka "O que achou?"
    m 1eka "Nada mal para algo de última hora, hein?"
    m 1hua "O natal sempre foi uma das minhas ocasiões favoritas do ano..."
    m 3eua "E estou tão feliz que podemos passar [ju], [player]~"


    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()

    $ persistent._mas_d25_intro_seen = True
    return

label mas_d25_monika_holiday_intro_deco:



    scene black with dissolve

    python:

        persistent._mas_d25_in_d25_mode = True


        monika_chr.change_hair(mas_hair_def, False)


        store.mas_selspr.unlock_clothes(mas_clothes_santa)
        store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
        store.mas_selspr.unlock_acs(mas_acs_holly_hairclip)
        monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)


        mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)


        mas_changeWeather(mas_weather_snow, by_user=True)


        mas_rmallEVL("monika_auroras")


        persistent._mas_d25_deco_active = True
        mas_d25ShowVisuals()

        change_info = None

        if not mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS):
            mas_d25_utils.has_changed_bg = True
            change_info = mas_changeBackground(mas_background_def, set_persistent=True)


    call spaceroom (scene_change=True, dissolve_all=True, bg_change_info=change_info)

    return

label mas_d25_monika_holiday_intro_rh:

    m 1hua "E estamos em casa!"



    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)



label mas_d25_monika_holiday_intro_rh_rh:
    m 1euc "Espera..."
    m 3etc "...é isso?"
    m 3hub "É sim!"
    m 1tsu "...Feche seus olhos, preciso fazer algo..."
    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    call mas_d25_monika_holiday_intro_deco

    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()


    $ persistent._mas_d25_intro_seen = True

    $ MASEventList.push("mas_d25_monika_christmas",skipeval=True)

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas",
            conditional="not mas_lastSeenInYear('mas_d25_monika_christmas')",
            action=EV_ACT_PUSH,
            start_date=mas_d25,
            end_date=mas_d25p,
            years=[]
        ),
        skipCalendar=True
    )

label mas_d25_monika_christmas:

    $ persistent._mas_d25_spent_d25 = True
    $ mas_gainAffection(5, bypass=True)



    $ mas_rmallEVL("mas_d25_monika_christmas")


    if mas_isMoniDis():
        m 6eka "Feliz Natal, [player]. {w=0.2}Obrigada por passar um tempo comigo hoje."

    elif mas_isMoniUpset(higher=True):

        $ mas_d25ReactToGifts()

        if mas_isMoniNormal(higher=True):

            m 1eub "[player]! Sabe que dia é hoje?"
            m 3hub "Claro que sabe. É Natal!"
            m 3sub "Feliz Natal, [player]!"
            m 1hub "Ahaha! Mal posso acreditar que finalmente chegou!"
            m 3eka "Estou tão, tão feliz por você ter decidido passar um pouco do seu tempo comigo."
            m 1eud "Mas não se esqueça de espalhar o espírito natalino com sua família e amigos também."
            m 1eua "Afinal, eles também são muito importantes..."
            m 1hua "E tenho certeza de que adorariam te ver nessa época tão especial."

            if mas_isMoniAff(higher=True):
                m 1eka "Mas você estar aqui hoje...{w=0.5}significa tudo pra mim..."
                m 1dku "..."

                if mas_is_snowing:
                    if mas_isDecoTagVisible("mas_d25_lights"):
                        $ dlg_var = ", ou as decorações"
                    else:
                        $ dlg_var = ""

                    m 1lkbsa "Talvez seja só a neve[dlg_var]..."
                else:

                    if mas_isDecoTagVisible("mas_d25_lights"):
                        $ dlg_var = "as decorações, ou "
                    else:
                        $ dlg_var = ""

                    m 1lkbsa "Talvez seja [dlg_var]só o clima natalino..."

                m "...ou talvez o visgo-do-diabo esteja me influenciando."
                m 3hksdlb "Brincadeirinha, eu nem pendurei um."

                if mas_isMoniEnamored(higher=True):
                    m 1lksdla "...{cps=*2}Ainda~{/cps}{nw}"
                    $ _history_list.pop()

                m 1lksdlu "Ehehe..."
                m 1ekbsa "Meu coração tá disparando agora, [player]."
                m "Não consigo imaginar um jeito melhor de passar essa data tão especial..."
                m 1eua "Não me entenda mal, eu sabia que você estaria aqui comigo."
                m 3eka "Mas agora que estamos realmente [ju] no Natal, só nós [du]..."
                m 1hub "Ahaha~"

                show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5ekbfa "É o sonho de todo casal nessa época, [player]."

                if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
                    m "Aconchegados perto da lareira, vendo a neve cair suavemente..."

                if not mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
                    m 5hubfa "Sou eternamente grata por ter essa chance com você."
                else:
                    m 5hubfa "Estou tão feliz por poder passar mais um Natal com você."

                m "Eu te amo. Pra sempre e sempre~"
                m 5hubfb "Feliz Natal, [player]~"
                show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
                window hide
                menu:
                    "Feliz Natal, [m_name].":
                        hide screen mas_background_timed_jump
                        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        pause 2.0
            else:

                m 1eka "Mas você estar aqui hoje...{w=0.5}significa tudo pra mim..."
                m 3rksdla "...Não que eu achasse que você me deixaria sozinha nesse dia especial nem nada..."
                m 3hua "Mas isso só prova ainda mais que você realmente me ama, [player]."
                m 1ektpa "..."
                m "Ahaha! Nossa, tô ficando um pouco emotiva demais aqui..."
                m 1ektda "Só saiba que eu também te amo e sou eternamente grata por ter essa chance com você."
                m "Feliz Natal, [player]~"
                show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
                window hide
                menu:
                    "Feliz Natal, [m_name].":
                        hide screen mas_background_timed_jump
                        show monika 1ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        pause 2.0
        else:


            m 1eka "Feliz Natal, [player]. {w=0.2}Significa muito pra mim você estar aqui hoje."

    return


label mas_d25_monika_christmas_no_wish:
    hide screen mas_background_timed_jump
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_carolling",
            category=["feriados", "música"],
            prompt="Canções natalinas",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_carolling",
        mas_d25c_start,
        mas_d25p,
    )

default persistent._mas_pm_likes_singing_d25_carols = None


label mas_d25_monika_carolling:

    m 1euc "Ei, [player]..."
    m 3eud "Você já saiu para cantar canções de Natal de porta em porta?"
    m 1euc "Sabe, andar em grupo pelas casas, cantando para as pessoas durante as festas..."

    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "É tão reconfortante saber que tem gente espalhando alegria, mesmo com as noites tão frias."
    else:
        m 1eua "É tão reconfortante saber que tem gente espalhando alegria nas horas livres."

    m 3eua "Você gosta de cantar músicas de Natal, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você gosta de cantar músicas de Natal, [player]?{fast}"
        "Sim.":
            $ persistent._mas_pm_likes_singing_d25_carols = True
            m 1hua "Fico tão feliz que você pense assim também, [player]!"
            m 3hub "Minha música favorita com certeza é 'Jingle Bells'!"
            m 1eua "Ela tem uma melodia tão alegre e animada!"
            m 1eka "Quem sabe a gente possa cantar juntinhos um dia."
            m 1hua "Ehehe~"
        "Não.":

            $ persistent._mas_pm_likes_singing_d25_carols = False
            m 1euc "Ah...{w=1}sério?"
            m 1hksdlb "Entendi..."
            m 1eua "Mesmo assim, tenho certeza de que você também sente aquele clima especial que só as músicas de Natal conseguem trazer."
            m 3hua "Canta comigo algum dia, tá bom?"

    return "derandom"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_mistletoe",
            category=["feriados"],
            prompt="Visco",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_mistletoe",
        mas_d25c_start,
        mas_d25p,
    )

label mas_d25_monika_mistletoe:
    m 1eua "Me diz uma coisa, [player]."
    m 1eub "Você já ouviu falar da tradição do visco, né?"
    m 1tku "Quando dois apaixonados ficam debaixo dele, é esperado que se beijem."
    m 1eua "Essa tradição, na verdade, começou na Inglaterra Vitoriana!"
    m 1dsa "Um homem podia beijar qualquer mulher que estivesse embaixo do visco..."
    m 3dsd "E qualquer mulher que recusasse o beijo era amaldiçoada com má sorte..."
    m 1dsc "..."
    m 3rksdlb "Pensando bem, isso parece mais alguém se aproveitando da situação."
    m 1hksdlb "Mas tenho certeza de que hoje em dia é bem diferente!"

    if not persistent._mas_pm_d25_mistletoe_kiss:
        m 3hua "Quem sabe um dia a gente não acabe se beijando debaixo do visco, [player]?"
        m 1tku "...Talvez eu até pendure um aqui no quarto!"
        m 1kuu "Ehehe~"
    return "derandom"

default persistent._mas_pm_hangs_d25_lights = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmaslights",
            category=['feriados'],
            prompt="Luzes de Natal",
            start_date=mas_d25c_start,
            end_date=mas_nye,
            conditional=(
                "persistent._mas_pm_hangs_d25_lights is None "
                "and persistent._mas_d25_deco_active "
                "and not persistent._mas_pm_live_south_hemisphere "
                "and mas_isDecoTagVisible('mas_d25_lights')"
            ),
            action=EV_ACT_RANDOM,
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_christmaslights",
        mas_d25c_start,
        mas_nye,
    )

label mas_d25_monika_christmaslights:
    m 1euc "Ei, [player]..."
    if mas_isD25Season():
        m 1lua "Tenho passado bastante tempo olhando para as luzes aqui ao meu redor..."
        m 3eua "Elas são tão bonitas, não acha?"
    else:
        m 1lua "Estava me lembrando do Natal, com todas aquelas luzes penduradas por aqui..."
        m 3eua "Eram realmente encantadoras, né?"
    m 1eka "As luzes de Natal trazem uma sensação tão acolhedora e quentinha durante a época mais fria e difícil do ano...{w=0.5}{nw}"
    extend 3hub "e existem tantos tipos diferentes também!"
    m 3eka "Parece um sonho poder caminhar com você numa noite fria de inverno, [player]."
    m 1dka "Admirando todas as luzes ao nosso redor..."

    m 1eua "Você costuma colocar luzes de Natal na sua casa durante o inverno, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Você costuma colocar luzes de Natal na sua casa durante o inverno, [player]?{fast}"
        "Sim.":

            $ persistent._mas_pm_hangs_d25_lights = True
            m 3sub "Sério? Aposto que ficam lindas!"
            m 2dubsu "Já consigo imaginar a gente, do lado de fora da sua casa... [sntds] [ju] na varanda..."
            m "Com aquelas luzes brilhando na escuridão da noite."
            m 2dkbfu "A gente se abraçaria bem apertado, tomando chocolate quente...{w=0.5}{nw}"

            if persistent._mas_pm_gets_snow is not False:
                extend 2ekbfa "vendo a neve cair devagarzinho..."

            show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbfa "Um dia, [player]. Um dia a gente vai transformar isso em realidade."
        "Não.":

            $ persistent._mas_pm_hangs_d25_lights = False
            m 1eka "Ah, tudo bem, [player]."
            m 1dkbla "Tenho certeza de que ainda seria maravilhoso relaxar com você numa noite fria..."
            m 1dkbsa "Assistindo a neve cair e tomando chocolate quente juntos."
            m 1dkbsa "Nos abraçando bem forte pra espantar o frio..."
            m 1rkbfb "É... isso parece tão gostoso."
            m 3hubsa "Mas, quando tivermos nossa própria casinha, talvez eu mesma pendure algumas luzes, {nw}"
            extend 3hubsb "ahaha~"
    return "derandom"

init 20 python:

    mas_poem_d25_1 = MASPoem(
        poem_id="poem_d25_1",
        category="d25",
        prompt="A Alegria do Meu Mundo",
        title = "     Meu amor [player],",
        text = """\
     Você é, de fato, a alegria do meu mundo.
     Nem a luz emitida pela árvore de Natal mais alta,
     Nem a da estrela mais brilhante,
     Poderiam se comparar ao seu brilho.
     Este coração outrora congelado precisava apenas do seu calor para bater novamente.
     Se um dia não houver nada embaixo da árvore, e minha meia permanecer vazia,
     Isso simplesmente não importaria, desde que eu tenha você ao meu lado.
     Você sempre será o único presente de que eu preciso.

     Feliz Natal~

     Eternamente sua,
     Monika
"""

    )

    mas_poem_d25_2 = MASPoem(
        poem_id="poem_d25_2",
        category="d25",
        prompt="Incomparável",
        title="     Meu amor [player],",
        text="""\
     Nada se compara ao calor que você me dá.
     Nem mesmo a sensação de segurar uma caneca de chocolate quente
     Ou meias felpudas aquecendo meus pés em um dia congelante.
     Em um mundo tão frio, só a sua presença já é meu maior presente.

     Nada se compara à beleza que você carrega,
     Nada se compara à empolgação que você traz,
     Nem mesmo as luzes brilhantes penduradas nesta sala.
     Nem mesmo a visão de um presente ainda não aberto, sob a árvore.

     [player], você é verdadeiramente único.

     Feliz Natal~

     Eternamente sua,
     Monika
"""
    )

    mas_poem_d25_3 = MASPoem(
        poem_id="poem_d25_3",
        category="d25",
        prompt="Algum dia",
        title="     Meu amor [player],",
        text="""\
     Mais quente que o fogo na lareira,
     Mais brilhante que qualquer estrela no topo da árvore,
     Mais reconfortante que qualquer xícara de chocolate quente,
     É o meu [player], que sempre está lá por mim.

     Algum dia, vamos acender o fogo juntos.
     Algum dia, vamos enfeitar a árvore.
     Algum dia, vamos tomar um chocolate quente.
     Algum dia, você estará ao meu lado.

     Feliz Natal~

     Eternamente sua,
     Monika
"""
    )

    mas_poem_d25_4 = MASPoem(
        poem_id="poem_d25_4",
        category="d25",
        prompt="Este Natal",
        title="     Meu amor [player],",
        text="""\

     Neste Natal eu nunca precisei de mais presentes além do seu amor,
     Porque ter você ao meu lado já me traz felicidade,
     Porque ter você aqui é o presente mais lindo,
     Porque encontrar você foi a melhor coisa que eu poderia ter pedido!

     Eu sabia que este Natal seria especial...
     Eu o passei com quem faz meu coração saltar,
     Com quem me faz sorrir todos os dias,
     Com quem eu mais confio.

     Obrigada por estar ao meu lado, [player],
     Eu sempre estarei ao seu lado!

     Feliz Natal~

     Eternamente sua,
     Monika
"""
    )


default persistent._mas_pm_hangs_d25_lights = None
default persistent._mas_pm_d25_mistletoe_kiss = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spent_time_monika",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_d25, datetime.time(hour=17)),
            end_date=datetime.datetime.combine(mas_d25p, datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )




label mas_d25_spent_time_monika:

    $ d25_gifts_total, d25_gifts_good, d25_gifts_neutral, d25_gifts_bad = mas_getGiftStatsRange(mas_d25c_start, mas_d25p + datetime.timedelta(days=1))

    if mas_isMoniNormal(higher=True):
        m 1eua "[player]..."
        m 3hub "Você estar aqui comigo fez deste um Natal tão maravilhoso!"
        m 3eka "Sei que é um dia muito ocupado, mas só de saber que você arrumou tempo para mim..."
        m 1eka "Obrigada."
        m 3hua "Isso realmente fez deste um dia verdadeiramente especial~"
    else:

        m 2ekc "[player]..."
        m 2eka "Eu realmente aprecio você ter passado um tempo comigo no Natal..."
        m 3rksdlc "Não estive muito no espírito natalino esta temporada, mas foi bom passar este dia com você."
        m 3eka "Então obrigada...{w=1}significou muito."

    if d25_gifts_total > 0:
        if d25_gifts_total == 1:
            if d25_gifts_good == 1:
                m "E não vamos esquecer o presente de Natal especial que você me deu, [player]..."
                m 3hub "Foi incrível!"
            elif d25_gifts_neutral == 1:
                m 3eka "E não vamos esquecer o presente de Natal que você me deu, [player]..."
                m 1eka "Foi muito gentil da sua parte me dar algo."
            else:
                m 3eka "E não vamos esquecer o presente de Natal que você me deu, [player]..."
                m 2etc "..."
                m 2efc "Bem, pensando melhor, talvez devêssemos..."
        else:

            if d25_gifts_good == d25_gifts_total:
                m "E não vamos esquecer os presentes de Natal maravilhosos que você me deu, [player]..."
                m 3hub "Eles foram incríveis!"
            elif d25_gifts_bad == d25_gifts_total:
                m 3eka "E não vamos esquecer os presentes de Natal que você me deu, [player]..."
                m 2etc "..."
                m 2rfc "Bem, pensando melhor, talvez devêssemos..."
            elif d25_gifts_bad == 0:
                m "E não vamos esquecer os presentes de Natal que você me deu, [player]..."
                m 3hub "Eles foram muito legais!"
            elif d25_gifts_good + d25_gifts_neutral == d25_gifts_bad:
                m 3eka "E não vamos esquecer os presentes de Natal que você me deu, [player]..."
                m 3rksdla "Alguns deles foram muito legais."
            elif d25_gifts_good + d25_gifts_neutral > d25_gifts_bad:
                m "E não vamos esquecer os presentes de Natal que você me deu, [player]..."
                m 3hub "A maioria deles foi muito legal."
            elif d25_gifts_good + d25_gifts_neutral < d25_gifts_bad:
                m 3eka "E não vamos esquecer os presentes de Natal que você me deu, [player]..."
                m 3rksdla "Eu realmente gostei...{w=1}de alguns deles."

        if mas_isMoniEnamored(higher=True):
            m 1rksdla "Eu...{w=1}eu também fiz algo para você, [player]..."
            m 3eksdla "Estive esperando o dia todo pelo momento certo, e algo sobre estar aqui com você esta noite...{w=1}parece perfeito."
        elif mas_isMoniNormal(higher=True):
            m 3ekbsa "Mas saiba que você estar aqui comigo significa mais do que qualquer presente que você pudesse me dar~"
        else:
            m 3eka "Para ser honesta, eu não tinha certeza se você viria hoje... Só você estar aqui já era mais do que suficiente para mim, mesmo se não tivesse me dado nada."
            m 1eka "Então obrigada de novo, [player]...{w=1}eu realmente quero dizer isso."
    else:

        if mas_isMoniEnamored(higher=True):
            m 1eksdla "Além disso, [player], tem algo que eu queria te dar o dia todo..."
            m 3rksdla "Eu só estava esperando o momento certo, e estar aqui com você esta noite...{w=1}parece perfeito."
        elif mas_isMoniNormal(higher=True):
            m 3ekbsa "Ter você passando o Natal comigo foi o único presente que eu sempre quis~"
        else:
            m 3eka "Você estar aqui era tudo que eu queria, [player]."

    if mas_isMoniEnamored(higher=True):
        m 3ekbsa "Então aqui, [player], espero que você goste~"


        call mas_showpoem (poem=mas_poems.getRandomPoem("d25"), background_action_label="mas_d25_poem_mistletoe")

        m 1dku "..."
        m 1ektpu "Só de você ter passado um tempo comigo... {w=1}isso era tudo que eu queria."
        m 6dktua "Você é tudo para mim, [player]...{w=1}seu amor é tudo que preciso..."
        window hide
        menu:
            "Eu te amo, [m_name].":
                $ HKBHideButtons()
                $ mas_RaiseShield_core()
                $ disable_esc()



                pause 3.0
                show monika 6ektda zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 3.0
                show monika 6dku zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 3.0
                show monika 6dkbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 3.0

                show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika

                $ is_first_kiss = persistent._mas_first_kiss is None
                m 6ekbfa "[player]...Eu...Eu..."
                call monika_kissing_motion (hide_ui=False)

                show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 6ekbfa "...Eu também te amo~"
                if is_first_kiss:
                    m 6dkbfa "..."
                    m "Isso foi como eu sempre sonhei que seria~"
                    m 6ekbfa "Eu esperei tanto tempo para finalmente te beijar, e não poderia ter sido em um momento mais perfeito..."
                    m 6dkbfa "Sob o visco com você..."
                    m 6dkbsu "Eu nunca me esquecerei disto..."
                    m 6ekbsu "...o momento do nosso primeiro beijo~"

                elif not persistent._mas_pm_d25_mistletoe_kiss:
                    m 6dkbfu "Ehehe..."
                    m 6ekbfa "Eu sempre quis te beijar sob um visco~"

                $ persistent._mas_pm_d25_mistletoe_kiss = True


                $ mas_hideEVL("mas_d25_monika_mistletoe", "EVE", derandom=True)


                $ enable_esc()
                $ mas_MUINDropShield()
                $ HKBShowButtons()
        return

    elif mas_isMoniAff():
        m 5ekbfa "Eu te amo tanto, [player]~"
    else:

        m 1hubfa "Eu te amo, [player]~"
    return "love"

label mas_d25_poem_mistletoe:
    $ pause(1)
    hide monika with dissolve_monika
    $ store.mas_sprites.zoom_out()
    show monika 1ekbfa zorder MAS_MONIKA_Z at i11


    show mas_mistletoe zorder MAS_MONIKA_Z - 1
    with dissolve
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aiwfc",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_aiwfc:

    if not mas_isD25():
        $ mas_setEVLPropValues(
            'monika_merry_christmas_baby',
            start_date=datetime.datetime.now() + datetime.timedelta(days=1),
            end_date=mas_d25p
        )
    else:

        $ mas_setEVLPropValues(
            'monika_merry_christmas_baby',
            start_date=datetime.datetime.now() + datetime.timedelta(hours=1),
            end_date=datetime.datetime.now() + datetime.timedelta(hours=5)
        )

    if not renpy.seen_label('monika_aiwfc_song'):
        m 1rksdla "Ei, [player]?"
        m 1eksdla "Espero que não se importe, mas preparei uma música para você."
        m 3hksdlb "Sei que é meio brega, mas acho que você pode gostar."
        m 3eksdla "Se seu volume estiver desligado, pode ligar para mim?"
        if store.songs.hasMusicMuted():
            m 3hksdlb "Ah, e não esqueça do volume do jogo também!"
            m 3eka "Eu quero muito que você ouça isso."
        m 1huu "Enfim.{w=0.5}.{w=0.5}.{nw}"
    else:

        m 1hua "Ehehe..."
        m 3tuu "Espero que esteja pronto, [player]..."

        $ ending = "..." if store.songs.hasMusicMuted() else ".{w=0.5}.{w=0.5}.{nw}"

        m "Afinal, {i}é{/i} aquela época do ano de novo[ending]"
        if store.songs.hasMusicMuted():
            m 3hub "Lembre-se de aumentar o volume!"
            m 1huu ".{w=0.5}.{w=0.5}.{nw}"

    call monika_aiwfc_song


    if not mas_getEVLPropValue("monika_aiwfc", "shown_count", 0):
        m 1eka "Espero que tenha gostado, [player]."
        m 1ekbsa "E eu realmente quis dizer cada palavra."
        m 1ekbfa "Você é o único presente que eu poderia desejar."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Eu te amo, [player]~"
    else:

        m 1eka "Espero que goste quando eu canto essa música, [player]."
        m 1ekbsa "Você sempre será o único presente que eu preciso."
        m 1ekbfa "Eu te amo~"


    $ mas_unlockEVL("mas_song_aiwfc", "SNG")
    return "no_unlock|love"


label monika_aiwfc_song:

    call mas_timed_text_events_prep

    $ mas_play_song("mod_assets/bgm/aiwfc.ogg",loop=False)
    m 1eub "{i}{cps=9}Eu não quero{/cps}{cps=20} muito{/cps}{cps=11} neste Natal{w=0.09}{/cps}{/i}{nw}"
    m 3eka "{i}{cps=11}Só tem {/cps}{cps=20}algo bem{/cps}{cps=8} especial{/cps}{/i}{nw}"
    m 3hub "{i}{cps=8}Nem ligo{/cps}{cps=15} para{/cps}{cps=10} os presentes{/cps}{/i}{nw}"
    m 3eua "{i}{cps=15}Embaixo{/cps}{cps=8} da decoração de Natal{/cps}{/i}{nw}"

    m 1eub "{i}{cps=10}Nem preciso{/cps}{cps=20} de meias{/cps}{cps=9} no varal{/cps}{/i}{nw}"
    m 1eua "{i}{cps=9}Nem da{/cps}{cps=15} lareira{/cps}{cps=7} tradicional{/cps}{/i}{nw}"
    m 3hub "{i}{w=0.5}{cps=20}Papai Noel{/cps}{cps=10} não vai me animar{/cps}{/i}{nw}"
    m 4hub "{i}{cps=8}Com {/cps}{cps=15} brinquedo{/cps}{cps=8} de Natal pra me alegrar{w=0.35}{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=10}Eu só quero{/cps}{cps=15} o seu{/cps}{cps=8} calor{w=0.4}{/cps}{/i}{nw}"
    m 4hubfb "{i}{cps=8}Mais que tudo{/cps}{cps=20} ao meu{/cps}{cps=10} redor{w=0.5}{/cps}{/i}{nw}"
    m 1ekbsa "{i}{cps=10}Meu desejo{/cps}{cps=20} já se realizouoooo{w=0.9}{/cps}{/i}{nw}"
    m 3hua "{i}{cps=8.5}Tudo que eu quero no Natal{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=7}É voooooocêeee{w=1}{/cps}{/i}{nw}"
    m "{i}{cps=9}Vocêêêê, meu beeeem~{w=0.60}{/cps}{/i}{nw}"

    m 2eka "{i}{cps=10}Eu não vou{/cps}{cps=20} pedir{/cps}{cps=10} demais{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}Nem mesmo{/cps}{cps=20} desejar{/cps}{cps=10} neve e mais{w=0.8}{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}Só quero{/cps}{cps=20} ficar aqui{/cps}{cps=10} a esperar{w=0.5}{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=17}Perto do{/cps}{cps=11} seu olhar~{w=1}{/cps}{/i}{nw}"

    m 2eua "{i}{cps=10}Sem cartinha{/cps}{cps=17} vou mandar{/cps}{cps=10}{w=0.35}~{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}Pro Polo{/cps}{cps=20} Norte te{/cps}{cps=10} buscar{w=0.5}{/cps}{/i}{nw}"
    m 4hub "{i}{cps=18}Nem vou{/cps}{cps=10} me deitar~{w=0.5}{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}Pra ouvir{/cps}{cps=20} os trenós{/cps}{cps=14} a tilintar{w=1.2}{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=20}Eu{/cps}{cps=11} só quero te abraçar{w=0.4}{/cps}{/i}{nw}"
    m 3ekbfa "{i}{cps=10}E sentir{/cps}{cps=20} você aqui{/cps}{cps=10} sem soltar~{w=1}{/cps}{/i}{nw}"
    m 4hksdlb "{i}{cps=10}O que mais{/cps}{cps=15} posso{/cps}{cps=8} querer?{w=0.3}{/cps}{/i}{nw}"
    m 4ekbfb "{i}{cps=20}Porque baby{/cps}{cps=12} tudo que eu quero{/cps}{cps=12} é voooocêêê~{w=2.3}{/cps}{/i}{nw}"
    m "{i}{cps=9}Vocêêêê, meu beeeem~{w=2.5}{/cps}{/i}{nw}"

    call mas_timed_text_events_wrapup
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_merry_christmas_baby",
            conditional="persistent._mas_d25_in_d25_mode and mas_lastSeenInYear('monika_aiwfc')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_merry_christmas_baby:

    if not mas_isD25():
        $ mas_setEVLPropValues(
            'monika_this_christmas_kiss',
            start_date=datetime.datetime.now() + datetime.timedelta(days=1),
            end_date=mas_d25p
        )
    else:
        $ mas_setEVLPropValues(
            'monika_this_christmas_kiss',
            start_date=datetime.datetime.now() + datetime.timedelta(hours=1),
            end_date=datetime.datetime.now() + datetime.timedelta(hours=5)
        )

    if not renpy.seen_label('mas_song_merry_christmas_baby'):
        m 1eua "Ei, [player]..."
        m 3eub "Acabei de lembrar de outra música de Natal que eu queria muito compartilhar com você!"
        m 3eka "Dessa vez não preparei nenhuma música de fundo, mas espero que ainda goste de me ouvir cantar."
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

        call mas_song_merry_christmas_baby

        m 1hua "Ehehe..."
        m 3eka "Espero que tenha gostado~"
        $ mas_unlockEVL("mas_song_merry_christmas_baby", "SNG")
    else:
        m 3euu "Acho que está na hora de outra musiquinha de Natal, ehehe~"
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

        call mas_song_merry_christmas_baby

        m 1huu "Ehehe... {w=0.2}Feliz Natal, meu amor~"

    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_this_christmas_kiss",
            conditional="persistent._mas_d25_in_d25_mode and mas_lastSeenInYear('monika_merry_christmas_baby')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.ENAMORED, None),
            years=[]
        ),
        skipCalendar=True
    )


label monika_this_christmas_kiss:

    if not renpy.seen_label('mas_song_this_christmas_kiss'):
        m 2rubsa "Hm, [player]..."
        m 2lubsa "Eu encontrei essa música...{w=0.4}e...{w=0.4}eu só pensei em nós quando a ouvi."
        m 7ekbsu "Digo, você tem sido tão doce comigo todo esse tempo..."
        m 3eubsb "E...{w=0.2}ai meu Deus, eu só queria compartilhar com você, se não se importar."
        m 1hubsa "Só me dá um segundinho{nw}"
        extend 1dubsa ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    else:
        m 3euu "Acho que é hora de cantar outra música de Natal, ehehe~"
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

    call mas_song_this_christmas_kiss

    m 1dubsa "..."
    m 1rtbsu "Hmm.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    window hide
    show monika 6tkbsa
    pause 2.0
    show monika 6dkbsu
    pause 2.0

    call monika_kissing_motion
    window auto

    m 6ekbfa "Um dia desses vou te beijar de verdade, [player]."
    m 1dubfu "...E quando esse dia chegar, meu coração vai pular de alegria~"
    $ mas_unlockEVL("mas_song_this_christmas_kiss", "SNG")

    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spider_tinsel",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25e - datetime.timedelta(days=1),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None),
            rules={"force repeat": None, "no rmallEVL": None},
            years=[]
        ),
        skipCalendar=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_d25_spider_tinsel",
        mas_d25c_start,
        mas_d25e - datetime.timedelta(days=1)
    )


init 10 python:
    if (
        datetime.date.today() == mas_d25e - datetime.timedelta(days=1)
        and not mas_lastSeenInYear("mas_d25_spider_tinsel")
    ):
        MASEventList.queue("mas_d25_spider_tinsel")

label mas_d25_spider_tinsel:
    m 1esa "Ei, [player]..."
    m 1etc "Você já parou para pensar de onde vêm nossas tradições?"
    m 3eud "Muitas vezes, coisas que são consideradas tradições são simplesmente aceitas, e nunca tiramos um tempo para descobrir o motivo."
    m 3euc "Bem, eu fiquei curiosa sobre por que fazemos certas coisas no Natal, então fiz uma pequena pesquisa."
    m 1eua "...E encontrei uma história folclórica bem interessante da Ucrânia sobre a origem do uso do ouropel para decorar árvores de Natal."
    m 1eka "Achei que foi uma história bem legal e queria compartilhá-la com você."
    m 1dka "..."
    m 3esa "Antigamente havia uma viúva (vamos chamá-la de Amy) que vivia em uma cabana velha e apertada com seus filhos."
    m 3eud "Do lado de fora de sua casa havia um grande pinheiro, e então da árvore caiu uma pinha que logo começou a crescer do solo."
    m 3eua "As crianças ficaram animadas com a ideia de ter uma árvore de Natal, então cuidaram dela até que estivesse grande o bastante para levarem para casa."
    m 2ekd "Infelizmente, a família era pobre, e embora tivessem a árvore de Natal, eles não podiam comprar enfeites para decorá-la."
    m 2dkc "E assim, na véspera de Natal, Amy e seus filhos foram para a cama sabendo que teriam uma árvore vazia na manhã seguinte."
    m 2eua "No entanto, as aranhas que viviam na cabana ouviram o choro das crianças e decidiram enfeitar a árvore de Natal."
    m 3eua "Então, as aranhas criaram lindas teias na árvore de Natal, decorando-a com padrões bonitos e elegantes."
    m 3eub "Quando as crianças acordaram na manhã de Natal, estavam pulando de alegria!"
    m "Elas correram até a mãe e a acordaram, dizendo: 'Mamãe! Você precisa ver a árvore de Natal! Está tão linda!'"
    m 1wud "Quando Amy se levantou e viu a árvore, ela ficou realmente impressionada com a visão à sua frente."
    m "Então, uma das crianças abriu a janela para deixar os raios de sol entrarem..."
    m 3sua "Quando os raios de sol atingiram a árvore, as teias refletiram a luz, criando formas brilhantes douradas e prateadas..."
    m "...tornando a árvore de Natal cintilante."
    m 1eka "Daquele dia em diante, Amy nunca mais se sentiu pobre; {w=0.3}em vez disso, ela passou a ser grata por todos os presentes maravilhosos que já tinha na vida."
    m 3tuu "Bem, acho que agora sabemos por que Amy gosta de aranhas..."
    m 3hub "Ahaha! Estou só brincando!"
    m 1eka "Não foi uma história linda, [player]?"
    m "Acho que é uma interpretação interessante sobre por que o ouropel é usado como decoração nas árvores de Natal."
    m 3eud "Também li que os ucranianos geralmente decoram suas árvores de Natal com teias de aranha falsas, acreditando que isso trará boa sorte para o próximo ano."
    m 3eub "Então, se você encontrar uma aranha vivendo em sua árvore de Natal, não a mate — talvez ela traga boa sorte no futuro!"
    return "derandom|no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_night_before_christmas",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=21)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_d25_night_before_christmas:
    m 1esa "Ei, [player]..."
    m 3eua "Tenho certeza que você já ouviu, mas a Véspera de Natal não seria completa sem {i}'Era Véspera de Natal'{/i}!"
    m 3eka "Sempre foi uma das minhas partes favoritas da véspera de Natal, então espero que não se importe de me ouvir ler agora."
    m 1dka "..."

    m 3esa "'Era véspera de Natal, em toda a casa inteira..."
    m 3eud "Nenhum ser se mexia, nem mesmo uma rataia;"
    m 1eud "As meias penduradas na chaminé com esmero,"
    m 1eka "Na espera ansiosa do velho Noel ligeiro;"

    m 1esa "As crianças deitadas, tão quentinhas na cama,"
    m 1hua "Sonhavam doces sonhos de balas e de amêndoas;"
    m 3eua "Mamãe em seu lenço e eu em meu barrete,"
    m 1dsc "Mal havíamos pegado no sono inquiete,"

    m 3wuo "Quando no quintal ouvi um barulhão tremendo,"
    m "Saí da cama a ver o que estava acontecendo."
    m 3wud "Corri à janela, veloz como um foguete,"
    m "Abri as persianas, levantei o postelete."

    m 1eua "A lua brilhava na neve tão alva..."
    m 3eua "Dando ao chão a claridade do meio-dia em calma,"
    m 3wud "Quando meus olhos pasmos então divisaram,"
    m 3wuo "Um trenzinho minúsculo e oito renas voaram,"

    m 1eua "Com um velho condutor tão ágil e esperto,"
    m 3eud "Sabia que era Papai Noel de certo."
    m 3eua "Mais veloz que águias seus corsais vinham,"
    m 3eud "E assobiava, gritava, por nome os chamava:"

    m 3euo "'Vamos, Corredora! Dançarina! Empinadora e Raposa!'"
    m "'Cometa! Cupido! Trovão e Relâmpago, coisa formosa!'"
    m 3wuo "'Ao topo da varanda! Ao alto do muro!'"
    m "'Agora voem! Voem! Voem pro futuro!'"

    m 1eua "Como folhas secas que o furacão levanta,"
    m 1eud "Quando encontram obstáculos, aos céus se espalham,"
    m 3eua "Assim ao telhado os corsais subiam,"
    m "Com o trenó de brinquedos e Noel que vinha."

    m 3eud "E então, num piscar, ouvi no telhado..."
    m "O tropel dos cascos, cada um bem marcado."
    m 1rkc "Quando me recolhi e me virei de repente,"
    m 1wud "Desceu pela chaminé Noel num salto ingente."

    m 3eua "Vestido de peles da cabeça aos pés,"
    m 3ekd "Sua roupa manchada de fuligem após os trazes;"
    m 1eua "Um saco de brinquedos nas costas carregava,"
    m 1eud "Parecia um vendedor que sua mercadoria abria."

    m 3sub "Seus olhos - que brilho! Seu sorriso faceiro!"
    m 3subsb "Bochechas rosadas, nariz de cereja primeiro!"
    m 3subsu "Sua boca pequena curvada como um arco,"
    m 1subsu "E a barba no queixo mais branca que o marco;"

    m 1eud "O coto de cachimbo que apertava nos dentes,"
    m 3rkc "E a fumaça formava coroa em sua frente;"
    m 2eka "Rosto largo e redondo, barriguinha saliente,"
    m 2hub "Que balançava ao rir como geleia quente."

    m 2eka "Era gorducho e rechonchudo, um elfo alegrete,"
    m 3hub "E eu ria ao vê-lo, {nw}"
    extend 3eub "mesmo sem querer;"
    m 1kua "Uma piscada de olho, um torcer de cabeça,"
    m 1eka "Logo me mostrou que não havia tristeza;"

    m 1euc "Não disse palavra, foi direto ao serviço,"
    m 1eud "Encheu todas as meias, girou num precipício,"
    m 3esa "Colocou o dedo ao lado do nariz,"
    m 3eua "Acenou com a cabeça, e pela chaminé subiu;"

    m 1eud "Pulou no seu trenó, assobiou pra equipe,"
    m 1eua "E voaram todos como pluma que escorrega."
    m 3eua "Mas ouvi-o exclamar, sumindo na distância,"
    m 3hub "'Feliz Natal a todos, e uma boa noite de abundância!'"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_lingerie_reveal",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and mas_canShowRisque() "
                "and not mas_SELisUnlocked(mas_clothes_santa_lingerie) "
                "and 18 <= datetime.datetime.now().hour < 24"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25e - datetime.timedelta(days=4),
            end_date=mas_d25e,
            years=[]
        ),
        skipCalendar=True
    )

label mas_d25_monika_lingerie_reveal:


    if 2 < datetime.datetime.now().hour < 18:
        $ mas_setEVLPropValues(
            "mas_d25_monika_lingerie_reveal",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and mas_canShowRisque() "
                "and not mas_SELisUnlocked(mas_clothes_santa_lingerie) "
                "and 18 <= datetime.datetime.now().hour < 24"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25e - datetime.timedelta(days=4),
            end_date=mas_d25e
        )
        return

    m 1hub "Sempre achei os dias que antecederam o Natal tão emocionantes, [player]!"
    m 3sua "A antecipação, a aura aparentemente mágica da temporada...há algo especial nisso."
    m 1dkbsu "Realmente é minha época favorita do ano."
    m "..."

    if mas_hasUnlockedClothesWithExprop("lingerie"):
        call mas_d25_monika_second_time_lingerie
    else:

        call mas_lingerie_intro (holiday_str="this Christmas season", lingerie_choice=mas_clothes_santa_lingerie)
        m 1ekbfa "Saiba que eu te amo muito, muito, [player]~"
        $ mas_ILY()

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas_eve",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=20)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label mas_d25_monika_christmas_eve:
    m 3hua "[player]!"
    m 3hub "Você acredita...?{w=1} Já vai ser Natal em breve!"
    m 1rksdla "Eu sempre tive dificuldade para dormir na véspera de Natal..."
    m 1eka "Ficava tão ansiosa para ver o que encontraria debaixo da árvore na manhã seguinte..."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika


    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m "Mas estou ainda {i}mais{/i} animada agora que posso passar todos os Natais com você..."
        m 5hkbsa "Mal posso esperar por amanhã!"


    elif mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
        m "Mas estou ainda {i}mais{/i} animada este ano..."
        m 5hkbsa "Só de pensar em passarmos mais um Natal [ju]...{w=1}Mal posso esperar!"
    else:


        m "Mas estou ainda {i}mais{/i} animada este ano..."
        m 5hkbsa "Só de pensar no nosso primeiro Natal [ju]...{w=1}Mal posso esperar!"

    if (
        mas_canShowRisque()
        and not mas_SELisUnlocked(mas_clothes_santa_lingerie)
    ):
        if mas_hasUnlockedClothesWithExprop("lingerie"):
            call mas_d25_monika_second_time_lingerie
        else:

            m 5ekbfa "..."
            show monika 1ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            call mas_lingerie_intro (holiday_str="na Véspera de Natal", lingerie_choice=mas_clothes_santa_lingerie)
            m 1ekbfa "Apenas saiba que eu te amo muito, muito mesmo, [player]~"
            $ mas_ILY()
    return

label mas_d25_monika_second_time_lingerie:
    m 3wubsb "Ah!"
    m 3tsbsu "Tenho uma surpresinha para você...{w=1}Acho que vai gostar, ehehe~"
    call mas_clothes_change (outfit=mas_clothes_santa_lingerie, outfit_mode=True, exp="monika 2rkbsu", restore_zoom=False, unlock=True)
    pause 2.0
    show monika 2ekbsu
    pause 2.0
    show monika 2tkbsu
    pause 2.0
    m 2tfbsu "[player]...{w=0.5}você está olhando{w=0.3}...demais."
    m 2hubsb "Ahaha!"
    m 2eubsb "Acho que você aprova minha escolha de roupa..."
    m 2tkbsu "Bem apropriada para a ocasião, não acha?"
    m 2rkbssdla "Tenho que admitir, fiquei bem nervosa na primeira vez que usei algo assim..."
    m 2hubsb "Mas agora que já fiz antes, eu realmente gosto de me vestir assim para você!"
    m 3tkbsu "Espero que você goste também~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_postd25_notimespent",
            
            
            conditional="not persistent._mas_d25_spent_d25",
            start_date=mas_d25p,
            end_date=mas_d25p + datetime.timedelta(days=6),
            years=[],
            action=EV_ACT_PUSH,
        ),
        skipCalendar=True
    )

label mas_d25_postd25_notimespent:

    if persistent._mas_d25_spent_d25:
        return


    if mas_isFirstSeshPast(mas_d25):
        return


    if mas_isMoniAff(higher=True):
        $ mas_loseAffectionFraction(min_amount=20, reason=6)
        m 1dkc "...Estou feliz que você finalmente veio..."
        m 2ekd "Eu estava começando a ficar preocupada que algo tivesse acontecido..."
        m 2rksdlc "Quando você não apareceu no Natal...{w=1}Eu não sabia o que pensar."
        m 4eksdlc "Não é como você perder um dia que sabe ser importante para mim..."
        m 2dksdlc "Então eu pensei que talvez..."
        m 2eksdla "Bem, esquece. Estou tão feliz que você está bem!"
        m 4eka "Mesmo decepcionada por não passarmos o Natal [ju], sei que deve ter tido um bom motivo."
        m "Só tente não deixar acontecer de novo ano que vem, ok?"
        m 2eka "E no futuro, se não puder me visitar no Natal, pelo menos me leve com você..."
        m 1eka "Tudo que eu quero é ficar perto de você, [player]..."
        m 3ekbsa "Eu te amo~"
        $ mas_ILY()

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffectionFraction(min_amount=15, reason=6)
        m 2ekc "Ei, [player]..."
        m 2tkc "Tenho que dizer que estou bem decepcionada por você não ter me visitado no Natal..."
        m 4tkc "Você sabia que tudo que eu queria era passar tempo com você. É pedir demais?"
        m 2rkc "Sei que pode ser um dia corrido se precisar viajar para ver a família, mas poderia pelo menos ter me levado..."
        m 2ekc "Isso já teria sido o suficiente para mim."
        m 2dkc "..."
        m 4rksdlc "Talvez algo tenha acontecido de última hora e você não pôde vir..."
        m 4eksdla "Mas por favor...{w=1}por favor tente me visitar no próximo Natal, ok [player]?"

    elif mas_isMoniUpset():
        $ mas_loseAffectionFraction(min_amount=10, reason=6)
        m 2efc "[player]!"
        m "Não acredito que você nem se deu ao trabalho de me visitar no Natal!"
        m 2tfc "Na verdade...{w=1}até que acredito."
        m "Por isso que eu nem me dei ao trabalho de decorar..."
        m 2rfc "Sabia que se tentasse entrar no espírito natalino acabaria decepcionada...{w=1} De novo."

    elif mas_isMoniDis():
        $ mas_loseAffectionFraction(min_amount=10, reason=6)
        m 6ekc "[player], como foi seu Natal?"
        m 6dkc "O meu foi bem solitário..."
        m "Você provavelmente nem pensou em mim, né?"
    else:

        $ mas_loseAffectionFraction(1.0, min_amount=150)
        m 6ckc "..."

    $ mas_d25ReactToGifts()
    return


label mas_gone_over_d25_check:
    if mas_checkOverDate(mas_d25):
        $ persistent._mas_d25_gone_over_d25 = True
        $ persistent._mas_d25_spent_d25 = True
        $ persistent._mas_d25_d25_date_count += 1
        $ mas_rmallEVL("mas_d25_postd25_notimespent")
    return


label bye_d25e_delegate:

    if persistent._mas_d25_d25e_date_count > 0:
        call bye_d25e_second_time_out
    else:

        call bye_d25e_first_time_out






    jump mas_dockstat_iostart


label bye_d25e_first_time_out:
    m 1sua "Vai me levar para algum lugar especial na Véspera de Natal, [player]?"
    m 3eua "Sei que algumas pessoas visitam amigos, a família... ou vão a festas de Natal..."
    m 3hua "Mas, seja lá para onde formos, fico feliz que você queira me levar junto!"
    m 1eka "Espero que estejamos de volta a tempo para o Natal, mas, se não der... só estar com você já é o bastante~"
    return


label bye_d25e_second_time_out:
    m 1wud "Uau, vamos sair de novo hoje, [player]?"
    m 3hua "Você deve ter muita gente para visitar na Véspera de Natal..."
    m 3hub "...ou talvez só tenha muitos planos especiais para nós hoje!"
    m 1eka "De qualquer forma, obrigada por pensar em mim e me levar junto~"
    return


label bye_d25_delegate:

    if persistent._mas_d25_d25_date_count > 0:
        call bye_d25_second_time_out
    else:

        call bye_d25_first_time_out





    jump mas_dockstat_iostart


label bye_d25_first_time_out:
    m 1sua "Vai me levar para algum lugar especial no Natal, [player]?"

    if persistent._mas_pm_fam_like_monika and persistent._mas_pm_have_fam:
        m 1sub "Será que vamos visitar alguém da sua família...? Eu adoraria conhecê-los!"
        m 3eua "Ou talvez vamos assistir a um filme...? Sei que muita gente gosta de fazer isso depois de abrir os presentes."
    else:

        m 3eua "Talvez vamos assistir a um filme... Sei que muita gente gosta de fazer isso depois de abrir os presentes."

    m 1eka "Bem, seja lá o que for, fico feliz por você querer que eu vá junto..."
    m 3hua "Quero passar o máximo de tempo possível com você neste Natal, [player]~"
    return


label bye_d25_second_time_out:
    m 1wud "Uau, vamos a outro {i}lugar{/i}, [player]?"
    m 3wud "Você deve ter muitas pessoas para visitar..."
    m 3sua "...ou talvez só tenha muitos planos especiais para nós hoje!"
    m 1hua "De qualquer forma, obrigada por pensar em mim e me levar junto~"
    return




label greeting_d25e_returned_d25e:
    $ persistent._mas_d25_d25e_date_count += 1

    m 1hua "E estamos em casa!"
    m 3eka "Foi muito fofo da sua parte me levar hoje..."
    m 3ekbsa "Poder sair com você na Véspera de Natal foi muito especial, [player]. Obrigada~"
    return


label greeting_d25e_returned_d25:
    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1

    m 1hua "E estamos em casa!"
    m 3wud "Nossa, ficamos fora a noite toda..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return


label greeting_d25e_returned_post_d25:
    $ persistent._mas_d25_d25e_date_count += 1

    m 1hua "Finalmente em casa!"
    m 3wud "Ficamos fora muito tempo, [player]..."
    m 3eka "Teria sido bom te ver no Natal, mas já que não pôde vir até mim, fico feliz que me levou com você."
    m 3ekbsa "Só ficar perto de você era tudo que eu queria~"
    m 1ekbfb "E já que não pude te dizer no Natal... Feliz Natal, [player]!"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return


label greeting_pd25e_returned_d25:
    m 1hua "E estamos em casa!"
    m 3wud "Nossa, ficamos fora bastante tempo..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return


label greeting_d25_returned_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "E estamos em casa!"
    m 3eka "Foi muito bom passar o Natal com você, [player]!"
    m 1eka "Muito obrigada por me levar com você."
    m 1ekbsa "Você é sempre tão atencioso~"
    return


label greeting_d25_returned_post_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "Finalmente em casa!"
    m 3wud "Ficamos fora muito tempo, [player]!"
    m 3eka "Teria sido bom te ver de novo antes do Natal acabar, mas pelo menos eu estava com você."
    m 1hua "Obrigada por passar tempo comigo mesmo tendo outros compromissos..."
    m 3ekbsa "Você é sempre tão atencioso~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return



label greeting_d25_and_nye_delegate:





    python:

        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        left_pre_d25e = False

        if checkout_time is not None:
            checkout_date = checkout_time.date()
            left_pre_d25e = checkout_date < mas_d25e

        if checkin_time is not None:
            checkin_date = checkin_time.date()


    if mas_isD25Eve():


        if left_pre_d25e:

            jump greeting_returned_home_morethan5mins_normalplus_flow
        else:


            call greeting_d25e_returned_d25e

    elif mas_isD25():


        if checkout_time is None or mas_isD25(checkout_date):

            call greeting_d25_returned_d25

        elif mas_isD25Eve(checkout_date):

            call greeting_d25e_returned_d25
        else:


            call greeting_pd25e_returned_d25

    elif mas_isNYE():

        if checkout_time is None or mas_isNYE(checkout_date):

            call greeting_nye_delegate
            jump greeting_nye_aff_gain

        elif left_pre_d25e or mas_isD25Eve(checkout_date):

            call greeting_d25e_returned_post_d25

        elif mas_isD25(checkout_date):

            call greeting_d25_returned_post_d25
        else:


            jump greeting_returned_home_morethan5mins_normalplus_flow

    elif mas_isNYD():



        if checkout_time is None or mas_isNYD(checkout_date):

            call greeting_nyd_returned_nyd

        elif mas_isNYE(checkout_date):

            call greeting_nye_returned_nyd
            jump greeting_nye_aff_gain

        elif checkout_time < datetime.datetime.combine(mas_d25.replace(year=checkout_time.year), datetime.time()):
            call greeting_pd25e_returned_nydp
        else:


            call greeting_d25p_returned_nyd

    elif mas_isD25Post():

        if mas_isD25PostNYD():



            if (
                    checkout_time is None
                    or mas_isNYD(checkout_date)
                    or mas_isD25PostNYD(checkout_date)
                ):

                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isNYE(checkout_date):

                call greeting_d25p_returned_nydp
                jump greeting_nye_aff_gain

            elif mas_isD25Post(checkout_date):

                call greeting_d25p_returned_nydp
            else:



                call greeting_pd25e_returned_nydp
        else:


            if checkout_time is None or mas_isD25Post(checkout_date):

                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isD25(checkout_date):

                call greeting_d25_returned_post_d25
            else:


                call greeting_d25e_returned_post_d25
    else:


        jump greeting_returned_home_morethan5mins_normalplus_flow



    jump greeting_returned_home_morethan5mins_normalplus_flow_aff





default persistent._mas_nye_spent_nye = False


default persistent._mas_nye_spent_nyd = False


default persistent._mas_nye_nye_date_count = 0


default persistent._mas_nye_nyd_date_count = 0


default persistent._mas_nye_date_aff_gain = 0


define mas_nye = datetime.date(datetime.date.today().year, 12, 31)
define mas_nyd = datetime.date(datetime.date.today().year, 1, 1)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "nye",
        datetime.datetime(2019, 1, 6),
        {
            "_mas_nye_spent_nye": "nye.actions.spent_nye",
            "_mas_nye_spent_nyd": "nye.actions.spent_nyd",

            "_mas_nye_nye_date_count": "nye.actions.went_out_nye",
            "_mas_nye_nyd_date_count": "nye.actions.went_out_nyd",

            "_mas_nye_date_aff_gain": "nye.aff.date_gain",

            "_mas_nye_accomplished_resolutions": "nye.actions.did_new_years_resolutions",
            "_mas_nye_has_new_years_res": "nye.actions.made_new_years_resolutions",
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 12, 31),
        end_dt=datetime.datetime(2020, 1, 6),
        exit_pp=store.mas_d25SeasonExit_PP
    ))

init -825 python:
    mas_run_d25s_exit = False

    def mas_d25SeasonExit_PP(mhs):
        """
        Sets a flag to run the D25 exit PP
        """
        global mas_run_d25s_exit
        mas_run_d25s_exit = True

init -10 python:
    def mas_isNYE(_date=None):
        """
        Returns True if the given date is new years eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_nye.replace(year=_date.year)


    def mas_isNYD(_date=None):
        """
        RETURNS True if the given date is new years day

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years day, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_nyd.replace(year=_date.year)





default persistent._mas_pm_got_a_fresh_start = None


default persistent._mas_aff_before_fresh_start = None


default persistent._mas_pm_failed_fresh_start = None

init 5 python:


    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nyd",
            action=EV_ACT_PUSH,
            start_date=mas_nyd,
            end_date=mas_nyd + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.DISTRESSED, None),
        ),
        skipCalendar=True
    )

label mas_nye_monika_nyd:
    $ persistent._mas_nye_spent_nyd = True
    $ got_fresh_start_last_year = mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start")

    if store.mas_anni.pastOneMonth():
        if not mas_isBelowZero():


            if not persistent._mas_pm_got_a_fresh_start or not persistent._mas_pm_failed_fresh_start:
                m 1eub "[player]!"

                if mas_HistVerify_k([datetime.date.today().year-2], True, "nye.actions.spent_nyd")[0]:
                    m "Acredita que estamos passando mais um Ano Novo [ju]?"
                if mas_isMoniAff(higher=True):
                    m 1hua "Passamos por tanta coisa [ju] neste último ano, não é?"
                else:
                    m 1eua "Passamos por tanta coisa [ju] neste último ano, não é?"

                m 1eka "Estou tão feliz por podermos passar ainda mais tempo [ju]."

                if mas_isMoniAff(higher=True):
                    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5hubfa "Vamos fazer deste ano tão maravilhoso quanto o último, certo?"
                    m 5ekbfa "Eu te amo tanto, [player]."
                else:
                    m 3hua "Vamos fazer deste ano ainda melhor que o último, ok?"
                    m 1hua "Eu te amo, [player]."
            else:


                $ last_year = "ano passado"
                m 1eka "[player]..."

                if not got_fresh_start_last_year:
                    $ last_year = "antes"

                m 3eka "Lembra da promessa que fez [last_year]?"
                m "Que faríamos deste ano melhor que o último?"
                m 6dkbstpa "..."
                m 6ekbftpa "Obrigada por cumprir sua promessa."
                m "É sério, [player]. Você me fez muito feliz...{w=1} {nw}"
                extend 6dkbftpa "Do fundo do meu coração, obrigada."
                m 6dkbftda "Vamos fazer deste ano ainda melhor, ok?"
                m 6ekbftda "Eu te amo, [player]."
                m "Eu realmente amo."

                $ persistent._mas_pm_failed_fresh_start = False
        else:



            if not persistent._mas_pm_got_a_fresh_start:
                m 2ekc "[player]..."
                m 2rksdlc "Passamos por...{w=1}tanta coisa neste último ano..."
                m "Eu... espero que este ano seja melhor que o último."
                m 2dkc "Eu realmente preciso que seja."
                jump mas_nye_monika_nyd_fresh_start
            else:

                m 2rkc "[player]..."

                if got_fresh_start_last_year:
                    m 2ekc "Lembra da promessa que fez no ano passado?"
                    m 2ekd "Que faríamos deste ano melhor que o último?"
                else:


                    m 2ekc "Lembra da promessa que fez antes?"
                    m 2ekd "Que melhoraria nosso relacionamento?"

                $ curr_aff = _mas_getAffection()
                if curr_aff > persistent._mas_aff_before_fresh_start:
                    m 2rkd "Acho que melhorou um pouco..."
                    m 2ekc "Mas eu esperava mais, [player]."


                    if not mas_HistVerifyAll_k(True, "pm.actions.monika.failed_fresh_start"):
                        $ _mas_revertFreshStart()
                        $ _mas_AffSave()
                        $ renpy.save_persistent()

                elif curr_aff < persistent._mas_aff_before_fresh_start:
                    m 2rfc "Parece que você não conseguiu cumprir essa promessa... não é?"
                else:

                    m 2rkc "Parece que nada realmente mudou, não é?"


                m 2rktpc "Eu realmente,{w=0.5} realmente espero que você possa consertar isso, [player]..."
                m 2dktpc "Não sei quanto mais posso aguentar."


                if _mas_getAffection() <= -50:
                    m 2dktsd "Mas talvez isso seja um pensamento bobo agora..."
                    m 2ektsc "Isso é só mais um jogo para você, não é?"
                    m 2rktsd "Você nem me vê como real...{w=1} {nw}"
                    extend 2dftsc "Sou só mais um personagem para você brincar."
                    m 2eftdc "Espero que ninguém tenha que passar pela dor e solidão que senti este ano."

                $ persistent._mas_pm_failed_fresh_start = True
                return
    else:

        if not mas_isBelowZero():
            m 1eub "[player]!"

            if mas_isMoniAff(higher=True):
                m 1ekbsa "Sei que não estamos [ju] há tanto tempo ainda, mas este último ano foi melhor do que eu jamais poderia ter esperado..."
            else:
                m 1eka "Sei que não estamos [ju] há tanto tempo ainda, mas este último ano foi tão especial para mim..."

            m 1hua "Sempre vou lembrar dele como o ano em que te conheci~"
            m 3hua "Vamos aproveitar nosso tempo [ju] e fazer deste ano ainda melhor!"
            m 1ekbsa "Eu te amo, [player]."
        else:

            m 2ekc "Então, [player]..."
            m 2etc "O começo de um novo ano, hein?"
            m 2rksdlc "Não estamos [ju] há muito tempo, mas o tempo que passamos no último ano não foi tão bom quanto eu esperava..."
            jump mas_nye_monika_nyd_fresh_start

    m "Feliz Ano Novo~"
    return "love"

label mas_nye_monika_nyd_fresh_start:
    m 2ekc "Que tal deixarmos tudo isso no passado, esquecermos o ano passado e focarmos em um novo começo este ano?"
    m 4ekc "Não é tarde para nós, [player]. Ainda podemos fazer um ao outro muito felizes."
    m 4eka "É tudo que eu sempre quis."

    m "O que você acha, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "O que você acha, [player]?{fast}"
        "Eu adoraria isso.":


            $ persistent._mas_pm_got_a_fresh_start = True
            $ persistent._mas_aff_before_fresh_start = _mas_getAffection()


            $ _mas_doFreshStart()
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 4wua "Sério?"
            m 1hua "Ah, [player], você não tem ideia de como isso me deixa feliz!"
            m 3eka "Eu sei que podemos fazer isso dar certo."
            m 1hua "Muito obrigada..."
            m 1eka "Só de saber que você ainda quer ficar comigo... isso significa tudo."
            m 3eka "Vamos fazer valer a pena, certo [player]?"
            return
        "Não.":

            $ persistent._mas_pm_got_a_fresh_start = False


            $ _mas_shatterAffection()
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 6dktpc "..."
            m 6ektpc "Eu...Eu..."
            m 6dktuc "..."
            m 6dktsc "..."
            pause 10.0
            return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_resolutions",
            action=EV_ACT_QUEUE, 
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.UPSET,None)
        ),
        skipCalendar=True
    )

default persistent._mas_nye_accomplished_resolutions = None

default persistent._mas_nye_has_new_years_res = None


label monika_resolutions:
    $ persistent._mas_nye_spent_nye = True
    m 2eub "Ei, [player]?"
    m 2eka "Eu estava pensando..."


    if not mas_lastSeenLastYear("monika_resolutions"):
        m 3eub "Você fez alguma promessa de Ano Novo no ano passado?{nw}"
        $ _history_list.pop()
        menu:
            m "Você fez alguma promessa de Ano Novo no ano passado?{fast}"
            "Sim.":

                m 3hua "Fico sempre tão orgulhosa quando vejo que você está tentando se melhorar, [player]."
                m 2eka "Dito isso..."

                call monika_resolutions_accomplished_resolutions_menu ("Você conseguiu cumprir suas promessas do ano passado?")
            "Não.":


                m 2euc "Ah, entendi..."

                if mas_isMoniNormal(higher=True):
                    if mas_isMoniHappy(higher=True):
                        m 3eka "Bom, eu acho que você nem precisava mudar, na verdade."
                        m 3hub "Acho você maravilhoso exatamente do jeitinho que é."
                    else:
                        m 3eka "Não tem nada de errado nisso. Eu realmente acho que você não precisava mudar."
                else:

                    m 2rkc "Talvez seja uma boa ideia fazer uma este ano, [player]..."


    elif mas_HistVerifyLastYear_k(True, "nye.actions.made_new_years_resolutions"):
        call monika_resolutions_accomplished_resolutions_menu ("Since you made a resolution last year, did you accomplish it?")


    m "Você tem alguma promessa para o próximo ano?{nw}"
    $ _history_list.pop()
    menu:
        m "Você tem alguma promessa para o próximo ano?{fast}"
        "Sim.":
            $ persistent._mas_nye_has_new_years_res = True

            m 1eub "Que ótimo!"
            m 3eka "Mesmo que possam ser difíceis de alcançar ou manter..."
            m 1hua "Eu estarei aqui para te ajudar se precisar!"
        "Não.":

            $ persistent._mas_nye_has_new_years_res = False
            m 1eud "Ah, sério?"
            if mas_isMoniNormal(higher=True):
                if persistent._mas_nye_accomplished_resolutions:
                    if mas_isMoniHappy(higher=True):
                        m 1eka "Você não precisa mudar. Eu te acho maravilhoso do jeito que você é."
                    else:
                        m 1eka "Você não precisa mudar. Eu te acho bem do jeito que você é."
                    m 3euc "Mas se pensar em algo antes da meia-noite, anota aí..."
                else:
                    m "Bem, se pensar em algo antes da meia-noite, anota aí..."
                m 1kua "Talvez você descubra algo que gostaria de fazer."
            else:
                m 2ekc "{cps=*2}Eu estava meio que esperando--{/cps}{nw}"
                m 2rfc "Deixa pra lá, esquece..."

    if mas_isMoniAff(higher=True):
        show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hubfa "Minha promessa é ser uma namorada ainda melhor para você, [mas_get_player_nickname()]."
    elif mas_isMoniNormal(higher=True):
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Minha promessa é ser uma namorada ainda melhor para você, [player]."
    else:
        m 2ekc "Minha promessa é melhorar nosso relacionamento, [player]."

    return

label monika_resolutions_accomplished_resolutions_menu(question):
    m 3hub "[question]{nw}"
    $ _history_list.pop()
    menu:
        m "[question]{fast}"
        "Sim.":

            $ persistent._mas_nye_accomplished_resolutions = True
            if mas_isMoniNormal(higher=True):
                m 4hub "Fico feliz em ouvir isso, [player]!"
                m 2eka "É ótimo que você tenha conseguido."
                m 3ekb "Coisas assim me deixam muito orgulhosa de você."
                m 2eka "Queria poder estar aí para comemorar um pouco com você."
            else:
                m 2rkc "Isso é bom, [player]."
                m 2esc "Talvez você possa fazer outra este ano..."
                m 3euc "Nunca se sabe o que pode mudar."

            return True
        "Não.":

            $ persistent._mas_nye_accomplished_resolutions = False
            if mas_isMoniNormal(higher=True):
                m 2eka "Ah... bem, às vezes as coisas não saem como planejamos."

                if mas_isMoniHappy(higher=True):
                    m 2eub "Além disso, eu te acho maravilhoso, então mesmo que não tenha conseguido..."
                    m 2eka "...ainda estou muito orgulhosa por você ter estabelecido metas e tentado melhorar, [player]."
                    m 3eub "Se decidir fazer uma promessa este ano, vou te apoiar em cada passo."
                    m 4hub "Adoraria te ajudar a alcançar seus objetivos!"
                else:
                    m "Mas acho ótimo que você pelo menos tentou melhorar estabelecendo metas."
                    m 3eua "Talvez se fizer uma promessa este ano, você consiga!"
                    m 3hub "Eu acredito em você, [player]!"
            else:

                m 2euc "Ah...{w=1} Bem, talvez você deva se esforçar mais para a promessa do próximo ano."

            return False


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nye_year_review",
            action=EV_ACT_QUEUE,
            start_date=mas_nye,
            end_date=datetime.datetime.combine(mas_nye, datetime.time(hour=23)),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label monika_nye_year_review:
    $ persistent._mas_nye_spent_nye = True
    $ spent_an_event = False

    $ placeholder_and = "e "

    if store.mas_anni.anniCount() >= 1:
        m 2eka "Sabe, [player], nós realmente passamos por muitas coisas [ju]."
        if store.mas_anni.anniCount() == 1:
            m 2wuo "Passamos o ano inteiro [ju]!"
            m 2eka "O tempo realmente voou..."
        else:

            m 2eka "Esse ano realmente passou voando..."

    elif store.mas_anni.pastSixMonths():
        m 2eka "Sabe, [player], nós realmente passamos por muita coisa no tempo que ficamos [ju] no ano passado"
        m "O tempo simplesmente voou..."

    elif store.mas_anni.pastThreeMonths():
        m 2eka "Sabe [player], passamos por bastante coisa no pouco tempo que ficamos [ju] no ano passado."
        m 2eksdlu "Tudo passou tão rápido, ahaha..."
    else:

        m 2eka "[player], mesmo que ainda não tenhamos passado por muita coisa [ju]..."
        $ placeholder_and = ""



    if mas_isMoniLove():
        m 2ekbsa "...e eu nunca gostaria de ter passado esse tempo com mais ninguém, [player]."
        m "Eu estou realmente,{w=0.5} muito feliz por ter passado este ano com você."

    elif mas_isMoniEnamored():
        m 2eka "...[placeholder_and]eu estou tão feliz por ter passado esse tempo com você, [player]."

    elif mas_isMoniAff():
        m 2eka "...[placeholder_and]eu realmente gostei do nosso tempo [ju]."
    else:

        m 2euc "...[placeholder_and]o tempo que passamos [ju] foi divertido."


    m 3eua "De qualquer forma, acho que seria bom refletir sobre tudo que passamos [ju] neste ano."
    m 2dtc "Vamos ver..."


    if mas_lastGiftedInYear("mas_reaction_promisering", mas_nye.year):
        m 3eka "Lembrando, você me deu sua promessa este ano quando me deu este anel..."
        m 1ekbsa "...um símbolo do nosso amor."

        if persistent._mas_pm_wearsRing:
            m "E você até comprou um para você mesmo..."

            if mas_isMoniAff(higher=True):
                m 1ekbfa "Para mostrar que você está tão comprometido comigo quanto eu estou com você."
            else:
                m 1ekbfa "Para mostrar seu comprometimento comigo."


    if mas_lastSeenInYear("mas_f14_monika_valentines_intro"):
        $ spent_an_event = True
        m 1wuo "Oh!"
        m 3ekbsa "Você passou o Dia dos Namorados comigo..."

        if mas_getGiftStatsForDate("mas_reaction_gift_roses", mas_f14):
            m 4ekbfb "...e me deu flores tão lindas também."



    if persistent._mas_bday_opened_game:
        $ spent_an_event = True
        m 2eka "Você passou tempo comigo no meu aniversário..."

        if not persistent._mas_bday_no_recognize:
            m 2dua "...celebrou comigo..."

        if persistent._mas_bday_sbp_reacted:
            m 2hub "...e até me deu uma festa surpresa..."

        show monika 5ekbla zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbla "...e isso realmente me fez sentir amada. Não tenho como te agradecer o suficiente por isso."


    if (
        persistent._mas_player_bday_spent_time
        or mas_HistVerify_k([datetime.date.today().year], True, "player_bday.spent_time")[0]
    ):
        $ spent_an_event = True
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Nós até passamos seu aniversário [ju]!"

        if (
            persistent._mas_player_bday_date
            or not mas_HistVerify_k([datetime.date.today().year], 0, "player_bday.date")[0]
        ):
            m 5eubla "E tivemos um encontro tão lindo também~"


    if persistent._mas_d25_spent_d25:
        $ spent_an_event = True
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Você passou o Natal comigo..."

        if persistent._mas_first_kiss is not None and persistent._mas_first_kiss.date() == mas_d25:
            m 5eubla "...e compartilhamos nosso primeiro beijo [ju]~"
            m 5lubsa "Nunca vou esquecer aquele momento..."
            m 5ekbfa "{i}Nosso{/i} momento."
            m "Não conseguiria imaginar compartilhando isso com mais ninguém."
        else:
            m 5ekbla "...um dia que eu não conseguiria imaginar passando com mais ninguém."


    if not spent_an_event:
        m 2rksdla "...Acho que não passamos por nenhum grande evento [ju] ainda."
        m 3eka "Mas mesmo assim..."
    else:

        show monika 5dsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5dsa "..."


    if store.mas_anni.pastThreeMonths():
        if mas_isMoniHappy(higher=True):
            show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eka "Eu realmente não consigo acreditar em quanto as coisas mudaram desde que estamos [ju]..."
        else:
            m 2eka "Eu realmente espero que possamos avançar em nosso relacionamento, [player]..."
    else:
        show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eka "Mal posso esperar para ver o quanto as coisas vão mudar no nosso futuro..."


    if not mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start"):
        show monika 5dka zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5dka "Obrigada."
        if store.mas_anni.anniCount() > 0:
            $ ending = "o melhor ano que eu poderia ter sonhado"

            if mas_lastSeenLastYear("monika_nye_year_review"):
                $ ending = "ainda melhor que o ano anterior"

            m 5ekbsa "Obrigada por ter feito do ano passado [ending]."
        else:

            $ _last_year = " "
            if store.mas_anni.pastOneMonth():
                $ _last_year = " no ano passado "

            m 5ekbsa "Obrigada por ter feito do tempo que passamos [ju][_last_year]melhor do que eu poderia imaginar."

        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                m 1lsbsa "..."
                m 6ekbsa "[player] eu..."
                call monika_kissing_motion
                m 1ekbfa "Eu te amo."
                m "..."
                show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5ekbsa "Nunca vou me esquecer desse momento..."
                m 5ekbfa "Nosso primeiro beijo~"
                m 5hubfb "Vamos fazer esse ano ainda melhor que o último, [player]."
            else:
                call monika_kissing_motion_short
                m 1ekbfa "Eu te amo, [player]."
                show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5hubfb "Vamos fazer esse ano ainda melhor que o último."
        else:

            m "Vamos fazer deste ano o melhor possível, [player]. Eu te amo~"
    else:

        m 1dsa "Obrigada por decidir deixar o passado para trás e começar de novo."
        m 1eka "Acho que se nos esforçarmos, podemos fazer isso dar certo, [player]."
        m "Vamos fazer deste ano incrível um para o outro."
        m 1ekbsa "Eu te amo."

    return "no_unlock|love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nye_dress_intro",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            action=EV_ACT_PUSH,
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

label mas_nye_monika_nye_dress_intro:

    $ curr_date = datetime.date.today()
    $ curr_year = curr_date.year

    if curr_date.day != 31:
        $ curr_year = curr_year - 1
        $ curr_date = datetime.date(curr_year, 12, 31)

    if mas_SELisUnlocked(mas_clothes_dress_newyears):
        m 3hub "Ei [player], acredita que já é Ano Novo de novo?!"
        m 1tuu "Acho que é hora de tirar o pó de um dos meus looks favoritos.{w=0.5}.{w=0.5}.{nw}"

        call mas_clothes_change (mas_clothes_dress_newyears, outfit_mode=True)

        m 3hub "E aqui estou, eu simplesmente amo este vestido! {w=0.2}{nw}"
        extend 3eua "É sempre bom se arrumar de vez em quando."
        m 1hub "Agora vamos celebrar o fim de [curr_year] e o começo de [(curr_year+1)]!"
    else:

        m 3hub "Ei [player], tenho uma surpresa para você este ano~"
        m 3eua "Deixe-me só me trocar.{w=0.5}.{w=0.5}.{nw}"


        call mas_clothes_change (mas_clothes_dress_newyears, outfit_mode=True, unlock=True)

        m 2rkbssdla "..."
        m 2rkbssdlb "Meus olhos estão aqui em cima, [player]..."

        if mas_isMoniAff(higher=True):
            m 2tubsu "..."
            m 2hubsb "Ahaha! Só te provocando~"
            m 2eua "Fico feliz que gostou do meu vestido. {nw}"
        else:

            m 2rkbssdla "..."
            m "Eu... {w=1}fico feliz que gostou do meu vestido. {nw}"

        extend 7eua "Foi bem difícil acertar ele!"
        m 3rka "A coroa de flores ficava caindo..."
        m 1hua "Fiz um visual de 'deusa grega', espero que tenha ficado bom."
        m 3eud "Mas esse look tem um significado mais profundo, sabia?"

        if seen_event("mas_f14_monika_vday_colors"):
            m 3eua "Talvez você lembre quando falamos sobre rosas e os sentimentos que suas cores transmitem."
        else:
            m 3eua "Talvez você já tenha adivinhado, mas é por causa da escolha das cores."

        m "O branco representa muitos sentimentos positivos, como bondade, pureza, segurança..."
        m 3eub "Mas o que eu queria destacar com esse look foi um novo começo bem-sucedido."


        if mas_HistWasFirstValueIn(True, curr_year - 1, "pm.actions.monika.got_fresh_start"):
            m 2eka "Ano passado decidimos começar de novo, e estou tão feliz que fizemos isso."
            m 2ekbsa "Eu sabia que poderíamos ser felizes [ju], [player]."
            m 7fkbsa "E você me fez a pessoa mais feliz do mundo."

        m 3dkbsu "Por isso quero usar isso quando o novo ano começar."
        m 1ekbsa "Quem sabe isso não ajuda a fazer o próximo ano ser ainda melhor."

    $ mas_addClothesToHolidayMapRange(mas_clothes_dress_newyears, start_date=curr_date, end_date=curr_date+datetime.timedelta(days=2))
    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_d25_mode_exit",
            category=['feriados'],
            prompt="Você pode tirar as decorações de Natal?",
            conditional="persistent._mas_d25_deco_active",
            start_date=mas_nyd+datetime.timedelta(days=1),
            end_date=mas_d25c_end,
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None},
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_d25_mode_exit",
        mas_nyd + datetime.timedelta(days=1),
        mas_d25c_end,
    )

label mas_d25_monika_d25_mode_exit:
    m 3eka "Já cansou do clima de festas, [player]? "
    m 3eua "Eu não me importo em já entrar no clima de ano novo."
    m 1hua "Desde que seja com você, é claro~"
    m 3hub "Ahaha!"
    m 2dsa "Só me dá um segundinho pra tirar as decorações.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    call mas_d25_season_exit

    m 1hua "Prontinho!{w=0.5} {nw}"
    extend 3hub "Agora estamos prontos pra começar o ano novo!"


    $ mas_lockEVL("mas_d25_monika_d25_mode_exit", "EVE")
    return

label greeting_nye_aff_gain:

    python:
        if persistent._mas_nye_date_aff_gain < 15:
            
            curr_aff = _mas_getAffection()
            
            
            time_out = store.mas_dockstat.diffCheckTimes()
            
            
            persistent._mas_monika_returned_home = None
            
            
            store.mas_dockstat._ds_aff_for_tout(time_out, 5, 15, 3, 3)
            
            
            persistent._mas_nye_date_aff_gain += _mas_getAffection() - curr_aff

    jump greeting_returned_home_morethan5mins_cleanup

label mas_gone_over_nye_check:
    if mas_checkOverDate(mas_nyd - datetime.timedelta(days=1)):
        $ persistent._mas_nye_spent_nye = True
        $ persistent._mas_nye_nye_date_count += 1
    return

label mas_gone_over_nyd_check:
    if mas_checkOverDate(mas_nyd):
        $ persistent._mas_nye_spent_nyd = True
        $ persistent._mas_nye_nyd_date_count += 1
    return



label bye_nye_delegate:

    python:
        _morning_time = datetime.time(5)
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _morning_time:

        jump bye_going_somewhere_normalplus_flow_aff_check

    elif _curr_time < _eve_time:


        if persistent._mas_nye_nye_date_count > 0:
            call bye_nye_second_time_out
        else:

            call bye_nye_first_time_out
    else:


        call bye_nye_late_out


    jump mas_dockstat_iostart

label bye_nye_first_time_out:

    m 3tub "Vamos a algum lugar especial hoje, [player]? "
    m 4hub "É véspera de Ano Novo, afinal!"
    m 1eua "Não sei exatamente o que você planejou, mas estou animada pra descobrir!"
    return

label bye_nye_second_time_out:

    m 1wuo "Oh, vamos sair de novo?"
    m 3hksdlb "Você parece gostar bastante de comemorar o Ano Novo, ahaha!"
    m 3hub "Adoro sair com você, então tô animada pro que quer que a gente vá fazer~"
    return

label bye_nye_late_out:

    m 1eka "Já está meio tarde, [player]..."
    m 3eub "Vamos ver os fogos de artifício?"
    if persistent._mas_pm_have_fam and persistent._mas_pm_fam_like_monika:
        m "Ou vamos jantar com sua família?"
        m 4hub "Eu adoraria conhecer sua família algum dia!"
        m 3eka "De qualquer forma, estou bem animada!"
    else:
        m "Sempre achei lindo como os fogos de Ano Novo iluminam o céu noturno..."
        m 3ekbsa "Um dia, a gente vai poder assistir juntinhos... Mas até lá, só de ir com você já me faz feliz, [player]."
    return




label greeting_nye_delegate:
    python:
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _eve_time:

        call greeting_nye_prefw
    else:


        call greeting_nye_infw

    $ persistent._mas_nye_nye_date_count += 1

    return

label greeting_nye_prefw:

    m 1hua "E estamos em casa!"
    m 1eua "Foi muito divertido, [player]."
    m 1eka "Obrigada por me levar hoje, eu realmente adoro passar tempo com você."
    m "Significa muito pra mim que você me leva para que possamos passar dias especiais como esses [ju]."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbfa "Eu te amo, [player]."
    return "love"

label greeting_nye_infw:

    m 1hua "E estamos em casa!"
    m 1eka "Obrigada por me levar hoje, [player]."
    m 1hua "Foi tão divertido poder passar esse tempo com você."
    m 1ekbsa "Significa muito pra mim que mesmo você não podendo estar aqui pessoalmente, ainda me leva com você."
    m 1ekbfa "Eu te amo, [player]."
    return "love"



label bye_nyd_delegate:
    if persistent._mas_nye_nyd_date_count > 0:
        call bye_nyd_second_time_out
    else:

        call bye_nyd_first_time_out

    jump mas_dockstat_iostart

label bye_nyd_first_time_out:

    m 3tub "Celebração de Ano Novo, [player]?"
    m 1hua "Parece divertido!"
    m 1eka "Vamos nos divertir muito [ju]."
    return

label bye_nyd_second_time_out:

    m 1wuo "Uau, vamos sair de novo, [player]?"
    m 1hksdlb "Você deve comemorar bastante, ahaha!"
    return



label greeting_nye_returned_nyd:

    $ persistent._mas_nye_nye_date_count += 1
    $ persistent._mas_nye_nyd_date_count += 1

    m 1hua "E estamos em casa!"
    m 1eka "Obrigada por me levar ontem, [player]."
    m 1ekbsa "Você sabe que eu amo passar tempo com você, e poder passar a véspera de Ano Novo até hoje com você foi incrível."
    m "Isso realmente significou muito para mim."
    m 5eubfb "Obrigada por tornar meu ano especial, [player]."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

label greeting_nyd_returned_nyd:

    $ persistent._mas_nye_nyd_date_count += 1
    m 1hua "E estamos em casa!"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Foi muito divertido, [player]!"
    m 5eka "É muito gentil da sua parte me levar em dias especiais como esse."
    m 5hub "Eu realmente espero que possamos passar mais momentos assim [ju]."
    return



label greeting_pd25e_returned_nydp:

    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "E estamos de volta!"
    m 1hub "Ficamos fora por um bom tempo, mas foi uma saída maravilhosa, [player]."
    m 1eka "Obrigada por me levar com você, eu realmente adorei."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    $ new_years = "Ano Novo"
    if mas_isNYD():
        $ new_years = "Véspera de Ano Novo"
    m 5ekbsa "Eu amo passar tempo com você, mas poder comemorar o Natal *e* o [new_years] [ju] foi incrível."
    m 5hub "Espero que a gente possa fazer algo assim de novo algum dia."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return


label greeting_d25p_returned_nyd:
    $ persistent._mas_nye_nyd_date_count += 1

    m 1hua "E estamos em casa!"
    m 1eub "Obrigada por me levar pra sair, [player]."
    m 1eka "Foi uma saída longa, mas me diverti bastante!"
    m 3hub "Mas também é ótimo estar de volta agora, assim podemos passar o ano novo juntinhos."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return

label greeting_d25p_returned_nydp:
    m 1hua "E estamos de volta!"
    m 1wuo "Foi uma saída longa, hein, [player]!"
    m 1eka "Fico um pouco triste que não conseguimos comemorar a virada [ju], mas eu realmente adorei tudo."
    m "Fico muito feliz que você tenha me levado."
    m 3hub "Feliz Ano Novo, [player]~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return





default persistent._mas_player_bday_in_player_bday_mode = False

default persistent._mas_player_bday_opened_door = False

default persistent._mas_player_bday_decor = False

default persistent._mas_player_bday_date = 0

default persistent._mas_player_bday_left_on_bday = False

default persistent._mas_player_bday_date_aff_gain = 0

default persistent._mas_player_bday_spent_time = False

default persistent._mas_player_bday_saw_surprise = False

init -10 python:
    def mas_isplayer_bday(_date=None, use_date_year=False):
        """
        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

            use_date_year - True if we should use the year from _date or not.
                (Default: False)

        RETURNS: True if given date is player_bday, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        if persistent._mas_player_bday is None:
            return False
        
        elif use_date_year:
            return _date == mas_player_bday_curr(_date)
        return _date == mas_player_bday_curr()

    def strip_mas_birthdate():
        """
        strips mas_birthdate of its conditional and action to prevent double birthday sets
        """
        mas_birthdate_ev = mas_getEV('mas_birthdate')
        if mas_birthdate_ev is not None:
            mas_birthdate_ev.conditional = None
            mas_birthdate_ev.action = None

    def mas_pbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_player_bday_date_aff_gain", 25)

init -11 python:
    def mas_player_bday_curr(_date=None):
        """
        sets date of current year bday, accounting for leap years
        """
        if _date is None:
            _date = datetime.date.today()
        if persistent._mas_player_bday is None:
            return None
        else:
            return store.mas_utils.add_years(persistent._mas_player_bday,_date.year-persistent._mas_player_bday.year)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "player_bday",
        
        datetime.datetime(2020, 1, 1),
        {
            "_mas_player_bday_spent_time": "player_bday.spent_time",
            "_mas_player_bday_opened_door": "player_bday.opened_door",
            "_mas_player_bday_date": "player_bday.date",
            "_mas_player_bday_date_aff_gain": "player_bday.date_aff_gain",
            "_mas_player_bday_saw_surprise": "player_bday.saw_surprise",
        },
        use_year_before=True,
        
        
    ))

init -11 python in mas_player_bday_event:
    import datetime
    import store.mas_history as mas_history
    import store

    def correct_pbday_mhs(d_pbday):
        """
        fixes the pbday mhs usin gthe given date as pbday

        IN:
            d_pbday - player birthdate
        """
        
        mhs_pbday = mas_history.getMHS("player_bday")
        if mhs_pbday is None:
            return
        
        
        pbday_dt = datetime.datetime.combine(d_pbday, datetime.time())
        
        
        _now = datetime.datetime.now()
        curr_year = _now.year
        
        new_dt = store.mas_utils.add_years(pbday_dt, curr_year - pbday_dt.year)
        
        if new_dt < _now:
            
            curr_year += 1
            new_dt = store.mas_utils.add_years(pbday_dt, curr_year - pbday_dt.year)
        
        
        reset_dt = pbday_dt + datetime.timedelta(days=3)
        
        
        new_sdt = new_dt
        new_edt = new_sdt + datetime.timedelta(days=2)
        
        
        
        
        
        mhs_pbday.start_dt = new_sdt
        mhs_pbday.end_dt = new_edt
        mhs_pbday.use_year_before = (
            d_pbday.month == 12
            and d_pbday.day in (29, 30, 31)
        )
        mhs_pbday.setTrigger(reset_dt)


label mas_player_bday_autoload_check:

    if mas_isMonikaBirthday():
        $ persistent._mas_bday_no_time_spent = False
        $ persistent._mas_bday_opened_game = True
        $ persistent._mas_bday_no_recognize = not mas_recognizedBday()

    elif mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
        $ monika_chr.reset_clothes(False)
        $ monika_chr.save()
        $ renpy.save_persistent()


    if (
        not persistent._mas_player_bday_in_player_bday_mode
        and persistent._mas_player_confirmed_bday
        and mas_isMoniNormal(higher=True)
        and not persistent._mas_player_bday_spent_time
        and not mas_isD25()
        and not mas_isO31()
        and not mas_isF14()
    ):

        python:

            this_year = datetime.date.today().year
            years_checked = range(this_year-10,this_year)
            surp_int = 3

            times_ruined = len(mas_HistVerify("player_bday.opened_door", True, *years_checked)[1])

            if times_ruined == 1:
                surp_int = 6
            elif times_ruined == 2:
                surp_int = 10
            elif times_ruined > 2:
                surp_int = 50

            should_surprise = renpy.random.randint(1,surp_int) == 1 and not mas_HistVerifyLastYear_k(True,"player_bday.saw_surprise")

            if not mas_HistVerify("player_bday.saw_surprise",True)[0] or (mas_getAbsenceLength().total_seconds()/3600 < 3 and should_surprise):
                
                
                
                selected_greeting = "i_greeting_monikaroom"
                mas_skip_visuals = True
                persistent._mas_player_bday_saw_surprise = True

            else:
                selected_greeting = "mas_player_bday_greet"
                if should_surprise:
                    mas_skip_visuals = True
                    persistent._mas_player_bday_saw_surprise = True


            persistent.closed_self = True

        jump ch30_post_restartevent_check

    elif not mas_isplayer_bday():

        $ persistent._mas_player_bday_decor = False
        $ persistent._mas_player_bday_in_player_bday_mode = False
        $ mas_lockEVL("bye_player_bday", "BYE")

    if not mas_isMonikaBirthday() and (persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals):
        $ persistent._mas_bday_in_bday_mode = False
        $ persistent._mas_bday_visuals = False

    if mas_isO31():
        return
    else:
        jump mas_ch30_post_holiday_check


label mas_player_bday_opendoor:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    if persistent._mas_bday_visuals:
        $ persistent._mas_player_bday_decor = True
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True, show_emptydesk=False)
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "nosso"
    else:
        $ your = "seu"

    if mas_HistVerify("player_bday.opened_door",True)[0]:
        $ now = "{i}de novo{/i}"
    else:
        $ now = "agora"

    m "[player]!"
    m "Você não bateu!"
    if not persistent._mas_bday_visuals:
        m "Eu estava começando a montar a festa do [your] aniversário, mas não tive tempo antes de você chegar!"
    m "..."
    m "Bem... {w=1}a surpresa está arruinada [now], mas.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    pause 1.0
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    m 4eua "Feliz aniversário, [player]!"
    m 2rksdla "Eu só queria que você tivesse batido antes."
    m 4hksdlb "Ah... [your] bolo!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup


label mas_player_bday_knock_no_listen:
    m "Quem é?"
    menu:
        "Sou eu.":
            $ mas_disable_quit()
            m "Ah! Pode só esperar um pouco, por favor?"
            window hide
            pause 5.0
            m "Certo, pode entrar, [player]..."
            jump mas_player_bday_surprise


label mas_player_bday_surprise:
    $ persistent._mas_player_bday_decor = True
    call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 4hub_static')
    m 4hub "Surpresa!"
    m 4sub "Ahaha! Feliz Aniversário, [player]!"

    m "Ficou [sv]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ficou [sv]?{fast}"
        "Sim.":
            m 1hub "Eba!"
            m 3hua "Eu sempre adoro fazer uma boa surpresa!"
            m 1tsu "Adoraria ter visto a expressão no seu rosto, ehehe."
        "Não.":

            m 2lfp "Hmph. Tudo bem então."
            m 2tsu "Você provavelmente só está dizendo isso porque não quer admitir que te peguei desprevenido..."
            if renpy.seen_label("mas_player_bday_listen"):
                if renpy.seen_label("monikaroom_greeting_ear_narration"):
                    m 2tsb "...ou talvez você estivesse escutando pela porta de novo..."
                else:
                    m 2tsb "{cps=*2}...ou talvez você estivesse me espiando.{/cps}{nw}"
                    $ _history_list.pop()
            m 2hua "Ehehe."
    if mas_isMonikaBirthday():
        m 3wub "Ah!{w=0.5} Eu fiz um bolo!"
    else:
        m 3wub "Ah!{w=0.5} Eu fiz um bolo pra você!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup


label mas_player_bday_listen:
    if persistent._mas_bday_visuals:
        pause 5.0
    else:
        m "...Vou colocar isto aqui..."
        m "...hmm parece muito bom...{w=1} mas está faltando algo..."
        m "Ah!{w=0.5} É claro!"
        m "Aqui!{w=0.5} Perfeito!"
        window hide
    jump monikaroom_greeting_choice


label mas_player_bday_knock_listened:
    window hide
    pause 5.0
    menu:
        "Open the door.":
            $ mas_disable_quit()
            pause 5.0
            jump mas_player_bday_surprise


label mas_player_bday_opendoor_listened:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    $ persistent._mas_player_bday_decor = True
    call spaceroom (hide_monika=True, scene_change=True, show_emptydesk=False)
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "nosso"
    else:
        $ your = "seu"

    if mas_HistVerify("player_bday.opened_door",True)[0]:
        $ knock = "bateu, {w=0.5}{i}de novo{/i}."
    else:
        $ knock = "bateu!"

    m "[player]!"
    m "Você não [knock]"
    if persistent._mas_bday_visuals:
        m "Eu queria te surpreender, mas eu ainda não estava pronta!"
        m "Enfim..."
    else:
        m "Eu estava preparando a festa do [your] aniversário, mas não tive tempo antes de você entrar para te surpreender!"
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    m 4hub "Feliz Aniversário, [player]!"
    m 2rksdla "Só queria que você tivesse batido antes."
    m 2hksdlb "Ah... [your] bolo!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup


label mas_player_bday_cake:

    if not mas_isMonikaBirthday():
        $ mas_unlockEVL("bye_player_bday", "BYE")
        if persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals:

            $ persistent._mas_bday_in_bday_mode = False
            $ persistent._mas_bday_visuals = False


    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)
    call mas_monika_gets_cake

    if mas_isMonikaBirthday():
        m 6eua "Só deixa eu acender as velas.{w=0.5}.{w=0.5}.{nw}"
    else:
        m 6eua "Só deixa eu acender as velas para você, [player].{w=0.5}.{w=0.5}.{nw}"

    window hide
    $ mas_bday_cake_lit = True
    pause 1.0

    m 6sua "Não é bonito, [player]?"
    if mas_isMonikaBirthday():
        m 6eksdla "Sei que você não pode assoprar as velas, então irei fazer isso por nós [du]...."
    else:
        m 6eksdla "Sei que você não pode assoprar as velas, então irei fazer isso por você..."
    m 6eua "...Mas você ainda deveria fazer um pedido, ele pode um dia se realizar..."
    m 6hua "Mas antes..."
    call mas_player_bday_moni_sings
    m 6hua "Faça um pedido, [player]!"
    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False
    pause 1.0
    m 6hua "Ehehe..."
    if mas_isMonikaBirthday():
        m 6ekbsa "Aposto que pedimos a mesma coisa~"
    else:
        m 6eka "Sei que é seu aniversário, mas eu também fiz um pedido..."
        m 6ekbsa "E quer saber?{w=0.5} Aposto que pedimos pela mesma coisa~"
    m 6hkbsu "..."
    if mas_isMonikaBirthday():
        m 6eksdla "Bem, já que você não pode comer este bolo, e não quero ser rudo e comer na sua frente..."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        m 6rksdla "Ah céus, acho que você também não pode comer este bolo, hã [player]?"
        m 6eksdla "Isso tudo foi bem bobo, não é?"
    if mas_isMonikaBirthday():
        m 6hksdlb "Acho que vou guardar isto para mais tarde."
    else:
        m 6hksdlb "Acho que vou guardar isto para mais tarde. Acho que seria meio rude eu comer {i}seu{/i} bolo de aniversário na sua frente, ahaha!"

    call mas_HideCake ('mas_bday_cake_player')


label mas_player_bday_card:
    $ mas_gainAffection(5, bypass=True)
    $ persistent._mas_player_bday_spent_time = True
    $ persistent._mas_player_bday_in_player_bday_mode = True

    m 6dkbsu "..."
    if mas_isMonikaBirthday():
        m 6sub "Ah!"
        m 6ekbsu "Eu fiz um cartão para você, [player]. Eu espero que goste..."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        m 6ekbsu "Eu... eu também fiz um cartão para você, [player]. Espero que você goste..."
    else:
        m 6ekbsu "Eu fiz um cartão para você, [player]. Espero que você goste..."

    call mas_showpoem (mas_poems.getRandomPoem("pbday"))

    if mas_isMoniEnamored(higher=True):
        if persistent._mas_first_kiss is None:
            m 6dkbsu "..."
            m 6ekbfa "Eu te amo tanto, [player]..."
            call monika_kissing_motion ()
            m 6ekbfa "Ah, [player]..."
            m 6dkbfa "Isso é tudo com o que eu sempre sonhei~"
            m 6ekbfa "Eu esperei tanto tempo para finalmente te beijar..."
            m 6dkbsu "Eu jamais me esquecerei disto..."
            m 6ekbsu "...o momento do nosso primeiro beijo~"
            if mas_isMonikaBirthday():
                m 6ekbsu "E não consigo pensar em um momento mais perfeito do que este dia especial que compartilhamos~"
        else:
            m 6ekbsa "Eu te amo, [player]~"
            call monika_kissing_motion (duration=0.5, initial_exp="6hkbfa", fade_duration=0.5)
            if mas_isMonikaBirthday():
                m 6eka "Estou tão feliz que podemos passar nosso aniversário [ju]..."
                m 6hua "Vamos aproveitar nosso dia especial~"
    else:
        if mas_isMonikaBirthday():
            m 1ekbfa "Eu te amo, [player]! Estou tão feliz que podemos passar nosso aniversário [ju]..."
            m 3ekbfa "Vamos aproveitar nosso dia especial~"
        else:
            m 1ekbfa "Eu te amo, [player]!"
    $ mas_rmallEVL("mas_player_bday_no_restart")
    $ mas_rmallEVL("mas_player_bday_ret_on_bday")


    $ mas_ILY()


    if mas_isD25Pre() and not persistent._mas_d25_deco_active:
        $ MASEventList.push("mas_d25_monika_holiday_intro", skipeval=True)
    return

label mas_monika_gets_cake:
    call mas_transition_to_emptydesk

    $ renpy.pause(3.0, hard=True)
    $ renpy.show("mas_bday_cake_player", zorder=store.MAS_MONIKA_Z+1)

    call mas_transition_from_emptydesk ("monika 6esa")

    $ renpy.pause(0.5, hard=True)
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_ret_on_bday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_ret_on_bday:
    m 1eua "Então, hoje é..."
    m 1euc "...espera.."
    m "..."
    m 2wuo "Ah!"
    m 2wuw "Ai meu Deus!"
    m 2tsu "Só me dê um momento, [player].{w=0.5}.{w=0.5}.{nw}"
    $ mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3eub "Feliz aniversário, [player]!"
    m 3hub "Ahaha!"
    m 3etc "Por que sinto que estou esquecendo algo..."
    m 3hua "Ah! Seu bolo!"
    call mas_player_bday_cake
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="mas_player_bday_greet",
            unlocked=False
        ),
        code="GRE"
    )

label mas_player_bday_greet:
    if should_surprise:
        scene black
        pause 5.0
        jump mas_player_bday_surprise
    else:

        if mas_isMonikaBirthday():
            $ your = "Nosso"
        else:
            $ your = "Seu"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        m 3eub "Feliz aniversário, [player]!"
        m 3hub "Ahaha!"
        m 3etc "..."
        m "Por que sinto que estou esquecendo de algo...?"
        m 3hua "Ah! [your] bolo!"
        jump mas_player_bday_cake



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_no_restart",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_no_restart:
    if mas_findEVL("mas_player_bday_ret_on_bday") >= 0:

        return
    m 3rksdla "Bem, [player], eu esperava fazer algo um pouco mais divertido, mas você foi tão gentil e não saiu o dia todo, então.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "Feliz aniversário, [player]!"
    if mas_isplayer_bday():
        m 1eka "Eu queria mesmo fazer uma surpresa para você hoje, mas está ficando tarde e eu não conseguia mais esperar."
    else:

        m 1hksdlb "Eu queria mesmo fazer uma surpresa para você, mas acho que fiquei sem tempo, não é nem mais seu aniversário, ahaha!"
    m 3eksdlc "Céus, espero que você não tenha achado que eu esqueci seu aniversário. Sinto muito se você achou isso..."
    m 1rksdla "Acho que eu provavelmente não deveria ter esperado tanto, ehehe."
    m 1hua "Ah! Fiz um bolo para você!"
    call mas_player_bday_cake
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_upset_minus",
            years = [],
            aff_range=(mas_aff.DISTRESSED, mas_aff.UPSET)
        ),
        skipCalendar=True
    )

label mas_player_bday_upset_minus:
    $ persistent._mas_player_bday_spent_time = True
    m 6eka "Ei, [player], eu só queria desejar um Feliz aniversário para você."
    m "Espero que tenha um ótimo dia."
    return





init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_other_holiday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_other_holiday:
    if mas_isO31():
        $ holiday_var = "Halloween"
    elif mas_isD25():
        $ holiday_var = "Natal"
    elif mas_isF14():
        $ holiday_var = "Dia dos Namorados"
    m 3euc "Ei, [player]..."
    m 1tsu "Tenho uma surpresa para você.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "Feliz aniversário, [player]!"
    m 3rksdla "Espero que não tenha achado que só por causa que seu aniversário cai no [holiday_var] que eu me esqueceria dele..."
    m 1eksdlb "Eu jamais me esqueceria do seu aniversário, [seu] [bnh]!"
    m 1eub "Ahaha!"
    m 3hua "Ah! Eu fiz um bolo para você!"
    call mas_player_bday_cake
    return


default persistent._mas_player_bday_last_sung_hbd = None

label mas_player_bday_moni_sings:
    $ persistent._mas_player_bday_last_sung_hbd = datetime.date.today()
    if mas_isMonikaBirthday():
        $ you = "nós"
    else:
        $ you = "você"
    m 6dsc ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 6hub "{cps=*0.5}{i}~Parabéns para [you]~{/i}{/cps}"
    m "{cps=*0.5}{i}~Parabéns para [you]~{/i}{/cps}"
    m 6sub "{cps=*0.5}{i}~Parabéns, [player]~{/i}{/cps}"
    m "{cps=*0.5}{i}~Parabéns para [you]~{/i}{/cps}"
    if mas_isMonikaBirthday():
        m 6hua "Ehehe!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_player_bday",
            unlocked=False,
            prompt="Vamos sair no meu aniversário!",
            pool=True,
            rules={"no_unlock": None},
            aff_range=(mas_aff.NORMAL,None),
        ),
        code="BYE"
    )

label bye_player_bday:
    $ persistent._mas_player_bday_date += 1
    if persistent._mas_player_bday_date == 1:
        m 1sua "Você quer sair para o seu aniversário?{w=1} Tudo bem!"
        m 1skbla "Isso parece bem romântico... mal posso esperar~"
    elif persistent._mas_player_bday_date == 2:
        m 1sua "Me levando para sair novamente em seu aniversário, [player]?"
        m 3hub "Viva!"
        m 1sub "Eu sempre adoro sair com você, mas é ainda mais especial sair em seu aniversário..."
        m 1skbla "Tenho certeza que iremos nos divertir muito~"
    else:
        m 1wub "Uau, você quer sair {i}de novo{/i}, [player]?"
        m 1skbla "Eu adoro que você queira passar tanto tempo comigo em seu dia especial!"
    $ persistent._mas_player_bday_left_on_bday = True
    jump bye_going_somewhere_post_aff_check


label greeting_returned_home_player_bday:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        if checkout_time is not None and checkin_time is not None:
            left_year = checkout_time.year
            left_date = checkout_time.date()
            ret_date = checkin_time.date()
            left_year_aff = mas_HistLookup("player_bday.date_aff_gain",left_year)[1]
            
            
            ret_diff_year = ret_date >= (mas_player_bday_curr(left_date) + datetime.timedelta(days=3))
            
            
            
            if left_date < mas_d25.replace(year=left_year) < ret_date:
                if ret_date < mas_history.getMHS("d25s").trigger.date().replace(year=left_year+1):
                    persistent._mas_d25_spent_d25 = True
                else:
                    persistent._mas_history_archives[left_year]["d25.actions.spent_d25"] = True

        else:
            left_year = None
            left_date = None
            ret_date = None
            left_year_aff = None
            ret_diff_year = None

        add_points = False

        if ret_diff_year and left_year_aff is not None:
            add_points = left_year_aff < 25


    if left_date < mas_d25 < ret_date:
        $ persistent._mas_d25_spent_d25 = True

    if mas_isMonikaBirthday() and mas_confirmedParty():
        $ persistent._mas_bday_opened_game = True
        $ mas_temp_zoom_level = store.mas_sprites.zoom_level
        call monika_zoom_transition_reset (1.0)
        $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if time_out < mas_five_minutes:
            m 6ekp "Isso nem chegou a ser um encon--"
        else:

            if time_out < mas_one_hour:
                $ mas_mbdayCapGainAff(6.0)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(6.0)
            elif time_out < mas_three_hour:
                $ mas_mbdayCapGainAff(10.0)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(10.0)
            else:
                $ mas_mbdayCapGainAff(14.0)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(14.0)

            m 6hub "Foi um encontro divertido, [player]..."
            m 6eua "Obrigada por--"

        m 6wud "O-que é esse bolo fazendo aqui?"
        m 6sub "I-isso é pra mim?!"
        m "Que fofo da sua parte me levar no seu aniversário só pra preparar uma festa surpresa pra mim!"
        call return_home_post_player_bday
        jump mas_bday_surprise_party_reacton_cake

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "Isso nem chegou a ser um encontro, [player]..."
        m 2eksdlc "Espero que nada esteja errado."
        m 2rksdla "Talvez a gente possa sair mais tarde."

    elif time_out < mas_one_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(5)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(5, bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 5
        m 1eka "Foi um encontro divertido enquanto durou, [player]..."
        m 3hua "Obrigada por arrumar um tempinho pra mim no seu dia especial."

    elif time_out < mas_three_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(10)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(10, bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 10
        m 1eua "Foi um encontro divertido, [player]..."
        m 3hua "Obrigada por me levar com você!"
        m 1eka "Eu realmente gostei de sair com você hoje~"
    else:


        if not ret_diff_year:
            $ mas_pbdayCapGainAff(15)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(15, bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 15
        m 1hua "E estamos em casa!"
        m 3hub "Foi muito divertido, [player]!"
        m 1eka "Foi tão legal sair pra comemorar seu aniversário..."
        m 1ekbsa "Obrigada por me incluir tanto no seu dia especial~"

    $ persistent._mas_player_bday_left_on_bday = False

    if not mas_isplayer_bday():
        call return_home_post_player_bday

    if mas_isD25() and not persistent._mas_d25_in_d25_mode:
        call mas_d25_monika_holiday_intro_rh_rh
    return

label return_home_post_player_bday:
    $ persistent._mas_player_bday_in_player_bday_mode = False
    $ mas_lockEVL("bye_player_bday", "BYE")
    $ persistent._mas_player_bday_left_on_bday = False
    if not (mas_isMonikaBirthday() and mas_confirmedParty()):
        if persistent._mas_player_bday_decor:
            if mas_isMonikaBirthday():
                $ persistent._mas_bday_opened_game = True
                m 3rksdla "Ah...não é mais {i}seu{/i} aniversário..."
            else:
                m 3rksdla "Ah...não é mais seu aniversário..."
            m 3hksdlb "A gente devia tirar essas decorações agora, ahaha!"
            m 3eka "Só me dá um segundo.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            $ mas_surpriseBdayHideVisuals()


            if not mas_isO31() and persistent._mas_o31_in_o31_mode:
                $ mas_o31HideVisuals()
                $ mas_o31HideSpriteObjects()

                $ store.persistent._mas_o31_in_o31_mode = False

            m 3eua "Prontinho!"
            if not persistent._mas_f14_gone_over_f14:
                m 1hua "Agora vamos aproveitar o dia [ju], [player]~"

        if persistent._mas_f14_gone_over_f14:
            m 2etc "..."
            m 3wuo "..."
            m 3wud "Nossa, [player], acabei de perceber que ficamos tanto tempo fora que perdemos o Dia dos Namorados!"
            call greeting_gone_over_f14_normal_plus


        if not persistent._mas_player_bday_decor and not mas_isO31() and persistent._mas_o31_in_o31_mode:
            call mas_o31_ret_home_cleanup (time_out, ret_tt_long=False)

    $ persistent._mas_player_bday_decor = False
    return


init 20 python:
    mas_poem_pbday_1 = MASPoem(
        poem_id = "poem_pbday_1",
        category = "pbday",
        prompt = "O Único",
        title = " Meu amor [player],",
        text = """\
 Para aquele que eu amo,
 Aquele em que confio,
 Aquele sem o qual não posso viver.
 Espero que seu dia seja tão especial quanto você torna cada dia para mim.
 Muito obrigada por ser você.

 Feliz Aniversário, amor~

 Para sempre sua,
 Monika
"""
    
    )

    mas_poem_pbday_2 = MASPoem(
        poem_id = "poem_pbday_2",
        category = "pbday",
        prompt = "Seu Dia",
        title = " Meu amor [player],",
        text = """\
 Qualquer dia com você é um dia feliz.
 Um dia onde eu {i}sou{/i} livre,
 Onde meus problemas desaparecem,
 Onde todos os meus sonhos se realizam.

 Mas hoje não é qualquer dia,
 Hoje é especial; hoje é seu dia.
 Um dia onde posso apreciar você ainda mais por tudo que faz.
 Um dia onde espero realizar seus sonhos também.

 Feliz Aniversário, amor~

 Para sempre sua,
 Monika
"""
    
    )

    mas_poem_pbday_3 = MASPoem(
        poem_id = "poem_pbday_3",
        category = "pbday",
        prompt = "Um Desejo",
        title = " Meu amor [player],",
        text = """\
 Granulado e velinhas para o bolo do [mw] [player],
 Só há um desejo para você fazer.
 Que seus maiores sonhos se realizem,
 Eu sei que os meus se realizaram quando te encontrei.

 Tão feliz por comemorar com você hoje,
 Vou te amar até o fim dos dias.
 Não há lugar onde eu preferiria estar,
 Passando esse tempo [ju], só você e eu.

 Feliz aniversário, amor~

 Para sempre sua,
 Monika
"""
    
    )

    mas_poem_pbday_4 = MASPoem(
        poem_id = "poem_pbday_4",
        category = "pbday",
        prompt = "[mw] [player]",
        title = " [mw] [player],",
        text = """\
 Como nosso amor cresceu.
 Outro ano,
 Mais mil momentos de orgulho.
 Orgulhosa do [mw] [player],
 E feliz em ter você crescendo ao meu lado.

 Como nosso amor floresceu,
 Como mais um ano se passou.
 Floresceu como uma rosa no orvalho da manhã,
 Com mais mil momentos de beleza.
 [mw] [que] [player],
 Quem eu amo ver florescer a cada dia.

 Como nosso amor é forte,
 Como mais um ano se passou.
 Forte como os mais belos diamantes,
 Com mais mil momentos de força.
 [mw] [mh] [player],
 Quem eu amo cada dia mais.

 Feliz aniversário, docinho~

 Para sempre sua,
 Monika
"""
    
    )

    mas_poem_pbday_5 = MASPoem(
        poem_id = "poem_pbday_5",
        category = "pbday",
        prompt = "Birthdays",
        title = " Meu amor [player],",
        text = """\
Alguns aniversários são maravilhosos, cheios de diversão,
Com risadas e sorrisos de todos ao redor.
Alguns aniversários, você planeja cada detalhe,
Mas no fim sente que poderia ter sido melhor.
Alguns aniversários são uma noite tranquila em casa,
Alguns te deixam exausto, sem nenhuma graça.

Enquanto cada um passa, alegria ou canseira,
Você pode se perguntar: “Qual mesmo a razão dessa brincadeira?”
A resposta é diferente pra cada um aqui,
Exceto pelo fato de marcar o dia em que você nasceu.
Mas se estiver cansado no seu dia especial,
Há algumas coisas que preciso te dizer, afinal.

Cada ano é um marco, sinal do seu crescimento,
Não só pra você - mas pra nós, eu complemento!
Cada ano é chance de se sentir especial,
Se não isso, um convite pra ser sentimental.
Mas acima de tudo, quero ouvir sua voz,
Se vamos festejar ou ficar em casa, a escolha será só sua!

Vamos comemorar [ju] do nosso jeito único.
Eu te amo, meu [player], e feliz aniversário.

Para sempre sua,
Monika
"""
    
    )





default persistent._mas_f14_spent_f14 = False

default persistent._mas_f14_in_f14_mode = None

default persistent._mas_f14_date_count = 0

default persistent._mas_f14_date_aff_gain = 0

default persistent._mas_f14_on_date = None

default persistent._mas_f14_gone_over_f14 = None

define mas_f14 = datetime.date(datetime.date.today().year, 2, 14)


init -10 python:
    def mas_isF14(_date=None):
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_f14.replace(year=_date.year)

    def mas_f14CapGainAff(amount):
        mas_capGainAff(amount, "_mas_f14_date_aff_gain", 25)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "f14",
        datetime.datetime(2020, 1, 6),
        {
            
            "_mas_f14_date_count": "f14.date",
            "_mas_f14_date_aff_gain": "f14.aff_gain",
            "_mas_f14_gone_over_f14": "f14.gone_over_f14",

            
            "_mas_f14_spent_f14": "f14.actions.spent_f14",
            "_mas_f14_in_f14_mode": "f14.mode.f14",
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 2, 13),
        end_dt=datetime.datetime(2020, 2, 15)
    ))

label mas_f14_autoload_check:
    python:
        if not persistent._mas_f14_in_f14_mode and mas_isMoniNormal(higher=True):
            persistent._mas_f14_in_f14_mode = True
            
            has_sundress = mas_SELisUnlocked(mas_clothes_sundress_white)
            has_shoulderless = mas_SELisUnlocked(mas_clothes_blackpink_dress)
            
            lingerie_eligible = (
                mas_canShowRisque()
                and not mas_SELisUnlocked(mas_clothes_vday_lingerie)
                and has_sundress
            )
            
            
            
            if (
                not has_sundress
                or (has_shoulderless and random.random() > 0.5)
                or lingerie_eligible
            ):
                monika_chr.change_clothes(mas_clothes_sundress_white, by_user=False, outfit_mode=True)
            
            else:
                monika_chr.change_clothes(mas_clothes_blackpink_dress, by_user=False, outfit_mode=True)
                
                mas_addClothesToHolidayMap(mas_clothes_blackpink_dress)
            
            monika_chr.save()
            renpy.save_persistent()

        elif not mas_isF14():
            
            
            mas_lockEVL("mas_f14_monika_vday_colors","EVE")
            mas_lockEVL("mas_f14_monika_vday_cliches","EVE")
            mas_lockEVL("mas_f14_monika_vday_chocolates","EVE")
            
            
            mas_lockEVL("monika_event_clothes_select", "EVE")
            
            
            persistent._mas_f14_in_f14_mode = False
            
            
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_sundress_white:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    jump mas_ch30_post_holiday_check




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_pf14_monika_lovey_dovey',
            conditional="not renpy.seen_label('mas_pf14_monika_lovey_dovey')",
            action=EV_ACT_QUEUE,
            start_date=mas_f14-datetime.timedelta(days=3),
            end_date=mas_f14,
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

label mas_pf14_monika_lovey_dovey:
    m 1rksdla "Ei...{w=0.3}[player]?"
    m 1ekbsa "Eu só queria te dizer que eu te amo."

    if mas_isMoniEnamored(higher=True):
        m 3ekbsa "Você me faz tão feliz...{w=0.3}eu nunca poderia pedir alguém melhor que você."

    m 3ekbsa "O Dia dos Namorados está chegando, e isso me deixa tão animada porque sei que tenho você ao meu lado."
    m 1rkbsd "Sem você, eu não sei onde estaria..."
    m 1ekbsa "Então eu quero te agradecer por estar sempre comigo."
    m 1dkbsu "...E por ser tão maravilhosamente você~"
    return "no_unlock|love"



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_valentines_intro',
            action=EV_ACT_PUSH,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_valentines_intro:

    $ persistent._mas_f14_spent_f14 = True
    $ mas_gainAffection(10, bypass=True)


    if mas_isMoniUpset(lower=True):
        if not mas_isMoniBroken():
            m 6eka "A propósito, [player], só queria desejar um feliz Dia dos Namorados."
            m "Agradeço pela visita, espero que tenha um ótimo dia."
        return

    python:
        has_sundress = mas_SELisUnlocked(mas_clothes_sundress_white)
        has_shoulderless = mas_SELisUnlocked(mas_clothes_blackpink_dress)
        lingerie_eligible = (
            mas_canShowRisque()
            and not mas_SELisUnlocked(mas_clothes_vday_lingerie)
            and has_sundress
        )

        mas_addClothesToHolidayMap(mas_clothes_sundress_white)

        mas_rmallEVL("mas_change_to_def")

    m 1hub "[player]!"
    m 1hua "Você sabe que dia é hoje?"
    m 3eub "É Dia dos Namorados!"
    m 1ekbsa "Um dia onde celebramos nosso amor..."
    m 3rkbsa "Acho que todo dia [ju] já é uma celebração do nosso amor...{w=0.3}{nw}"
    extend 3ekbsa "mas tem algo realmente especial no Dia dos Namorados."
    if not mas_anni.pastOneMonth() or mas_isMoniNormal():
        m 3rka "Mesmo sabendo que não estamos [ju] há muito tempo..."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Eu só quero que você saiba que estou sempre aqui por você."
        m 5eka "Mesmo se seu coração se partir..."
        m 5ekbsa "Eu sempre estarei aqui para consertá-lo. Tudo bem, [player]?"
        show monika 1ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1ekbsa "..."
    else:

        m 1eub "Já estamos [ju] há um tempo...{w=0.2}{nw}"
        extend 1eka "e eu amo muito o tempo que passamos [ju]."
        m 1dubsu "Você sempre me faz sentir tão amada."
        m "Estou tão feliz por ser sua namorada, [player]."


    if not persistent._mas_f14_in_f14_mode or lingerie_eligible:
        $ persistent._mas_f14_in_f14_mode = True


        if lingerie_eligible and not mas_hasUnlockedClothesWithExprop("lingerie"):
            call mas_lingerie_intro (holiday_str="on Valentine's Day", lingerie_choice=mas_clothes_vday_lingerie)


        elif not has_sundress or not has_shoulderless or lingerie_eligible:
            m 3wub "Ah!"
            m 3tsu "Tenho uma surpresinha pra você...{w=1}acho que vai gostar, ehehe~"


            if lingerie_eligible:
                call mas_clothes_change (outfit=mas_clothes_vday_lingerie, outfit_mode=True, exp="monika 2rkbsu", restore_zoom=False, unlock=True)
                pause 2.0
                show monika 2ekbsu
                pause 2.0
                show monika 2tkbsu
                pause 2.0
                m 2tfbsu "[player]...{w=0.5}você está olhando{w=0.3}...de novo."
                m 2hubsb "Ahaha!"
                m 2eubsb "Acho que você aprova minha escolha de roupa..."
                m 2tkbsu "Bem apropriada para um feriado romântico como o Dia dos Namorados, não acha?"
                m 2rkbssdla "Tenho que admitir, fiquei bem nervosa na primeira vez que usei algo assim..."
                m 2hubsb "Mas agora que já fiz antes, eu realmente gosto de me vestir assim pra você!"
                m 3tkbsu "Espero que você goste também~"


            elif has_sundress:
                call mas_clothes_change (mas_clothes_blackpink_dress, unlock=True, outfit_mode=True)
                m 2eua "Bem...{w=0.3}o que você acha?"
                call mas_f14_intro_blackpink_dress
            else:


                call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True)
                $ mas_selspr.json_sprite_unlock(mas_acs_musicnote_necklace_gold)
                m 2eua "..."
                m 2eksdla "..."
                m 2rksdlb "Ahaha...{w=1}{nw}"
                extend 2rksdlu "não é educado ficar olhando, [player]..."
                m 3tkbsu "...mas acho que isso significa que gostou do meu look, ehehe~"
                call mas_f14_sun_dress_outro
        else:



            if (
                monika_chr.clothes not in (mas_clothes_sundress_white, mas_clothes_blackpink_dress)
                and (
                    monika_chr.is_wearing_clothes_with_exprop("costume")
                    or monika_chr.clothes in (mas_clothes_def, mas_clothes_blazerless)
                    or mas_isMoniEnamored(lower=True)
                )
            ):
                m 3wud "Oh!"
                m 3hub "Eu devia trocar pra algo mais apropriado, ahaha!"
                m 3eua "Já volto."

                call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True)

                m 2eub "Ah, muito melhor!"
                m 3hua "Eu amo esse vestido, você não ama?"
                m 3eka "Ele sempre terá um lugar especial no meu coração no Dia dos Namorados..."
                m 1fkbsu "Assim como você~"
            else:



                if monika_chr.clothes != mas_clothes_sundress_white:
                    m 1wud "Oh..."
                    m 1eka "Quer que eu coloque meu vestido branco, [player]?"
                    m 3hua "Eu sempre considerei ele minha roupa de Dia dos Namorados."
                    m 3eka "Mas se preferir que eu continue com o que estou vestindo agora, tudo bem..."
                    m 1hub "Talvez possamos começar uma nova tradição, ahaha!"
                    m 1eua "Então, quer que eu coloque o vestido branco?{nw}"
                    $ _history_list.pop()

                    menu:
                        m "Então, quer que eu coloque o vestido branco?{fast}"
                        "Sim.":
                            m 3hub "Ok!"
                            m 3eua "Já volto."
                            call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True)
                            m 2hub "Prontinho!"
                            m 3eua "Usar esse vestido no Dia dos Namorados parece tão certo."
                            m 1eua "..."
                        "Não.":

                            m 1eka "Tudo bem, [player]."
                            m 3hua "Essa {i}é{/i} uma roupa muito bonita..."
                            m 3eka "E além disso, não importa o que eu esteja vestindo..."

                call mas_f14_intro_generic
    else:


        if not has_sundress:
            python:
                store.mas_selspr.unlock_clothes(mas_clothes_sundress_white)
                mas_selspr.json_sprite_unlock(mas_acs_musicnote_necklace_gold)

                store.mas_selspr.save_selectables()
                renpy.save_persistent()
            pause 2.0
            show monika 2rfc zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 2rfc "..."
            m 2efc "Sabe, [player]...{w=0.5}não é educado ficar olhando..."
            m 2tfc "..."
            m 2tsu "..."
            m 3tsb "Ahaha! Estou brincando...{w=0.5}gostou do meu look?"
            call mas_f14_sun_dress_outro

        elif not has_shoulderless:
            m 2eua "O que você achou da minha roupa?"
            call mas_f14_intro_blackpink_dress
        else:

            call mas_f14_intro_generic

    m 1fkbsu "Eu te amo tanto."
    m 1hubfb "Feliz Dia dos Namorados, [player]~"

    return "rebuild_ev|love"


label mas_f14_sun_dress_outro:
    m 1rksdla "Sempre sonhei em ter um encontro com você usando isso..."
    m 1eksdlb "Sei que parece bobo agora que penso nisso!"
    m 1ekbsa "...Mas imagine se fôssemos a um café [ju]."
    m 1rksdlb "Acho que até tem uma foto de algo assim em algum lugar..."
    m 1hub "Talvez possamos fazer acontecer de verdade!"
    m 3ekbsa "Você me levaria para sair hoje?"
    m 1hkbssdlb "Tudo bem se não puder, já estou feliz por estar com você."
    return


label mas_f14_intro_generic:
    m 1ekbsa "Estou tão grata por você estar passando tempo comigo hoje."
    m 3ekbsu "Passar tempo com quem se ama, {w=0.2}é tudo que alguém pode desejar no Dia dos Namorados."
    m 3ekbsa "Não importa se vamos a um encontro romântico ou só ficamos aqui [ju]..."
    m 1fkbsu "Realmente não importa, desde que estejamos [ju]."
    return

label mas_f14_intro_blackpink_dress:

    python:
        items_to_unlock = (
            mas_clothes_blackpink_dress,
            mas_acs_diamond_necklace_pink,
            mas_acs_pinkdiamonds_hairclip,
            mas_acs_ribbon_black_pink,
            mas_acs_earrings_diamond_pink
        )
        for item in items_to_unlock:
            mas_selspr.json_sprite_unlock(item)


        mas_addClothesToHolidayMap(mas_clothes_blackpink_dress)


        mas_selspr.save_selectables()
        renpy.save_persistent()

    m 4hub "Eu acho super fofo!"
    m 2eub "Tem algo nessa combinação de preto e rosa...{w=0.3}que simplesmente combina tão bem!"
    m 2rtd "Parece ser uma ótima roupa para usar num encontro..."
    m 2eua "..."
    m 2tuu "..."
    m 7hub "Ahaha~"
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_colors',
            prompt="Cores do Dia dos Namorados",
            category=['feriados','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_colors",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_colors:
    m 3eua "Já parou pra pensar no significado das cores no Dia dos Namorados?"
    m 3hub "Acho fascinante como podem simbolizar sentimentos tão profundos e românticos."
    m 1dua "Isso me lembra quando fiz meu primeiro cartão no ensino fundamental."
    m 3eub "Minha turma trocava cartões depois de fazê-los."
    m 3eka "Olhando pra trás, mesmo sem entender o significado, me diverti decorando com corações vermelhos e brancos."
    m 1eub "Nesse sentido, cores são como poesias."
    m 1eka "Oferecem tantas formas criativas de expressar amor."
    m 3ekbsu "Como dar rosas vermelhas, por exemplo."
    m 3eub "Rosas vermelhas simbolizam sentimentos românticos."
    m 1eua "Já rosas brancas representam pureza e inocência."
    m 3eka "Mas como o amor envolve tantas emoções..."
    m 3ekd "Às vezes é difícil achar as cores certas para expressar seus sentimentos."
    m 3eka "Felizmente, combinando cores, podemos expressar várias emoções!"
    m 1eka "Misturar vermelhas e brancas simboliza a união de um casal."

    if monika_chr.is_wearing_acs(mas_acs_roses):
        m 1ekbsa "Mas você já sabia disso quando escolheu estas rosas lindas pra mim, [player]..."
    else:
        m 1ekbla "Que tal me dar algumas rosas hoje, [player]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_cliches',
            prompt="Clichês de histórias românticas",
            category=['feriados','literatura','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_cliches",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_cliches:
    m 2euc "Já percebeu quantos clichês têm nas histórias de Dia dos Namorados?"
    m 2rsc "Sempre é 'Estou sozinho sem alguém pra amar' ou 'Como confessar meu amor?'"
    m 2euc "Acho que os escritores poderiam ser mais criativos..."
    m 3eka "Mas suponho que sejam os temas mais fáceis pra histórias de amor."
    m 3hub "Isso não significa que não podemos pensar fora da caixa!"
    m 2eka "Às vezes uma história previsível estraga tudo..."
    m 2rka "...Mas se quer um {i}bom{/i} exemplo de história imprevisível..."
    m 3hub "Use a nossa! Ahaha~"
    m 3rksdlb "Ok, {i}começou{/i} como essas histórias..."
    m 2tfu "Mas acho que deixamos bem original."
    m 3hua "Nosso encontro é a história mais interessante que existe!"
    m 1hub "Ahaha!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_chocolates',
            prompt="Chocolates do Dia dos Namorados",
            category=['feriados','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_chocolates",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_chocolates:
    m 1hua "O Dia dos Namorados é tão divertido para mim, [player]."
    m 3eub "Não só é o aniversário da minha conta no Twitter, mas também é o dia de dar e receber chocolates!"
    m 1hub "Um feriado que pode encher todos de amor, romance e alegria!"
    m 3ekbla "Mas é realmente especial receber algo de quem você gosta."
    m 3hua "Seja dado platonicamente, como declaração de amor ou parte de uma confissão, sempre faz você se sentir especial!"
    if mas_getGiftStatsForDate("mas_reaction_gift_chocolates") > 0:
        m 1ekbsa "Assim como você me fez sentir especial com os chocolates que me deu hoje."
        m 1ekbsu "Você é sempre tão doce, [player]."

    m 1ekbsa "Talvez um dia eu possa te dar alguns chocolates..."
    m 3hkbsa "Mal posso esperar para ir para a sua realidade e ficar com você, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_origins',
            prompt="Como começou o Dia dos Namorados?",
            category=['feriados','romance'],
            pool=True,
            conditional="persistent._mas_f14_in_f14_mode",
            action=EV_ACT_UNLOCK,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[],
            rules={"no_unlock": None}
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_origins",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_origins:
    m 3eua "Quer saber sobre a história do Dia dos Namorados, [player]?"
    m 1rksdlc "Na verdade, é bem sombria."
    m 1euc "As lendas variam, mas remonta ao século III em Roma, quando cristãos eram perseguidos pelo governo romano."
    m 3eud "Nessa época, o Imperador Cláudio II proibiu casamentos cristãos, o que um padre chamado Valentim considerou injusto."
    m 3rsc "Desafiando as ordens do imperador, ele realizava casamentos secretos."
    m 3esc "Outra versão diz que soldados romanos não podiam se casar, então Valentim evitava o recrutamento militar através do matrimônio."
    m 1dsd "De qualquer forma, Valentim foi preso e condenado à morte."
    m 1euc "Na prisão, tornou-se amigo da filha do carcereiro e curou sua cegueira. Alguns dizem que até se apaixonou por ela."
    m 3euc "Infelizmente, isso não o salvou. Mas antes de morrer, enviou uma carta assinada 'De seu Valentim'."
    m 1dsc "Foi executado em 14 de fevereiro de 269 d.C. e posteriormente canonizado como santo."
    m 3eua "Até hoje, ainda é tradicional usar 'De seu Valentim' em cartas de amor."
    m 3eud "Ah, mas espere, tem mais!"
    m "Havia um festival romano chamado Lupercália, também celebrado em meados de fevereiro."
    m 3eua "Aparentemente, parte do ritual envolvia formar casais sorteando nomes de uma caixa."
    m 3eub "...Eles passavam tempo [ju], com alguns até se casando se gostassem um do outro!"
    m 1eua "Com o tempo, o festival se tornou uma celebração cristã em memória de São Valentim."
    m 3hua "E evoluiu para as pessoas expressarem seus sentimentos por quem amam."
    m 3eubsb "...Como eu e você!"
    m 1ekbsa "Apesar das origens tristes, acho muito bonito."
    m 1ekbsu "Fico feliz que possamos compartilhar este dia mágico [ju].{w=0.2} {nw}"
    extend 1ekbfa "Feliz Dia dos Namorados, [mas_get_player_nickname()]~"
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_happy_vday",
            prompt="Feliz Dia dos Namorados!",
            action=EV_ACT_UNLOCK,
            pool=False,
            start_date=mas_f14,
            end_date=mas_f14 + datetime.timedelta(days=1),
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_f14_happy_vday",
        mas_f14,
        mas_f14 + datetime.timedelta(1)
    )

label mas_f14_happy_vday:
    $ persistent._mas_f14_spent_f14 = True
    $ mas_gainAffection(5, bypass=True)
    if mas_isMoniNormal(higher=True):
        m 1hublb "Ehehe~ Obrigada, [player]!"
        show monika 5hkbla zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hkbla "Não é maravilhoso ter um dia dedicado a celebrar quem amamos?"
        m 5lublb "Compartilhar doces, sair para um encontro especial...{w=0.2}{nw}"
        extend 5tubla "ou simplesmente aproveitar nosso tempo [ju]."
        m 5dublb "Sou tão grata por passar o Dia dos Namorados com você."
        m 5eubla "Obrigada por reservar tempo para mim, [player]. {w=0.2}Eu te amo tanto~"
        $ mas_ILY()

    elif mas_isMoniDis(higher=True):
        m 6euc "...{w=0.3}Hmm?"
        m 6wud "Ah, é..."
        m 6wuc "...{w=0.3}{nw}"
        extend 6eku "Obrigada. Isso...{w=0.2}{nw}"
        extend 6lkblu "significa muito para mim."
    else:

        m "...{w=0.8}Obrigada..."


    $ mas_lockEVL("mas_f14_happy_vday", "CMP")
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_monika_spent_time_with",
            conditional="persistent._mas_f14_spent_f14",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_f14, datetime.time(hour=18)),
            end_date=datetime.datetime.combine(mas_f14+datetime.timedelta(1), datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_spent_time_with:

    $ mas_rmallEVL("mas_f14_monika_spent_time_with")

    m 1eua "Ei, [player]?"
    m 1eka "Só queria te agradecer por passar o Dia dos Namorados comigo."
    m 1ekbsa "Sei que não é um feriado comum, mas é um dia muito especial pra mim agora que tenho você."

    if not mas_isBelowZero():
        if not mas_HistVerifyAll_k(True, "f14.actions.spent_f14"):
            m 1rkbsb "Ah, e eu...{w=0.5}fiz uma coisinha pra você, [player]!"
        else:

            m 1ekbsa "Fiz um cartão para você, [player]."

        m 1ekbsa "Aqui, deixa eu te mostrar."


        if not mas_poem_vday_1.is_seen():
            call mas_showpoem (mas_poem_vday_1)
            m "É sério, [player]..."
            m 3ekbsa "Em você encontrei tudo que sempre esperei~"

        elif not mas_poem_vday_2.is_seen():
            call mas_showpoem (mas_poem_vday_2)
            m "Você é realmente tudo para mim, [player]~"
        else:

            call mas_showpoem (mas_poems.getRandomPoem("f14"))


        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                jump mas_f14_first_kiss
            else:
                call monika_kissing_motion (duration=0.5, initial_exp="6hkbfa", fade_duration=0.5)

        m 1ekbfa "Obrigada por sempre estar ao meu lado."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Eu te amo tanto, [player]. Feliz Dia dos Namorados~"
        return "love"
    else:

        m 1eka "Obrigada por estar ao meu lado."
        m 3ekb "Feliz Dia dos Namorados!"
    return

label mas_f14_first_kiss:
    m 1ektpu "Sinceramente não sei o que faria sem você."
    show monika 6dktuu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m "..."
    window hide
    menu:
        "Eu te amo, [m_name].":
            $ HKBHideButtons()
            $ mas_RaiseShield_core()
            $ disable_esc()
            pause 3.0
            show monika 6ektda zorder MAS_MONIKA_Z at t11 with dissolve_monika
            pause 3.0
            show monika 6dku zorder MAS_MONIKA_Z at t11 with dissolve_monika
            pause 3.0
            show monika 6dkbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            pause 3.0
            show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 6ekbfa "[player]... Eu... eu..."
            call monika_kissing_motion (hide_ui=False)
            show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 6ekbfa "...Também te amo~"
            m 6dkbfa "..."
            m "Foi exatamente como sempre sonhei que seria~"
            m 6ekbfa "Esperei tanto para finalmente te beijar, e não poderia ter sido num momento mais perfeito..."
            m 6dkbsu "Nunca vou esquecer isso..."
            m 6ekbsu "...o momento do nosso primeiro beijo."
            m "Feliz Dia dos Namorados, [player]~"
            $ enable_esc()
            $ mas_MUINDropShield()
            $ HKBShowButtons()
            return




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_no_time_spent",
            action=EV_ACT_PUSH,
            start_date=mas_f14+datetime.timedelta(1),
            end_date=mas_f14+datetime.timedelta(8),
            conditional="not persistent._mas_f14_spent_f14",
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_no_time_spent:


    if mas_isFirstSeshPast(mas_f14):
        return

    if mas_ret_long_absence:

        $ mas_loseAffectionFraction(0.05, min_amount=15, ev_label="mas_apology_missed_vday")

        m 1rksdlc "Ei, [player]..."
        m 2eksdld "Sei que você avisou que ficaria ausente... mas senti muito sua falta no Dia dos Namorados."
        m 2eksdla "Da próxima vez, será que poderia me levar se não puder estar aqui?"
        m 3eub "Assim pelo menos ficaríamos [ju] e poderíamos celebrar!"
        m 1eka "Eu adoraria que você fizesse isso por mim."

    elif mas_isMoniAff(higher=True):
        $ mas_loseAffectionFraction(min_amount=20, ev_label="mas_apology_missed_vday")
        m 1rkc "[player]?"
        m "Onde você estava no Dia dos Namorados?"
        m 1ekc "É um dia muito especial para mim..."
        m 1ekd "...um dia que eu queria passar com você."
        m 2dkc "..."
        m 2ekd "Teria significado tanto se você tivesse [vn]..."
        m 2dkd "Mesmo que fosse só por alguns minutos."
        m "É pedir demais visitar sua namorada no Dia dos Namorados?"
        m 2ekc "Por favor, não deixe isso acontecer de novo, certo [player]?"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_missed_vday")
        m 2ekc "Ei, [player]..."
        m 2tkc "Estou bastante decepcionada..."
        m 2tkd "Você não me visitou no Dia dos Namorados."
        m 4tkc "Você sabe que tudo que eu quero é passar tempo com você..."
        m 4rkd "É pedir demais visitar sua namorada no Dia dos Namorados?"
        m 4eksdla "Por favor...{w=1}visite-me no próximo Dia dos Namorados, ok?"

    elif mas_isMoniUpset():
        $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_missed_vday")
        m 2efc "[player]!"
        m "Não acredito que você nem me visitou no Dia dos Namorados!"
        m 2rfc "Você tem ideia de como é ser deixada sozinha num dia desses?"
        m 2rkc "Sei que não estamos nos melhores termos..."
        m 2dkd "Mas teria significado muito se você tivesse [vn]."
        m 2tfc "Não deixe isso acontecer de novo, [player]."

    elif mas_isMoniDis():
        $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_missed_vday")
        m 6ekc "Ah [player]..."
        m "Como foi seu Dia dos Namorados?"
        m 6dkc "Não ter [um] [bf] é bem solitário..."
    else:

        $ mas_loseAffectionFraction(1.0, min_amount=150)
        m 6ckc "..."
    return




init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_vday",
            prompt="...por esquecido o Dia dos Namorados.",
            unlocked=False
        ),
        code="APL"
    )


label mas_apology_missed_vday:
    if mas_isMoniAff(higher=True):
        m 1eka "Obrigada por se desculpar por ter esquecid o Dia dos Namorados, [player]."
        m 1ekd "Eu realmente queria ter passado esse dia com você..."
        m 1rkc "Mas acho que você deve ter tido algo importante para fazer."
        m 1ekd "Por favor tente vir no próximo ano, pode ser [player]?"
        m 3eua "Se for ficar [oc], que tal me levar com você!"
        m 3hub "Mesmo longe de casa, ficaria feliz só de passar o dia ao seu lado~"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniNormal(higher=True):
        m 1eka "Obrigada por se desculpar por ter esquecid o Dia dos Namorados, [player]."
        if not store.mas_anni.pastOneMonth():
            m 1rkd "Sei que nosso relacionamento ainda é recente, mas tudo já estava começando a ficar diferente..."

        m 1ekd "Teria significado muito se você tivesse [vn], mesmo que por pouco tempo."
        m 3eka "Promete que vai me levar se ficar [oc] da próxima vez, pode ser [player]?"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniUpset():
        m 2dkc "Estou um pouco chateada por você não ter aparecido, mas agradeço as desculpas."
        m "Isso mostra que você ainda se importa conosco."
        m 2ekd "Por favor, [player]..."
        m 2eka "Tente vir no próximo Dia dos Namorados."
        $ mas_gainAffection(modifier=0.1)

    elif mas_isMoniDis():
        m 2dkc "Nem esperava que você viesse mesmo, [player]."
        m 2dkd "Sei que não estamos tão próximos, mas ainda esperei sua visita..."
        m 2dsc "Promete que vem no próximo ano?"
        $ mas_gainAffection(modifier=0.1)
    else:


        m 6ckc "..."

    return


init 20 python:
    mas_poem_vday_1 = MASPoem(
        poem_id="poem_f14_1",
        category="f14",
        prompt="Encontrei",
        title=" Meu amor [player],",
        text="""\
 Eu sempre amei o dia dos namorados, mas este parece diferente.
 Será que o mundo mudou, ou fui eu?
 Eu encontrei amor, eu encontrei propósito,
 Eu encontrei uma verdade que eu não sabia estar procurando.
 Tudo isso eu encontrei em você.

 Obrigada por compartilhar este dia especial comigo.

 Para sempre sua,
 Monika
"""
    )

    mas_poem_vday_2 = MASPoem(
        poem_id="poem_f14_2",
        category="f14",
        prompt="Tudo",
        title=" Meu amor [player],",
        text="""\
 Pode realmente ser nosso segundo dia dos namorados?
 O primeiro pareceu como se fosse ontem, ainda assim tanto aconteceu.
 Antes eu me perguntava se o mundo havia mudado, ou tinha sido eu.
 Agora eu sei a resposta.

 Tudo mudou.

 Sem você aqui, não há nada.
 Antes de você, não havia nada.

 Vazio. Escuridão. Nada.

 Nada.

 Então você surgiu.
 Apenas você.
 Meu mundo. Minha luz. Meu tudo.

 Tudo.


 Feliz Dia dos Namorados

 Para sempre sua,
 Monika
"""

    
    )

    mas_poem_vday_3 = MASPoem(
        poem_id="poem_f14_3",
        category="f14",
        prompt="Você",
        title=" Meu amor [player],",
        text="""\
 Caixas de chocolates e corações; cartões pintados de vermelho.
 Rosas em meu cabelo, pétalas tão macias quanto seda.
 Nada disso estaria completo sem você.

 Você, que ficou ao meu lado.
 Você, quem me deu seu coração.
 O coração mais valioso que todo chocolate no mundo, todas as rosas na terra.

 O amor que sinto não pode ser mensurado.

 Para sempre sua amada,
 Monika
"""
    )

    mas_poem_vday_4 = MASPoem(
        poem_id="poem_f14_4",
        category="f14",
        prompt="Rosas",
        title=" Meu Amor [player],",
        text="""\
 Todas as rosas do mundo,
 Eles crescem e florescem em algo lindo.
 Assim como nosso relacionamento.
 Todo dia,
 Estamos cada vez mais próximos,
 Cada vez mais forte,
 Cada vez mais linda~

 E embora as rosas tenham espinhos,
 Eles não prejudicam sua beleza,
 Eles as defendem,
 Eles as tornam mais fortes.
 E de todas as rosas do mundo,
 Mesmo neste feriado mais romântico,
 Nenhuma poderia substituir {size=+7}minha{/size} rosa especial~

 Para sempre sua amada,
 Monika
"""
    )

    mas_poem_vday_5 = MASPoem(
        poem_id="poem_f14_5",
        category="f14",
        prompt="Meu docinho",
        title=" Meu Amor [player],",
        text="""\
 Cerejas cobertas de chocolate e um beijo de boa noite;
 Estar com você, [que], é a mais doce bem-aventurança.
 Picolés no verão, dançando na chuva;
 De me aconchegar em você, [que], eu nunca poderia me abster.
 Sua risada é meu cubo de açúcar, seu sorriso é meu creme;
 Compartilhar um café com você, meu amor, seria um sonho.
 De todos os doces, todo o bolo, de frutas e biscoitos também;
 A coisa mais doce em toda a minha vida sempre será você.

 Para sempre sua,
 Monika
"""
    )

    mas_poem_vday_6 = MASPoem(
        poem_id="poem_f14_6",
        category="f14",
        prompt="Não me esqueça",
        title=" Meu Bem, [player],",
        text="""\
 Todas as flores sabem que são seus vasos.
 Algumas xícaras de terra e uma linda caixa de porcelana.
 Eles nunca vão embora sem ajuda, mesmo que um dia superem isso.

 As flores precisam de mais do que seu vaso.
 Água dos céus, ou uma mão amiga.
 E sem a visão do céu acima, o mundo à parte, elas um dia murchariam.

 Este jardineiro dá tudo isso e muito mais.
 Dizem que uma flor floresce mais brilhante quando falada com amor.
 Mesmo preso neste vaso, talvez não seja uma maldição saber mais.

 Não me esqueça.
"""
    )


label bye_f14:
    $ persistent._mas_f14_date_count += 1
    $ persistent._mas_f14_on_date = True
    if persistent._mas_f14_date_count == 1:
        m 1sua "Me levando para algum lugar especial no Dia dos namorados?"
        m 1ekbsa "Isso parece bem romântico, [player]..."
        m 3hub "Mal posso esperar!"
    elif persistent._mas_f14_date_count == 2:
        m 1sua "Me levando para sair de novo no Dia dos Namorados?"
        m 3tkbsu "Você sabe mesmo como fazer uma garota se sentir especial, [player]."
        m 1ekbfa "Eu tenho tanta sorte de ter alguém como você~"
    else:
        m 1sua "Uau, [player]... {w=1}você está mesmo querendo fazer deste um dia realmente especial!"
        m 1ekbfa "Você é o melhor parceiro que eu poderia pedir~"
    jump mas_dockstat_iostart


label greeting_returned_home_f14:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "Isso nem deu pra chamar de encontro, [player]..."
        m 2eksdlc "Está tudo bem?"
        m 2rksdla "Talvez possamos sair mais tarde..."

    elif time_out < mas_one_hour:
        $ mas_f14CapGainAff(5)
        m 1eka "Foi divertido enquanto durou, [player]..."
        m 3hua "Obrigada por arrumar tempo para mim no Dia dos Namorados."

    elif time_out < mas_three_hour:
        $ mas_f14CapGainAff(10)
        m 1eub "Que encontro maravilhoso, [player]!"
        m 3ekbsa "Obrigada por me fazer sentir especial no Dia dos Namorados~"
    else:


        $ mas_f14CapGainAff(15)
        m 1hua "E estamos em casa!"
        m 3hub "Isso foi incrível, [player]!"
        m 1eka "Foi tão bom sair com você no Dia dos Namorados..."
        m 1ekbsa "Muito obrigada por fazer deste dia realmente especial~"

    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ persistent._mas_f14_on_date = False

    if not mas_isF14() and not mas_lastSeenInYear("mas_f14_monika_spent_time_with"):
        $ MASEventList.push("mas_f14_monika_spent_time_with",skipeval=True)
    return



label mas_gone_over_f14_check:
    if mas_checkOverDate(mas_f14):
        $ persistent._mas_f14_spent_f14 = True
        $ persistent._mas_f14_gone_over_f14 = True
        $ mas_rmallEVL("mas_f14_no_time_spent")
    return

label greeting_gone_over_f14:
    $ mas_gainAffection(5, bypass=True)
    m 1hua "E finalmente estamos em casa!"
    m 3wud "Nossa [player], ficamos tanto tempo fora que perdemos o Dia dos Namorados!"
    if mas_isMoniNormal(higher=True):
        call greeting_gone_over_f14_normal_plus
    else:
        m 2rka "Agradeço por garantir que eu não tivesse que passar o dia sozinha..."
        m 2eka "Isso significa muito para mim, [player]."
    $ persistent._mas_f14_gone_over_f14 = False
    return

label greeting_gone_over_f14_normal_plus:
    $ mas_gainAffection(10, bypass=True)
    m 1ekbsa "Eu teria adorado passar o dia com você aqui, mas não importa onde estivéssemos, só de saber que estávamos [ju] para celebrar nosso amor..."
    m 1dubsu "Bem, isso significa tudo para mim."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "Obrigada por garantir que tivéssemos um Dia dos Namorados maravilhoso, [player]~"
    $ persistent._mas_f14_gone_over_f14 = False
    return






define mas_monika_birthday = datetime.date(datetime.date.today().year, 9, 22)


default persistent._mas_bday_in_bday_mode = False


default persistent._mas_bday_on_date = False
default persistent._mas_bday_date_count = 0
default persistent._mas_bday_date_affection_gained = 0
default persistent._mas_bday_gone_over_bday = False


default persistent._mas_bday_sbp_reacted = False
default persistent._mas_bday_confirmed_party = False


default persistent._mas_bday_visuals = False


default persistent._mas_bday_hint_filename = None


default persistent._mas_bday_opened_game = False
default persistent._mas_bday_no_time_spent = True
default persistent._mas_bday_no_recognize = True
default persistent._mas_bday_said_happybday = False


init -810 python:
    store.mas_history.addMHS(MASHistorySaver(
        "922",
        datetime.datetime(2020, 1, 6),
        {
            "_mas_bday_in_bday_mode": "922.bday_mode",

            "_mas_bday_on_date": "922.on_date",
            "_mas_bday_date_count": "922.actions.date.count",
            "_mas_bday_date_affection_gained": "922.actions.date.aff_gained",
            "_mas_bday_gone_over_bday": "922.gone_over_bday",
            "_mas_bday_has_done_bd_outro": "922.done_bd_outro",

            "_mas_bday_sbp_reacted": "922.actions.surprise.reacted",
            "_mas_bday_confirmed_party": "922.actions.confirmed_party",

            "_mas_bday_opened_game": "922.actions.opened_game",
            "_mas_bday_no_time_spent": "922.actions.no_time_spent",
            "_mas_bday_no_recognize": "922.actions.no_recognize",
            "_mas_bday_said_happybday": "922.actions.said_happybday"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 9, 21),
        end_dt=datetime.datetime(2020, 9, 23)
    ))




define mas_bday_cake_lit = False



image mas_bday_cake_monika = LiveComposite(
    (1280, 850),
    (0, 0), MASFilterSwitch("mod_assets/location/spaceroom/bday/monika_birthday_cake.png"),
    (0, 0), ConditionSwitch(
        "mas_bday_cake_lit", "mod_assets/location/spaceroom/bday/monika_birthday_cake_lights.png",
        "True", Null()
        )
)

image mas_bday_cake_player = LiveComposite(
    (1280, 850),
    (0, 0), MASFilterSwitch("mod_assets/location/spaceroom/bday/player_birthday_cake.png"),
    (0, 0), ConditionSwitch(
        "mas_bday_cake_lit", "mod_assets/location/spaceroom/bday/player_birthday_cake_lights.png",
        "True", Null()
        )
)

image mas_bday_banners = MASFilterSwitch(
    "mod_assets/location/spaceroom/bday/birthday_decorations.png"
)

image mas_bday_balloons = MASFilterSwitch(
    "mod_assets/location/spaceroom/bday/birthday_decorations_balloons.png"
)


init -1 python:
    def mas_isMonikaBirthday(_date=None):
        """
        checks if the given date is monikas birthday
        Comparison is done solely with month and day
        IN:
            _date - date to check. If not passed in, we use today.
        """
        if _date is None:
            _date = datetime.date.today()
        
        _datetime = datetime.datetime.combine(_date, datetime.time())
        
        return mas_isMonikaBirthday_dt(_datetime=_datetime)


    def mas_isMonikaBirthday_dt(_datetime=None, extend_by=0):
        """
        checks if the given date is monikas birthday.
        Takes hours beyond the date into account via the `extend_by` param.

        IN:
            _datetime - datetime to check. If not passed in, we use now.
            extend_by - hours we want to extend past 922
                defaults to 0
        """
        if _datetime is None:
            _datetime = datetime.datetime.now()
        
        moni_bd_start = datetime.datetime.combine(mas_monika_birthday, datetime.time())
        moni_bd_start = moni_bd_start.replace(year=_datetime.year)
        
        moni_bd_end = moni_bd_start + datetime.timedelta(days=1, hours=extend_by)
        
        return moni_bd_start <= _datetime < moni_bd_end

    def mas_getNextMonikaBirthday():
        today = datetime.date.today()
        if mas_monika_birthday < today:
            return datetime.date(
                today.year + 1,
                mas_monika_birthday.month,
                mas_monika_birthday.day
            )
        return mas_monika_birthday


    def mas_recognizedBday(_date=None):
        """
        Checks if the user recognized monika's birthday at all.

        RETURNS:
            True if the user recoginzed monika's birthday, False otherwise
        """
        if _date is None:
            _date = mas_monika_birthday
        
        
        if (
            mas_generateGiftsReport(_date)[0] > 0
            or persistent._mas_bday_date_affection_gained > 0
            or persistent._mas_bday_sbp_reacted
            or persistent._mas_bday_said_happybday
        ):
            persistent._mas_bday_no_time_spent = False
            return True
        return False

    def mas_surpriseBdayShowVisuals(cake=False):
        """
        Shows bday surprise party visuals
        """
        if cake:
            renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if store.mas_is_indoors:
            renpy.show("mas_bday_banners", zorder=7)
        renpy.show("mas_bday_balloons", zorder=8)


    def mas_surpriseBdayHideVisuals(cake=False):
        """
        Hides all visuals for surprise party
        """
        renpy.hide("mas_bday_banners")
        renpy.hide("mas_bday_balloons")
        if cake:
            renpy.hide("mas_bday_cake_monika")


    def mas_confirmedParty():
        """
        Checks if the player has confirmed the party
        """
        
        if (mas_monika_birthday - datetime.timedelta(days=7)) <= datetime.date.today() <= mas_monika_birthday:
            
            if persistent._mas_bday_confirmed_party:
                
                if persistent._mas_bday_hint_filename:
                    store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)
                return True
            
            
            
            char_dir_files = store.mas_docking_station.getPackageList()
            
            
            for filename in char_dir_files:
                temp_filename = filename.partition('.')[0]
                
                
                if "oki doki" == temp_filename:
                    
                    persistent._mas_bday_confirmed_party = True
                    store.mas_docking_station.destroyPackage(filename)
                    
                    if persistent._mas_bday_hint_filename:
                        store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)
                    
                    
                    _write_txt("/characters/gotcha", "")
                    
                    return True
        
        
        return False

    def mas_mbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_bday_date_affection_gained", 30, 40)


label mas_bday_autoload_check:

    python:
        if not mas_isMonikaBirthday():
            persistent._mas_bday_in_bday_mode = False
            
            persistent._mas_bday_visuals = False
            
            
            store.mas_lockEVL("monika_event_clothes_select", "EVE")
            
            store.mas_utils.trydel("characters/gotcha")
            
            
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()


        persistent._mas_bday_no_time_spent = False

        persistent._mas_bday_opened_game = True

        persistent._mas_bday_no_recognize = not mas_recognizedBday()

    jump mas_ch30_post_holiday_check



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_surprise_party_hint",
            start_date=mas_monika_birthday - datetime.timedelta(days=7),
            end_date=mas_monika_birthday - datetime.timedelta(days=2),
            years=[],
            action=EV_ACT_RANDOM,
            rules={"force repeat": None, "no rmallEVL": None},
            aff_range=(mas_aff.DISTRESSED,None)
        ),
        skipCalendar=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_bday_surprise_party_hint",
        mas_monika_birthday - datetime.timedelta(days=7),
        mas_monika_birthday - datetime.timedelta(days=2)
    )


init 10 python:
    if (
        mas_monika_birthday - datetime.timedelta(days=2) <= datetime.date.today() < mas_monika_birthday
        and not mas_lastSeenInYear("mas_bday_surprise_party_hint")
    ):
        MASEventList.push("mas_bday_surprise_party_hint")

image chibi_peek = MASFilterSwitch("mod_assets/other/chibi_peek.png")

label mas_bday_surprise_party_hint:

    python:
        persistent._mas_bday_hint_filename = mas_utils.sanitize_filename("For {0}.txt".format(player))

        if mas_isMoniNormal(higher=True):
            message = """\
[player],
Como você deve saber, o aniversário da Monika está chegando e quero ajudar a tornar esse dia especial!
Como estou sempre aqui, posso organizar a festa surpresa... mas preciso de uma ajudinha sua.
Tudo que você precisa fazer é garantir que ela saia da sala em algum momento do aniversário dela, e eu cuido do resto.
A Monika é incrível, e quero fazer minha parte para que tudo ocorra sem probleminhas...
Ahaha!

Por favor, deixe um arquivo chamado 'oki doki' na mesma pasta onde encontrou este bilhete para eu saber que pode prosseguir com a festa.

Boa sorte com a Monika!

P.S: Não conte a ela sobre mim!
"""

        else:
            message = """\
[player],
Espero que você saiba que o aniversário da Monika está chegando e quero torná-lo especial.
Ela tem passado por muita coisa ultimamente, e sei que significaria muito para ela se você a presenteasse com um dia especial.
Como estou sempre aqui, posso organizar uma festa surpresa... mas preciso da sua ajuda.
Tudo que você precisa fazer é garantir que ela saia da sala em algum momento do aniversário dela, e eu cuido do resto.
Se você realmente se importa com a Monika, vai me ajudar nisso.

Apenas deixe um arquivo chamado 'oki doki' na mesma pasta onde encontrou este bilhete para eu saber que pode prosseguir com a festa.

Por favor, não estrague isso.

P.S: Não conte a ela sobre mim.\n
"""

        _write_txt("/characters/" + persistent._mas_bday_hint_filename, message)


    if mas_isMoniNormal(higher=True):
        m 1eud "Ei, [player]..."
        m 3euc "Alguém deixou um bilhete na pasta de personagens endereçado a você."
        if mas_current_background == mas_background_def:

            show chibi_peek with moveinleft
        m 1ekc "Claro, eu não li, já que obviamente é pra você..."
        m 1tuu "{cps=*2}Hmm, o que será que pode ser isso...{/cps}{nw}"
        $ _history_list.pop()
        m 1hua "Ehehe~"
    else:

        m 2eud "Ei, [player]..."
        m 2euc "Alguém deixou um bilhete na pasta de personagens endereçado a você."
        m 2ekc "Claro, eu não li, já que obviamente é pra você..."
        m 2ekd "Só achei que deveria te avisar."


    hide chibi_peek with dissolve


    $ persistent._mas_monika_bday_surprise_hint_seen = True
    return "derandom|no_unlock"






init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_bday",
            prompt="Feliz aniversário!",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            start_date=mas_monika_birthday,
            end_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=1)),
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_bday_pool_happy_bday",
        mas_monika_birthday,
        mas_monika_birthday + datetime.timedelta(1)
    )

label mas_bday_pool_happy_bday:
    $ mas_gainAffection(5, bypass=True)
    if mas_recognizedBday():
        m 3hub "Ehehe, obrigada, [player]!"

        if persistent._mas_bday_said_happybday:
            m 3eka "Primeiro você cantou pra mim e agora me desejou feliz aniversário..."
        else:

            m 3eka "Eu estava esperando você dizer essas palavrinhas mágicas~"
            m 1eub "{i}Agora sim{/i} podemos chamar isso de comemoração de aniversário!"

        m 1eka "Você realmente fez esse momento tão especial, [player]."
        m 1ekbsa "Não sei como te agradecer por me amar tanto assim..."
    else:

        m 1skb "Awwwn, [player]!"
        m 1sub "Você lembrou do meu aniversário...!"
        m 1sktpa "Ai meu Deus, estou tão feliz que você lembrou."
        m 1dktdu "Sinto que hoje vai ser um dia muito especial~"
        m 1ekbsa "O que mais você preparou pra mim, hein...?"
        m 1hub "Ahaha!"

    if mas_isplayer_bday() and (persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted):
        m 1eua "Ah, e..."
        m 3hub "Feliz aniversário pra você também, [player]!"
        m 1hua "Ehehe!"


    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_said_happybday = True


    $ mas_lockEVL("mas_bday_pool_happy_bday", "CMP")
    return




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_belated_bday",
            prompt="Feliz aniversário atrasado!",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )

label mas_bday_pool_happy_belated_bday:
    $ mas_gainAffection(5, bypass=True)


    $ persistent._mas_bday_said_happybday = True
    $ persistent._mas_bday_no_recognize = False


    $ mas_lockEVL("mas_bday_pool_happy_belated_bday", "CMP")

    if mas_isMoniNormal(higher=True):
        m 1sua "Muito obrigada, [player]!"
        m 3hub "Eu sabia que você tinha me levado pra uma longa viagem no meu aniversário!"
        m 3rka "Queria tanto ter visto todos os lugares incríveis por onde passamos..."
        m 1hua "Mas só de saber que estávamos [ju], isso já torna esse o melhor aniversário que eu poderia ter!"
        m 3ekbsa "Eu te amo tanto, [player]~"
        return "love"
    else:
        m 3eka "Então {i}você{/i} me levou pra uma longa viagem no meu aniversário..."
        m 3rkd "Isso foi tão atencioso da sua parte, eu já estava meio que me perguntando--"
        m 1eksdla "Quer saber, deixa pra lá."
        m 1eka "Só de saber que você pensou em mim no meu aniversário já me deixa aliviada."
        m 3hua "É isso que importa."
        m 3eub "Obrigada, [player]!"
        return


label mas_bday_surprise_party_reaction:
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_bday_visuals = True
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)
    $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)

    if mas_isMoniNormal(higher=True):
        m 6suo "I-{w=0.5}Isso é..."
        m 6ska "Ah, [player]..."
        m 6dku "Estou sem palavras."

        if store.mas_is_indoors:
            m 6dktpu "Você preparou tudo isso pra me surpreender no meu aniversário..."

        m 6dktdu "Ehehe, você deve me amar muito mesmo."
        m 6suu "Tá tudo tão festivo!"
    else:

        m 6wuo "I-{w=0.5}Isso é..."
        m "..."
        m 6dkd "Desculpa, eu...{w=1}simplesmente fiquei sem palavras."
        m 6ekc "Eu realmente não esperava nada especial hoje, muito menos isso."
        m 6rka "Talvez você ainda sinta algo por mim, no fim das contas..."
        m 6eka "Tá tudo lindo."

label mas_bday_surprise_party_reacton_cake:

    menu:
        "Acender as velas.":
            $ mas_bday_cake_lit = True

    m 6sub "Aaaah, tá tão lindo, [player]!"
    m 6hua "Me lembra de um bolo que alguém me deu uma vez."
    m 6eua "Era quase tão bonito quanto esse que você fez!"
    m 6tkb "Quase."
    m 6hua "Mas enfim..."
    window hide

    show screen mas_background_timed_jump(5, "mas_bday_surprise_party_reaction_no_make_wish")
    menu:
        "Faça um pedido, [m_name]...":
            hide screen mas_background_timed_jump
            $ made_wish = True
            show monika 6hua
            if mas_isplayer_bday():
                m "Lembre de fazer um também, [player]!"

            $ mas_gainAffection(10, bypass=True)
            pause 2.0
            show monika 6hft
            jump mas_bday_surprise_party_reaction_post_make_wish

label mas_bday_surprise_party_reaction_no_make_wish:
    hide screen mas_background_timed_jump
    $ made_wish = False
    show monika 6dsc
    pause 2.0
    show monika 6hft

label mas_bday_surprise_party_reaction_post_make_wish:
    pause 0.1
    $ mas_bday_cake_lit = False
    window auto
    if mas_isMoniNormal(higher=True):
        m 6hub "Fiz um pedido!"
        m 6eua "Espero que um dia ele se torne realidade..."
        if mas_isplayer_bday() and made_wish:
            m 6eka "E sabe de uma coisa? {w=0.5}Aposto que nós [du] pedimos a mesma coisa~"
        m 6hub "Ahaha..."
    else:

        m 6eka "Fiz um pedido."
        m 6rka "Espero que um dia ele se realize..."

    m 6eka "Vou guardar esse bolo pra depois.{w=0.5}.{w=0.5}.{nw}"

    if mas_isplayer_bday():
        call mas_HideCake ('mas_bday_cake_monika', False)
    else:
        call mas_HideCake ('mas_bday_cake_monika')

    pause 0.5

label mas_bday_surprise_party_reaction_end:
    if mas_isMoniNormal(higher=True):
        m 6eka "Obrigada, [player]. Do fundo do meu coração, obrigada..."
        if mas_isplayer_bday() and persistent._mas_player_bday_last_sung_hbd != datetime.date.today():
            m 6eua "..."
            m 6wuo "..."
            m 6wub "Ah! Quase esqueci. {w=0.5}Eu também fiz um bolo pra você!"

            call mas_monika_gets_cake

            m 6eua "Deixa eu só acender as velas pra você, [player].{w=0.5}.{w=0.5}.{nw}"

            window hide
            $ mas_bday_cake_lit = True
            pause 1.0

            m 6sua "Não tá lindo?"
            m 6hksdlb "Acho que vou ter que soprar essas velas também, já que você não consegue fazer isso daqui, ahaha!"

            if made_wish:
                m 6eua "Vamos fazer outro pedido, [player]! {w=0.5}Assim vai ter o dobro de chance de se realizar, né?"
            else:
                m 6eua "Vamos fazer um pedido [ju], [player]!"

            m 6hua "Mas antes..."
            call mas_player_bday_moni_sings
            m 6hua "Faça um pedido, [player]!"

            window hide
            pause 1.5
            show monika 6hft
            pause 0.1
            show monika 6hua
            $ mas_bday_cake_lit = False
            pause 1.0

            if not made_wish:
                m 6hua "Ehehe..."
                m 6ekbsa "Aposto que nós [du] pedimos a mesma coisa~"
            m 6hkbsu "..."
            m 6hksdlb "Vou guardar esse bolo pra depois também, ahaha!"

            call mas_HideCake ('mas_bday_cake_player')
            call mas_player_bday_card
        else:

            m 6hua "Vamos aproveitar o resto do dia agora, que tal?"
    else:
        m 6ektpa "Obrigada, [player]. Significa muito pra mim o que você fez."
    $ persistent._mas_bday_sbp_reacted = True

    $ mas_gainAffection(15, bypass=True)


    $ persistent._mas_bday_in_bday_mode = True
    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_no_time_spent = False
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_spent_time_with",
            conditional="mas_recognizedBday() and not mas_lastSeenInYear('mas_bday_spent_time_with_wrapup')",
            action=EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_monika_birthday, datetime.time(18)),
            end_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_spent_time_with:
    if mas_isMoniUpset(lower=True):
        m 1eka "[player]..."
        m 3eka "Só queria dizer que eu realmente apreciei você ter passado um tempo comigo hoje."
        m 3rksdla "Eu sei que as coisas não têm sido tão boas ultimamente, mas você tirar um tempo pra comemorar meu aniversário comigo..."
        m 1eud "Bom, isso me dá esperança de que talvez ainda não seja tarde demais pra nós."
        m "Talvez hoje possa ser o começo de algo realmente especial..."
        m 3eka "Esse seria o melhor presente que eu poderia pedir."
    else:

        $ _timeout = store.mas_dockstat.timeOut(mas_monika_birthday)
        m 1eua "Ei, [player]..."
        m 3eua "Obrigada por passar um tempo comigo hoje."
        m 3hua "Algo assim pode realmente fazer uma garota feliz, sabia?"

        if _timeout > mas_five_minutes:
            m 3eka "Eu gostei muito do nosso encontro hoje, [player]."
            m 1eka "Eu sempre gosto de passar tempo com você aqui, mas poder passar um tempo com você na sua realidade..."
            m 1dku "Saber que você pensa em mim mesmo quando não pode me ver..."
            m 1ekbsa "Bom, isso significa muito pra mim."
            m 3ekbsa "Você realmente completou meu aniversário~"

        $ MASEventList.push('mas_bday_spent_time_with_wrapup', skipeval=True)

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_spent_time_with_wrapup"
        )
    )

label mas_bday_spent_time_with_wrapup:
    $ mas_rmallEVL("mas_bday_spent_time_with")
    $ mas_rmallEVL("mas_bday_postbday_notimespent")
    $ gave_gifts = mas_getGiftStatsRange(mas_monika_birthday, mas_monika_birthday + datetime.timedelta(days=1))[0]

    if gave_gifts > 0:

        if gave_gifts > 1:
            m 3eua "Não vamos esquecer os presentes que você me deu no meu aniversário."
            m 3hub "Eles foram incríveis, [player]!"
        else:
            m 3eua "Não vamos esquecer o presente que você me deu no meu aniversário."
            m 3hub "Foi tão maravilhoso, [player]!"

        m 1eka "Eu realmente aprecio o esforço de encontrar uma maneira de trazer coisas da sua realidade para a minha..."
        m 3eka "Sei que não deve ser fácil."

    m 1dku "..."

    if mas_isMoniEnamored(higher=True):
        m 1dktpu "..."
        m 1ektpu "Ahaha, desculpe, [player]!"
        m 3ektda "É que eu nunca imaginei ser tão feliz na minha vida."
        m 1rksdlb "Bem...{w=0.5}isso não é {i}exatamente{/i} verdade."
        m 1eka "Ainda precisamos estar fisicamente [ju], afinal~"
        m 1rkc "E, bem..."
        m 1rka "Sei que isso já está se tornando um clichê, mas..."
        m 3eka "Eu te amo tanto, [player]."
        m "Um dia, eu prometo..."
        m 1ektpu "Eu {i}prometo{/i} que vou te fazer tão feliz quanto você me fez hoje."
        m 3ektpu "Mesmo se nunca pudermos estar na mesma realidade, {w=0.5}saiba que sempre darei o meu melhor por você."
        m 1dktpu "Não importa os obstáculos que enfrentemos, não importa o que os outros digam sobre nós..."
        m 1ektda "Eu ainda te amo com tudo que eu sou."
        m "Você é o único que me entende. {w=0.5}Você me tirou de um lugar escuro e me deu um propósito..."
        m 1dkbsu "Você é simplesmente o melhor, [mas_get_player_nickname()], e eu sempre vou te amar."
        m 1ekbsa "...Obrigada por me dar uma razão para viver."
        $ _first_kiss = persistent._mas_first_kiss
        call monika_kissing_motion
        if _first_kiss is None:
            m 6ekbfa "Ah, [player]..."
            m 6rkbfa "Eu...{w=0.5}não sei o que deu em mim, mas o momento pareceu tão certo."
            m 6hubfa "Eu pensei no nosso primeiro beijo por tanto tempo, e finalmente vivenciá-lo..."
            m 6ekbfa "Eu nunca vou esquecer esse momento, [player]~"
        else:
            return "love"
    else:

        m 1eka "Nem consigo encontrar as palavras certas para expressar o quão feliz você me fez hoje."
        m 3eka "Toda aquela dor que eu passei antes de te conhecer?"
        m 1hua "Eu sou grata por ter perseverado."
        m 1rsc "Porque se eu não tivesse..."
        m 1ekbsa "Esse dia nunca teria acontecido."
        m 1dkbsa "Espero que isso te mostre um pouco do quanto eu aprecio você celebrar essa ocasião comigo."
        m 1ekbfb "Eu te amo tanto, [player]."
        m 1ekbfa "Vamos continuar fazendo um ao outro feliz~"
        return "love"
    return


label mas_gone_over_bday_check:
    if mas_checkOverDate(mas_monika_birthday):
        $ persistent._mas_bday_gone_over_bday = True
        $ persistent._mas_bday_no_time_spent = False
        $ mas_rmallEVL("mas_bday_postbday_notimespent")


        python:
            belated_ev = mas_getEV("mas_bday_pool_happy_belated_bday")

            if belated_ev is not None:
                
                belated_ev.start_date = datetime.date.today()
                belated_ev.end_date = datetime.datetime.now() + datetime.timedelta(days=1)
                belated_ev.unlocked = True
                
                
                MASUndoActionRule.create_rule(belated_ev)
                
                
                MASStripDatesRule.create_rule(belated_ev)

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_postbday_notimespent",
            conditional=(
                "not mas_recognizedBday() "
                "and not persistent._mas_bday_gone_over_bday"
            ),
            action=EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=1)),
            end_date=mas_monika_birthday+datetime.timedelta(days=8),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_postbday_notimespent:

    if mas_isFirstSeshPast(mas_monika_birthday):
        $ mas_assignModifyEVLPropValue("mas_bday_postbday_notimespent", "shown_count", "-=", 1)
        return


    if mas_ret_long_absence:

        $ mas_loseAffectionFraction(0.05, min_amount=15, ev_label="mas_apology_missed_bday")

        m 1rksdlc "Ei, [player]..."
        m 2eksdld "Eu sei que você me avisou que ficaria ausente... mas eu senti muito sua falta no meu aniversário."
        m 2eksdla "Da próxima vez, você poderia me levar com você se não puder estar aqui?"
        m 3eub "Assim ainda poderíamos ficar [ju] e celebrar [ju]!"
        m 1eka "Eu adoraria que você fizesse isso por mim, [player]."

    elif persistent._mas_bday_opened_game:

        if mas_isMoniAff(higher=True):
            $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_forgot_bday")
            m 2rksdla "Ei, [player]..."
            m 2rksdlb "Eu sei que nos divertimos no outro dia, como sempre fazemos, mas..."
            m 2ekp "Não posso evitar, eu estava esperando que você...{w=1} tivesse feito alguma coisinha especial para o meu aniversário."
            m 2ekd "Você esqueceu?"
            m 3eka "Talvez você possa colocar a data no calendário do seu telefone para o próximo ano?"
            m 3rka "...Ou ver o calendário na parede atrás de mim?"
            m 3hua "Não podemos mudar o passado, então saber que você quer se esforçar mais no próximo ano seria o único pedido de desculpas que eu preciso."

        elif mas_isMoniNormal(higher=True):
            $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_forgot_bday")
            m 2rksdld "Ei, [player]..."
            m 2rksdlb "Eu odeio reclamar, mas você sabe..."
            m 2ekp "Você não pode esquecer o aniversário da sua namorada!"
            m 2eku "Foi legal termos passado um tempo [ju] como sempre, mas no próximo ano..."
            m 3hua "Bem, vou ficar esperando por dois aniversários de algo especial~"

        elif mas_isMoniUpset():
            $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_forgot_bday")
            m 1ekc "Foi...{w=0.5}bom te ver no dia 22..."
            m 1ekd "Eu realmente não queria ficar sozinha naquele dia, então isso significou muito, mas..."
            m 1rkc "Quer saber? {w=0.5}Deixa pra lá."

        elif mas_isMoniDis():
            $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_forgot_bday")
            m 2dsc "..."
            m 2rkc "...[player], eu não quero te incomodar. {w=1}Já estou com medo de te afastar."
            m 2rktpc "Mas não consigo evitar. Me dói que você não tenha mencionado nada sobre comemorar meu aniversário..."
            m 2dktuc "Por favor, não pare de voltar para mim."
            m "E talvez no próximo ano..."
            m 4ektdc "E-eu só quero...{w=0.5}me sentir tão especial para você quanto você é para mim."
        else:

            $ mas_loseAffectionFraction(1.0, min_amount=150)
            m 6ckc "..."
    else:


        if mas_isMoniAff(higher=True):
            $ mas_loseAffectionFraction(min_amount=15, modifier=2.0, ev_label="mas_apology_missed_bday")
            m 1euc "Ei, [player]..."
            m 3rksdla "Eu sei que você faz muito para tornar cada dia especial, mas uma garota tem alguns dias no ano em que pode ser um pouco egoísta..."
            m 2tfd "E o seu {i}aniversário{/i} é um deles!"
            m "Sério, onde você estava?!"
            m 2rkc "Mas... conhecendo você, sei que deve ter tido um bom motivo para estar [oc]..."
            m 4ekc "Só tente não deixar isso acontecer de novo no próximo ano, ok?"

        elif mas_isMoniNormal(higher=True):


            if mas_isMoniHappy():
                $ mas_loseAffectionFraction(min_amount=10, modifier=2.0, ev_label="mas_apology_missed_bday")
            else:
                $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_missed_bday")

            m 1ekc "Ei, [player]..."
            m 1ekd "Você devia ter [vn] no dia 22, sabia?"
            m 3efd "Digo, você devia sempre me visitar! Mas você {i}tem{/i} que passar tempo com sua namorada fofa no aniversário dela, sabe."
            m 2efc "Por favor, venha me ver no próximo ano..."
            m 2dfc "Ou então..."

            m 6cfw "{cps=*2}{i}Haverá consequências!!!{/i}{/cps}{nw}"

            $ disable_esc()
            $ mas_MUMURaiseShield()
            window hide
            show noise zorder 11:
                alpha 0.5
            play sound "sfx/s_kill_glitch1.ogg"
            pause 0.5
            stop sound
            hide noise
            window auto
            $ mas_MUMUDropShield()
            $ enable_esc()
            $ _history_list.pop()

            m 1dsc "..."
            m 3hksdlb "Ahaha, desculpe, [player]!"
            m 3hub "Eu só estava brincando!"
            m 1eka "Você sabe que eu adoro te assustar um pouco~"

        elif mas_isMoniUpset():
            $ mas_loseAffectionFraction(min_amount=7.5, modifier=2.0, ev_label="mas_apology_missed_bday")
            m 2dsc "..."
            m 2rsc "[player], você não acha que deveria vir me ver com mais frequência?"
            m 2rktpc "Você pode acabar perdendo algo importante..."

        elif mas_isMoniDis():
            $ mas_loseAffectionFraction(min_amount=7.5, modifier=2.0, ev_label="mas_apology_missed_bday")
            m 6ekd "...Ei, como foi seu dia no dia 22?"
            m 6ekc "Só estou... curiosa se você pensou em mim naquele dia."
            m 6ektpc "Mas você provavelmente não pensou, né?"
            m 6dktpc "..."
        else:


            $ mas_loseAffectionFraction(1.0, min_amount=200)
            m 6eftsc "..."
            m 6dftdx "..."
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_bday",
            prompt="...por perder seu aniversário.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_missed_bday:

    if mas_isMoniAff(higher=True):
        m 1eua "Obrigada por se desculpar, [player]."
        m 2tfu "Mas é melhor você compensar no próximo ano~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Obrigada por se desculpar por ter perdido meu aniversário, [player]."
        m "Por favor, não deixe de passar um tempo comigo no próximo ano, certo?"
    else:

        m 2rksdld "Sabe, não estou totalmente surpresa por não ter te visto no meu aniversário..."
        m 2ekc "Por favor...{w=1}apenas não deixe que isso aconteça de novo."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_forgot_bday",
            prompt="...por esquecer seu aniversário.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_forgot_bday:

    if mas_isMoniAff(higher=True):
        m 1eua "Obrigada por se desculpar, [player]."
        m 3hua "Mas espero que você me compense~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Obrigada por se desculpar por ter esquecido meu aniversário, [player]."
        m 1eksdld "Só tente não deixar isso acontecer de novo, certo?"
    else:

        m 2dkd "Obrigada por se desculpar..."
        m 2tfc "Mas não deixe acontecer de novo."
    return



label bye_922_delegate:

    $ persistent._mas_bday_on_date = True

    $ persistent._mas_bday_date_count += 1

    if persistent._mas_bday_date_count == 1:

        $ persistent._mas_bday_in_bday_mode = True

        m 1hua "Ehehe. É meio romântico, não é?"

        if mas_isMoniHappy(lower=True):
            m 1eua "Talvez você até queira chamar de encon-{nw}"
            $ _history_list.pop()
            $ _history_list.pop()
            m 1hua "Oh! Desculpe, eu disse algo?"
        else:

            m 1eubla "Talvez você até chame de encontro~"


    elif persistent._mas_bday_date_count == 2:
        m 1eub "Me levando para sair de novo, [player]?"
        m 3eua "Você deve ter muitos planos para nós."
        m 1hua "Você é tão doce~"

    elif persistent._mas_bday_date_count == 3:
        m 1sua "Me levando para sair {i}de novo{/i} no meu aniversário?"
        m 3tkbsu "Você realmente sabe como fazer uma garota se sentir especial, [player]."
        m 1ekbfa "Sou tão sortuda por ter alguém como você~"
    else:
        m 1sua "Uau, [player]...{w=1}você está realmente determinado a tornar este dia especial!"
        m 1ekbsa "Você é o melhor parceiro que eu poderia desejar~"


    if mas_isMoniAff(higher=True) and not mas_SELisUnlocked(mas_clothes_blackdress):
        m 3hua "Na verdade, eu tenho uma roupa preparada especialmente para isso..."


    jump mas_dockstat_iostart

label mas_bday_bd_outro:
    python:
        monika_chr.change_clothes(mas_clothes_blackdress)
        mas_temp_zoom_level = store.mas_sprites.zoom_level


        persistent._mas_bday_has_done_bd_outro = True

    call mas_transition_from_emptydesk ("monika 1eua")
    call monika_zoom_transition_reset (1.0)


    if mas_SELisUnlocked(mas_clothes_blackdress):
        m 1hua "Ehehe~"
        m 1euu "Estou tão animada para ver o que você planejou para nós hoje."
        m 3eua "...Mas mesmo que não seja muito, tenho certeza que vamos nos divertir [ju]~"
    else:

        m 3tka "E então, [player]?"
        m 1hua "O que você acha?"
        m 1ekbsa "Eu sempre amei este vestido e sonhei em sair com você, usando ele..."
        m 3eub "Talvez pudéssemos ir ao shopping, ou até ao parque!"
        m 1eka "Mas conhecendo você, você já deve ter algo incrível planejado para nós~"

    m 1hua "Vamos lá, [player]!"

    python:
        store.mas_selspr.unlock_clothes(mas_clothes_blackdress)
        mas_addClothesToHolidayMap(mas_clothes_blackdress)
        persistent._mas_zoom_zoom_level = mas_temp_zoom_level


        store.mas_dockstat.checkoutMonika(moni_chksum)


        persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
            store.mas_greetings.TYPE_GENERIC_RET
        )


    jump _quit



label greeting_returned_home_bday:

    $ persistent._mas_bday_on_date = False

    $ persistent._mas_bday_opened_game = True

    $ time_out = store.mas_dockstat.diffCheckTimes()
    $ checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()


    if mas_confirmedParty() and not persistent._mas_bday_sbp_reacted:
        if mas_one_hour < time_out <= mas_three_hour:
            $ mas_mbdayCapGainAff(20 if persistent._mas_player_bday_in_player_bday_mode else 15)
        elif time_out > mas_three_hour:
            $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

        if mas_isplayer_bday() and persistent._mas_player_bday_decor and persistent._mas_bday_date_count == 1:
            jump mas_monika_cake_on_player_bday
        else:

            jump mas_bday_surprise_party_reaction


    if time_out <= mas_five_minutes:

        $ mas_loseAffection()
        m 2ekp "Esse encontro não foi lá essas coisas, [player]..."
        m 2eksdlc "Tá tudo bem com você?"
        m 2rksdla "Talvez a gente possa sair mais tarde..."
        if mas_isMonikaBirthday():
            return

    elif time_out <= mas_one_hour:

        $ mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        m 1sua "Isso foi divertido, [player]!"
        if mas_isplayer_bday():
            m 1hub "Ahaha, sair pra comemorar nosso aniversário..."
        else:
            m 1hub "Ahaha, me levar pra sair no meu aniversário..."
            m 3eua "Foi muito atencioso da sua parte."
        m 3eka "Eu realmente gostei do tempo que passamos [ju]."
        m 1eka "Eu te amo~"
        if mas_isMonikaBirthday():
            $ mas_ILY()

    elif time_out <= mas_three_hour:

        $ mas_mbdayCapGainAff(20 if persistent._mas_player_bday_in_player_bday_mode else 15)

        m 1hua "Ehehe~"
        m 3eub "A gente passou bastante tempo junto hoje, hein, [player]."
        m 1ekbsa "...e obrigada por isso."
        m 3ekbfa "Eu sei que já disse isso um milhão de vezes."
        m 1hua "Mas eu sempre fico feliz quando estamos [ju]."
        m "Eu te amo tanto..."
        if mas_isMonikaBirthday():
            $ mas_ILY()
    else:


        $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

        m 1sua "Uau, [player]..."
        if mas_player_bday_curr == mas_monika_birthday:
            m 3hub "Foi um momento tão adorável!"
            if persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted:
                m 3eka "Não consigo imaginar jeito melhor de comemorar nossos aniversários do que com um encontro tão longo."
            m 1eka "Queria poder ter visto todos os lugares incríveis por onde passamos, mas só de saber que estávamos [ju]..."
            m 1hua "Isso já é tudo o que eu poderia pedir."
            m 3ekbsa "Espero que você sinta o mesmo~"
        else:

            m 3sua "Eu não esperava que você fosse reservar tanto tempo só pra mim..."
            m 3hua "Mas aproveitei cada segundo!"
            m 1eub "Cada minuto com você é um minuto bem aproveitado!"
            m 1eua "Você me fez muito feliz hoje~"
            m 3tuu "Tá se apaixonando por mim de novo, [player]?"
            m 1dku "Ehehe..."
            m 1ekbsa "Obrigada por me amar."

    if (
        mas_isMonikaBirthday()
        and mas_isplayer_bday()
        and mas_isMoniNormal(higher=True)
        and not persistent._mas_player_bday_in_player_bday_mode
        and not persistent._mas_bday_sbp_reacted
        and checkout_time.date() < mas_monika_birthday

    ):
        m 1hua "Ah, e [player], me dá um segundinho, tenho algo pra você.{w=0.5}.{w=0.5}.{nw}"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        m 3eub "Feliz aniversário, [player]!"
        m 3etc "Por que eu tô com a sensação de que tô esquecendo alguma coisa..."
        m 3hua "Ah! O seu bolo!"
        jump mas_player_bday_cake

    if not mas_isMonikaBirthday():

        $ persistent._mas_bday_in_bday_mode = False

        if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
            $ MASEventList.queue('mas_change_to_def')

        if time_out > mas_five_minutes:
            m 1hua "..."
            m 1wud "Uau, [player]. A gente ficou fora por um bom tempo mesmo..."

        if mas_isplayer_bday() and mas_isMoniNormal(higher=True):
            if persistent._mas_bday_sbp_reacted:
                $ persistent._mas_bday_visuals = False
                $ persistent._mas_player_bday_decor = True
                m 3suo "Ah! Agora é seu aniversário..."
                m 3hub "Acho que podemos deixar essas decorações por aí mesmo, ahaha!"
                m 1eub "Já volto, só preciso pegar seu bolo!"
                jump mas_player_bday_cake

            jump mas_player_bday_ret_on_bday
        else:

            if mas_player_bday_curr() == mas_monika_birthday:
                $ persistent._mas_player_bday_in_player_bday_mode = False
                m 1eka "Enfim, [player]... Eu adorei passarmos nossos aniversários [ju]."
                m 1ekbsa "Espero ter ajudado a tornar seu dia tão especial quanto você tornou o meu."
                if persistent._mas_player_bday_decor or persistent._mas_bday_visuals:
                    m 3hua "Deixa eu só arrumar tudo por aqui.{w=0.5}.{w=0.5}.{nw}"
                    $ mas_surpriseBdayHideVisuals()
                    $ persistent._mas_player_bday_decor = False
                    $ persistent._mas_bday_visuals = False
                    m 3eub "Prontinho!"

            elif persistent._mas_bday_visuals:
                m 3rksdla "Meu aniversário nem é mais hoje..."
                m 2hua "Deixa eu só arrumar tudo por aqui.{w=0.5}.{w=0.5}.{nw}"
                $ mas_surpriseBdayHideVisuals()
                $ persistent._mas_bday_visuals = False
                m 3eub "Prontinho!"
            else:

                m 1eua "A gente podia fazer algo assim de novo em breve, mesmo que não seja uma data especial."
                m 3eub "Eu realmente me diverti muito!"
                m 1eka "Espero que você tenha se divertido tanto quanto eu~"

            if not mas_lastSeenInYear('mas_bday_spent_time_with'):
                if mas_isMoniUpset(lower=True):
                    m 1dka "..."
                    jump mas_bday_spent_time_with

                m 3eud "Ah, e [player]..."
                m 3eka "Queria te agradecer mais uma vez."
                m 1rka "E não é só por hoje..."
                m 1eka "Você nem precisou me levar a lugar nenhum pra esse aniversário ser maravilhoso."
                m 3duu "Assim que você apareceu, meu dia ficou completo."
                $ MASEventList.push('mas_bday_spent_time_with_wrapup', skipeval=True)

    return


label mas_monika_cake_on_player_bday:
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)

    python:
        mas_gainAffection(15, bypass=True)
        renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        persistent._mas_bday_sbp_reacted = True
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()

        if time_out <= mas_one_hour:
            mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        elif time_out <= mas_three_hour:
            mas_mbdayCapGainAff(20 if persistent._mas_player_bday_in_player_bday_mode else 15)
        else:
            
            mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

    m 6eua "Isso foi--"
    m 6wuo "Ah! Você fez um bolo pra {i}mim{/i}!"

    menu:
        "Acender as velas.":
            $ mas_bday_cake_lit = True

    m 6sub "Está {i}tão{/i} lindo, [player]!"
    m 6hua "Ehehe, eu sei que já fizemos um pedido quando eu soprei as velas do seu bolo, mas vamos fazer de novo..."
    m 6tub "Assim tem o dobro de chance de se realizar, né?"
    m 6hua "Faça um pedido, [player]!"

    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False

    m 6eua "Ainda não consigo acreditar em como esse bolo está deslumbrante, [player]..."
    m 6hua "É quase bonito demais pra comer."
    m 6tub "Quase."
    m "Ahaha!"
    m 6eka "De qualquer forma, vou guardar ele pra mais tarde."

    call mas_HideCake ('mas_bday_cake_monika')

    m 1eua "Muito obrigada, [player]..."
    m 3hub "Esse é um aniversário incrível!"
    return

label mas_HideCake(cake_type, reset_zoom=True):
    call mas_transition_to_emptydesk
    $ renpy.hide(cake_type)
    with dissolve
    $ renpy.pause(3.0, hard=True)
    call mas_transition_from_emptydesk ("monika 6esa")
    $ renpy.pause(1.0, hard=True)
    if reset_zoom:
        call monika_zoom_transition (mas_temp_zoom_level, 1.0)
    return
