import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { neon } from "@neondatabase/serverless";
import { Kysely } from "kysely";
import { NeonDialect } from "kysely-neon";
import { toNextJsHandler } from "better-auth/next-js";

// Create Kysely instance with Neon dialect
const db = new Kysely({
    dialect: new NeonDialect({
        neon: neon(process.env.DATABASE_URL!),
    }),
});

export const auth = betterAuth({
    database: {
        provider: "pg",
        db,
        schema: {
            user: "auth_user",
            account: "auth_account",
            session: "auth_session",
            verification: "auth_verification",
        }
    },
    plugins: [
        jwt()
    ],
    emailAndPassword: {
        enabled: true
    },
    basePath: "/api/auth",
    baseURL: (process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000").replace(/\/$/, "") // Remove trailing slash
});

export const { GET, POST } = toNextJsHandler(auth);
