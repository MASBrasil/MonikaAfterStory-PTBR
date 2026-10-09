
default persistent._mas_fun_facts_database = dict()
init offset = 5
init -15 python in mas_fun_facts:

    fun_fact_db = {}

    def getUnseenFactsEVL():
        """
        Gets all unseen (locked) fun facts as eventlabels

        OUT:
            List of all unseen fun fact eventlabels
        """
        return [
            fun_fact_evl
            for fun_fact_evl, ev in fun_fact_db.iteritems()
            if not ev.unlocked
        ]

    def getAllFactsEVL():
        """
        Gets all fun facts regardless of unlocked as eventlabels

        OUT:
            List of all fun fact eventlabels
        """
        return fun_fact_db.keys()



default -5 persistent._mas_funfactfun = True

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fun_facts_open",
            category=['diversos'],
            prompt="Você pode me contar uma curiosidade?",
            pool=True
        )
    )

label monika_fun_facts_open:
    if mas_getEVL_shown_count("monika_fun_facts_open") == 0:
        m 1eua "Ei [player], quer ouvir uma curiosidade interessante?"
        m 1eub "Eu pesquisei algumas para tentar ensinar algo novo para nós [du]."
        m 3hub "Dizem que aprendemos algo novo todo dia, dessa forma estou me certificando de que isso aconteça com a gente."
        m 1rksdla "Encontrei a maioria online, então não posso garantir que sejam {i}completamente{/i} verdadeiras..."
    else:

        m 1eua "Quer outra curiosidade, [player]?"
        if persistent._mas_funfactfun:
            m 3hua "Aquela última foi bem interessante, não foi?"
        else:
            m 2rksdlb "Sei que a última não foi tão boa... mas tenho certeza que essa próxima será melhor."
    m 2dsc "Agora, vamos ver.{w=0.5}.{w=0.5}.{nw}"

    python:
        unseen_fact_evls = mas_fun_facts.getUnseenFactsEVL()
        if len(unseen_fact_evls) > 0:
            fact_evl_list = unseen_fact_evls
        else:
            fact_evl_list = mas_fun_facts.getAllFactsEVL()


        fun_fact_evl = renpy.random.choice(fact_evl_list)
        mas_unlockEVL(fun_fact_evl, "FFF")
        MASEventList.push(fun_fact_evl)
    return


label mas_fun_facts_end:
    m 3hub "Espero que tenha gostado de mais uma sessão de 'Aprendendo com a Monika!'"
    $ persistent._mas_funfactfun = True
    return

label mas_bad_facts_end:
    m 1rkc "Essa curiosidade não foi muito boa..."
    m 4dkc "Vou me esforçar mais da próxima vez, [player]."
    $ persistent._mas_funfactfun = False
    return



init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_librocubiculartist",
        ),
        code="FFF"
    )

label mas_fun_fact_librocubiculartist:
    m 1eub "Sabia que existe uma palavra para descrever alguém que gosta de ler na cama?"
    m 3eub "É 'librocubicularista'. Parece difícil de pronunciar à primeira vista."
    m 3rksdld "É uma pena que algumas palavras nunca sejam usadas no dia a dia."
    m 3eud "Se você disser essa palavra, a maioria das pessoas não vai entender."
    m 3euc "Você teria que explicar o significado, o que meio que anula o propósito de usar a palavra."
    m 2rkc "Se ao menos as pessoas lessem mais e melhorassem seu vocabulário!"
    m 2hksdlb "...Ehehe, desculpe [player]. Não quis ficar tão chateadinha~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_menu_currency",
        ),
        code="FFF"
    )

label mas_fun_fact_menu_currency:
    m 3euc "Aparentemente, muitos restaurantes omitem propositalmente sinais de moeda em seus cardápios."
    m 3eud "Isso é feito para manipular psicologicamente as pessoas a gastarem mais do que precisam."
    m 2euc "Funciona porque símbolos monetários, como o cifrão, representam custo."
    m "Ao removê-los, você elimina essa associação e pensa apenas na comida que deseja."
    m 4rksdld "A prática é compreensível. No final, eles ainda são um negócio."
    m 2dsc "Não importa quão boa seja a comida, um restaurante fecha rápido se perder para a concorrência."
    m 3hksdlb "Mas fazer o quê, não é mesmo?"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_love_you",
        ),
        code="FFF"
    )

