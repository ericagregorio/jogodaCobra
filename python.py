import tkinter as tk
import random

# Configurações do jogo
LARGURA = 400
ALTURA = 400
TAMANHO_SEGMENTO = 20
VELOCIDADE = 100  # Milissegundos

# Classe para o jogo da cobrinha
class JogoCobrinha:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Cobrinha")
        self.canvas = tk.Canvas(root, width=LARGURA, height=ALTURA, bg="black")
        self.canvas.pack()

        # Inicia o jogo
        self.reset_jogo()
        
        # Controles
        self.root.bind("<Left>", lambda _: self.mudar_direcao("esquerda"))
        self.root.bind("<Right>", lambda _: self.mudar_direcao("direita"))
        self.root.bind("<Up>", lambda _: self.mudar_direcao("cima"))
        self.root.bind("<Down>", lambda _: self.mudar_direcao("baixo"))
        
        # Atualiza o jogo
        self.atualizar_jogo()

    def reset_jogo(self):
        self.direcao = "direita"
        self.cobra = [(100, 100), (80, 100), (60, 100)]
        self.comida = self.criar_comida()
        self.jogo_ativo = True

    def criar_comida(self):
        x = random.randint(0, (LARGURA - TAMANHO_SEGMENTO) // TAMANHO_SEGMENTO) * TAMANHO_SEGMENTO
        y = random.randint(0, (ALTURA - TAMANHO_SEGMENTO) // TAMANHO_SEGMENTO) * TAMANHO_SEGMENTO
        return x, y

    def mudar_direcao(self, nova_direcao):
        direcao_oposta = {"esquerda": "direita", "direita": "esquerda", "cima": "baixo", "baixo": "cima"}
        if nova_direcao != direcao_oposta.get(self.direcao):
            self.direcao = nova_direcao

    def atualizar_jogo(self):
        if self.jogo_ativo:
            nova_cabeca = self.mover_cobra()
            if self.verificar_colisoes(nova_cabeca):
                self.jogo_ativo = False
                self.canvas.create_text(LARGURA/2, ALTURA/2, text="Game Over", fill="red", font=("Arial", 24))
            else:
                self.cobra.insert(0, nova_cabeca)
                if nova_cabeca == self.comida:
                    self.comida = self.criar_comida()
                else:
                    self.cobra.pop()
                self.desenhar_elementos()
                self.root.after(VELOCIDADE, self.atualizar_jogo)

    def mover_cobra(self):
        x, y = self.cobra[0]
        if self.direcao == "direita":
            x += TAMANHO_SEGMENTO
        elif self.direcao == "esquerda":
            x -= TAMANHO_SEGMENTO
        elif self.direcao == "cima":
            y -= TAMANHO_SEGMENTO
        elif self.direcao == "baixo":
            y += TAMANHO_SEGMENTO
        return x, y

    def verificar_colisoes(self, pos):
        x, y = pos
        if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA or pos in self.cobra:
            return True
        return False

    def desenhar_elementos(self):
        self.canvas.delete("all")
        for segmento in self.cobra:
            x, y = segmento
            self.canvas.create_rectangle(x, y, x + TAMANHO_SEGMENTO, y + TAMANHO_SEGMENTO, fill="green")
        x, y = self.comida
        self.canvas.create_oval(x, y, x + TAMANHO_SEGMENTO, y + TAMANHO_SEGMENTO, fill="red")

# Cria a janela e executa o jogo
root = tk.Tk()
jogo = JogoCobrinha(root)
root.mainloop()