package com.acme.users;

public final class User {
    private final long id;
    private final String email;
    private final String displayName; // may be null

    public User(long id, String email, String displayName) {
        this.id = id;
        this.email = email;
        this.displayName = displayName;
    }

    public long getId() { return id; }
    public String getEmail() { return email; }
    public String getDisplayName() { return displayName; }

    @Override public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof User)) return false;
        User u = (User) o;
        return id == u.id && email.equals(u.email);
    }

    @Override public int hashCode() { return Long.hashCode(id) * 31 + email.hashCode(); }

    @Override public String toString() { return "User#" + id; }
}
