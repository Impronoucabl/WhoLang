from lottie import objects
from lottie.exporters.core import export_lottie
from gall_wrd import G_word

def main(text):
    A = G_word(text, 500, (0,0))
    A.spawn_syllables()
    A.spawn_letters()
    A.spawn_nodes()
    B = lottie_gen(A)
    export_lottie(B, "test.json")

def lottie_gen(word):
    pass


if __name__ == "__main__":
    main(input())
