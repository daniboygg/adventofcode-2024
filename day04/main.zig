const std = @import("std");

pub fn main() !void {
    // according to documentation https://ziglang.org/documentation/0.13.0/#Choosing-an-Allocator
    // change the allocator to this makes more sense
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const buffer = try std.fs.cwd().readFileAlloc(allocator, "input.txt", 1024 * 1024);
    defer allocator.free(buffer);

    var lines = std.ArrayList([]const u8).init(allocator);
    var iter = std.mem.split(u8, buffer, "\n");
    while (iter.next()) |line| {
        if (line.len == 0) {
            continue;
        }
        try lines.append(line);
    }

    var result = try first(allocator, lines.items);
    std.debug.print("Result 1: {d}\n", .{result});

    result = try second(allocator, lines.items);
    std.debug.print("Result 2: {d}\n", .{result});
}

fn first(_: std.mem.Allocator, lines: [][]const u8) !i32 {
    var total: i32 = 0;
    for (0..lines.len) |row| {
        for (0..lines[row].len) |col| {
            std.debug.assert(lines.len == lines[row].len);
            if (lines[row][col] == 'X') {
                const current = Pos{ .row = @intCast(row), .col = @intCast(col) };

                inline for (@typeInfo(Direction).Enum.fields) |field| {
                    if (searchWordInDirection(lines, current, lines.len, @enumFromInt(field.value))) {
                        total += 1;
                    }
                }
            }
        }
    }

    return total;
}

fn searchWordInDirection(lines: [][]const u8, start: Pos, size: usize, direction: Direction) bool {
    var word = [4]u8{ 'X', ' ', ' ', ' ' };
    for (1..4) |multiplier| {
        const new_pos = start.move(direction, @intCast(multiplier), size) orelse {
            return false;
        };
        const new_char = lines[@intCast(new_pos.row)][@intCast(new_pos.col)];
        word[multiplier] = new_char;

        switch (multiplier) {
            1 => {
                if (!std.mem.eql(u8, word[0..], "XM  ")) {
                    return false;
                }
            },
            2 => {
                if (!std.mem.eql(u8, word[0..], "XMA ")) {
                    return false;
                }
            },
            3 => {
                if (!std.mem.eql(u8, word[0..], "XMAS")) {
                    return false;
                }
            },
            else => unreachable,
        }
    }
    return true;
}

fn second(_: std.mem.Allocator, lines: [][]const u8) !i32 {
    var total: i32 = 0;
    for (1..lines.len - 1) |row| {
        for (1..lines[row].len - 1) |col| {
            std.debug.assert(lines.len == lines[row].len);
            if (lines[row][col] == 'A') {
                const current = Pos{ .row = @intCast(row), .col = @intCast(col) };
                if (isDiagonalCross(lines, current, lines.len)) {
                    total += 1;
                }
            }
        }
    }

    return total;
}

fn isDiagonalCross(lines: [][]const u8, start: Pos, size: usize) bool {
    const start_cross = Pos{ .row = 1, .col = 1 };
    for (crosses) |cross| {
        const directions = [_]Direction{ .left_up, .right_up, .right_down, .left_down };

        var is_cross = true;
        for (directions) |direction| {
            const lines_pos = start.move(direction, 1, size) orelse {
                return false;
            };
            const cross_pos = start_cross.move(direction, 1, 3) orelse {
                return false;
            };
            if (lines[@intCast(lines_pos.row)][@intCast(lines_pos.col)] != cross[@intCast(cross_pos.row)][@intCast(cross_pos.col)]) {
                is_cross = false;
            }
        }
        if (is_cross) {
            return true;
        }
    }

    return false;
}

const crosses = [4][3][3]u8{
    [3][3]u8{
        [3]u8{ 'M', '.', 'S' },
        [3]u8{ '.', 'A', '.' },
        [3]u8{ 'M', '.', 'S' },
    },
    [3][3]u8{
        [3]u8{ 'M', '.', 'M' },
        [3]u8{ '.', 'A', '.' },
        [3]u8{ 'S', '.', 'S' },
    },
    [3][3]u8{
        [3]u8{ 'S', '.', 'M' },
        [3]u8{ '.', 'A', '.' },
        [3]u8{ 'S', '.', 'M' },
    },
    [3][3]u8{
        [3]u8{ 'S', '.', 'S' },
        [3]u8{ '.', 'A', '.' },
        [3]u8{ 'M', '.', 'M' },
    },
};

const Pos = struct {
    row: i32,
    col: i32,

    pub fn move(self: Pos, direction: Direction, multiplier: i32, size: usize) ?Pos {
        switch (direction) {
            .up => {
                if (self.row - 1 * multiplier < 0) {
                    return null;
                }
                return Pos{ .row = self.row - 1 * multiplier, .col = self.col };
            },
            .right_up => {
                if (self.row - 1 * multiplier < 0) {
                    return null;
                }
                if (self.col + 1 * multiplier > size - 1) {
                    return null;
                }
                return Pos{ .row = self.row - 1 * multiplier, .col = self.col + 1 * multiplier };
            },
            .right => {
                if (self.col + 1 * multiplier > size - 1) {
                    return null;
                }
                return Pos{ .row = self.row, .col = self.col + 1 * multiplier };
            },
            .right_down => {
                if (self.row + 1 * multiplier > size - 1) {
                    return null;
                }
                if (self.col + 1 * multiplier > size - 1) {
                    return null;
                }
                return Pos{ .row = self.row + 1 * multiplier, .col = self.col + 1 * multiplier };
            },
            .down => {
                if (self.row + 1 * multiplier > size - 1) {
                    return null;
                }
                return Pos{ .row = self.row + 1 * multiplier, .col = self.col };
            },
            .left_down => {
                if (self.row + 1 * multiplier > size - 1) {
                    return null;
                }
                if (self.col - 1 * multiplier < 0) {
                    return null;
                }
                return Pos{ .row = self.row + 1 * multiplier, .col = self.col - 1 * multiplier };
            },
            .left => {
                if (self.col - 1 * multiplier < 0) {
                    return null;
                }
                return Pos{ .row = self.row, .col = self.col - 1 * multiplier };
            },
            .left_up => {
                if (self.row - 1 * multiplier < 0) {
                    return null;
                }
                if (self.col - 1 * multiplier < 0) {
                    return null;
                }
                return Pos{ .row = self.row - 1 * multiplier, .col = self.col - 1 * multiplier };
            },
        }
    }
};

const Direction = enum {
    up,
    right_up,
    right,
    right_down,
    down,
    left_down,
    left,
    left_up,
};
