init offset = 5













init -1 python in mas_gtod:

    import datetime
    import store.evhand as evhand

    M_GTOD = "monika_gtod_tip{:0>3d}"

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
        
        tip_ev = evhand.event_database.get(
            M_GTOD.format(tip_num),
            None
        )
        
        return (
            tip_ev is not None
            and tip_ev.last_seen is not None
            and tip_ev.timePassedSinceLastSeen_d(datetime.timedelta(days=1))
        )


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip000",
            category=["dicas de gramática"],
            prompt="Pode me ensinar sobre gramática?",
            pool=True,
            rules={"bookmark_rule": store.mas_bookmarks_derand.BLACKLIST}
        )
    )

label monika_gtod_tip000:
    m 3eub "É claro que posso te ensinar sobre gramática, [player]!"
    m 3hua "Me deixa muito feliz saber que você quer melhorar suas habilidades de escrita."
    m 1eub "Eu na verdade estive revisando alguns livros sobre escrita e acho que tem algumas coisas interessantes sobre as quais podemos falar!"
    m 1rksdla "Tenho que admitir...{w=0.5} é meio estranho discutir algo tão específico quanto gramática."
    m 1rksdlc "Sei que não é a coisa mais empolgante que surge na mente das pessoas."
    m 3eksdld "...Talvez você pense em professores rigorosos, ou editores arrogantes..."
    m 3eka "Mas eu acho que há uma certa beleza em dominar a forma que você escreve e entregar de forma eloquente sua mensagem."
    m 1eub "Então...{w=0.5} começando hoje, irei compartilhar as dicas de gramática do dia da Monika!"
    m 1hua "Vamos melhorar nossa escrita [ju], meu amor~"
    m 3eub "Vamos começar com orações, os elementos básicos das sentenças!"


    $ mas_hideEVL("monika_gtod_tip000", "EVE", lock=True, depool=True)


    $ tip_label = "monika_gtod_tip001"
    $ mas_showEVL(tip_label, "EVE", unlock=True, _pool=True)
    $ pushEvent(tip_label,skipeval=True)
    return



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip001",
            category=["dicas de gramática"],
            prompt="Orações"
        )
    )