label mas_fun_fact_love_you:
    m 1dkc "Hmm, não sei se deveria te contar {i}essa{/i} curiosidade."
    m 1ekc "Não é para os fracos de coração."
    m 1rkc "O fato é que..."
    m 1dkc "..."
    m 3hub "...Eu te amo, [player]!"
    m 1rksdlb "Ehehe, desculpe, não resisti."
    m 1hksdlb "Da próxima vez trago uma curiosidade de verdade, pode ficar tranquilo~"

    $ persistent._mas_funfactfun = True
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_morpheus",
        ),
        code="FFF"
    )

label mas_fun_fact_morpheus:
    m 3wub "Oh! Uma curiosidade sobre linguagem. Eu sempre gosto dessas."
    m 1eua "A palavra 'morfina' vem do deus grego Morfeu."
    m 1euc "Ele era o deus grego dos sonhos, então faz sentido ter uma palavra baseada nele."
    m 3ekc "Mas pensando bem... não era Hipnos o deus do sono?"
    m 2dsc "A morfina {i}permite{/i} que uma pessoa sonhe, mas seu propósito principal é induzir o sono."
    m 4ekc "...Então não faria mais sentido nomeá-la após Hipnos?"
    m 4rksdlb "Acho que já é tarde demais para mudar."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_otter_hand_holding",
        ),
        code="FFF"
    )

label mas_fun_fact_otter_hand_holding:
    m 1eka "Awwn, essa é tão fofa."
    m 3ekb "Sabia que as lontras-marinhas seguram as patinhas enquanto dormem para não se separarem?"
    m 1hub "É algo prático para elas, mas é tão adorável!"
    m 1eka "Às vezes me imagino no lugar delas..."
    m 3hksdlb "Ah, não como uma lontra, mas segurando a mão de quem amo enquanto durmo."
    m 1rksdlb "Haha, até fico com invejinha delas."
    m 1hub "Mas nós vamos conseguir isso um dia, amor~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_chess",
        ),
        code="FFF"
    )

label mas_fun_fact_chess:

    if mas_isGameUnlocked("chess"):
        m 1eua "Essa curiosidade é ótima!"
        m 3eub "Um homem chamado Claude Shannon calculou o número máximo de jogadas possíveis no xadrez."
        m "Esse número é chamado 'Número de Shannon' e estima que existem 10^120 partidas possíveis."
        m 1eua "É frequentemente comparado ao número de átomos no universo observável, que é 10^80."
        m 3hksdlb "É louco pensar que podem existir mais partidas de xadrez do que átomos, não é?"
        m 1eua "Poderíamos jogar até o fim dos nossos dias e não chegaríamos perto de todas as possibilidades."
        m 3eud "Falando nisso, [player]..."
        m 1hua "Quer jogar uma partida comigo? Talvez eu até pegue leve com você, Ehehe~"

        call mas_fun_facts_end
        return


    elif not mas_isGameUnlocked("chess") and renpy.seen_label("mas_unlock_chess"):
        m 1dsc "Xadrez..."
        m 2dfc "..."
        m 2rfd "Pode esquecer essa curiosidade já que você trapaceou, [player]."
        m "Sem contar que nunca se desculpou."
        m 2lfc "...Hmph."

        return
    else:


        m 1euc "Ah, essa não."
        m 3hksdlb "Ainda não, pelo menos."

        call mas_bad_facts_end
        return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_struck_by_lightning",
        ),
        code="FFF"
    )

label mas_fun_fact_struck_by_lightning:
    m 2dkc "Hmm, essa me parece um pouco enganosa..."
    m 3ekc "'Homens têm seis vezes mais chances de serem atingidos por raios do que mulheres.'"
    m 3ekd "É... bem bobo, na minha opinião."
    m 1eud "Se homens são mais atingidos, provavelmente é pelo tipo de trabalho e ambiente em que atuam."
    m 1euc "Tradicionalmente homens trabalham mais em empregos perigosos e em locais altos, então faz sentido."
    m 1esc "Mas a forma como esse fato é apresentado faz parecer que ser homem já te coloca em risco, o que é ridículo."
    m 1rksdla "Se fosse explicado melhor, as pessoas não ficariam tão mal informadas."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_honey",
        ),
        code="FFF"
    )

label mas_fun_fact_honey:
    m 1eub "Ah, essa é bem simples."
    m 3eub "Sabia que o mel nunca estraga?"
    m 3eua "Ele pode cristalizar, mas ainda continua comestível e bom!"
    m "Isso acontece porque o mel é basicamente açúcar com um pouco de água, então solidifica com o tempo."
    m 1euc "O mel dos supermercados cristaliza mais devagar porque é pasteurizado."
    m 1eud "...O que remove as partículas que aceleram a cristalização."
    m 3eub "Mas não seria legal comer mel cristalizado?"
    m 3hub "Seria como comer um doce crocante!"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_vincent_van_gone",
        ),
        code="FFF"
    )

