# -*- coding: utf-8 -*-
#King (Vua)

#Queen (Hậu)

#Rook (Xe)

#Bishop (Tượng)

#Knight (Mã)

#Pawn (Tốt)
# Luật cờ
class Piece: 
    def __init__ (self, color):
        self.color = color 
class Pawn(Piece): 
    def __init__(self, color):
        super().__init__(color)
    def get_moves (self, board, r, c):
        moves = []
        if self.color == "white":
            dr, start = -1,6
            enemy = 'black'
        else: 
            dr, start = 1, 1
            enemy = "white"
         # Di chuyển 1 ô hoặc 2 ô nếu ở hàng xuất phát
        if 0 <= r+dr < 8 and board.board[r+dr][c] is None:
            moves.append((r+dr, c)) #danh sáchh các bước đi hợp lệ 
            if r == start and board.board[r+2*dr][c] is None:
                moves.append((r+2*dr, c))
        # Ăn chéo
        for dc in (-1, 1): #phía trái -1 or phải 1
            # tính vị trí mới khi di chuyển 1 bước chéo  
            nr, nc = r+dr, c+dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board.board[nr][nc]
                if target and target.color == enemy:
                    moves.append((nr, nc))
        return moves
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
    def get_moves(self, board, r, c):
        moves = []
        # Đi theo 4 hướng: lên, xuống, trái, phải
        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                if board.board[nr][nc] is None:
                    moves.append((nr, nc))
                else:
                    if board.board[nr][nc].color != self.color:
                        moves.append((nr, nc))
                    break
                nr += dr; nc += dc
        return moves
    
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
    def get_moves(self, board, r, c):
        moves = []
        # 8 nước có thể của mã
        offsets = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        for dr, dc in offsets:
            nr, nc = r+dr, c+dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board.board[nr][nc]
                if target is None or target.color != self.color:
                    moves.append((nr, nc))
        return moves
    
class Bishop (Piece):
    def __init__(self,color):
        super().__init__(color)
    def get_moves(self, board, r, c):
        moves = []
        dirs = [(1,1),(1,-1),(-1,1),(-1,-1)]
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                if board.board[nr][nc] is None:
                    moves.append((nr, nc))
                else:
                    if board.board[nr][nc].color != self.color:
                        moves.append((nr, nc))
                    break
                nr += dr; nc += dc
        return moves
class King(Piece):
    def __init__(self, color):
        super().__init__(color)
    def get_moves(self, board, r, c):
        moves = []
        # Vua đi 1 ô mọi hướng (không tính nhập thành)
        dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board.board[nr][nc]
                if target is None or target.color != self.color:
                    moves.append((nr, nc))
        return moves
class Queen (Piece):
    def __init__ (self,color):
        super(). __init__(color)
    def get_moves(self, board, r,c):
        moves = []
        dirs = [(1,1),(1,-1),(-1,1),(-1,-1),(-1,0),(1,0),(0,-1),(0,1)]
        for dr,dc in dirs:
            nr,nc = r+dr, c+dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                if board.board[nr][nc] is None:
                    moves.append((nr, nc))
                else:
                    if board.board[nr][nc].color != self.color:
                        moves.append((nr, nc))
                    break
                nr += dr; nc += dc
        return moves   
