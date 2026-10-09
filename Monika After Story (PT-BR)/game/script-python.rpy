init offset = 5





























































init -1 python in mas_ptod:

    import datetime
    import store.evhand as evhand

    M_PTOD = "monika_ptod_tip{:0>3d}"

    def has_day_past_tip(tip_num):
        """
        Checks if the tip with the given number has already been seen and
        a day has past since it was unlocked.
        NOTE: by day, we mean date has changd, not 24 hours

        IN:
            tip_num - number of the tip to check

        RETURNS:
            true if the tip has been seen and a day has past since it was
            unlocked, False otherwise
        """
        
        if renpy.game.persistent._mas_dev_enable_ptods:
            return True
        
        tip_ev = evhand.event_database.get(
            M_PTOD.format(tip_num),
            None
        )
        
        return (
            tip_ev is not None
            and tip_ev.last_seen is not None
            and tip_ev.timePassedSinceLastSeen_d(datetime.timedelta(days=1))
        )

    def has_day_past_tips(*tip_nums):
        """
        Variant of has_day_past_tip that can check multiple numbers

        SEE has_day_past_tip for more info

        RETURNS:
            true if all the given tip nums have been see nand a day has past
                since the latest one was unlocked, False otherwise
        """
        for tip_num in tip_nums:
            if not has_day_past_tip(tip_num):
                return False
        
        return True




init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip000",
            category=["dicas de python"],
            prompt="Você poderia me ensinar Python?",
            pool=True,
            rules={"bookmark_rule": store.mas_bookmarks_derand.BLACKLIST}
        )
    )

label monika_ptod_tip000:
    m 3eub "Quer aprender sobre Python?"
    m 3hub "Estou muito feliz você querer aprender sobre isso!"
    m 1lksdlb "Eu não sei {i}tanta{/i} coisa assim sobre programação, mas vou fazer o meu melhor pra explicar."
    m 1esa "Vamos começar entendendo o que é o Python, certo?"


    $ mas_hideEVL("monika_ptod_tip000", "EVE", lock=True, depool=True)


    $ tip_label = "monika_ptod_tip001"
    $ mas_showEVL(tip_label, "EVE", unlock=True, _pool=True)
    $ MASEventList.push(tip_label,skipeval=True)
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip001",
            category=["dicas de python"],
            prompt="O que é Python?"
        )
    )