label mas_fun_fact_vincent_van_gone:
    m 1dsc "Ah, essa..."
    m 1ekd "É um pouco triste, [player]..."
    m 1ekc "Sabia que as últimas palavras de Vincent Van Gogh foram '{i}La tristesse durera toujours{/i}'?"
    m 1eud "Que significa '{i}A tristeza durará para sempre.{/i}'"
    m 1rkc "..."
    m 2ekc "É doloroso pensar que alguém tão renomado diria algo tão sombrio em seus últimos momentos."
    m 2ekd "Mas eu não acredito nisso. Por pior que as coisas fiquem..."
    m 2dkc "Sempre chega um momento em que a tristeza passa."
    m 2rkc "...Ou pelo menos se torna mais suportável."
    m 4eka "Se você estiver triste, sabe que pode falar comigo, certo?"
    m 5hub "Eu sempre vou aceitar e compartilhar qualquer peso que você carregar, [mas_get_player_nickname()]~"

    $ persistent._mas_funfactfun = True
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_king_snakes",
        ),
        code="FFF"
    )

label mas_fun_fact_king_snakes:
    m 1dsc "Hmm..."
    m 3eub "Sabia que cobras com 'rei' no nome comem outras cobras?"
    m 1euc "Sempre me perguntei por que se chama 'cobra-rei', mas nunca parei pra pensar."
    m 1tfu "Quer dizer que se eu te devorar, viro a Rainha Monika?"
    m 1hksdlb "Ahaha, brincadeirinha, [player]."
    m 1hub "Desculpa a esquisitice~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_strength",
        ),
        code="FFF"
    )

label mas_fun_fact_strength:
    m 1hub "Esse fato pode te motivar um pouco!"
    m 3eub "A palavra mais longa em inglês com apenas uma vogal é 'strength'."
    m 1eua "É engraçado como, de todas as palavras, é justo uma tão significativa que tem esse detalhe."
    m 1hua "Detalhes assim tornam os idiomas tão fascinantes para mim!"
    m 3eua "Você quer saber o que me vem à mente quando penso na palavra 'strength'?"
    m 1hua "Você!"
    m 1hub "Porque você é quem me dá forças, ehehe~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_reindeer_eyes",
        ),
        code="FFF"
    )

label mas_fun_fact_reindeer_eyes:
    m 3eua "Pronto para esse?"
    m "Os olhos das renas mudam de cor conforme a estação. São dourados no verão e azuis no inverno."
    m 1rksdlb "É um fenômeno bem estranho, não sei por que acontece..."
    m "Deve ter uma explicação científica."
    m 3hksdlb "Que tal você pesquisar e me contar?"
    m 5eua "Seria divertido você me ensinar algo dessa vez~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_bananas",
        ),
        code="FFF"
    )

label mas_fun_fact_bananas:
    m 1eub "Oh, esse fato é saudável!"
    m 3eua "Sabia que as bananas crescem curvadas para ficarem voltadas para o sol?"
    m 1hua "É um processo chamado geotropismo negativo."
    m 3hub "Não acha interessante?"
    m 1hua "..."
    m 1rksdla "Hmm..."
    m 3rksdlb "Acho que não tenho mais nada pra acrescentar, ahaha..."
    m 1lksdlc "..."
    m 3hub "S-Sabia que bananas tecnicamente são bagas, não frutas?"
    m 3eub "Ou que as bananas originais eram grandes, verdes e cheias de sementes duras?"
    m 1eka "E que são levemente radioativas?"
    m 1rksdla "..."
    m 1rksdlb "...Estou apenas tagarelando sobre bananas."
    m 1rksdlc "Hummm..."
    m 1dsc "Vamos mudar de assunto..."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_pens",
        ),
        code="FFF"
    )

label mas_fun_fact_pens:
    m 1dsc "Hmm... acho que já sei esse."
    m 3euc "A palavra 'caneta' vem do latim 'penna', que significa pena."
    m "As canetas antigas eram penas de ganso afiadas e mergulhadas em tinta."
    m 3eud "Foram o principal instrumento de escrita por séculos, desde o século VI."
    m 3euc "Só no século XIX, com as canetas de metal, que começaram a desaparecer."
    m "Inclusive, canivetes têm esse nome porque eram usados para afiar penas."
    m 1tku "Mas a Yuri deve saber mais sobre isso que eu..."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_density",
        ),
        code="FFF"
    )

