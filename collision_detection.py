import turtle
import math

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("pacman game")


pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

shapes = ["wizard.gif", "goblin.gif", "pacman.gif", "cherry.gif", "bar.gif", "ball.gif", "x.gif"]

for shape in shapes:
    wn.register_shape(shape)
    
class Sprite():
    
    ## 생성자: 스프라이트의 위치, 가로/세로 크기, 이미지 지정

    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    ## 스프라이트 메서드

    # 지정된 위치로 스프라이트 이동 후 도장 찍기
    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    # 충돌 감지 방법 1: 두 스프라이트의 중심이 일치할 때 충돌 발생
    def is_overlapping_collision(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    # 충돌 감지 방법 2: 두 스프라이트 사이의 거리가 두 객체의 너비의 평균값 보다 작을 때 충돌 발생
    def is_distance_collision(self, other):
        distance = (((self.x-other.x) ** 2) + ((self.y-other.y) ** 2)) ** 0.5
        if distance < (self.width + other.width)/2.0:
            return True
        else:
            return False

    # 충돌 감지 방법 3: 각각의 스프라이트를 둘러썬 경계상자가 겹칠 때 충돌 발생
    # aabb: Axis Aligned Bounding Box
    def is_aabb_collision(self, other):
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

class Character(Sprite):
    def __init__(self, x, y, width, height, image, jump=False):
        super().__init__(x, y, width, height, image)
        self.jump = jump
        self.y_velocity = 0
        self.floor = -300


    def hop(self, value):
        if self.jump:
            self.y_velocity = value

    def apply_gravity(self, gravity):
        self.y_velocity += gravity
        self.y += self.y_velocity

        if self.y - self.height/2 <= self.floor:
            self.y = self.floor + self.height/2
            self.y_velocity = 0
                        
	
wizard = Character(-250, 150, 128, 128, "wizard.gif")
goblin = Sprite(128, 200, 108, 128, "goblin.gif")

pacman = Character(0, -200, 20, 20, "pacman.gif", jump=True)
cherry = Sprite(128, -50, 128, 128, "cherry.gif")

bar = Sprite(-350, -200, 128, 24, "bar.gif")
bar1 = Sprite(-100, -200, 128, 24, "bar.gif")
bar2 = Sprite(150, -200, 128, 24, "bar.gif")
bar3 = Sprite(-350, -250, 128, 24, "bar.gif")
ball = Sprite(350, -200, 32, 32, "ball.gif")

# 스프라이트 모음 리스트
sprites = [wizard, goblin, pacman, cherry, bar, bar1, bar2, bar3, ball]




def move_left():
    pacman.x -= 10


def move_right():
    pacman.x += 10



# 팩맨 점프
def jump_pacman():
    pacman.hop(0.5)



# 이벤트 처리
wn.listen()
wn.onkeypress(move_left, "Left")  # 왼쪽 방향 화살표 입력
wn.onkeypress(move_right, "Right") # 오른쪽 방향 화살표 입력
wn.onkeypress(jump_pacman, "space") # 스페이크 키 입력


wizard_col = False
cherry_col = False
goblin_col = False
ball_col = False
bar1_col = False

score = 0
wn.tracer(0)
while True:
    
    # 각 스프라이트 위치 이동 및 도장 찍기
    for sprite in sprites:
        sprite.render(pen)

    pacman.apply_gravity(-0.005)


    if pacman.is_distance_collision(wizard):
        wizard.image = "x.gif"
        if wizard_col == False:
            score += 1
            wizard_col = True
    
        
    if pacman.is_distance_collision(cherry):
        cherry.image = "x.gif"
        pacman.hop(1.5)
        if cherry_col == False:
            score += 1
            cherry_col = True

    if pacman.is_aabb_collision(goblin):
        goblin.image = "x.gif"
        pacman.hop(0.7)
        if goblin_col == False:
            score += 1
            goblin_col = True

    if pacman.is_aabb_collision(ball):
        ball.image = "x.gif"
        pacman.hop(1.5)
        if ball_col == False:
            score += 1
            ball_col = True

    if pacman.is_aabb_collision(bar):
        pacman.hop(0.3)
    
    if pacman.is_aabb_collision(bar1):
        pacman.hop(0.3)

    if pacman.is_aabb_collision(bar2):
        pacman.hop(0.5)
    
    if pacman.is_aabb_collision(bar3):
        pacman.hop(1)

    pen.penup()
    pen.goto(-400, -300)
    pen.pendown()
    pen.setheading(0)
    pen.forward(800)
    pen.penup()

    if score == 4:
        pen.color("white")
        pen.penup()
        pen.goto(0, 0)
        pen.write("Clear!", align="center", font=("Arial", 48, "bold"))  
    else:
        pen.color("white")
        pen.penup()
        pen.goto(200, 280)
        pen.write(f"Score: {score}", align="center", font=("Arial", 24, "normal"))
        
    
    wn.update() # 화면 업데이트
    pen.clear() # 스프라이트 이동흔적 삭제