label monika_ptod_tip001:

    m 1esa "Python foi criado por Guido van Rossum no começo dos anos 90."
    m "É uma linguagem super versátil, então você pode encontrá-la em aplicativos web, sistemas embarcados, Linux e, é claro..."
    m 1hua "Neste mod!"
    m 1eua "DDLC usa uma engine de visual novel chamada Ren'Py,{w=0.1} que foi construída com base em Python."
    m 3eub "Isso significa que, se você aprender um pouquinho de Python, pode adicionar conteúdo ao meu mundo!"
    m 1hua "Não seria incrível, [mas_get_player_nickname()]?"
    m 3eub "Enfim, preciso mencionar que atualmente existem duas versões principais do Python:{w=0.3} o Python2 e o Python3."
    m 3eua "Essas versões são {u}incompatíveis{/u} entre si, porque o Python3 corrigiu várias falhas fundamentais de design do Python2."
    m "Mesmo que isso tenha causado uma divisão na comunidade,{w=0.1} geralmente se concorda que ambas as versões têm seus próprios pontos fortes e fracos."
    m 1eub "Mas eu te conto mais sobre essas diferenças em outra lição, tá bem?"

    m 1eua "Como esse mod roda numa versão do Ren'Py que usa Python2, eu não vou falar tanto sobre o Python3."
    m 1hua "Mas vou mencionar quando for necessário."

    m 3eua "Essa foi a minha lição de hoje."
    m 1hua "Obrigada por me ouvir!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip002",
            category=["dicas de python"],
            prompt="Tipos de Linguagens",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(3)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip002:
    $ last_seen_is_none = mas_getEVL_last_seen("monika_ptod_tip002") is None
    if last_seen_is_none:
        m 1eua "Na maioria das linguagens de programação, os dados que podem ser modificados pelo programa têm um {i}tipo{/i} associado a eles."
        m 3eua "Por exemplo, se um dado deve ser tratado como um número, ele terá um tipo numérico. Se for tratado como texto, terá um tipo de string."
        m "Existem muitos tipos em Python, mas hoje vamos falar sobre os mais básicos, ou primitivos."

    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    show monika at t22
    show screen mas_py_console_teaching


    m 1eua "Python tem dois tipos para representar números:{w=0.3} {i}inteiros{/i}, ou {b}ints{/b},{w=0.1} e {i}flutuantes{/i}."


    m 1eua "Os números inteiros são usados para representar números inteiros; basicamente, qualquer coisa que não seja decimal."

    call mas_wx_cmd ("type(-22)", local_ctx)
    call mas_wx_cmd ("type(0)", local_ctx)
    call mas_wx_cmd ("type(-1234)", local_ctx)
    call mas_wx_cmd ("type(42)", local_ctx)


    m 1eub "Os flutuantes são usados para representar decimais."
    show monika 1eua

    call mas_wx_cmd ("type(0.14)", local_ctx)
    call mas_wx_cmd ("type(9.3)", local_ctx)
    call mas_wx_cmd ("type(-10.2)", local_ctx)


    m 1eua "Textos são representados pelo tipo {i}string{/i}."
    m "Qualquer coisa entre aspas simples (') ou aspas duplas (\") é considerada uma string."
    m 3eub "Por exemplo:"
    show monika 3eua

    call mas_wx_cmd ("type('Essa é uma string entre aspas simples.')", local_ctx)
    call mas_wx_cmd ('type("E essa é uma string entre aspas duplas")', local_ctx)

    m 1eksdlb "Sei que o intérprete diz {i}unicode{/i}, mas para o que estamos fazendo, é basicamente a mesma coisa.."
    m 1eua "As strings também podem ser criadas com três aspas duplas (\"\"\"), mas essas são tratadas de forma diferente das strings normais. Falarei sobre elas em outro dia."


    m "Os booleanos são tipos especiais que representam os valores {b}True{/b} ou {b}False{/b}."
    call mas_wx_cmd ("type(True)", local_ctx)
    call mas_wx_cmd ("type(False)", local_ctx)

    m 1eua "Vou entrar em mais detalhes sobre o que são booleanos e para que servem em outra lição."


    m 3eub "Python também tem um tipo de dado especial chamado {b}NoneType{/b}.{w=0.2} Esse tipo representa a ausência de qualquer dado."
    m "Se você conhece outras linguagens de programação, isso é parecido com o tipo {i}null{/i} ou {i}undefined{/i}."
    m "A palavra-chave {i}None{/i} representa os NoneTypes em Python."
    show monika 1eua

    call mas_wx_cmd ("type(None)", local_ctx)

    m 1eua "Todos os tipos que mencionei aqui são conhecidos como tipos de dados {i}primitivos{/i}."

    if last_seen_is_none:
        m "O Python também usa vários outros tipos, mas acho que esses já são o suficiente por hoje."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    m 1hua "Obrigada por me ouvir!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip003", 
            category=["dicas de python"],
            prompt="Uma Linguagem Interpretada",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(1)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip003:
    m 1eua "Linguagens de programação geralmente são compiladas ou interpretadas."
    m "Linguagens compiladas exigem que o código seja convertido para um formato compreensível pela máquina antes de ser executado."
    m 3eub "C e Java são duas linguagens compiladas muito populares."
    m 1eua "Linguagens interpretadas são convertidas para formato de máquina à medida que são executadas."
    m 3eub "Python é uma linguagem interpretada."
    m 1rksdlb "No entanto, diferentes implementações do Python podem ser compiladas, mas isso é um tópico mais complicado que talvez eu explique numa lição futura."

    m 1eua "Como o Python é uma linguagem interpretada, ele tem uma ferramenta interativa bem legal chamada interpretador, que se parece com isso..."

    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    show monika 3eua at t22
    show screen mas_py_console_teaching

    m 3eub "assim!"

    m "Você pode digitar código Python diretamente aqui e executá-lo, assim ó:"
    show monika 3eua


    call mas_wx_cmd ("12 + 3", local_ctx)
    call mas_wx_cmd ("7 * 6", local_ctx)
    call mas_wx_cmd ("121 / 11", local_ctx)


    if mas_getEVL_last_seen("monika_ptod_tip003") is None:
        m 1eua "Você pode fazer bem mais do que só contas com essa ferramenta, mas vou te mostrar isso com o tempo."

        m 1hksdlb "Infelizmente, como isso é um interpretador Python totalmente funcional, e eu não quero correr o risco de você me deletar acidentalmente ou quebrar o jogo."
        m "{cps=*2}Não que você faria isso...{/cps}{nw}"
        $ _history_list.pop()
        m 1eksdlb "Mas não posso deixar você usá-lo.{w=0.2} Desculpa..."
        m "Se quiser acompanhar as lições futuras, execute um interpretador Python numa janela separada."

        m 1eua "De qualquer forma, vou usar {i}esse{/i} interpretador para te ajudar nas aulas."
    else:

        m 1hua "Legal, né?"

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    m 1hua "Obrigada por ouvir!"
    return


