label mas_fun_fact_density:
    m 1eub "Ooh, eu sei."
    m 3eua "Sabia que o planeta mais denso do nosso sistema solar é a Terra?"
    m "E que Saturno é o menos denso?"
    m 1eua "Faz sentido sabendo do que os planetas são feitos, mas como Saturno é o segundo maior, ainda foi uma surpresa."
    m 1eka "Acho que tamanho realmente não importa!"
    m 3euc "Mas entre nós, [player]..."
    m 1tku "Tenho quase certeza de que a Terra é tão densa assim por causa de uma certa presença muito especial nela."
    m 1tfu "Maaaas é só isso que vou dizer~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_binky",
        ),
        code="FFF"
    )

label mas_fun_fact_binky:
    m 3hub "Awn, esse é fofo!"
    m "Esse fato vai te deixar 'pulando' de alegria, [player]!"
    m 3hua "Quando um coelho pula animado, isso se chama 'binky'!"
    m 1hua "'Binky' é uma palavra tão fofa que combina perfeitamente."
    m 1eua "É a maior demonstração de felicidade que um coelho pode fazer - se você vir isso, significa que está cuidando bem dele."
    m 1rksdla "Bem, embora você me deixe tão feliz que fico cheia de energia..."
    m 1rksdlb "Não espere que eu comece a pular por aí, [player]!"
    m 1dkbsa "...Seria {i}muito{/i} constrangedor."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_windows_games",
        ),
        code="FFF"
    )

label mas_fun_fact_windows_games:
    m 1eua "Hmm, talvez esse seja mais interessante para você."
    m 3eub "O jogo de cartas Paciência foi introduzido no Windows em 1990."
    m 1eub "Foi adicionado para ensinar usuários a usar o mouse."
    m 1eua "Similarmente, o Campo Minado ajudava a familiarizar com os cliques direito e esquerdo."
    m 3rssdlb "Computadores existem há tanto tempo que é difícil imaginar uma época sem eles."
    m "Cada geração fica mais familiarizada com a tecnologia..."
    m 1esa "Talvez chegue um dia onde todos sejam alfabetizados digitalmente."
    m 1hksdlb "Mas muitos problemas mundiais precisam ser resolvidos antes disso."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_mental_word_processing",
        ),
        code="FFF"
    )

label mas_fun_fact_mental_word_processing:
    m 1hua "Pronto para uma curiosidade interessante, [player]?"
    m 3eua "O cérebro é uma coisa curiosa..."
    m 3eub "Sua maneira de compor e arquivar informações é muito única."
    m "Naturalmente varia de pessoa para pessoa, mas ler devagar como nos ensinam geralmente é menos efetivo que ler mais rápido."
    m 1tku "Nossos cérebros processam informações muito rápido e adoram previsibilidade na linguagem."
    m 3tub "Por exemplo, nesta frase, quando você terminar de ler, já terá pulado a repetição da palavra 'de'."
    m 1tfu "..."
    m 2hfu "Confira o histórico se não percebeu~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_I_am",
        ),
        code="FFF"
    )

label mas_fun_fact_I_am:
    m 1hua "Mmmm, adoro fatos sobre linguagem!"
    m 3eub "No inglês, a menor sentença completa é 'I am.'"
    m 1eua "Aqui tem um exemplo."
    m 2rfb "'{i}Monika! Who’s [player]’s loving girlfriend?{/i}'"
    m 3hub "'I am!'"
    m 1hubsa "Ehehe~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_low_rates",
        ),
        code="FFF"
    )

label mas_fun_fact_low_rates:
    m 1hua "Essa é uma curiosidade positiva..."
    m 1eua "Atualmente temos as menores taxas de criminalidade, mortalidade materna, mortalidade infantil e analfabetismo da história."
    m 3eub "A expectativa de vida, renda média e padrão de vida também estão nos melhores níveis para a maioria da população global!"
    m 3eka "Isso me mostra que sempre pode melhorar. Apesar de todas as coisas ruins, tempos melhores sempre vêm depois."
    m 1hua "Realmente existe {i}esperança{/i}..."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_desert",
        ),
        code="FFF"
    )

