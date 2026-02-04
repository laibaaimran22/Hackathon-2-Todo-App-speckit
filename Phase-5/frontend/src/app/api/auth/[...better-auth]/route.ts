import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { neon } from "@neondatabase/serverless";
import { Kysely } from "kysely";
import { NeonDialect } from "kysely-neon";
import { toNextJsHandler } from "better-auth/next-js";

const databaseUrl = process.env.DATABASE_URL;

let GET: (request: Request) => Promise<Response>;
let POST: (request: Request) => Promise<Response>;

if (!databaseUrl) {
    const handler = async () =>
        new Response("DATABASE_URL is not configured", { status: 500 });

    GET = handler;
    POST = handler;
} else {
    // Create Kysely instance with Neon dialect
    const db = new Kysely({
        dialect: new NeonDialect({
            neon: neon(databaseUrl),
        }),
    });

    const auth = betterAuth({
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
        baseURL: (process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000").replace(/\/$/, "")
    });

    const handlers = toNextJsHandler(auth);
    GET = handlers.GET;
    POST = handlers.POST;
}

export { GET, POST };