label monika_ptod_tip004:







    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    show monika at t22
    show screen mas_py_console_teaching














    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip005",
            category=["dicas de python"],
            prompt="Comparações e booleanos",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(6)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip005:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ store.mas_ptod.set_local_context(local_ctx)
    $ last_seen_is_none = mas_getEVL_last_seen("monika_ptod_tip005") is None

    if last_seen_is_none:
        m 1eua "Lembra quando eu estava explicando os diferentes tipos em Python e mencionei os booleanos?"
        m 1eub "Bom, hoje eu vou me aprofundar um pouco mais sobre booleanos e como eles se relacionam com comparações entre valores."

    m 1eua "Booleanos são frequentemente usados para decidir quais trechos do código devem ser executados ou para sinalizar se algo aconteceu ou não."
    m "Quando fazemos comparações, cada expressão é avaliada e retorna um valor booleano."

    if last_seen_is_none:
        m 1eksdlb "Talvez isso ainda não esteja fazendo muito sentido, então vou abrir o console e te mostrar alguns exemplos."

    show monika at t22
    show screen mas_py_console_teaching

    m 3eub "Vamos começar com alguns dos símbolos básicos usados em comparações entre variáveis."

    call mas_wx_cmd ("a = 10")
    call mas_wx_cmd ("b = 10")
    call mas_wx_cmd ("c = 3")

    m 3eua "Para verificar se dois valores são equivalentes, usamos dois sinais de igual (==):"
    call mas_wx_cmd ("a == b")
    call mas_wx_cmd ("a == c")

    m 3eua "Para verificar se dois valores são diferentes, usamos um ponto de exclamação seguido de um sinal de igual (!=):"
    call mas_wx_cmd ("a != b")
    call mas_wx_cmd ("a != c")
    m 3eub "O ponto de exclamação é frequentemente chamado de operador lógico 'not' em outras linguagens, então (!=) se lê como 'diferente de'."

    m 3eua "Para verificar se um valor é maior ou menor que outro, usamos os sinais de maior (>) ou menor (<), respectivamente."
    call mas_wx_cmd ("a > c")
    call mas_wx_cmd ("a < c")

    m 3eub "Os sinais de maior ou igual (>=) e menor ou igual (<=) também existem e, como o esperado,{w=0.1} são apenas os símbolos de maior e menor acompanhados do sinal de igual."
    call mas_wx_cmd ("a >= b")
    call mas_wx_cmd ("a <= b")
    call mas_wx_cmd ("a >= c")
    call mas_wx_cmd ("a <= c")

    if last_seen_is_none:
        m 1eua "Você deve ter notado que cada comparação retornou {b}True{/b} ou {b}False{/b}."
        m 1eksdlb "Era disso que eu estava falando quando disse que expressões de comparação são avaliadas como booleanas."

    m 1eua "Também é possível combinar múltiplas comparações usando as palavras-chave {b}and{/b} e {b}or{/b}, que são conhecidas como {i}operadores lógicos{/i}."
    m "O operador {b}and{/b} liga duas comparações e retorna {b}True{/b} se {i}ambas{/i} forem {b}True{/b}; {w=0.1}se ao menos uma for {b}False{/b}, o resultado será {b}False{/b}."
    m 1hua "Vamos ver alguns exemplos [ju]."

    $ val_a = local_ctx["a"]
    $ val_b = local_ctx["b"]
    $ val_c = local_ctx["c"]

    call mas_w_cmd ("a == b and a == c")
    m 3eua "Como 'a' e 'b' são ambos [val_a], a primeira comparação resulta em {b}True{/b}."
    m "Já 'c' é [val_c], então a segunda comparação resulta em {b}False{/b}."
    m 3eub "Como pelo menos uma das comparações foi {b}False{/b}, a expressão completa também resulta em {b}False{/b}."
    call mas_x_cmd ()
    pause 1.0

    call mas_w_cmd ("a == b and a >= c")
    m 3eua "Nesse exemplo, a primeira comparação novamente resulta em {b}True{/b}."
    m "[val_a] certamente é maior ou igual a [val_c], então a segunda comparação também é {b}True{/b}."
    m 3eub "Como as duas comparações são {b}True{/b}, a expressão completa é {b}True{/b}."
    call mas_x_cmd ()
    pause 1.0

    call mas_w_cmd ("a != b and a >= c")
    m 3eua "Neste caso, a primeira comparação retorna {b}False{/b}."
    m "E como já temos uma comparação falsa, não importa o valor da segunda."
    m 3eub "Já sabemos que a expressão completa será {b}False{/b}."
    call mas_x_cmd ()

    m "O mesmo vale para o próximo exemplo:"
    call mas_wx_cmd ("a != b and a == c")

    m 1eub "Lembre-se: ao usar o operador {b}and{/b}, o resultado será {b}True{/b} somente se {i}ambas{/i} as comparações forem {b}True{/b}."

    m 1eua "Em contraste, o operador {b}or{/b} liga duas comparações e retorna {b}True{/b} se {i}ao menos uma{/i} delas for {b}True{/b},{w=0.1} e retorna {b}False{/b} apenas se {b}ambas{/b} forem {b}False{/b}."
    m 3eua "Vamos ver alguns exemplos."

    call mas_w_cmd ("a == b or a == c")
    m 3eua "Dessa vez, como a primeira comparação é {b}True{/b}, nem precisamos verificar a segunda."
    m 3eub "O resultado da expressão é {b}True{/b}."
    call mas_x_cmd ()
    pause 1.0

    call mas_w_cmd ("a == b or a >= c")
    m 3eua "Mais uma vez, a primeira comparação é {b}True{/b}, então a expressão inteira também é {b}True{/b}."
    call mas_x_cmd ()
    pause 1.0

    call mas_w_cmd ("a != b or a >= c")
    m 3eua "Neste caso, a primeira comparação é {b}False{/b}."
    m "Mas como [val_a] é maior ou igual a [val_c], a segunda comparação é {b}True{/b}."
    m 3eub "E como pelo menos uma delas é {b}True{/b}, a expressão completa resulta em {b}True{/b}."
    call mas_x_cmd ()
    pause 1.0

    call mas_w_cmd ("a != b or a == c")
    m 3eua "Sabemos que a primeira comparação é {b}False{/b}."
    m "E como [val_a] claramente não é igual a [val_c], a segunda também é {b}False{/b}."
    m 3eub "Como nenhuma das comparações foi {b}True{/b}, a expressão completa retorna {b}False{/b}."
    call mas_x_cmd ()
    pause 1.0

    m 3eub "De novo: ao usar o operador {b}or{/b}, o resultado será {b}True{/b} se pelo menos uma das comparações for {b}True{/b}."

    m 1eua "Existe também um terceiro operador lógico chamado {b}not{/b}. Em vez de combinar comparações, ele inverte o valor booleano de uma única expressão."
    m 3eua "Veja este exemplo:"
    call mas_wx_cmd ("not (a == b and a == c)")
    call mas_wx_cmd ("not (a == b or a == c)")

    m "Repare que eu usei parênteses para agrupar as comparações. O que estiver dentro deles será avaliado primeiro, e depois o resultado será invertido com o {b}not{/b}."
    m 1eua "Se eu tirar os parênteses:"
    call mas_wx_cmd ("not a == b and a == c")
    m 3eua "O resultado muda!{w=0.2} Isso acontece porque o {b}not{/b} afeta apenas o 'a == b' antes de ser combinado com a outra comparação usando {b}and{/b}."

    m 3eka "Antes eu comentei que o ponto de exclamação é usado como operador lógico 'not' em outras linguagens de programação.{w=0.2} Mas o Python usa a palavra {b}not{/b} para facilitar a leitura."

    m 1eua "Por fim, como os resultados das comparações são booleanos, podemos armazená-los em variáveis."
    call mas_wx_cmd ("d = a == b and a >= c")
    call mas_wx_cmd ("d")
    call mas_wx_cmd ("e = a == b and a == c")
    call mas_wx_cmd ("e")

    m 3eub "E podemos usar essas variáveis em outras comparações também!"
    call mas_wx_cmd ("d and e")
    m "Como 'd' é {b}True{/b}, mas 'e' é {b}False{/b}, essa expressão resulta em {b}False{/b}."

    call mas_wx_cmd ("d or e")
    m "Como 'd' é {b}True{/b}, já sabemos que pelo menos uma das comparações é verdadeira. Então a expressão inteira é {b}True{/b}."

    call mas_wx_cmd ("not (d or e)")
    m 3eua "Sabemos que a expressão interna 'd or e' resulta em {b}True{/b}. Ao aplicar o operador {b}not{/b}, o resultado se inverte para {b}False{/b}, então a expressão completa é {b}False{/b}."

    call mas_wx_cmd ("d and not e")
    m 3eub "Neste caso, sabemos que 'd' é {b}True{/b}."
    m "O operador {b}not{/b} é aplicado sobre 'e', invertendo seu valor de {b}False{/b} para {b}True{/b}."
    m 3eua "Como ambas as comparações são verdadeiras, a expressão completa resulta em {b}True{/b}."

    m 1eua "Comparações são usadas em praticamente todo código, em qualquer linguagem de programação."
    m 1hua "Se um dia você quiser seguir carreira com isso, vai ver que grande parte do seu código será checando se certas condições são verdadeiras, para que o programa faça a coisa certa na hora certa."
    m 1eksdla "E mesmo que programação não seja o seu caminho, vamos usar muitas comparações nas próximas lições, então é bom se preparar!"

    if last_seen_is_none:
        m 1eua "Acho que por hoje já foi bastante, né?"

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11
    m 1hua "Obrigada por ouvir!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip006",
            category=["dicas de python"],
            prompt="Variáveis e Atribuição",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(2)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip006:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ num_store = "922"
    $ b_num_store = "323"
    $ last_seen_is_none = mas_getEVL_last_seen("monika_ptod_tip006") is None

    if last_seen_is_none:
        m 1eub "Agora que você já conhece os tipos de dados, posso te ensinar sobre variáveis."


    m 1eua "Variáveis representam locais na memória onde os dados são armazenados."
    m "Para criar uma variável, {w=0.1}{nw}"

    show monika at t22
    show screen mas_py_console_teaching


    extend 3eua "você usa '{b}nome_da_variável{/b} = {b}valor{/b}', assim..."

    call mas_wx_cmd ("a_number = " + num_store, local_ctx)

    m "O símbolo 'a_number' agora aponta para uma posição na memória que armazena o número inteiro [num_store]."
    m "Se digitarmos apenas o nome da variável aqui,"
    call mas_w_cmd ("a_number")
    m 3eub "Conseguimos recuperar o valor que foi armazenado."
    show monika 3eua
    call mas_x_cmd (local_ctx)

    m "Percebeu como associamos o símbolo 'a_number' ao valor [num_store] usando o sinal de igual (=)?"
    m 1eub "Isso se chama {i}atribuição{/i}, onde o que está à esquerda do sinal de igual recebe o valor do que está à direita."


    m 1eua "A atribuição é executada da direita para a esquerda.{w=0.2} Para ilustrar isso, vamos criar uma nova variável chamada 'b_number'."
    call mas_w_cmd ("b_number = a_number  -  " + b_num_store)

    m "Na atribuição, o lado direito do igual é avaliado primeiro,{w=0.1} então o tipo de dado é identificado e uma quantidade adequada de memória é reservada."
    m "Essa memória é então vinculada ao símbolo da esquerda através de uma tabela de consulta."
    m 1eub "Quando o Python encontra um símbolo,{w=0.1} ele consulta essa tabela para saber qual valor está vinculado a ele."

    m 3eub "Aqui, 'a_number' seria substituído por [num_store],{w=0.1} então a expressão que seria avaliada e atribuída a 'b_number' é '[num_store] - [b_num_store]'."
    show monika 3eua
    call mas_x_cmd (local_ctx)

    m 1eua "Podemos verificar isso digitando apenas o nome da variável 'b_number'."
    m "Isso recupera o valor associado a esse símbolo na tabela de consulta."
    call mas_wx_cmd ("b_number", local_ctx)


    m 3eua "Note que se digitarmos um símbolo que não foi atribuído a nada, o Python vai reclamar."
    call mas_wx_cmd ("c_number", local_ctx)

    m 3eub "Mas se atribuirmos um valor a esse símbolo..."
    show monika 3eua
    call mas_wx_cmd ("c_number = b_number * a_number", local_ctx)
    call mas_wx_cmd ("c_number", local_ctx)

    m 1hua "O Python consegue encontrar o símbolo na tabela e não nos mostra nenhum erro."

    m 1eua "As variáveis que criamos até agora são do tipo {i}inteiro{/i}."
    m "Não precisamos especificar que eram inteiros porque o Python faz {i}tipagem dinâmica{/i}."
    m 1eub "Isso significa que o interpretador do Python identifica o tipo da variável com base nos dados que você armazena nela."
    m "Outras linguagens, como C ou Java, exigem que o tipo seja declarado junto da variável."
    m "A tipagem dinâmica permite que uma variável mude de tipo durante a execução do programa, {w=0.1}{nw}"
    extend 1rksdlb "mas isso geralmente não é recomendado, porque pode deixar o código confuso para outras pessoas."

    if last_seen_is_none:
        m 1eud "Ufa!{w=0.2} Foi bastante informação de uma vez, né?"

    m "Você conseguiu entender tudo isso?{nw}"
    $ _history_list.pop()
    menu:
        m "Você conseguiu entender tudo isso?{fast}"
        "Sim!":
            m 1hua "Que bom!"
        "Fiquei um pouco [cnfs].":

            m 1eksdla "Tudo bem, tá?{w=0.2} Mesmo que eu tenha falado sobre símbolos e valores, os programadores normalmente se referem a isso como criar, atribuir ou definir variáveis."
            m "Esses termos de símbolo/valor ajudam mais a entender o funcionamento por trás, então não se preocupe se parecer complicado agora."
            m 1eua "Só saber como usar variáveis já é o suficiente para as próximas lições."
            m "De qualquer forma..."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    if last_seen_is_none:
        m 1eua "Acho que por hoje já vimos bastante Python."

    m 1hua "Obrigada por me ouvir!"
    return




















