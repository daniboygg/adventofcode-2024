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

    const file = try std.fs.cwd().openFile("input.txt", .{});
    defer file.close();

    const stat = try file.stat();
    const buffer = try file.readToEndAlloc(allocator, stat.size);
    defer allocator.free(buffer);

    var lines = std.ArrayList([]const u8).init(allocator);
    defer lines.deinit();
    var iter = std.mem.split(u8, buffer, "\n");
    while (iter.next()) |line| {
        try lines.append(line);
    }

    var result = try first(allocator, lines.items);
    std.debug.print("Result 1: {d}\n", .{result});

    result = try second(allocator, lines.items);
    std.debug.print("Result 2: {d}\n", .{result});
}

fn first(allocator: std.mem.Allocator, lines: [][]const u8) !i32 {
    var col_1 = std.ArrayList(i32).init(allocator);
    defer col_1.deinit();
    var col_2 = std.ArrayList(i32).init(allocator);
    defer col_2.deinit();

    for (lines) |line| {
        var iter = std.mem.split(u8, line, "   ");
        const f = try std.fmt.parseInt(i32, iter.first(), 10);
        const s = try std.fmt.parseInt(i32, iter.next().?, 10);
        try col_1.append(f);
        try col_2.append(s);
    }

    std.mem.sort(i32, col_1.items, {}, comptime std.sort.asc(i32));
    std.mem.sort(i32, col_2.items, {}, comptime std.sort.asc(i32));

    var total: i32 = 0;
    for (col_1.items, col_2.items) |i_1, i_2| {
        total += @max(i_1, i_2) - @min(i_1, i_2);
    }
    return total;
}

fn second(allocator: std.mem.Allocator, lines: [][]const u8) !i32 {
    var col_1 = std.ArrayList(i32).init(allocator);
    defer col_1.deinit();
    var col_2 = std.ArrayList(i32).init(allocator);
    defer col_2.deinit();

    for (lines) |line| {
        var iter = std.mem.split(u8, line, "   ");
        const f = try std.fmt.parseInt(i32, iter.first(), 10);
        const s = try std.fmt.parseInt(i32, iter.next().?, 10);
        try col_1.append(f);
        try col_2.append(s);
    }

    var counter = std.AutoHashMap(i32, i32).init(allocator);
    defer counter.deinit();
    for (col_2.items) |i| {
        const count = counter.get(i) orelse 0;
        try counter.put(i, count + 1);
    }

    var total: i32 = 0;
    for (col_1.items) |i| {
        total += i * (counter.get(i) orelse 0);
    }
    return total;
}