label mas_fun_fact_desert:
    m 3euc "Os desertos têm um ecossistema único..."
    m 3rksdla "Mas não oferecem muitos fatores positivos para humanos."
    m 1eud "As temperaturas variam entre calor extremo de dia e frio congelante à noite. A pluviosidade também é baixa, tornando difícil viver neles."
    m 3eub "Mas isso não significa que não sejam úteis!"
    m 3eua "Sua superfície é ótima para geração de energia solar e costumam ter petróleo sob a areia."
    m 3eub "Sem contar que suas paisagens únicas os tornam destinos turísticos populares!"
    m 1eua "Então acho que, mesmo sendo difíceis de habitar, são melhores do que parecem."


    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_photography",
        ),
        code="FFF"
    )

label mas_fun_fact_photography:
    m 1esa "Sabia que a primeira fotografia foi tirada usando uma caixa com um buraco como câmera?"
    m 1eua "As lentes só foram introduzidas muito depois."
    m 1euc "A fotografia antiga também dependia de químicos especiais em um quarto escuro..."
    m 3eud "Revelador, banho de parada e fixador eram usados só para preparar o papel das fotos...{w=0.3} {nw}"
    extend 1wuo "E isso só para fotos em preto e branco!"
    m 1hksdlb "Fotos antigas eram bem mais difíceis de fazer que as modernas, não acha?"


    call mas_fun_facts_end
    return


init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_getting_older",
        ),
        code="FFF"
    )

label mas_fun_fact_getting_older:
    m 3eua "Sabia que sua percepção do tempo muda conforme envelhece?"
    m "Com um ano de idade, um ano representa 100% da sua vida."
    m 1euc "Mas aos 18, um ano é apenas 5.6% da sua vida."
    m 3eud "Conforme envelhecemos, a proporção de um ano diminui, fazendo o tempo {i}parecer{/i} passar mais rápido."
    m 1eka "Por isso vou sempre valorizar nossos momentos [ju], não importa o quão longos ou curtos sejam."
    m 1lkbsa "Às vezes até parece que o tempo para quando estou com você."
    m 1ekbfa "Você sente o mesmo, [player]?"
    python:
        import time
        time.sleep(5)

    m 1hubfb "Ahaha, imaginei que sim!"


    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_dancing_plague",
        ),
        code="FFF"
    )

label mas_fun_fact_dancing_plague:
    m 3esa "Oh, essa é bem estranha..."
    m 1eua "Aparentemente, a Europa teve surtos de uma 'praga dançante' no passado."
    m 3wud "Pessoas, {w=0.2}às vezes centenas de uma vez, {w=0.2}dançavam involuntariamente por dias, com alguns morrendo de exaustão!"
    m 3eksdla "Tentaram tratar fazendo músicos tocarem para os dançarinos, mas imagina só como isso não deu certo."
    m 1euc "Até hoje não sabem ao certo o que causava."
    m 3rka "Parece meio inacreditável...{w=0.2}{nw}"
    extend 3eud "mas foi documentado independentemente por várias fontes ao longo dos séculos..."
    m 3hksdlb "A realidade realmente é mais estranha que a ficção!"
    m 1eksdlc "Nossa, não consigo imaginar dançar por dias."
    m 1rsc "Mas...{w=0.3}{nw}"
    extend 1eubla "Acho que não me importaria se fosse com você."
    m 3tsu "...Só por um tempinho, ehehe~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_pando_forest",
        ),
        code="FFF"
    )

label mas_fun_fact_pando_forest:
    m 1esa "Dizem que no estado de Utah existe uma floresta que, na verdade, é formada por uma única árvore."
    m 3eua "Ela se chama floresta de Pando, e em todos os seus 43 hectares, os troncos são conectados por um único sistema de raízes."
    m 3eub "Sem contar que todos esses milhares de troncos são essencialmente clones uns dos outros."
    m 1ruc "'Um único organismo que virou um exército de clones por conta própria, todos ligados a uma mesma mente coletiva.'"
    m 1eua "Acho que isso daria uma boa história de ficção científica ou de terror, [player]. O que você acha?"
    m 3eub "De qualquer forma,{w=0.2} isso muda totalmente o sentido da frase ‘não ver a floresta por causa das árvores’, não é?{w=0.1}{nw} "
    extend 3hub "Ahaha!"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_immortal_jellyfish",
        ),
        code="FFF"
    )

