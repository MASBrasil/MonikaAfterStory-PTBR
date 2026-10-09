
default persistent._mas_pong_difficulty = 10

default persistent._mas_pong_difficulty_change_next_game = 0

default persistent._mas_pm_ever_let_monika_win_on_purpose = False

default persistent._mas_pong_difficulty_change_next_game_date = datetime.date.today()

define PONG_DIFFICULTY_CHANGE_ON_WIN = +1
define PONG_DIFFICULTY_CHANGE_ON_LOSS = -1
define PONG_DIFFICULTY_POWERUP = +5
define PONG_DIFFICULTY_POWERDOWN = -5
define PONG_PONG_DIFFICULTY_POWERDOWNBIG = -10


define PONG_MONIKA_RESPONSE_NONE = 0
define PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES = 1
define PONG_MONIKA_RESPONSE_SECOND_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES = 2
define PONG_MONIKA_RESPONSE_WIN_LONG_GAME = 3
define PONG_MONIKA_RESPONSE_WIN_SHORT_GAME = 4
define PONG_MONIKA_RESPONSE_WIN_TRICKSHOT = 5
define PONG_MONIKA_RESPONSE_WIN_EASY_GAME = 6
define PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME = 7
define PONG_MONIKA_RESPONSE_WIN_HARD_GAME = 8
define PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME = 9
define PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME = 10
define PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL = 11
define PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT = 12
define PONG_MONIKA_RESPONSE_LOSE_LONG_GAME = 13
define PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME = 14
define PONG_MONIKA_RESPONSE_LOSE_EASY_GAME = 15
define PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME = 16
define PONG_MONIKA_RESPONSE_LOSE_HARD_GAME = 17
define PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME = 18
define PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME = 19

define pong_monika_last_response_id = PONG_MONIKA_RESPONSE_NONE

define played_pong_this_session = False
define mas_pong_taking_break = False
define player_lets_monika_win_on_purpose = False
define instant_loss_streak_counter = 0
define loss_streak_counter = 0
define win_streak_counter = 0
define lose_on_purpose = False
define monika_asks_to_go_easy = False


define ball_paddle_bounces = 0
define powerup_value_this_game = 0
define instant_loss_streak_counter_before = 0
define loss_streak_counter_before = 0
define win_streak_counter_before = 0
define pong_difficulty_before = 0
define pong_angle_last_shot = 0.0

