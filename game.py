import arcade
import arcade.gui
from bs4 import BeautifulSoup
import requests
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_TITLE = "GENERAL KNOWLEDGE"
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 20
NO_OF_LIVES = 5
url_list = [ "https://www.gktoday.in/quizbase/world-geography",
             "https://www.gktoday.in/quizbase/world-geography?pageno=2",
             "https://www.gktoday.in/quizbase/world-geography?pageno=3",
             "https://www.gktoday.in/quizbase/indian-geography-mcqs",
             "https://www.gktoday.in/quizbase/indian-geography-mcqs?pageno=2",
             "https://www.gktoday.in/quizbase/indian-geography-mcqs?pageno=3",
             "https://www.gktoday.in/quizbase/environment-biodiversity-current-affairs",
             "https://www.gktoday.in/quizbase/environment-biodiversity-current-affairs?pageno=2",
             "https://www.gktoday.in/quizbase/environment-biodiversity-current-affairs?pageno=3",
             "https://www.gktoday.in/quizbase/general-science-for-competitive-examinations",
             "https://www.gktoday.in/quizbase/general-science-for-competitive-examinations?pageno=2",
             "https://www.gktoday.in/quizbase/general-science-for-competitive-examinations?pageno=3",
             "https://www.gktoday.in/quizbase/science-technology-current-affairs",
             "https://www.gktoday.in/quizbase/science-technology-current-affairs?pageno=2",
             "https://www.gktoday.in/quizbase/science-technology-current-affairs?pageno=3",
             "https://www.gktoday.in/quizbase/art-culture-current-affairs",
             "https://www.gktoday.in/quizbase/summits-and-conferences-in-current-affairs" ]


class InstructionView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("...QUIZ...", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameOverView(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        self.total_score = 0
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(" GAME OVER ", self.window.width/2, self.window.height/2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("SCORE : {}".format(self.total_score), self.window.width/2, self.window.height/2 - 75,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        ins_view = InstructionView()
        self.window.show_view(ins_view)


class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BABY_POWDER)

        self.ques_list = []
        self.options_list = []
        self.ans_list = []
        self.q_no_list = []
        self.lives = 0
        self.score = 0
        self.q_no = 0
        self.answer = ""

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout(x=75, y=300, aling='center')

        A_button = arcade.gui.UIFlatButton(text="A", width=50)
        B_button = arcade.gui.UIFlatButton(text="B", width=50)
        C_button = arcade.gui.UIFlatButton(text="C", width=50)
        D_button = arcade.gui.UIFlatButton(text="D", width=50)

        A_button.on_click = self.on_click_A
        B_button.on_click = self.on_click_B
        C_button.on_click = self.on_click_C
        D_button.on_click = self.on_click_D

        self.v_box.add(A_button.with_space_around(bottom=10, left=60))
        self.v_box.add(B_button.with_space_around(bottom=10, left=60))
        self.v_box.add(C_button.with_space_around(bottom=10, left=60))
        self.v_box.add(D_button.with_space_around(bottom=150, left=60))
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="left",
                                                   anchor_y="bottom",
                                                   child=self.v_box)
                                                   )

    def setup(self):

        for url in url_list:
            result = requests.get(url)
            doc = BeautifulSoup(result.text , "html.parser")
            doc.prettify()

            ques = doc.find_all("div" , {"class" : "wp_quiz_question testclass"})
            for q in ques:
                Q = q.find("span")
                Q.decompose()
            self.ques_list.extend(ques)

            options = doc.find_all("div" , {"class" : "wp_quiz_question_options"})

            for ops in options:
                opt = ops.find("p")
                brs = opt.find_all("br")
                for br in brs:
                    br.decompose()
                self.options_list.append(opt.contents)

            ans = doc.find_all("div" , {"class" : "ques_answer"})
            self.ans_list.extend(ans)

            ans.clear()
            ques.clear()
            options.clear()

        self.lives = NO_OF_LIVES
        self.score = 0
        for _ in range(1,165):
            self.q_no_list.append(_)
        self.q_no = random.choice(self.q_no_list)

    def reset_game(self):
        self.ques_list.clear()
        self.options_list.clear()
        self.ans_list.clear()
        self.q_no_list.clear()

    def skip_this(self):
        self.q_no_list.remove(self.q_no)
        self.q_no = random.choice(self.q_no_list)
        if self.ques_list[self.q_no].string == None:
            self.skip_this()

    def my_update(self):
        if self.answer == (self.ans_list[self.q_no].contents)[1].strip()[0] :
            self.score += 1
        else :
            self.lives = self.lives - 1

        self.q_no_list.remove(self.q_no)
        self.q_no = random.choice(self.q_no_list)

        if self.ques_list[self.q_no].string == None:
            self.skip_this()

        if self.lives == 0:
            self.reset_game()
            view = GameOverView()
            view.total_score = self.score
            self.window.show_view(view)

    def on_click_A(self, event):
        self.answer = 'A'
        self.my_update()

    def on_click_B(self, event):
        self.answer = 'B'
        self.my_update()

    def on_click_C(self, event):
        self.answer = 'C'
        self.my_update()

    def on_click_D(self, event):
        self.answer = 'D'
        self.my_update()

    def get_my_score(self):
        return self.score

    def on_draw(self):

        arcade.start_render()
        shift = 0
        ops_start_x = 120
        ques_start_x = 10
        ques_start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5

        arcade.draw_text( str(self.ques_list[self.q_no].string),
                            ques_start_x,
                            ques_start_y-75,
                            arcade.color.CHARLESTON_GREEN,
                            DEFAULT_FONT_SIZE ,
                            width=SCREEN_WIDTH,
                            align="center")

        for op in self.options_list[self.q_no]:
            arcade.draw_text(str(op).strip(),
                                ops_start_x,
                                ques_start_y-shift-190,
                                arcade.color.BLUE,
                                DEFAULT_FONT_SIZE ,
                                width=SCREEN_WIDTH,
                                align="left")
            shift += 60

            self.manager.draw()

            arcade.draw_text( "LIVES : {}".format(self.lives),
                                  ques_start_x,
                                  ques_start_y+25,
                                  arcade.color.ALABAMA_CRIMSON,
                                  DEFAULT_FONT_SIZE,
                                  width=SCREEN_WIDTH,
                                  align="left")

            arcade.draw_text( "SCORE : {}".format(self.score),
                                  ques_start_x-30,
                                  ques_start_y+25,
                                  arcade.color.AO,
                                  DEFAULT_FONT_SIZE,
                                  width=SCREEN_WIDTH,
                                  align="right")

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
