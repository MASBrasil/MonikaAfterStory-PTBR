default persistent._mas_game_database = dict()
init offset = 5
init -15 python in mas_games:
    import store


    game_db = {}

    def is_platform_good_for_chess():
        import platform
        import sys
        
        if sys.maxsize > 2**32:
            return platform.system() == 'Windows' or platform.system() == 'Linux' or platform.system() == 'Darwin'
        
        else:
            return platform.system() == 'Windows'

init -4 python in mas_games:
    def _total_games_played(exclude_list=[]):
        """
        Returns the total number of games played by adding up the shown_count of each game

        IN:
            exclude_list - A list of event_label strings for games we want to exclude from the number of games played
                defaults to an empty list
        """
        global game_db
        
        total_shown_count = 0
        for ev in game_db.itervalues():
            if ev.eventlabel not in exclude_list:
                total_shown_count += ev.shown_count
        
        return total_shown_count

init 2 python in mas_games:
    def getGameEVByPrompt(gamename):
        """
        Gets a game event by its prompt or event label (gamename)

        IN:
            gamename - Prompt, event label, or event label suffix of the game

        OUT:
            event object for the game entered if found. None if not found
        """
        global game_db
        
        
        gamename = gamename.lower()

        # Prefer stable identifiers so translated prompts do not break lookups.
        for ev in game_db.itervalues():
            eventlabel = ev.eventlabel.lower()
            if gamename == eventlabel or (
                eventlabel.startswith("mas_") and gamename == eventlabel[4:]
            ):
                return ev

        # Keep prompt lookup for existing callers that pass a displayed name.
        for ev in game_db.itervalues():
            if renpy.substitute(ev.prompt).lower() == gamename:
                return ev
        return None


init 3 python:
    def mas_isGameUnlocked(gamename):
        """
        Checks if the given game is unlocked.

        IN:
            gamename - name of the game to check

        OUT:
            True if the game is unlocked, False if not, or the game doesn't exist
        """
        game_ev = mas_games.getGameEVByPrompt(gamename)
        
        if game_ev:
            return (
                game_ev.unlocked
                and game_ev.checkConditional()
                and game_ev.checkAffection(store.mas_curr_affection)
            )
        return False

    def mas_unlockGame(gamename):
        """
        Unlocks the given game.

        IN:
            gamename - name of the game to unlock
        """
        game_ev = store.mas_games.getGameEVByPrompt(gamename)
        if game_ev:
            game_ev.unlocked = True

    def mas_lockGame(gamename):
        """
        Locks the given game.

        IN:
            gamename - name of the game to lock
        """
        game_ev = store.mas_games.getGameEVByPrompt(gamename)
        if game_ev:
            game_ev.unlocked = False


init python:
    addEvent(
        Event(
            persistent._mas_game_database,
            eventlabel="mas_pong",
            prompt="Pong",
            unlocked=True
        ),
        code="GME",
        restartBlacklist=True
    )

label mas_pong:
    call game_pong
    return

init python:
    addEvent(
        Event(
            persistent._mas_game_database,
            eventlabel="mas_chess",
            prompt="Xadrez",
            conditional=(
                "persistent._mas_chess_timed_disable is not True "
                "and mas_games.is_platform_good_for_chess() "
                "and mas_timePastSince(persistent._mas_chess_timed_disable, datetime.timedelta(hours=1))"
            ),
            rules={
                "display_name": "chess",
            }
        ),
        code="GME",
        restartBlacklist=True
    )

label mas_chess:
    $ persistent._mas_chess_timed_disable = None
    call game_chess
    return

init python:
    addEvent(
        Event(
            persistent._mas_game_database,
            eventlabel="mas_hangman",
            prompt="Jogo da Forca"
        ),
        code="GME",
        restartBlacklist=True
    )

label mas_hangman:
    call game_hangman
    return

init python:
    addEvent(
        Event(
            persistent._mas_game_database,
            eventlabel="mas_piano",
            prompt="Piano",
            rules={
                "display_name": "piano",
            }
        ),
        code="GME",
        restartBlacklist=True
    )

label mas_piano:
    call mas_piano_start
    return

init python:
    addEvent(
        Event(
            persistent._mas_game_database,
            eventlabel="mas_nou",
            prompt="NOU",
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="GME",
        restartBlacklist=True
    )

label mas_nou:
    call mas_nou_game_start
    return

label mas_pick_a_game:

    $ mas_RaiseShield_dlg()

    python:

        play_menu_dlg = store.mas_affection.play_quip()[1]


        game_menuitems = sorted([
            (ev.prompt, ev.eventlabel, False, False)
            for ev in mas_games.game_db.itervalues()
            if mas_isGameUnlocked(renpy.substitute(ev.prompt))
        ], key=lambda x:renpy.substitute(x[0]))

        ret_back = ("Deixa pra lá", False, False, False, 20)


    show monika 1eua at t21


    $ renpy.say(m, play_menu_dlg, interact=False)


    call screen mas_gen_scrollable_menu(game_menuitems, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ret_back)

    $ selected_game = _return

    if selected_game:
        show monika at t11
        if selected_game != "mas_piano" and not (selected_game == "mas_pong" and played_pong_this_session):
            python:
                if mas_isMoniUpset(lower=True):
                    begin_quips = [
                        _("Ok, vamos jogar."),
                        _("Acho que podemos jogar isso."),
                        _("Vamos começar."),
                        _("Claro."),
                        _("Tá bom."),
                        _("Beleza."),
                    ]

                else:
                    begin_quips = [
                        _("Vamos nessa!"),
                        _("Pode vir, [mas_get_player_nickname()]!"),
                        _("Pronto para perder, [mas_get_player_nickname()]?"),
                        _("Estou pronta quando você estiver, [mas_get_player_nickname()]!"),
                        _("Espero que esteja pronto, [mas_get_player_nickname()]~"),
                        _("Vamos nos divertir, [mas_get_player_nickname()]!"),
                        _("Não espere que eu vá pegar leve com você, [mas_get_player_nickname()]!~"),
                        _("Está me desafiando, hein?"),
                        _("É hora do duelo!"),
                        _("Desafio aceito!"),
                    ]

                game_quip = renpy.substitute(renpy.random.choice(begin_quips))


            if mas_isMoniBroken():
                m 6ckc "..."

            elif mas_isMoniUpset(lower=True):
                m 2ekd "[game_quip]"
            else:

                m 3hub "[game_quip]"

        $ MASEventList.push(selected_game, skipeval=True)

    if not renpy.showing("monika idle"):
        show monika idle at t11

    $ mas_DropShield_dlg()

    jump ch30_loop
