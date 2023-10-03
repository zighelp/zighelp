test "{{ for_loop }}" {
    // {{ character_equivalent_to_integer }}
    const string = [_]u8{ 'a', 'b', 'c' };

    for (string, 0..) |character, index| {
        _ = character; {{ character_comment }}
        _ = index; {{ index_comment }}
    }

    for (string) |character| {
        _ = character;
    }

    for (string, 0..) |_, index| {
        _ = index;
    }

    for (string) |_| {}
}