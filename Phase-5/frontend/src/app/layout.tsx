import type { Metadata } from "next";
import "./globals.css";
import { Toaster } from "sonner";

export const metadata: Metadata = {
  title: "Todo Evolution - Phase 5",
  description: "Advanced cloud todo application with event-driven architecture",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
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