import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
import pygame
import sqlite3
import os
import shutil


# ==========================================
# CLASSE DA URNA (TELA DA VOTAÇÃO)
# ==========================================
class UrnaEletronicaApp:
    def __init__(self, master, admin_root, eleicao_id, eleicao_nome, logo_path, sound_file):
        self.root = master
        self.admin_root = admin_root
        self.root.title("Urna Eletrônica")
        self.root.attributes("-fullscreen", True)
        self.root.protocol("WM_DELETE_WINDOW", self.pedir_senha_fechar)
        self.root.bind("<Escape>", lambda e: self.pedir_senha_fechar())

        self.eleicao_id = eleicao_id
        self.titulo_eleicao = eleicao_nome
        self.subtitulo_eleicao = "Escolha um dos candidatos abaixo para ser o representante de turma"
        self.logo_path = logo_path
        self.sound_file = sound_file
        self.ID_BRANCO_NULO = 99

        self.conectar_banco()
        self.candidatos = self.buscar_candidatos()
        self.configurar_tela_votacao()

    def pedir_senha_fechar(self):
        senha = simpledialog.askstring("Segurança", "Digite a senha para encerrar a votação:", show='*',
                                       parent=self.root)
        if senha == "admin123":
            self.admin_root.deiconify()
            self.root.destroy()
        elif senha is not None:
            messagebox.showerror("Erro", "Senha incorreta!", parent=self.root)

    def conectar_banco(self):
        self.conn = sqlite3.connect("urna_escolar.db")
        self.cursor = self.conn.cursor()

    def buscar_candidatos(self):
        self.cursor.execute("SELECT id, nome, foto FROM candidatos WHERE eleicao_id = ?", (self.eleicao_id,))
        return [{"id": c[0], "nome": c[1], "foto": c[2]} for c in self.cursor.fetchall()]

    def configurar_tela_votacao(self):
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20)

        try:
            pil_image = Image.open(self.logo_path)
            base_width = 200
            w_percent = (base_width / float(pil_image.size[0]))
            h_size = int((float(pil_image.size[1]) * float(w_percent)))
            self.logo_photo = ImageTk.PhotoImage(pil_image.resize((base_width, h_size), Image.Resampling.LANCZOS))
            tk.Label(self.frame_principal, image=self.logo_photo).pack(side=tk.TOP, pady=(20, 10))
        except:
            pass

        tk.Label(self.frame_principal, text=self.titulo_eleicao, font=("Arial", 22, "bold"), fg="red").pack(
            pady=(10, 5))
        tk.Label(self.frame_principal, text=self.subtitulo_eleicao, font=("Times New Roman", 18, "bold")).pack(
            pady=(5, 20))

        frame_lista = tk.Frame(self.frame_principal)
        frame_lista.pack(fill=tk.BOTH, expand=True)
        meu_canvas = tk.Canvas(frame_lista)
        meu_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=meu_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        meu_canvas.configure(yscrollcommand=scrollbar.set)

        frame_candidatos = tk.Frame(meu_canvas)
        janela_id = meu_canvas.create_window((0, 0), window=frame_candidatos, anchor="n")
        meu_canvas.bind('<Configure>', lambda e: (meu_canvas.coords(janela_id, e.width / 2, 0),
                                                  meu_canvas.configure(scrollregion=meu_canvas.bbox("all"))))

        max_colunas = 1
        for i, c in enumerate(self.candidatos):
            self.criar_botao(frame_candidatos, c, i, 0)
        self.criar_botao_branco(frame_candidatos, len(self.candidatos), 0)
        meu_canvas.bind_all("<MouseWheel>", lambda e: meu_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def criar_botao(self, pai, c, l, col):
        f = tk.Frame(pai);
        f.grid(row=l, column=col, padx=20, pady=15, sticky="we")
        try:
            img = ImageTk.PhotoImage(Image.open(c["foto"]).resize((150, 150), Image.Resampling.LANCZOS))
            btn = tk.Button(f, image=img, text=f"   {c['nome']}", font=("Arial", 18, "bold"), compound=tk.LEFT,
                            command=lambda: self.confirmar_voto(c), borderwidth=4, relief="raised", cursor="hand2",
                            padx=30, pady=15)
            btn.image = img;
            btn.pack(fill=tk.BOTH, expand=True)
        except:
            tk.Button(f, text=f"Sem Foto\n\n{c['nome']}", font=("Arial", 18, "bold"), width=35, height=7,
                      command=lambda: self.confirmar_voto(c), borderwidth=4, relief="raised").pack(fill=tk.BOTH,
                                                                                                   expand=True)

    def criar_botao_branco(self, pai, l, col):
        f = tk.Frame(pai);
        f.grid(row=l, column=col, padx=20, pady=15, sticky="we")
        tk.Button(f, text="BRANCO / NULO", font=("Arial", 18, "bold"), width=35, height=6,
                  command=lambda: self.confirmar_voto({"id": 99, "nome": "BRANCO / NULO"}), borderwidth=4,
                  relief="raised", bg="white").pack(fill=tk.BOTH, expand=True)

    def confirmar_voto(self, c):
        if messagebox.askyesno("Confirmar", f"Confirma seu voto em {c['nome']}?", parent=self.root):
            if os.path.exists(self.sound_file) and pygame.mixer.get_init() is not None:
                try:
                    pygame.mixer.music.load(self.sound_file); pygame.mixer.music.play()
                except:
                    pass
            self.cursor.execute("INSERT INTO votos (candidato_id, eleicao_id) VALUES (?, ?)",
                                (c['id'], self.eleicao_id));
            self.conn.commit()
            self.mostrar_fim()

    def mostrar_fim(self):
        self.frame_principal.pack_forget()
        f = tk.Frame(self.root);
        f.pack(fill=tk.BOTH, expand=True)
        tk.Label(f, text="FIM", font=("Arial", 80, "bold"), fg="green").pack(expand=True, pady=(100, 0))
        tk.Label(f, text="Obrigado pelo seu voto!", font=("Arial", 30), fg="blue").pack(pady=10, expand=True)
        self.tempo = 5
        btn = tk.Button(f, text="", font=("Arial", 18, "bold"), state=tk.DISABLED,
                        command=lambda: (f.destroy(), self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20)),
                        width=25, height=2)
        btn.pack(pady=60)

        def timer():
            if self.tempo > 0:
                btn.config(text=f"Aguarde... {self.tempo}s"); self.tempo -= 1; self.root.after(1000, timer)
            else:
                btn.config(text="Nova Votação", state=tk.NORMAL, bg="#28a745", fg="white", cursor="hand2")

        timer()


