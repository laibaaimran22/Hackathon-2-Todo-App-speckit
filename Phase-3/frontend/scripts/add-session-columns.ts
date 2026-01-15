import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

async function addSessionColumns() {
  console.log("Adding missing columns to session table...\n");

  try {
    // Add ipAddress column
    await sql`
      ALTER TABLE session
      ADD COLUMN IF NOT EXISTS "ipAddress" TEXT
    `;
    console.log("✓ Added ipAddress column");

    // Add userAgent column
    await sql`
      ALTER TABLE session
      ADD COLUMN IF NOT EXISTS "userAgent" TEXT
    `;
    console.log("✓ Added userAgent column");

    console.log("\n✅ Session table updated successfully!");
  } catch (error) {
    console.error("❌ Update failed:", error);
    process.exit(1);
  }
}

addSessionColumns();
