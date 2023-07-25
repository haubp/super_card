import arcade

arcade.open_window(600, 600, "Drawing window")
arcade.set_background_color(arcade.csscolor.SKY_BLUE)
arcade.start_render()
arcade.draw_lrtb_rectangle_filled(0, 599, 300, 0, arcade.csscolor.GREEN)
arcade.finish_render()
arcade.run()