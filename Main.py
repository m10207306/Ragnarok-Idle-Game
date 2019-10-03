import World


class Ragnarok:
    def __init__(self):
        print("""\
================================================
============== Ragnarok Idle Game ==============
================================================

          Enter [S] to start new game
                [L] to load data                
                [E] to exit                     """)

        while True:
            answer = input(">> ")
            if answer.lower() == "s":
                world_obj = World.WorldClass()
            elif answer.lower() == "l":
                print(">> load game")
            elif answer.lower() == "e":
                print(">> See ya!")
                break
            else:
                print(">> Undefined Answer.")


RO = Ragnarok()