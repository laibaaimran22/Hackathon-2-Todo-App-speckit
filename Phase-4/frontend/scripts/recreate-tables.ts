import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

async function recreateTables() {
  console.log("Recreating database tables with camelCase columns...\n");

  try {
    // Drop existing tables
    console.log("Dropping existing tables...");
    await sql`DROP TABLE IF EXISTS verification CASCADE`;
    await sql`DROP TABLE IF EXISTS account CASCADE`;
    await sql`DROP TABLE IF EXISTS session CASCADE`;
    await sql`DROP TABLE IF EXISTS "user" CASCADE`;
    console.log("✓ Dropped old tables\n");

    // Create user table with camelCase
    await sql`
      CREATE TABLE "user" (
        id TEXT PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        "emailVerified" BOOLEAN NOT NULL DEFAULT FALSE,
        name TEXT,
        "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
        "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
      )
    `;
    console.log("✓ Created user table");

    // Create session table
    await sql`
      CREATE TABLE session (
        id TEXT PRIMARY KEY,
        "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
        "expiresAt" TIMESTAMP NOT NULL,
        token TEXT NOT NULL UNIQUE,
        "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
        "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
      )
    `;
    console.log("✓ Created session table");

    // Create account table
    await sql`
      CREATE TABLE account (
        id TEXT PRIMARY KEY,
        "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
        "accountId" TEXT NOT NULL,
        "providerId" TEXT NOT NULL,
        "accessToken" TEXT,
        "refreshToken" TEXT,
        "idToken" TEXT,
        "accessTokenExpiresAt" TIMESTAMP,
        "refreshTokenExpiresAt" TIMESTAMP,
        scope TEXT,
        password TEXT,
        "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
        "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW(),
        UNIQUE("providerId", "accountId")
      )
    `;
    console.log("✓ Created account table");

    // Create verification table
    await sql`
      CREATE TABLE verification (
        id TEXT PRIMARY KEY,
        identifier TEXT NOT NULL,
        value TEXT NOT NULL,
        "expiresAt" TIMESTAMP NOT NULL,
        "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
        "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
      )
    `;
    console.log("✓ Created verification table");

    console.log("\n✅ Tables recreated successfully with camelCase columns!");
  } catch (error) {
    console.error("❌ Recreation failed:", error);
    process.exit(1);
  }
}

recreateTables();
