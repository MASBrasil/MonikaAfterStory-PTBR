















init python:


    def mas_open_extra_menu():
        """
        Jumps to the extra menu workflow
        """
        renpy.jump("mas_extra_menu")





















































init -1 python in mas_extramenu:
    import store

    menu_visible = False

init -1 python:
    if not persistent._mas_gender or persistent._mas_gender not in ["M", "F", "X"]:
        persistent._mas_gender = "M"


label mas_extra_menu:
    $ store.mas_extramenu.menu_visible = True
    $ prev_zoom = store.mas_sprites.zoom_level


    $ mas_RaiseShield_core()

    if not persistent._mas_opened_extra_menu:
        call mas_extra_menu_firsttime

    $ persistent._mas_opened_extra_menu = True

    show screen mas_extramenu_area
    jump mas_idle_loop

label mas_extra_menu_close:
    $ store.mas_extramenu.menu_visible = False
    hide screen mas_extramenu_area

    if store.mas_sprites.zoom_level != prev_zoom:
        call mas_extra_menu_zoom_callback


    if store.mas_globals.in_idle_mode:
        $ mas_coreToIdleShield()
    else:
        $ mas_DropShield_core()

    show monika idle

    jump ch30_loop

label mas_idle_loop:
    pause 10.0
    jump mas_idle_loop

default persistent._mas_opened_extra_menu = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_extra_menu_firsttime",
            prompt="Você poderia me explicar o menu Extras?",
            category=["diversos"]
        )
    )

label mas_extra_menu_firsttime:
    if not persistent._mas_opened_extra_menu:
        m 1hua "Seja bem-[vn] ao menu Extras, [player]!"

    m 1eua "Aqui é onde vou adicionar coisas que não são jogos, tipo interações especiais que você pode fazer com o mouse."
    m "Você também pode abrir este menu pressionando a tecla 'E'."

    if not persistent._mas_opened_extra_menu:
        m 1hua "Espere por coisas bem legais neste menu!"

    $ mas_setEVLPropValues(
        "mas_extra_menu_firsttime",
        unlocked=True,
        pool=True
    )


    call mas_extra_menu_zoom_intro

    return




label mas_extra_menu_zoom_intro:
    m 1eua "Uma coisa que eu adicionei foi uma forma de você ajustar seu campo de visão, então agora você pode ficar mais perto ou mais longe de mim."
    m 1eub "Você pode ajustar isso usando a barra deslizante na seção 'Zoom' do menu Extras."
    return

default persistent._mas_pm_zoomed_out = False
default persistent._mas_pm_zoomed_in = False
default persistent._mas_pm_zoomed_in_max = False

label mas_extra_menu_zoom_callback:
    $ import store.mas_sprites as mas_sprites
    $ aff_larger_than_zero = _mas_getAffection() > 0


    if mas_sprites.zoom_level < mas_sprites.default_zoom_level:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_out
            ):

            call mas_extra_menu_zoom_out_first_time
            $ persistent._mas_pm_zoomed_out = True

    elif mas_sprites.zoom_level == mas_sprites.max_zoom:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_in_max
            ):

            call mas_extra_menu_zoom_in_max_first_time
            $ persistent._mas_pm_zoomed_in_max = True
            $ persistent._mas_pm_zoomed_in = True

    elif mas_sprites.zoom_level > mas_sprites.default_zoom_level:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_in
            ):

            call mas_extra_menu_zoom_in_first_time
            $ persistent._mas_pm_zoomed_in = True

    return

label mas_extra_menu_zoom_out_first_time:
    m 1ttu "Não consegue ficar [sntd] direito por muito tempo?"
    m "Ou será que só quer ver o topo da minha cabeça?"
    m 1hua "Ehehe~"
    return

label mas_extra_menu_zoom_in_first_time:
    m 1ttu "Chegando um pouquinho mais perto, hein?"
    m 1hua "Tudo bem~"
    return

label mas_extra_menu_zoom_in_max_first_time:
    m 6wuo "[player]!"
    m 6rkbfd "Quando seu rosto fica tão perto assim..."
    m 6ekbfd "Eu me sinto..."
    show monika 6hkbfa
    pause 2.0
    m 6hubfa "Quentinha..."
    return





label mas_extra_menu_boop_intro:
    m 1eua "boop intro"
    return

default persistent._mas_pm_boop_stats = {}










style mas_mbs_vbox is vbox:
    spacing 0

style mas_mbs_button is generic_button_light


style mas_mbs_button_dark is generic_button_dark


style mas_mbs_button_text is generic_button_text_light

style mas_mbs_button_text_dark is generic_button_text_dark































































style mas_extra_menu_frame:
    background Frame("mod_assets/frames/trans_pink2pxborder100.png", Borders(2, 2, 2, 2, pad_top=2, pad_bottom=4))

style mas_extra_menu_frame_dark:
    background Frame("mod_assets/frames/trans_pink2pxborder100_d.png", Borders(2, 2, 2, 2, pad_top=2, pad_bottom=4))

style mas_extra_menu_label_text is hkb_button_text:
    color "#FFFFFF"

style mas_extra_menu_label_text_dark is hkb_button_text_dark:
    color "#FD5BA2"

style mas_adjust_vbar:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"
    bar_vertical True

style mas_adjustable_button is generic_button_light:
    xysize (None, None)
    padding (3, 3, 3, 3)

style mas_adjustable_button_dark is generic_button_dark:
    xysize (None, None)
    padding (3, 3, 3, 3)

style mas_adjustable_button_text is generic_button_text_light:
    kerning 0.2

style mas_adjustable_button_text_dark is generic_button_text_dark:
    kerning 0.2

screen mas_extramenu_area():
    zorder 52

    key "e" action Jump("mas_extra_menu_close")
    key "E" action Jump("mas_extra_menu_close")

    frame:
        area (0, 0, 1280, 720)
        background Solid("#0000007F")


        textbutton _("Fechar"):
            area (60, 596, 120, 35)
            style "hkb_button"
            action Jump("mas_extra_menu_close")


        frame:
            area (195, 450, 80, 255)
            style "mas_extra_menu_frame"
            has vbox
            spacing 2
            label "Zoom":
                text_style "mas_extra_menu_label_text"
                xalign 0.5


            textbutton _("Redefinir"):
                style "mas_adjustable_button"
                selected False
                xsize 72
                ysize 35
                xalign 0.3
                action SetField(store.mas_sprites, "zoom_level", store.mas_sprites.default_zoom_level)


            bar value FieldValue(store.mas_sprites, "zoom_level", store.mas_sprites.max_zoom):
                style "mas_adjust_vbar"
                xalign 0.5
            $ store.mas_sprites.adjust_zoom()
