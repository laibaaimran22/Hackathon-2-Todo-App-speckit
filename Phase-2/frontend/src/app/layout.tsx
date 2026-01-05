import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { Toaster } from "sonner";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Todo Evolution - Phase 2",
  description: "Spec-driven authenticated todo application",
};

// Suppress Ed25519 experimental crypto warning from Better Auth
if (typeof window !== 'undefined') {
  // Store the original console.error
  const originalError = console.error.bind(console);

  // Override console.error to filter out the warning
  console.error = function (...args: unknown[]) {
    // Filter out Ed25519 and other crypto warnings
    const message = args[0];
    if (
      typeof message === 'string' &&
      (message.includes('Ed25519') ||
       message.includes('crypto') ||
       message.includes('experimental') ||
       message.includes('Web Crypto API'))
    ) {
      return;
    }
    originalError(...args);
  };
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
        <Toaster
          position="top-center"
          richColors
          closeButton
          toastOptions={{
            className: 'backdrop-blur-xl bg-white/10 border border-white/20 text-white',
          }}
        />
      </body>
    </html>
  );
}
