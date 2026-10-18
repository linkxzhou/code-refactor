package com.acme.users;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

/** Stays in Java for now — must keep compiling unchanged after the port. */
public final class ReportJob {
    public static void main(String[] args) {
        try {
            List<User> users = UserIndex.load(Path.of(args[0]));
            Map<String, User> idx = UserIndex.byEmail(users);
            String name = UserIndex.findName(idx, args[1]);
            System.out.println(name == null ? "(unknown)" : name);
            System.out.println(users.get(0));
        } catch (IOException e) {
            System.err.println("cannot read " + args[0]);
            System.exit(2);
        } catch (IllegalStateException e) {
            System.err.println("duplicate email");
            System.exit(3);
        }
    }
}
