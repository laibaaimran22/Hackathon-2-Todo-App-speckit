import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

async function addJwksTable() {
  console.log("Creating jwks table for JWT plugin...\n");

  try {
    await sql`
      CREATE TABLE IF NOT EXISTS jwks (
        id TEXT PRIMARY KEY,
        "publicKey" TEXT NOT NULL,
        "privateKey" TEXT NOT NULL,
        "createdAt" TIMESTAMP NOT NULL DEFAULT NOW()
      )
    `;
    console.log("✓ Created jwks table");

    console.log("\n✅ JWKS table created successfully!");
  } catch (error) {
    console.error("❌ Creation failed:", error);
    process.exit(1);
  }
}

addJwksTable();