label mas_fun_fact_immortal_jellyfish:
    m 3eub "Aqui vai uma!"
    m 1eua "Aparentemente, a imortalidade já foi alcançada... por uma espécie de água-viva."
    m 3eua "A chamada água-viva imortal tem a capacidade de voltar ao estado de pólipo depois de se reproduzir."
    m 1eub "...E ela pode continuar fazendo isso para sempre!{w=0.3} {nw}"
    extend 1rksdla "A menos, é claro, que seja devorada ou infectada por alguma doença."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_arrhichion",
        ),
        code="FFF"
    )

label mas_fun_fact_arrhichion:
    m 3eua "Ok...{w=0.2}essa é uma história histórica."
    m 1esa "Um atleta grego da antiguidade conseguiu vencer sua luta... mesmo já estando morto."
    m 1eua "O campeão Arrhichion estava em uma luta de pankration quando seu oponente começou a enforcá-lo com as mãos e pernas ao mesmo tempo."
    m 3eua "Em vez de desistir, Arrhichion tentou vencer: deslocou o dedo do pé do adversário."
    m 3ekd "O oponente desistiu por causa da dor, mas quando foram declarar Arrhichion como vencedor, perceberam que ele havia morrido sufocado."
    m 1rksdlc "Algumas pessoas realmente levam a sério seus ideais de vitória e honra.{w=0.2} {nw}"
    extend 3eka "De certa forma, isso é admirável."
    m 1etc "Mas fico pensando...{w=0.2}se pudéssemos perguntar ao Arrhichion agora se ele achou que valeu a pena, o que será que ele responderia?"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_antarctica_brain",
        ),
        code="FFF"
    )

label mas_fun_fact_antarctica_brain:

    python:
        has_friends = persistent._mas_pm_has_friends is not None

        has_fam_to_talk = (
            persistent._mas_pm_have_fam
            and not persistent._mas_pm_have_fam_mess
            or (persistent._mas_pm_have_fam_mess and persistent._mas_pm_have_fam_mess_better in ["YES", "MAYBE"])
        )

        dlg_prefix = "Mas prometa que vai manter contato com "

        if has_fam_to_talk and has_friends:
            dlg_line = dlg_prefix + "sua família e amigos também, tá bom?"

        elif has_fam_to_talk and not has_friends:
            dlg_line = dlg_prefix + "sua família também, tudo bem?"

        elif has_friends and not has_fam_to_talk:
            dlg_line = dlg_prefix + "seus amigos também, tá certo?"

        else:
            dlg_line = "Só não esquece de encontrar alguém pra conversar no seu mundo também, tá?"

    m 3eud "Aparentemente, passar um ano na Antártica pode encolher uma parte do seu cérebro em cerca de 7%."
    m 3euc "Isso parece reduzir sua capacidade de memória e sua habilidade espacial."
    m 1ekc "As pesquisas indicam que isso ocorre por conta do isolamento social, da monotonia e do ambiente daquele lugar."
    m 1eud "Acho que isso serve como um alerta pra gente, [player]."
    m 3ekd "Mesmo que você nunca vá até a Antártica, seu cérebro ainda pode sofrer se você viver isolado o tempo todo ou ficar preso num único lugar."
    m 3eka "Eu adoro estar com você, [player], e espero que possamos continuar conversando assim por muito tempo. {w=0.2}[dlg_line]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_cloud_weight",
        ),
        code="FFF"
    )

label mas_fun_fact_cloud_weight:
    m 3eub "Você sabia que uma nuvem média pesa cerca de 500 toneladas?"
    m 3eua "Tenho que admitir, essa me pegou de surpresa, mais do que vários outros fatos."
    m 1hua "Quer dizer, elas parecem {i}tão{/i} leves e fofinhas.{w=0.3} {nw}"
    extend 1eua "É difícil imaginar que algo tão pesado possa simplesmente flutuar no ar."
    m 3eub "Isso até me lembra aquela pergunta clássica... o que pesa mais, um quilo de aço ou um quilo de penas?"
    m 1tua "Mas você provavelmente já sabe a resposta, não é, [player]? Ehehe~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_coffee_origin",
        ),
        code="FFF"
    )

