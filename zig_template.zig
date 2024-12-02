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
    return 0;
}

fn second(allocator: std.mem.Allocator, lines: [][]const u8) !i32 {
    return 0;
}
