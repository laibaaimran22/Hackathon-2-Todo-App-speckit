import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

async function verifyTables() {
  console.log("Verifying database tables...\n");

  try {
    const tables = await sql`
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
      AND table_type = 'BASE TABLE'
      ORDER BY table_name
    `;

    console.log("Found tables:");
    tables.forEach((table: any) => {
      console.log(`  ✓ ${table.table_name}`);
    });

    // Check user table columns
    console.log("\n'user' table columns:");
    const userColumns = await sql`
      SELECT column_name, data_type, is_nullable
      FROM information_schema.columns
      WHERE table_name = 'user'
      ORDER BY ordinal_position
    `;

    userColumns.forEach((col: any) => {
      console.log(`  - ${col.column_name} (${col.data_type}) ${col.is_nullable === 'NO' ? 'NOT NULL' : 'NULL'}`);
    });

    console.log("\n✅ Database verification complete!");
  } catch (error) {
    console.error("❌ Verification failed:", error);
    process.exit(1);
  }
}

verifyTables();
