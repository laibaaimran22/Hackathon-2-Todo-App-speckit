import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { neon } from "@neondatabase/serverless";
import { Kysely } from "kysely";
import { NeonDialect } from "kysely-neon";

// Create Kysely instance with Neon dialect
const db = new Kysely({
    dialect: new NeonDialect({
        neon: neon(process.env.DATABASE_URL!),
    }),
});

export const auth = betterAuth({
    database: {
        provider: "pg",
        db: db as any,
    },
    plugins: [
        jwt({
            secret: process.env.JWT_SECRET || "development-secret-key-change-me",
        } as any)
    ],
    emailAndPassword: {
        enabled: true
    },
    basePath: "/api/auth",
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"
});