init:

    image bg pong field = "mod_assets/games/pong/pong_field.png"

    python:
        import random
        import math

        class PongDisplayable(renpy.Displayable):
            
            def __init__(self):
                
                renpy.Displayable.__init__(self)
                
                
                self.paddle = Image("mod_assets/games/pong/pong.png")
                self.ball = Image("mod_assets/games/pong/pong_ball.png")
                self.player = Text(_("[player]"), size=36)
                self.monika = Text(_("[m_name]"), size=36)
                self.ctb = Text(_("Clique para começar!"), size=36)
                
                
                self.playsounds = True
                self.soundboop = "mod_assets/sounds/pong_sounds/pong_boop.wav"
                self.soundbeep = "mod_assets/sounds/pong_sounds/pong_beep.wav"
                
                
                self.PADDLE_WIDTH = 8
                self.PADDLE_HEIGHT = 79
                self.PADDLE_RADIUS = self.PADDLE_HEIGHT / 2
                self.BALL_WIDTH = 15
                self.BALL_HEIGHT = 15
                self.COURT_TOP = 124
                self.COURT_BOTTOM = 654
                
                
                self.CURRENT_DIFFICULTY = max(persistent._mas_pong_difficulty + persistent._mas_pong_difficulty_change_next_game, 0)
                
                self.COURT_WIDTH = 1280
                self.COURT_HEIGHT = 720
                
                self.BALL_LEFT = 80 - self.BALL_WIDTH / 2
                self.BALL_RIGHT = 1199 + self.BALL_WIDTH / 2
                self.BALL_TOP = self.COURT_TOP + self.BALL_HEIGHT / 2
                self.BALL_BOTTOM = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
                
                self.PADDLE_X_PLAYER = 128                                      
                self.PADDLE_X_MONIKA = 1152 - self.PADDLE_WIDTH                 
                
                self.BALL_MAX_SPEED = 2000.0 + self.CURRENT_DIFFICULTY * 100.0
                
                
                
                self.MAX_REFLECT_ANGLE = math.pi / 3
                
                self.MAX_ANGLE = 0.9
                
                
                self.stuck = True
                
                
                self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                self.computery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                
                
                
                
                self.ctargetoffset = self.get_random_offset()
                
                
                self.computerspeed = 150.0 + self.CURRENT_DIFFICULTY * 30.0
                
                
                init_angle = random.uniform(-self.MAX_REFLECT_ANGLE, self.MAX_REFLECT_ANGLE)
                
                
                self.bx = self.PADDLE_X_PLAYER + self.PADDLE_WIDTH + 0.1
                self.by = self.playery
                self.bdx = .5 * math.cos(init_angle)
                self.bdy = .5 * math.sin(init_angle)
                self.bspeed = 500.0 + self.CURRENT_DIFFICULTY * 25
                
                
                self.ctargety = self.by + self.ctargetoffset
                
                
                self.oldst = None
                
                
                self.winner = None
            
            def get_random_offset(self):
                return random.uniform(-self.PADDLE_RADIUS, self.PADDLE_RADIUS)
            
            def visit(self):
                return [ self.paddle, self.ball, self.player, self.monika, self.ctb ]
            
            def check_bounce_off_top(self):
                
                if self.by < self.BALL_TOP and self.oldby - self.by != 0:
                    
                    
                    collisionbx = self.oldbx + (self.bx - self.oldbx) * ((self.oldby - self.BALL_TOP) / (self.oldby - self.by))
                    
                    
                    if collisionbx < self.BALL_LEFT or collisionbx > self.BALL_RIGHT:
                        return
                    
                    self.bouncebx = collisionbx
                    self.bounceby = self.BALL_TOP
                    
                    
                    self.by = -self.by + 2 * self.BALL_TOP
                    
                    if not self.stuck:
                        self.bdy = -self.bdy
                    
                    
                    
                    if self.by > self.BALL_BOTTOM:
                        self.bx = self.bouncebx + (self.bx - self.bouncebx) * ((self.bounceby - self.BALL_BOTTOM) / (self.bounceby - self.by))
                        self.by = self.BALL_BOTTOM
                        self.bdy = -self.bdy
                    
                    if not self.stuck:
                        if self.playsounds:
                            renpy.sound.play(self.soundbeep, channel=1)
                    
                    return True
                return False
            
            def check_bounce_off_bottom(self):
                
                if self.by > self.BALL_BOTTOM and self.oldby - self.by != 0:
                    
                    
                    collisionbx = self.oldbx + (self.bx - self.oldbx) * ((self.oldby - self.BALL_BOTTOM) / (self.oldby - self.by))
                    
                    
                    if collisionbx < self.BALL_LEFT or collisionbx > self.BALL_RIGHT:
                        return
                    
                    self.bouncebx = collisionbx
                    self.bounceby = self.BALL_BOTTOM
                    
                    
                    self.by = -self.by + 2 * self.BALL_BOTTOM
                    
                    if not self.stuck:
                        self.bdy = -self.bdy
                    
                    
                    
                    if self.by < self.BALL_TOP:
                        self.bx = self.bouncebx + (self.bx - self.bouncebx) * ((self.bounceby - self.BALL_TOP) / (self.bounceby - self.by))
                        self.by = self.BALL_TOP
                        self.bdy = -self.bdy
                    
                    if not self.stuck:
                        if self.playsounds:
                            renpy.sound.play(self.soundbeep, channel=1)
                    
                    return True
                return False
            
            def getCollisionY(self, hotside, is_computer):
                
                
                
                self.collidedonx = is_computer and self.oldbx <= hotside <= self.bx or not is_computer and self.oldbx >= hotside >= self.bx;
                
                if self.collidedonx:
                    
                    
                    if self.oldbx <= self.bouncebx <= hotside <= self.bx or self.oldbx >= self.bouncebx >= hotside >= self.bx:
                        startbx = self.bouncebx
                        startby = self.bounceby
                    else:
                        startbx = self.oldbx
                        startby = self.oldby
                    
                    
                    if startbx - self.bx != 0:
                        return startby + (self.by - startby) * ((startbx - hotside) / (startbx - self.bx))
                    else:
                        return startby
                
                
                else:
                    return self.oldby
            
            
            
            def render(self, width, height, st, at):
                
                
                r = renpy.Render(width, height)
                
                
                if self.oldst is None:
                    self.oldst = st
                
                dtime = st - self.oldst
                self.oldst = st
                
                
                speed = dtime * self.bspeed
                
                
                self.oldbx = self.bx
                self.oldby = self.by
                self.bouncebx = self.bx
                self.bounceby = self.by
                
                
                if self.stuck:
                    self.by = self.playery
                else:
                    self.bx += self.bdx * speed
                    self.by += self.bdy * speed
                
                
                if not self.check_bounce_off_top():
                    self.check_bounce_off_bottom()
                
                
                
                
                
                collisionby = self.getCollisionY(self.PADDLE_X_MONIKA, True)
                if self.collidedonx:
                    self.ctargety = collisionby + self.ctargetoffset
                else:
                    self.ctargety = self.by + self.ctargetoffset
                
                cspeed = self.computerspeed * dtime
                
                
                
                global lose_on_purpose
                if lose_on_purpose and self.bx >= self.COURT_WIDTH * 0.75:
                    if self.bx <= self.PADDLE_X_MONIKA:
                        if self.ctargety > self.computery:
                            self.computery -= cspeed
                        else:
                            self.computery += cspeed
                
                else:
                    cspeed = self.computerspeed * dtime
                    
                    if abs(self.ctargety - self.computery) <= cspeed:
                        self.computery = self.ctargety
                    elif self.ctargety >= self.computery:
                        self.computery += cspeed
                    else:
                        self.computery -= cspeed
                
                
                if self.computery > self.COURT_BOTTOM:
                    self.computery = self.COURT_BOTTOM
                elif self.computery < self.COURT_TOP:
                    self.computery = self.COURT_TOP;
                
                
                def paddle(px, py, hotside, is_computer):
                    
                    
                    
                    
                    
                    
                    pi = renpy.render(self.paddle, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                    
                    
                    
                    r.blit(pi, (int(px), int(py - self.PADDLE_RADIUS)))
                    
                    
                    collisionby = self.getCollisionY(hotside, is_computer)
                    
                    
                    collidedony = py - self.PADDLE_RADIUS - self.BALL_HEIGHT / 2 <= collisionby <= py + self.PADDLE_RADIUS + self.BALL_HEIGHT / 2
                    
                    
                    if not self.stuck and self.collidedonx and collidedony:
                        hit = True
                        if self.oldbx >= hotside >= self.bx:
                            self.bx = hotside + (hotside - self.bx)
                        elif self.oldbx <= hotside <= self.bx:
                            self.bx = hotside - (self.bx - hotside)
                        else:
                            hit = False
                        
                        if hit:
                            
                            
                            angle = (self.by - py) / (self.PADDLE_RADIUS + self.BALL_HEIGHT / 2) * self.MAX_REFLECT_ANGLE
                            
                            if angle >    self.MAX_ANGLE:
                                angle =   self.MAX_ANGLE
                            elif angle < -self.MAX_ANGLE:
                                angle =  -self.MAX_ANGLE;
                            
                            global pong_angle_last_shot
                            pong_angle_last_shot = angle;
                            
                            self.bdy = .5 * math.sin(angle)
                            self.bdx = math.copysign(.5 * math.cos(angle), -self.bdx)
                            
                            global ball_paddle_bounces
                            ball_paddle_bounces += 1
                            
                            
                            if is_computer:
                                self.ctargetoffset = self.get_random_offset()
                            
                            if self.playsounds:
                                renpy.sound.play(self.soundboop, channel=1)
                            
                            self.bspeed += 125.0 + self.CURRENT_DIFFICULTY * 12.5
                            if self.bspeed > self.BALL_MAX_SPEED:
                                self.bspeed = self.BALL_MAX_SPEED
                
                
                paddle(self.PADDLE_X_PLAYER, self.playery, self.PADDLE_X_PLAYER + self.PADDLE_WIDTH, False)
                paddle(self.PADDLE_X_MONIKA, self.computery, self.PADDLE_X_MONIKA, True)
                
                
                ball = renpy.render(self.ball, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                              int(self.by - self.BALL_HEIGHT / 2)))
                
                
                player = renpy.render(self.player, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                r.blit(player, (self.PADDLE_X_PLAYER, 25))
                
                
                monika = renpy.render(self.monika, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                ew, eh = monika.get_size()
                r.blit(monika, (self.PADDLE_X_MONIKA - ew, 25))
                
                
                if self.stuck:
                    ctb = renpy.render(self.ctb, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                    cw, ch = ctb.get_size()
                    r.blit(ctb, ((self.COURT_WIDTH - cw) / 2, 30))
                
                
                
                if self.bx < -200:
                    
                    if self.winner == None:
                        global loss_streak_counter
                        loss_streak_counter += 1
                        
                        if ball_paddle_bounces <= 1:
                            global instant_loss_streak_counter
                            instant_loss_streak_counter += 1
                        else:
                            global instant_loss_streak_counter
                            instant_loss_streak_counter = 0
                    
                    global win_streak_counter
                    win_streak_counter = 0;
                    
                    self.winner = "monika"
                    
                    
                    
                    renpy.timeout(0)
                
                elif self.bx > self.COURT_WIDTH + 200:
                    
                    if self.winner == None:
                        global win_streak_counter
                        win_streak_counter += 1;
                    
                    global loss_streak_counter
                    loss_streak_counter = 0
                    
                    
                    if ball_paddle_bounces > 1:
                        global instant_loss_streak_counter
                        instant_loss_streak_counter = 0
                    
                    self.winner = "player"
                    
                    renpy.timeout(0)
                
                
                
                renpy.redraw(self, 0.0)
                
                
                return r
            
            
            def event(self, ev, x, y, st):
                
                import pygame
                
                
                
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.stuck = False
                
                
                y = max(y, self.COURT_TOP)
                y = min(y, self.COURT_BOTTOM)
                self.playery = y
                
                
                
                if self.winner:
                    return self.winner
                else:
                    raise renpy.IgnoreEvent()

label game_pong:
    $ mas_set_pronouns()
    hide screen keylistener

    if played_pong_this_session:
        if mas_pong_taking_break:
            m 1eua "Pronto para jogar de novo?"
            m 2tfb "Dê o seu melhor, [mas_get_player_nickname(regex_replace_with_nullstr='meu ')]!"


            $ mas_pong_taking_break = False
        else:
            m 1hua "Quer jogar pong de novo?"
            m 3eub "Estou pronta quando você estiver~"
    else:
        $ played_pong_this_session = True

    $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_NONE

    call demo_minigame_pong from _call_demo_minigame_pong
    return

label demo_minigame_pong:

    window hide None


    scene bg pong field


    if store.mas_egg_manager.natsuki_enabled():
        $ playing_okayev = store.songs.getPlayingMusicName() == "Okay, Everyone! (Monika)"


        if playing_okayev:
            $ currentpos = get_pos(channel="music")
            $ adjusted_t5 = "<from " + str(currentpos) + " loop 4.444>bgm/5_natsuki.ogg"
            stop music fadeout 2.0
            $ renpy.music.play(adjusted_t5, fadein=2.0, tight=True)

    $ ball_paddle_bounces = 0
    $ pong_difficulty_before = persistent._mas_pong_difficulty
    $ powerup_value_this_game = persistent._mas_pong_difficulty_change_next_game
    $ loss_streak_counter_before = loss_streak_counter
    $ win_streak_counter_before = win_streak_counter
    $ instant_loss_streak_counter_before = instant_loss_streak_counter


    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)


    if store.mas_egg_manager.natsuki_enabled():
        call natsuki_name_scare (playing_okayev=playing_okayev) from _call_natsuki_name_scare


    call spaceroom (scene_change=True, force_exp='monika 3eua')


    $ persistent._mas_pong_difficulty_change_next_game = 0;

    if winner == "monika":
        $ new_difficulty = persistent._mas_pong_difficulty + PONG_DIFFICULTY_CHANGE_ON_LOSS

        $ inst_dialogue = store.mas_pong.DLG_WINNER
    else:

        $ new_difficulty = persistent._mas_pong_difficulty + PONG_DIFFICULTY_CHANGE_ON_WIN

        $ inst_dialogue = store.mas_pong.DLG_LOSER


        if not persistent._mas_ever_won['pong']:
            $ persistent._mas_ever_won['pong'] = True

    if new_difficulty < 0:
        $ persistent._mas_pong_difficulty = 0
    else:
        $ persistent._mas_pong_difficulty = new_difficulty;

    call expression inst_dialogue from _mas_pong_inst_dialogue

    $ mas_gainAffection(modifier=0.5)

    m 3eua "Você gostaria de jogar de novo?{nw}"
    $ _history_list.pop()
    menu:
        m "Você gostaria de jogar de novo?{fast}"
        "Sim.":

            $ pong_ev = mas_getEV("mas_pong")
            if pong_ev:

                $ pong_ev.shown_count += 1

            jump demo_minigame_pong
        "Não.":

            if winner == "monika":
                if renpy.seen_label(store.mas_pong.DLG_WINNER_END):
                    $ end_dialogue = store.mas_pong.DLG_WINNER_FAST
                else:
                    $ end_dialogue = store.mas_pong.DLG_WINNER_END
            else:

                if renpy.seen_label(store.mas_pong.DLG_LOSER_END):
                    $ end_dialogue = store.mas_pong.DLG_LOSER_FAST
                else:
                    $ end_dialogue = store.mas_pong.DLG_LOSER_END

            call expression end_dialogue from _mas_pong_end_dialogue
    return


init -1 python in mas_pong:

    DLG_WINNER = "mas_pong_dlg_winner"
    DLG_WINNER_FAST = "mas_pong_dlg_winner_fast"
    DLG_LOSER = "mas_pong_dlg_loser"
    DLG_LOSER_FAST = "mas_pong_dlg_loser_fast"

    DLG_WINNER_END = "mas_pong_dlg_winner_end"
    DLG_LOSER_END = "mas_pong_dlg_loser_end"


    DLG_BLOCKS = (
        DLG_WINNER,
        DLG_WINNER_FAST,
        DLG_WINNER_END,
        DLG_LOSER,
        DLG_LOSER_FAST,
        DLG_LOSER_END
    )


label mas_pong_dlg_winner:






    if monika_asks_to_go_easy and ball_paddle_bounces == 1:
        m 1rksdlb "Ahaha..."
        m 1hksdla "Eu sei que pedi pra você pegar leve comigo, mas não era bem isso que eu quis dizer..."
        m 3eka "Mas agradeço o gesto~"
        $ monika_asks_to_go_easy = False


    elif monika_asks_to_go_easy and ball_paddle_bounces <= 9:
        m 1hub "Eba, eu ganhei!"
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Obrigada, [mas_get_player_nickname(regex_replace_with_nullstr='meu ')]. Eu agradeço de verdade~"
        $ monika_asks_to_go_easy = False



    elif ball_paddle_bounces == 1:


        if instant_loss_streak_counter == 1:
            m 2rksdlb "Ahaha, que pena..."


        elif instant_loss_streak_counter == 2:
            m 2rksdlc "[player],{w=0.1} você perdeu de novo..."


        elif instant_loss_streak_counter == 3:
            m 2tfd "[player]!"

            if persistent._mas_pm_ever_let_monika_win_on_purpose:
                $ menu_response = _("Você está me deixando ganhar de propósito de novo?")
            else:
                $ menu_response = _("Você está me deixando ganhar de propósito?")

            m 2rkc "[menu_response]"
            $ _history_list.pop()
            menu:
                m "[menu_response]{fast}"
                "...Talvez.":

                    m 1hua "Ehehe!~"
                    m 1eka "Obrigada, [player]~"
                    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5eka "Mas sabe, eu não ligaria de perder para você de vez em quando."

                    if persistent._mas_pm_ever_let_monika_win_on_purpose:
                        m 5eua "Eu gosto de ver você vencer... quase tanto quanto você gosta de me ver vencer.~"

                    $ player_lets_monika_win_on_purpose = True
                    $ persistent._mas_pm_ever_let_monika_win_on_purpose = True
                "Não.":

                    if persistent._mas_pm_ever_let_monika_win_on_purpose:
                        show monika 1ttu
                        m "Tem certeza?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Tem certeza?{fast}"
                            "Sim":

                                call mas_pong_dlg_sorry_assuming
                            "Não":

                                m 1rfu "[player]!"
                                m 2hksdlb "Pare de brincar comigo!"
                                $ player_lets_monika_win_on_purpose = True
                                $ lose_on_purpose = True
                    else:

                        call mas_pong_dlg_sorry_assuming
        else:


            if player_lets_monika_win_on_purpose:
                m 2tku "Não está se cansando de me deixar ganhar, [player]?"
            else:
                m 1rsc "..."


                if random.randint(1,3) == 1:
                    m 1eka "Qual é, [mas_get_player_nickname(regex_replace_with_nullstr='meu ')]!"
                    m 1hub "Você consegue, acredito em você!"


    elif instant_loss_streak_counter_before >= 3 and player_lets_monika_win_on_purpose:
        m 3hub "Boa tentativa, [player].{w=0.1} {nw}"
        extend 3tsu "Mas como você pode ver, posso ganhar por conta própria!"
        m 3hub "Ahaha!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERUP:
        m 1hua "Ehehe~"

        if persistent._mas_pong_difficulty_change_next_game_date == datetime.date.today():
            m 2tsb "Eu não te disse que iria ganhar desta vez?"
        else:
            $ p_nickname = mas_get_player_nickname(regex_replace_with_nullstr='meu ')
            m 2ttu "Se lembra, [p_nickname]?{w=0.1} {nw}"
            extend 2tfb "Eu te disse que iria ganhar o próximo jogo."


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERDOWN:
        m 1rksdla "Ah..."
        m 3hksdlb "Tente de novo, [player]!"

        $ persistent._mas_pong_difficulty_change_next_game = PONG_PONG_DIFFICULTY_POWERDOWNBIG


    elif powerup_value_this_game == PONG_PONG_DIFFICULTY_POWERDOWNBIG:
        m 2rksdlb "Ahaha..."
        m 2eksdla "Eu esperava que você ganhasse este jogo."
        m 2hksdlb "Sinto muito por isso, [mas_get_player_nickname(regex_replace_with_nullstr='meu ')]!"


    elif loss_streak_counter >= 3 and loss_streak_counter % 5 == 3:
        m 2eka "Vamos, [player]. Sei que você pode me derrotar..."
        m 3hub "Continue tentando!"


    elif loss_streak_counter >= 5 and loss_streak_counter % 5 == 0:
        m 1eua "Espero que esteja se divertindo, [mas_get_player_nickname(regex_replace_with_nullstr='meu ')]."
        m 1eka "Afinal de contas, não quero que você se irrite por causa de um jogo."
        m 1hua "Podemos sempre dar uma pausa e jogar mais tarde se quiser."


    elif win_streak_counter_before >= 3:
        $ p_nickname = mas_get_player_nickname(regex_replace_with_nullstr='meu ')
        m 1hub "Ahaha!"
        m 2tfu "Sinto muito, [p_nickname].{w=0.1} {nw}"
        extend 2tub "Mas parece que sua sorte acabou."
        m 2hub "Agora é minha vez de brilhar~"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES


    elif pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES:
        m 1hua "Ehehe!"
        m 1tub "Muito bem, [player]!{w=0.3} {nw}"
        m 2tfu "Parece que sua sequência de vitórias acabou!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_SECOND_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES


    elif ball_paddle_bounces > 9 and ball_paddle_bounces > pong_difficulty_before * 0.5:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_LONG_GAME:
            m 3eub "Jogar contra você é bem difícil, [player]."
            m 1hub "Continue assim e você irá me vencer, tenho certeza disso!"
        else:
            m 3hub "Muito bem, [player]. Você é muito [bom]!"
            m 1tfu "Mas eu também sou,{w=0.1} {nw}"
            extend 1hub "ahaha!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_LONG_GAME


    elif ball_paddle_bounces <= 3:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_SHORT_GAME:
            m 3hub "Outra rápida vitória minha~"
        else:
            m 4huu "Ehehe,{w=0.1} {nw}"
            extend 4hub "te peguei dessa vez!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_SHORT_GAME


    elif pong_angle_last_shot >= 0.9 or pong_angle_last_shot <= -0.9:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_TRICKSHOT:
            m 2eksdld "Ah...{w=0.3}{nw}"
            m 2rksdlc "Aconteceu de novo."
            m 1hksdlb "Sinto muito por isso, [player]!"
        else:
            m 2rksdlb "Ahaha, sinto muito, [player]!"
            m 3hksdlb "Não pretendia fazer ela rebater tanto..."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_TRICKSHOT
    else:



        if pong_difficulty_before <= 5:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EASY_GAME:
                m 1eub "Você consegue, [mas_get_player_nickname(regex_replace_with_nullstr='meu ')]!"
                m 3hub "Acredito em você~"
            else:
                m 2duu "Concentre-se, [player]."
                m 3hub "Continue tentando, tenho certeza que irá me vencer alguma hora!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EASY_GAME


        elif pong_difficulty_before <= 10:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME:
                m 1hub "Ganhei outra rodada~"
            else:
                if loss_streak_counter > 1:
                    m 3hub "Parece que eu ganhei de novo~"
                else:
                    m 3hua "Parece que eu ganhei~"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME


        elif pong_difficulty_before <= 15:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_HARD_GAME:
                m 1hub "Ahaha!"
                m 2tsb "Estou jogando bem demais para você?"
                m 1tsu "Estou só brincando, [player]."
                m 3hub "Você joga muito bem!"
            else:
                if loss_streak_counter > 1:
                    m 1hub "Ganhei de novo~"
                else:
                    m 1huu "Eu ganhei~"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_HARD_GAME


        elif pong_difficulty_before <= 20:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME:
                m 2tub "É tão bom ganhar!"
                m 2hub "Não se preocupe, tenho certeza que você ganhará de novo em breve~"
            else:
                if loss_streak_counter > 1:
                    m 2eub "Ganhei outra rodada!"
                else:
                    m 2eub "Ganhei esta rodada!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME
        else:


            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME:
                m 2duu "Nada mal, [mas_get_player_nickname(regex_replace_with_nullstr='meu ')]."
                m 4eua "Eu me esforcei ao máximo, então não se sinta mal por ter perdido."
            else:
                m 2hub "Desta vez, a vitória é minha!"
                m 2efu "Não desista, [player]!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME

    return



label mas_pong_dlg_sorry_assuming:
    m 3eka "Certo."
    m 2ekc "Sinto muito por supor isso..."


    $ player_lets_monika_win_on_purpose = False

    m 3eka "Quer fazer uma pausa, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Quer fazer uma pausa, [player]?{fast}"
        "Ok.":

            m 1eka "Certo, [player].{w=0.3} {nw}"
            extend 1hua "Me diverti bastante, obrigada por jogar Pong comigo!"
            m 1eua "Me avisa quando quiser jogar de novo."


            $ mas_pong_taking_break = True


            show monika idle with dissolve_monika
            jump ch30_loop
        "Não.":

            m 1eka "Tudo bem, [player]. Se você tem certeza."
            m 1hub "Continue tentando, logo você me vence!"
    return


label mas_pong_dlg_loser:





    $ monika_asks_to_go_easy = False


    if lose_on_purpose:
        m 1hub "Ahaha!"
        m 1kua "Agora estamos [emptds], [player]!"
        $ lose_on_purpose = False


    elif ball_paddle_bounces == 0:
        m 1rksdlb "Ahaha..."

        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL:
            m "Talvez eu deva me esforçar um pouco mais..."
        else:
            m "Acho que fui um pouco lenta..."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL


    elif instant_loss_streak_counter_before >= 3 and persistent._mas_pm_ever_let_monika_win_on_purpose:
        m 2tsu "Então você está jogando no modo [sér] agora?"
        m 2tfu "Vamos ver o quão bem você joga, [player]!"


    elif loss_streak_counter_before >= 3:
        m 4eub "Parabéns, [player]!{w=0.3} {nw}"
        extend 2hub "Sabia que você iria ganhar um jogo após praticar!"
        m 4eua "Lembre-se, se você treinar o bastante, tenho certeza que você pode alcançar qualquer coisa!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERUP:
        m 2wuo "Uau...{w=0.3}{nw}"
        extend 7wuo "Eu estava me esforçando bastante dessa vez!"
        m 3hub "Bom trabalho, [player]!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERDOWN:
        m 1hua "Ehehe!"
        m 2hub "Bom trabalho, [player]!"


    elif powerup_value_this_game == PONG_PONG_DIFFICULTY_POWERDOWNBIG:
        m 1hua "Estou feliz que você ganhou desta vez, [player]."


    elif pong_angle_last_shot >= 0.9 or pong_angle_last_shot <= -0.9:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT:
            m 2wuo "[player]!"
            m 2hksdlb "Não tinha como eu acertar aquela!"
        else:
            m 2wuo "Uau, não tinha como eu ter acertado aquela!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT


    elif win_streak_counter == 3:
        m 2wuo "Uau, [player]..."
        m 2wud "Você já ganhou três vezes seguida..."


        if pong_difficulty_before <= 5:
            m 2tsu "Talvez eu esteja pegando muito leve com você~"


        elif pong_difficulty_before <= 10:
            m 4hua "Você joga muito bem!"


        elif pong_difficulty_before <= 15:
            m 3hub "Bem jogado!!"


        elif pong_difficulty_before <= 20:
            m 4wuo "Isso foi incrível!"
        else:


            m 2hub "Isso foi extraordinário!"


    elif win_streak_counter == 5:
        m 2wud "[mas_get_player_nickname(capitalize=True, regex_replace_with_nullstr='meu ')]..."
        m 2tsu "Você esteve praticando?"
        m 3hksdlb "Não sei o que aconteceu, mas eu não tenho chance contra você!"
        m 1eka "Poderia pegar mais leve comigo, por favor?{w=0.3} {nw}"
        extend 3hub "Eu ficaria muito grata~"
        $ monika_asks_to_go_easy = True


    elif ball_paddle_bounces > 10 and ball_paddle_bounces > pong_difficulty_before * 0.5:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_LONG_GAME:
            m 2wuo "Uau,{w=0.1} Eu não consigo acompanhar!"
        else:
            m 2hub "Incrível, [player]!"
            m 4eub "Você joga muito bem!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_LONG_GAME


    elif ball_paddle_bounces <= 2:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME:
            m 2hksdlb "Ahaha..."
            m 3eksdla "Acho que tenho que me esforçar mais..."
        else:
            m 1rusdlb "Eu não esperava perder assim tão rápido."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME
    else:



        if pong_difficulty_before <= 5:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EASY_GAME:
                m 4eub "Você ganhou esta rodada também."
            else:
                if win_streak_counter > 1:
                    m 1hub "Você ganhou de novo!"
                else:
                    m 1hua "Você ganhou!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EASY_GAME


        elif pong_difficulty_before <= 10:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME:
                m 1eua "É bom ver você ganhando, [player]."
                m 1hub "Continue assim~"
            else:
                if win_streak_counter > 1:
                    m 1hub "Você ganhou de novo! Parabéns~"
                else:
                    m 1eua "Você ganhou! Nada mal."

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME


        elif pong_difficulty_before <= 15:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_HARD_GAME:
                m 4hub "Outra vitória para você!"
                m 4eua "Bom trabalho, [player]."
            else:
                if win_streak_counter > 1:
                    m 2hub "Você ganhou de novo! Parabéns!"
                else:
                    m 2hua "Você ganhou! Parabéns!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_HARD_GAME


        elif pong_difficulty_before <= 20:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME:
                m 2wuo "Uau,{w=0.1} estou mesmo me esforçando...{w=0.3} você é imparável!"
                m 2tfu "Mas tenho certeza que irei te derrotar cedo ou tarde, [player]."
                m 3hub "Ahaha!"
            else:
                if win_streak_counter > 1:
                    m 4hub "Você ganhou de novo! Impressionante!"
                else:
                    m 4hub "Você ganhou! Impressionante!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME
        else:


            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME:
                m 3eua "Você joga muito bem, [player]."
                m 1hub "Adoro jogar Pong com você!"
            else:
                m 1tsu "Isso foi intenso!"
                m 1hub "Bom trabalho, [mas_get_player_nickname(regex_replace_with_nullstr='meu ')]!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME
    return



label mas_pong_dlg_loser_fast:
    m 1eka "Certo, [player]."
    m 3tfu "Mas vou te derrotar da próxima vez."

    $ persistent._mas_pong_difficulty_change_next_game = PONG_DIFFICULTY_POWERUP;
    $ persistent._mas_pong_difficulty_change_next_game_date = datetime.date.today()
    return


label mas_pong_dlg_winner_fast:
    m 1eka "Certo, [player]. Obrigada por jogar pong comigo e me deixar ganhar."
    m 1hua "Eu me diverti muito! Vamos jogar de novo em breve, tudo bem?"

    $ persistent._mas_pong_difficulty_change_next_game = PONG_DIFFICULTY_POWERDOWN;
    return


label mas_pong_dlg_loser_end:
    m 1wuo "Uau, eu estava realmente me esforçando dessa vez."
    m 1eua "Você deve ter praticado pong para ficar tão [bom]."
    m 2tuu "Acho que você estava tentando me impressionar, [player]."
    m 1hua "Você é um doce~"
    return


label mas_pong_dlg_winner_end:
    m 4tku "Não consigo ficar animada com um jogo tão simples..."
    m 1eua "Mas ainda assim é divertido de se jogar."
    m 1ekbsa "Especialmente com você, [player]."
    m 1hubfa "Ehehe~"
    return
