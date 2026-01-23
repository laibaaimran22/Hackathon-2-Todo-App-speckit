import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

async function fixUserTable() {
  console.log("Fixing user table schema...\n");

  try {
    // Add missing columns to user table
    await sql`
      ALTER TABLE "user"
      ADD COLUMN IF NOT EXISTS email_verified BOOLEAN NOT NULL DEFAULT FALSE
    `;
    console.log("✓ Added email_verified column");

    await sql`
      ALTER TABLE "user"
      ADD COLUMN IF NOT EXISTS name TEXT
    `;
    console.log("✓ Added name column");

    await sql`
      ALTER TABLE "user"
      ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT NOW()
    `;
    console.log("✓ Added updated_at column");

    // Ensure email is unique
    await sql`
      DO $$
      BEGIN
        IF NOT EXISTS (
          SELECT 1 FROM pg_constraint
          WHERE conname = 'user_email_key'
        ) THEN
          ALTER TABLE "user" ADD CONSTRAINT user_email_key UNIQUE (email);
        END IF;
      END $$
    `;
    console.log("✓ Ensured email uniqueness constraint");

    console.log("\n✅ User table fixed successfully!");
  } catch (error) {
    console.error("❌ Fix failed:", error);
    process.exit(1);
  }
}

fixUserTable();
