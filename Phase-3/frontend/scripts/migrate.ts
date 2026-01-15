import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

async function migrate() {
  console.log("Starting database migration...");

  try {
    // Create user table for Better Auth
    await sql`
      CREATE TABLE IF NOT EXISTS "user" (
        id TEXT PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        email_verified BOOLEAN NOT NULL DEFAULT FALSE,
        name TEXT,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
      )
    `;
    console.log("✓ Created user table");

    // Create session table for Better Auth
    await sql`
      CREATE TABLE IF NOT EXISTS "session" (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
        expires_at TIMESTAMP NOT NULL,
        token TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
      )
    `;
    console.log("✓ Created session table");

    // Create account table for Better Auth (for OAuth and password)
    await sql`
      CREATE TABLE IF NOT EXISTS "account" (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
        account_id TEXT NOT NULL,
        provider_id TEXT NOT NULL,
        access_token TEXT,
        refresh_token TEXT,
        id_token TEXT,
        access_token_expires_at TIMESTAMP,
        refresh_token_expires_at TIMESTAMP,
        scope TEXT,
        password TEXT,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
        UNIQUE(provider_id, account_id)
      )
    `;
    console.log("✓ Created account table");

    // Create verification table for Better Auth
    await sql`
      CREATE TABLE IF NOT EXISTS "verification" (
        id TEXT PRIMARY KEY,
        identifier TEXT NOT NULL,
        value TEXT NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
      )
    `;
    console.log("✓ Created verification table");

    console.log("\n✅ Migration completed successfully!");
  } catch (error) {
    console.error("❌ Migration failed:", error);
    process.exit(1);
  }
}

migrate();
