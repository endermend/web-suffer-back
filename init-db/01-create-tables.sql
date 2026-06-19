CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS "users" (
    "id" uuid NOT NULL DEFAULT uuid_generate_v4(),
    "created_at" timestamp NOT NULL DEFAULT now(),
    "updated_at" timestamp NOT NULL DEFAULT now(),
    "version" bigint NOT NULL DEFAULT 0,
    "email" varchar(255) NOT NULL UNIQUE,
    "password_hash" varchar(255) NOT NULL,
    "role" varchar(255) NOT NULL,
    "status" INTEGER NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "tasks" (
    "id" uuid NOT NULL DEFAULT uuid_generate_v4(),
    "created_at" timestamp NOT NULL DEFAULT now(),
    "updated_at" timestamp NOT NULL DEFAULT now(),
    "version" bigint NOT NULL DEFAULT 0,
    "title" varchar(255) NOT NULL,
    "description" varchar(255) NOT NULL,
    "deadline" timestamp NOT NULL,
    "exp" INTEGER NOT NULL,
    "money" INTEGER NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "users_t" (
    "id" uuid NOT NULL,
    "created_at" timestamp NOT NULL DEFAULT now(),
    "updated_at" timestamp NOT NULL DEFAULT now(),
    "version" bigint NOT NULL DEFAULT 0,
    "exp" INTEGER NOT NULL DEFAULT 0,
    "money" INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY ("id") REFERENCES "users" ("id"),
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "submissions" (
    "id" uuid NOT NULL,
    "created_at" timestamp NOT NULL DEFAULT now(),
    "updated_at" timestamp NOT NULL DEFAULT now(),
    "version" bigint NOT NULL DEFAULT 0,
    "task_id" uuid NOT NULL,
    "user_id" uuid NOT NULL,
    "content" varchar(65535) NOT NULL,
    "file" varchar(255),
    "status" varchar(255) NOT NULL,
    "admin_comment" varchar(65535) NOT NULL,
    FOREIGN KEY ("task_id") REFERENCES "tasks" ("id"),
    FOREIGN KEY ("user_id") REFERENCES "users" ("id"),
    PRIMARY KEY("id")
);

-- Auto-update updated_at (optional, or handle in app)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON users_t
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subms_updated_at
    BEFORE UPDATE ON submissions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();