# ==========================================
# CLASSE ADMINISTRATIVA
# ==========================================
class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Painel de Administração - Urna Escolar")
        self.root.geometry("800x650")
        try:
            pygame.mixer.init()
        except:
            pass
        self.sound_file = "confirma-urna.mp3"
        self.logo_path = "logo-sagrado-1024x597.png"
        self.conn = sqlite3.connect("urna_escolar.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS eleicoes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS candidatos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, foto TEXT NOT NULL, eleicao_id INTEGER)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS votos (id INTEGER PRIMARY KEY AUTOINCREMENT, candidato_id INTEGER, eleicao_id INTEGER)")
        self.container = tk.Frame(self.root);
        self.container.pack(fill=tk.BOTH, expand=True)
        self.mostrar_eleicoes()

    def mostrar_eleicoes(self):
        for w in self.container.winfo_children(): w.destroy()
        tk.Label(self.container, text="Eleições Cadastradas", font=("Arial", 22, "bold")).pack(pady=20)

        self.cursor.execute("SELECT id, nome FROM eleicoes")
        eleicoes = self.cursor.fetchall()

        frame_lista = tk.Frame(self.container)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=40)

        if not eleicoes:
            tk.Label(frame_lista, text="Nenhuma eleição cadastrada ainda.", font=("Arial", 14)).pack(pady=10)
        else:
            for el in eleicoes:
                f = tk.Frame(frame_lista, bd=2, relief="solid", padx=15, pady=10);
                f.pack(fill=tk.X, pady=8)
                tk.Label(f, text=el[1], font=("Arial", 16, "bold")).pack(side=tk.LEFT)
                tk.Button(f, text="⚙️ Gerenciar", font=("Arial", 12, "bold"), bg="#007bff", fg="white", cursor="hand2",
                          padx=15, pady=5, command=lambda i=el[0], n=el[1]: self.gerenciar(i, n)).pack(side=tk.RIGHT)

        tk.Button(self.container, text="+ Criar Nova Votação", font=("Arial", 16, "bold"), bg="#28a745", fg="white",
                  cursor="hand2", padx=30, pady=15, command=self.nova_el).pack(pady=30)

    def nova_el(self):
        n = simpledialog.askstring("Nova Votação", "Nome da eleição:", parent=self.root)
        if n: self.cursor.execute("INSERT INTO eleicoes (nome) VALUES (?)",
                                  (n,)); self.conn.commit(); self.mostrar_eleicoes()

    def gerenciar(self, eid, enome):
        for w in self.container.winfo_children(): w.destroy()

        f_cab = tk.Frame(self.container);
        f_cab.pack(pady=20)
        tk.Label(f_cab, text=enome, font=("Arial", 20, "bold"), fg="blue").pack(side=tk.LEFT, padx=10)
        tk.Button(f_cab, text="✏️ Editar Nome", font=("Arial", 12, "bold"), cursor="hand2", padx=10, command=lambda: (
            self.cursor.execute("UPDATE eleicoes SET nome=? WHERE id=?",
                                (simpledialog.askstring("Editar Nome", "Novo nome:", initialvalue=enome,
                                                        parent=self.root), eid)), self.conn.commit(),
            self.gerenciar(eid, enome))).pack(side=tk.LEFT, padx=10)

        f_ac = tk.Frame(self.container);
        f_ac.pack(pady=15)
        tk.Button(f_ac, text="▶ Iniciar Urna", font=("Arial", 14, "bold"), bg="#28a745", fg="white", width=16, pady=8,
                  cursor="hand2", command=lambda: (self.root.withdraw(),
                                                   UrnaEletronicaApp(tk.Toplevel(self.root), self.root, eid, enome,
                                                                     self.logo_path, self.sound_file))).pack(
            side=tk.LEFT, padx=10)
        tk.Button(f_ac, text="📊 Ver Resultados", font=("Arial", 14, "bold"), bg="#ffc107", width=16, pady=8,
                  cursor="hand2", command=lambda: self.ver_res(eid, enome)).pack(side=tk.LEFT, padx=10)
        tk.Button(f_ac, text="🗑️ Excluir Votação", font=("Arial", 14, "bold"), bg="#dc3545", fg="white", width=16,
                  pady=8, cursor="hand2", command=lambda: self.del_el(eid)).pack(side=tk.LEFT, padx=10)

        tk.Label(self.container, text="Alunos Cadastrados:", font=("Arial", 16, "bold")).pack(pady=(20, 10))

        frame_cands = tk.Frame(self.container)
        frame_cands.pack(fill=tk.BOTH, expand=True, padx=60)
        self.cursor.execute("SELECT nome FROM candidatos WHERE eleicao_id=?", (eid,))
        candidatos_db = self.cursor.fetchall()
        if not candidatos_db:
            tk.Label(frame_cands, text="Nenhum aluno. Adicione abaixo.", font=("Arial", 12)).pack()
        else:
            for c in candidatos_db: tk.Label(frame_cands, text=f"• {c[0]}", font=("Arial", 14)).pack(anchor="w", pady=2)

        f_bot = tk.Frame(self.container);
        f_bot.pack(side=tk.BOTTOM, pady=30)
        tk.Button(f_bot, text="Adicionar Aluno", font=("Arial", 14, "bold"), bg="#17a2b8", fg="white", cursor="hand2",
                  padx=20, pady=10, command=lambda: self.add_cand(eid, enome)).pack(side=tk.LEFT, padx=15)
        tk.Button(f_bot, text="Voltar", font=("Arial", 14, "bold"), cursor="hand2", padx=20, pady=10,
                  command=self.mostrar_eleicoes).pack(side=tk.LEFT, padx=15)

    def add_cand(self, eid, enome):
        n = simpledialog.askstring("Novo Aluno", "Nome do Aluno:", parent=self.root)
        if n:
            messagebox.showinfo("Foto", "Na próxima tela, selecione a foto do aluno.", parent=self.root)
            f = filedialog.askopenfilename(title="Selecione a Foto", filetypes=[("Imagens", "*.jpg *.png *.jpeg")],
                                           parent=self.root)
            if f:
                pasta_destino = "fotos_salvas"
                if not os.path.exists(pasta_destino):
                    os.makedirs(pasta_destino)

                nome_arquivo = os.path.basename(f)

                caminho_relativo = os.path.join(pasta_destino, nome_arquivo)

                shutil.copy(f, caminho_relativo)

                # Salva no banco de dados o caminho RELATIVO, e não o completo!
                self.cursor.execute("INSERT INTO candidatos (nome, foto, eleicao_id) VALUES (?, ?, ?)",
                                    (n.upper(), caminho_relativo, eid))
                self.conn.commit()

                messagebox.showinfo("Sucesso", "Aluno adicionado!", parent=self.root)
                self.gerenciar(eid, enome)

    def del_el(self, eid):
        if simpledialog.askstring("Segurança", "Senha de Administrador:", show="*", parent=self.root) == "admin123":
            if messagebox.askyesno("Atenção", "Tem certeza que deseja apagar a votação e todos os dados?",
                                   parent=self.root):
                self.cursor.execute("DELETE FROM votos WHERE eleicao_id=?", (eid,))
                self.cursor.execute("DELETE FROM candidatos WHERE eleicao_id=?", (eid,))
                self.cursor.execute("DELETE FROM eleicoes WHERE id=?", (eid,))
                self.conn.commit();
                self.mostrar_eleicoes()

    def gerar_segundo_turno(self, nome_original, vencedores_ids, janela_res):
        novo_nome = f"{nome_original} - 2º Turno"
        self.cursor.execute("INSERT INTO eleicoes (nome) VALUES (?)", (novo_nome,))
        nova_eleicao_id = self.cursor.lastrowid
        for cid in vencedores_ids:
            self.cursor.execute("SELECT nome, foto FROM candidatos WHERE id = ?", (cid,))
            cand = self.cursor.fetchone()
            if cand: self.cursor.execute("INSERT INTO candidatos (nome, foto, eleicao_id) VALUES (?, ?, ?)",
                                         (cand[0], cand[1], nova_eleicao_id))
        self.conn.commit()
        messagebox.showinfo("Sucesso", f"Eleição '{novo_nome}' criada!\nAlunos empatados copiados para ela.",
                            parent=self.root)
        janela_res.destroy();
        self.mostrar_eleicoes()

    def ver_res(self, eid, enome):
        if simpledialog.askstring("Acesso Restrito", "Senha:", show="*", parent=self.root) != "admin123": return

        self.cursor.execute("""
                            SELECT c.id, c.nome, c.foto, COUNT(v.id) as tv
                            FROM candidatos c
                                     LEFT JOIN votos v ON v.candidato_id = c.id AND v.eleicao_id = ?
                            WHERE c.eleicao_id = ?
                            GROUP BY c.id
                            UNION ALL
                            SELECT 99, 'BRANCO/NULO', '', COUNT(id)
                            FROM votos
                            WHERE eleicao_id = ?
                              AND candidato_id = 99
                            ORDER BY tv DESC
                            """, (eid, eid, eid))
        res = self.cursor.fetchall()

        # Identificar vencedores
        votos_reais = [r[3] for r in res if r[0] != 99]
        max_votos = max(votos_reais) if votos_reais else 0
        vencedores_ids = [r[0] for r in res if r[3] == max_votos and r[0] != 99] if max_votos > 0 else []
        is_empate = len(vencedores_ids) > 1

        j = tk.Toplevel(self.root)
        j.title("Resultados")
        j.geometry("550x700")

        j.image_refs = []

        tk.Label(j, text="EMPATE DETECTADO" if is_empate else "Resultados Oficiais", font=("Arial", 20, "bold"),
                 fg="red" if is_empate else "black").pack(pady=15)
        tk.Label(j, text=enome, font=("Arial", 16, "bold"), fg="blue").pack(pady=(0, 10))

        # --- ÁREA DE ROLAGEM DOS RESULTADOS ---
        frame_canvas = tk.Frame(j)
        frame_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas_res = tk.Canvas(frame_canvas)
        canvas_res.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_res = tk.Scrollbar(frame_canvas, orient=tk.VERTICAL, command=canvas_res.yview)
        scrollbar_res.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_res.configure(yscrollcommand=scrollbar_res.set)

        frame_inner = tk.Frame(canvas_res)
        janela_id = canvas_res.create_window((0, 0), window=frame_inner, anchor="n")

        def on_configure(event):
            canvas_res.coords(janela_id, event.width / 2, 0)
            canvas_res.configure(scrollregion=canvas_res.bbox("all"))

        canvas_res.bind('<Configure>', on_configure)

        j.bind("<MouseWheel>", lambda e: canvas_res.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        for r in res:
            cand_id, nome, foto_path, votos = r[0], r[1], r[2], r[3]
            cor = "#d4edda" if cand_id in vencedores_ids else "#f8f9fa"
            trofeu = " 🏆" if cand_id in vencedores_ids else ""

            f = tk.Frame(frame_inner, bd=2, relief="groove", bg=cor, padx=15, pady=10)
            f.pack(fill=tk.X, padx=10, pady=5, ipadx=40)

            if foto_path and os.path.exists(foto_path):
                try:
                    img = ImageTk.PhotoImage(Image.open(foto_path).resize((60, 60), Image.Resampling.LANCZOS))
                    j.image_refs.append(img)  # Salvando referência da imagem
                    tk.Label(f, image=img, bg=cor).pack(side=tk.LEFT, padx=(0, 15))
                except:
                    pass

            # Texto
            tk.Label(f, text=f"{nome}{trofeu}\n{votos} voto(s)",
                     font=("Arial", 14, "bold" if cand_id in vencedores_ids else "normal"), bg=cor,
                     justify=tk.LEFT).pack(side=tk.LEFT, pady=5)

        # Botão de Segundo Turno
        if is_empate:
            tk.Button(j, text="🏆 Criar Eleição de 2º Turno", font=("Arial", 14, "bold"), bg="#17a2b8", fg="white",
                      cursor="hand2", pady=10, command=lambda: self.gerar_segundo_turno(enome, vencedores_ids, j)).pack(
                pady=20)


if __name__ == "__main__":
    root = tk.Tk();
    app = AdminApp(root);
    root.mainloop()