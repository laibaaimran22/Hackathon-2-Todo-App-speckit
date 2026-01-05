import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

async function checkSchema() {
  console.log("Checking all table schemas...\n");

  const tables = ['user', 'session', 'account', 'verification'];

  for (const tableName of tables) {
    console.log(`\n=== ${tableName} table ===`);
    const columns = await sql`
      SELECT column_name, data_type, is_nullable, column_default
      FROM information_schema.columns
      WHERE table_name = ${tableName}
      ORDER BY ordinal_position
    `;

    columns.forEach((col: any) => {
      console.log(`  ${col.column_name}: ${col.data_type} ${col.is_nullable === 'NO' ? 'NOT NULL' : ''} ${col.column_default ? `DEFAULT ${col.column_default}` : ''}`);
    });
  }
}

checkSchema();
