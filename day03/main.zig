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

fn second(_: std.mem.Allocator, lines: [][]const u8) !i32 {
    var total: i32 = 0;
    for (lines) |line| {
        var found = lookFirstOfPos(line, 0);
        var is_valid = true;
        while (found) |value| {
            // std.debug.print("{d}\n", .{value.pos});
            var new_pos: usize = undefined;
            switch (value.value) {
                .mult => {
                    if (is_valid) {
                        if (getNumbers(line, value.pos + SearchType.mult.str().len)) |numbers| {
                            total += numbers.first * numbers.second;
                            // std.debug.print("{}\n", .{numbers});
                            new_pos = numbers.pos;
                        } else {
                            new_pos = value.pos + 1;
                        }
                    } else {
                        new_pos = value.pos + 1;
                    }
                },
                .do => {
                    is_valid = true;
                    // std.debug.print("{}\n", .{is_valid});
                    new_pos = value.pos;
                },
                .do_not => {
                    is_valid = false;
                    //                     std.debug.print("{}\n", .{is_valid});
                    new_pos = value.pos;
                },
            }

            // for (line) |l| {
            //     std.debug.print("{c:>3}", .{l});
            // }
            // std.debug.print("\n", .{});
            // for (0..line.len) |i| {
            //     std.debug.print("{d:>3}", .{i});
            // }
            // std.debug.print("\n", .{});
            // std.debug.print("{d}\n", .{new_pos});

            found = lookFirstOfPos(line, new_pos);
        }
    }
    return total;
}

fn lookFirstOfPos(line: []const u8, start: usize) ?struct { value: SearchType, pos: usize } {
    const x = std.mem.indexOfPos(
        u8,
        line,
        start,
        SearchType.mult.str(),
    ) orelse line.len - 1;
    const y = std.mem.indexOfPos(
        u8,
        line,
        start,
        SearchType.do_not.str(),
    ) orelse line.len - 1;
    const z = std.mem.indexOfPos(
        u8,
        line,
        start,
        SearchType.do.str(),
    ) orelse line.len - 1;

    const m = @min(x, @min(y, z));
    if (m == line.len - 1) {
        return null;
    }
    std.debug.print("{d} {d} {d} min {d}\n", .{ x, y, z, m });

    if (x == m) {
        return .{ .value = .mult, .pos = x };
    }
    if (y == m) { // do an don't overlap so can start at same position
        return .{ .value = .do_not, .pos = y + SearchType.do_not.str().len + 1 };
    }
    if (z == m) {
        return .{ .value = .do, .pos = z + SearchType.do.str().len + 1 };
    }

    return null;

    // if (x < y and x < z) {
    //     return .{ .value = .mult, .pos = x };
    // }
    // if (y < x and y < z) { // do an don't overlap so can start at same position
    //     return .{ .value = .do_not, .pos = y + SearchType.do_not.str().len };
    // }
    // if (z < x and z < y) {
    //     return .{ .value = .do, .pos = z + SearchType.do.str().len };
    // }

    // return null;
}

const SearchType = enum {
    mult,
    do,
    do_not,

    pub fn str(self: SearchType) []const u8 {
        return switch (self) {
            .mult => "mul(",
            .do => "do()",
            .do_not => "don't()",
        };
    }
};