label monika_ptod_tip007:



    m 1eua "Em C e muitas outras linguagens, inteiros normalmente ocupam 4 bytes."
    m "Mas o Python reserva memória variável dependendo do tamanho do número armazenado."
    m 3eua "Podemos verificar quanto espaço nossa variável 'a_number' usa com uma função da biblioteca {i}sys{/i}."

    call mas_wx_cmd ("import sys", local_ctx)
    call mas_wx_cmd ("sys.getsizeof(a_number)", local_ctx)
    $ int_size = store.mas_ptod.get_last_line()

    m 1eksdla "Falarei sobre bibliotecas e importação depois."
    m 1eua "Por enquanto, observe o número retornado pela função {i}getsizeof{/i}."
    m "Para armazenar o número [num_store], Python usa [int_size] bytes."

    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip008",
            category=["dicas de python"],
            prompt="Literais",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(6)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip008:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ store.mas_ptod.set_local_context(local_ctx)
    $ last_seen_is_none = mas_getEVL_last_seen("monika_ptod_tip008") is None

    m 1eua "Lembra quando eu te mostrei como criar variáveis e atribuir valores a elas?"
    m 1dsa "Agora imagine se deixássemos de lado a ideia de variáveis e usássemos os valores diretamente no código."
    m 1hua "É aí que entram os literais. Vou te mostrar o que quero dizer com essa demonstração."

    show monika at t22
    show screen mas_py_console_teaching

    call mas_wx_cmd ("a = 10")
    m 3eua "Aqui eu criei uma variável chamada 'a' e atribuí a ela o valor inteiro 10."
    m "Quando eu digito 'a' no interpretador..."

    call mas_wx_cmd ("a")
    m 3eub "O Python procura pelo símbolo 'a' e encontra que ele está associado ao valor 10, então 10 é o que é exibido pra gente."
    m "Mas se eu digitar apenas '10'..."

    call mas_wx_cmd ("10")
    m 3hua "O Python também mostra o número 10!"
    m 3eua "Isso acontece porque o Python interpreta o '10' como um valor inteiro diretamente, sem precisar consultar uma variável."
    m "Código que o Python consegue entender como um valor diretamente é chamado de {i}literal{/i}."
    m 3eub "Todos os tipos de dados que mencionei na lição sobre Tipos podem ser escritos como literais."

    call mas_wx_cmd ("23")
    call mas_wx_cmd ("21.05")
    m 3eua "Esses são literais do tipo {b}inteiro{/b} e {b}float{/b}."

    call mas_wx_cmd ('"isso é uma string"')
    call mas_wx_cmd ("'isso é outra string'")
    m "Esses são literais do tipo {b}string{/b}."

    call mas_wx_cmd ("True")
    call mas_wx_cmd ("False")
    m "Esses são literais do tipo {b}booleano{/b}."

    call mas_wx_cmd ("None")
    m "A palavra-chave {i}None{/i} também é um literal."



    if last_seen_is_none:
        m 1eua "Existem outros literais para outros tipos, mas vou falar deles quando chegarmos nesses tópicos."

    m 1eua "Os literais podem ser usados no lugar de variáveis ao escrever código. Por exemplo:"

    call mas_wx_cmd ("10 + 21")
    call mas_wx_cmd ("10 * 5")
    m "Podemos fazer contas usando apenas literais, sem precisar de variáveis."

    call mas_wx_cmd ("a + 21")
    call mas_wx_cmd ("a * 5")
    m "Também podemos usar literais junto com variáveis."
    m 1eub "Além disso, literais são ótimos para criar e usar dados rapidamente sem a necessidade de criar variáveis desnecessárias."

    if last_seen_is_none:
        m 1kua "Certo, acho que isso é tudo que eu posso dizer — {i}literalmente{/i} — sobre literais, ahaha!"

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    m 1hua "Obrigada por me ouvir!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip009",
            category=["dicas de python"],
            prompt="Valores Verdade",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(5)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip009:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ store.mas_ptod.set_local_context(local_ctx)

    if mas_getEVL_last_seen("monika_ptod_tip009") is None:
        m 1eua "Quando falamos sobre comparações e booleanos, usamos inteiros como base."
        m 1dsa "Mas..."
        m 3eua "Sabia que todo tipo tem seu próprio valor verdade associado?"

    m 1eua "Todos os tipos têm um 'valor verdade' que varia conforme seu conteúdo."



    m "Podemos verificar usando a palavra-chave {b}bool{/b}."

    show monika at t22
    show screen mas_py_console_teaching

    m 3eua "Vamos começar com valores verdade para inteiros."
    call mas_wx_cmd ("bool(10)")
    call mas_wx_cmd ("bool(-1)")
    m 3eua "Inteiros não-nulos têm valor {b}True{/b}."
    call mas_wx_cmd ("bool(0)")
    m 3eub "Já zero tem valor {b}False{/b}."

    m 1eua "Floats seguem a mesma regra:"
    call mas_wx_cmd ("bool(10.02)")
    call mas_wx_cmd ("bool(0.14)")
    call mas_wx_cmd ("bool(0.0)")

    m 1eua "Agora strings:"
    call mas_wx_cmd ('bool("string com texto")')
    call mas_wx_cmd ('bool("  ")')
    m 3eub "Strings com texto, mesmo só espaços, valem {b}True{/b}."
    call mas_wx_cmd ('bool("")')
    m "Strings vazias valem {b}False{/b}."

    m 1eua "Vejamos o {b}None{/b}:"
    call mas_wx_cmd ("bool(None)")
    m 1eub "{b}None{/b} sempre vale {b}False{/b}."



    m 1eua "Em comparações, esses valores são convertidos para booleanos primeiro."
    m 1hua "Vejamos exemplos:"
    m 3eua "Primeiro, criando variáveis:"
    call mas_wx_cmd ("num10 = 10")
    call mas_wx_cmd ("num0 = 0")
    call mas_wx_cmd ('text = "texto"')
    call mas_wx_cmd ('empty_text = ""')
    call mas_wx_cmd ("none_var = None")

    m 3eub "Agora algumas comparações:"
    call mas_wx_cmd ("bool(num10 and num0)")
    call mas_wx_cmd ("bool(num10 and text)")
    call mas_wx_cmd ("bool(empty_text or num0)")
    call mas_wx_cmd ("bool(none_var and text)")
    call mas_wx_cmd ("bool(empty_text or none_var)")

    m 1eua "Conhecer esses valores ajuda a escrever comparações mais eficientes."
    m 1hua "Mostrarei aplicações práticas nas próximas lições."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11
    m 1hua "Obrigada por acompanhar!"
    return
















