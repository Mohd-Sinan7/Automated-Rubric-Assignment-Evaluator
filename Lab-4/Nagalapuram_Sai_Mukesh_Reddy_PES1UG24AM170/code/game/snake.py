import pygame

# Turns queued between two moves; enough for a quick "up then left" double tap.
MAX_QUEUED_TURNS = 2

class Snake:
    def __init__(self, x, y, cell_size):
        self.cell_size = cell_size
        # body is a list of (x, y) grid-cell positions, head is body[0]
        self.body = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = (1, 0)  # direction of the last move (moving right)
        self.pending_turns = []  # key presses not yet applied to a move
        self.grow_pending = False

    def set_direction(self, dx, dy):
        # Validate against the last queued turn (or the current heading), not
        # just the current heading: otherwise two quick presses between moves
        # (e.g. Up then Left while moving Right) still reverse into the body.
        last = self.pending_turns[-1] if self.pending_turns else self.direction
        if (dx, dy) == last or (dx, dy) == (-last[0], -last[1]):
            return
        if len(self.pending_turns) < MAX_QUEUED_TURNS:
            self.pending_turns.append((dx, dy))

    def next_head(self):
        # Where the head will be after the next move, without moving.
        dx, dy = self.pending_turns[0] if self.pending_turns else self.direction
        head_x, head_y = self.body[0]
        return (head_x + dx, head_y + dy)

    def move(self):
        new_head = self.next_head()
        if self.pending_turns:
            self.direction = self.pending_turns.pop(0)

        self.body.insert(0, new_head)
        if self.grow_pending:
            self.grow_pending = False
        else:
            self.body.pop()

    def grow(self):
        self.grow_pending = True

    def head_rect(self):
        x, y = self.body[0]
        return pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

    def segment_rects(self):
        return [
            pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            for (x, y) in self.body
        ]

    def collides_with_self(self, cell):
        # The tail moves out of the way on this step unless the snake is
        # growing, so following your own tail closely is not a collision.
        blocking = self.body if self.grow_pending else self.body[:-1]
        return cell in blocking

    def collides_with_wall(self, cell, grid_width, grid_height):
        x, y = cell
        return x < 0 or y < 0 or x >= grid_width or y >= grid_height