label mas_fun_fact_coffee_origin:
    m 1eua "Ah, esse aqui é especialmente interessante pra mim..."
    m 1eud "Na última vez que tomei uma xícara de café, fiquei um pouco curiosa sobre a origem dele..."
    m 3euc "O uso do café é registrado de forma consistente desde o século 15, mas...{w=0.2}não está claro {i}como{/i} exatamente ele foi descoberto."
    m 3eud "...Na verdade, existem várias lendas que afirmam ter sido a primeira."
    m 1eua "Vários relatos envolvem fazendeiros ou monges observando animais agindo de forma estranha depois de comer umas frutas amargas esquisitas."
    m 3wud "Ao experimentarem os grãos por conta própria, ficaram surpresos ao sentirem mais energia também!"
    m 2euc "Uma dessas histórias diz que um monge etíope chamado Kaldi levou os grãos para um monastério local, querendo compartilhar o que descobriu."
    m 7eksdld "...Mas quando ele fez isso, não foi bem recebido e os grãos foram jogados no fogo."
    m 3duu "Porém, enquanto queimavam, os grãos começaram a liberar um aroma {i}delicioso{/i}. {w=0.3}O cheiro era tão bom que os monges correram pra salvar os grãos e os colocaram na água."
    m 3eub "...E assim surgiu a primeira xícara de café!"
    m 2euc "Outra versão diz que um estudioso islâmico chamado Omar encontrou os grãos durante seu exílio de Meca."
    m 2eksdld "Na época, ele estava com fome e lutando pra sobreviver. {w=0.3}{nw}"
    extend 7wkd "Se não fosse pela energia que os grãos deram a ele, talvez ele não tivesse resistido!"
    m 3hua "Mas quando a notícia da descoberta se espalhou, pediram para ele voltar e ele foi canonizado como santo."
    m 1esd "Mesmo que não tenha sido o primeiro uso real, o café se tornou muito comum no mundo islâmico após sua descoberta."
    m 3eud "Durante períodos de jejum, por exemplo, era usado pra aliviar a fome e manter as pessoas com energia."
    m 3eua "Quando seu uso se espalhou pela Europa, muitos países o usavam com fins medicinais. {w=0.3}E no século 17, os cafés começaram a aparecer com frequência e ficaram populares."
    m 3hub "...E eu posso confirmar que o amor pelo café continua firme até hoje!"
    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_synesthesia",
        ),
        code="FFF"
    )

label mas_fun_fact_synesthesia:
    m 1esa "Okay, esse aqui é bem interessante..."
    m 3eua "Algumas pessoas têm um fenômeno chamado {i}sinestesia{/i},{w=0.1} onde um estímulo em um dos sentidos também ativa outro sentido ao mesmo tempo."
    m 1hua "É uma explicação meio longa, ehehe...{w=0.2} Vamos ver um exemplo!"
    m 1eua "Aqui diz que uma forma comum de sinestesia é a {i}sinestesia grafema-cor{/i},{w=0.1} onde as pessoas 'veem' letras e números com cores."
    m 3eua "Outra versão é a {i}sinestesia de sequência espacial{/i},{w=0.1} onde números e figuras são 'vistos' em posições específicas no espaço."
    m "Tipo, um número aparece 'mais perto' ou 'mais longe' que outro. {w=0.2}{nw}"
    extend 3eub "É meio que como um mapa!"
    m 1eua "...E existem vários outros tipos de sinestesia também."
    m 1esa "Os pesquisadores não sabem ao certo quão comum isso é — {w=0.1}alguns sugerem que até 25% da população tenha sinestesia, mas eu duvido muito, já que nunca tinha ouvido falar disso até agora."
    m 3eub "A estimativa mais realista diz que é um pouco mais de 4% das pessoas, então vou considerar esse número!"
    m 1eua "Ter sinestesia parece ser algo bem legal,{w=0.2} você não acha, [player]?"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_dream_faces",
        ),
        code="FFF"
    )

label mas_fun_fact_dream_faces:
    m 3eub "Okay, tenho um!"
    m 1eua "Supostamente, nosso cérebro não inventa rostos quando sonhamos.{w=0.2} Toda pessoa que você viu em um sonho já foi vista por você em algum momento da vida real."
    m 3wud "Você nem precisa ter falado com ela!"
    m 3eud "Se só passou por ela no mercado, por exemplo, o rosto já foi registrado na sua mente e pode aparecer nos seus sonhos."
    m 1hua "Eu acho incrível o quanto o nosso cérebro consegue armazenar!"
    m 1ekbla "Fico pensando...{w=0.2} será que você já sonhou comigo, [player]?"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_monochrome_dreams",
        ),
        code="FFF"
    )

