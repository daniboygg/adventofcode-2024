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
        for (0..line.len - search.len - 1) |i| {
            const slice = line[i .. i + search.len];
            if (std.mem.eql(u8, slice, search)) {
                const number_position1 = get_next_number(
                    line,
                    i + search.len,
                    ',',
                ) catch continue;
                const number_position2 = get_next_number(
                    line,
                    number_position1.next_position + 1,
                    ')',
                ) catch continue;

                total += number_position1.number * number_position2.number;
            }
        }
    }
    return total;
}

fn get_next_number(line: []const u8, start: usize, until: u8) !struct { number: i32, next_position: usize } {
    const next_position = get_next_position(line, start, until);
    const number_str1 = line[start..next_position];
    // std.debug.print("number str {s}\n", .{number_str1});
    const number = try std.fmt.parseInt(i32, number_str1, 10);
    return .{ .number = number, .next_position = next_position };
}

fn get_next_position(line: []const u8, start: usize, char: u8) usize {
    var position = start;
    while (line[position] != char) {
        position += 1;
    }
    return position;
}

fn second(_: std.mem.Allocator, _: [][]const u8) !i32 {
    return 0;
}
