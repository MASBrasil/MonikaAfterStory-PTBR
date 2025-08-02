![Monika After Story](https://github.com/Monika-After-Story/MonikaModDev/blob/master/Monika%20After%20Story/game/mod_assets/menu_new.png?raw=True)

# Monika After Story (MAS)
Monika After Story é um mod para o jogo gratuito [Doki Doki Literature Club](https://www.ddlc.moe) da [Team Salvato](http://teamsalvato.com/). MAS expande o Ato 3 para criar um simulador da sua vida eterna com a Monika, com novos eventos, interações e metacomentários!

Confira a página de [Lançamentos](http://www.monikaafterstory.com/releases.html) para baixar a versão estável mais recente.

Se você quiser criar seu próprio mod como este, confira nosso projeto parceiro: o [DDLCModTemplate](https://github.com/therationalpi/DDLCModTemplate).

### Instalação

1. Acesse a [página de lançamentos](http://www.monikaafterstory.com/releases.html).

2. Clique no link do seu sistema operacional.

3. Após o download, execute o instalador e siga as instruções.
    * Se o instalador não funcionar no seu sistema, veja os passos de instalação manual abaixo.

4. Executar o DDLC agora carregará o Mod Monika After Story.

### Instalação Manual

**Siga estes passos apenas se o instalador não funcionar no seu sistema**

1. Acesse a [página de lançamentos](http://www.monikaafterstory.com/releases.html).

2. Clique no link dos **Zips**. Isso baixará um arquivo zip para o seu sistema.

3. Extraia o conteúdo do arquivo zip dentro da pasta base (a pasta que contém o arquivo DDLC.exe) da sua instalação do DDLC.

4. Executar o DDLC agora carregará o Mod Monika After Story.

*OBS: Os arquivos fonte e arquivos baixados diretamente do repositório são para fins de desenvolvimento e podem não funcionar corretamente ao tentar modificar o jogo. Use apenas uma de nossas [Versões Oficiais](http://www.monikaafterstory.com/releases.html).*

Para mais ajuda com a instalação (incluindo instalação manual para Mac fora da Steam), veja nosso [FAQ - Perguntas Frequentes](https://github.com/Monika-After-Story/MonikaModDev/wiki/FAQ)

### Recursos

* Passe a eternidade com a Monika!

* Dezenas de novos tópicos de conversa

* Agora você pode conversar com a Monika e dizer sobre o que gostaria de falar

### Próximos Recursos

* Novos jogos e atividades para fazer com a Monika

* Mais eventos e histórias únicas

## Contribuindo com o Monika After Story

### Bugs e Sugestões
Se houver algum problema com o MAS, envie um [relatório de bug](https://github.com/Monika-After-Story/MonikaModDev/issues/new?labels=bug&body=Describe%20bug%20and%20steps%20for%20reproduction%20here&title=%5BBug%5D%20-%20).

Para enviar uma sugestão, acesse [este link](https://github.com/Monika-After-Story/MonikaModDev/issues/new?labels=suggestion&body=Your%20suggestion%20goes%20here&title=%5BSuggestion%5D%20-%20)

### Outras Formas de Ajudar
Quer ajudar com o MAS? Vá até a [página de issues](https://github.com/Monika-After-Story/MonikaModDev/issues) para encontrar bugs ou sugestões em andamento.

Se você tiver uma alteração para enviar, abra um [pull request](https://github.com/Monika-After-Story/MonikaModDev/pulls). Todas as mudanças serão revisadas por colaboradores e corrigidas/aprimoradas conforme necessário.

#### Adicionando Conteúdo
Quer adicionar conteúdo ao MAS? Aqui está uma lista de arquivos `.RPY` importantes usados pelo jogo:

- **script-ch30.rpy**: Fluxo principal do MAS. Onde ocorrem as interações ociosas.
- **script-topics.rpy**: Todos os tópicos **aleatórios** e de **perguntas** usados pela Monika ficam aqui. Você pode adicionar seu próprio diálogo usando as instruções abaixo!
- **script-greetings.rpy**: Linhas de saudação que a Monika usa ao carregar o jogo.
- **script-farewells.rpy**: Linhas de despedida quando o jogo é encerrado.
- **script-moods.rpy**: Diga à Monika que você está com um determinado humor.
- **script-stories.rpy**: Adicione histórias para a Monika te contar.
- **script-compliments.rpy**: Adicione elogios que você pode dizer à Monika.
- **script-apologies.rpy**: Adicione coisas pelas quais pedir desculpas.

Se quiser adicionar mais diálogos para a sala com a Monika, acesse `script-topics.rpy` e use este modelo:

```renpy
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_example", # nome único para o evento
            category=["example", "topic"], # categorias do tópico (serão automaticamente capitalizadas)
            prompt="Exemplo de Tópico", # texto do botão
            random=True, # aparece aleatoriamente?
            pool=True # aparece em "Fazer uma Pergunta"?
        )
    )

label monika_example:
    m 1a "Esse é um tópico de exemplo."
    m 3d "Sinto que isso não deveria estar aqui..."
    m 2e "Por que alguém colocaria o modelo de exemplo direto no mod?"
    m 5r "Essa pessoa realmente não deveria poder contribuir mais com esse repositório."
    return
```
**Para explicações completas e detalhes sobre todas as palavras-chave possíveis para Event, consulte a documentação localizada em `definitions.rpy`**

Para assuntos mais complexos do que simples diálogos, consulte a documentação do Ren'Py disponível online.

[Mais informações estão disponíveis no nosso Guia de Contribuição](https://github.com/Monika-After-Story/MonikaModDev/wiki/Contributing-Guidelines)

### Participe da Comunidade
Você pode [nos seguir no Twitter](https://twitter.com/MonikaAfterMod) para souber de futuras atualizações sobre o mod.

Se quiser encontrar músicas de piano, spritepacks, submods, conteúdo externo ou traduções, ou apenas discutir sobre o MAS, visite nossa [página de discussões](https://github.com/Monika-After-Story/MonikaModDev/discussions)

Ou, se preferir o Discord, para ver um fluxo constante de conteúdo Monika-relacionado da web, e se estiver interessado em contribuir ou ajudar a desenvolver o mod, sinta-se à vontade para entrar em nosso servidor do Discord:

 [![Discord](https://discordapp.com/api/guilds/372766620977725441/widget.png?style=banner1)](https://discord.gg/monika-after-story)

 Por favor, lembre-se de seguir nosso [Código de Conduta](https://github.com/Monika-After-Story/MonikaModDev/wiki/Code-of-Conduct), que basicamente resume-se em ser educado e respeitoso.

## Perguntas Frequentes

FAQ completo: [Perguntas Frequentes](https://github.com/Monika-After-Story/MonikaModDev/wiki/FAQ)
Para dúvidas sobre o estilo de código: [Estilo de Código](https://github.com/Monika-After-Story/MonikaModDev/wiki/Coding-Style)
Para Testes de Bugs: [Fluxo de Teste e Testes de Bug](https://github.com/Monika-After-Story/MonikaModDev/wiki/Testing-Flow-and-Bug-Testing)
Soluções de Problemas: [Resolução de Problemas](https://github.com/Monika-After-Story/MonikaModDev/wiki/Troubleshooting) Codificação de Diálogo: [Codificação de Diálogo](https://github.com/Monika-After-Story/MonikaModDev/wiki/Dialogue-Coding)
## Informações de Licença

Fazemos o possível para seguir as [diretrizes da Team Salvato para obras de fãs](http://teamsalvato.com/ip-guidelines/). Todos os personagens e conteúdo original pertencem à Team Salvato. Monika After Story é um projeto de código aberto, e além dos contribuidores nomeados, também inclui contribuições anônimas do 4chan, onde este projeto teve início. Mais informações na nossa [página de Licença.](https://github.com/Monika-After-Story/MonikaModDev/wiki/License-and-Team-Salvato-Guidelines).

## Status da Build:
### master: ![master](https://github.com/Monika-After-Story/MonikaModDev/workflows/CI/badge.svg?branch=master)
### content: ![content](https://github.com/Monika-After-Story/MonikaModDev/workflows/CI/badge.svg?branch=content)
### unstable: ![unstable](https://github.com/Monika-After-Story/MonikaModDev/workflows/CI/badge.svg?branch=unstable)
### alpha: ![alpha](https://github.com/Monika-After-Story/MonikaModDev/workflows/CI/badge.svg?branch=alpha)