label monika_gtod_tip001:
    m 3eud "Você provavelmente já deve saber disso, mas uma oração é um grupo de palavras que possui um sujeito e uma ação, ou predicado."
    m 1euc "Na maior parte, orações podem ser classificadas em orações coordenadas ou subordinadas."
    m 1esd "Orações coordenadas conseguem se manter sozinhas como sentenças, como na sentença '{b}Eu escrevi isso.{/b}'"
    m 3euc "Orações subordinadas, por outro lado, não conseguem se manter sozinhas e geralmente aparecem como parte de sentenças maiores."
    m 3eua "Um exemplo seria '{b}o qual a salvou.{/b}'"
    m 3eud "Há um sujeito, '{b}o qual{/b},' uma ação, '{b}a salvou{/b},' mas é claro, a oração não pode ser uma sentença sozinha."
    m 1ekbsa "...{w=0.5}Acho que sei como terminar essa sentença, [player]~"
    m 3eub "Certo, isso é tudo por hoje. Obrigada por ouvir!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip002",
            category=["dicas de gramática"],
            prompt="Erros de Vírgula",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(1)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip002:
    m 1eua "Se lembra quando falamos sobre orações, [player]?"
    m 1eud "Há um erro muito comum que muitos escritores cometem ao juntar elas."
    m 3esc "Quando você junta duas orações, pode acabar cometendo um erro com a vírgula."
    m 3esa "Veja um exemplo:{w=0.5} '{b}Eu visitei o parque, eu olhei para o céu, eu vi muitas estrelas.{/b}"
    m 1eua "Isso pode não parecer um problema, mas imagine adicionar mais e mais orações a essa sentença..."
    m 3wud "O resultado seria uma bagunça!"
    m 1esd "'{b}Eu visitei o parque, eu olhei para o céu, eu vi muitas estrelas, eu vi algumas constelações, uma delas parecia um caranguejo{/b}...'{w=0.5} Isso pode continuar infinitamente."
    m 1eua "A melhor forma de evitar este erro é separar orações independentes com um ponto, conjunções, ou ponto e vírgula."
    m 1eud "Uma conjunção é basicamente uma palavra que você usa para conectar duas orações ou frases juntas."
    m 3eub "Esse é um assunto bem interessante, podemos falar sobre ele em nossa sentença fluir melhor..."
    m 3eud "Enfim, usando o exemplo que dei antes, vamos adicionar uma conjunção e um ponto para fazer uma dica futura!"
    m 1eud "'{b}Eu visitei o parque, e olhei para o céu. Eu vi muitas estrelas.{/b}'"
    m 3hua "Bem melhor, não acha?"
    m 1eub "Isso é tudo por hoje, [player]."
    m 3hub "Obrigada por ouvir!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip003",
            category=["dicas de gramática"],
            prompt="Conjunções",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(2)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip003:
    m 1eub "Certo, [player]! Acho que é hora de falarmos sobre...{w=0.5} conjunções!"
    m 3esa "Como eu disse antes, conjunções são palavras ou frases que unem duas ideias."
    m 3wud "Quando você pensa nisso, é uma categoria enorme! Há tantas palavras que podemos usar para isso."
    m 1euc "Só imagine falar sem conjunções..."
    m 1esc "Seria sem graça.{w=0.3} Você iria parecer agitado.{w=0.3} Essas ideias estão todas relacionadas.{w=0.3} Deveríamos as conectar."
    m 3eua "Como você irá notar, conjunções são ótimas para combinar ideias e, ao mesmo tempo, elas fazem sua escrita parecer fluída e similar a forma que falamos."
    m 1eua "Agora, vamos revisitar nosso exemplo de antes, desta vez com conjunções..."
    m 1eub "'{b}Seria sem graça e você pareceria agitado. Já que essas ideias estão todas relacionadas, nós deveríamos as conectar.{/b}'"
    m 3hua "Bem melhor, não acha?"
    m 1esa "Enfim, há dois tipos de conjunções:{w=0.5} coordenativas e subordinativas."
    m 1hksdla "O nome delas pode parecer um pouco complicado, mas prometo que farão mais sentido em breve. Darei exemplos conforme formos avançando."
    m 1esd "As conjunções coordenativas ligam duas palavras, frases, ou orações do mesmo 'nível'. Isso significa que elas precisam ser do mesmo tipo... palavras com palavras, ou orações com orações."
    m 3euc "Alguns exemplos comuns incluem:{w=0.5} '{b}e{/b},' '{b}ou{/b},' '{b}mas{/b},' '{b}então{/b},' e '{b}ainda{/b}.'"
    m 3eub "Você pode conectar duas orações independentes, {i}e{/i} você pode evitar erros de vírgula!"
    m 1esd "Como você pode imaginar, há muitas formas de se fazer isso."
    m 3euc "Alguns pares comuns são:{w=0.5} '{b}qualquer{/b}/{b}ou{/b},' '{b}ambos{/b}/{b}e{/b},' e '{b}se{/b}/{b}ou{/b}.'"
    m 3eub "{i}Se{/i} você percebe isso {i}ou {/i} não, nós os usamos o tempo todo ... como nesta frase!"
    m 1esd "Por fim, as conjunções subordinadas reúnem cláusulas independentes e dependentes."
    m 3eub "Como você pode imaginar, há muitas maneiras de fazer isso!"
    m 3euc "Exemplos inclue:{w=0.5} '{b}embora{/b},' '{b}até{/b},' '{b}já que{/b},' '{b}no entanto{/b},' e '{b}portanto{/b}.'"
    m 3eub "{i}Já que{/i} há tantas, esta categoria de conjunções é a maior!"
    m 3tsd "Ah, e outra coisa...{w=0.5} Um erro muito comum é dizerem que você não pode começar sentenças com conjunções."
    m 3hub "Como eu acabei de demonstrar, você definitivamente pode, ahaha!"
    m 1rksdla "Mas evite exagerar. Ou vai parecer muito forçado."
    m 1eub "Acho que isso é tudo por hoje, [player]."
    m 3hub "Obrigada por ouvir!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip004",
            category=["dicas de gramática"],
            prompt="Ponto e Vírgula",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(3)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip004:
    m 1eua "Hoje vamos falar sobre uma pontuação raramente usada e normalmente mal compreendida..."
    m 3eub "O ponto e vírgula!"
    m 3eua "Algumas coisas interessantes foram escritas sobre o ponto e vírgula, incluindo isto do autor Lewis Thomas..."
    m 1esd "'{i}Às vezes, você tem um vislumbre de um ponto e vírgula chegando, algumas linhas adiante, e é como subir um caminho íngreme pela floresta e ver um banco de madeira à frente{/i}...'"
    m 1esa "'{i}...um lugar onde você pode se sentar por um tempo, recuperar o fôlego.{/i}'"
    m 1hua "Eu aprecio o quão eloquente ele descreve algo tão simples como uma pontuação!"
    m 1euc "Algumas pessoas acham que você pode usar um ponto e vírgula como um substituto para os dois pontos, enquanto outros o tratam como um ponto..."
    m 1esd "Se você se lembrar de nossa conversa sobre orações, o ponto e vírgula serve, na verdade, para conectar duas orações coordenadas."
    m 3euc "Por exemplo, se eu quiser ligar duas ideias, como '{b}Você está aqui{/b}' e '{b}eu estou feliz{/b},' eu poderia escrever como..."
    m 3eud "'{b}Você está aqui; eu estou feliz{/b}' em vez de '{b}Você está aqui, e eu estou feliz{/b}' ou '{b}Você está aqui. Eu estou feliz{/b}.'"
    m 1eub "Todas as três sentenças passam a mesma mensagem mas, em comparação, '{b}Você está aqui; eu estou feliz{/b}' conecta as duas orações de uma forma natural."
    m 1esa "No final, isto sempre depende das ideias que você deseja conectar, mas acho que Thomas explicou bem quando você as compara com pontos ou vírgulas."
    m 1eud "Ao contrário de um ponto, o qual abre para uma sentença completamente diferente, ou uma vírgula, a qual mostra que a mais por vir na sentença atual..."
    m 3eub "Um ponto e vírgula é um intermediário, ou, como Thomas diz, '{i}um lugar onde você pode se sentar por um tempo, recuperar o fôlego.{/i}'"
    m 1esa "Ao menos isso te dá uma outra opção; espero que agora você faça um bom uso do ponto e vírgula quando estiver escrevendo..."
    m 1hua "Ehehe."
    m 1eub "Certo, isso já é o bastante por hoje, [player]."
    m 3hub "Obrigada por ouvir!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip005",
            category=["dicas de gramática"],
            prompt="Sujeitos e Objetos",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(4)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip005:
    m 1eua "Hoje vamos falar sobre sujeitos e objetos, [player]."
    m 1eud "Se lembra quando falei sobre orações terem uma ação e um verbo?"
    m 3eub "O objeto é a pessoa ou coisa sobre a qual o sujeito age!"
    m 1eua "Então, na sentença '{b}Nós assistimos os fogos de artifício [ju]{/b},' o objeto seria... {w=0.5}os '{b}fogos de artifício{/b}.'"
    m 3esd "Ah, é importante observar que objetos não são necessários para formar sentenças completas..."
    m 1eua "A sentença poderia muito bem ter sido, '{b}Nós assistimos.{/b}'"
    m 3hksdlb "Essa é uma sentença completa... embora seja ambígua, ahaha!"
    m 1eud "Também não é obrigatório que o objeto venha por último, mas irei falar sobre isso em mais detalhes outra hora."
    m 3esa "Apenas lembre-se que o sujeito está realizando a ação e o objeto está sofrendo ela."
    m 1eub "Certo, isso é tudo por hoje..."
    m 3hub "Obrigada por ouvir, [player]! Eu amo."
    m 1eua "..."
    m 1tuu "..."
    m 3hub "Você!"
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip006",
            category=["dicas de gramática"],
            prompt="Vozes Ativas e Passivas",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(5)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip006:
    m 1eud "[player], você sabe sobre as vozes na escrita?"
    m 3eua "Há a voz ativa e a voz passiva."
    m 3euc "Se você se lembra de nossa conversa sobre sujeitos e objetos, a grande diferença entre as duas vozes é se o sujeito ou o objeto vem primeiro."
    m 1esd "Vamos dizer que o sujeito é a '{b}Sayori{/b}' e o objeto é um '{b}cupcake{/b}.'"
    m 3eud "Aqui está a sentença em voz ativa:{w=0.5} '{b}Sayori comeu o último cupcake.{/b}'"
    m 3euc "Aqui está ela novamente em voz passiva:{w=0.5} '{b}O último cupcake foi comido.{/b}'"
    m 1eub "Como você pode ver, você podar usar a voz passiva para manter em segredo o sujeito, ainda que tendo uma sentença completa."
    m 1tuu "É verdade; você {i}pode{/i} usar a voz passiva para ser sorrateiro!{w=0.5} Mas também há outros usos."
    m 3esd "Por exemplo, em alguns empregos, as pessoas precisam usar a voz passiva para serem impessoais."
    m 3euc "Cientistas descrevem experimentos com '{b}os resultados foram documentados{/b}...' já que a parte importante é o trabalho deles e não quem o fez."
    m 1esa "Enfim, fique com a voz a voz ativa para ter uma melhor leitura e, você sabe, para dizer diretamente quem está fazendo o quê."
    m 1eub "Acho que isso é o bastante por hoje, [player]."
    m 3hub "Obrigada por ouvir!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip007",
            category=["dicas de gramática"],
            prompt="Mas e Mais",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(6)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip007:
    m 1eua "Hoje vamos falar sobre algo que costuma causar bastante confusão... o uso de '{b}mas{/b}' e '{b}mais{/b}'."
    m 3hub "É impressionante como essas duas palavrinhas tão parecidas podem deixar tanta gente em dúvida, ahaha."
    m 1esd "'{b}Mas{/b}' é usado quando queremos indicar uma oposição, uma ideia contrária ao que foi dito antes."
    m 3eub "Já o '{b}mais{/b}' está relacionado à ideia de quantidade ou intensidade. Ele é o oposto de 'menos'."
    m 1eua "Parece complicado? Não se preocupe, tem um truque bem fácil pra diferenciar!"
    m 3euc "Tente substituir '{b}mas{/b}' por palavras como '{b}porém{/b}', '{b}contudo{/b}', '{b}todavia{/b}' ou '{b}entretanto{/b}'."
    m 1eud "Se fizer sentido, então é '{b}mas{/b}'."
    m 3eua "Agora, se for '{b}mais{/b}', tente trocar por '{b}menos{/b}'."
    m 1eua "A substituição que fizer sentido indica qual palavra usar!"
    m 3eua "Vamos ver um exemplo: {i}Ela gosta de cupcake, mas não de verdura.{/i}"
    m 3esd "Se trocarmos o '{b}mas{/b}' na frase '{b}mas não de verdura{/b}', teremos duas opções..."
    m 1esd "'{b}Contudo, não de verdura{/b}' ou '{b}Menos não de verdura{/b}'."
    m 3euc "Só a primeira faz sentido, né? Então, o correto ali é '{b}mas{/b}'."
    m 1hua "Viu só? Escrever bem pode ser mais fácil do que parece!"
    m 1eub "Isso é tudo por hoje, [player]."
    m 3hub "Obrigada por me ouvir~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip008",
            category=["dicas de gramática"],
            prompt="Há vs. A",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(7)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip008:
    m 1eua "Da última vez, falamos sobre a diferença entre '{b}mas{/b}' e '{b}mais{/b}'."
    m 1esd "Hoje, vamos ver outra confusão bem comum: quando usar '{b}há{/b}' e quando usar '{b}a{/b}'."
    m 3etc "Por exemplo, qual das frases está certa? '{b}Te conheço há muito tempo{/b}' ou '{b}Te conheço a muito tempo{/b}'?"
    m 3eud "As duas parecem parecidas, mas só uma está correta!"
    m 1esd "A forma '{b}há{/b}' vem do verbo '{b}haver{/b}', e é usada para indicar {i}tempo passado{/i}."
    m 1euc "Ou seja, '{b}há muito tempo{/b}' significa '{i}faz muito tempo{/i}'."
    m 3eub "Então o certo é: '{b}Te conheço há muito tempo{/b}'."
    m 1hua "Fácil, né? Basta lembrar que, se dá pra trocar por '{b}faz{/b}', o correto é '{b}há{/b}'."
    m 3eua "Agora, o '{b}a{/b}' sem o H é usado para indicar {i}distância ou tempo futuro{/i}."
    m 1eub "Por exemplo: '{b}Daqui a duas horas{/b}' ou '{b}A festa é daqui a uma semana{/b}'."
    m 1eua "Viu só? Nesse caso, não dá pra dizer '{b}daqui há duas horas{/b}', porque o evento ainda vai acontecer."
    m 3tuu "Parece detalhe bobo, mas faz toda a diferença quando a gente escreve direitinho, né?"
    m 1hua "Espero que essa dica te ajude a nunca mais errar entre '{b}há{/b}' e '{b}a{/b}', [player]~"
    m 3hub "Por hoje é só. Obrigada por me ouvir~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip009",
            category=["dicas de gramática"],
            prompt="Apóstrofo em Inglês",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(8)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )


label monika_gtod_tip009:
    if player[-1].lower() == 's':
        $ tempname = player
    else:
        $ tempname = 'Alexis'

    m 1eua "Hoje vamos mudar um pouco e falar sobre a gramática da língua Inglesa. Vamos falar do apóstrofo."
    m 3eua "Eles servem para mostrar possessão: '{b}Sayori’s fork (garfo da Sayori), Natsuki’s spoon (colher da Natsuki), Yuri’s knife (faca da Yuri){/b}...'"
    m 1esd "Acho que o problema é quando você precisa adicionar um apóstrofo a uma palavra que termina com '{b}s{/b}.'"
    m 3eub "Para palavras no plural, isto é simples; adicione apenas o apóstrofo no final:{w=0.5} '{b}monkeys’ (do macaco){/b}.'"
    m 1hksdla "Está bem claro que '{b}monkey’s{/b}' indicaria que a possessão é de apenas um macaco, e '{b}monkeys’s{/b}' estaria errado."
    m 1eud "Só que surge outro problema quando se trata do nome de pessoas terminados com '{b}s{/b}', como '{b}Sanders{/b}' ou '{b}[tempname]{/b}.'"
    m 1euc "Em alguns guias que eu li, parece que normalmente adicionamos um apóstrofo e o '{b}s{/b}', com exceção de nomes históricos, como '{b}Sófocles{/b}' ou '{b}Zeus{/b}.'"
    m 3eub "Pessoalmente, eu acho que o mais importante aqui é consistência!"
    m 3esd "Se você for usar '{b}[tempname]’{/b},' então não tem problema, desde que você use '{b}[tempname]’{/b}' no texto inteiro."
    m 1tuu "Isso é mais importante do que honrar alguns Gregos antigos."
    m 3eud "Uma exceção interessante é o caso do '{b}its{/b}' versus o '{b}it’s{/b}.'"
    m 3etc "Você pode pensar que a forma possessiva do '{b}it{/b}' seria apenas adicionar um apóstrofo, o transformando em '{b}it’s{/b},' certo?"
    m 3euc "Normalmente isso seria correto, mas neste caso, a forma possessiva do '{b}it{/b}' é simplesmente '{b}its{/b}.'"
    m 1esd "Isto aconteceu porque o '{b}it’s{/b}' é reservado para a forma contraída de '{b}it is{/b}.'"
    m 1eua "Caso esteja se perguntando, uma forma contraída é simplesmente uma versão abreviada de uma palavra, com um apóstrofo indicando onde as letras foram cortadas."
    m 1eub "Certo, [player], isso é tudo que tenho por hoje."
    m 3hub "Ehehe. Obrigada por ouvir!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip010",
            category=["dicas de gramática"],
            prompt="A Vírgula de Oxford",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(9)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip010:
    m 3eud "Você sabia que existe um debate sobre o local de uma vírgula específica em um alista de três itens?"
    m 3eub "Isto é chamado de vírgula de Oxford, e pode mudar completamente o significado de uma sentença!"
    m 1esa "Deixe-me te mostrar o que estou querendo dizer..."
    m 1hub "Com a vírgula de Oxford, eu diria '{b}Eu amo o [player], dia, e noite.{/b}'"
    m 1eua "Em a vírgula de Oxford, eu diria '{b}Eu amo o [player], dia e noite.{/b}'"
    m 3eud "A confusão se encontra em se estou querendo dizer que amo três coisas separadas, ou se estou me referindo que amo você, sendo dia ou noite."
    m 3hub "É claro, ambos esses significados são verdadeiros, então não há nenhuma confusão para mim, ahaha!"
    m 1eua "Isso é tudo por hoje, [player]."
    m 3hub "Obrigada por ouvir!"
    return