# Board
class Board: 
    def __init__ (self):
        self.board = [[None for _ in range(8)] for _ in  range(8)]
        self.board[0] = [Rook('black'), Knight('black'), Bishop('black'), 
                         Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')]
        for c in range(8):
            self.board[1][c] = Pawn('black')
        # Đặt quân trắng ở hàng 6-7
        self.board[7] = [Rook('white'), Knight('white'), Bishop('white'), 
                         Queen('white'), King('white'), Bishop('white'), Knight('white'), Rook('white')]
        for c in range(8):
            self.board[6][c] = Pawn('white')

    def get_king_position(self, color):
        # Tìm vị trí vua của màu chỉ định
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if isinstance(p, King) and p.color == color:
                    return (r, c)
        return None
    def is_in_check(self, color):
        # Kiểm tra xem màu chỉ định có bị chiếu (có bị đe dọa bởi quân địch) không
        pos = self.get_king_position(color)
        if pos is None:
            return True
        enemy = 'black' if color=='white' else 'white'
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color == enemy:
                    if pos in p.get_moves(self, r, c):
                        return True
        return False
    def move_piece(self, move):
        # Thực hiện di chuyển (và phong cấp nếu pawn tới cuối bàn)
        (r1,c1), (r2,c2) = move # xuất phát và đích
        p = self.board[r1][c1]
        # Phong cấp pawn
        if isinstance(p, Pawn) and (r2 == 0 or r2 == 7):
            self.board[r2][c2] = Queen(p.color)
            self.board[r1][c1] = None
        else:
            self.board[r2][c2] = p
            self.board[r1][c1] = None
    def get_all_moves(self, color):
        # Sinh tất cả nước đi (hợp lệ) của một màu
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color == color:
                    for dest in p.get_moves(self, r, c):
                        moves.append(((r,c), dest))
        # Lọc bớt các nước đi khiến chính mình bị chiếu
        legal = []
        import copy
        for move in moves:
            newb = copy.deepcopy(self)#tao bản sao bàn cờ hiện tại 
            newb.move_piece(move) 
            if not newb.is_in_check(color):
                legal.append(move)
        return legal
    def evaluate(self):
        # Hàm đánh giá: tổng điểm trắng trừ điểm đen
        score = 0
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p:
                    v = 0
                    if isinstance(p, Pawn):   v = 1
                    elif isinstance(p, Knight): v = 3
                    elif isinstance(p, Bishop): v = 3
                    elif isinstance(p, Rook):   v = 5
                    elif isinstance(p, Queen):  v = 9
                    # King bỏ qua vì chiếu tướng mới kết thúc
                    if p.color == 'white':
                        score += v
                    else:
                        score -= v
        return score
    # Hàm heuristic 2
    # def evaluate(self):
    #     score = 0
    
    #    # Giá trị vật chất của các quân cờ
    #     piece_value = {
    #         Pawn: 1,
    #         Knight: 3,
    #         Bishop: 3,
    #         Rook: 5,
    #         Queen: 9,
    #         King: 0  # Bỏ qua Vua vì chiếu hết quyết định kết thúc
    #     }
    
    #     # Tọa độ: C4=(4,2), D4=(4,3), E4=(4,4), F4=(4,5), C5=(3,2), D5=(3,3), E5=(3,4), F5=(3,5)
    #     center_squares = [(4,2), (4,3), (4,4), (4,5), (3,2), (3,3), (3,4), (3,5)]
    
    #     for r in range(8):
    #         for c in range(8):
    #             p = self.board[r][c]
    #             if p:
    #                 # Giá trị vật chất
    #                 value = piece_value[type(p)]
                  
    #                 # Ưu tiên kiểm soát trung tâm
    #                 center_bonus = 0
    #                 if (r, c) in center_squares:
    #                     center_bonus = 0.3  # Thưởng 0.3 điểm cho quân ở trung tâm
                
    #                 # Ưu tiên tấn công: Đếm số quân địch bị đe dọa bởi quân này
    #                 attack_bonus = 0
    #                 enemy_color = 'black' if p.color == 'white' else 'white'
    #                 for dest in p.get_moves(self, r, c):
    #                     target = self.board[dest[0]][dest[1]]
    #                     if target and target.color == enemy_color:
    #                         attack_bonus += 0.2  # Thưởng 0.2 điểm cho mỗi quân địch bị đe dọa
    #                 # Cộng/trừ điểm theo màu
    #                 if p.color == 'white':
    #                     score += value + center_bonus + attack_bonus
    #                 else:
    #                     score -= value + center_bonus + attack_bonus
    
    #     # Ưu tiên chiếu vua
    #     if self.is_in_check('white'):
    #         score -= 0.5  # Trừ điểm nếu trắng bị chiếu
    #     if self.is_in_check('black'):
    #         score += 0.5  # Cộng điểm nếu đen bị chiếu
    
    #     return score
    #
    # Hàm heuristic 3
    # def evaluate(self):
    #     # Đoạn này gần giống với heuristic của Vi
    #     score = 0
    #     piece_value = {
    #         Pawn: 1,
    #         Knight: 3,
    #         Bishop: 3,
    #         Rook: 5,
    #         Queen: 9,
    #         King: 0
    #     }
    #     center_squares = [(4,2), (4,3), (4,4), (4,5), (3,2), (3,3), (3,4), (3,5)]
    #     near_center_squares = [(5,2), (5,3), (5,4), (5,5), (2,2), (2,3), (2,4), (2,5)]
    #     # Đếm số quân bị đe dọa và tính linh hoạt
    #     white_threats = 0
    #     black_threats = 0
    #     white_mobility = 0
    #     black_mobility = 0
    #     for r in range(8):
    #         for c in range(8):
    #             p = self.board[r][c]
    #             if p:
    #                 # Giá trị vật chất
    #                 value = piece_value[type(p)]
    #                 # Kiểm soát trung tâm và gần trung tâm
    #                 center_bonus = 0
    #                 if (r, c) in center_squares:
    #                     center_bonus = 0.4 # Thưởng nhiều hơn cho trung tâm
    #                 elif (r, c) in near_center_squares:
    #                     center_bonus = 0.2 # Thưởng ít hơn cho vùng gần trung tâm
    #                 # Tính linh hoạt (mobility) và đe dọa
    #                 attack_bonus = 0
    #                 moves = p.get_moves(self, r, c)
    #                 move_count = len(moves)
    #                 enemy_color = 'black' if p.color == 'white' else 'white'
    #                 for dest in moves:
    #                     target = self.board[dest[0]][dest[1]]
    #                     if target and target.color == enemy_color:
    #                         attack_bonus += 0.25 # Thưởng cho mỗi quân địch bị đe dọa
    #                 # Cộng điểm linh hoạt
    #                 mobility_bonus = move_count * 0.1 # Thưởng 0.1 điểm cho mỗi nước đi hợp lệ
    #                 # Cộng điểm cho bên tương ứng
    #                 if p.color == 'white':
    #                     score += value + center_bonus + attack_bonus + mobility_bonus
    #                     white_threats += attack_bonus
    #                     white_mobility += move_count
    #                 else:
    #                     score -= value + center_bonus + attack_bonus + mobility_bonus
    #                     black_threats += attack_bonus
    #                     black_mobility += move_count
    #     # An toàn Vua
    #     white_king_pos = self.get_king_position('white')
    #     black_king_pos = self.get_king_position('black')
    #     # Phạt nếu Vua ở vị trí nguy hiểm (gần trung tâm hoặc bị đe dọa nhiều)
    #     if white_king_pos:
    #         r, c = white_king_pos
    #         # Phạt nếu Vua ở trung tâm (ít an toàn)
    #         king_safety = 0
    #         if (r, c) in center_squares:
    #             king_safety -= 0.5
    #         # Phạt nếu Vua bị nhiều quân đe dọa
    #         attackers = 0
    #         for r2 in range(8):
    #             for c2 in range(8):
    #                 p = self.board[r2][c2]
    #                 if p and p.color == 'black':
    #                     if white_king_pos in p.get_moves(self, r2, c2):
    #                         attackers += 1
    #         king_safety -= attackers * 0.3
    #         score += king_safety
    #     if black_king_pos:
    #         r, c = black_king_pos
    #         king_safety = 0
    #         if (r, c) in center_squares:
    #             king_safety -= 0.5
    #         attackers = 0
    #         for r2 in range(8):
    #             for c2 in range(8):
    #                 p = self.board[r2][c2]
    #                 if p and p.color == 'white':
    #                     if black_king_pos in p.get_moves(self, r2, c2):
    #                         attackers += 1
    #         king_safety -= attackers * 0.3
    #         score -= king_safety
    #     # Ưu tiên chiếu vua
    #     if self.is_in_check('white'):
    #         score -= 0.6
    #     if self.is_in_check('black'):
    #         score += 0.6
    #     return score
                        


import math
def minimax(board, depth, alpha, beta, maximizing):
    # Nếu đã đạt độ sâu tối đa hoặc game kết thúc
    if depth == 0:
        return board.evaluate(), None
    if maximizing: #true la trang flase là đen
        moves = board.get_all_moves('white')
        if not moves:
            # Nếu trắng không còn nước đi
            if board.is_in_check('white'):
                return -math.inf, None  # trắng bị chiếu hết
            else:
                return 0, None  # hòa
        maxv, best_move = -math.inf, None # gia tri max white dat dc
        for m in moves:
            newb = copy.deepcopy(board)
            newb.move_piece(m)
            val,_ = minimax(newb, depth-1, alpha, beta, False)#val giá trị đánh giá điểm
            if val > maxv:
                maxv, best_move = val, m
            alpha = max(alpha, maxv)
            if beta <= alpha: break
        return maxv, best_move
    else:
        moves = board.get_all_moves('black')
        if not moves:
            if board.is_in_check('black'):
                return math.inf, None
            else:
                return 0, None
        minv, best_move = math.inf, None
        for m in moves:
            newb = copy.deepcopy(board)
            newb.move_piece(m)
            val,_ = minimax(newb, depth-1, alpha, beta, True)
            if val < minv:
                minv, best_move = val, m
            beta = min(beta, minv)
            if beta <= alpha: break
        return minv, best_move


import pygame, math, sys, copy
pygame.init()
# Khởi tạo âm thanh
pygame.mixer.init()  # Khởi tạo mixer của pygame để phát âm thanh

# Tải âm thanh di chuyển quân cờ
move_sound = pygame.mixer.Sound("images/music.mp3")  # Tải file âm thanh
WIDTH =800
HEIGHT = 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess with AI")
font = pygame.font.SysFont(None, 40)
WHITE = (232,232,232); BLACK = (125,135,150)
# Biến đồng hồ
font = pygame.font.SysFont(None, 40)

# Thời gian giới hạn (5 phút)
time_limit = 5 * 60 * 1000  # Giới hạn thời gian 5 phút (5 * 60 giây * 1000 milliseconds)
start_time = pygame.time.get_ticks()  # Thời gian bắt đầu
# Người chơi chọn phe
player_color = input("Chọn phe (white/black): ")
player_color = 'white' if player_color.lower()!='black' else 'black'
turn = 'white'
selected = None; valid_moves = []
square = (WIDTH - 160) // 8
def draw_board():
    # Vẽ bàn cờ và quân cờ
    
    for r in range(8):
        for c in range(8):
            rect = pygame.Rect(c*square, r*square, square, square)
            bg = WHITE if (r+c)%2==0 else BLACK
            pygame.draw.rect(screen, bg, rect)

            # Nếu có bước đi hợp lệ, vẽ ô hợp lệ lên bàn cờ
            if (r, c) in valid_moves:
                # Vẽ nền màu vàng nhạt cho ô hợp lệ (hoặc màu khác nếu muốn)
                pygame.draw.rect(screen, (255, 255, 0), rect, 5)  # Vẽ viền vàng cho ô hợp lệ

            p = board.board[r][c]
            if p:
                # Xác định ký hiệu quân
                if isinstance(p, Pawn):
                    # Xác định tệp hình ảnh của quân Pawn
                    image_file = f"images/{'white' if p.color == 'white' else 'black'}_pawn.png"
                elif isinstance(p, Knight): 
                    image_file = f"images/{'white' if p.color == 'white' else 'black'}_knight.png"
                elif isinstance(p, Bishop): 
                    image_file = f"images/{'white' if p.color == 'white' else 'black'}_bishop.png"
                elif isinstance(p, Rook):   
                    image_file = f"images/{'white' if p.color == 'white' else 'black'}_rook.png"
                elif isinstance(p, Queen):  
                    image_file = f"images/{'white' if p.color == 'white' else 'black'}_queen.png"
                elif isinstance(p, King):   
                    image_file = f"images/{'white' if p.color == 'white' else 'black'}_king.png"
                
                piece_image = pygame.image.load(image_file).convert_alpha()  
                piece_image = pygame.transform.scale(piece_image, (square, square))
                screen.blit(piece_image, rect)  
    # Nếu vua bị chiếu, vẽ viền đỏ quanh ô vua
    white_king_pos = board.get_king_position('white')
    black_king_pos = board.get_king_position('black')

    # Kiểm tra nếu vua trắng bị chiếu
    if board.is_in_check('white') and white_king_pos:
        r, c = white_king_pos
        rect = pygame.Rect(c * square, r * square, square, square)
        pygame.draw.rect(screen, (255, 0, 0), rect, 5)  # Vẽ viền đỏ cho ô vua trắng bị chiếu

    # Kiểm tra nếu vua đen bị chiếu
    if board.is_in_check('black') and black_king_pos:
        r, c = black_king_pos
        rect = pygame.Rect(c * square, r * square, square, square)
        pygame.draw.rect(screen, (255, 0, 0), rect, 5)  # Vẽ viền đỏ cho ô vua đen bị chiếu


board = Board()  # Khởi tạo bàn cờ
running = True
while running:
    
    
    
    # Kiểm tra thời gian đã trôi qua
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= time_limit:
        # Nếu đã hết thời gian, dừng trò chơi
        print("Hết thời gian! Trò chơi kết thúc.")
        running = False  # Thoát vòng lặp_start_time

    
    # Xử lý sự kiện người dùng
    if turn == player_color:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False; pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if x < WIDTH - 160:
                    row, col = y//((WIDTH - 160)//8), x//(HEIGHT//8)
                    if selected:
                        # Nếu đã chọn quân, và click vào ô trong nước đi hợp lệ -> di chuyển
                        if (row,col) in valid_moves:
                            board.move_piece((selected,(row,col)))
                            turn = 'black' if turn=='white' else 'white'
                            move_sound.play() 
                        selected = None; valid_moves = []
                    else:
                        # Chọn quân của mình
                        p = board.board[row][col]
                        if p and p.color == turn:
                            selected = (row,col)
                            # Lấy các nước đi hợp lệ của quân đó
                            moves = board.get_all_moves(turn)
                            valid_moves = [dest for (src,dest) in moves if src==selected]
    else:
        # Lượt AI đi
        score, move = minimax(board, 3, -math.inf, math.inf, turn=='white')
        if move:
            board.move_piece(move)
        else:
            print("Hết nước đi. Kết thúc trò chơi.")
            running = False
        turn = 'black' if turn=='white' else 'white'
    
    # Vẽ khu vực tính điểm và thời gian
    screen.fill((0, 0, 0))  # Đặt màu nền cho màn hình là đen

    # Vẽ khu vực bàn cờ (bên trái màn hình)
    board_rect = pygame.Rect(0, 0, WIDTH - 160, HEIGHT)
    pygame.draw.rect(screen, (255, 255, 255), board_rect)  # Nền trắng cho bàn cờ
    draw_board()  # Vẽ bàn cờ trong khu vực này

    # Vẽ khu vực hiển thị thời gian và điểm số (bên phải màn hình)
    info_rect = pygame.Rect(WIDTH - 160, 0, 200, HEIGHT)
    pygame.draw.rect(screen, (50, 50, 50), info_rect)  # Nền xám cho khu vực hiển thị

    # Hiển thị thời gian đã trôi qua (Tính bằng phút:giây)
    elapsed_minutes = elapsed_time // 60000  # Tính phút
    elapsed_seconds = (elapsed_time % 60000) // 1000  # Tính giây
    time_text = f"Time: {elapsed_minutes:02}:{elapsed_seconds:02}"
    
    # Hiển thị thời gian ngoài màn hình (ở khu vực bên phải)
    time_surface = font.render(time_text, True, (255, 255, 255))
    screen.blit(time_surface, (WIDTH - 160, 20))  # Hiển thị thời gian ở góc trên bên phải của khu vực hiển thị

    pygame.display.flip()
    pygame.time.Clock().tick(60)