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
        var iter = std.mem.split(u8, line, " ");
        var last_number = try std.fmt.parseInt(i32, iter.first(), 10);

        var last_diff: i32 = 0;
        var is_valid = false;
        while (iter.next()) |next| {
            is_valid = false;

            const number = try std.fmt.parseInt(i32, next, 10);
            const diff = number - last_number;
            if (last_diff != 0) {
                if (last_diff > 0 and diff < 0) {
                    break;
                }
                if (last_diff < 0 and diff > 0) {
                    break;
                }
            }
            last_number = number;
            if (@abs(diff) <= 0 or @abs(diff) > 3) {
                break;
            }
            is_valid = true;
            last_diff = diff;
        }
        if (is_valid) {
            total += 1;
        }
    }

    return total;
}

fn second(_: std.mem.Allocator, lines: [][]const u8) !i32 {
    var total: i32 = 0;
    const BUFFER_SIZE = 20;
    for (lines) |line| {
        var buffer: [BUFFER_SIZE]i32 = undefined;
        var count: usize = 0;

        var iter = std.mem.split(u8, line, " ");
        while (iter.next()) |next| {
            const n = try std.fmt.parseInt(i32, next, 10);
            buffer[count] = n;
            count += 1;
        }
        const buffer_slice = buffer[0..count];

        if (isValidLine(buffer_slice)) {
            total += 1;
            continue;
        }

        var subset_buffer: [BUFFER_SIZE]i32 = undefined;
        for (0..buffer_slice.len) |skip_index| {
            var count_subset: usize = 0;
            for (buffer_slice, 0..) |value, i| {
                if (i == skip_index) {
                    continue;
                }
                subset_buffer[count_subset] = value;
                count_subset += 1;
            }
            const subset_slice = subset_buffer[0..count_subset];

            if (isValidLine(subset_slice)) {
                total += 1;
                break;
            }
        }
    }

    return total;
}

fn isValidLine(line: []const i32) bool {
    var last_diff: i32 = 0;
    var last_number = line[0];
    for (line[1..line.len]) |next| {
        const diff = last_number - next;
        if (last_diff != 0) {
            if (last_diff > 0 and diff < 0) {
                return false;
            }
            if (last_diff < 0 and diff > 0) {
                return false;
            }
        }
        last_number = next;
        if (@abs(diff) <= 0 or @abs(diff) > 3) {
            return false;
        }
        last_diff = diff;
    }
    return true;
}
