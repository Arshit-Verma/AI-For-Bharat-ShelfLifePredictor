import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'ShelfLife AI - Smart Food Safety Predictor',
  description: 'AI-powered food shelf life prediction with expert recommendations and voice explanations',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
