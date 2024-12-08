const std = @import("std");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const buffer = try std.fs.cwd().readFileAlloc(allocator, "input.txt", 1024 * 1024);

    var lines = std.ArrayList([]const u8).init(allocator);
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
    var total: i32 = 0;

    var parsing_rules = true;
    var rules = std.ArrayList(Rule).init(allocator);
    for (lines) |line| {
        if (parsing_rules) {
            if (line.len == 0) {
                parsing_rules = false;
            } else {
                var iter = std.mem.split(u8, line, "|");
                try rules.append(Rule{
                    .before = std.fmt.parseInt(i32, iter.first(), 10) catch unreachable,
                    .after = std.fmt.parseInt(i32, (iter.next() orelse unreachable), 10) catch unreachable,
                });
            }
            continue;
        }

        var numbers = std.ArrayList(i32).init(allocator);
        var iter = std.mem.split(u8, line, ",");
        while (iter.next()) |number| {
            const n = try std.fmt.parseInt(i32, number, 10);
            try numbers.append(n);
        }

        if (isValid(rules.items, numbers.items)) {
            const middle = @divTrunc(numbers.items.len, 2);
            // std.debug.print("{s} [{d}]\n", .{ line, numbers.items[middle] });
            total += numbers.items[middle];
        }
    }
    return total;
}

fn second(allocator: std.mem.Allocator, lines: [][]const u8) !i32 {
    var total: i32 = 0;

    var parsing_rules = true;
    var rules = std.ArrayList(Rule).init(allocator);
    for (lines) |line| {
        if (parsing_rules) {
            if (line.len == 0) {
                parsing_rules = false;
            } else {
                var iter = std.mem.split(u8, line, "|");
                try rules.append(Rule{
                    .before = std.fmt.parseInt(i32, iter.first(), 10) catch unreachable,
                    .after = std.fmt.parseInt(i32, (iter.next() orelse unreachable), 10) catch unreachable,
                });
            }
            continue;
        }

        var numbers = std.ArrayList(i32).init(allocator);
        var iter = std.mem.split(u8, line, ",");
        while (iter.next()) |number| {
            const n = try std.fmt.parseInt(i32, number, 10);
            try numbers.append(n);
        }

        if (!isValid(rules.items, numbers.items)) {
            const context = Context{ .rules = rules.items, .numbers = numbers.items };
            std.mem.sort(i32, numbers.items, context, Context.lessThan);

            const middle = @divTrunc(numbers.items.len, 2);
            // std.debug.print("{} [{d}]\n", .{ numbers, numbers.items[middle] });
            total += numbers.items[middle];
        }
    }
    return total;
}

fn isValid(rules: []const Rule, numbers: []const i32) bool {
    for (rules) |rule| {
        const before_index = std.mem.indexOfScalar(i32, numbers, rule.before) orelse continue;
        const after_index = std.mem.indexOfScalar(i32, numbers, rule.after) orelse continue;

        if (before_index > after_index) {
            return false;
        }
    }
    return true;
}

const Context = struct {
    rules: []Rule,
    numbers: []i32,

    fn lessThan(self: Context, lhs: i32, rhs: i32) bool {
        for (self.rules) |rule| {
            if (rule.before == lhs and rule.after == rhs) {
                return true;
            }
            if (rule.before == rhs and rule.after == lhs) {
                return false;
            }
        }
        return false;
    }
};

const Rule = struct { before: i32, after: i32 };