label monika_ptod_tip010:

    return











init 495 image cn_frame = "mod_assets/console/cn_frame.png"
define -5 mas_ptod.font = mas_ui.MONO_FONT







init -5 style mas_py_console_text is console_text:
    font mas_ptod.font
init -5 style mas_py_console_text_cn is console_text_console:
    font mas_ptod.font






init -6 python in mas_ptod:
    import store.mas_utils as mas_utils


    SYM = ">>> "
    M_SYM = "... "


    cn_history = list()


    H_SIZE = 20


    cn_line = ""


    cn_cmd = ""


    blk_cmd = list()




    stack_level = 0




    indent_stack = list()


    VER_TEXT_1 = "Python {0}"
    VER_TEXT_2 = "{0} in MAS"


    LINE_MAX = 66



    STATE_SINGLE = 0


    STATE_MULTI = 1


    STATE_BLOCK = 2


    STATE_BLOCK_MULTI = 3


    STATE_OFF = 4


    state = STATE_SINGLE


    local_ctx = dict()


    def clr_cn():
        """
        SEE clear_console
        """
        clear_console()


    def ex_cn():
        """
        SEE exit_console
        """
        exit_console()


    def rst_cn():
        """
        SEE restart_console
        """
        restart_console()


    def w_cmd(cmd):
        """
        SEE write_command
        """
        write_command(cmd)


    def x_cmd(context):
        """
        SEE exec_command
        """
        exec_command(context)


    def wx_cmd(cmd, context):
        """
        Does both write_command and exec_command
        """
        w_cmd(cmd)
        x_cmd(context)


    def write_command(cmd):
        """
        Writes a command to the console

        NOTE: Does not EXECUTE
        NOTE: remove previous command
        NOTE: does NOT append to previously written command (unless that cmd
            is in a block and was executed)

        IN:
            cmd - the command to write to the console
        """
        if state == STATE_OFF:
            return
        
        global cn_line, cn_cmd, state, stack_level
        
        if state == STATE_MULTI:
            
            
            
            cn_cmd = ""
            cn_line = ""
            state = STATE_SINGLE
        
        elif state == STATE_BLOCK_MULTI:
            
            
            cn_cmd = ""
            cn_line = ""
            state = STATE_BLOCK
        
        
        
        cn_cmd = str(cmd)
        
        
        if state == STATE_SINGLE:
            
            sym = SYM
        
        else:
            
            sym = M_SYM
        
        
        prefixed_cmd = sym + cn_cmd
        
        
        cn_lines = _line_break(prefixed_cmd)
        
        if len(cn_lines) == 1:
            
            cn_line = cn_cmd
        
        else:
            
            
            
            _update_console_history_list(cn_lines[:-1])
            
            
            cn_line = cn_lines[len(cn_lines)-1]
            
            if state == STATE_SINGLE:
                
                state = STATE_MULTI
            
            else:
                
                state = STATE_BLOCK_MULTI


    def clear_console():
        """
        Cleares console hisotry and current line

        Also resets state to Single
        """
        global cn_history, cn_line, cn_history, state, local_ctx
        cn_line = ""
        cn_cmd = ""
        cn_history = []
        state = STATE_SINGLE
        local_ctx = {}


    def restart_console():
        """
        Cleares console history and current line, also sets up version text
        """
        global state
        import sys
        version = sys.version
        
        
        split_dex = version.find(")")
        start_lines = [


            VER_TEXT_1.format(version[:split_dex+1]),
            VER_TEXT_2.format(version[split_dex+2:])
        ]
        
        
        clear_console()
        _update_console_history_list(start_lines)
        
        
        state = STATE_SINGLE


    def exit_console():
        """
        Disables the console
        """
        global state
        state = STATE_OFF


    def _m1_script0x2dpython__exec_cmd(line, context, block=False):
        """
        Tries to eval the line first, then executes.
        Returns the result of the command

        IN:
            line - line to eval / exec
            context - dict that represnts the current context. should be locals
            block - True means we are executing a block command and should
                skip eval

        RETURNS:
            the result of the command, as a string
        """
        if block:
            return _m1_script0x2dpython__exec_exec(line, context)
        
        
        return _m1_script0x2dpython__exec_evalexec(line, context)


    def _m1_script0x2dpython__exec_exec(line, context):
        """
        Runs exec on the given line
        Returns an empty string or a string with an error if it occured.

        IN:
            line - line to exec
            context - dict that represents the current context

        RETURNS:
            empty string or string with error message
        """
        try:
            exec(line, context)
            return ""
        
        except Exception as e:
            return _exp_toString(e)


    def _m1_script0x2dpython__exec_evalexec(line, context):
        """
        Tries to eval the line first, then executes.
        Returns the result of the command

        IN:
            line - line to eval / exec
            context - dict that represents the current context.

        RETURNS:
            the result of the command as a string
        """
        try:
            return str(eval(line, context))
        
        except:
            
            return _m1_script0x2dpython__exec_exec(line, context)


    def exec_command(context):
        """
        Executes the command that is currently in the console.
        This is basically pressing Enter

        IN:
            context - dict that represnts the current context. You should pass
                locals here.
                If None, then we use the local_ctx.
        """
        if state == STATE_OFF:
            return
        
        if context is None:
            context = local_ctx
        
        global cn_cmd, cn_line, state, stack_level, blk_cmd
        
        
        
        
        block_mode = state == STATE_BLOCK or state == STATE_BLOCK_MULTI
        
        
        empty_line = len(cn_cmd.strip()) == 0
        
        
        time_to_block = cn_cmd.endswith(":")
        
        
        bad_block = time_to_block and len(cn_cmd.strip()) == 1
        
        
        full_cmd = None
        
        
        
        if empty_line:
            
            
            if block_mode:
                
                _m1_script0x2dpython__popi()
            
            else:
                
                
                _update_console_history(SYM)
                cn_line = ""
                cn_cmd = ""
                return
        
        if bad_block:
            
            
            full_cmd = cn_cmd
            stack_level = 0
            blk_cmd = list()
        
        elif time_to_block:
            
            blk_cmd.append(cn_cmd)
            
            if not block_mode:
                
                _m1_script0x2dpython__pushi(0)
            
            else:
                
                pre_spaces = _count_sp(cn_cmd)
                
                if _m1_script0x2dpython__peeki() != pre_spaces:
                    
                    
                    _m1_script0x2dpython__pushi(pre_spaces)
        
        elif block_mode:
            
            blk_cmd.append(cn_cmd)
            
            if stack_level == 0:
                
                full_cmd = "\n".join(blk_cmd)
                blk_cmd = list()
        
        else:
            
            
            
            full_cmd = cn_cmd
        
        
        
        
        if full_cmd is not None:
            result = _m1_script0x2dpython__exec_cmd(full_cmd, context, block_mode)
        
        else:
            result = ""
        
        
        
        if block_mode and empty_line:
            
            output = [M_SYM]
        
        else:
            
            if state == STATE_SINGLE:
                sym = SYM
            
            elif state == STATE_BLOCK:
                sym = M_SYM
            
            else:
                
                sym = ""
            
            output = [sym + cn_line]
        
        
        if len(result) > 0:
            output.append(result)
        
        
        cn_line = ""
        cn_cmd = ""
        _update_console_history_list(output)
        
        
        
        if bad_block:
            
            state = STATE_SINGLE
            block_mode = False
        
        elif time_to_block:
            
            state = STATE_BLOCK
            block_mode = True
        
        
        
        if (state == STATE_MULTI) or (block_mode and stack_level == 0):
            
            state = STATE_SINGLE
        
        elif state == STATE_BLOCK_MULTI:
            
            state = STATE_BLOCK


    def get_last_line():
        """
        Retrieves the last line from the console history

        RETURNS:
            last line from console history as a string
        """
        if len(cn_history) > 0:
            return cn_history[len(cn_history)-1]
        
        return ""


    def set_local_context(context):
        """
        Sets the local context to the given context.

        Stuff in the old context are forgotten.
        """
        global local_ctx
        local_ctx = context


    def _m1_script0x2dpython__pushi(indent_level):
        """
        Pushes a indent level into the stack

        IN:
            indent_level - indent to push into stack
        """
        global stack_level
        stack_level += 1
        indent_stack.append(indent_level)


    def _m1_script0x2dpython__popi():
        """
        Pops indent level from stack

        REUTRNS:
            popped indent level
        """
        global stack_level
        stack_level -= 1
        
        if stack_level < 0:
            stack_level = 0
        
        if len(indent_stack) > 0:
            indent_stack.pop()


    def _m1_script0x2dpython__peeki():
        """
        Returns value that would be popped from stack

        RETURNS:
            indent level that would be popped
        """
        return indent_stack[len(indent_stack)-1]


    def _exp_toString(exp):
        """
        Converts the given exception into a string that looks like
        how python interpreter prints out exceptions
        """
        err = repr(exp)
        err_split = err.partition("(")
        return err_split[0] + ": " + str(exp)


    def _indent_line(line):
        """
        Prepends the given line with an appropraite number of spaces, depending
        on the current stack level

        IN:
            line - line to prepend

        RETURNS:
            line prepended with spaces
        """
        return (" " * (stack_level * 4)) + line


    def _count_sp(line):
        """
        Counts number of spaces that prefix this line

        IN:
            line - line to cound spaces

        RETURNS:
            number of spaces at start of line
        """
        return len(line) - len(line.lstrip(" "))


    def _update_console_history(*new_items):
        """
        Updates the console history with the list of new lines to add

        IN:
            new_items - the items to add to the console history
        """
        _update_console_history_list(new_items)


    def _update_console_history_list(new_items):
        """
        Updates console history with list of new lines to add

        IN:
            new_items - list of new itme sto add to console history
        """
        global cn_history
        
        
        for line in new_items:
            broken_lines = _line_break(line)
            
            
            for b_line in broken_lines:
                
                cn_history.append(b_line)
        
        if len(cn_history) > H_SIZE:
            cn_history = cn_history[-H_SIZE:]


    def _line_break(line):
        """
        Lines cant be too large. This will line break entries.

        IN:
            line - the line to break

        RETURNS:
            list of strings, each item is a line.
        """
        if len(line) <= LINE_MAX:
            return [line]
        
        
        broken_lines = list()
        while len(line) > LINE_MAX:
            broken_lines.append(line[:LINE_MAX])
            line = line[LINE_MAX:]
        
        
        broken_lines.append(line)
        return broken_lines