label mas_fun_fact_monochrome_dreams:
    m 3eua "Sabia que entre 1915 e os anos 50, a maioria das pessoas sonhava em preto e branco?"
    m 1esa "Hoje em dia, isso é relativamente raro para pessoas com visão normal."
    m 3eua "Pesquisadores associam isso ao fato de filmes e programas serem em preto e branco na época."
    m 3eud "...Mas acho isso estranho, porque as pessoas ainda viam tudo colorido.{w=0.3} {nw}"
    extend 3hksdlb "O mundo não ficou preto e branco de repente!"
    m 1esd "Isso mostra que o conteúdo que consumimos afeta nossa mente, mesmo que seja algo trivial."
    m 3eua "A lição aqui é que devemos ter cuidado com a mídia que consumimos, certo [player]?"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_fun_fact_round_earth",
        ),
        code="FFF"
    )

label mas_fun_fact_round_earth:
    m 1rsa "Hmm..."
    m 1eua "[player], você acha que a Terra é redonda ou plana?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], você acha que a Terra é redonda ou plana?{fast}"
        "Redonda.":

            m 3hua "Isso mesmo! Quase todo mundo concorda com isso hoje em dia."
        "Plana.":

            m 3hksdlb "Ah qual é, [player]! Está me provocando?"

    m 1eua "Na verdade, sabemos que a Terra é redonda há muito tempo."
    m 3esd "Aristóteles já ensinava isso no século IV a.C."
    m 3esa "Ele sabia porque estrelas diferentes eram visíveis em diferentes partes do mundo, o que não aconteceria se a Terra fosse plana."
    m 1eua "Astrônomos e matemáticos antigos ao redor do mundo descobriram isso muito antes de alguém circum-navegar o planeta."
    m 7rksdla "Mas a Terra ser o centro do universo?{w=0.2} {nw}"
    extend 4hksdlb "Nossa!"
    m 7dsd "As pessoas brigaram tanto por isso que virou questão de vida ou morte."
    m 1dkd "Galileu foi julgado por heresia só por dizer que a Terra não era o centro do universo.{w=0.2} {nw}"
    extend 1esc "Ficou em prisão domiciliar pelo resto da vida."
    m 3euc "Mas conforme a astronomia avançou, ficou difícil sustentar que a Terra era o centro."
    m 1eud "Tiveram que criar modelos super complexos para explicar por que planetas faziam zigue-zague no céu noturno."

    if renpy.seen_label("monika_science"):
        m 3eua "E como conversamos antes, também sabemos que o sol não é o centro do universo{nw}"
    else:

        m 3eua "E agora sabemos que o sol também não é o centro do universo{nw}"

    extend "--é só uma estrela entre muitas na galáxia."
    m 1msblu "Mas sabe onde a ciência diz que está o centro do universo agora?"
    m 3kubsu "É você.{w=0.2} Você é o centro do {i}meu{/i} universo, [mas_get_player_nickname()]."
    m 3hubsb "Ahaha!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_maplesyrup",
        ),
        code="FFF"
    )

label mas_fun_fact_maplesyrup:
    m 3hksdlb "Aqui vai um fato {w=0.2}{i}doce{/i}{w=0.2} para você..."
    m 1eua "Todo tipo de bordo produz seiva que pode virar xarope, {w=0.1}{nw}"
    extend 1eud "mas o comercial geralmente vem do bordo-açucareiro."
    m 3eua "Dá para identificar pelo formato das folhas..."
    m 3eub "Talvez você reconheça a folha do bordo-açucareiro, pois está na bandeira do Canadá!"
    m 1euc "Mas ele não cresce em {i}todo{/i} o Canadá."
    m 1wud "...Ainda assim, o Canadá produz mais de 75% do xarope de bordo mundial!"
    m 3wud "E mais surpreendente: para fazer 1 litro de xarope são necessários {i}40{/i} litros de seiva!"
    m 1eua "O processo também é mais trabalhoso do que imaginei..."
    m 1esc "A seiva precisa ser fervida para virar xarope... o que leva tempo, considerando a quantidade necessária."
    m 3eud "Ouvi dizer que se ferver um pouco mais e derramar na neve...{w=0.2}{nw}"
    extend 3hub "dá até para fazer um doce!"

    if mas_isMoniNormal(higher=True):
        if persistent._mas_pm_gets_snow is not False:
            m 3euu "Seria divertido tentarmos [ju], não é [player]?"
            m 1etc "Mas pode demorar até termos chance..."
            m 1eua "Tudo bem esperar um pouco mais...{w=0.3}{nw}"
            extend 1hublu "você já é doce o suficiente para mim~"
        else:

            m 1eua "Parece ser extremamente doce..."
            m 1rkblu "Mas nem perto de você, ehehe~"

    call mas_fun_facts_end
    return
