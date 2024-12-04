const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    defer {
        const check = gpa.deinit();
        switch (check) {
            .leak => {
                std.debug.print("Memory leak detected!\n", .{});
            },
            .ok => {},
        }
    }

    const buffer = try std.fs.cwd().readFileAlloc(allocator, "input.txt", 1024 * 1024);
    defer allocator.free(buffer);

    var lines = std.ArrayList([]const u8).init(allocator);
    defer lines.deinit();
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
    for (lines) |line| {
        const search = "mul(";

        var mult_pos = std.mem.indexOfPos(u8, line, 0, search);
        while (mult_pos) |value| {
            const new_start = value + search.len;
            const numbers = getNumbers(line, new_start) orelse {
                mult_pos = std.mem.indexOfPos(u8, line, new_start, search);
                continue;
            };

            total += numbers.first * numbers.second;

            mult_pos = std.mem.indexOfPos(u8, line, new_start, search);
        }
    }
    return total;
}

fn second(_: std.mem.Allocator, lines: [][]const u8) !i32 {
    var total: i32 = 0;
    var enabled = true;
    for (lines) |line| {
        var pos: usize = 0;
        while (pos < line.len) {
            const dont_pos = std.mem.indexOfPos(u8, line, pos, "don't()") orelse line.len;
            const do_pos = std.mem.indexOfPos(u8, line, pos, "do()") orelse line.len;
            const mul_pos = std.mem.indexOfPos(u8, line, pos, "mul(") orelse line.len;

            const min = @min(dont_pos, @min(do_pos, mul_pos));
            if (dont_pos == min) {
                pos = dont_pos;
                enabled = false;
                pos += "don't()".len;
                continue;
            }
            if (do_pos == min) {
                pos = do_pos;
                enabled = true;
                pos += "do()".len;
                continue;
            }
            if (enabled and mul_pos == min) {
                pos = mul_pos;
                if (getNumbers(line, pos + "mul(".len)) |result| {
                    total += result.first * result.second;
                    pos = result.pos;
                    continue;
                }
                pos += "mul(".len;
                continue;
            }

            pos += 1;
        }
    }
    return total;
}

fn getNumbers(line: []const u8, start: usize) ?struct { first: i32, second: i32, pos: usize } {
    var last_position = std.mem.indexOfPos(u8, line, start, ",") orelse return null;
    var number_str = line[start..last_position];
    const f = std.fmt.parseInt(i32, number_str, 10) catch return null;
    if (f > 999 or f < 0) {
        std.debug.print("{d}\n", .{f});
    }

    const next_start = last_position + 1;
    last_position = std.mem.indexOfPos(u8, line, next_start, ")") orelse return null;
    number_str = line[next_start..last_position];
    const s = std.fmt.parseInt(i32, number_str, 10) catch return null;
    if (s > 999 or s < 0) {
        std.debug.print("{d}\n", .{s});
    }

    return .{ .first = f, .second = s, .pos = last_position + 1 };
}