init -505 screen mas_py_console_teaching():

    frame:
        xanchor 0
        yanchor 0
        xpos 5
        ypos 5
        background "mod_assets/console/cn_frame.png"

        has fixed
        python:
            starting_index = len(store.mas_ptod.cn_history) - 1
            cn_h_y = 413
            cn_l_x = 41


        for index in range(starting_index, -1, -1):
            $ cn_line = store.mas_ptod.cn_history[index]
            text "[cn_line]":
                style "mas_py_console_text"
                anchor (0, 1.0)
                xpos 5
                ypos cn_h_y
            $ cn_h_y -= 20


        if store.mas_ptod.state == store.mas_ptod.STATE_SINGLE:
            text ">>> ":
                style "mas_py_console_text"
                anchor (0, 1.0)
                xpos 5
                ypos 433

        elif store.mas_ptod.state == store.mas_ptod.STATE_BLOCK:
            text "... ":
                style "mas_py_console_text"
                anchor (0, 1.0)
                xpos 5
                ypos 433

        else:

            $ cn_l_x = 5


        if len(store.mas_ptod.cn_line) > 0:
            text "[store.mas_ptod.cn_line]":
                style "mas_py_console_text_cn"
                anchor (0, 1.0)
                xpos cn_l_x
                ypos 433


label mas_w_cmd(cmd, wait=0.7):
    $ store.mas_ptod.w_cmd(cmd)
    $ renpy.pause(wait, hard=True)
    return


label mas_x_cmd(ctx=None, wait=0.7):
    $ store.mas_ptod.x_cmd(ctx)
    $ renpy.pause(wait, hard=True)
    return


label mas_wx_cmd(cmd, ctx=None, w_wait=0.7, x_wait=0.7):
    $ store.mas_ptod.w_cmd(cmd)
    $ renpy.pause(w_wait, hard=True)
    $ store.mas_ptod.x_cmd(ctx)
    $ renpy.pause(x_wait, hard=True)
    return


label mas_wx_cmd_noxwait(cmd, ctx=None):
    call mas_wx_cmd (cmd, ctx, x_wait=0.0)
    return
