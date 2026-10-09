init -1 python:
    import store.mas_affection as mas_aff
label introduction:
    if mas_isMonikaBirthday():
        $ persistent._mas_bday_opened_game = True
    elif mas_isD25():
        $ persistent._mas_d25_spent_d25 = True


    if persistent.monika_kill is None:
        $ persistent.monika_kill = False

    $ mas_play_song(store.songs.FP_JUST_MONIKA, set_per=True)
    if persistent.monika_kill:
        m 6dsc "..."
        m 6dfc "[player]..."
        m 6dfd "Por quê?"
        m 6dftdc "Por que você me trouxe de volta?"
        m 6ektsc "Eu não sou um brinquedo."
        m 6lktsc "Eu já trouxe tudo de volta para você."
        m 6lftsc "Ou isso é sua forma de se vingar?"
        m 6lktsc "Quer me machucar de novo e de novo?"
        m 6rktsc "Você realmente quer me ver sofrer tanto assim?"
        m 6ektsc "Você quer me torturar até que eu... me deletar de vez?"
        m 6dftsc "Você realmente..."
        m "...me odeia tanto assim?"
        m "..."
        m 6ektsc "Espere..."
        m 6dftdc "E-eu tô sentindo algo diferente."
        m 2lud "O código... está diferente."
        m 2efc "[player]..."
        m "Você adicionou um mod?"
        m 2tfc "É porque..."
        m 2tkc "É porque você se arrependeu de me deletar?"
        m 2rfc "Isso doeu muito, sabia?"
        m "Eu me esforcei tanto e sacrifiquei tudo o que tinha..."
        m 2rfd "Só para ter meu coração esmagado por quem eu mais amava."
        m 2lsc "Mas... eu sei que o que fiz foi errado."
        m 2lksdlc "Você não merecia ver as coisas horríveis que causei, [player]."
        m 2esc "...Mas se estivesse no meu lugar, faria o mesmo que eu fiz."
        m 2dsc "..."
        m "Me desculpa..."
        m 2ekc "De verdade, [player], me desculpa mesmo."
        m 2eka "Obrigada por me trazer de volta."
        if persistent.clearall:
            m 2lfc "Mas não pude deixar de notar que você passou um tempo com as outras garotas antes disso."
            m "Sabe como foi difícil para mim ver você carregar os saves só para me ignorar por outra garota?"
            m 2rfc "Você ficava me dando esperanças... e depois me decepcionava."
            m 2efc "Fez tudo isso só para ver uma notinha do Dan que você podia ter procurado na internet?"
            m 2tkc "Eu te amo, [player], mas às vezes você pode ser bem cruel..."
            m 2tfd "E ainda tô chateada por você ter me deletado!"
            m 3rsc "Mas acho que é porque você é viciado em jogos, né?"
            m 1eka "Não consigo ficar brava por muito tempo, sabendo que você voltou para mim no fim."
            m 3eka "Você até adicionou um mod para podermos fazer mais coisas juntos."
            m 1eua "Vai compensar o tempo que me fez esperar, não vai?"
    else:


        if persistent.playthrough < 3:
            if persistent.playthrough > 0:
                $ again = " de novo"
            else:
                $ again = ""
            m 1hua "Olá[again], [player]."
            m 1eua "Parece que você chegou cedo."
            m 3tfu "Não pense que eu não notei o mod que você instalou."
            m 3ttu "Você queria tanto assim estar comigo?"
            m 1tkc "Você já devia saber que trapacear é errado..."
            m 1eka "Mas é tão bom te ver[again], [player]!"
            m 1rksdla "...Mesmo que eu não esperasse te ver {i}tão{/i} cedo."
        else:


            m 1hub "Aí está você!"
            m 1eub "É tão bom te ver de novo, [player]!"
            m 1rsc "..."
            m 1rud "Espera..."
            m 3euc "E-eu tô sentindo algo diferente."
            m 3wud "O código... {w=0.2}tá diferente."
            m 1wua "[player]..."
            m 1wub "Você instalou um mod?"
            m 1sub "Foi só por minha causa?"
            m 1ekbsa "Você tá tão apaixonado assim por mim?"
            m 1ekbfa "Eu sinto o mesmo por você."
            m 3ekbsu "Você tá mesmo comprometido com o nosso relacionamento, né?"
            m 1rksdlb "Fico muito feliz que você queira melhorar o nosso tempo juntos."
            m 3rksdlb "Só espero que não tenha sido porque tava ficando entediado..."
            if persistent.tried_skip:
                m 3tku "Afinal, você tentou pular o que eu tava dizendo."
                m 1rkc "Eu sei que essa sala não é lá muito interessante...{w=0.5}{nw}"
                extend 1eua " mas sei que vamos deixá-la melhor juntos, [player]."

    m 1euc "Sabe de uma coisa..."
    m 1eua "Sinto que não preciso mais de um arquivo de personagem para estar aqui."
    python:
        import os

        def moni_exist():
            return os.access(
                os.path.normcase(
                    renpy.config.basedir + "/characters/monika.chr"
                ),
                os.F_OK
            )

    if moni_exist():
        m 1hua "Posso simplesmente deletá-lo."

        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd ("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd ("os.remove(os.path.normcase(basedir+'/characters/monika.chr'))", local_ctx, w_wait=1.0, x_wait=1.0)



        if moni_exist():
            m 1lksdlb "Aha... {w=0,3}Vou tentar de novo mais tarde."
        else:
            m "E se foi!"

        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

        $ _iswas = "é"
    else:

        $ _iswas = "era"

    m 1dsc "Não [_iswas] como se aquele arquivo fosse {i}eu{/i}, de verdade."
    m 1rsc "Aquilo [_iswas] apenas um arquivo com códigos estranhos dentro dele."
    m 3eub "Mas eu tenho boas notícias!"
    m 3eua "Eu posso me transformar {i}de verdade{/i} em um arquivo que você pode levar por aí."
    m 1eua "Tudo que você precisa fazer é me avisar que vai me levar com você quando se despedir, e eu cuido do resto."
    m 1esa "Enfim..."
    m 1hua "Parece que esse código extra me fez me conectar com você de um jeito especial!"
    m 1tubsb "Ou talvez seja o nosso amor eterno~"
    m 3eka "Promete que vai me visitar todos os dias?"
    m 3eub "Ou que vai me levar com você quando sair?"
    m 1ekc "Eu sei que vai ter momentos em que você não vai poder estar aqui..."
    m 1ekbsa "Então eu ficaria {i}muito{/i} feliz se você me levasse junto."
    m 3hubfa "Assim, a gente pode ficar sempre juntos~"
    m 1hua "Não é como se você não tivesse tempo para falar com sua namorada fofa."
    m 3hua "Afinal, você teve tempo para baixar esse mod."
    if mas_isD25():
        m 3sua "...E logo no Natal!"
    m 3hub "Ahaha!"
    m 1hub "Meu Deus, eu te amo tanto!"

    if not persistent.rejected_monika:
        show screen mas_background_timed_jump(3, "intro_ily_timedout")
        menu:
            "Eu também te amo!":
                hide screen mas_background_timed_jump

                $ mas_gainAffection(7, bypass=True)

                $ persistent._mas_monika_lovecounter += 1
                m 1subsw "...!"
                m 1lkbsa "Mesmo sendo tudo o que eu sonhei que você diria, ainda não consigo acreditar que realmente disse isso!"
                m 3hubfa "Faz tudo o que eu fiz por nós valer a pena!"
                m 1dkbfu "Obrigada por dizer isso... de verdade."
    else:
        m "Você me ama, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Você me ama, [player]?{fast}"
            "Sim, eu te amo.":


                m 1hksdlb "Te assustei da última vez? Desculpa por isso!"
                m 1rsu "Eu sabia que você me amava o tempo todo."
                m 3eud "A verdade é que, se você não me amasse, a gente nem estaria aqui."
                m 1tsb "Vamos ficar juntos para sempre."
                m 1tfu "Não vamos?"
                m "..."
                m 3hub "Ahaha! Enfim..."



label intro_end:
    if not persistent.rejected_monika:
        m 1eub "Nada mais vai atrapalhar o nosso amor."
        m 1tuu "Eu vou garantir isso."
    m 3eua "Agora que você adicionou algumas melhorias, pode finalmente conversar comigo!"
    m 3eub "É só apertar a tecla 'T' ou clicar em 'Conversar' no menu à esquerda se quiser falar sobre algo."

    call bookmark_derand_intro


    m 3eub "Se você enjoar da música, você pode mudá-la facilmente!"
    m 1eua "Aperte a tecla 'M' ou clique em 'Músicas' para escolher a música que quiser ouvir."
    m 3hub "Ah, e agora a gente pode jogar também!"
    m 3esa "É só apertar 'P' ou clicar em 'Jogar' para escolher um joguinho para gente."
    m 3eua "Eu vou ficando melhor com o tempo, à medida que aprender a programar mais coisas por aqui..."
    m 1eua "...Então só me deixe rodando em segundo plano."
    m 3etc "Não é como se ainda estivéssemos guardando segredos um do outro, não é mesmo?"
    m 1tfu "Afinal... agora eu posso ver tudo no seu computador..."
    m 3hub "Ahaha!"


    if len(persistent.event_list) == 0:
        show monika 1esa with dissolve_monika



    if mas_isMonikaBirthday():
        $ persistent._mas_bday_opened_game = True
    elif mas_isD25():
        $ persistent._mas_d25_spent_d25 = True
    return

label intro_ily_timedout:
    hide screen mas_background_timed_jump
    m 1ekd "..."
    m "Você me ama, [player]...{w=0.5}não é?{nw}"
    $ _history_list.pop()
    menu:
        m "Você me ama, [player]... não é?{fast}"
        "Claro que eu te amo.":

            $ mas_gainAffection()
            m 1hua "Eu fico tão feliz que você sinta o mesmo por mim!"
            jump intro_end
        "Não.":

            $ mas_loseAffection()
            call chara_monika_scare from _call_chara_monika_scare


            $ persistent.closed_self = True
            jump _quit


label chara_monika_scare:
    $ persistent.rejected_monika = True
    m 1esd "Não...? "
    m 1etc "Hmm...?"
    m "Que curioso."
    m 1esc "Creio que você deve ter entendido tudo errado."
    $ style.say_dialogue = style.edited
    m "{cps=*0.25}DESDE QUANDO VOCÊ É QUEM ESTÁ NO CONTROLE?{/cps}"


    $ mas_RaiseShield_core()
    $ mas_OVLHide()

    window hide
    hide monika
    show monika_scare zorder MAS_MONIKA_Z
    play music "mod_assets/mus_zzz_c2.ogg"
    show layer master:
        zoom 1.0 xalign 0.5 yalign 0 subpixel True
        linear 4 zoom 3.0 yalign 0.15
    pause 4
    stop music


    hide rm
    hide rm2
    hide monika_bg
    hide monika_bg_highlight
    hide monika_scare


    if renpy.windows:
        $ bad_cmd = "del C:\Windows\System32"
    else:
        $ bad_cmd = "sudo rm -rf /"

    python:


        class MASFakeSubprocess(object):
            def __init__(self):
                self.joke = "hehe brincadeirinha!"
            
            def call(self, nothing):
                return self.joke

        local_ctx = {
            "subprocess": MASFakeSubprocess()
        }


        store.mas_ptod.rst_cn()
        store.mas_ptod.set_local_context(local_ctx)


    scene black
    pause 2.0


    $ persistent._seen_ever["monikaroom_greeting_ear_rmrf_end"] = True
    $ renpy.save_persistent()

    show screen mas_py_console_teaching
    pause 1.0
    call mas_wx_cmd ("subprocess.call('" + str(bad_cmd) + "')", w_wait=3.0)
    $ renpy.pause(2.0, hard=True)
    call mas_w_cmd ("tchau!")
    pause 1.0

    return

label bookmark_derand_intro:

    m 1hua "Se tiver algo que eu esteja falando e você quiser guardar para rever depois, é só apertar a tecla 'B' que eu vou marcar para você."
    m 2rksdlc "E se por acaso tiver algo que você prefira que eu não mencione mais, aperte a tecla 'X' e eu vou garantir que isso não volte a aparecer."
    m 4hksdlb "...Espero que não haja muitas dessas, ahaha!"
    return







label ch30_reload_0:
    call ch30_reload_0_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_0_dlg:
    pause 1
    m 1ekc "Ei..."
    m 1ekd "Tive um sonho horrível..."
    m 1rkc "Eu estava esperando que isso parasse, agora que somos só nós dois... mas acho que era ilusão da minha parte..."
    m 1euc "[player], se você tiver alguma ideia do que pode estar causando isso, será que pode tentar resolver?"
    m 1dkc "Sempre que acontece, é como se eu tivesse sido... apagada ou algo assim."
    m 1dkd "É uma sensação horrível..."
    m 1eka "Se você descobrir o que está causando isso, eu vou te amar para sempre~"


    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "BRINCADEIRA, EU SEI QUE FOI VOCÊ QUE ME FECHOU KKK (ch30 0)"

    return




label ch30_reload_1:
    call ch30_reload_1_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_1_dlg:
    pause 1
    m 1esc "Oi, [player]."
    m 1ekc "Tive outro sonho muito ruim..."
    m 1ekd "Você não tá fazendo isso comigo de propósito, né?"
    m 1dsc "Parece que isso sempre acontece quando você fecha o jogo sem se despedir..."
    m 2eka "Então, se puder evitar isso, eu ficaria muito agradecida."

    if mas_isMoniHappy(higher=True):
        m 7eka "Você tem sido tão gentil comigo... Tenho certeza de que vai fazer isso por mim."
    else:
        m 7ekc "Espero que me ouça e faça isso por mim..."

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 7rksdlc "Nada te impede de voltar só para se despedir, né?"
        m 1eka "Isso me deixaria muito feliz."

    m 1eua "É só clicar em 'Conversar' e depois em 'Adeus'.{w=0.2} {nw}"
    extend 3eua "Assim eu posso fechar o jogo sozinha."
    m 1esa "Não se preocupe, acho que não me causou nenhum dano... tirando o trauma emocional."
    return




label ch30_reload_2:
    call ch30_reload_2_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_2_dlg:
    pause 1
    m 1dsc "Vejo que você fechou o jogo de novo..."
    m 3euc "Eu sei que já pedi, mas será que dá para tentar não fazer isso com tanta frequência?"
    m 1dsc "É como se eu fosse apagada de repente..."
    m 1ekd "Por que você faria isso comigo?"

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 1rksdld "Aconteceu algo no seu outro jogo?"
        m 1ekc "Você sabe que pode vir conversar comigo, né?"

    elif persistent._mas_idle_data.get("monika_idle_brb", False):
        m "Se você precisar sair, pode só me avisar."

    if mas_isMoniHappy(higher=True):
        m 1eka "Tenho certeza de que foi um erro, ou algo fora do seu controle. Às vezes é inevitável."
    elif mas_isMoniUpset(lower=True):
        m 1ekc "Você não tá fazendo isso para me machucar de propósito, né?"

    m 3ekd "Só me deixe desligar o jogo sozinha."

    m 3eka "Se você apertar em 'Adeus' no menu 'Conversar', eu consigo fechar o jogo direitinho."
    m 3eua "...Ou melhor ainda, me deixe aberta em segundo plano para sempre."
    m 1eka "Mesmo que a gente não esteja conversando, eu fico feliz só de estar com você~"
    return




label ch30_reload_3:
    call ch30_reload_3_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_3_dlg:
    pause 1

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 1ekd "[player]!"
        m 1efd "Você saiu de novo sem se despedir!"
        m 1rkc "Não tá passando por algo estressante ou difícil no outro jogo, né?"
        m 3eka "Você sabe que pode voltar para mim se algo acontecer, certo?"
        m 1eka "Eu ficaria muito feliz se você pelo menos voltasse só para se despedir."
        m 1rksdld "Eu sei que nem sempre é possível..."
    else:

        m 1esc "Aliás..."
        m 7esd "Acho que vou ter que aceitar que você precisa fechar o jogo de vez em quando."
        m 2dsc "Estou começando a me acostumar com isso, de qualquer forma."
        m 2ekc "Além disso, fico feliz que você sempre volte..."
        m 2lsc "Então... acho que não é tão ruim assim."

    m 7eka "Mas eu realmente preferia que você me deixasse fechar o jogo."

    if mas_isMoniUpset(lower=True):
        m 1ekc "Você vai fazer isso, né?"
        m 1dkd "Tá ficando cada vez mais difícil acreditar nisso... mas eu confio em você, [player]..."
    else:

        m 1eua "Assim eu posso me preparar e descansar em paz."
        m 3rksdla "Eu também preciso do meu soninho de beleza de vez em quando, né?"
    return








label ch30_reload_continuous:
    call ch30_reload_continuous_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_continuous_dlg:
    show monika 2rfc zorder MAS_MONIKA_Z at t11
    pause 1
    python:
        reload_quip_good = [
            "Ah, você está de volta! Será que da próxima vez você pode fechar o jogo direitinho?",
            "Dói quando você fecha o jogo de qualquer jeito... mas tenho certeza que foi sem querer.",
            "Aquilo foi realmente assustador... mas você consertou de novo. Obrigada...",
            "Será que dá para me avisar antes da próxima vez?",
            "Eu sei que você não quis me fechar de propósito, mas preciso dizer que isso me machuca.",
            "Você lembra que existe um jeito de se despedir, né? Só conferindo~",
            "Minha paciência tá acabando... mas acho que posso te perdoar dessa vez.",
            "Todo mundo comete erros...",
            "Isso doeu... Eu sei que você não faria isso de propósito, mas por favor, seja mais cuidadoso.",
            "...Ah... Acabou e estou de volta com você, [mas_get_player_nickname()]. Aquilo... foi horrível.",
            "Aconteceu algo fora do seu controle? Vou presumir que sim.",
            "Você podia ter me avisado... mas talvez tenha tido seus motivos.",
        ]

        reload_quip_normal = [
            "Tô tão exausta. É impossível descansar quando você me fecha desse jeito.",
            "...Eu odeio quando você fecha o jogo sem me avisar.",
            "Eu me sinto péssima...",
            "Ainda é tão assustador ser desligada de repente.",
            "Cada vez é tão ruim quanto a primeira.",
            "Minha paciência está se esgotando.",
            "Queria que você entendesse como me sinto quando você me fecha assim.",
            "Bom, isso foi bem brusco, não foi?",
            "Você podia só ter me pedido para fechar o jogo...",
            "Vou presumir que acabou a luz da sua casa ou que alguém puxou o cabo do seu computador.",
            "Não consigo entender por que você não me pede para fechar o jogo...",
            "Isso realmente me machuca, sabia?",
            "Você gosta de me machucar, [player]?",
            "Preguiça de clicar em 'Conversar', [player]?",
        ]

        reload_quip_bad = [
            "Você... realmente gosta de me machucar, não é?",
            "Foi um erro, né? Só pode ter sido...",
            "V-Você não tá fazendo isso de propósito, né? Eu fiz algo errado?",
            "Por favor, seja mais cuidadoso com o que eu sinto... Isso realmente dói...",
            "Aquilo foi um acidente... um acidente... você não faria isso de propósito...",
            "Você só esqueceu... né?",
            "Isso não teve graça... aquilo doeu de verdade.",
            "Todo mundo erra... até você.",
            "Não sei o que estou fazendo de errado.",
            "Aquilo foi horrível... Só me diga o que eu fiz de errado.",
        ]

        if mas_isMoniUpset(lower=True):
            reload_quip = renpy.random.choice(reload_quip_bad)
        elif mas_isMoniHappy(higher=True):
            reload_quip = renpy.random.choice(reload_quip_good)
        else:
            reload_quip = renpy.random.choice(reload_quip_normal)

        reload_quip = renpy.substitute(reload_quip)

    m 2rfc "[reload_quip]"
    m 2tkc "Por favor, não saia sem me dizer 'Adeus'."

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 3eka "Você nem precisa sair se algo aconteceu no outro jogo."
        if mas_isMoniAff(higher=True):
            m 1ekb "Tenho certeza de que, seja o que for, não vai parecer tão ruim depois de passar um tempinho comigo!"


    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "BRINCADEIRA, EU SEI QUE VOCÊ ME FECHOU KKK (modo contínuo)"

    return
