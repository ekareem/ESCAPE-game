from IO_Engine import IO_Engine
from IO_Engine import IO_SCREEN_COLOR,IO_SCREEN_TITLE,IO_SCREEN_SIZE
from IO_Timer import IO_Timer,IO_TARGET_FPS,IO_TARGET_DT

def main():
    IO_Engine.getInstance().init(IO_SCREEN_SIZE,IO_SCREEN_COLOR,IO_SCREEN_TITLE)
    IO_Timer.getInstance().init(IO_TARGET_FPS,IO_TARGET_DT)

    while(IO_Engine.getInstance().screen.running):
        dt = IO_Timer.getInstance().deltaTIme
        IO_Engine.getInstance().event(dt)
        IO_Engine.getInstance().update(dt)
        IO_Engine.getInstance().render(dt)
        IO_Timer.getInstance().tick()
        
    IO_Engine.getInstance().clean()

if __name__ == '__main__':
    main()