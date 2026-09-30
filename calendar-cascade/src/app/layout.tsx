import type { Metadata } from 'next';
import { Inter_Tight, JetBrains_Mono } from 'next/font/google';
import './globals.css';

const inter = Inter_Tight({ subsets: ['latin'], variable: '--font-inter-tight' });
const mono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-jetbrains-mono' });

export const metadata: Metadata = {
  title: 'Calendar Cascade',
  description: 'Keep every calendar blocked: cascade events, blocks and buffers across Google calendars.',
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${mono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
