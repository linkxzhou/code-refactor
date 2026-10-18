package com.acme.users;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

public final class UserIndex {
    private UserIndex() {}

    /** Throws IllegalStateException when two users share an email (data error upstream). */
    public static Map<String, User> byEmail(List<User> users) {
        return users.stream().collect(Collectors.toMap(u -> u.getEmail().toLowerCase(), Function.identity()));
    }

    /** Returns null when the user is unknown or has no display name. */
    public static String findName(Map<String, User> index, String email) {
        User u = index.get(email.toLowerCase());
        return u == null ? null : u.getDisplayName();
    }

    public static List<User> load(Path csv) throws IOException {
        return Files.readAllLines(csv).stream()
                .skip(1)
                .map(line -> line.split(",", -1))
                .map(f -> new User(Long.parseLong(f[0]), f[1], f[2].isEmpty() ? null : f[2]))
                .collect(Collectors.toList());
    }
}
